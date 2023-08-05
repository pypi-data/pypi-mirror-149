def create_flow(flow):
    alias = flow['displayName']
    pid = None if not 'provider' in flow else flow['providerId']
    provider = 'registration-page-flow' if not pid else pid
    flow_type = 'basic-flow' if not pid else 'form-flow'

    # WARN: The value description is not well validated in Keycloak, it can return 500.
    return {
        "alias": alias,
        "type": flow_type,
        "description": "empty",
        "provider": provider,
    }


def get_executions(execution):
    provider = execution['providerId']
    return {'provider': provider}


def is_auth_flow(body):
    return 'authenticationFlow' in body


def get_node_level(node):
    return node['level']


def consistent(parent, flow):
    published_flows = parent.all()

    for publishedFlow in published_flows:
        resource_id = False

        if 'providerId' in publishedFlow and 'providerId' in flow:
            resource_id = publishedFlow['providerId'] == flow['providerId']
        else:
            resource_id = publishedFlow['displayName'] == flow['displayName']

        level_is_equal = publishedFlow['level'] == flow['level']
        index_is_equal = publishedFlow['index'] == flow['index']

        if resource_id and level_is_equal and index_is_equal:
            publishedFlow['requirement'] = flow['requirement']
            parent.update(obj_id=None, payload=publishedFlow).isOk()
            return True

    return False


class AuthenticationFlowsImporter():
    def __init__(self, authentication_api):
        self.flowAPI = authentication_api

    def update(self, root_node, flows):
        if self.flowAPI.is_built_in(root_node):
            for flow in flows:
                if is_auth_flow(flow):
                    self.flowAPI.flows(root_node).update(None, flow).isOk()
                else:
                    self.flowAPI.executions(root_node).update(None, flow).isOk()
        else:
            self.remove(root_node)
            self.flowAPI.create(root_node).isOk()
            self.publish(root_node, flows)

    def remove(self, root_node):
        unique_identifier = root_node['alias'] if 'alias' in root_node else root_node['displayName']
        key = 'alias' if 'alias' in root_node else 'displayName'

        self.flowAPI.removeFirstByKV(key, unique_identifier)

    def publish(self, root_node, flows):
        if not isinstance(flows, list):
            raise Exception("Bad Parameters for Authentication Flow: auth_flow parameter should be an array.")

        root_node = root_node
        nodes = {0: root_node}

        root_flow = self.flowAPI.executions(root_node)

        for flow in flows:
            current_level = get_node_level(flow)
            parent = nodes[current_level]

            if is_auth_flow(flow):
                authentication_flow = create_flow(flow)
                nodes[current_level + 1] = authentication_flow
                self.flowAPI.flows(parent).create(authentication_flow).isOk()
            else:
                execution = get_executions(flow)
                self.flowAPI.executions(parent).create(execution).isOk()

            if not consistent(root_flow, flow):
                raise Exception(
                    'There is an inconsistency problem: Changes are not taking place in the server, latency problems ?.')
