# Delete Campaign

Deletes campaign vertex with ID equal to given path paramter `{campaign}`.

**URL** : `/data/campaign/{campaign}`

**Method** : `DELETE`

**Auth required** : NO

## Success Response

**Code** : `200 OK`

## Error Response

**Condition** : If campaign does not exist. Running this query in Gremlin Python results in an exception though no details are included in the exception.

**Code** : `400 BAD REQUEST`

**Content example** :

```json
Campaign does not exist
```