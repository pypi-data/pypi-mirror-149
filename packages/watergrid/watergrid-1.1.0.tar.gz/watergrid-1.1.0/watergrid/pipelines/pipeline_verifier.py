from watergrid.steps import Step


class PipelineVerifier:
    @staticmethod
    def verify_pipeline_dependencies_fulfilled(pipeline_steps: list):
        """
        Verifies that all dependencies of the pipeline are fulfilled by at least one other step. Does not check
        validity of step ordering in the pipeline.
        :param pipeline_steps: List of all steps in the pipeline.
        :return: None
        """
        # Get a list of all provided data keys.
        provided_keys = PipelineVerifier.__get_all_step_provides(pipeline_steps)
        # Check that all dependencies are met.
        PipelineVerifier.__check_for_unlinked_dependencies(
            provided_keys, pipeline_steps
        )

    @staticmethod
    def __get_all_step_provides(pipeline_steps: list) -> list:
        """
        Gets a list of all unique keys provided by all steps in the pipeline.
        :param pipeline_steps: List of all steps in the pipeline.
        :return: List of all data keys provided by all steps in the pipeline.
        """
        provided_keys = []
        for step in pipeline_steps:
            provided_keys.extend(
                PipelineVerifier.__get_unique_step_provides(step, provided_keys)
            )
        return provided_keys

    @staticmethod
    def __get_unique_step_provides(step: Step, provided_keys: list) -> list:
        """
        Gets a list of all unique keys provided by a single step.
        :param step: Step to check.
        :param provided_keys: List of all data keys provided by all steps in the pipeline.
        :return: List of all data keys provided by the step.
        """
        new_keys = []
        for key in step.get_step_provides():
            if key not in provided_keys:
                new_keys.append(key)
        return new_keys

    @staticmethod
    def __check_for_unlinked_dependencies(
        provided_keys: list, pipeline_steps: list
    ) -> None:
        """
        Checks that all dependencies of the pipeline are fulfilled by at least one other step. Does not check
        validity of step ordering in the pipeline.
        :param provided_keys: List of all data keys provided by all steps in the pipeline.
        :param pipeline_steps: List of all steps in the pipeline.
        :return: None
        """
        for step in pipeline_steps:
            PipelineVerifier.__check_step_dependencies(step, provided_keys)

    @staticmethod
    def __check_step_dependencies(step: Step, provided_keys: list) -> None:
        """
        Checks that all dependencies of a single step are fulfilled by at least one other step.
        :param step: Step to check.
        :param provided_keys: List of all data keys provided by all steps in the pipeline.
        :return: None
        """
        for step_dependency in step.get_step_requirements():
            if step_dependency not in provided_keys:
                raise Exception(
                    f"Step {step.get_step_name()} requires {step_dependency} to be provided."
                )

    @staticmethod
    def verify_pipeline_step_ordering(pipeline_steps: list) -> None:
        """
        Verifies that all steps in the pipeline are in the correct order.
        :return: None
        """
        # Get a list of all provided data keys.
        provided_keys = []
        step_index = 0
        index_hop_count = 0
        while step_index < len(pipeline_steps):
            index_hop_count += 1
            PipelineVerifier.__recursive_loop_failsafe(
                index_hop_count, len(pipeline_steps)
            )
            if PipelineVerifier.__check_step_position_is_correct(
                pipeline_steps, step_index, provided_keys
            ):
                step_index += 1

    @staticmethod
    def __recursive_loop_failsafe(hop_count: int, total_steps: int) -> None:
        if hop_count > total_steps**2:
            raise Exception("Unable to resolve step dependencies.")

    @staticmethod
    def __check_step_position_is_correct(
        pipeline_steps: list, step_index: int, provided_keys: list
    ) -> bool:
        if not PipelineVerifier.__bump_step_if_dependency_not_met(
            pipeline_steps, step_index, provided_keys
        ):
            provided_keys.extend(
                PipelineVerifier.__get_unique_step_provides(
                    pipeline_steps[step_index], provided_keys
                )
            )
            return True
        return False

    @staticmethod
    def __bump_step_if_dependency_not_met(
        pipeline_steps: list, step_index: int, provided_keys: list
    ) -> bool:
        for step_dependency in pipeline_steps[step_index].get_step_requirements():
            if step_dependency not in provided_keys:
                pipeline_steps.append(pipeline_steps.pop(step_index))
                return True
        return False
