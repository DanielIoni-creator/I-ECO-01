#!/usr/bin/env python3
"""
Fusion Power Integration - Pulsar Technology for MyZubster Space Station.

Sub-package che integra i principi della fusione aneutronica (Pulsar Sunbird)
nella centrale energetica della Space Station MyZubster.

Componenti esportati:
- FusionPowerPlant: orchestratore centrale
- FusionModel: modello teorico aneutronico (D-T / T-T / p-11B)
- PlasmaSimulator: simulazione plasma con diagnostiche
- PropulsionModule: stime di spinta e Isp dal plasma
- FusionDashboardClient: client per la dashboard
- AICoreHook: integrazione con AI Core della stazione

Test: ``python3 -m unittest robots.spacestation.fusion_power.test_fusion_power -v``
"""

from .ai_core import AICoreHook, AIDecision
from .dashboard import FusionDashboardClient
from .fusion_power import FusionPowerPlant
from .model import FusionModel, FusionReaction
from .plasma import PlasmaSimulator, PlasmaState
from .propulsion import PropulsionModule

__all__ = [
    "FusionPowerPlant",
    "FusionModel",
    "FusionReaction",
    "PlasmaSimulator",
    "PlasmaState",
    "PropulsionModule",
    "FusionDashboardClient",
    "AICoreHook",
    "AIDecision",
]

__version__ = "1.0.0"
