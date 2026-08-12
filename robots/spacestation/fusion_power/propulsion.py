#!/usr/bin/env python3
"""
Modulo di propulsione avanzata aneutronica.

Stima spinta e impulso specifico (Isp) a partire dai parametri del plasma
e della reazione scelta. Le formule usate sono semplificate ma mantengono
le dipendenze qualitative corrette:

- Isp cresce con sqrt(Q * E_reazione) (la temperatura "scarica" piu` velocita`)
- La spinta cresce con la portata di massa espulsa

Per la propulsione spaziale con reazioni aneutroniche (D-He3, p-B11) la
maggior parte dell'energia va nelle particelle cariche, che possono essere
dirette magneticamente per generare spinta senza le perdite di un ciclo
termodinamico.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from .model import FusionModel


# Costanti utili
EV_TO_JOULES = 1.602176634e-19
MEV_TO_JOULES = EV_TO_JOULES * 1e6


@dataclass
class PropulsionModule:
    """Propulsione derivata dal plasma di fusione.

    Args:
        exhaust_mass_flow_kg_s: portata di massa espulsa in kg/s.
        nozzle_efficiency: rendimento dell'ugello (0..1).
    """

    model: FusionModel
    exhaust_mass_flow_kg_s: float = 0.001
    nozzle_efficiency: float = 0.75

    def specific_impulse_s(self) -> float:
        """Impulso specifico in secondi.

        Approssimazione: Isp ~ nozzle_eff * sqrt(2 * Q * E_reaction / m_kg).
        Dove m_kg e` la massa "efficace" espulsa per reazione, posta a 4 amu
        (elio-4) come valore rappresentativo per i prodotti di fusione
        leggeri. Il fattore Q qui e` un proxy della temperatura del plasma
        in unita` di T_ign (clampato a 2 per ragioni fisiche).

        Per mantenere i numeri in range realistico per una propulsione
        aneutronica spaziale (10^4 - 10^6 s) introduciamo un fattore di
        condivisione del ciclo termico eta_cycle = 0.2 (solo una frazione
        dell'energia di reazione va direttamente in energia cinetica di
        scarico; il resto resta nel plasma per il ciclo).
        """
        e_joules = self.model.reaction.q_mev * MEV_TO_JOULES
        # Massa espulsa per reazione: 4 amu = 4 * 1.66e-27 kg.
        m_per_reaction = 4.0 * 1.66053906660e-27
        t_ign = self.model.ignition_temperature_kev()
        # Temperativa temperatura: T_eff in unita` di t_ign, clamp 0..2.
        # Senza misura diretta di T, usiamo 1.0 (regime nominale).
        t_norm = 1.0
        q_eff = max(0.1, min(2.0, t_norm))
        eta_cycle = 0.2  # solo una frazione diventa spinta
        v_exhaust = math.sqrt(2.0 * q_eff * e_joules * eta_cycle / m_per_reaction)
        return self.nozzle_efficiency * v_exhaust / 9.80665

    def thrust_newton(self) -> float:
        """Spinta in Newton."""
        # v_exhaust in m/s: dall'impulso specifico, v = Isp * g0.
        v_exhaust = self.specific_impulse_s() * 9.80665
        return self.exhaust_mass_flow_kg_s * v_exhaust

    def summary(self) -> dict:
        return {
            "reaction": self.model.reaction.value,
            "aneutronic": self.model.reaction.is_aneutronic,
            "specific_impulse_s": self.specific_impulse_s(),
            "thrust_newton": self.thrust_newton(),
            "exhaust_mass_flow_kg_s": self.exhaust_mass_flow_kg_s,
            "nozzle_efficiency": self.nozzle_efficiency,
        }
