#!/usr/bin/env python3
"""
Unit tests per il modulo Fusion Power Integration (issue #134).

Eseguibili con:
    python3 -m unittest robots.spacestation.fusion_power.test_fusion_power -v
"""

import unittest

from robots.spacestation.fusion_power.ai_core import (
    AICoreHook,
    AIDecision,
    ControlAction,
)
from robots.spacestation.fusion_power.dashboard import FusionDashboardClient
from robots.spacestation.fusion_power.fusion_power import FusionPowerPlant
from robots.spacestation.fusion_power.model import FusionModel, FusionReaction
from robots.spacestation.fusion_power.plasma import PlasmaSimulator
from robots.spacestation.fusion_power.propulsion import PropulsionModule


# ------------------ model.py ------------------

class TestFusionModel(unittest.TestCase):
    def test_d_he3_is_aneutronic(self):
        m = FusionModel(reaction=FusionReaction.D_HE3)
        self.assertTrue(m.reaction.is_aneutronic)

    def test_d_t_is_not_aneutronic(self):
        m = FusionModel(reaction=FusionReaction.D_T)
        self.assertFalse(m.reaction.is_aneutronic)

    def test_p_b11_is_aneutronic(self):
        m = FusionModel(reaction=FusionReaction.P_B11)
        self.assertTrue(m.reaction.is_aneutronic)

    def test_q_mev_positive(self):
        for r in FusionReaction:
            self.assertGreater(r.q_mev, 0.0)

    def test_classify_sub_ignition(self):
        m = FusionModel(reaction=FusionReaction.D_HE3)
        # 0.5 * T_ign = 30 keV, regime sub_ignition
        t_ign = m.ignition_temperature_kev()
        self.assertEqual(m.classify_regime(0.5 * t_ign), "sub_ignition")

    def test_classify_ignition(self):
        m = FusionModel(reaction=FusionReaction.D_HE3)
        t_ign = m.ignition_temperature_kev()
        self.assertEqual(m.classify_regime(t_ign), "ignition")

    def test_classify_over_ignition(self):
        m = FusionModel(reaction=FusionReaction.D_HE3)
        t_ign = m.ignition_temperature_kev()
        self.assertEqual(m.classify_regime(2.0 * t_ign), "over_ignition")

    def test_electrical_power_zero_sub_ignition(self):
        m = FusionModel(reaction=FusionReaction.D_HE3)
        t_ign = m.ignition_temperature_kev()
        # a 0.5 T_ign siamo sub-ignition => potenza zero
        self.assertEqual(m.electrical_power_mw(0.5 * t_ign, 1.0), 0.0)

    def test_electrical_power_grows_with_density(self):
        m = FusionModel(reaction=FusionReaction.D_HE3)
        t_ign = m.ignition_temperature_kev()
        p_low = m.electrical_power_mw(t_ign, 0.5)
        p_high = m.electrical_power_mw(t_ign, 1.2)
        self.assertGreater(p_high, p_low)

    def test_meets_demand(self):
        m = FusionModel(
            reaction=FusionReaction.D_HE3,
            station_power_demand_mw=5.0,
            plasma_volume_m3=200.0,
        )
        t_ign = m.ignition_temperature_kev()
        # 1.2 * T_ign con n=1.2 deve coprire la domanda
        self.assertTrue(m.meets_demand(1.2 * t_ign, 1.2))
        # 0.5 T_ign e` sub-ignition => P=0 => domanda non coperta
        self.assertFalse(m.meets_demand(0.5 * t_ign, 1.0))

    def test_summary_keys(self):
        m = FusionModel(reaction=FusionReaction.D_HE3)
        s = m.summary(1.1 * m.ignition_temperature_kev(), 1.0)
        for key in (
            "reaction", "aneutronic", "ignition_temperature_kev",
            "current_temperature_kev", "regime", "density_1e20_m3",
            "thermal_power_mw", "electrical_power_mw",
            "station_demand_mw", "demand_met",
        ):
            self.assertIn(key, s)


# ------------------ plasma.py ------------------

class TestPlasmaSimulator(unittest.TestCase):
    def test_initial_step_produces_state(self):
        sim = PlasmaSimulator()
        s = sim.step()
        self.assertIsNotNone(s)
        self.assertGreater(s.density_1e20_m3, 0.0)
        self.assertGreater(s.temperature_kev, 0.0)

    def test_state_persisted(self):
        sim = PlasmaSimulator()
        s1 = sim.step()
        s2 = sim.step()
        self.assertIs(sim.state, s2)
        self.assertGreaterEqual(s2.timestamp, s1.timestamp)
        self.assertEqual(len(sim.history), 2)

    def test_run_returns_states(self):
        sim = PlasmaSimulator()
        states = sim.run(cycles=4)
        self.assertEqual(len(states), 4)
        for s in states:
            self.assertIn(s.regime, {"sub_ignition", "ignition", "over_ignition"})

    def test_diagnostics_keys(self):
        sim = PlasmaSimulator()
        sim.step()
        d = sim.diagnostics()
        for key in (
            "ion_temperature_kev", "electron_temperature_kev",
            "target_ion_temperature_kev", "density_1e20_m3",
            "confinement_time_s", "q_factor", "kinetic_pressure_kpa",
            "regime", "ignition_temperature_kev", "ignition_ratio", "samples",
        ):
            self.assertIn(key, d)
        self.assertEqual(d["samples"], 1)

    def test_deterministic(self):
        s1 = PlasmaSimulator(seed=123)
        s2 = PlasmaSimulator(seed=123)
        s1.run(5)
        s2.run(5)
        for a, b in zip(s1.history, s2.history):
            self.assertAlmostEqual(a.temperature_kev, b.temperature_kev, places=6)
            self.assertAlmostEqual(a.density_1e20_m3, b.density_1e20_m3, places=6)

    def test_q_factor_nonnegative(self):
        sim = PlasmaSimulator()
        for s in sim.run(10):
            self.assertGreaterEqual(s.q_factor, 0.0)


# ------------------ propulsion.py ------------------

class TestPropulsionModule(unittest.TestCase):
    def test_isp_positive(self):
        m = FusionModel(reaction=FusionReaction.D_HE3)
        p = PropulsionModule(model=m)
        self.assertGreater(p.specific_impulse_s(), 0.0)

    def test_thrust_positive(self):
        m = FusionModel(reaction=FusionReaction.D_HE3)
        p = PropulsionModule(model=m)
        self.assertGreater(p.thrust_newton(), 0.0)

    def test_thrust_grows_with_mass_flow(self):
        m = FusionModel(reaction=FusionReaction.D_HE3)
        a = PropulsionModule(model=m, exhaust_mass_flow_kg_s=0.001)
        b = PropulsionModule(model=m, exhaust_mass_flow_kg_s=0.005)
        self.assertGreater(b.thrust_newton(), a.thrust_newton())

    def test_summary_contains_aneutronic_flag(self):
        m = FusionModel(reaction=FusionReaction.D_HE3)
        p = PropulsionModule(model=m)
        s = p.summary()
        self.assertIn("aneutronic", s)
        self.assertTrue(s["aneutronic"])


# ------------------ dashboard.py ------------------

class TestDashboard(unittest.TestCase):
    def test_build_payload(self):
        sim = PlasmaSimulator()
        sim.step()
        assert sim.state is not None
        m = FusionModel()
        prop = PropulsionModule(model=m)
        d = FusionDashboardClient()
        payload = d.build_payload(
            "I-ECO-01", sim.state, prop,
            electrical_power_mw=4.0, station_demand_mw=12.0,
            regime="ignition",
        )
        self.assertEqual(payload["station_id"], "I-ECO-01")
        self.assertEqual(payload["module"], "fusion_power")
        self.assertEqual(payload["regime"], "ignition")
        self.assertFalse(payload["demand_met"])
        self.assertIn("plasma", payload)
        self.assertIn("propulsion", payload)

    def test_publish_without_transport(self):
        sim = PlasmaSimulator()
        sim.step()
        assert sim.state is not None
        m = FusionModel()
        prop = PropulsionModule(model=m)
        d = FusionDashboardClient()
        d.publish("I-ECO-01", sim.state, prop, 1.0, 1.0, "ignition")
        self.assertEqual(d.sent_count, 0)
        self.assertEqual(d.failed_count, 0)
        self.assertIsNotNone(d.last_payload)

    def test_to_json(self):
        d = FusionDashboardClient()
        self.assertEqual(d.to_json(), "{}")
        d.last_payload = {"hello": "world"}
        self.assertIn("hello", d.to_json())


# ------------------ ai_core.py ------------------

class TestAICoreHook(unittest.TestCase):
    def test_default_fallback_sub_ignition(self):
        from robots.spacestation.fusion_power.plasma import PlasmaState
        p = PlasmaState(
            timestamp=0, temperature_kev=5.0, electron_temperature_kev=4.0,
            density_1e20_m3=0.9, confinement_time_s=2.0, q_factor=0.0,
            kinetic_pressure_kpa=10.0, regime="sub_ignition",
        )
        hook = AICoreHook()
        d = hook.decide(p)
        self.assertEqual(d.action, ControlAction.INCREASE_HEAT)

    def test_default_fallback_over_ignition(self):
        from robots.spacestation.fusion_power.plasma import PlasmaState
        p = PlasmaState(
            timestamp=0, temperature_kev=200.0, electron_temperature_kev=180.0,
            density_1e20_m3=1.0, confinement_time_s=2.0, q_factor=10.0,
            kinetic_pressure_kpa=100.0, regime="over_ignition",
        )
        hook = AICoreHook()
        d = hook.decide(p)
        self.assertEqual(d.action, ControlAction.DECREASE_HEAT)

    def test_default_fallback_nominal(self):
        from robots.spacestation.fusion_power.plasma import PlasmaState
        p = PlasmaState(
            timestamp=0, temperature_kev=70.0, electron_temperature_kev=65.0,
            density_1e20_m3=1.0, confinement_time_s=2.5, q_factor=5.0,
            kinetic_pressure_kpa=60.0, regime="ignition",
        )
        hook = AICoreHook()
        d = hook.decide(p)
        self.assertEqual(d.action, ControlAction.HOLD)

    def test_custom_ai_core(self):
        from robots.spacestation.fusion_power.plasma import PlasmaState

        class StubCore:
            def __init__(self):
                self.calls = 0

            def decide(self, plasma):
                self.calls += 1
                return AIDecision(ControlAction.HOLD, 0.99, "stub")

        core = StubCore()
        hook = AICoreHook(core=core)
        p = PlasmaState(0, 50, 45, 1.0, 2.0, 1.0, 50, "ignition")
        d = hook.decide(p)
        self.assertEqual(d.action, ControlAction.HOLD)
        self.assertEqual(core.calls, 1)

    def test_emergency_shutdown_stops_plant(self):
        from robots.spacestation.fusion_power.plasma import PlasmaState

        class StopCore:
            def decide(self, plasma):
                return AIDecision(ControlAction.EMERGENCY_SHUTDOWN, 1.0, "fire")

        p = FusionPowerPlant(ai_hook=AICoreHook(core=StopCore()))
        p.start()
        p.tick()
        self.assertFalse(p._running)

    def test_feedback_annotates_last_decision(self):
        from robots.spacestation.fusion_power.plasma import PlasmaState
        hook = AICoreHook()
        p = PlasmaState(0, 50, 45, 1.0, 2.0, 1.0, 50, "ignition")
        hook.decide(p)
        hook.feedback(True, "ok")
        self.assertIn("feedback=ok", hook.history[-1][1].reason)


# ------------------ fusion_power.py ------------------

class TestFusionPowerPlant(unittest.TestCase):
    def test_start_stop(self):
        p = FusionPowerPlant()
        p.start()
        self.assertTrue(p._running)
        p.stop()
        self.assertFalse(p._running)

    def test_tick_raises_when_not_started(self):
        p = FusionPowerPlant()
        with self.assertRaises(RuntimeError):
            p.tick()

    def test_run_returns_payloads(self):
        p = FusionPowerPlant()
        p.start()
        out = p.run(cycles=3)
        self.assertEqual(len(out), 3)
        for o in out:
            self.assertEqual(o["module"], "fusion_power")
            self.assertEqual(o["station_id"], "I-ECO-01")

    def test_status(self):
        p = FusionPowerPlant()
        p.start()
        p.run(cycles=2)
        s = p.status()
        self.assertEqual(s["station_id"], "I-ECO-01")
        self.assertTrue(s["running"])
        self.assertEqual(s["tick_count"], 2)
        self.assertIn(s["reaction"], {"D-He3", "D-T", "D-D", "p-B11"})
        self.assertIn("plasma", s)
        self.assertIn("last_decision", s)
        self.assertIn("propulsion", s)

    def test_demand_met_in_overdrive(self):
        m = FusionModel(
            reaction=FusionReaction.D_HE3,
            station_power_demand_mw=2.0,
            plasma_volume_m3=200.0,
        )
        p = FusionPowerPlant(model=m)
        p.start()
        # forza il regime di over-ignition modificando il target del simulatore
        p.simulator._target_T = 2.0 * m.ignition_temperature_kev()
        p.run(cycles=10)
        # almeno un payload dovrebbe segnalare domanda soddisfatta
        self.assertTrue(any(payload["demand_met"] for payload in p.payloads))


if __name__ == "__main__":
    unittest.main()
