#!/usr/bin/env python3
"""
Life Support System - Space Station
Modulo di supporto vitale per la Space Station MyZubster.
Esporta LifeSupportSystem, SensorSuite, AlarmManager, DashboardClient.
"""

from .life_support import LifeSupportSystem
from .sensors import SensorSuite, SensorReading
from .alarms import AlarmManager, Alarm
from .dashboard import DashboardClient

__all__ = [
    "LifeSupportSystem",
    "SensorSuite",
    "SensorReading",
    "AlarmManager",
    "Alarm",
    "DashboardClient",
]

__version__ = "1.0.0"
