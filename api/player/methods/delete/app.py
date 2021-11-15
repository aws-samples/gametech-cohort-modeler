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


def playerDelete(player):
    
    try:
        query = g.V(player).drop().iterate()
        return {
            'statusCode': 200
        }
 
    except Exception as e:
        print("exception")
        print(e)
        return {
            'body': str(e),
            'statusCode': 400
        }

    return response

def handler(event, context):

    input = event["pathParameters"]

    validationResult =  validation.validate(input, ['player'])

    if validationResult[0] is True:
        return playerDelete(input["player"])
    else:
        return {
            'statusCode': 400,
            'body': validationResult[0]
        }
 