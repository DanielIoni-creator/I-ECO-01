#!/usr/bin/env python3
"""
Alarm Manager - valuta le letture dei sensori e genera allarmi.
Le soglie operative sono ispirate a standard tipici di moduli abitati
(NASA-STD-3000 / ISS ECLSS). Ogni soglia e` configurabile per consentire
il test deterministico.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .sensors import SensorReading


@dataclass(frozen=True)
class Alarm:
    """Singolo allarme emesso dall'AlarmManager."""
    code: str
    severity: str   # "info" | "warning" | "critical"
    message: str

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.code}: {self.message}"


class AlarmManager:
    """Valuta una SensorReading e produce la lista allarmi."""

    DEFAULT_THRESHOLDS = {
        # O2: < 19.5% e` pericoloso, < 18% critico; > 23% rischio incendio.
        "oxygen_low_warning": 19.5,
        "oxygen_low_critical": 18.0,
        "oxygen_high_warning": 23.0,
        "oxygen_high_critical": 25.0,
        # CO2: > 1000 ppm fastidio, > 5000 ppm pericolo.
        "co2_warning": 1000.0,
        "co2_critical": 5000.0,
        # Acqua: < 95% warning, < 90% critico.
        "water_warning": 95.0,
        "water_critical": 90.0,
        # Temperatura: 18-26 C comfort, oltre allarme.
        "temp_low_warning": 18.0,
        "temp_low_critical": 15.0,
        "temp_high_warning": 26.0,
        "temp_high_critical": 30.0,
        # Umidita`: 30-60% comfort.
        "humidity_low_warning": 30.0,
        "humidity_low_critical": 20.0,
        "humidity_high_warning": 60.0,
        "humidity_high_critical": 70.0,
    }

    def __init__(self, thresholds: dict | None = None):
        merged = dict(self.DEFAULT_THRESHOLDS)
        if thresholds:
            merged.update(thresholds)
        self.thresholds = merged

    def evaluate(self, reading: SensorReading) -> List[Alarm]:
        alarms: List[Alarm] = []
        t = self.thresholds

        # O2
        if reading.oxygen_percent < t["oxygen_low_critical"]:
            alarms.append(Alarm("O2_CRIT_LOW", "critical",
                                 f"Ossigeno critico: {reading.oxygen_percent}% (< {t['oxygen_low_critical']}%)"))
        elif reading.oxygen_percent < t["oxygen_low_warning"]:
            alarms.append(Alarm("O2_WARN_LOW", "warning",
                                 f"Ossigeno basso: {reading.oxygen_percent}% (< {t['oxygen_low_warning']}%)"))
        elif reading.oxygen_percent > t["oxygen_high_critical"]:
            alarms.append(Alarm("O2_CRIT_HIGH", "critical",
                                 f"Ossigeno critico: {reading.oxygen_percent}% (> {t['oxygen_high_critical']}%)"))
        elif reading.oxygen_percent > t["oxygen_high_warning"]:
            alarms.append(Alarm("O2_WARN_HIGH", "warning",
                                 f"Ossigeno alto: {reading.oxygen_percent}% (> {t['oxygen_high_warning']}%)"))

        # CO2
        if reading.co2_ppm >= t["co2_critical"]:
            alarms.append(Alarm("CO2_CRIT", "critical",
                                 f"CO2 critico: {reading.co2_ppm} ppm (>= {t['co2_critical']})"))
        elif reading.co2_ppm >= t["co2_warning"]:
            alarms.append(Alarm("CO2_WARN", "warning",
                                 f"CO2 elevato: {reading.co2_ppm} ppm (>= {t['co2_warning']})"))

        # Acqua
        if reading.water_purity_percent < t["water_critical"]:
            alarms.append(Alarm("WATER_CRIT", "critical",
                                 f"Acqua contaminata: {reading.water_purity_percent}% (< {t['water_critical']}%)"))
        elif reading.water_purity_percent < t["water_warning"]:
            alarms.append(Alarm("WATER_WARN", "warning",
                                 f"Purezza acqua bassa: {reading.water_purity_percent}% (< {t['water_warning']}%)"))

        # Temperatura
        if reading.temperature_c < t["temp_low_critical"]:
            alarms.append(Alarm("TEMP_CRIT_LOW", "critical",
                                 f"Temperatura critica: {reading.temperature_c}°C (< {t['temp_low_critical']}°C)"))
        elif reading.temperature_c < t["temp_low_warning"]:
            alarms.append(Alarm("TEMP_WARN_LOW", "warning",
                                 f"Temperatura bassa: {reading.temperature_c}°C (< {t['temp_low_warning']}°C)"))
        elif reading.temperature_c > t["temp_high_critical"]:
            alarms.append(Alarm("TEMP_CRIT_HIGH", "critical",
                                 f"Temperatura critica: {reading.temperature_c}°C (> {t['temp_high_critical']}°C)"))
        elif reading.temperature_c > t["temp_high_warning"]:
            alarms.append(Alarm("TEMP_WARN_HIGH", "warning",
                                 f"Temperatura alta: {reading.temperature_c}°C (> {t['temp_high_warning']}°C)"))

        # Umidita`
        if reading.humidity_percent < t["humidity_low_critical"]:
            alarms.append(Alarm("HUM_CRIT_LOW", "critical",
                                 f"Umidita` critica: {reading.humidity_percent}% (< {t['humidity_low_critical']}%)"))
        elif reading.humidity_percent < t["humidity_low_warning"]:
            alarms.append(Alarm("HUM_WARN_LOW", "warning",
                                 f"Umidita` bassa: {reading.humidity_percent}% (< {t['humidity_low_warning']}%)"))
        elif reading.humidity_percent > t["humidity_high_critical"]:
            alarms.append(Alarm("HUM_CRIT_HIGH", "critical",
                                 f"Umidita` critica: {reading.humidity_percent}% (> {t['humidity_high_critical']}%)"))
        elif reading.humidity_percent > t["humidity_high_warning"]:
            alarms.append(Alarm("HUM_WARN_HIGH", "warning",
                                 f"Umidita` alta: {reading.humidity_percent}% (> {t['humidity_high_warning']}%)"))

        return alarms
