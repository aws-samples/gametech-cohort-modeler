from cerberus import Validator
import os

from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.process.strategies import *
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import T
from gremlin_python.driver.protocol import GremlinServerError
from gremlin_python.process.traversal import Cardinality

neptuneEndpoint = os.environ['NeptuneEndpoint']
neptuneEndpoint = 'wss://' + neptuneEndpoint + ':8182/gremlin'

graph = Graph()
remoteConn = DriverRemoteConnection(neptuneEndpoint,'g')
g = graph.traversal().withRemote(remoteConn)

def playerCheck(field, value, error):
    try:
        player = g.V(value).next()
    except Exception as e:
        error(field, 'player does not exist')
        
def campaignCheck(field, value, error):
    try:
        player = g.V(value).next()
    except Exception as e:
        error(field, 'campaign does not exist')
        


required = {'required', True}
def validate(input = None, required = None, dependencies = None):
    v = Validator()
    v.allow_unknown = True  
    to_bool = lambda v: v.lower() in ('true', '1')
    schema = {
        'player': {
            'type': 'string',
            'check_with': playerCheck
        },
        'targetPlayer': {
            'type': 'string',
            'check_with': playerCheck,
        },
        'action': {
            'type': 'string',
            'allowed': ['action_chat', 'action_sharepii', 'action_partyjoin', 'action_randomheal', 'action_grief', 'action_badname', 'action_harass', 'action_stalk', 'action_badlanguage', 'action_endorse', 'action_report', 'action_badimage']
        },
        'playerAttribute': {
            'type': 'string',
            'allowed': ['ea_reputation', 'ea_altruism','ea_duty','ea_mischief','ea_malice','ea_atrisk']
        },
        'playerStat': {
            'type': 'string',
            'allowed': ['stat_uuid','status','stat_joinedDate','stat_lastPlayed','stat_totalSkinPurchases']
        },
        'incrementBy': {
            'type': 'integer',
            'coerce': int
        },
        'bidirectional': {
            'type': 'boolean',
            'coerce': (str, to_bool),
            'default': False
        },
        'relationshipOrder': {
            'type': 'integer',
            'default': 1
        },
        'campaign': {
            'type': 'string',
            'check_with': campaignCheck
        },
        'campaignAction': {
            'type': 'string',
            'allowed': ['campaign_login', 'campaign_emailOpened', 'campaign_linkClicked']
        },
        'campaignAttribute': {
            'type': 'string',
            'allowed': ['stat_totalEmailOpened','stat_messagesSent','stat_messagesDelivered','stat_dailyActive','stat_newPlayers']
        }
    }

    if required:
        for item in required:
            schema[item]['required']= True
    if dependencies:
        for item in dependencies:
            schema[item]['dependencies'] = dependencies[item]
    if v.validate(input, schema) is True:
        print ([True, v.document, v.normalized])
        return [True, v.document, v.normalized]
    else:
        print(v.errors)
        return [v.errors]