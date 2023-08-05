import unittest

from watergrid.context import DataContext
from watergrid.pipelines.pipeline import Pipeline
from watergrid.steps import Step


class MockStep(Step):
    def __init__(self, name):
        super().__init__(name)

    def run(self, context: DataContext):
        pass


class MockStep2(Step):
    def __init__(self, name):
        super().__init__(name)

    def run(self, context: DataContext):
        pass


class PipelineVersioningTestCase(unittest.TestCase):
    def test_pipeline_has_guid_function(self):
        pipeline = Pipeline("test_pipeline")
        self.assertIsNotNone(pipeline.get_pipeline_guid())

    def test_pipeline_guid_is_unique_by_name(self):
        pipeline1 = Pipeline("test_pipeline1")
        pipeline2 = Pipeline("test_pipeline2")
        self.assertNotEqual(
            pipeline1.get_pipeline_guid(), pipeline2.get_pipeline_guid()
        )

    def test_pipeline_guid_is_unique_by_steps(self):
        pipeline1 = Pipeline("test_pipeline")
        pipeline1.add_step(MockStep("step1"))
        pipeline2 = Pipeline("test_pipeline")
        pipeline2.add_step(MockStep("step2"))
        self.assertNotEqual(
            pipeline1.get_pipeline_guid(), pipeline2.get_pipeline_guid()
        )

    def test_pipeline_guid_is_unique_by_step_class_names(self):
        pipeline1 = Pipeline("test_pipeline")
        pipeline1.add_step(MockStep("step1"))
        pipeline2 = Pipeline("test_pipeline")
        pipeline2.add_step(MockStep2("step1"))
        self.assertNotEqual(
            pipeline1.get_pipeline_guid(), pipeline2.get_pipeline_guid()
        )

    def test_pipeline_has_clean_guid(self):
        pipeline = Pipeline("test_pipeline")
        self.assertNotIn(str(pipeline.get_pipeline_guid()), " ")


if __name__ == "__main__":
    unittest.main()
