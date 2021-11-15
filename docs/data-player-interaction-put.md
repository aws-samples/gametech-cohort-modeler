# Create Interaction

Gets interactions for a single `{player}`.

**URL** : `/data/player/{player}/interaction`

**Method** : `PUT`

**Auth required** : NO

## Query Parameters**

* `targetPlayer=[valid player]`
* `action=[interaction type, such as 'action_sharepii']`



## Success Response

**Code** : `200 OK`

## Error Response

**Condition** : If `{player}` or `target-player` does not exist.

**Code** : `400 BAD REQUEST`

**Content example** :

```json
500: {
    "detailedMessage": "Encountered a traverser that does not map to a value for child traversal: [GraphStep(vertex,[btromano])]",
    "code": "IllegalArgumentException",
    "requestId": "db0a7127-5d4a-4906-aa89-baf80d24c096"
}
```

```
can only concatenate str (not "GraphTraversal") to str
```








