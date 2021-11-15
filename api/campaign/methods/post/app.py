from __future__  import print_function  # Python 2/3 compatibility


from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import T
from gremlin_python.driver.protocol import GremlinServerError
from gremlin_python.process.traversal import Cardinality
import json
import os
import validation 



neptuneEndpoint = os.environ['NeptuneEndpoint']
neptuneEndpoint = 'wss://' + neptuneEndpoint + ':8182/gremlin'

graph = Graph()
remoteConn = DriverRemoteConnection(neptuneEndpoint,'g')
g = graph.traversal().withRemote(remoteConn)


def campaignUpdate(input):
    
    try:
        query = g.V(input['campaign']).property(Cardinality.single,input['campaignAttribute'],__.union(__.values(input['campaignAttribute']), __.constant(input['incrementBy'])).sum()).next()
        return {
            'statusCode': 200,
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

    validationResult =  validation.validate(input, ['campaignAttribute','incrementBy'])
    if validationResult[0] is True:
        return campaignUpdate(validationResult[1])
    else:
        return {
            'statusCode': 400,
            'body': str(validationResult[0])
        }
    