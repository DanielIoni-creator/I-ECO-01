#!/usr/bin/env python3
"""
Dashboard client per la centrale a fusione.

Costruisce payload JSON con stato del plasma, potenza prodotta e spinta,
pronto per essere inoltrato a HTTP/MQTT/WS. L'invio vero richiede un
``transport`` (la stazione puo` fornire la sua implementazione); in
assenza il client si limita a registrare l'ultimo payload.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .plasma import PlasmaState
from .propulsion import PropulsionModule


@dataclass
class FusionDashboardClient:
    """Client per la dashboard della centrale a fusione."""

    endpoint: str = "https://dashboard.local/api/fusion_power"
    last_payload: Optional[Dict[str, Any]] = None
    sent_count: int = 0
    failed_count: int = 0
    log: List[Dict[str, Any]] = field(default_factory=list)

    def build_payload(self,
                      station_id: str,
                      plasma: PlasmaState,
                      propulsion: PropulsionModule,
                      electrical_power_mw: float,
                      station_demand_mw: float,
                      regime: str) -> Dict[str, Any]:
        return {
            "station_id": station_id,
            "module": "fusion_power",
            "plasma": plasma.as_dict(),
            "propulsion": propulsion.summary(),
            "electrical_power_mw": electrical_power_mw,
            "station_demand_mw": station_demand_mw,
            "demand_met": electrical_power_mw >= station_demand_mw,
            "regime": regime,
        }

    def publish(self,
                station_id: str,
                plasma: PlasmaState,
                propulsion: PropulsionModule,
                electrical_power_mw: float,
                station_demand_mw: float,
                regime: str,
                *,
                transport: Optional[Any] = None) -> Dict[str, Any]:
        """Costruisce il payload e, se fornito, lo inoltra via ``transport``."""
        payload = self.build_payload(
            station_id, plasma, propulsion, electrical_power_mw,
            station_demand_mw, regime,
        )
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
