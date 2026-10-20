"""Coordinates recording sessions between engine, pipeline, telemetry and export."""
from __future__ import annotations

import time

from rrt.core.route_engine import RouteEngine
from rrt.core.capture_pipeline import CapturePipeline
from rrt.services.telemetry_service import TelemetryService
from rrt.services.export_service import ExportService
from rrt.utils.logging_setup import get_logger

log = get_logger("orchestrator")


class SessionOrchestrator:
    def __init__(
        self,
        engine: RouteEngine,
        pipeline: CapturePipeline,
        telemetry: TelemetryService,
        exporter: ExportService,
    ) -> None:
        self.engine = engine
        self.pipeline = pipeline
        self.telemetry = telemetry
        self.exporter = exporter
        self.recording = False
        self.started_at = 0.0

    def start(self) -> None:
        self.started_at = time.time()
        self.telemetry.record("session_start", {"version": "0.9.3"})
        log.info("Roadside Research Trainer session started")

    def toggle_recording(self) -> None:
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self) -> None:
        self.recording = True
        self.engine.start_segment("live")
        self.telemetry.record("record_start", {})
        log.info("recording started")

    def stop_recording(self) -> None:
        self.recording = False
        stats = self.engine.close_segment()
        self.telemetry.record("record_stop", stats)
        log.info("recording stopped: %s", stats)

    def shutdown(self) -> None:
        if self.recording:
            self.stop_recording()
        path = self.exporter.export_route(self.engine.route)
        self.telemetry.record("session_end", {"export": str(path)})
        self.telemetry.flush()
        log.info("session exported to %s", path)