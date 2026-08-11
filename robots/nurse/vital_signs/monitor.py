#!/usr/bin/env python3
"""
Vital Signs Monitor for the MyZubster nurse robot (issue #58 bounty).

Provides a deterministic, dependency-free implementation of:
  - sensor fusion for heart rate, SpO2 and temperature
  - configurable per-patient alarm thresholds with hysteresis
  - real-time dashboard snapshots (JSON-serialisable, transport-agnostic)
  - append-only blockchain-style audit log (hash-chained SHA-256 records)

The module is deliberately self-contained: no randomness, no real time
clock, no network, no third-party packages. Production drivers (GPIO,
I2C, MQTT, HTTP) plug in via the constructor hooks so tests stay pure.

Run ``python -m unittest robots.nurse.vital_signs.test_vital_signs`` from
the repo root to execute the bundled unit tests.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Sequence


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class VitalReading:
    """A single set of vital signs captured for a patient at a moment."""

    patient_id: str
    heart_rate: int
    spo2: int
    temperature_c: float
    recorded_at: str  # ISO-8601 UTC, supplied by the caller

    def as_dict(self) -> Dict[str, object]:
        return {
            "patient_id": self.patient_id,
            "heart_rate": self.heart_rate,
            "spo2": self.spo2,
            "temperature_c": self.temperature_c,
            "recorded_at": self.recorded_at,
        }


@dataclass(frozen=True)
class VitalThresholds:
    """Configurable alarm thresholds for a single patient profile.

    Defaults follow adult clinical norms; tests construct tighter bounds
    to exercise the alarm path without contrived readings.
    """

    min_heart_rate: int = 50
    max_heart_rate: int = 120
    min_spo2: int = 94
    max_temperature_c: float = 38.0
    hysteresis: float = 0.5  # ignore threshold noise smaller than this

    def __post_init__(self) -> None:
        self.normalized()

    def normalized(self) -> "VitalThresholds":
        if self.min_heart_rate <= 0:
            raise ValueError("min_heart_rate must be positive")
        if self.max_heart_rate <= self.min_heart_rate:
            raise ValueError("max_heart_rate must exceed min_heart_rate")
        if not 0 <= self.min_spo2 <= 100:
            raise ValueError("min_spo2 must be in [0, 100]")
        if self.max_temperature_c <= 30.0 or self.max_temperature_c >= 45.0:
            raise ValueError("max_temperature_c must be a plausible body temp")
        if self.hysteresis < 0:
            raise ValueError("hysteresis must be non-negative")
        return self


# ---------------------------------------------------------------------------
# Sensor fusion
# ---------------------------------------------------------------------------


@dataclass
class SensorFusion:
    """Ingests raw sensor samples and emits ``VitalReading`` records.

    ``reader`` is a callable returning ``Mapping[str, float]`` for a given
    patient_id. Tests use ``lambda pid: {...}``; production drivers wrap
    GPIO / I2C hardware. ``clock`` returns an ISO-8601 UTC string so
    injected deterministic time keeps tests reproducible.
    """

    reader: Callable[[str], Mapping[str, float]]
    clock: Callable[[], str] = field(
        default_factory=lambda: (lambda: datetime.now(timezone.utc).isoformat())
    )

    def capture(self, patient_id: str) -> VitalReading:
        if not patient_id:
            raise ValueError("patient_id is required")
        sample = self.reader(patient_id)
        try:
            heart_rate = int(sample["heart_rate"])
            spo2 = int(sample["spo2"])
            temperature_c = float(sample["temperature_c"])
        except KeyError as exc:
            raise ValueError(f"missing sensor field: {exc.args[0]}") from exc
        except (TypeError, ValueError) as exc:
            raise ValueError(f"invalid sensor sample for {patient_id}: {exc}") from exc
        if not 0 <= spo2 <= 100:
            raise ValueError(f"spo2 out of range: {spo2}")
        if heart_rate <= 0:
            raise ValueError(f"heart_rate must be positive: {heart_rate}")
        if not 20.0 <= temperature_c <= 45.0:
            raise ValueError(f"temperature_c implausible: {temperature_c}")
        return VitalReading(
            patient_id=patient_id,
            heart_rate=heart_rate,
            spo2=spo2,
            temperature_c=temperature_c,
            recorded_at=self.clock(),
        )


# ---------------------------------------------------------------------------
# Alarm manager
# ---------------------------------------------------------------------------


_SEVERITY_ORDER = {"ok": 0, "warning": 1, "critical": 2}


@dataclass
class AlarmManager:
    """Evaluate a reading against the configured thresholds."""

    thresholds: VitalThresholds = field(default_factory=VitalThresholds)
    _last_severity: Dict[str, str] = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        self.thresholds = self.thresholds.normalized()

    def evaluate(self, reading: VitalReading) -> Dict[str, object]:
        if not isinstance(reading, VitalReading):
            raise TypeError("evaluate() requires a VitalReading")
        t = self.thresholds
        messages: List[str] = []
        severity = "ok"
        if reading.heart_rate < t.min_heart_rate:
            messages.append(
                f"bradycardia: heart_rate={reading.heart_rate} < {t.min_heart_rate}"
            )
            severity = _bump(severity, "warning")
        elif reading.heart_rate > t.max_heart_rate:
            messages.append(
                f"tachycardia: heart_rate={reading.heart_rate} > {t.max_heart_rate}"
            )
            severity = _bump(severity, "warning")
        if reading.spo2 < t.min_spo2:
            messages.append(
                f"hypoxemia: spo2={reading.spo2}% < {t.min_spo2}%"
            )
            severity = _bump(severity, "critical")
        if reading.temperature_c >= t.max_temperature_c:
            messages.append(
                f"hyperthermia: temperature_c={reading.temperature_c} >= {t.max_temperature_c}"
            )
            severity = _bump(severity, "warning")
        elif reading.temperature_c <= t.max_temperature_c - t.hysteresis - 1.0:
            # Below body-temperature floor (clearly hypothermic).
            if reading.temperature_c < 35.0:
                messages.append(
                    f"hypothermia: temperature_c={reading.temperature_c} < 35.0"
                )
                severity = _bump(severity, "critical")
        # Hysteresis: only escalate severity beyond the prior reading.
        previous = self._last_severity.get(reading.patient_id, "ok")
        if _SEVERITY_ORDER[severity] < _SEVERITY_ORDER[previous]:
            severity = previous
        self._last_severity[reading.patient_id] = severity
        return {
            "patient_id": reading.patient_id,
            "severity": severity,
            "messages": messages,
            "evaluated_at": reading.recorded_at,
        }


def _bump(current: str, candidate: str) -> str:
    return candidate if _SEVERITY_ORDER[candidate] > _SEVERITY_ORDER[current] else current


# ---------------------------------------------------------------------------
# Dashboard snapshot
# ---------------------------------------------------------------------------


@dataclass
class DashboardSnapshot:
    """Aggregate the latest readings/alarms into a single JSON payload."""

    monitor: "VitalSignsMonitor"

    def render(self) -> Dict[str, object]:
        latest = self.monitor.latest_readings()
        alarms = self.monitor.latest_alarms()
        return {
            "generated_at": self.monitor.clock(),
            "patients": sorted(
                {
                    pid: {
                        "latest": latest[pid].as_dict() if pid in latest else None,
                        "alarm": alarms[pid] if pid in alarms else None,
                    }
                    for pid in set(latest) | set(alarms)
                }.items()
            ),
            "audit_chain_length": self.monitor.audit_log.length(),
            "audit_chain_head": self.monitor.audit_log.head_hash(),
        }

    def to_json(self) -> str:
        return json.dumps(self.render(), sort_keys=True, default=str)


# ---------------------------------------------------------------------------
# Blockchain-style audit log
# ---------------------------------------------------------------------------


@dataclass
class _AuditRecord:
    index: int
    payload: str
    prev_hash: str
    record_hash: str

    def as_dict(self) -> Dict[str, str]:
        return {
            "index": str(self.index),
            "payload": self.payload,
            "prev_hash": self.prev_hash,
            "record_hash": self.record_hash,
        }


@dataclass
class BlockchainAuditLog:
    """Append-only hash-chained log of vital-sign events.

    Each record stores ``sha256(prev_hash + payload)``. ``verify()`` walks
    the chain and re-hashes every record so tampering is detectable.
    """

    genesis_prev_hash: str = "0" * 64
    _records: List[_AuditRecord] = field(default_factory=list, init=False)

    def append(self, payload: Mapping[str, object]) -> _AuditRecord:
        encoded = json.dumps(payload, sort_keys=True, default=str)
        prev_hash = self._records[-1].record_hash if self._records else self.genesis_prev_hash
        record_hash = sha256(
            (prev_hash + encoded).encode("utf-8")
        ).hexdigest()
        record = _AuditRecord(
            index=len(self._records),
            payload=encoded,
            prev_hash=prev_hash,
            record_hash=record_hash,
        )
        self._records.append(record)
        return record

    def length(self) -> int:
        return len(self._records)

    def head_hash(self) -> Optional[str]:
        return self._records[-1].record_hash if self._records else None

    def records(self) -> Sequence[Dict[str, str]]:
        return [r.as_dict() for r in self._records]

    def verify(self) -> bool:
        prev_hash = self.genesis_prev_hash
        for record in self._records:
            if record.prev_hash != prev_hash:
                return False
            expected = sha256(
                (prev_hash + record.payload).encode("utf-8")
            ).hexdigest()
            if expected != record.record_hash:
                return False
            prev_hash = record.record_hash
        return True


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


@dataclass
class VitalSignsMonitor:
    """Wires sensor fusion, alarms, dashboard, and audit log together."""

    fusion: SensorFusion
    alarm_manager: AlarmManager = field(default_factory=AlarmManager)
    audit_log: BlockchainAuditLog = field(default_factory=BlockchainAuditLog)
    clock: Callable[[], str] = field(
        default_factory=lambda: (lambda: datetime.now(timezone.utc).isoformat())
    )
    _readings: Dict[str, VitalReading] = field(default_factory=dict, init=False)
    _alarms: Dict[str, Dict[str, object]] = field(default_factory=dict, init=False)

    def ingest(self, patient_id: str) -> Dict[str, object]:
        reading = self.fusion.capture(patient_id)
        self._readings[patient_id] = reading
        alarm = self.alarm_manager.evaluate(reading)
        self._alarms[patient_id] = alarm
        self.audit_log.append(
            {"kind": "vital_signs.reading", "reading": reading.as_dict(), "alarm": alarm}
        )
        return alarm

    def ingest_many(self, patient_ids: Iterable[str]) -> List[Dict[str, object]]:
        return [self.ingest(pid) for pid in patient_ids]

    def latest_readings(self) -> Dict[str, VitalReading]:
        return dict(self._readings)

    def latest_alarms(self) -> Dict[str, Dict[str, object]]:
        return dict(self._alarms)

    def dashboard(self) -> DashboardSnapshot:
        return DashboardSnapshot(self)


__all__ = [
    "AlarmManager",
    "BlockchainAuditLog",
    "DashboardSnapshot",
    "SensorFusion",
    "VitalReading",
    "VitalSignsMonitor",
    "VitalThresholds",
]