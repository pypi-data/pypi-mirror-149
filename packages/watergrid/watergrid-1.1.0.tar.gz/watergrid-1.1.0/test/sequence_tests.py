import unittest

from watergrid.context import DataContext
from watergrid.pipelines.pipeline import Pipeline
from watergrid.steps import Sequence
from watergrid.steps import Step


class MockStep(Step):
    def __init__(self):
        super().__init__("mock_step")
        self.flag = False

    def run(self, context: DataContext):
        self.flag = True

    def get_flag(self) -> bool:
        return self.flag


class TestSequence(Sequence):
    def __init__(self):
        super().__init__("test_sequence")


class SequenceTestCase(unittest.TestCase):
    def test_sequence_adds_steps(self):
        pipeline = Pipeline("test_pipeline")
        mock_step = MockStep()
        sequence = TestSequence()
        sequence.add_step(mock_step)
        pipeline.add_steps(sequence)
        pipeline.run()
        self.assertTrue(mock_step.get_flag())


if __name__ == "__main__":
    unittest.main()
