import logging

from watergrid.metrics.MetricsExporter import MetricsExporter


class ConsoleMetricsExporter(MetricsExporter):
    def __init__(self):
        super().__init__()
        logging.basicConfig(level=logging.INFO)
        self._logger = logging.getLogger(__name__)

    def start_pipeline(self, pipeline_name):
        logging.info("Starting pipeline: " + pipeline_name)

    def end_pipeline(self):
        logging.info("Ending pipeline")

    def start_step(self, step_name):
        logging.info("Starting step: " + step_name)

    def end_step(self):
        logging.info("Ending step")

    def capture_exception(self, exception: Exception):
        logging.error("Exception: " + str(exception))
