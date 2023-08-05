from abc import ABC

from watergrid.steps import Step


class Sequence(ABC):
    """
    A sequence object is used to form a logical grouping of steps. It can be
    used to simplify your pipeline initialization code, or it can be used to
    rapidly re-use multiple steps at once.
    """

    def __init__(self, name: str):
        self.name = name
        self.steps = []

    def add_step(self, step: Step) -> None:
        """
        Adds a step to the sequence.
        :param step: Step to add.
        :return: None
        """
        self.steps.append(step)

    def export_steps(self) -> list:
        """
        Returns a list of all steps in the sequence. Used internally by the
        pipeline class.
        :return: List of all steps.
        """
        return self.steps
