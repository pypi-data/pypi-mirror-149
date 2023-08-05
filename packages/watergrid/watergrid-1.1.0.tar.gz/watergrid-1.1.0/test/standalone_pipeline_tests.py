import unittest

from watergrid.pipelines import StandalonePipeline


class StandalonePipelineTestCases(unittest.TestCase):
    def test_can_initialize_pipeline(self):
        pipeline = StandalonePipeline("test_pipeline")
        self.assertEqual(pipeline.get_pipeline_name(), "test_pipeline")
