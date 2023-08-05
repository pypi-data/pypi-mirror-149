import unittest
import json

from .testbed import TestBed


def load_sample(fname):
    f = open(fname)
    file1 = json.loads(f.read())
    f.close()
    return file1


class TestClients(unittest.TestCase):
    def test_client_extra_methods(self):
        clients = self.testbed.getKeycloak().build('clients', self.REALM)
        self.assertIsNotNone(clients.roles, 'The client object should have a roles method.')

    def test_client_roles(self):
        client_payload = load_sample('./test/payloads/client.json')
        clients = self.testbed.getKeycloak().build('clients', self.REALM)
        svc_state = clients.create(client_payload).isOk()
        self.assertTrue(svc_state, 'The service should return a 200.')

        ret = clients.findFirstByKV('clientId', client_payload['clientId'])
        self.assertNotEqual(ret, [], 'It should return the posted client')

        client_query = {'key': 'clientId', 'value': client_payload['clientId']}
        client_roles_api = clients.roles(client_query)
        svc_roles_state = client_roles_api.create(
            {"name": "new-role", "description": "here should go a description."}).isOk()
        self.assertTrue(svc_roles_state, 'The client_roles service should return a 200.')

        ret_client_roles = client_roles_api.findFirstByKV('name', 'new-role')
        self.assertNotEqual(ret_client_roles, [], 'It should return the posted client')


    def test_client_roles_removal(self):
        client_payload = load_sample('./test/payloads/client.json')
        client_payload['clientId'] = 'test_client_roles_removal'
        client_role_name = "deleteme-role"

        clients = self.testbed.getKeycloak().build('clients', self.REALM)
        svc_state = clients.create(client_payload).isOk()

        client_query = {'key': 'clientId', 'value': client_payload['clientId']}
        client_roles_api = clients.roles(client_query)
        svc_roles_state = client_roles_api.create(
            {"name": client_role_name, "description": "A role that need to be deleted."}).isOk()

        ret_client_roles = client_roles_api.findFirstByKV('name', client_role_name)
        self.assertNotEqual(ret_client_roles, [], 'It should return the posted client')

        result = client_roles_api.removeFirstByKV('name', client_role_name)
        self.assertTrue(result, 'The server should return ok.')

        self.assertEqual(client_roles_api.findFirstByKV('name', client_role_name), [], 'It should return the posted client')

    @classmethod
    def setUpClass(self):
        self.testbed = TestBed()
        self.testbed.createRealms()
        self.testbed.createUsers()
        self.testbed.createClients()
        self.REALM = self.testbed.REALM

    @classmethod
    def tearDownClass(self):
        self.testbed.goodBye()
        return 1
