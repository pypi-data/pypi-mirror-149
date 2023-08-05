# Hyperscience SaaS Client Library
With the Hyperscience SaaS client library, you can authenticate to SaaS instances of Hyperscience and make API requests. 

## Quickstart Guide
### 1. Install Hyperscience SaaS Client Library
Install the Hyperscience SAAS Client Library from PyPI:
```shell
pip install hyperscience-saas-client
```

To upgrade the package:
```shell
pip install hyperscience-saas-client --upgrade
```

### 2. Set Up API Credentials
Retrieve your API credentials from your Hyperscience SaaS instance. To learn more, see API Access for SaaS Instances.

### 3. Configure Authentication Parameters
To configure authentication, the ApiController uses a Configuration class. A configuration object contains:
- Authentication domain ("auth_server”)
- Hyperscience's domain to make the requests to ("hs_domain")
- Timeout for requests in seconds (optional) ("request_timeout")

By default, these values are used:
```json
{
    "auth_server": "login.hyperscience.net",
    "hs_domain": "cloud.hyperscience.net",
    "request_timeout": 120 
}
```

You can set your Configuration object in one of the following three ways:
#### Passing a JSON object
```python
from hyperscience import Configuration

config = '{ "auth_server": "login.hyperscience.net", "hs_domain": "cloud.hyperscience.net" }'
configuration = Configuration.from_json_string(config)
```

Full path to a JSON file containing the configuration
```python
from hyperscience import Configuration

configuration = Configuration.from_file('/absolute/path/to/config.json')
```

Specifying the parameters
````python
from hyperscience import Configuration

configuration = Configuration(hs_domain='cloud.hyperscience.net')
````
##### or
```python
configuration = Configuration(hs_domain='cloud.hyperscience.net', auth_server='login.hyperscience.net')
```
##### or 
```python
configuration = Configuration(
    hs_domain='cloud.hyperscience.net', auth_server='login.hyperscience.net', request_timeout=60
)
```

### 4. Provide Credentials
There are two options for providing credentials:

#### a. Environment Variables (Recommended) 
To use environment variables to store your credentials:
1. Put your client_id in an environment variable called HS_CLIENT_ID
2. Put the client_secret in an environment variable called HS_CLIENT_SECRET

To load them and pass them to ApiController, you can do it with:
```python
from hyperscience import EnvironmentCredentialsProvider, Configuration, ApiController

credentials = EnvironmentCredentialsProvider()
configuration = Configuration('<hyperscience.domain>')
api_controller = ApiController(configuration, credentials)
```

#### b. Pass them via a CredentialsProvider object
If you prefer having credentials loaded from a different place instead of environment variables, you can create an instance of the CredentialsProvider class and pass it to ApiController:
```python
from hyperscience import CredentialsProvider, Configuration, ApiController
credentials = CredentialsProvider('client_id', 'client_secret')
configuration = Configuration('<hyperscience.domain>')
api_controller = ApiController(configuration, credentials)
```

> **WARNING**: Keeping credentials in code is a bad practice. CredentialsProvider is best used when loading credentials from secret stores.

### 5. Make a Test Call
Finally, ensure that your setup is correct by making a test call to GET submissions from your instance.
```python
from hyperscience import ApiController, CredentialsProvider, Configuration

credentials = CredentialsProvider('<client_id>', '<client_secret>')
configuration = Configuration('<hyperscience.domain>')
api_controller = ApiController(configuration, credentials)

response = api_controller.get('/api/v5/submissions')
```

## Using the ApiController 
The ApiController allows users to interact with the Hyperscience API using easy-to-use wrapper methods. You can find Hyperscience’s API documentation here.

### Supported HTTP Methods
GET, POST and PUT operations are supported by the ApiController.\
Content (query params, encoded url parameters or files input) is accepted in the form of Dict[str, str] or List[Tuple[str, str]].\
To support multiple parameters of the same type (e.g. 'file' for submitting multiple files), parameters should be passed as List[Tuple[str, str]].
#### Examples
Configuration and Setup
```python
from hyperscience import ApiController, Configuration
from hyperscience.api import DataSupportedMediaType, PayloadSupportedMediaType
```

# Create an ApiController instance 
```python
api_controller = ApiController(Configuration('cloud.hyperscience.net'))
```


#### GET Submissions
GET request with query params provided in dictionary
```python
query_params = {'state': 'complete'}
res = api_controller.get('/api/v5/submissions', query_params)
print(res, res.content)
```

GET request with query params provided in List[Tuple] format
```python
query_params = [('state', 'complete')]
res = api_controller.get('/api/v5/submissions', query_params)
print(res, res.content)
```

#### POST a New Submission using URL-Encoded Form.
POST request with WwwFormUrlEncoded content-type to submit files from remote servers
with List[Tuple] (multiple identical keys, e.g. multiple files)
```python
data = [
    ('file', 'https://www.dropbox.com/demo-long.pdf'),
    (
        'file',
        's3://hyperscience/bucket/form1.pdf',
    ),
    ('machine_only', True),
]
res = api_controller.post('/api/v5/submissions', data, DataSupportedMediaType.FORM_URL_ENCODED)
print(res, res.content)
```

POST request to submit files from remote servers with a dictionary (unique keys)
```python
data = {
    'file': 'https://www.dropbox.com/demo-long.pdf',
    'machine_only': True,
}
res = api_controller.post('/api/v5/submissions', data, DataSupportedMediaType.FORM_URL_ENCODED)
print(res, res.content)
```

POST request to submit files from remote servers with a dictionary (unique keys)
```python
data = {
    'file': 'https://www.dropbox.com/demo-long.pdf',
    'machine_only': True,
}
res = api_controller.post('/api/v5/submissions', data, DataSupportedMediaType.FORM_URL_ENCODED)
print(res, res.content)
```

#### POST a New Submission Using MultipartFormData
POST request with MultipartFormData content-type to upload files from local filesystem with dictionary (unique keys)
```python
data = {'file': '/absolute/path/to/file.pdf', 'machine_only': True}
res = api_controller.post('/api/v5/submissions', data, DataSupportedMediaType.MULTIPART_FORM_DATA)
print(res, res.content)
```

POST request with MultipartFormData content-type to upload files from local filesystem with List[Tuple] (multiple identical keys, e.g. multiple files)
```python
data = [
    ('file', '/absolute/path/to/file.pdf'),
    ('file', '/absolute/path/to/file2.pdf'),
    ('machine_only', True),
]
res = api_controller.post('/api/v5/submissions', data, DataSupportedMediaType.MULTIPART_FORM_DATA)
print(res, res.content)
```

#### POST a New Submission Using JSON
POST request with ApplicationJson content-type to submit base 64 encoded files using a dictionary
```python
json_data = {
    "metadata": {},
    "machine_only": True,
    "goal_duration_minutes": 5,
    "single_document_per_page": True,
    "restrictions": [],
    "source_routing_tags": ["tag1", "tag2"],
    "files": [
        {
            "file_content_base64": "data:image/png;base64,iVBORw0KGgoAAA…II=",
            "filename": "image.png"
        }
    ],
    "cases": [
        {
            "external_case_id": "case_1",
            "filenames": ["image.png"]
        }
    ]
}
res = api_controller.post('/api/v5/submissions', json_data, PayloadSupportedMediaType.APPLICATION_JSON)
print(res, res.content)
```

## Logging
The library implements HyperscienceLogging class to log messages related to the library.\ 
To set a different logging level, you can use the function HyperscienceLogging.set_hyperscience_logging_level() and choose from the following list of logging levels: CRITICAL, FATAL, ERROR, WARNING, INFO, DEBUG.