#!/usr/bin/env python3
"""
Medication Dispenser - dosage validation, QR authorization, administration
history, and XMR wallet payout metadata for nurse robot workflows.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from hashlib import sha256
from typing import Dict, List, Optional


@dataclass(frozen=True)
class MedicationOrder:
    order_id: str
    patient_id: str
    medication: str
    dosage_mg: int
    qr_secret_hash: str
    schedule: str


@dataclass
class MedicationDispenser:
    xmr_wallet_address: str
    inventory: Dict[str, int] = field(default_factory=dict)
    orders: Dict[str, MedicationOrder] = field(default_factory=dict)
    administrations: List[Dict[str, object]] = field(default_factory=list)

    def add_inventory(self, medication: str, units: int) -> int:
        if units <= 0:
            raise ValueError("units must be positive")
        self.inventory[medication] = self.inventory.get(medication, 0) + units
        return self.inventory[medication]

    def create_order(
        self,
        order_id: str,
        patient_id: str,
        medication: str,
        dosage_mg: int,
        qr_secret: str,
        schedule: str,
    ) -> MedicationOrder:
        if not all([order_id, patient_id, medication, qr_secret, schedule]):
            raise ValueError("order_id, patient_id, medication, qr_secret, and schedule are required")
        if dosage_mg <= 0:
            raise ValueError("dosage_mg must be positive")
        order = MedicationOrder(
            order_id=order_id,
            patient_id=patient_id,
            medication=medication,
            dosage_mg=dosage_mg,
            qr_secret_hash=self._hash_secret(qr_secret),
            schedule=schedule,
        )
        self.orders[order_id] = order
        return order

    def authorize_qr(self, order_id: str, qr_secret: str) -> bool:
        order = self._get_order(order_id)
        return order.qr_secret_hash == self._hash_secret(qr_secret)

    def dispense(
        self,
        order_id: str,
        qr_secret: str,
        nurse_id: str,
        administered_at: Optional[str] = None,
    ) -> Dict[str, object]:
        order = self._get_order(order_id)
        if not nurse_id:
            raise ValueError("nurse_id is required")
        if not self.authorize_qr(order_id, qr_secret):
            raise PermissionError("invalid QR authorization")
        if self.inventory.get(order.medication, 0) <= 0:
            raise RuntimeError(f"{order.medication} is out of stock")

        self.inventory[order.medication] -= 1
        record = {
            "order_id": order.order_id,
            "patient_id": order.patient_id,
            "medication": order.medication,
            "dosage_mg": order.dosage_mg,
            "nurse_id": nurse_id,
            "administered_at": administered_at or datetime.now(timezone.utc).isoformat(),
            "xmr_wallet_address": self.xmr_wallet_address,
            "inventory_remaining": self.inventory[order.medication],
            "status": "administered",
        }
        record["record_hash"] = sha256(str(sorted(record.items())).encode("utf-8")).hexdigest()
        self.administrations.append(record)
        return record

    def dashboard_snapshot(self) -> Dict[str, object]:
        return {
            "inventory": dict(self.inventory),
            "open_orders": len(self.orders),
            "administrations": list(self.administrations),
            "xmr_wallet_configured": bool(self.xmr_wallet_address),
        }

    def _get_order(self, order_id: str) -> MedicationOrder:
        if order_id not in self.orders:
            raise KeyError(f"order {order_id} not found")
        return self.orders[order_id]

    def _hash_secret(self, value: str) -> str:
        return sha256(value.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    dispenser = MedicationDispenser("xmr-wallet-placeholder")
    dispenser.add_inventory("Paracetamol", 4)
    dispenser.create_order("ORD-1", "P001", "Paracetamol", 500, "qr-token", "08:00")
    print(dispenser.dispense("ORD-1", "qr-token", "NURSE-1"))
