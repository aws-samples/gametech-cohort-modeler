"""

TASK: implement target player interactions with query parameter

"""

from __future__  import print_function  # Python 2/3 compatibility


from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import T
import json
import os
import validation


neptuneEndpoint = os.environ['NeptuneEndpoint']
neptuneEndpoint = "wss://" + neptuneEndpoint + ":8182/gremlin"

graph = Graph()
remoteConn = DriverRemoteConnection(neptuneEndpoint,'g')
g = graph.traversal().withRemote(remoteConn)

def interactions(input):
    query = g.V(input['player'])
    if input['bidirectional']:
        query = query.bothE()
    else:
        query = query.outE()
    if 'targetPlayer' in input:
        query = query.where(__.otherV().hasId(input['targetPlayer'])).elementMap()
    else:
        query = query.where(__.and_(__.inV().hasLabel("player"), __.outV().hasLabel("player"))).elementMap()

    try:
        return {
            'statusCode': 200,
            'body': str(query.toList())
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }

def handler(event, context):
    if event['queryStringParameters'] is not None:
        input = {
            **event['pathParameters'],
            **event['queryStringParameters']
        }
    else: 
        input = event['pathParameters']

    validationResult =  validation.validate(input)
 
    if validationResult[0] is True:
        return interactions(validationResult[1])
    else:
        return {
            'statusCode': 400,
            'body': str(validationResult[0])
        }