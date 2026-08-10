import json
import unittest

from security_robot import (
    SecurityRobot,
    SensorFusionIntrusionDetector,
    SensorReading,
    VisionObservation,
    WebhookSecuritySystem,
)


class FakeSensors:
    def __init__(self, readings):
        self.readings = readings

    def read(self, area):
        return self.readings.get(area, SensorReading(area=area))


class FakeVision:
    def __init__(self, observations=None):
        self.observations = observations or {}

    def infer(self, area):
        return self.observations.get(area, ())


class FakeNavigator:
    def __init__(self, blocked=()):
        self.blocked = set(blocked)
        self.visited = []

    def move_to(self, area):
        self.visited.append(area)
        return area not in self.blocked


class Recorder:
    def __init__(self, fail=False):
        self.alerts = []
        self.fail = fail

    def notify(self, alert):
        self.alerts.append(alert)
        if self.fail:
            raise RuntimeError("offline")

    def report_event(self, alert):
        self.notify(alert)


def make_robot(*, sensors=None, vision=None, navigator=None, notifiers=(), security_system=None, clock=lambda: 100):
    return SecurityRobot(
        route=("ingresso", "deposito"),
        sensors=sensors or FakeSensors({}),
        vision=vision or FakeVision(),
        navigator=navigator or FakeNavigator(),
        notifiers=notifiers,
        security_system=security_system,
        alert_cooldown_seconds=60,
        clock=clock,
    )


class SecurityRobotTests(unittest.TestCase):
    def test_safe_patrol_visits_the_complete_route(self):
        navigator = FakeNavigator()
        robot = make_robot(navigator=navigator)

        results = robot.run_patrol(cycles=2)

        self.assertEqual(navigator.visited, ["ingresso", "deposito", "ingresso", "deposito"])
        self.assertTrue(all(item["status"] == "safe" for item in results))
        self.assertEqual(robot.status, "idle")

    def test_sensor_and_ai_observation_trigger_intrusion_alert(self):
        notifier = Recorder()
        system = Recorder()
        robot = make_robot(
            sensors=FakeSensors({"ingresso": SensorReading(area="ingresso", motion=True)}),
            vision=FakeVision({"ingresso": [VisionObservation("person", 0.93, "track-7")]}),
            notifiers=(notifier,),
            security_system=system,
        )

        result = robot.scan_area("ingresso")

        self.assertEqual(result["status"], "alert")
        self.assertEqual(result["detections"][0]["category"], "unauthorized_person")
        self.assertEqual(len(notifier.alerts), 1)
        self.assertEqual(len(system.alerts), 1)

    def test_authorized_access_does_not_trigger_person_alert(self):
        detector = SensorFusionIntrusionDetector(person_confidence_threshold=0.7)
        reading = SensorReading(area="ingresso", motion=True, access_authorized=True)

        detections = detector.detect(reading, [VisionObservation("person", 0.99)])

        self.assertEqual(detections, [])

    def test_forced_door_triggers_alert_without_ai_guess(self):
        robot = make_robot(sensors=FakeSensors({"deposito": SensorReading(area="deposito", door_forced=True)}))

        result = robot.scan_area("deposito")

        self.assertEqual(result["detections"][0]["category"], "perimeter_breach")
        self.assertEqual(result["detections"][0]["sources"], ("physical_sensor",))

    def test_cooldown_suppresses_duplicate_notifications(self):
        now = [100.0]
        notifier = Recorder()
        robot = make_robot(
            sensors=FakeSensors({"ingresso": SensorReading(area="ingresso", motion=True)}),
            vision=FakeVision({"ingresso": [VisionObservation("person", 0.9)]}),
            notifiers=(notifier,),
            clock=lambda: now[0],
        )

        first = robot.scan_area("ingresso")
        second = robot.scan_area("ingresso")
        now[0] = 161
        third = robot.scan_area("ingresso")

        self.assertEqual(len(first["alerts"]), 1)
        self.assertEqual(len(second["alerts"]), 0)
        self.assertEqual(len(third["alerts"]), 1)
        self.assertEqual(len(notifier.alerts), 2)

    def test_adapter_failure_is_audited_without_stopping_patrol(self):
        robot = make_robot(
            sensors=FakeSensors({"ingresso": SensorReading(area="ingresso", tamper=True)}),
            notifiers=(Recorder(fail=True),),
        )

        result = robot.scan_area("ingresso")

        self.assertEqual(result["status"], "alert")
        self.assertEqual(result["errors"], ["notifier:RuntimeError"])
        self.assertEqual(len(robot.alerts), 1)

    def test_navigation_failure_is_reported(self):
        robot = make_robot(navigator=FakeNavigator(blocked={"deposito"}))

        results = robot.run_patrol()

        self.assertEqual(results[1]["status"], "navigation_failed")

    def test_webhook_enforces_transport_and_serializes_alert(self):
        with self.assertRaises(ValueError):
            WebhookSecuritySystem("http://security.example/events")

        captured = {}

        class Response:
            status = 202

            def __enter__(self): return self
            def __exit__(self, *_): return None

        def opener(request, timeout):
            captured["payload"] = json.loads(request.data)
            captured["timeout"] = timeout
            return Response()

        system = WebhookSecuritySystem("https://security.example/events", token="secret", opener=opener)
        robot = make_robot(
            sensors=FakeSensors({"ingresso": SensorReading(area="ingresso", tamper=True)}),
            security_system=system,
        )

        robot.scan_area("ingresso")

        self.assertEqual(captured["payload"]["category"], "perimeter_breach")
        self.assertEqual(captured["timeout"], 5)

        system.notify(robot.alerts[0])
        self.assertEqual(captured["payload"]["area"], "ingresso")


if __name__ == "__main__":
    unittest.main()
