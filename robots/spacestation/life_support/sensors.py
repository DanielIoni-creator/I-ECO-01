#!/usr/bin/env python3
"""
Sensor Suite - Lettura sensori ossigeno, CO2, acqua, temperatura, umidita`.
Astratto sopra una semplice sorgente di letture; in produzione i valori
verranno letti da GPIO/I2C, qui sono simulati in modo deterministico.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional


@dataclass
class SensorReading:
    """Singola lettura aggregata di tutti i sensori vitali della stazione."""
    oxygen_percent: float = 21.0       # O2 frazione (nominale 21.0)
    co2_ppm: float = 400.0             # CO2 parti per milione (nominale 400)
    water_purity_percent: float = 100.0  # Purezza acqua del circuito (0-100)
    temperature_c: float = 22.0        # Temperatura cabina (C)
    humidity_percent: float = 45.0     # Umidita` relativa (0-100)
    timestamp: float = 0.0
    extra: Dict[str, float] = field(default_factory=dict)

    def as_dict(self) -> Dict[str, float]:
        base = {
            "oxygen_percent": self.oxygen_percent,
            "co2_ppm": self.co2_ppm,
            "water_purity_percent": self.water_purity_percent,
            "temperature_c": self.temperature_c,
            "humidity_percent": self.humidity_percent,
            "timestamp": self.timestamp,
        }
        base.update(self.extra)
        return base


class SensorSuite:
    """
    Collezione di sensori della cabina. Mantiene l'ultima lettura e
    ne permette l'aggiornamento tramite una funzione di lettura
    (sostituibile con adapter GPIO/I2C reali in produzione).
    """

    def __init__(self, reader: Optional[Callable[[], SensorReading]] = None,
                 seed: Optional[int] = None):
        self._reader = reader
        self._last: Optional[SensorReading] = None
        if seed is not None:
            self._rng = random.Random(seed)
        else:
            self._rng = random.Random()

    def set_reader(self, reader: Callable[[], SensorReading]) -> None:
        """Installa un lettore esterno (es. driver reale)."""
        self._reader = reader

    def _default_reading(self) -> SensorReading:
        """Lettura simulata stazionaria intorno ai valori nominali."""
        return SensorReading(
            oxygen_percent=round(21.0 + self._rng.uniform(-0.5, 0.5), 2),
            co2_ppm=round(400.0 + self._rng.uniform(-50.0, 50.0), 1),
            water_purity_percent=round(99.5 + self._rng.uniform(-0.5, 0.4), 2),
            temperature_c=round(22.0 + self._rng.uniform(-0.5, 0.5), 2),
            humidity_percent=round(45.0 + self._rng.uniform(-2.0, 2.0), 1),
            timestamp=self._last.timestamp + 1.0 if self._last else 0.0,
        )

    def read(self) -> SensorReading:
        """Legge i sensori e memorizza l'ultimo valore."""
        reading = self._reader() if self._reader else self._default_reading()
        self._last = reading
        return reading

    @property
    def last(self) -> Optional[SensorReading]:
        return self._last
