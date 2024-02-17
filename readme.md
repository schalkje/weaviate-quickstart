# Weaviate quick start
https://weaviate.io/developers/weaviate/quickstart



# Testing Weaviate running in a container

http://localhost:8080/v1
http://localhost:8080/v1/meta
http://localhost:8080/v1/schema

http://localhost:8080/v1/.well-known/live
http://localhost:8080/v1/.well-known/ready


{
    "links": [
        {
            "href": "/v1/meta",
            "name": "Meta information about this instance/cluster"
        },
        {
            "documentationHref": "https://weaviate.io/developers/weaviate/api/rest/schema",
            "href": "/v1/schema",
            "name": "view complete schema"
        },
        {
            "documentationHref": "https://weaviate.io/developers/weaviate/api/rest/schema",
            "href": "/v1/schema{/:className}",
            "name": "CRUD schema"
        },
        {
            "documentationHref": "https://weaviate.io/developers/weaviate/api/rest/objects",
            "href": "/v1/objects{/:id}",
            "name": "CRUD objects"
        },
        {
            "documentationHref": "https://weaviate.io/developers/weaviate/api/rest/classification,https://weaviate.io/developers/weaviate/api/rest/classification#knn-classification",
            "href": "/v1/classifications{/:id}",
            "name": "trigger and view status of classifications"
        },
        {
            "documentationHref": "https://weaviate.io/developers/weaviate/api/rest/well-known#liveness",
            "href": "/v1/.well-known/live",
            "name": "check if Weaviate is live (returns 200 on GET when live)"
        },
        {
            "documentationHref": "https://weaviate.io/developers/weaviate/api/rest/well-known#readiness",
            "href": "/v1/.well-known/ready",
            "name": "check if Weaviate is ready (returns 200 on GET when ready)"
        },
        {
            "documentationHref": "https://weaviate.io/developers/weaviate/api/rest/well-known#openid-configuration",
            "href": "/v1/.well-known/openid-configuration",
            "name": "view link to openid configuration (returns 404 on GET if no openid is configured)"
        }
    ]
}