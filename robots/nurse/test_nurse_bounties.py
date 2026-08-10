import unittest

from medication_dispenser import MedicationDispenser
from patient_call_system import PatientCallSystem
from monitor.vital_monitor import VitalSignsMonitor, VitalThresholds


class VitalSignsMonitorTests(unittest.TestCase):
    def test_records_vitals_alerts_and_blockchain_hashes(self):
        monitor = VitalSignsMonitor(
            VitalThresholds(max_heart_rate=100, min_spo2=94, max_temperature_c=37.8)
        )

        result = monitor.record_reading("P001", heart_rate=130, spo2=91, temperature_c=38.5)

        self.assertEqual(result["status"], "critical")
        self.assertEqual([alarm["code"] for alarm in result["alarms"]], [
            "heart_rate_high",
            "spo2_low",
            "temperature_high",
        ])
        self.assertEqual(len(monitor.blockchain_log), 1)
        self.assertEqual(len(monitor.blockchain_log[0]["hash"]), 64)

    def test_dashboard_returns_latest_patient_status(self):
        monitor = VitalSignsMonitor()
        monitor.record_reading("P001", heart_rate=80, spo2=98, temperature_c=36.8)
        monitor.record_reading("P001", heart_rate=88, spo2=97, temperature_c=36.9)

        snapshot = monitor.dashboard_snapshot()

        self.assertEqual(snapshot["patient_count"], 1)
        self.assertEqual(snapshot["patients"][0]["heart_rate"], 88)
        self.assertEqual(snapshot["patients"][0]["status"], "stable")


class MedicationDispenserTests(unittest.TestCase):
    def test_qr_authorized_dispense_logs_administration(self):
        dispenser = MedicationDispenser("xmr-wallet")
        dispenser.add_inventory("Amoxicillin", 2)
        dispenser.create_order("O-1", "P002", "Amoxicillin", 250, "secret", "14:00")

        record = dispenser.dispense("O-1", "secret", "N-1")

        self.assertEqual(record["status"], "administered")
        self.assertEqual(record["inventory_remaining"], 1)
        self.assertEqual(len(record["record_hash"]), 64)
        self.assertEqual(dispenser.dashboard_snapshot()["administrations"][0]["order_id"], "O-1")

    def test_invalid_qr_is_rejected_without_inventory_change(self):
        dispenser = MedicationDispenser("xmr-wallet")
        dispenser.add_inventory("Aspirin", 1)
        dispenser.create_order("O-2", "P003", "Aspirin", 100, "correct", "09:00")

        with self.assertRaises(PermissionError):
            dispenser.dispense("O-2", "wrong", "N-2")

        self.assertEqual(dispenser.inventory["Aspirin"], 1)
        self.assertEqual(dispenser.administrations, [])


class PatientCallSystemTests(unittest.TestCase):
    def test_patient_button_creates_notification_and_dashboard_entry(self):
        system = PatientCallSystem()

        call = system.press_wireless_button("P004", "Room 12", "emergency")

        self.assertEqual(call["status"], "open")
        self.assertEqual(call["notification_id"], "PUSH-0001")
        snapshot = system.dashboard_snapshot()
        self.assertEqual(snapshot["open_count"], 1)
        self.assertEqual(snapshot["open_calls"][0]["priority"], "emergency")

    def test_acknowledge_and_resolve_moves_call_to_history(self):
        system = PatientCallSystem()
        call = system.press_wireless_button("P005", "Room 20")

        acknowledged = system.acknowledge_call(call["call_id"], "N-3")
        resolved = system.resolve_call(call["call_id"], "N-3", "Patient assisted")

        self.assertEqual(acknowledged["status"], "acknowledged")
        self.assertEqual(resolved["status"], "resolved")
        self.assertEqual(system.dashboard_snapshot()["open_count"], 0)
        self.assertEqual(system.dashboard_snapshot()["history_count"], 1)


if __name__ == "__main__":
    unittest.main()
