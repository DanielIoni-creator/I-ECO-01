#!/usr/bin/env python3
"""
Dashboard Client - inoltro di letture e allarmi alla dashboard.
In questa implementazione si limita a serializzare lo stato come payload
JSON pronto per essere inviato via HTTP / MQTT / WebSocket.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .alarms import Alarm
from .sensors import SensorReading


@dataclass
class DashboardClient:
    """Client per la dashboard di bordo. Tiene lo stato piu` recente."""

    endpoint: str = "https://dashboard.local/api/life_support"
    last_payload: Optional[Dict[str, Any]] = None
    sent_count: int = 0
    failed_count: int = 0
    log: List[Dict[str, Any]] = field(default_factory=list)

    def build_payload(self, station_id: str, reading: SensorReading,
                      alarms: List[Alarm]) -> Dict[str, Any]:
        return {
            "station_id": station_id,
            "sensor": reading.as_dict(),
            "alarms": [
                {"code": a.code, "severity": a.severity, "message": a.message}
                for a in alarms
            ],
            "alarm_count": len(alarms),
            "critical": any(a.severity == "critical" for a in alarms),
        }

    def publish(self, station_id: str, reading: SensorReading,
                alarms: List[Alarm], *, transport: Optional[Any] = None) -> Dict[str, Any]:
        """Costruisce il payload, lo registra, e prova ad inviarlo se
        viene fornito un `transport` (es. requests.Session, mqtt.Client)."""
        payload = self.build_payload(station_id, reading, alarms)
        self.last_payload = payload
        if transport is not None:
            try:
                response = transport.post(self.endpoint, json=payload, timeout=5)
                ok = 200 <= getattr(response, "status_code", 0) < 300
                if ok:
                    self.sent_count += 1
                else:
                    self.failed_count += 1
                self.log.append({"ok": ok, "status": getattr(response, "status_code", None)})
            except Exception as exc:  # noqa: BLE001
                self.failed_count += 1
                self.log.append({"ok": False, "error": str(exc)})
        return payload

    def to_json(self) -> str:
        if self.last_payload is None:
            return "{}"
        return json.dumps(self.last_payload, indent=2, ensure_ascii=False)
