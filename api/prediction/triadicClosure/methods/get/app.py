from __future__  import print_function  # Python 2/3 compatibility


from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import T
from gremlin_python.process.traversal import P
import json
import os
import validation


neptuneEndpoint = os.environ['NeptuneEndpoint']
neptuneEndpoint = "wss://" + neptuneEndpoint + ":8182/gremlin"

graph = Graph()
remoteConn = DriverRemoteConnection(neptuneEndpoint,'g')
g = graph.traversal().withRemote(remoteConn)

def triadicClosure(player, action):
    try:
        query = g.V(player).out('interaction_edge').as_('bad_actors').where(__.out('action_edge').hasId(action).in_('action_edge').hasId(player)).toList()
        return {
            'statusCode': 200,
            'body': str(query)
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }


def handler(event, context):
    if event['queryStringParameters'] is not None:
        input = {
            **event['queryStringParameters']
        }
    else:
        return {
            'statusCode': 400,
            'body': 'missing query parameters.'
        }

    validationResult =  validation.validate(input, ['player','action'])

    if validationResult[0] is True:
        return triadicClosure(input['player'],input['action'])
    else:
        return {
            'statusCode': 400,
            'body': str(validationResult[0])
        }
