import unittest

from watergrid.context import DataContext, OutputMode
from watergrid.pipelines.pipeline import Pipeline
from watergrid.steps import Step


class TestDTO:
    def __init__(self, value):
        self.value = value

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value


class TestCreateDTOStep(Step):
    def run(self, context: DataContext):
        context.set("dto", TestDTO(1))
        context.set("val", [1, 2])
        context.set_output_mode(OutputMode.SPLIT)

    def __init__(self):
        super().__init__("test_create_dto_step", provides=["val", "dto"])


class TestModifyDTOStep(Step):
    def __init__(self):
        super().__init__("test_modify_dto_step", requires=["val"])

    def run(self, context: DataContext):
        if context.get("val") == 1:
            context.get("dto").set_value(5)


class TestVerifyCopySafetyStep(Step):
    def __init__(self):
        super().__init__("test_verify_copy_safety_step", requires=["val"])
        self.mod_1_flag = -1
        self.keep_2_flag = -1

    def run(self, context: DataContext):
        if context.get("val") == 1:
            self.mod_1_flag = context.get("dto").get_value()
        elif context.get("val") == 2:
            self.keep_2_flag = context.get("dto").get_value()


class Bug6TestCase(unittest.TestCase):
    def test_bug6(self):
        pipeline = Pipeline("test_pipeline")
        pipeline.add_step(TestCreateDTOStep())
        pipeline.add_step(TestModifyDTOStep())
        step3 = TestVerifyCopySafetyStep()
        pipeline.add_step(step3)
        pipeline.run()
        self.assertEqual(5, step3.mod_1_flag)
        self.assertEqual(1, step3.keep_2_flag)
