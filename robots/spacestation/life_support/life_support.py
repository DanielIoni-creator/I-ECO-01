#!/usr/bin/env python3
"""
Life Support System - Space Station MyZubster.
Orchestratore: legge i sensori, valuta gli allarmi, pubblica sulla dashboard.
"""

from __future__ import annotations

import time
from typing import Any, Callable, List, Optional

from .alarms import Alarm, AlarmManager
from .dashboard import DashboardClient
from .sensors import SensorReading, SensorSuite


class LifeSupportSystem:
    """Ciclo di vita del supporto vitale della Space Station."""

    def __init__(self,
                 station_id: str = "I-ECO-01",
                 sensors: Optional[SensorSuite] = None,
                 alarms: Optional[AlarmManager] = None,
                 dashboard: Optional[DashboardClient] = None,
                 clock: Callable[[], float] = time.time):
        self.station_id = station_id
        self.sensors = sensors or SensorSuite()
        self.alarms = alarms or AlarmManager()
        self.dashboard = dashboard or DashboardClient()
        self._clock = clock
        self._running = False
        self._tick_count = 0
        self._last_alarms: List[Alarm] = []

    def start(self) -> None:
        self._running = True
        print(f"🛰️  Life Support avviato per stazione {self.station_id}")

    def stop(self) -> None:
        self._running = False
        print("🛑 Life Support arrestato")

    @property
    def last_alarms(self) -> List[Alarm]:
        return list(self._last_alarms)

    def tick(self) -> dict:
        """Esegue un singolo ciclo: lettura sensori, allarmi, pubblicazione."""
        if not self._running:
            raise RuntimeError("LifeSupportSystem non avviato (chiamare start())")
        self._tick_count += 1
        reading = self.sensors.read()
        alarms = self.alarms.evaluate(reading)
        self._last_alarms = alarms
        payload = self.dashboard.publish(self.station_id, reading, alarms)
        return payload

    def run(self, cycles: int = 1, delay: float = 0.0) -> List[dict]:
        """Esegue N cicli; ritorna la lista dei payload pubblicati."""
        payloads: List[dict] = []
        for _ in range(cycles):
            payloads.append(self.tick())
            if delay > 0:
                time.sleep(delay)
        return payloads

    def status(self) -> dict:
        """Riepilogo dello stato corrente (utile per test / dashboard)."""
        return {
            "station_id": self.station_id,
            "running": self._running,
            "tick_count": self._tick_count,
            "last_sensor": self.sensors.last.as_dict() if self.sensors.last else None,
            "last_alarms": [str(a) for a in self._last_alarms],
            "dashboard_sent": self.dashboard.sent_count,
            "dashboard_failed": self.dashboard.failed_count,
        }


if __name__ == "__main__":
    lss = LifeSupportSystem()
    lss.start()
    lss.run(cycles=1)
    lss.stop()
