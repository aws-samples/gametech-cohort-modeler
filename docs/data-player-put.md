# Create Player

Creates a player node with ID equal to given path paramter `{player}`.

**URL** : `/data/player/{player}`

**Method** : `PUT`

**Auth required** : NO

## Success Response

**Code** : `200 OK`

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
