# bimdata_api_client.WebhookApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_web_hook**](WebhookApi.md#create_web_hook) | **POST** /cloud/{cloud_pk}/webhook | Create a new Webhook
[**delete_web_hook**](WebhookApi.md#delete_web_hook) | **DELETE** /cloud/{cloud_pk}/webhook/{id} | Delete a webhook
[**get_web_hook**](WebhookApi.md#get_web_hook) | **GET** /cloud/{cloud_pk}/webhook/{id} | Retrieve one configured webhook
[**get_web_hooks**](WebhookApi.md#get_web_hooks) | **GET** /cloud/{cloud_pk}/webhook | Retrieve all configured webhooks
[**ping_web_hook**](WebhookApi.md#ping_web_hook) | **POST** /cloud/{cloud_pk}/webhook/{id}/ping | Test a webhook
[**update_web_hook**](WebhookApi.md#update_web_hook) | **PATCH** /cloud/{cloud_pk}/webhook/{id} | Update some field of a webhook


# **create_web_hook**
> WebHook create_web_hook(cloud_pk, web_hook_request)

Create a new Webhook

Create a new Webhook  Required scopes: webhook:manage

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import webhook_api
from bimdata_api_client.model.web_hook import WebHook
from bimdata_api_client.model.web_hook_request import WebHookRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration.api_key['ApiKey'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKey'] = 'Bearer'

# Configure OAuth2 access token for authorization: BIMData_Connect
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: BIMData_Connect
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure API key authorization: Bearer
configuration.api_key['Bearer'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Bearer'] = 'Bearer'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = webhook_api.WebhookApi(api_client)
    cloud_pk = 1 # int | 
    web_hook_request = WebHookRequest(
        events=[
            "events_example",
        ],
        url="url_example",
        secret="secret_example",
    ) # WebHookRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Create a new Webhook
        api_response = api_instance.create_web_hook(cloud_pk, web_hook_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling WebhookApi->create_web_hook: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**|  |
 **web_hook_request** | [**WebHookRequest**](WebHookRequest.md)|  |

### Return type

[**WebHook**](WebHook.md)

### Authorization

[ApiKey](../README.md#ApiKey), [BIMData_Connect](../README.md#BIMData_Connect), [BIMData_Connect](../README.md#BIMData_Connect), [Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** |  |  -  |
**400** | A required field is missing in the body |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_web_hook**
> delete_web_hook(cloud_pk, id)

Delete a webhook

Delete a webhook  Required scopes: webhook:manage

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import webhook_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration.api_key['ApiKey'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKey'] = 'Bearer'

# Configure OAuth2 access token for authorization: BIMData_Connect
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: BIMData_Connect
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure API key authorization: Bearer
configuration.api_key['Bearer'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Bearer'] = 'Bearer'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = webhook_api.WebhookApi(api_client)
    cloud_pk = 1 # int | 
    id = 1 # int | A unique integer value identifying this web hook.

    # example passing only required values which don't have defaults set
    try:
        # Delete a webhook
        api_instance.delete_web_hook(cloud_pk, id)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling WebhookApi->delete_web_hook: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**|  |
 **id** | **int**| A unique integer value identifying this web hook. |

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey), [BIMData_Connect](../README.md#BIMData_Connect), [BIMData_Connect](../README.md#BIMData_Connect), [Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |
**400** | A required field is missing in the body |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_web_hook**
> WebHook get_web_hook(cloud_pk, id)

Retrieve one configured webhook

Retrieve one configured webhook  Required scopes: webhook:manage

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import webhook_api
from bimdata_api_client.model.web_hook import WebHook
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration.api_key['ApiKey'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKey'] = 'Bearer'

# Configure OAuth2 access token for authorization: BIMData_Connect
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: BIMData_Connect
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure API key authorization: Bearer
configuration.api_key['Bearer'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Bearer'] = 'Bearer'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = webhook_api.WebhookApi(api_client)
    cloud_pk = 1 # int | 
    id = 1 # int | A unique integer value identifying this web hook.

    # example passing only required values which don't have defaults set
    try:
        # Retrieve one configured webhook
        api_response = api_instance.get_web_hook(cloud_pk, id)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling WebhookApi->get_web_hook: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**|  |
 **id** | **int**| A unique integer value identifying this web hook. |

### Return type

[**WebHook**](WebHook.md)

### Authorization

[ApiKey](../README.md#ApiKey), [BIMData_Connect](../README.md#BIMData_Connect), [BIMData_Connect](../README.md#BIMData_Connect), [Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_web_hooks**
> [WebHook] get_web_hooks(cloud_pk)

Retrieve all configured webhooks

Retrieve all configured webhooks  Required scopes: webhook:manage

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import webhook_api
from bimdata_api_client.model.web_hook import WebHook
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration.api_key['ApiKey'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKey'] = 'Bearer'

# Configure OAuth2 access token for authorization: BIMData_Connect
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: BIMData_Connect
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure API key authorization: Bearer
configuration.api_key['Bearer'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Bearer'] = 'Bearer'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = webhook_api.WebhookApi(api_client)
    cloud_pk = 1 # int | 

    # example passing only required values which don't have defaults set
    try:
        # Retrieve all configured webhooks
        api_response = api_instance.get_web_hooks(cloud_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling WebhookApi->get_web_hooks: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**|  |

### Return type

[**[WebHook]**](WebHook.md)

### Authorization

[ApiKey](../README.md#ApiKey), [BIMData_Connect](../README.md#BIMData_Connect), [BIMData_Connect](../README.md#BIMData_Connect), [Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ping_web_hook**
> WebHook ping_web_hook(cloud_pk, id, web_hook_request)

Test a webhook

Trigger a Ping Event sending {\"ok\": true} to the webhook URL. Useful to test your app  Required scopes: webhook:manage

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import webhook_api
from bimdata_api_client.model.web_hook import WebHook
from bimdata_api_client.model.web_hook_request import WebHookRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration.api_key['ApiKey'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKey'] = 'Bearer'

# Configure OAuth2 access token for authorization: BIMData_Connect
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: BIMData_Connect
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure API key authorization: Bearer
configuration.api_key['Bearer'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Bearer'] = 'Bearer'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = webhook_api.WebhookApi(api_client)
    cloud_pk = 1 # int | 
    id = 1 # int | A unique integer value identifying this web hook.
    web_hook_request = WebHookRequest(
        events=[
            "events_example",
        ],
        url="url_example",
        secret="secret_example",
    ) # WebHookRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Test a webhook
        api_response = api_instance.ping_web_hook(cloud_pk, id, web_hook_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling WebhookApi->ping_web_hook: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**|  |
 **id** | **int**| A unique integer value identifying this web hook. |
 **web_hook_request** | [**WebHookRequest**](WebHookRequest.md)|  |

### Return type

[**WebHook**](WebHook.md)

### Authorization

[ApiKey](../README.md#ApiKey), [BIMData_Connect](../README.md#BIMData_Connect), [BIMData_Connect](../README.md#BIMData_Connect), [Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | A required field is missing in the body |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_web_hook**
> WebHook update_web_hook(cloud_pk, id)

Update some field of a webhook

Update some field of a webhook  Required scopes: webhook:manage

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import webhook_api
from bimdata_api_client.model.web_hook import WebHook
from bimdata_api_client.model.patched_web_hook_request import PatchedWebHookRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKey
configuration.api_key['ApiKey'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKey'] = 'Bearer'

# Configure OAuth2 access token for authorization: BIMData_Connect
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure OAuth2 access token for authorization: BIMData_Connect
configuration = bimdata_api_client.Configuration(
    host = "http://localhost"
)
configuration.access_token = 'YOUR_ACCESS_TOKEN'

# Configure API key authorization: Bearer
configuration.api_key['Bearer'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['Bearer'] = 'Bearer'

# Enter a context with an instance of the API client
with bimdata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = webhook_api.WebhookApi(api_client)
    cloud_pk = 1 # int | 
    id = 1 # int | A unique integer value identifying this web hook.
    patched_web_hook_request = PatchedWebHookRequest(
        events=[
            "events_example",
        ],
        url="url_example",
        secret="secret_example",
    ) # PatchedWebHookRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update some field of a webhook
        api_response = api_instance.update_web_hook(cloud_pk, id)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling WebhookApi->update_web_hook: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update some field of a webhook
        api_response = api_instance.update_web_hook(cloud_pk, id, patched_web_hook_request=patched_web_hook_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling WebhookApi->update_web_hook: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**|  |
 **id** | **int**| A unique integer value identifying this web hook. |
 **patched_web_hook_request** | [**PatchedWebHookRequest**](PatchedWebHookRequest.md)|  | [optional]

### Return type

[**WebHook**](WebHook.md)

### Authorization

[ApiKey](../README.md#ApiKey), [BIMData_Connect](../README.md#BIMData_Connect), [BIMData_Connect](../README.md#BIMData_Connect), [Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |
**400** | A required field is missing in the body |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

