"""
Vital Signs module for the MyZubster nurse robot.

Implements issue #58 bounty (Vital Signs Monitor, 3 XMR) as a focused,
additive subpackage under `robots/nurse/vital_signs/`. The existing
`robots/nurse/monitor/vital_monitor.py` stub is intentionally left
untouched so this module can coexist with or precede an in-flight
replacement PR on the same issue.

Public surface:
    - VitalReading            : dataclass for a single patient reading.
    - VitalThresholds         : configurable alarm thresholds.
    - SensorFusion            : heart-rate / SpO2 / temperature ingest.
    - AlarmManager            : threshold + trend alarm evaluation.
    - DashboardSnapshot       : JSON snapshot consumable by HTTP / WS.
    - BlockchainAuditLog       : append-only hash-chained audit record.
    - VitalSignsMonitor       : orchestrator wiring the above together.

Design constraints:
    * Zero external dependencies (stdlib only).
    * Deterministic in tests (no real time, no random, no network).
    * Pure-Python so it runs on the cloud executor and on the targeted
      Raspberry Pi / ESP32 class hardware without extra tooling.
    * All injection points (sensor readers, transport, clock, log sink)
      are explicit constructor arguments so the module is testable and
      production drivers can be substituted without changing call sites.
"""

from .monitor import (
    AlarmManager,
    BlockchainAuditLog,
    DashboardSnapshot,
    SensorFusion,
    VitalReading,
    VitalSignsMonitor,
    VitalThresholds,
)

__all__ = [
    "AlarmManager",
    "BlockchainAuditLog",
    "DashboardSnapshot",
    "SensorFusion",
    "VitalReading",
    "VitalSignsMonitor",
    "VitalThresholds",
]