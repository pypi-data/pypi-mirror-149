from watergrid.pipelines.pipeline import Pipeline


class StandalonePipeline(Pipeline):
    """
    A composable pipeline that runs on a single host. Provides no high availability or fault tolerance.

    :param name: The name of the pipeline.
    :type name: str
    """

    def __init__(self, pipeline_name: str):
        super().__init__(pipeline_name)
