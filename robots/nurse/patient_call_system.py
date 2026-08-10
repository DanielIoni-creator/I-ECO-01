#!/usr/bin/env python3
"""
Patient Call System - wireless call button events, push notification queue,
nurse dashboard, and call history.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional


@dataclass(frozen=True)
class PatientCall:
    call_id: str
    patient_id: str
    room: str
    priority: str
    created_at: str
    status: str = "open"

    def as_dict(self) -> Dict[str, str]:
        return {
            "call_id": self.call_id,
            "patient_id": self.patient_id,
            "room": self.room,
            "priority": self.priority,
            "created_at": self.created_at,
            "status": self.status,
        }


@dataclass
class PatientCallSystem:
    calls: Dict[str, PatientCall] = field(default_factory=dict)
    push_notifications: List[Dict[str, str]] = field(default_factory=list)
    history: List[Dict[str, str]] = field(default_factory=list)

    def press_wireless_button(
        self,
        patient_id: str,
        room: str,
        priority: str = "normal",
        created_at: Optional[str] = None,
    ) -> Dict[str, str]:
        if priority not in {"normal", "urgent", "emergency"}:
            raise ValueError("priority must be normal, urgent, or emergency")
        if not patient_id or not room:
            raise ValueError("patient_id and room are required")

        call_id = f"CALL-{len(self.history) + len(self.calls) + 1:04d}"
        call = PatientCall(
            call_id=call_id,
            patient_id=patient_id,
            room=room,
            priority=priority,
            created_at=created_at or datetime.now(timezone.utc).isoformat(),
        )
        self.calls[call_id] = call
        notification = self._notify(call, "patient_call_opened")
        return {**call.as_dict(), "notification_id": notification["notification_id"]}

    def acknowledge_call(self, call_id: str, nurse_id: str) -> Dict[str, str]:
        call = self._get_call(call_id)
        if not nurse_id:
            raise ValueError("nurse_id is required")
        updated = PatientCall(**{**call.as_dict(), "status": "acknowledged"})
        self.calls[call_id] = updated
        self._notify(updated, "patient_call_acknowledged", nurse_id=nurse_id)
        return updated.as_dict()

    def resolve_call(self, call_id: str, nurse_id: str, notes: str = "") -> Dict[str, str]:
        call = self._get_call(call_id)
        if not nurse_id:
            raise ValueError("nurse_id is required")
        completed = {
            **call.as_dict(),
            "status": "resolved",
            "nurse_id": nurse_id,
            "notes": notes,
            "resolved_at": datetime.now(timezone.utc).isoformat(),
        }
        self.history.append(completed)
        del self.calls[call_id]
        self._notify(call, "patient_call_resolved", nurse_id=nurse_id)
        return completed

    def dashboard_snapshot(self) -> Dict[str, object]:
        open_calls = sorted(
            [call.as_dict() for call in self.calls.values()],
            key=lambda c: (self._priority_rank(c["priority"]), c["created_at"]),
        )
        return {
            "open_calls": open_calls,
            "open_count": len(open_calls),
            "history_count": len(self.history),
            "pending_push_notifications": len(self.push_notifications),
        }

    def _notify(self, call: PatientCall, event: str, nurse_id: Optional[str] = None) -> Dict[str, str]:
        notification = {
            "notification_id": f"PUSH-{len(self.push_notifications) + 1:04d}",
            "event": event,
            "call_id": call.call_id,
            "patient_id": call.patient_id,
            "room": call.room,
            "priority": call.priority,
            "nurse_id": nurse_id or "",
        }
        self.push_notifications.append(notification)
        return notification

    def _get_call(self, call_id: str) -> PatientCall:
        if call_id not in self.calls:
            raise KeyError(f"call {call_id} not found")
        return self.calls[call_id]

    def _priority_rank(self, priority: str) -> int:
        return {"emergency": 0, "urgent": 1, "normal": 2}[priority]


if __name__ == "__main__":
    system = PatientCallSystem()
    opened = system.press_wireless_button("P001", "Room 101", "urgent")
    print(opened)
    print(system.dashboard_snapshot())
