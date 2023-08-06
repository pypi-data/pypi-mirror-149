from watergrid.metrics.MetricsExporter import MetricsExporter


class MetricsStore:
    def __init__(self):
        self._metrics_exporters = []

    def add_metrics_exporter(self, metrics_exporter: MetricsExporter):
        self._metrics_exporters.append(metrics_exporter)

    def start_pipeline_monitoring(self, pipeline_name: str):
        for exporter in self._metrics_exporters:
            exporter.start_pipeline(pipeline_name)

    def stop_pipeline_monitoring(self):
        for exporter in self._metrics_exporters:
            exporter.end_pipeline()

    def start_step_monitoring(self, step_name: str):
        for exporter in self._metrics_exporters:
            exporter.start_step(step_name)

    def stop_step_monitoring(self):
        for exporter in self._metrics_exporters:
            exporter.end_step()

    def report_exception(self, exception: Exception):
        for exporter in self._metrics_exporters:
            exporter.capture_exception(exception)
