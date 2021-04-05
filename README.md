# GameJolt API for Python

Single threaded Python interface for the GameJolt API running through HTTP requests.

## Reference

### `GameJoltAPI(gameId, privateKey, username=None, userToken=None, responseFormat="json", submitRequests=True)`

The main GameJolt API class. Aside from the required arguments, most of the optional arguments are provided to avoid asking for them in every single method.

### Attributes

- `gameId`: The game ID. Required in all requests.
- `privateKey`: The API private key. Required in all requests.
- `username`: Username used in some requests. Optional.
- `userToken`: User access token used in some requests. Optional.
- `responseFormat`: The response format of the requests. Can be `"json"`, `"xml"`, `"keypair"` or `"dump"`. Optional, defaults to `"json"`.
- `submitRequests`: If submit the requests or just get the generated URLs from the method calls. Useful to generate URLs for batch requests. Optional, defaults to `True`.

### Examples

#### Instancing the API class

```python
import gamejoltapi

GAME_ID = "602381"
PRIVATE_KEY = "de7ac4c81d064cdc1121b495e2165b53"
USERNAME = "bgempire"
TOKEN = "bgempire"

api = gamejoltapi.GameJoltAPI(
    GAME_ID, 
    PRIVATE_KEY, 
    username=USERNAME, 
    userToken=TOKEN,
    responseFormat="json",
    submitRequests=True
)
```

#### Requesting the server time

```python
result = api.time()
```

#### Storing data in the global data store

```python
result = api.dataStoreSet("some_global_value", "500", globalData=True)
```

#### Increasing value by 100 in the global data store

```python
result = api.dataStoreUpdate("some_global_value", "add", "100", globalData=True)
```

#### Batch request

```python
# Disable request submitting to get URLs from methods
api.submitRequests = False

# Generate list of request URLs
requests = [
    api.usersFetch(),
    api.sessionsCheck(),
    api.scoresTables(),
    api.trophiesFetch(),
    api.dataStoreGetKeys("*", globalData=True),
    api.friends(),
    api.time()
]

# Enable request submitting again
api.submitRequests = True

# Submit batch request and get all results
result = api.batch(requests=requests)
```
