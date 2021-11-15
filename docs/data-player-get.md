# Get Player

Returns a player node with ID equal to given path paramter `{player}`.

**URL** : `/data/player/{player}`

**Method** : `GET`

**Auth required** : NO

## Success Response

**Code** : `200 OK`

## Error Response

**Condition** : If user does not exist. Running this query in Gremlin Python results in an exception though no details are included in the exception.

**Code** : `400 BAD REQUEST`

**Content example** :

```json
Player does not exist
```
