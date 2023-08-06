import base64
import copy
import time
from abc import ABC

import pycron

from watergrid.context import DataContext, OutputMode, ContextMetadata
from watergrid.metrics.MetricsStore import MetricsStore
from watergrid.pipelines.pipeline_verifier import PipelineVerifier
from watergrid.steps import Sequence
from watergrid.steps import Step


class Pipeline(ABC):
    """
    Internal class that represents a pipeline of steps.

    :param pipeline_name: Name of the pipeline.
    :type pipeline_name: str
    """

    def __init__(self, pipeline_name: str):
        self._pipeline_name = pipeline_name
        self._steps = []
        self._metrics_store = MetricsStore()
        self._last_run = None

    def add_step(self, step: Step):
        """
        Add a step to the pipeline.

        :param step: Step to add.
        :type step: Step
        """
        self._steps.append(step)

    def add_steps(self, steps: Sequence):
        """
        Adds a sequence of steps to the pipeline.
        :param steps: Sequence implementation that contains the steps to add.
        :return: None
        """
        for step in steps.export_steps():
            self.add_step(step)

    def run(self):
        """
        Blocking operation that runs all steps in the pipeline once.
        :return: None
        """
        self.verify_pipeline()
        self._metrics_store.start_pipeline_monitoring(self._pipeline_name)
        try:
            self.__run_pipeline_steps()
            self._last_run = time.time()
        except Exception as e:
            self._metrics_store.report_exception(e)
            self._metrics_store.stop_step_monitoring()
        finally:
            self._metrics_store.stop_pipeline_monitoring()

    def run_loop(self):
        """
        Runs the pipeline in a loop. Subsequent executions will run immediately after the previous execution.
        """
        while True:
            self.run()

    def run_scheduled(self, cron_expression: str):
        """
        Runs the pipeline once every time the cron expression matches.

        :param cron_expression: Cron expression to match.
        :type cron_expression: str
        """
        while True:
            if pycron.is_now(cron_expression):
                start_time = time.perf_counter()
                self.run()
                elapsed_time = time.perf_counter() - start_time
                time.sleep(
                    60 - (elapsed_time / 1000)
                )  # Sleep for the remaining time in the minute so that the pipeline does not run multiple times per cron trigger.
            else:
                time.sleep(1)

    def get_step_count(self):
        """
        :return: Number of steps in the pipeline.
        """
        return len(self._steps)

    def get_pipeline_name(self) -> str:
        """
        :return: Name of the pipeline.
        """
        return self._pipeline_name

    def verify_pipeline(self):
        """
        Verifies that the pipeline is valid and that all step dependencies are met.
        :return: None
        """
        PipelineVerifier.verify_pipeline_dependencies_fulfilled(self._steps)
        PipelineVerifier.verify_pipeline_step_ordering(self._steps)

    def add_metrics_exporter(self, exporter):
        """
        Adds a metrics exporter to the pipeline metric store.
        :param exporter: Exporter to add.
        :return: None
        """
        self._metrics_store.add_metrics_exporter(exporter)

    def get_pipeline_guid(self):
        """
        Generates a unique identifier for the pipeline that can be used to
        identify all pipelines that have the same steps in the same order with
        the same name.
        :return: GUID of the pipeline.
        """
        result = self._pipeline_name
        for step in self._steps:
            result += step.get_step_name() + type(step).__name__
        return base64.urlsafe_b64encode(result.encode("utf-8"))

    def __run_pipeline_steps(self):
        """
        Performs setup and runs all steps in the pipeline.
        :return:
        """
        contexts = [self.__generate_first_context()]
        for step in self._steps:
            contexts = self.__run_step_for_each_context(step, contexts)
            if len(contexts) == 0:
                break

    def __generate_first_context(self) -> DataContext:
        """
        Generates the first context for the pipeline.
        :return: First context.
        """
        context = DataContext()
        context_meta = ContextMetadata(self._last_run)
        context.set_run_metadata(context_meta)
        return context

    def __run_step_for_each_context(self, step: Step, context_list: list) -> list:
        """
        Runs the given step once for each context in the context list and performs post-processing.
        :param step: Step to run.
        :param context_list: List of contexts to provide to the step runtime.
        :return: List of contexts to provide to the next step.
        """
        next_contexts = []
        for context in context_list:
            self.__run_step_with_performance_monitoring(step, context)
            self.__process_step_output(context, step.get_step_provides(), next_contexts)
        return next_contexts

    def __process_step_output(
        self, context: DataContext, step_provides: list, next_contexts: list
    ):
        """
        Performs post-processing on the output of a step.
        :param context: Output from the current step.
        :param step_provides: List of data keys that the step provides.
        :param next_contexts: List of contexts that will be passed to the next step.
        :return: None
        """
        if context.get_output_mode() == OutputMode.SPLIT:
            self.__split_context(step_provides, context, next_contexts)
        elif context.get_output_mode() == OutputMode.FILTER:
            self.__filter_context(step_provides, context, next_contexts)
        else:
            self.__forward_context(context, next_contexts)

    def __run_step_with_performance_monitoring(self, step: Step, context: DataContext):
        """
        Runs a single step in the pipeline and forwards performance data to any installed monitoring plugins.
        :param step: Step to run.
        :param context: Context to provide to the step runtime.
        :return: None
        """
        self._metrics_store.start_step_monitoring(step.get_step_name())
        step.run_step(context)
        self._metrics_store.stop_step_monitoring()

    def __split_context(
        self, step_provides: list, context: DataContext, next_contexts: list
    ):
        """
        Splits the context into multiple contexts based on the output of the current step.
        :param step_provides: The list of data keys that the current step provides.
        :param context: The context instance from the current step.
        :param next_contexts: The list of contexts that will be passed to the next step.
        :return: None
        """
        split_key = step_provides[0]
        split_value = context.get(split_key)
        for value in split_value:
            new_context = copy.deepcopy(context)
            new_context.set_output_mode(OutputMode.DIRECT)
            new_context.set(split_key, value)
            next_contexts.append(new_context)

    def __filter_context(
        self, step_provides: list, context: DataContext, next_contexts: list
    ):
        """
        Forwards the context to the next step if the given filter key is present.
        :param step_provides: The list of context keys that the step provides.
        :param context: The context instance from the current step.
        :param next_contexts: The list of contexts that will be passed to the next step.
        :return: None
        """
        if context.get(step_provides[0]) is not None:
            new_context = copy.deepcopy(context)
            new_context.set_output_mode(OutputMode.DIRECT)
            next_contexts.append(new_context)

    def __forward_context(self, context: DataContext, next_contexts: list):
        """
        Forwards the context to the next step with no post-processing.
        :param context: Context to forward.
        :param next_contexts: List of contexts that will be used by the next step.
        :return: None
        """
        next_contexts.append(copy.deepcopy(context))
