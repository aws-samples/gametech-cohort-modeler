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




def relationship(player, order):
    try:
        if order==1:
            edges = g.V(player).outE().inV().hasLabel('player').toSet()
            
        elif order==2:
            edges = g.V(player).outE().inV().outE().inV().hasLabel('player').toSet()
            
        elif order==3:
            edges = g.V(player).outE().inV().outE().inV().outE().inV().hasLabel('player').toSet()
        else: 
            edges = "relationshipOrder must be 1, 2, 3"
    
        return {
            'statusCode': 200,
            'body': str(edges)
        }
    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }

def handler(event, context):
    input = {
        **event['pathParameters'],
        **event['queryStringParameters']
        }
    input_validation = validation.validate(input)
    
    if input_validation[0] is True:
        return relationship(input_validation[1]['player'], input_validation[1]['relationshipOrder'])
    else:
        return {
            'statusCode': 400,
            'body': str(input_validation[0])
        }
    


