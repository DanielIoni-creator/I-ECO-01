#!/usr/bin/env python3
"""Hera security patrol orchestration.

Hardware, computer-vision and alarm providers are injected through small
interfaces.  The module therefore remains testable without pretending that a
camera, an AI model or a physical security system is available.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
import time
from typing import Any, Callable, Mapping, Protocol, Sequence
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from uuid import uuid4


@dataclass(frozen=True)
class SensorReading:
    area: str
    motion: bool = False
    door_forced: bool = False
    tamper: bool = False
    access_authorized: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class VisionObservation:
    label: str
    confidence: float
    track_id: str | None = None


@dataclass(frozen=True)
class Detection:
    category: str
    severity: str
    confidence: float
    sources: tuple[str, ...]
    details: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SecurityAlert:
    id: str
    robot: str
    area: str
    category: str
    severity: str
    confidence: float
    sources: tuple[str, ...]
    created_at: str
    details: Mapping[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class SensorSuite(Protocol):
    def read(self, area: str) -> SensorReading: ...


class VisionModel(Protocol):
    def infer(self, area: str) -> Sequence[VisionObservation]: ...


class Navigator(Protocol):
    def move_to(self, area: str) -> bool: ...


class AlertNotifier(Protocol):
    def notify(self, alert: SecurityAlert) -> None: ...


class SecuritySystem(Protocol):
    def report_event(self, alert: SecurityAlert) -> None: ...


class SensorFusionIntrusionDetector:
    """Fuse physical sensors with observations produced by an AI adapter."""

    def __init__(self, person_confidence_threshold: float = 0.75):
        if not 0 <= person_confidence_threshold <= 1:
            raise ValueError("person_confidence_threshold must be between 0 and 1")
        self.person_confidence_threshold = person_confidence_threshold

    def detect(
        self,
        reading: SensorReading,
        observations: Sequence[VisionObservation],
    ) -> list[Detection]:
        detections: list[Detection] = []

        if reading.door_forced or reading.tamper:
            reasons = []
            if reading.door_forced:
                reasons.append("door_forced")
            if reading.tamper:
                reasons.append("sensor_tamper")
            detections.append(Detection(
                category="perimeter_breach",
                severity="critical",
                confidence=1.0,
                sources=("physical_sensor",),
                details={"signals": reasons},
            ))

        if reading.access_authorized:
            return detections

        people = [
            item for item in observations
            if item.label.lower() == "person"
            and item.confidence >= self.person_confidence_threshold
        ]
        if reading.motion and people:
            strongest = max(people, key=lambda item: item.confidence)
            detections.append(Detection(
                category="unauthorized_person",
                severity="high",
                confidence=strongest.confidence,
                sources=("motion_sensor", "vision_model"),
                details={"track_id": strongest.track_id},
            ))

        return detections


class WebhookSecuritySystem:
    """Send alerts to a security system or notification webhook."""

    def __init__(
        self,
        endpoint: str,
        *,
        token: str | None = None,
        timeout_seconds: float = 5,
        opener: Callable[..., Any] = urlopen,
    ):
        parsed = urlparse(endpoint)
        local_http = parsed.scheme == "http" and parsed.hostname in {"localhost", "127.0.0.1", "::1"}
        if parsed.scheme != "https" and not local_http:
            raise ValueError("security webhook must use HTTPS (HTTP is allowed only for localhost)")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self.endpoint = endpoint
        self.token = token
        self.timeout_seconds = timeout_seconds
        self.opener = opener

    def report_event(self, alert: SecurityAlert) -> None:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = Request(
            self.endpoint,
            data=json.dumps(alert.to_dict()).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with self.opener(request, timeout=self.timeout_seconds) as response:
            status = getattr(response, "status", 200)
            if status >= 300:
                raise RuntimeError(f"security webhook returned HTTP {status}")

    def notify(self, alert: SecurityAlert) -> None:
        self.report_event(alert)


class SecurityRobot:
    def __init__(
        self,
        *,
        route: Sequence[str] = ("ingresso",),
        sensors: SensorSuite,
        vision: VisionModel,
        navigator: Navigator,
        detector: SensorFusionIntrusionDetector | None = None,
        notifiers: Sequence[AlertNotifier] = (),
        security_system: SecuritySystem | None = None,
        alert_cooldown_seconds: float = 60,
        clock: Callable[[], float] = time.time,
    ):
        cleaned_route = tuple(area.strip() for area in route if area.strip())
        if not cleaned_route:
            raise ValueError("route must contain at least one area")
        if alert_cooldown_seconds < 0:
            raise ValueError("alert_cooldown_seconds cannot be negative")
        self.name = "Hera SecurityBot"
        self.route = cleaned_route
        self.sensors = sensors
        self.vision = vision
        self.navigator = navigator
        self.detector = detector or SensorFusionIntrusionDetector()
        self.notifiers = tuple(notifiers)
        self.security_system = security_system
        self.alert_cooldown_seconds = alert_cooldown_seconds
        self.clock = clock
        self.status = "idle"
        self.alerts: list[SecurityAlert] = []
        self.audit_log: list[dict[str, Any]] = []
        self._last_alert_at: dict[tuple[str, str], float] = {}

    def _record(self, event: str, **details: Any) -> None:
        self.audit_log.append({
            "at": datetime.now(timezone.utc).isoformat(),
            "event": event,
            **details,
        })
        self.audit_log[:] = self.audit_log[-1000:]

    def start_patrol(self) -> bool:
        self.status = "patrolling"
        self._record("patrol_started", route=list(self.route))
        return True

    def stop_patrol(self) -> None:
        self.status = "idle"
        self._record("patrol_stopped")

    def _new_alert(self, area: str, detection: Detection) -> SecurityAlert | None:
        now = self.clock()
        key = (area, detection.category)
        if now - self._last_alert_at.get(key, float("-inf")) < self.alert_cooldown_seconds:
            self._record("alert_suppressed", area=area, category=detection.category)
            return None
        self._last_alert_at[key] = now
        alert = SecurityAlert(
            id=str(uuid4()),
            robot=self.name,
            area=area,
            category=detection.category,
            severity=detection.severity,
            confidence=detection.confidence,
            sources=detection.sources,
            created_at=datetime.now(timezone.utc).isoformat(),
            details=detection.details,
        )
        self.alerts.append(alert)
        return alert

    def _dispatch(self, alert: SecurityAlert) -> list[str]:
        errors: list[str] = []
        for notifier in self.notifiers:
            try:
                notifier.notify(alert)
            except Exception as exc:  # adapters must not stop the patrol loop
                errors.append(f"notifier:{type(exc).__name__}")
        if self.security_system:
            try:
                self.security_system.report_event(alert)
            except Exception as exc:
                errors.append(f"security_system:{type(exc).__name__}")
        self._record("alert_dispatched", alert_id=alert.id, errors=errors)
        return errors

    def scan_area(self, area: str) -> dict[str, Any]:
        self.status = "scanning"
        try:
            reading = self.sensors.read(area)
            if reading.area != area:
                raise ValueError("sensor reading area does not match requested area")
            observations = tuple(self.vision.infer(area))
            detections = self.detector.detect(reading, observations)
        except Exception as exc:
            self.status = "degraded"
            self._record("scan_failed", area=area, error=type(exc).__name__)
            return {"area": area, "status": "degraded", "detections": [], "alerts": [], "errors": [type(exc).__name__]}

        emitted: list[SecurityAlert] = []
        dispatch_errors: list[str] = []
        for detection in detections:
            alert = self._new_alert(area, detection)
            if alert:
                emitted.append(alert)
                dispatch_errors.extend(self._dispatch(alert))
        self.status = "alert" if detections else "patrolling"
        self._record("area_scanned", area=area, detections=len(detections), alerts=len(emitted))
        return {
            "area": area,
            "status": "alert" if detections else "safe",
            "detections": [asdict(item) for item in detections],
            "alerts": [item.to_dict() for item in emitted],
            "errors": dispatch_errors,
        }

    def run_patrol(self, *, cycles: int = 1, delay_seconds: float = 0) -> list[dict[str, Any]]:
        if cycles < 1:
            raise ValueError("cycles must be at least 1")
        if delay_seconds < 0:
            raise ValueError("delay_seconds cannot be negative")
        self.start_patrol()
        results: list[dict[str, Any]] = []
        for _ in range(cycles):
            for area in self.route:
                if not self.navigator.move_to(area):
                    self.status = "degraded"
                    self._record("navigation_failed", area=area)
                    results.append({"area": area, "status": "navigation_failed", "detections": [], "alerts": [], "errors": ["navigation_failed"]})
                    continue
                results.append(self.scan_area(area))
                if delay_seconds:
                    time.sleep(delay_seconds)
        self.stop_patrol()
        return results

    def run(self) -> list[dict[str, Any]]:
        return self.run_patrol()


class DemoSensors:
    def read(self, area: str) -> SensorReading:
        return SensorReading(area=area)


class DemoVision:
    def infer(self, area: str) -> Sequence[VisionObservation]:
        return ()


class DemoNavigator:
    def move_to(self, area: str) -> bool:
        print(f"🤖 Spostamento verso: {area}")
        return True


if __name__ == "__main__":
    robot = SecurityRobot(
        route=("ingresso", "magazzino", "uscita"),
        sensors=DemoSensors(),
        vision=DemoVision(),
        navigator=DemoNavigator(),
    )
    print(json.dumps(robot.run(), ensure_ascii=False, indent=2))
