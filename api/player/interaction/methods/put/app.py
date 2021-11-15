from __future__  import print_function  # Python 2/3 compatibility


from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import T
from gremlin_python.process.traversal import Cardinality

import json
import os
import validation 

neptuneEndpoint = os.environ['NeptuneEndpoint']
neptuneEndpoint = "wss://" + neptuneEndpoint + ":8182/gremlin"

graph = Graph()
remoteConn = DriverRemoteConnection(neptuneEndpoint,'g')
g = graph.traversal().withRemote(remoteConn)


def interactionEdge(input):
    try:
        query = g.V(input['action']).fold().coalesce(
            __.unfold(),
            __.addV('action').property(T.id,input['action'])
        ).as_('a').V(input['player']).coalesce(
            __.outE('action_edge').where(__.inV().has(T.id, input['action'])).property('count',__.union(__.values('count'), __.constant(1)).sum()),
            __.addE('action_edge').to('a').property('count',1)
        ).next()

        if 'targetPlayer' in input:
            try:
                query = g.V(input['targetPlayer']).as_('a').V(input['player']).coalesce(
                    __.outE('interaction_edge').where(__.inV().has(T.id, input['targetPlayer'])).property(input['action'],__.union(__.values(input['action']), __.constant(1)).sum()),
                    __.addE('interaction_edge').to('a').property(input['action'],1)
                ).next()
            except Exception as e:
                print(e)

        query = g.V(input['action']).valueMap().unfold().next()
        for key, value in query.items():
            print(key, type(value[0]))
            query = g.V(input['player']).property(Cardinality.single,key,__.union(__.values(key), __.constant(value[0])).sum()).next()

        return {
            'statusCode': 200
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': str(e)
        }

def campaignEdge(input):
    try:
        query = g.V(input['campaign']).as_('a').V(input['player']).coalesce(
                __.outE('campaign_edge').where(__.inV().has(T.id, input['campaign'])).property(input['campaignAction'],__.union(__.values(input['campaignAction']), __.constant(1)).sum()),
                __.addE('campaign_edge').to('a').property(input['campaignAction'],1)
            ).next()
        return {
            'statusCode': 200
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

    if 'action' in input and 'campaign' not in input:
        validationResult =  validation.validate(input, ['action'])

        if validationResult[0] is True:
            return interactionEdge(input)
        else:
            return {
                'statusCode': 400,
                'body': str(validationResult[0])
            }
    elif 'campaign' in input and 'action' not in input:
        validationResult =  validation.validate(input, ['campaign', 'campaignAction'])

        if validationResult[0] is True:
            return campaignEdge(input)
        else:
            return {
                'statusCode': 400,
                'body': str(validationResult[0])
            }
    else:
        return {
            'statusCode': 400,
            'body': 'must specify action or campaign and campaignAction'
        }




 
    