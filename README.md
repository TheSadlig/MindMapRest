[![Build&Deploy](https://github.com/TheSadlig/MindMapRest/actions/workflows/main.yml/badge.svg)](https://github.com/TheSadlig/MindMapRest/actions/workflows/main.yml)
# MindMapRest

MindMapRest is a small API to generate mind-maps.


## Installation

### Prerequisites
* Python 3.9
* Bash (you can adapt the run.sh script if you don't have it)

### Configuration
By default, the project uses a sqlite database. The location of that file can be configured in `run.sh`:
```
export DATABASE_URI="sqlite:////tmp/mindmap.sqlite"
```

### Local Deployment
The following command will install dependencies, run unit test and deploy the server locally

```
./run.sh
```

### Run unit tests
To run the unit tests, simply run the following command (from the root of the project):
```
nose2 --with-coverage
```

## Usage
I have taken a few liberties from the original subject. The main one is that nodes don't have text: the node text constitute the path for future nodes. This was done to be closer to an actual MindMap, but also ease the printing of the MindMap.
### Check if the server is running
#### Request
`GET /isalive`
```
curl -X GET http://localhost:5000/isalive -H 'content-type: application/json'
```
#### Response
```
HTTP/1.1 418 I'M A TEAPOT
Server: Werkzeug/2.1.1 Python/3.8.10
Date: Wed, 27 Apr 2022 01:37:33 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 19

The teapot is alive
```
Note: [HTTP code 418 IS useful](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418)

### Create a new minmdap
#### Request
`POST /map/`
```
curl -X POST http://localhost:5000/map -H 'content-type: application/json' -d '{"id": "toto"}'
```
#### Response
```
HTTP/1.1 201 CREATED
Server: Werkzeug/2.1.1 Python/3.8.10
Date: Wed, 27 Apr 2022 01:34:31 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 14

{"id": "toto"}
```

### Add a node to a MindMap
#### Request
`POST /map/{map}/node`
```
curl -X POST http://localhost:5000/map/toto/node -H 'content-type: application/json' -d '{ "path": "/", "text": "i"}'
```
#### Response
Returns the node that was created
```
HTTP/1.1 201 CREATED
Server: Werkzeug/2.1.1 Python/3.8.10
Date: Wed, 27 Apr 2022 01:41:04 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 25

{"path": "i", "text": []}
```

### Read a node from the map
#### Request
`GET /map/{map}/node/{path}`
```
curl -X GET http://localhost:5000/map/toto/node/i/like -H 'content-type: application/json'
```

#### Response
Returns the node at the requested path and its children (in the `text` element)
```
HTTP/1.1 200 OK
Server: Werkzeug/2.1.1 Python/3.8.10
Date: Wed, 27 Apr 2022 01:46:52 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 48

{"path": "i/like", "text": ["sushi", "chicken"]}
```
In this case, the node `/i/like` possess the children `sushi` and `chicken`

### Pretty print a map
#### Request
`GET /map/{map}/print`
```
curl -X GET http://localhost:5000/map/toto/print -H 'content-type: application/json'
```
#### Response
```
HTTP/1.1 200 OK
Server: Werkzeug/2.1.1 Python/3.8.10
Date: Wed, 27 Apr 2022 01:52:02 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 124

root/
    i/
        like/
            sushi/
                very
            chicken/
                nuggets
    B
    i
```
## Calling the version deployed in AWS
Replace the API key:
```
curl -X GET -H "x-api-key: APIKEY"  https://evrt4izpqh.execute-api.ca-central-1.amazonaws.com/default/isalive
```

## Bonuses
:heavy_check_mark: Unit tests coverage to 75%.

:heavy_check_mark: If not already done, a nice storage backend (SQL Database, ...).

:arrow_right: SQLite is almost cheating but it is still a SQL database engine. The gap to setup a full database is not that big.

:x: Docker image.

:arrow_right: I decided to use AWS Lambda instead. You can find some (very old) docker example in other projects in this github: [NLPF](https://github.com/TheSadlig/NLPF)

:heavy_check_mark: Pipeline to build the docker image, execute the unit tests (example, github + travis CI).

:arrow_right: Using Github actions to execute unit tests and deploy to AWS Lambda.

:heavy_check_mark: Deployment in a Cloud service (Heroku, GCP AppEngine...)

:arrow_right: The API is deployed as an AWS Lambda. There is not automated setup into AWS, but the Github workflows is able to deploy any new version merged into the `main` branch

## Contributing
Please don't. This is a coding exercise, and it wouldn't make sense to have outside contributors.