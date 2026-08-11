#!/usr/bin/env python3
"""
Simulazione del plasma e diagnostiche per la centrale a fusione.

Il simulatore e` deterministico: dato lo stesso seed produce la stessa
sequenza di stati. Espone un semplice modello "0.5D" (evoluzione
temporale di variabili globali) che include:

- Temperatura ionica T_i (keV)
- Temperatura elettronica T_e (keV)
- Densita` elettronica n_e (normalizzata a 10^20 m^-3)
- Tempo di confinamento tau_E (s)
- Pressione cinetica del plasma p (kPa)
- Fattore di guadagno Q istantaneo

Le letture dei sensori sintetici includono un piccolo rumore gaussiano
per riflettere il comportamento dei veri diagnostici Thomson scattering
e bolometri.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Callable, List, Optional

from .model import FusionModel


@dataclass
class PlasmaState:
    """Stato istantaneo del plasma."""

    timestamp: float
    temperature_kev: float
    electron_temperature_kev: float
    density_1e20_m3: float
    confinement_time_s: float
    q_factor: float
    kinetic_pressure_kpa: float
    regime: str = ""

    def as_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "temperature_kev": self.temperature_kev,
            "electron_temperature_kev": self.electron_temperature_kev,
            "density_1e20_m3": self.density_1e20_m3,
            "confinement_time_s": self.confinement_time_s,
            "q_factor": self.q_factor,
            "kinetic_pressure_kpa": self.kinetic_pressure_kpa,
            "regime": self.regime,
        }


class PlasmaSimulator:
    """Simulatore 0.5D del plasma per la centrale a fusione.

    Mantiene uno stato interno che evolve ad ogni chiamata di ``step()``.
    Il seed rende la simulazione deterministica.
    """

    def __init__(self,
                 model: Optional[FusionModel] = None,
                 seed: int = 42,
                 heating_power_mw: float = 25.0,
                 target_temperature_kev: Optional[float] = None) -> None:
        self.model = model or FusionModel()
        self._rng = random.Random(seed)
        self.heating_power_mw = heating_power_mw
        # Se l'utente non fissa un target, usiamo 1.1 * T_ign.
        self._target_T = (target_temperature_kev
                          or 1.1 * self.model.ignition_temperature_kev())
        self._t = 0.0
        self._dt = 1.0  # secondi simulati per step
        self._n = 0.9  # densita` iniziale
        self._Te = 5.0  # elettroni iniziano piu` freddi
        self._tau_E = 2.5
        self.state: Optional[PlasmaState] = None
        self.history: List[PlasmaState] = []

    def _gaussian(self, mean: float, sigma: float) -> float:
        return self._rng.gauss(mean, sigma)

    def _update_confinement(self) -> None:
        # Scaling ITER98(y,1) semplificato: tau_E ~ 0.05 * H * n^0.5 * T^0.5
        # (rappresentativo, non e` una calibrazione di macchina reale).
        H = 1.0  # fattore di enhancement
        n = max(0.1, self._n)
        T = max(0.1, self._Te)
        self._tau_E = 0.05 * H * math.sqrt(n) * math.sqrt(T)

    def _update_temperatures(self) -> None:
        # T_i tende al target con rilassamento esponenziale.
        # T_e segue T_i con un piccolo scarto (accoppiamento debole).
        alpha = 0.25
        self._t = self._t + self._dt
        # Rumore di misura realistico sui target heating.
        dT = alpha * (self._target_T - self._Ti) + self._gaussian(0, 0.2)
        self._Ti = max(0.1, self._Ti + dT)
        # T_e insegue T_i ma con un gap di 1-2 keV.
        gap = 1.0 + abs(self._gaussian(0, 0.1))
        self._Te = max(0.1, self._Ti - gap)

    def _update_density(self) -> None:
        # La densita` fluttua attorno a 1.0 con derive lente.
        drift = self._gaussian(0, 0.01)
        self._n = max(0.3, min(1.6, self._n + drift))

    def _compute_q(self) -> float:
        # Q = P_fusion / P_input (heating).
        t_ign = self.model.ignition_temperature_kev()
        # Approssimazione: Q = target_Q * (T/T_ign)^1.5, clampato a 4*target.
        if self._Ti < 0.5 * t_ign:
            return 0.0
        ratio = max(0.0, min(2.0, self._Ti / t_ign))
        return self.model.target_q * (ratio ** 1.5)

    def _compute_pressure(self) -> float:
        # Pressione cinetica: p = n * k_B * T (in unita` convenienti).
        # n in 10^20 m^-3, T in keV => p in kPa quando V e` 80 m^3.
        n = self._n
        T = self._Ti
        return n * T * 10.0  # fattore di scala per la stazione

    def step(self) -> PlasmaState:
        """Avanza la simulazione di un passo e ritorna il nuovo stato."""
        # Se e` il primo step, inizializza T_i al valore di accensione.
        if self.state is None:
            self._Ti = 0.6 * self.model.ignition_temperature_kev()
            self._Te = 0.5 * self.model.ignition_temperature_kev()
            self._n = 0.9
            self._tau_E = 2.5
        self._update_confinement()
        self._update_temperatures()
        self._update_density()
        q = self._compute_q()
        p = self._compute_pressure()
        regime = self.model.classify_regime(self._Ti)
        self.state = PlasmaState(
            timestamp=self._t,
            temperature_kev=self._Ti,
            electron_temperature_kev=self._Te,
            density_1e20_m3=self._n,
            confinement_time_s=self._tau_E,
            q_factor=q,
            kinetic_pressure_kpa=p,
            regime=regime,
        )
        self.history.append(self.state)
        return self.state

    def run(self, cycles: int = 5) -> List[PlasmaState]:
        """Esegue N passi di simulazione e ritorna gli stati."""
        return [self.step() for _ in range(cycles)]

    def diagnostics(self) -> dict:
        """Restituisce un riepilogo diagnostico per la dashboard."""
        if self.state is None:
            self.step()
        latest = self.state
        assert latest is not None
        # Terna temperatura: ioni, elettroni, target.
        t_ign = self.model.ignition_temperature_kev()
        return {
            "ion_temperature_kev": latest.temperature_kev,
            "electron_temperature_kev": latest.electron_temperature_kev,
            "target_ion_temperature_kev": self._target_T,
            "density_1e20_m3": latest.density_1e20_m3,
            "confinement_time_s": latest.confinement_time_s,
            "q_factor": latest.q_factor,
            "kinetic_pressure_kpa": latest.kinetic_pressure_kpa,
            "regime": latest.regime,
            "ignition_temperature_kev": t_ign,
            "ignition_ratio": latest.temperature_kev / t_ign,
            "samples": len(self.history),
        }
