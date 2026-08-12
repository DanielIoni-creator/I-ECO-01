#!/usr/bin/env python3
"""
Orchestratore della centrale a fusione Pulsar per la Space Station MyZubster.

Coordina:
- ``FusionModel`` (modello teorico)
- ``PlasmaSimulator`` (stato del plasma)
- ``PropulsionModule`` (spinta / Isp)
- ``FusionDashboardClient`` (pubblicazione stato)
- ``AICoreHook`` (controllo AI)

Ciclo di vita:
1. ``start()`` inizializza i componenti e l'AI Core hook.
2. ``tick()`` esegue un ciclo (simula plasma, calcola potenza, consulta AI
   Core, pubblica su dashboard).
3. ``run(cycles)`` esegue N cicli.
4. ``stop()`` arresta la centrale.
"""

from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, Optional

from .ai_core import AICoreHook, AICoreLike, AIDecision, ControlAction
from .dashboard import FusionDashboardClient
from .model import FusionModel, FusionReaction
from .plasma import PlasmaSimulator, PlasmaState
from .propulsion import PropulsionModule


class FusionPowerPlant:
    """Centrale a fusione aneutronica Pulsar per la Space Station MyZubster."""

    def __init__(self,
                 station_id: str = "I-ECO-01",
                 model: Optional[FusionModel] = None,
                 simulator: Optional[PlasmaSimulator] = None,
                 propulsion: Optional[PropulsionModule] = None,
                 dashboard: Optional[FusionDashboardClient] = None,
                 ai_hook: Optional[AICoreHook] = None,
                 clock: Callable[[], float] = time.time) -> None:
        self.station_id = station_id
        self.model = model or FusionModel(reaction=FusionReaction.D_HE3)
        self.simulator = simulator or PlasmaSimulator(model=self.model, seed=42)
        self.propulsion = propulsion or PropulsionModule(model=self.model)
        self.dashboard = dashboard or FusionDashboardClient()
        self.ai_hook = ai_hook or AICoreHook()
        self._clock = clock
        self._running = False
        self._tick_count = 0
        self.last_plasma: Optional[PlasmaState] = None
        self.last_decision: Optional[AIDecision] = None
        self._payloads: List[Dict[str, Any]] = []

    # ------------------ ciclo di vita ------------------

    def start(self) -> None:
        self._running = True
        print(f"⚛️  Fusion Power Plant avviata su {self.station_id} "
              f"(reazione: {self.model.reaction.value})")

    def stop(self) -> None:
        self._running = False
        print("🛑 Fusion Power Plant arrestata")

    @property
    def payloads(self) -> List[Dict[str, Any]]:
        return list(self._payloads)

    # ------------------ logica di ciclo ------------------

    def _consult_ai(self, plasma: PlasmaState) -> AIDecision:
        decision = self.ai_hook.decide(plasma)
        self.last_decision = decision
        # Azioni di sicurezza.
        if decision.action == ControlAction.EMERGENCY_SHUTDOWN:
            self._running = False
        return decision

    def tick(self) -> Dict[str, Any]:
        if not self._running:
            raise RuntimeError("FusionPowerPlant non avviata (chiamare start())")
        self._tick_count += 1
        plasma = self.simulator.step()
        self.last_plasma = plasma
        decision = self._consult_ai(plasma)
        e_mw = self.model.electrical_power_mw(plasma.temperature_kev, plasma.density_1e20_m3)
        payload = self.dashboard.publish(
            self.station_id,
            plasma,
            self.propulsion,
            e_mw,
            self.model.station_power_demand_mw,
            plasma.regime,
        )
        if decision.action == ControlAction.INCREASE_HEAT:
            self.simulator.heating_power_mw *= 1.1
        elif decision.action == ControlAction.DECREASE_HEAT:
            self.simulator.heating_power_mw *= 0.9
        elif decision.action == ControlAction.RAMP_DOWN:
            self.simulator.heating_power_mw *= 0.5
        self._payloads.append(payload)
        return payload

    def run(self, cycles: int = 1, delay: float = 0.0) -> List[Dict[str, Any]]:
        out: List[Dict[str, Any]] = []
        for _ in range(cycles):
            out.append(self.tick())
            if delay > 0:
                time.sleep(delay)
        return out

    def status(self) -> Dict[str, Any]:
        plasma = self.last_plasma
        return {
            "station_id": self.station_id,
            "running": self._running,
            "tick_count": self._tick_count,
            "reaction": self.model.reaction.value,
            "plasma": plasma.as_dict() if plasma is not None else None,
            "last_decision": (
                {
                    "action": self.last_decision.action.value,
                    "confidence": self.last_decision.confidence,
                    "reason": self.last_decision.reason,
                }
                if self.last_decision is not None else None
            ),
            "dashboard_sent": self.dashboard.sent_count,
            "dashboard_failed": self.dashboard.failed_count,
            "propulsion": self.propulsion.summary(),
        }


if __name__ == "__main__":
    plant = FusionPowerPlant()
    plant.start()
    plant.run(cycles=3)
    print(plant.status())
    plant.stop()
