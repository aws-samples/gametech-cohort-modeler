from __future__  import print_function


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

def badActors(startingPlayer, relatedPlayer, relatedAction):
    
    try:
        query = g.V()                           \
            .hasLabel('player')                 \
            .has('ea_reputation',P.lt(0))       \
            .aggregate(startingPlayer)          \
            .out('interaction_edge')            \
            .where(                             \
                __.out('action_edge')           \
                .hasId(relatedAction)           \
                .in_('action_edge')             \
                .where(                         \
                    P.within(startingPlayer)    \
                )                               \
            ).as_(relatedPlayer)                \
            .path()                             \
            .by(__.id())                        \
            .toList()                           
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
    validation_result = validation.validate(input, required = ['player','targetPlayer','action'])

    if validation_result[0] is True:
        return badActors(input['player'],input['targetPlayer'],input['action'])
    else:
        return {
            'statusCode': 400,
            'body': str(validation_result[0])
        }
