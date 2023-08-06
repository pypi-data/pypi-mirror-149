import unittest

from arps.core.agent_id_manager import AgentIDManager, AgentID

class TestAgentIDManager(unittest.TestCase):

    def test_agent_identifier(self):
        agent_identifier_one = AgentID(0, 18)
        agent_identifier_two = AgentID(0, 18)
        agent_identifier_three = AgentID(0, 1)

        self.assertEqual(agent_identifier_one, agent_identifier_two)
        self.assertNotEqual(agent_identifier_one, agent_identifier_three)

        self.assertEqual(0, agent_identifier_one.root_id)
        self.assertEqual(18, agent_identifier_one.agent_identifier)
        self.assertEqual('0.18', str(agent_identifier_one))
        self.assertEqual('0.1', str(agent_identifier_three))

    def test_without_commit(self):
        agent_id_mananger = AgentIDManager(0)

        agent_identifier = agent_id_mananger.next_available_id()
        self.assertEqual(agent_identifier, AgentID(0, 1))
        self.assertEqual(set(), agent_id_mananger.identifiers)

        agent_identifier = agent_id_mananger.next_available_id()
        self.assertEqual(agent_identifier, AgentID(0, 1))
        self.assertEqual(set(), agent_id_mananger.identifiers)

    def test_with_commit(self):
        agent_id_mananger = AgentIDManager(0)

        agent_identifier = agent_id_mananger.next_available_id()
        self.assertEqual(agent_identifier, AgentID(0, 1))
        agent_id_mananger.commit()
        self.assertEqual({AgentID(0, 1)}, agent_id_mananger.identifiers)

        agent_identifier = agent_id_mananger.next_available_id()
        self.assertEqual(agent_identifier, AgentID(0, 2))
        agent_id_mananger.commit()
        self.assertEqual({AgentID(0, 1), AgentID(0, 2)}, agent_id_mananger.identifiers)

    def test_identifiers(self):
        agent_id_mananger = AgentIDManager(0)
        agent_id_mananger.next_available_id()
        agent_id_mananger.commit()
        agent_id_mananger.next_available_id()
        agent_id_mananger.commit()
        agent_id_mananger.next_available_id()
        agent_id_mananger.commit()
        self.assertEqual({AgentID(0, 1), AgentID(0, 2), AgentID(0, 3)},
                         agent_id_mananger.identifiers)

        agent_id_mananger.identifiers.remove(AgentID(0, 1))

        self.assertEqual({AgentID(0, 1), AgentID(0, 2), AgentID(0, 3)},
                         agent_id_mananger.identifiers)

    def test_commit_only_once(self):
        agent_id_mananger = AgentIDManager(0)
        agent_id_mananger.next_available_id()
        agent_id_mananger.commit()
        agent_id_mananger.commit()
        agent_id_mananger.commit()
        self.assertEqual({AgentID(0, 1)}, agent_id_mananger.identifiers)

        agent_id_mananger.next_available_id()
        agent_id_mananger.commit()

        self.assertEqual({AgentID(0, 1), AgentID(0, 2)}, agent_id_mananger.identifiers)

    def test_agent_id_from_str(self):
        self.assertEqual(AgentID(0,1), AgentID.from_str('0.1'))
        with self.assertRaises(ValueError):
            AgentID.from_str('invalid_id')

if __name__ == '__main__':
    unittest.main()
