from watergrid.context import OutputMode
from watergrid.context.context_metadata import ContextMetadata


class DataContext:
    """
    Stores data from previous steps, and allows you to pass KV pairs to
    subsequent steps.
    """

    def __init__(self):
        self.data = {}
        self.output_mode = OutputMode.DIRECT
        self.metadata = ContextMetadata()

    def set(self, key: str, value: object) -> None:
        """
        Sets a key-value pair in the pipeline context to be passed to another step.
        :param key: Key to set.
        :param value: Value to assign to the given key.
        :return: None
        """
        self.data[key] = value

    def get(self, key: str):
        """
        Gets the value of a given key.
        :param key: Key of the value to get.
        :return: Value of the given key (if found in the KV store).
        """
        return self.data[key]

    def get_all(self) -> dict:
        """
        Gets all the data stored in the pipeline context.
        :return: Dictionary of all KV pairs in the pipeline context.
        """
        return self.data

    def set_batch(self, batch: dict) -> None:
        """
        Overwrites all data in the pipeline context with the given dict.
        :param batch: Data to overwrite the pipeline context with.
        :return: None
        """
        self.data = batch

    def has(self, key: str) -> bool:
        """
        Checks if a given key is in the pipeline context.
        :param key: Key to check for.
        :return: Boolean denoting if the key was found.
        """
        return key in self.data

    def set_output_mode(self, mode: OutputMode) -> None:
        """
        Sets the output mode of the pipeline context. Determines if the context will be deleted, forwarded,
        or split before the next step.
        :param mode: Mode to set the pipeline context to.
        :return: None
        """
        self.output_mode = mode

    def reset_context(self):
        """
        Resets the pipeline context mode to the default.
        :return:
        """
        self.output_mode = OutputMode.DIRECT

    def get_output_mode(self) -> OutputMode:
        """
        Gets the output mode of the pipeline context.
        :return: Currently configured output mode of the pipeline context.
        """
        return self.output_mode

    def get_run_metadata(self) -> ContextMetadata:
        """
        Gets the metadata associated with the current run.
        :return: Metadata associated with the current run.
        """
        return self.metadata

    def set_run_metadata(self, metadata: ContextMetadata) -> None:
        """
        Sets the metadata associated with the current run.
        :param metadata: Metadata to associate with the current run.
        :return: None
        """
        self.metadata = metadata

    @staticmethod
    def deep_copy_context(context):
        """
        Creates a deep copy of a DataContext object.
        :param context: Context instance to be copied.
        :return: New copy of the given context instance.
        """
        new_context = DataContext()
        new_context.set_batch(dict(context.get_all()))
        return new_context
