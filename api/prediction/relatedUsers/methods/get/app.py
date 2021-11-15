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

# Find users that a given user has not directly interacted with, but that they might want to interact with based on common interactions.
def relatedUsers(player, playerAttribute):
    try:
        query = g.V().hasLabel('player').has(playerAttribute,P.lt(0)).as_(player).outE('interaction_edge').inV().outE('action_edge').inV().hasId('action_report','action_badimage','action_badlanguage','action_badname','action_sharepii').inE('action_edge').outV().where(__.is_(P.eq(player))).path().by(__.id()).by(T.label).toList()
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

    validationResult =  validation.validate(input, required = ['player', 'playerAttribute'])

    if validationResult[0] is True:
        return relatedUsers(input['player'], input['playerAttribute'])
    else:
        return {
            'statusCode': 400,
            'body': str(validationResult[0])
        }



