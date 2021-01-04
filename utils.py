"""
This script provides functionality to allow for visualization of the DAG with networkx.

Author:
    Caio Martins Ramos de Oliveira

Since:
    2021-01
"""

from typing import List, Tuple
from itertools import product

import networkx as nx
from kedro.pipeline.node import Node
from kedro.pipeline import Pipeline

def get_links(nodes: List[Node]) -> List[str]:
    """
    Returns a list of the possible links given a list of nodes.
    """
    all_possible_links = []
    for possible_link_list in [node[1]['inputs'] + node[1]['outputs'] for node in nodes]:
        all_possible_links += possible_link_list
    all_possible_links = list(set(all_possible_links))
    return all_possible_links

def get_edge_list_for_link(link: str, nodes: List[Node]) -> Tuple[Node, Node]:
    edges = []
    input_nodes = list(filter(lambda x: link in x[1]['inputs'], nodes))
    output_nodes = list(filter(lambda x: link in x[1]['outputs'], nodes))
    if (len(input_nodes) > 0) & (len(output_nodes) > 0):
        # I invert the order here to reflect the correct
        # order process
        return list(product(map(lambda x: x[0], output_nodes), 
                            map(lambda x: x[0], input_nodes)))
    return

def get_edges(nodes: List[Node]) -> Tuple[str, str]:
    edges = []
    for link in get_links(nodes):
        temp_edges = get_edge_list_for_link(link, nodes)
        if temp_edges:
            edges += temp_edges
    edges = list(set(edges))
    return edges

def get_graph_from_pipeline(pipeline_list: List[Node]) -> nx.Graph:
    """
    Returns a Graph for a given pipeline.
    """
    nodes = list(map(lambda x: (x._func.__name__,
                                {'outputs': x.outputs, 'inputs': x.inputs}),
                     pipeline_list))
    edges = get_edges(nodes)

    G = nx.DiGraph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G