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
def collaborativeFilter(player):
    try:
        query = g.V(player).as_('user').out().aggregate('friends').out().where(P.neq('user')).where(P.without('friends')).groupCount().by(__.id()).toList()
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

    validationResult =  validation.validate(input, required = ['player'])

    if validationResult[0] is True:
        return collaborativeFilter(input['player'])
    else:
        return {
            'statusCode': 400,
            'body': str(validationResult[0])
        }



