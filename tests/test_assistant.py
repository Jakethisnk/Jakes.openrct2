import unittest

from assistant.engine import Assistant
from assistant.logic.recommendation import Priority
from assistant.state import ParkState
from assistant.state.loader import MockSource


class AssistantTests(unittest.TestCase):
    def test_struggling_park_has_high_priority_advice(self):
        recs = Assistant().analyze(MockSource("struggling_park").load())
        self.assertTrue(recs)
        self.assertEqual(recs[0].priority, Priority.HIGH)
        self.assertEqual({r.category for r in recs},
                         {"finance", "guests", "rides", "staff", "scenery"})

    def test_healthy_park_has_no_advice(self):
        self.assertEqual(Assistant().analyze(MockSource("healthy_park").load()), [])

    def test_empty_park_does_not_crash(self):
        Assistant().analyze(ParkState())

    def test_from_dict_defaults(self):
        self.assertEqual(ParkState.from_dict({}).name, "Unnamed Park")


if __name__ == "__main__":
    unittest.main()
