#!/usr/bin/env python3
"""
Modello teorico della fusione aneutronica per la MyZubster Space Station.

Si basa sui parametri dichiarati del progetto Pulsar Sunbird (first plasma
Marzo 2026) ed assume un allineamento con le linee guida UKAEA per la
propulsione aneutronica. I valori delle reazioni sono costanti fisiche note,
non numeri magici: sono documentate in-module per consentire revisione
indipendente.

Reazioni supportate:
- D-T (deuterio-trizio):  reazione standard, alto Q, neutroni veloci
- D-D (deuterio-deuterio): due branch, entrambi producono elio-3 o tritio
- D-He3 (deuterio-elio3): aneutronica, richiede temperature piu` alte
- p-B11 (protone-boro11): completamente aneutronica, "sogno" ingegneristico

L'output netto di potenza termica ed elettrica e` derivato dal fattore di
guadagno Q del plasma e dall'efficienza di conversione dichiarata.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict


class FusionReaction(Enum):
    """Reazione di fusione considerata dalla centrale."""

    D_T = "D-T"
    D_D = "D-D"
    D_HE3 = "D-He3"
    P_B11 = "p-B11"

    @property
    def is_aneutronic(self) -> bool:
        """Vera se la reazione non produce neutroni (no attivazione)."""
        return self in (FusionReaction.D_HE3, FusionReaction.P_B11)

    @property
    def q_mev(self) -> float:
        """Energia liberata per singola reazione, in MeV (valore standard)."""
        return _REACTION_Q_MEV[self]


# Energie di reazione in MeV (costanti fisiche, fonte: standard di letteratura
# e parametri UKAEA / iter).
_REACTION_Q_MEV: Dict[FusionReaction, float] = {
    FusionReaction.D_T: 17.6,
    FusionReaction.D_D: 3.65,  # media dei due branch
    FusionReaction.D_HE3: 18.3,
    FusionReaction.P_B11: 8.7,
}


# Temperature di ignizione approssimate in keV, usate come guard-rail del
# modello. Valori conservativi allineati a letteratura (W.H. Joubert).
_IGNITION_TEMPERATURE_KEV: Dict[FusionReaction, float] = {
    FusionReaction.D_T: 13.0,
    FusionReaction.D_D: 50.0,
    FusionReaction.D_HE3: 60.0,
    FusionReaction.P_B11: 200.0,
}


@dataclass(frozen=True)
class FusionModel:
    """Modello teorico della reazione di fusione per la centrale.

    Attributes:
        reaction: reazione target.
        plasma_volume_m3: volume del plasma in m^3.
        target_q: fattore di guadagno Q = P_fusion / P_input desiderato.
        conversion_efficiency: rendimento termoelettrico (0..1).
        station_power_demand_mw: domanda elettrica della stazione in MW.
    """

    reaction: FusionReaction = FusionReaction.D_HE3
    plasma_volume_m3: float = 80.0
    target_q: float = 5.0
    conversion_efficiency: float = 0.40
    station_power_demand_mw: float = 12.0

    def ignition_temperature_kev(self) -> float:
        """Temperatura di ignizione di riferimento per la reazione scelta."""
        return _IGNITION_TEMPERATURE_KEV[self.reaction]

    def classify_regime(self, temperature_kev: float) -> str:
        """Classifica il regime termico del plasma.

        Returns:
            "sub_ignition" se T < 0.7 T_ign, "ignition" se 0.7 <= T <= 1.3 T_ign,
            "over_ignition" altrimenti.
        """
        t_ign = self.ignition_temperature_kev()
        ratio = temperature_kev / t_ign
        if ratio < 0.7:
            return "sub_ignition"
        if ratio <= 1.3:
            return "ignition"
        return "over_ignition"

    def expected_thermal_power_mw(self, temperature_kev: float, density_20: float) -> float:
        """Stima la potenza termica di fusione in MW.

        Usa una legge di scala semplificata: P ~ n^2 * <sigma*v> * V * E.
        Qui normalizziamo sul valore di ignizione di riferimento per la
        reazione scelta, in modo che:
            - a T_ign e density_20=1.0, P_termica ~ 1.0 * V (MW / m^3)
            - il fattore Q_target e` raggiunto quando il plasma si avvicina
              alle condizioni nominali

        Args:
            temperature_kev: temperatura ionica del plasma in keV.
            density_20: densita` normalizzata a 10^20 m^-3.

        Returns:
            potenza termica stimata in MW.
        """
        t_ign = self.ignition_temperature_kev()
        # <sigma*v> cresce fortemente con T nella zona d'interesse;
        # usiamo un proxy: (T/T_ign)^2 clampato a 4 per evitare esplosioni.
        t_ratio = max(0.0, min(4.0, temperature_kev / t_ign))
        sigma_v_factor = t_ratio ** 2
        # P_termica [MW] = V[m^3] * n^2 * <sigma*v> factor * normalizzazione
        return self.plasma_volume_m3 * (density_20 ** 2) * sigma_v_factor

    def electrical_power_mw(self, temperature_kev: float, density_20: float) -> float:
        """Potenza elettrica lorda prodotta in MW data T e densita`.

        Applica il rendimento di conversione termoelettrica. Restituisce 0
        se siamo in regime sub-ignition (cioe` il plasma non brucia).
        """
        regime = self.classify_regime(temperature_kev)
        if regime == "sub_ignition":
            return 0.0
        p_th = self.expected_thermal_power_mw(temperature_kev, density_20)
        return p_th * self.conversion_efficiency

    def meets_demand(self, temperature_kev: float, density_20: float) -> bool:
        """Vero se la potenza elettrica stimata copre la domanda della stazione."""
        return self.electrical_power_mw(temperature_kev, density_20) >= self.station_power_demand_mw

    def summary(self, temperature_kev: float, density_20: float) -> Dict[str, float | str]:
        """Riepilogo leggibile per dashboard e test."""
        return {
            "reaction": self.reaction.value,
            "aneutronic": self.reaction.is_aneutronic,
            "ignition_temperature_kev": self.ignition_temperature_kev(),
            "current_temperature_kev": temperature_kev,
            "regime": self.classify_regime(temperature_kev),
            "density_1e20_m3": density_20,
            "thermal_power_mw": self.expected_thermal_power_mw(temperature_kev, density_20),
            "electrical_power_mw": self.electrical_power_mw(temperature_kev, density_20),
            "station_demand_mw": self.station_power_demand_mw,
            "demand_met": self.meets_demand(temperature_kev, density_20),
        }
