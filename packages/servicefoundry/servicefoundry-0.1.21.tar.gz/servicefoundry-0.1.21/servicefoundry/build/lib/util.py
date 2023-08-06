from typing import Optional, List, Union, Tuple

import questionary

from servicefoundry.build.clients.service_foundry_client import (
    ServiceFoundryServiceClient,
)
from servicefoundry.build.model.entity import Cluster, Workspace


# TODO: Move type casting downwards into `ServiceFoundrySession` and `ServiceFoundryServiceClient`


def resolve_clusters(
    client: ServiceFoundryServiceClient,
    name_or_id: Optional[str] = None,
    ignore_context: bool = False,
) -> List[Cluster]:
    if not ignore_context and not name_or_id:
        cluster = client.session.get_cluster()
        if cluster:
            cluster = Cluster.from_dict(cluster)
            return [cluster]
    clusters = [Cluster.from_dict(c) for c in client.list_cluster()]
    if name_or_id:
        found = [c for c in clusters if c.name == name_or_id]
        if not found:
            found = [c for c in clusters if c.id == name_or_id]
    else:
        found = clusters
    return found


def resolve_workspaces(
    client: ServiceFoundryServiceClient,
    name_or_id: Optional[str] = None,
    cluster_name_or_id: Optional[Union[Cluster, str]] = None,
    ignore_context: bool = False,
) -> List[Workspace]:
    if not ignore_context and not name_or_id:
        workspace = client.session.get_workspace()
        if workspace:
            workspace = Workspace.from_dict(workspace)
            return [workspace]

    if isinstance(cluster_name_or_id, Cluster):
        clusters = [cluster_name_or_id]
        cluster_name_or_id = clusters[0].id
    else:
        clusters = resolve_clusters(client=client, name_or_id=cluster_name_or_id)

    if not cluster_name_or_id and not clusters:
        workspaces = [Workspace.from_dict(w) for w in client.list_workspace()]
    else:
        if not clusters:
            if cluster_name_or_id:
                raise ValueError(
                    f"No cluster found with name or id {cluster_name_or_id!r}"
                )
            else:
                raise ValueError(f"No clusters found!")
        elif len(clusters) > 1:
            raise ValueError(
                f"More than one cluster found with name or id {cluster_name_or_id!r}: {clusters!r}"
            )
        else:
            cluster = clusters[0]
            workspaces = [
                Workspace.from_dict(w)
                for w in client.get_workspace_by_name(
                    workspace_name="", cluster_id=cluster.id
                )
            ]
    if name_or_id:
        found = [w for w in workspaces if w.name == name_or_id]
        if not found:
            found = [w for w in workspaces if w.id == name_or_id]
    else:
        found = workspaces
    return found


def ask_pick_cluster(clusters: List[Cluster]) -> Cluster:
    choices = [
        questionary.Choice(title=f"{c.name} ({c.fqn})", value=c) for c in clusters
    ]
    return questionary.select("Pick a cluster", choices=choices).ask()


def maybe_ask_pick_cluster(clusters: List[Cluster]) -> Cluster:
    if len(clusters) == 1:
        return clusters[0]
    return ask_pick_cluster(clusters=clusters)


def ask_pick_workspace(workspaces: List[Workspace]) -> Workspace:
    choices = [
        questionary.Choice(title=f"{w.name} ({w.fqn})", value=w) for w in workspaces
    ]
    return questionary.select("Pick a workspace", choices=choices).ask()


def maybe_ask_pick_workspace(workspaces: List[Workspace]) -> Workspace:
    if len(workspaces) == 1:
        return workspaces[0]
    return ask_pick_workspace(workspaces=workspaces)


def resolve_cluster_or_error(
    name_or_id: Optional[str] = None,
    ignore_context: bool = False,
    non_interactive: bool = True,
    client: Optional[ServiceFoundryServiceClient] = None,
) -> Cluster:
    if non_interactive:
        if not name_or_id:
            raise ValueError(
                "cluster name or id cannot be null in `--non-interactive` mode"
            )

    clusters = resolve_clusters(
        client=client, name_or_id=name_or_id, ignore_context=ignore_context
    )

    if not clusters:
        if name_or_id:
            raise ValueError(f"No cluster found with name or id {name_or_id!r}")
        else:
            raise ValueError(f"No clusters found!")
    else:
        if non_interactive:
            if len(clusters) > 1:
                raise ValueError(
                    f"More than one cluster found with name or id {name_or_id!r}: {clusters!r}"
                )
            else:
                cluster = clusters[0]
        else:
            cluster = maybe_ask_pick_cluster(clusters=clusters)
    return cluster


def resolve_workspace_or_error(
    name_or_id: Optional[str] = None,
    cluster_name_or_id: Optional[Union[Cluster, str]] = None,
    ignore_context: bool = False,
    non_interactive: bool = True,
    client: Optional[ServiceFoundryServiceClient] = None,
) -> Tuple[Workspace, Cluster]:
    if non_interactive:
        if not name_or_id:
            raise ValueError(
                "workspace name or id cannot be null in `--non-interactive` mode"
            )

    if isinstance(cluster_name_or_id, Cluster):
        cluster = cluster_name_or_id
    else:
        cluster = resolve_cluster_or_error(
            name_or_id=cluster_name_or_id,
            non_interactive=non_interactive,
            ignore_context=ignore_context,
            client=client,
        )

    workspaces = resolve_workspaces(
        client=client,
        name_or_id=name_or_id,
        cluster_name_or_id=cluster,
        ignore_context=ignore_context,
    )
    if not workspaces:
        if name_or_id:
            raise ValueError(
                f"No workspace found with name or id {name_or_id!r} in cluster {cluster.name!r}"
            )
        else:
            raise ValueError(f"No workspaces found!")
    else:
        if non_interactive:
            if len(workspaces) > 1:
                raise ValueError(
                    f"More than one workspace found with name or id {name_or_id!r}: {workspaces!r}"
                )
            else:
                workspace = workspaces[0]
        else:
            workspace = maybe_ask_pick_workspace(workspaces=workspaces)
    return workspace, cluster
