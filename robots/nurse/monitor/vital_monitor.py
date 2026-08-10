#!/usr/bin/env python3
"""
Vital Signs Monitor - patient vital signs, alarms, dashboard snapshots,
and append-only blockchain-style audit records.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Dict, Iterable, List, Optional


@dataclass(frozen=True)
class VitalReading:
    patient_id: str
    heart_rate: int
    spo2: int
    temperature_c: float
    recorded_at: str

    def as_dict(self) -> Dict[str, object]:
        return {
            "patient_id": self.patient_id,
            "heart_rate": self.heart_rate,
            "spo2": self.spo2,
            "temperature_c": self.temperature_c,
            "recorded_at": self.recorded_at,
        }


@dataclass
class VitalThresholds:
    min_heart_rate: int = 50
    max_heart_rate: int = 120
    min_spo2: int = 94
    max_temperature_c: float = 37.8


@dataclass
class VitalSignsMonitor:
    thresholds: VitalThresholds = field(default_factory=VitalThresholds)
    readings: List[VitalReading] = field(default_factory=list)
    blockchain_log: List[Dict[str, object]] = field(default_factory=list)

    def record_reading(
        self,
        patient_id: str,
        heart_rate: int,
        spo2: int,
        temperature_c: float,
        recorded_at: Optional[str] = None,
    ) -> Dict[str, object]:
        reading = VitalReading(
            patient_id=patient_id,
            heart_rate=heart_rate,
            spo2=spo2,
            temperature_c=round(float(temperature_c), 1),
            recorded_at=recorded_at or datetime.now(timezone.utc).isoformat(),
        )
        self._validate_reading(reading)
        self.readings.append(reading)
        alarms = self.evaluate_alarms(reading)
        audit_record = self.log_to_blockchain(reading, alarms)
        return {
            "reading": reading.as_dict(),
            "alarms": alarms,
            "audit_hash": audit_record["hash"],
            "status": "critical" if alarms else "stable",
        }

    def evaluate_alarms(self, reading: VitalReading) -> List[Dict[str, object]]:
        alarms: List[Dict[str, object]] = []
        if reading.heart_rate < self.thresholds.min_heart_rate:
            alarms.append(self._alarm("heart_rate_low", reading.heart_rate, self.thresholds.min_heart_rate))
        if reading.heart_rate > self.thresholds.max_heart_rate:
            alarms.append(self._alarm("heart_rate_high", reading.heart_rate, self.thresholds.max_heart_rate))
        if reading.spo2 < self.thresholds.min_spo2:
            alarms.append(self._alarm("spo2_low", reading.spo2, self.thresholds.min_spo2))
        if reading.temperature_c > self.thresholds.max_temperature_c:
            alarms.append(
                self._alarm("temperature_high", reading.temperature_c, self.thresholds.max_temperature_c)
            )
        return alarms

    def dashboard_snapshot(self) -> Dict[str, object]:
        latest_by_patient: Dict[str, Dict[str, object]] = {}
        active_alarms = 0
        for reading in self.readings:
            alarms = self.evaluate_alarms(reading)
            active_alarms += len(alarms)
            latest_by_patient[reading.patient_id] = {
                **reading.as_dict(),
                "status": "critical" if alarms else "stable",
                "alarms": alarms,
            }
        return {
            "patients": list(latest_by_patient.values()),
            "patient_count": len(latest_by_patient),
            "active_alarm_count": active_alarms,
            "last_audit_hash": self.blockchain_log[-1]["hash"] if self.blockchain_log else None,
        }

    def import_sensor_batch(self, patient_id: str, sensor_rows: Iterable[Dict[str, object]]) -> List[Dict[str, object]]:
        return [
            self.record_reading(
                patient_id=patient_id,
                heart_rate=int(row["heart_rate"]),
                spo2=int(row["spo2"]),
                temperature_c=float(row["temperature_c"]),
                recorded_at=str(row.get("recorded_at")) if row.get("recorded_at") else None,
            )
            for row in sensor_rows
        ]

    def log_to_blockchain(self, reading: VitalReading, alarms: List[Dict[str, object]]) -> Dict[str, object]:
        previous_hash = self.blockchain_log[-1]["hash"] if self.blockchain_log else "GENESIS"
        payload = f"{previous_hash}|{reading.as_dict()}|{alarms}"
        record = {
            "index": len(self.blockchain_log) + 1,
            "patient_id": reading.patient_id,
            "previous_hash": previous_hash,
            "hash": sha256(payload.encode("utf-8")).hexdigest(),
            "payload": reading.as_dict(),
            "alarms": alarms,
        }
        self.blockchain_log.append(record)
        return record

    def _alarm(self, code: str, value: object, threshold: object) -> Dict[str, object]:
        return {"code": code, "value": value, "threshold": threshold, "severity": "critical"}

    def _validate_reading(self, reading: VitalReading) -> None:
        if not reading.patient_id:
            raise ValueError("patient_id is required")
        if not 20 <= reading.heart_rate <= 240:
            raise ValueError("heart_rate outside supported sensor range")
        if not 50 <= reading.spo2 <= 100:
            raise ValueError("spo2 outside supported sensor range")
        if not 30.0 <= reading.temperature_c <= 45.0:
            raise ValueError("temperature_c outside supported sensor range")


if __name__ == "__main__":
    monitor = VitalSignsMonitor()
    result = monitor.record_reading("P001", heart_rate=88, spo2=97, temperature_c=36.8)
    print(result)
    print(monitor.dashboard_snapshot())
