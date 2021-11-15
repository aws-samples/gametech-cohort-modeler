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

def campaignCreate(campaign):
    
    try:
        query = g.addV("campaign").property(T.id, campaign).iterate()
        return {
            'statusCode': 200
        }
        
 
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }

        
def handler(event, context):
    input = {**event["pathParameters"]}

    return campaignCreate(input["campaign"])
    


    

    
    
