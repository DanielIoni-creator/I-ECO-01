#!/usr/bin/env python3
"""
Unit tests per il modulo Life Support System.
Eseguibili con: python3 -m unittest robots.spacestation.life_support.test_life_support
"""

import unittest

from robots.spacestation.life_support.alarms import Alarm, AlarmManager
from robots.spacestation.life_support.dashboard import DashboardClient
from robots.spacestation.life_support.life_support import LifeSupportSystem
from robots.spacestation.life_support.sensors import SensorReading, SensorSuite


def _r(**overrides) -> SensorReading:
    base = dict(
        oxygen_percent=21.0,
        co2_ppm=400.0,
        water_purity_percent=100.0,
        temperature_c=22.0,
        humidity_percent=45.0,
        timestamp=0.0,
    )
    base.update(overrides)
    return SensorReading(**base)


class TestSensorSuite(unittest.TestCase):
    def test_default_reader_is_deterministic_around_nominal(self):
        s = SensorSuite(seed=42)
        r = s.read()
        # valori nominali +/- jitter
        self.assertAlmostEqual(r.oxygen_percent, 21.0, delta=1.0)
        self.assertAlmostEqual(r.co2_ppm, 400.0, delta=100.0)
        self.assertAlmostEqual(r.temperature_c, 22.0, delta=1.0)
        self.assertGreaterEqual(r.water_purity_percent, 90.0)
        self.assertLessEqual(r.humidity_percent, 100.0)
        self.assertIs(s.last, r)

    def test_custom_reader_used(self):
        sentinel = _r(oxygen_percent=18.0, co2_ppm=200.0)
        s = SensorSuite(reader=lambda: sentinel)
        self.assertIs(s.read(), sentinel)


class TestAlarmManager(unittest.TestCase):
    def setUp(self):
        self.am = AlarmManager()

    def test_nominal_reading_has_no_alarms(self):
        self.assertEqual(self.am.evaluate(_r()), [])

    def test_oxygen_low_critical(self):
        alarms = self.am.evaluate(_r(oxygen_percent=17.0))
        codes = [a.code for a in alarms]
        self.assertIn("O2_CRIT_LOW", codes)
        self.assertEqual(alarms[0].severity, "critical")

    def test_oxygen_low_warning(self):
        alarms = self.am.evaluate(_r(oxygen_percent=19.0))
        codes = [a.code for a in alarms]
        self.assertIn("O2_WARN_LOW", codes)
        self.assertNotIn("O2_CRIT_LOW", codes)

    def test_oxygen_high_critical(self):
        alarms = self.am.evaluate(_r(oxygen_percent=27.0))
        self.assertIn("O2_CRIT_HIGH", [a.code for a in alarms])

    def test_co2_warning_and_critical(self):
        warn = self.am.evaluate(_r(co2_ppm=2000.0))
        crit = self.am.evaluate(_r(co2_ppm=8000.0))
        self.assertIn("CO2_WARN", [a.code for a in warn])
        self.assertIn("CO2_CRIT", [a.code for a in crit])

    def test_water_purity(self):
        self.assertIn("WATER_WARN", [a.code for a in self.am.evaluate(_r(water_purity_percent=92.0))])
        self.assertIn("WATER_CRIT", [a.code for a in self.am.evaluate(_r(water_purity_percent=85.0))])

    def test_temperature(self):
        self.assertIn("TEMP_WARN_LOW", [a.code for a in self.am.evaluate(_r(temperature_c=17.0))])
        self.assertIn("TEMP_CRIT_LOW", [a.code for a in self.am.evaluate(_r(temperature_c=10.0))])
        self.assertIn("TEMP_WARN_HIGH", [a.code for a in self.am.evaluate(_r(temperature_c=27.0))])
        self.assertIn("TEMP_CRIT_HIGH", [a.code for a in self.am.evaluate(_r(temperature_c=33.0))])

    def test_humidity(self):
        self.assertIn("HUM_WARN_LOW", [a.code for a in self.am.evaluate(_r(humidity_percent=25.0))])
        self.assertIn("HUM_CRIT_LOW", [a.code for a in self.am.evaluate(_r(humidity_percent=15.0))])
        self.assertIn("HUM_WARN_HIGH", [a.code for a in self.am.evaluate(_r(humidity_percent=65.0))])
        self.assertIn("HUM_CRIT_HIGH", [a.code for a in self.am.evaluate(_r(humidity_percent=75.0))])

    def test_custom_thresholds_override_defaults(self):
        am = AlarmManager({"oxygen_low_warning": 22.0})
        alarms = am.evaluate(_r(oxygen_percent=21.5))
        # con soglia a 22% e lettura 21.5% deve scattare il warning
        self.assertIn("O2_WARN_LOW", [a.code for a in alarms])

    def test_alarm_dataclass_string(self):
        a = Alarm("TEST", "warning", "msg")
        s = str(a)
        self.assertIn("WARNING", s)
        self.assertIn("TEST", s)
        self.assertIn("msg", s)


class TestDashboardClient(unittest.TestCase):
    def test_build_payload_includes_alarms(self):
        client = DashboardClient()
        reading = _r()
        alarms = [Alarm("X", "warning", "y")]
        payload = client.build_payload("S1", reading, alarms)
        self.assertEqual(payload["station_id"], "S1")
        self.assertEqual(payload["alarm_count"], 1)
        self.assertEqual(payload["alarms"][0]["code"], "X")
        self.assertFalse(payload["critical"])

    def test_payload_marks_critical(self):
        client = DashboardClient()
        alarms = [Alarm("X", "critical", "y")]
        payload = client.build_payload("S1", _r(), alarms)
        self.assertTrue(payload["critical"])

    def test_publish_records_outcome_via_transport(self):
        class FakeResp:
            status_code = 200
        class FakeTransport:
            def __init__(self):
                self.calls = []
            def post(self, url, json, timeout):
                self.calls.append((url, json, timeout))
                return FakeResp()
        t = FakeTransport()
        client = DashboardClient(endpoint="https://dash/api")
        client.publish("S1", _r(), [], transport=t)
        self.assertEqual(len(t.calls), 1)
        self.assertEqual(t.calls[0][0], "https://dash/api")
        self.assertEqual(client.sent_count, 1)
        self.assertEqual(client.failed_count, 0)

    def test_publish_records_failure(self):
        class FakeTransport:
            def post(self, *a, **kw):
                raise ConnectionError("down")
        client = DashboardClient()
        client.publish("S1", _r(), [], transport=FakeTransport())
        self.assertEqual(client.failed_count, 1)
        self.assertEqual(client.sent_count, 0)


class TestLifeSupportSystem(unittest.TestCase):
    def test_tick_requires_start(self):
        lss = LifeSupportSystem(sensors=SensorSuite(reader=lambda: _r()))
        with self.assertRaises(RuntimeError):
            lss.tick()

    def test_tick_publishes_to_dashboard(self):
        lss = LifeSupportSystem(
            station_id="ST-1",
            sensors=SensorSuite(reader=lambda: _r()),
            dashboard=DashboardClient(),
        )
        lss.start()
        payload = lss.tick()
        self.assertEqual(payload["station_id"], "ST-1")
        self.assertEqual(payload["alarm_count"], 0)
        self.assertFalse(payload["critical"])
        self.assertEqual(lss.status()["tick_count"], 1)

    def test_tick_emits_critical_alarm(self):
        lss = LifeSupportSystem(
            sensors=SensorSuite(reader=lambda: _r(oxygen_percent=17.0)),
            dashboard=DashboardClient(),
        )
        lss.start()
        payload = lss.tick()
        self.assertTrue(payload["critical"])
        self.assertEqual(payload["alarms"][0]["code"], "O2_CRIT_LOW")

    def test_run_runs_n_cycles(self):
        calls = {"n": 0}
        def reader():
            calls["n"] += 1
            return _r()
        lss = LifeSupportSystem(sensors=SensorSuite(reader=reader))
        lss.start()
        out = lss.run(cycles=5)
        self.assertEqual(len(out), 5)
        self.assertEqual(calls["n"], 5)

    def test_status_shape(self):
        lss = LifeSupportSystem(sensors=SensorSuite(reader=lambda: _r()))
        lss.start()
        lss.tick()
        s = lss.status()
        self.assertEqual(s["station_id"], "I-ECO-01")
        self.assertTrue(s["running"])
        self.assertEqual(s["tick_count"], 1)
        self.assertIsNotNone(s["last_sensor"])


if __name__ == "__main__":
    unittest.main()
