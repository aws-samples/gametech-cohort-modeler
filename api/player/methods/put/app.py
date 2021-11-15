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

def playerCreate(player):
    response = {}
    try:
        return {
            'statusCode': 200,
            'body': str(g.addV("player").property(T.id, player).iterate())
        }
        
 
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }

        
def handler(event, context):
    input = {**event["pathParameters"]}

    return playerCreate(input["player"])
    


    

    
    
