# bimdata_api_client.SsoApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**accept_invitation**](SsoApi.md#accept_invitation) | **POST** /identity-provider/invitation/{id}/accept | Accept an invitation
[**delete_user**](SsoApi.md#delete_user) | **DELETE** /identity-provider/user | Delete user from BIMData
[**deny_invitation**](SsoApi.md#deny_invitation) | **POST** /identity-provider/invitation/{id}/deny | Deny an invitation
[**get_invitation**](SsoApi.md#get_invitation) | **GET** /identity-provider/invitation/{id} | Retrieve an invitation
[**get_invitations**](SsoApi.md#get_invitations) | **GET** /identity-provider/invitation | Retrieve all invitations


# **accept_invitation**
> accept_invitation(id)

Accept an invitation

If the user already exists, s·he is added to the cloud and projet. If not, we wait their first connection to add them.  Required scopes: org:manage

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import sso_api
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
    api_instance = sso_api.SsoApi(api_client)
    id = 1 # int | A unique integer value identifying this invitation.

    # example passing only required values which don't have defaults set
    try:
        # Accept an invitation
        api_instance.accept_invitation(id)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling SsoApi->accept_invitation: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this invitation. |

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

# **delete_user**
> delete_user()

Delete user from BIMData

Delete the user and all clouds where the user is alone

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import sso_api
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
    api_instance = sso_api.SsoApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Delete user from BIMData
        api_instance.delete_user()
    except bimdata_api_client.ApiException as e:
        print("Exception when calling SsoApi->delete_user: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

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
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **deny_invitation**
> deny_invitation(id)

Deny an invitation

The invitation status change to DENIED and the user is not added to the cloud. You can accept an invitation previously denied  Required scopes: org:manage

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import sso_api
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
    api_instance = sso_api.SsoApi(api_client)
    id = 1 # int | A unique integer value identifying this invitation.

    # example passing only required values which don't have defaults set
    try:
        # Deny an invitation
        api_instance.deny_invitation(id)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling SsoApi->deny_invitation: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this invitation. |

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

# **get_invitation**
> Invitation get_invitation(id)

Retrieve an invitation

Retrieve all invitations of your identity provider  Required scopes: org:manage

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import sso_api
from bimdata_api_client.model.invitation import Invitation
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
    api_instance = sso_api.SsoApi(api_client)
    id = 1 # int | A unique integer value identifying this invitation.

    # example passing only required values which don't have defaults set
    try:
        # Retrieve an invitation
        api_response = api_instance.get_invitation(id)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling SsoApi->get_invitation: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **int**| A unique integer value identifying this invitation. |

### Return type

[**Invitation**](Invitation.md)

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

# **get_invitations**
> [Invitation] get_invitations()

Retrieve all invitations

Retrieve all invitations of your identity provider  Required scopes: org:manage

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import sso_api
from bimdata_api_client.model.invitation import Invitation
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
    api_instance = sso_api.SsoApi(api_client)
    status = "A" # str |          A: Accepted         D: Denied         P: Pending          (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Retrieve all invitations
        api_response = api_instance.get_invitations(status=status)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling SsoApi->get_invitations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **status** | **str**|          A: Accepted         D: Denied         P: Pending          | [optional]

### Return type

[**[Invitation]**](Invitation.md)

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

