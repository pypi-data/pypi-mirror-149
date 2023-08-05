class ContextMetadata:
    def __init__(self, last_pipeline_run_timestamp=None):
        self._last_pipeline_run = last_pipeline_run_timestamp

    def get_last_pipeline_run(self) -> float:
        """
        Gets the timestamp of the last pipeline run. The time represents the current time when the last step finished.
        :return: Timestamp of last pipeline run.
        """
        return self._last_pipeline_run
