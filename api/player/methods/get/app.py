from __future__  import print_function  # Python 2/3 compatibility


from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import T
from gremlin_python.driver.protocol import GremlinServerError
import json
import os
import validation


neptuneEndpoint = os.environ['NeptuneEndpoint']
neptuneEndpoint = "wss://" + neptuneEndpoint + ":8182/gremlin"

graph = Graph()
remoteConn = DriverRemoteConnection(neptuneEndpoint,'g')
g = graph.traversal().withRemote(remoteConn)

def player(player):
    response = {}
    try:
        query = g.V(player).elementMap().toList()
        return {
            'statusCode': 200,
            'body': str(query)
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }
        

    return response


def handler(event, context):

    input = event["pathParameters"]

    validationResult =  validation.validate(input, ['player'])

    if validationResult[0] is True:
        return player(input["player"])
    else:
        return {
            'statusCode': 400,
            'body': str(validationResult[0])
        }
 













    resource = event["resource"]
    method = event["httpMethod"]
    pathParameters = event["pathParameters"]
    queryParameters = {}
    try:
        queryParameters = event["queryStringParameters"]
    except KeyError:
        print (KeyError)
    
    response = None

    query = player(pathParameters["player"])
    response = {
        'statusCode': query['statusCode'],
        'body': str(query['body'])
    }

    return response