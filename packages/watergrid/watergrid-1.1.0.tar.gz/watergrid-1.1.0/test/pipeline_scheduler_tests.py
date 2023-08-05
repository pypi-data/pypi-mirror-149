import unittest

from watergrid.context import DataContext
from watergrid.pipelines.pipeline import Pipeline
from watergrid.steps import Step


class MockStep(Step):
    def __init__(self, provides=[], requires=[]):
        super().__init__(self.__class__.__name__, provides, requires)
        if provides is None:
            provides = []
        self.run_order = 0

    def run(self, context: DataContext):
        if context.has("test_key"):
            self.run_order = context.get("test_key") + 1
            context.set("test_key", self.run_order)
        else:
            context.set("test_key", 1)
            self.run_order = 1

    def get_flag(self):
        return self.run_order


class PipelineSchedulerTestCase(unittest.TestCase):
    def test_pipeline_does_not_break_in_order_steps(self):
        pipeline = Pipeline("test_pipeline")
        step_a = MockStep(provides=["a"])
        pipeline.add_step(step_a)
        step_b = MockStep(requires=["a"])
        pipeline.add_step(step_b)
        pipeline.run()
        self.assertEqual(1, step_a.get_flag())
        self.assertEqual(2, step_b.get_flag())

    def test_pipeline_does_not_delete_steps(self):
        pipeline = Pipeline("test_pipeline")
        step_a = MockStep(provides=["a"])
        pipeline.add_step(step_a)
        step_b = MockStep(requires=["a"])
        pipeline.add_step(step_b)
        pipeline.run()
        self.assertEqual(2, pipeline.get_step_count())

    def test_pipeline_throws_if_unmet_dependencies(self):
        pipeline = Pipeline("test_pipeline")
        step_b = MockStep(requires=["a"])
        pipeline.add_step(step_b)
        with self.assertRaises(Exception):
            pipeline.run()
        self.assertEqual(0, step_b.get_flag())

    def test_pipeline_schedules_basic_dependencies_in_steps(self):
        pipeline = Pipeline("test_pipeline")
        step_a = MockStep(provides=["a"])
        step_b = MockStep(requires=["a"])
        pipeline.add_step(step_b)
        pipeline.add_step(step_a)
        pipeline.run()
        self.assertEqual(pipeline.get_step_count(), 2)
        self.assertEqual(step_a.get_flag(), 1)
        self.assertEqual(step_b.get_flag(), 2)

    def test_pipeline_schedules_three_dependencies(self):
        pipeline = Pipeline("test_pipeline")
        step_a = MockStep(provides=["a"])
        step_b = MockStep(requires=["a"], provides=["b"])
        step_c = MockStep(requires=["b"])
        pipeline.add_step(step_c)
        pipeline.add_step(step_b)
        pipeline.add_step(step_a)
        pipeline.run()
        self.assertEqual(3, pipeline.get_step_count())
        self.assertEqual(1, step_a.get_flag())
        self.assertEqual(2, step_b.get_flag())
        self.assertEqual(3, step_c.get_flag())

    def test_pipeline_throw_error_on_circular_dependencies(self):
        pipeline = Pipeline("test_pipeline")
        step_a = MockStep(provides=["a"], requires=["b"])
        step_b = MockStep(provides=["b"], requires=["a"])
        pipeline.add_step(step_a)
        pipeline.add_step(step_b)
        with self.assertRaises(Exception):
            pipeline.run()


if __name__ == "__main__":
    unittest.main()
