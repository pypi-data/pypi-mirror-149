# innocuousbook_api

1. [How to use](#how-to-use)

## <span id="how-to-use"> How to use </span>

1. Install
```bash
pip install innocuousbook-api
```

2. Import
```python
from innocuousbook-api import InnoucousBookAPI
```

3. Use default
> default server host: https://dashboard.innocuous.ai  
```python
# export INNOCUOUSBOOK_TOKEN=USER_TOKEN
api = InnoucousBookAPI()
```
4. Use the specified token
```python
token = "USER_TOKEN"
api = InnoucousBookAPI(token)
```

5. Use the specified server host
```python
token = "USER_TOKEN"
host = "SERVER_HOST"
api = InnoucousBookAPI(token, host=host)
```
