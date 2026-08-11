"""Unit tests for the MyZubster nurse robot Vital Signs Monitor (issue #58).

Covers:
  * SensorFusion validation and happy-path capture
  * AlarmManager threshold evaluation + hysteresis
  * DashboardSnapshot JSON shape and content
  * BlockchainAuditLog append, hash chain, and tamper detection
  * VitalSignsMonitor orchestrator end-to-end
"""
import json
import unittest
from typing import Dict, Mapping

from monitor import (
    AlarmManager,
    BlockchainAuditLog,
    DashboardSnapshot,
    SensorFusion,
    VitalReading,
    VitalSignsMonitor,
    VitalThresholds,
)


def _sample_reader(samples: Dict[str, Mapping[str, float]]):
    def _reader(patient_id: str) -> Mapping[str, float]:
        if patient_id not in samples:
            raise KeyError(patient_id)
        return samples[patient_id]
    return _reader


def _fixed_clock(value: str = "2026-08-10T20:00:00+00:00"):
    return lambda: value


class SensorFusionTests(unittest.TestCase):
    def test_capture_returns_vital_reading(self):
        fusion = SensorFusion(
            reader=_sample_reader({"P001": {"heart_rate": 72, "spo2": 98, "temperature_c": 36.7}}),
            clock=_fixed_clock(),
        )
        reading = fusion.capture("P001")
        self.assertEqual(reading.patient_id, "P001")
        self.assertEqual(reading.heart_rate, 72)
        self.assertEqual(reading.spo2, 98)
        self.assertAlmostEqual(reading.temperature_c, 36.7)
        self.assertEqual(reading.recorded_at, "2026-08-10T20:00:00+00:00")

    def test_capture_rejects_invalid_spo2(self):
        fusion = SensorFusion(
            reader=_sample_reader({"P001": {"heart_rate": 72, "spo2": 150, "temperature_c": 36.7}}),
            clock=_fixed_clock(),
        )
        with self.assertRaises(ValueError):
            fusion.capture("P001")

    def test_capture_rejects_missing_field(self):
        fusion = SensorFusion(
            reader=_sample_reader({"P001": {"heart_rate": 72, "temperature_c": 36.7}}),
            clock=_fixed_clock(),
        )
        with self.assertRaises(ValueError):
            fusion.capture("P001")

    def test_capture_requires_patient_id(self):
        fusion = SensorFusion(reader=lambda _pid: {"heart_rate": 72, "spo2": 98, "temperature_c": 36.7})
        with self.assertRaises(ValueError):
            fusion.capture("")


class AlarmManagerTests(unittest.TestCase):
    def test_thresholds_normalization_rejects_bad_values(self):
        with self.assertRaises(ValueError):
            VitalThresholds(min_heart_rate=0)
        with self.assertRaises(ValueError):
            VitalThresholds(min_heart_rate=120, max_heart_rate=60)
        with self.assertRaises(ValueError):
            VitalThresholds(min_spo2=120)
        with self.assertRaises(ValueError):
            VitalThresholds(max_temperature_c=10)

    def test_nominal_reading_is_ok(self):
        manager = AlarmManager(thresholds=VitalThresholds())
        reading = VitalReading("P001", 72, 98, 36.7, "2026-08-10T20:00:00+00:00")
        result = manager.evaluate(reading)
        self.assertEqual(result["severity"], "ok")
        self.assertEqual(result["messages"], [])

    def test_low_spo2_is_critical(self):
        manager = AlarmManager(thresholds=VitalThresholds(min_spo2=94))
        reading = VitalReading("P001", 80, 88, 36.7, "2026-08-10T20:00:00+00:00")
        result = manager.evaluate(reading)
        self.assertEqual(result["severity"], "critical")
        self.assertTrue(any("hypoxemia" in m for m in result["messages"]))

    def test_high_heart_rate_is_warning(self):
        manager = AlarmManager(thresholds=VitalThresholds(max_heart_rate=100))
        reading = VitalReading("P001", 140, 98, 36.7, "2026-08-10T20:00:00+00:00")
        result = manager.evaluate(reading)
        self.assertEqual(result["severity"], "warning")
        self.assertTrue(any("tachycardia" in m for m in result["messages"]))

    def test_low_heart_rate_is_warning(self):
        manager = AlarmManager(thresholds=VitalThresholds(min_heart_rate=60))
        reading = VitalReading("P001", 40, 98, 36.7, "2026-08-10T20:00:00+00:00")
        result = manager.evaluate(reading)
        self.assertEqual(result["severity"], "warning")
        self.assertTrue(any("bradycardia" in m for m in result["messages"]))

    def test_hypothermia_is_critical(self):
        manager = AlarmManager(thresholds=VitalThresholds())
        reading = VitalReading("P001", 72, 98, 34.0, "2026-08-10T20:00:00+00:00")
        result = manager.evaluate(reading)
        self.assertEqual(result["severity"], "critical")

    def test_hysteresis_does_not_lower_severity(self):
        manager = AlarmManager(thresholds=VitalThresholds(min_spo2=94))
        # First reading: critical (spo2 below threshold)
        manager.evaluate(VitalReading("P001", 72, 88, 36.7, "t1"))
        # Second reading is borderline ok but hysteresis keeps severity elevated
        result = manager.evaluate(VitalReading("P001", 72, 95, 36.7, "t2"))
        self.assertEqual(result["severity"], "critical")


class BlockchainAuditLogTests(unittest.TestCase):
    def test_empty_chain_is_valid(self):
        log = BlockchainAuditLog()
        self.assertEqual(log.length(), 0)
        self.assertIsNone(log.head_hash())
        self.assertTrue(log.verify())

    def test_append_grows_chain_and_links_hashes(self):
        log = BlockchainAuditLog()
        first = log.append({"event": "ingest", "value": 1})
        second = log.append({"event": "ingest", "value": 2})
        self.assertEqual(log.length(), 2)
        self.assertEqual(second.prev_hash, first.record_hash)
        self.assertTrue(log.verify())

    def test_tamper_detection(self):
        log = BlockchainAuditLog()
        log.append({"event": "ingest", "value": 1})
        log.append({"event": "ingest", "value": 2})
        # Mutate the payload of record 0 in place
        log._records[0].payload = json.dumps({"event": "tampered"})
        self.assertFalse(log.verify())


class DashboardSnapshotTests(unittest.TestCase):
    def test_render_includes_alarm_and_audit_head(self):
        fusion = SensorFusion(
            reader=_sample_reader({"P001": {"heart_rate": 72, "spo2": 98, "temperature_c": 36.7}}),
            clock=_fixed_clock(),
        )
        monitor = VitalSignsMonitor(fusion=fusion, clock=_fixed_clock())
        monitor.ingest("P001")
        snapshot = DashboardSnapshot(monitor)
        rendered = snapshot.render()
        self.assertIn("generated_at", rendered)
        self.assertEqual(rendered["audit_chain_length"], 1)
        self.assertEqual(len(rendered["audit_chain_head"]), 64)
        # patients list is a list of (id, dict) tuples -> serialized via json
        patients = rendered["patients"]
        self.assertEqual(len(patients), 1)
        pid, payload = patients[0]
        self.assertEqual(pid, "P001")
        self.assertEqual(payload["alarm"]["severity"], "ok")

    def test_to_json_is_serializable(self):
        fusion = SensorFusion(
            reader=_sample_reader({"P001": {"heart_rate": 72, "spo2": 98, "temperature_c": 36.7}}),
            clock=_fixed_clock(),
        )
        monitor = VitalSignsMonitor(fusion=fusion, clock=_fixed_clock())
        monitor.ingest("P001")
        text = DashboardSnapshot(monitor).to_json()
        # Round-trip must succeed without TypeError.
        decoded = json.loads(text)
        self.assertIn("generated_at", decoded)


class VitalSignsMonitorTests(unittest.TestCase):
    def test_orchestrator_persists_audit_and_emits_alarm(self):
        samples = {
            "P001": {"heart_rate": 72, "spo2": 98, "temperature_c": 36.7},
            "P002": {"heart_rate": 140, "spo2": 98, "temperature_c": 36.7},
        }
        fusion = SensorFusion(reader=_sample_reader(samples), clock=_fixed_clock())
        monitor = VitalSignsMonitor(fusion=fusion, clock=_fixed_clock())
        monitor.ingest_many(["P001", "P002"])
        self.assertEqual(monitor.audit_log.length(), 2)
        self.assertTrue(monitor.audit_log.verify())
        alarms = monitor.latest_alarms()
        self.assertEqual(alarms["P001"]["severity"], "ok")
        self.assertEqual(alarms["P002"]["severity"], "warning")


if __name__ == "__main__":
    unittest.main()