# Get Interaction

Gets interactions for a single `{player}`.

**URL** : `/data/player/{player}/interaction`

**Method** : `GET`

**Auth required** : NO

## Query Parameters

**`targetPlayer=[valid player]`**

Required: No

**`bidirectional=[True/False]`**

Returns edges from player to target-player and/or target-player to player.

Required: No, may only be present if `target-player` specified.



## Success Response

**Code** : `200 OK`

**Content example** :

```json
[
    {<T.id: 1>: '80bc8cbd-d2b1-d830-df07-96bd56686462', <T.label: 4>: 'Interactions', <Direction.IN: 2>: {<T.id: 1>: 'ashwinmr', <T.label: 4>: 'player'
        }, <Direction.OUT: 3>: {<T.id: 1>: 'kalescky', <T.label: 4>: 'player'
        }, 'report': 2, 'sharepii': 1
    },
    {<T.id: 1>: '16bc8ccb-344d-ca8b-620d-c3bcdaf1ac94', <T.label: 4>: 'Interactions', <Direction.IN: 2>: {<T.id: 1>: 'finch', <T.label: 4>: 'player'
        }, <Direction.OUT: 3>: {<T.id: 1>: 'kalescky', <T.label: 4>: 'player'
        }, 'report': 1
    },
    {<T.id: 1>: 'a8bc8cc6-a4d7-2cb1-5a51-e2af7545d249', <T.label: 4>: 'Interactions', <Direction.IN: 2>: {<T.id: 1>: 'kalescky', <T.label: 4>: 'player'
        }, <Direction.OUT: 3>: {<T.id: 1>: 'ashwinmr', <T.label: 4>: 'player'
        }, 'report': 1
    },
    {<T.id: 1>: '02bc8ccb-40e1-e31e-ccae-442e59b108ef', <T.label: 4>: 'Interactions', <Direction.IN: 2>: {<T.id: 1>: 'kalescky', <T.label: 4>: 'player'
        }, <Direction.OUT: 3>: {<T.id: 1>: 'finch', <T.label: 4>: 'player'
        }, 'report': 1
    }
]
```

## Error Response

**Condition** : If user already exists

**Code** : `400 BAD REQUEST`

**Content example** :

```json
499: {
    "detailedMessage": "Vertex with id already exists: ",
    "code": "ConstraintViolationException",
    "requestId": "96f02122-0623-4afc-8650-3d756819f104"
}
```


```json
optoinal field bidirectional must be "True" or "False"
```