"""
Network utilities for agent graph construction and failure simulation.
"""

from __future__ import annotations

import math
from typing import Iterable

import networkx as nx
import numpy as np
import pandas as pd


def build_agent_graph_from_environment(
    env_df: pd.DataFrame,
    *,
    comm_radius: float = 1.5,
    directed: bool = True,
) -> nx.Graph:
    """
    Build an agent communication graph from environment coordinates.
    """
    graph: nx.Graph = nx.DiGraph() if directed else nx.Graph()
    coords = env_df[["x", "y"]].to_numpy(dtype=float)
    n = len(coords)

    for node in range(n):
        graph.add_node(int(node), x=float(coords[node, 0]), y=float(coords[node, 1]))

    # Use a naive pairwise radius graph to stay dependency-light.
    radius = float(comm_radius)
    for i in range(n):
        xi, yi = coords[i]
        for j in range(i + 1, n):
            xj, yj = coords[j]
            dist = math.hypot(xi - xj, yi - yj)
            if dist <= radius:
                weight = 1.0 / (1.0 + dist)
                graph.add_edge(int(i), int(j), weight=weight)
                if directed:
                    graph.add_edge(int(j), int(i), weight=weight)
    return graph


def largest_component_fraction(graph: nx.Graph) -> float:
    """Return largest connected component size normalized to node count."""
    if graph.number_of_nodes() == 0:
        return 0.0
    base = graph.to_undirected() if graph.is_directed() else graph
    components = list(nx.connected_components(base))
    if not components:
        return 0.0
    largest = max(len(component) for component in components)
    return float(largest / max(1, graph.number_of_nodes()))


def apply_failure_step(
    graph: nx.Graph,
    *,
    removal_fraction: float,
    strategy: str = "targeted",
    seed: int = 42,
) -> tuple[nx.Graph, list[int]]:
    """
    Remove a fraction of nodes using random or targeted strategy.
    """
    if graph.number_of_nodes() == 0:
        return graph.copy(), []

    frac = float(np.clip(removal_fraction, 0.0, 1.0))
    remove_count = int(np.floor(frac * graph.number_of_nodes()))
    if remove_count <= 0:
        return graph.copy(), []

    nodes = list(graph.nodes())
    if strategy == "targeted":
        centrality = nx.betweenness_centrality(graph.to_undirected())
        ranked = sorted(nodes, key=lambda node: centrality.get(node, 0.0), reverse=True)
        removed = ranked[:remove_count]
    else:
        rng = np.random.default_rng(seed)
        removed = list(rng.choice(nodes, size=remove_count, replace=False))

    out = graph.copy()
    out.remove_nodes_from(removed)
    return out, [int(node) for node in removed]


def induced_subgraph(graph: nx.Graph, nodes: Iterable[int]) -> nx.Graph:
    """Return induced subgraph while preserving graph type."""
    return graph.subgraph(list(nodes)).copy()

