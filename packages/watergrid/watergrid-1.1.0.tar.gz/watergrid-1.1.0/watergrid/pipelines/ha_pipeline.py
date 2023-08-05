import logging
import time

from watergrid.locks.PipelineLock import PipelineLock
from watergrid.pipelines.pipeline import Pipeline


class HAPipeline(Pipeline):
    """
    The high availability pipeline allows for several machines to have the pipeline loaded at once. If one of the
    machines fails, or if the pipeline context times out, the pipeline will run on another machine.

    :param pipeline_name: The name of the pipeline.
    :param pipeline_lock: The lock implementation to use for this pipeline.
    """

    def __init__(self, pipeline_name: str, pipeline_lock: PipelineLock):
        super().__init__(pipeline_name)
        self.__pipeline_lock = pipeline_lock
        self.__lock_timings = []

    def run(self):
        self.verify_pipeline()
        if self.__pipeline_lock.lock():
            super().run()
            self.__pipeline_lock.unlock()
        else:
            logging.debug(
                "Pipeline {} is already running on another instance".format(
                    self.get_pipeline_name()
                )
            )

    def run_interval(self, job_interval_s: int) -> None:
        """
        Runs the pipeline in a blocking interval mode. Every job_interval_s seconds, the pipeline is run.
        :param job_interval_s: Number of seconds to wait between pipeline runs.
        :return: None
        """
        self.verify_pipeline()
        while True:
            self._run_interval_loop(job_interval_s)
            time.sleep(self._calculate_delay(job_interval_s) / 1000)

    def _run_interval_loop(self, job_interval_s: int) -> None:
        """
        Runs the pipeline in interval mode once. If the lock is successfully acquired, the pipeline steps are run.
        :param job_interval_s: Number of seconds to wait between pipeline runs.
        :return: None
        """
        if self.__pipeline_lock.lock():
            self._perform_locked_interval_actions(job_interval_s)
            self.__pipeline_lock.unlock()
        else:
            self._handle_lock_acquire_failure()

    def _perform_locked_interval_actions(self, job_interval_s: int) -> None:
        """
        Performs the actions that should be performed when the pipeline is locked. Note that this method assumes that
        the lock has already been acquired and is held by the calling class/function.
        :param job_interval_s: Number of seconds to wait between pipeline runs.
        :return: None
        """
        self._verify_lock_metadata(job_interval_s)
        last_run = self._get_last_run()
        if time.time() - last_run > job_interval_s:
            super().run()
            self._set_last_run(last_run + job_interval_s)

    def _verify_lock_metadata(self, job_interval_s: int) -> None:
        """
        Verifies that the lock metadata is correct. If the metadata is not correct, the lock is deleted and recreated.
        :param job_interval_s: Number of seconds to wait between pipeline runs.
        :return: None
        """
        last_run = self._get_last_run()
        if last_run == 0:
            self._set_last_run(time.time() - job_interval_s)
        if time.time() - last_run > job_interval_s * 3:
            logging.warning(
                "Pipeline {} has fallen more than three cycles behind. Consider increasing the job interval or "
                "provisioning more machines.".format(self.get_pipeline_name())
            )
            self._set_last_run(time.time() - job_interval_s)

    def _handle_lock_acquire_failure(self) -> None:
        """
        Handles the case where the pipeline lock could not be acquired. This is a no-op for the HA pipeline. Does not
        run if the lock could not be acquired due to an exception.
        :return: None
        """
        logging.debug(
            "Pipeline {} is already running on another instance".format(
                self.get_pipeline_name()
            )
        )

    def _set_last_run(self, last_run: float) -> None:
        """
        Sets the timestamp of the last run of this pipeline as recorded in the lock backend.
        :param last_run: Timestamp to record as the last run of this pipeline.
        :return: None
        """
        self.__pipeline_lock.write_key(self._get_pipeline_lock_name(), last_run)

    def _get_last_run(self) -> float:
        """
        Gets the timestamp of the last run of this pipeline as recorded in the lock backend. Note that this value
        keeps the interval defined by job_interval_s, and may not represent the exact time of the last run.
        :return: Timestamp of the last run of this pipeline.
        """
        try:
            return float(self.__pipeline_lock.read_key(self._get_pipeline_lock_name()))
        except TypeError:
            return 0

    def _get_pipeline_lock_name(self) -> str:
        """
        Builds the name of the lock assigned to this pipeline.
        :return: Pipeline lock name.
        """
        return "{}_last_run".format(self.get_pipeline_name())

    def lock_with_timing(self) -> None:
        """
        Acquire the pipeline lock and record the time it took to acquire the lock to the lock timings counter.
        :return: None
        """
        start_time = time.perf_counter()
        self.__pipeline_lock.lock()
        self._append_timing(time.perf_counter() - start_time)

    def unlock_with_timing(self) -> None:
        """
        Unlocks the pipeline and appends the time taken to unlock to the lock timings counter.
        :return: None
        """
        start_time = time.perf_counter()
        self.__pipeline_lock.unlock()
        self._append_timing(time.perf_counter() - start_time)

    def get_average_lock_delay(self) -> float:
        """
        Returns the average time it takes to perform a lock operation with the currently configured backend lock.
        :return: Average operation time in milliseconds.
        """
        if len(self.__lock_timings) == 0:
            return 0
        return float(sum(self.__lock_timings)) / float(len(self.__lock_timings))

    def _calculate_delay(
        self,
        pipeline_interval_s: int,
        checks_per_interval: int = 10,
        check_ratio: int = 3,
    ) -> int:
        """
        Calculates the delay in milliseconds to wait before running the pipeline again. This is based on the configured
        pipeline interval, and the average performance of the backend hosting the pipeline lock.
        :param pipeline_interval_s: The interval in seconds between pipeline runs.
        :param checks_per_interval: Number of times the lock should be chedked per interval across all nodes.
        :param check_ratio: Should be a number close to the average number of pipeline nodes.
        :return: Delay in milliseconds to wait before running the pipeline again.
        """
        redis_delay_ms = self.get_average_lock_delay()
        job_delay_ms = float(pipeline_interval_s * 1000) / float(checks_per_interval)
        if redis_delay_ms > job_delay_ms:
            logging.warning(
                "Slow redis cluster detected. Consider increasing the size of your cluster."
            )
        return int(max(redis_delay_ms, job_delay_ms)) * check_ratio

    def _append_timing(self, timing: float) -> None:
        """
        Adds a lock operation benchmark timing to the rolling average counter. Used for calculating mutex lookup delays.
        :param timing: The time in milliseconds it took to perform the lock operation.
        :return: None
        """
        self.__lock_timings.append(timing)
        if len(self.__lock_timings) > 100:
            self.__lock_timings.pop(0)
