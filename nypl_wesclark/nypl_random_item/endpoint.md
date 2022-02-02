# Description

Random is how you retrieve a random capture based on a provided resource type from the 500 most recently listed captures.

# Endpoint

GET random/?type_of_resource={type_of_resource_value}

type_of_resource parameters are strings and possible values are: still image, text, cartographic, moving image, notated music, sound recording, three dimensional object, sound recording-musical, sound recording-nonmusical

Only one parameter may be provided.

# Example

random/?type_of_resource=still+image will return a random capture from the 500 most recently added that is categorized as a still image.

# Response

A malformed request will return a 400 with an error message. A successful request will return a response in JSON form that follows the format:

{uuid: uuid, type_of_resource: type_of_resource, item_link: url}

An example of a possible concrete response is:

{"uuid": "510d47dc-caf8-a3d9-e040-e00a18064a99", "type_of_resource": "still image", "item_link": "http://digitalcollections.nypl.org/items/510d47dc-caf8-a3d9-e040-e00a18064a99"}

The uuid is useful for other endpoints of the NYPL Digital API, and the item link will take you directly to view the capture.