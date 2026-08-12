#!/usr/bin/env python3
"""
Hook di integrazione con l'AI Core della MyZubster Space Station.

L'AI Core puo`:
- consumare lo stato del plasma e produrre decisioni di controllo
  (aumenta riscaldamento, modula densita`, spegni, mantieni, ...)
- ricevere feedback dalle decisioni precedenti (closed-loop)

Questo modulo e` un'interfaccia pura: non importa l'AI Core, espone solo
l'API che l'AI Core dovra` implementare. Cio` mantiene il pacchetto
``fusion_power`` self-contained, senza dipendenze esterne.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional, Protocol

from .plasma import PlasmaState


class ControlAction(str, Enum):
    """Azione di controllo che l'AI Core puo` richiedere."""

    HOLD = "hold"
    INCREASE_HEAT = "increase_heat"
    DECREASE_HEAT = "decrease_heat"
    INCREASE_FUEL = "increase_fuel"
    DECREASE_FUEL = "decrease_fuel"
    RAMP_DOWN = "ramp_down"
    EMERGENCY_SHUTDOWN = "emergency_shutdown"


@dataclass(frozen=True)
class AIDecision:
    """Decisione dell'AI Core relativa al controllo del plasma."""

    action: ControlAction
    confidence: float  # 0..1
    reason: str


class AICoreLike(Protocol):
    """Protocollo che l'AI Core della stazione deve implementare.

    Esporre ``decide(plasma) -> AIDecision`` consente di iniettare qualunque
    implementazione reale (modello locale, remoto, rule-based, ...) senza
    dover importare nulla di pesante qui dentro.
    """

    def decide(self, plasma: PlasmaState) -> AIDecision:  # pragma: no cover - protocol
        ...


class AICoreHook:
    """Bridge tra la centrale a fusione e l'AI Core.

    Mantiene lo storico delle decisioni e consente di fornire un fallback
    rule-based se l'AI Core non e` disponibile.
    """

    def __init__(self,
                 core: Optional[AICoreLike] = None,
                 fallback: Optional[Callable[[PlasmaState], AIDecision]] = None) -> None:
        self._core = core
        self._fallback = fallback or self._default_fallback
        self.history: list[tuple[PlasmaState, AIDecision]] = []

    @staticmethod
    def _default_fallback(plasma: PlasmaState) -> AIDecision:
        """Fallback rule-based: comportamento di sicurezza minimo."""
        if plasma.q_factor <= 0.0:
            return AIDecision(
                action=ControlAction.INCREASE_HEAT,
                confidence=0.5,
                reason="plasma not yet burning",
            )
        if plasma.regime == "over_ignition":
            return AIDecision(
                action=ControlAction.DECREASE_HEAT,
                confidence=0.7,
                reason="over-ignition: reduce heating",
            )
        if plasma.regime == "sub_ignition":
            return AIDecision(
                action=ControlAction.INCREASE_HEAT,
                confidence=0.7,
                reason="sub-ignition: add heating",
            )
        return AIDecision(
            action=ControlAction.HOLD,
            confidence=0.9,
            reason="nominal regime",
        )

    def decide(self, plasma: PlasmaState) -> AIDecision:
        """Chiede una decisione all'AI Core (o al fallback) e la registra."""
        if self._core is not None:
            try:
                decision = self._core.decide(plasma)
            except Exception as exc:  # noqa: BLE001
                decision = AIDecision(
                    action=ControlAction.RAMP_DOWN,
                    confidence=0.3,
                    reason=f"ai core error: {exc}",
                )
        else:
            decision = self._fallback(plasma)
        self.history.append((plasma, decision))
        return decision

    def feedback(self, success: bool, note: str = "") -> None:
        """Annota l'ultima decisione con un feedback (per training on-line)."""
        if not self.history:
            return
        _plasma, decision = self.history[-1]
        # Marca l'esito sul dataclass "freezing" in modo non distruttivo.
        # AIDecision e` frozen, quindi creiamo un record di feedback a parte.
        self.history[-1] = (_plasma, AIDecision(
            action=decision.action,
            confidence=decision.confidence,
            reason=decision.reason + ("" if not note else f" | feedback={note} ok={success}"),
        ))
