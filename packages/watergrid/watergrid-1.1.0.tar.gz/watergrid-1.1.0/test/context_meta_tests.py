import unittest

from watergrid.context import DataContext
from watergrid.pipelines.pipeline import Pipeline
from watergrid.steps import Step


class MockStepA(Step):
    def __init__(self):
        super().__init__(self.__class__.__name__)
        self.mock_flag = False
        self.last_run_flag = False

    def run(self, context: DataContext):
        if context.get_run_metadata() is not None:
            self.mock_flag = True
            if context.get_run_metadata().get_last_pipeline_run() is not None:
                self.last_run_flag = True

    def get_context_flag(self):
        return self.mock_flag

    def get_last_run_flag(self):
        return self.last_run_flag


class ContextMetaTestCase(unittest.TestCase):
    def test_meta_initializes(self):
        context = DataContext()
        self.assertIsNotNone(context.get_run_metadata())

    def test_can_use_meta_in_step(self):
        pipeline = Pipeline("test_pipeline")
        step1 = MockStepA()
        pipeline.add_step(step1)
        pipeline.run()
        self.assertTrue(step1.get_context_flag())

    def test_can_use_meta_in_step_with_last_run(self):
        pipeline = Pipeline("test_pipeline")
        step1 = MockStepA()
        pipeline.add_step(step1)
        pipeline.run()
        pipeline.run()
        self.assertTrue(step1.get_last_run_flag())


if __name__ == "__main__":
    unittest.main()
