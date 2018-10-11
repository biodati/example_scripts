#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""
Usage:  program.py <customer>

"""

import click
import json

api_url = 'https://api.bel.bio'


def template(name, creator):

    jgf_tmpl = {
        "graph": {
            "directed": False,
            "type": "BEL",
            "label": name,
            "metadata": {
                "gd:version": "1.0",
                "gd:creator": creator,
                "gd:description": "Create network from node list to use as a source of nodes for network edge searches",
            },
            "nodes": [],
            "edges": []
        }
    }

    return jgf_tmpl


@click.command()
@click.option('--name', '-n', default="TmpNetwork", help="Network name")
@click.option('--creator', '-c', default="nobody")
@click.option('--namespace', default="SP")
@click.option('--function', default="p")
@click.option('--api', default=api_url)
@click.argument('input_fn', type=click.Path(exists=True))
@click.argument('output_fn', type=click.Path())
def main(input_fn, output_fn, api, name, creator, namespace, function):

    nodes = []
    with open(input_fn, 'r') as f:
        for line in f:
            nodes.append(f'{function}({namespace}:{line.strip()})')

    graph_nodes = []
    for node in nodes:
        graph_nodes.append({'id': node, 'label': node, 'metadata': {}})

    graph_edges = []
    length = len(nodes)

    for i in range(length):
        if i == 0:
            continue
        else:
            graph_edges.append({
                'source': nodes[i],
                'target': nodes[i - 1],
                'relation': 'association',
                'metadata': {},
            })

    network = template(name, creator)
    network['graph']['nodes'] = graph_nodes
    network['graph']['edges'] = graph_edges

    with open(output_fn, 'w') as f:
        json.dump(network, f, indent=4)


if __name__ == '__main__':
    main()

