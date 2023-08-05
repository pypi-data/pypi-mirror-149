from abc import ABC, abstractmethod

from watergrid.context import DataContext


class Step(ABC):
    """
    Abstract class for a single step in a pipeline.

    :param step_name: Name of the step.
    :type step_name: str
    :param provides: List of data keys that this step provides.
    :type provides: list
    :param requires: List of data keys that this step requires.
    :type requires: list
    """

    def __init__(self, step_name: str, provides: list = None, requires: list = None):
        self._step_name = step_name

        if provides is None:
            self.__dep_provides = []
        else:
            self.__dep_provides = provides

        if requires is None:
            self.__dep_requires = []
        else:
            self.__dep_requires = requires

    def run_step(self, context: DataContext):
        """
        Used internally by the pipeline. Performs setup and teardown
        in addition to running the step function run().
        :return: None
        """
        self.run(context)

    def get_step_requirements(self) -> list:
        """
        Returns a list of data keys that this step requires.
        :return: List of data keys that this step requires.
        :rtype: list
        """
        return self.__dep_requires

    def get_step_provides(self) -> list:
        """
        Returns a list of data keys that this step provides.
        :return: List of data keys that this step provides.
        :rtype: list
        """
        return self.__dep_provides

    def get_step_name(self) -> str:
        """
        Returns the name of the step.
        :return: Name of the step.
        """
        return self._step_name

    @abstractmethod
    def run(self, context: DataContext):
        pass

    def __str__(self) -> str:
        return self._step_name
