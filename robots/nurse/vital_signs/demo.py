#!/usr/bin/env python3
"""Runnable demo for the Vital Signs Monitor (issue #58).

Ingest three synthetic patients with realistic readings (one normal,
one tachycardic, one hypoxic), then print the resulting dashboard
payload and the audit chain verification status.
"""
from __future__ import annotations

import json
import os
import sys

# Allow running from any cwd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from monitor import (
    AlarmManager,
    BlockchainAuditLog,
    DashboardSnapshot,
    SensorFusion,
    VitalSignsMonitor,
    VitalThresholds,
)


SAMPLES = {
    "P001": {"heart_rate": 72, "spo2": 98, "temperature_c": 36.7},
    "P002": {"heart_rate": 140, "spo2": 97, "temperature_c": 37.1},
    "P003": {"heart_rate": 88, "spo2": 89, "temperature_c": 36.9},
}


def _reader(patient_id: str):
    return SAMPLES[patient_id]


def main() -> int:
    monitor = VitalSignsMonitor(
        fusion=SensorFusion(reader=_reader),
        alarm_manager=AlarmManager(
            thresholds=VitalThresholds(
                min_heart_rate=60,
                max_heart_rate=120,
                min_spo2=94,
                max_temperature_c=38.0,
            )
        ),
        audit_log=BlockchainAuditLog(),
    )

    for pid in sorted(SAMPLES):
        alarm = monitor.ingest(pid)
        print(f"{pid}: severity={alarm['severity']:>8}  messages={alarm['messages']}")

    snapshot = DashboardSnapshot(monitor)
    rendered = snapshot.render()
    print("\nDashboard JSON:")
    print(json.dumps(rendered, indent=2, default=str))

    print(
        f"\nAudit chain length = {monitor.audit_log.length()}, "
        f"verify = {monitor.audit_log.verify()}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())