class Entity:
    name = "entity"
    # url ?
    # defining multiple output types
    display_columns_ps = ["id", "name", "status", "createdAt"]


class Cluster(Entity):
    name = "cluster"
    display_columns_ps = ["id", "name", "fqn", "region", "createdAt"]


class Workspace(Entity):
    name = "workspace"
    display_columns_ps = ["id", "name", "status", "createdAt"]


class Service(Entity):
    name = "service"
    display_columns_ps = ["id", "name", "status", "createdAt"]


class Deployment(Entity):
    name = "deployment"


class SecretGroup(Entity):
    name = "secret-group"


class Secret(Entity):
    name = "secret"
