"""Application entry point and main Qt bootstrap for Roadside Research Trainer."""
from __future__ import annotations

import sys
import signal
from pathlib import Path

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QTimer

from rrt.bootstrap.single_instance import acquire_instance_lock
from rrt.core.route_engine import RouteEngine
from rrt.core.capture_pipeline import CapturePipeline
from rrt.core.session_orchestrator import SessionOrchestrator
from rrt.services.telemetry_service import TelemetryService
from rrt.services.export_service import ExportService
from rrt.handlers.hotkey_handler import HotkeyHandler
from rrt.handlers.overlay_handler import OverlayHandler
from rrt.handlers.annotation_handler import AnnotationHandler
from rrt.utils.logging_setup import get_logger
from rrt.utils.paths import app_data_dir

log = get_logger("bootstrap")


class RoadsideTrainerApp:
    """Wires up the engine, services, and handlers for one trainer session."""

    def __init__(self, argv: list[str]) -> None:
        self.argv = argv
        self.qt_app: QApplication | None = None
        self.engine: RouteEngine | None = None
        self.pipeline: CapturePipeline | None = None
        self.orchestrator: SessionOrchestrator | None = None

    def _build_services(self) -> None:
        self.telemetry = TelemetryService(app_data_dir() / "telemetry.db")
        self.exporter = ExportService(app_data_dir() / "exports")

    def _build_handlers(self) -> None:
        self.hotkeys = HotkeyHandler()
        self.overlay = OverlayHandler()
        self.annotator = AnnotationHandler()

    def run(self) -> int:
        if not acquire_instance_lock():
            log.warning("another Roadside Research Trainer instance is running")
            return 1

        self.qt_app = QApplication(self.argv)
        self.qt_app.setApplicationName("Roadside Research Trainer")
        self.qt_app.setOrganizationName("RRT")

        self._build_services()
        self._build_handlers()

        self.engine = RouteEngine()
        self.pipeline = CapturePipeline(engine=self.engine)
        self.orchestrator = SessionOrchestrator(
            engine=self.engine,
            pipeline=self.pipeline,
            telemetry=self.telemetry,
            exporter=self.exporter,
        )

        self.hotkeys.bind("F8", self.orchestrator.toggle_recording)
        self.hotkeys.bind("F9", self.annotator.mark_waypoint)
        self.hotkeys.bind("F10", self.overlay.toggle)
        self.hotkeys.start()

        QTimer.singleShot(0, self.orchestrator.start)
        signal.signal(signal.SIGINT, lambda *_: self.qt_app.quit())
        return self.qt_app.exec()


def launch(argv: list[str] | None = None) -> int:
    return RoadsideTrainerApp(argv or sys.argv).run()


if __name__ == "__main__":
    raise SystemExit(launch())