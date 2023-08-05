# bimdata_api_client.CheckerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_checker**](CheckerApi.md#create_checker) | **POST** /cloud/{cloud_pk}/project/{project_pk}/model/{model_pk}/checker | Create a checker to a model
[**create_checker_result**](CheckerApi.md#create_checker_result) | **POST** /cloud/{cloud_pk}/project/{project_pk}/model/{model_pk}/checker/{checker_pk}/result | Create a CheckerResult
[**create_checkplan**](CheckerApi.md#create_checkplan) | **POST** /cloud/{cloud_pk}/project/{project_pk}/checkplan | Create a Checkplan
[**create_rule**](CheckerApi.md#create_rule) | **POST** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset/{ruleset_pk}/rule | Create a Rule
[**create_rule_component**](CheckerApi.md#create_rule_component) | **POST** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset/{ruleset_pk}/rule/{rule_pk}/rulecomponent | Create a RuleComponent
[**create_ruleset**](CheckerApi.md#create_ruleset) | **POST** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset | Create a Ruleset
[**delete_checker**](CheckerApi.md#delete_checker) | **DELETE** /cloud/{cloud_pk}/project/{project_pk}/model/{model_pk}/checker/{id} | Delete a checker of a model
[**delete_checker_result**](CheckerApi.md#delete_checker_result) | **DELETE** /cloud/{cloud_pk}/project/{project_pk}/model/{model_pk}/checker/{checker_pk}/result/{id} | Delete a CheckerResult
[**delete_checkplan**](CheckerApi.md#delete_checkplan) | **DELETE** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{id} | Delete a Checkplan
[**delete_rule**](CheckerApi.md#delete_rule) | **DELETE** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset/{ruleset_pk}/rule/{id} | Delete a Rule
[**delete_rule_component**](CheckerApi.md#delete_rule_component) | **DELETE** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset/{ruleset_pk}/rule/{rule_pk}/rulecomponent/{id} | Delete a RuleComponent
[**delete_ruleset**](CheckerApi.md#delete_ruleset) | **DELETE** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset/{id} | Delete a Ruleset
[**get_checker**](CheckerApi.md#get_checker) | **GET** /cloud/{cloud_pk}/project/{project_pk}/model/{model_pk}/checker/{id} | Retrieve a checker of a model
[**get_checker_result**](CheckerApi.md#get_checker_result) | **GET** /cloud/{cloud_pk}/project/{project_pk}/model/{model_pk}/checker/{checker_pk}/result/{id} | Retrieve one CheckerResult
[**get_checker_results**](CheckerApi.md#get_checker_results) | **GET** /cloud/{cloud_pk}/project/{project_pk}/model/{model_pk}/checker/{checker_pk}/result | Retrieve all CheckerResults
[**get_checkers**](CheckerApi.md#get_checkers) | **GET** /cloud/{cloud_pk}/project/{project_pk}/model/{model_pk}/checker | Retrieve all checkers of a model
[**get_checkplan**](CheckerApi.md#get_checkplan) | **GET** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{id} | Retrieve one Checkplan
[**get_checkplans**](CheckerApi.md#get_checkplans) | **GET** /cloud/{cloud_pk}/project/{project_pk}/checkplan | Retrieve all Checkplans
[**get_rule**](CheckerApi.md#get_rule) | **GET** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset/{ruleset_pk}/rule/{id} | Retrieve one Rule
[**get_rule_component**](CheckerApi.md#get_rule_component) | **GET** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset/{ruleset_pk}/rule/{rule_pk}/rulecomponent/{id} | Retrieve one RuleComponent
[**get_rule_components**](CheckerApi.md#get_rule_components) | **GET** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset/{ruleset_pk}/rule/{rule_pk}/rulecomponent | Retrieve all RuleComponents
[**get_rules**](CheckerApi.md#get_rules) | **GET** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset/{ruleset_pk}/rule | Retrieve all Rules
[**get_ruleset**](CheckerApi.md#get_ruleset) | **GET** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset/{id} | Retrieve one Ruleset
[**get_rulesets**](CheckerApi.md#get_rulesets) | **GET** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset | Retrieve all Rulesets
[**launch_new_check**](CheckerApi.md#launch_new_check) | **POST** /cloud/{cloud_pk}/project/{project_pk}/model/{model_pk}/checker/{id}/launch-check | Launch a new check on the model
[**update_checker**](CheckerApi.md#update_checker) | **PATCH** /cloud/{cloud_pk}/project/{project_pk}/model/{model_pk}/checker/{id} | Update some fields of a checker of a model
[**update_checker_result**](CheckerApi.md#update_checker_result) | **PATCH** /cloud/{cloud_pk}/project/{project_pk}/model/{model_pk}/checker/{checker_pk}/result/{id} | Update some fields of a CheckerResult
[**update_checkplan**](CheckerApi.md#update_checkplan) | **PATCH** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{id} | Update some fields of a Checkplan
[**update_rule**](CheckerApi.md#update_rule) | **PATCH** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset/{ruleset_pk}/rule/{id} | Update some fields of a Rule
[**update_rule_component**](CheckerApi.md#update_rule_component) | **PATCH** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset/{ruleset_pk}/rule/{rule_pk}/rulecomponent/{id} | Update some fields of a RuleComponent
[**update_ruleset**](CheckerApi.md#update_ruleset) | **PATCH** /cloud/{cloud_pk}/project/{project_pk}/checkplan/{check_plan_pk}/ruleset/{id} | Update some fields of a Ruleset


# **create_checker**
> IfcChecker create_checker(cloud_pk, model_pk, project_pk)

Create a checker to a model

A checker is a link between a checkplan and a model. A checker can launch a check multiple time and store all the results  Required scopes: check:write, ifc:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.ifc_checker import IfcChecker
from bimdata_api_client.model.ifc_checker_request import IfcCheckerRequest
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
    api_instance = checker_api.CheckerApi(api_client)
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    model_pk = 1 # int | A unique integer value identifying this model.
    project_pk = 1 # int | A unique integer value identifying this project.
    ifc_checker_request = IfcCheckerRequest(
        name="name_example",
        checkplan_id=1,
    ) # IfcCheckerRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create a checker to a model
        api_response = api_instance.create_checker(cloud_pk, model_pk, project_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->create_checker: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create a checker to a model
        api_response = api_instance.create_checker(cloud_pk, model_pk, project_pk, ifc_checker_request=ifc_checker_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->create_checker: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **model_pk** | **int**| A unique integer value identifying this model. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **ifc_checker_request** | [**IfcCheckerRequest**](IfcCheckerRequest.md)|  | [optional]

### Return type

[**IfcChecker**](IfcChecker.md)

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

# **create_checker_result**
> CheckerResult create_checker_result(checker_pk, cloud_pk, model_pk, project_pk)

Create a CheckerResult

TCreate a CheckerResult  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.checker_result_request import CheckerResultRequest
from bimdata_api_client.model.checker_result import CheckerResult
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
    api_instance = checker_api.CheckerApi(api_client)
    checker_pk = 1 # int | A unique integer value identifying this ifc checker.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    model_pk = 1 # int | A unique integer value identifying this model.
    project_pk = 1 # int | A unique integer value identifying this project.
    checker_result_request = CheckerResultRequest(
        status="C",
        result="result_example",
        collisions="collisions_example",
        error_detail="error_detail_example",
    ) # CheckerResultRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create a CheckerResult
        api_response = api_instance.create_checker_result(checker_pk, cloud_pk, model_pk, project_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->create_checker_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create a CheckerResult
        api_response = api_instance.create_checker_result(checker_pk, cloud_pk, model_pk, project_pk, checker_result_request=checker_result_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->create_checker_result: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **checker_pk** | **int**| A unique integer value identifying this ifc checker. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **model_pk** | **int**| A unique integer value identifying this model. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **checker_result_request** | [**CheckerResultRequest**](CheckerResultRequest.md)|  | [optional]

### Return type

[**CheckerResult**](CheckerResult.md)

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

# **create_checkplan**
> CheckPlan create_checkplan(cloud_pk, project_pk, check_plan_request)

Create a Checkplan

TCreate a Checkplan  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.check_plan_request import CheckPlanRequest
from bimdata_api_client.model.check_plan import CheckPlan
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
    api_instance = checker_api.CheckerApi(api_client)
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    project_pk = 1 # int | A unique integer value identifying this project.
    check_plan_request = CheckPlanRequest(
        name="name_example",
        description="description_example",
        rulesets=[
            RulesetRequest(
                parent_ruleset_id=1,
                name="name_example",
                description="description_example",
                rules=[
                    RuleRequest(
                        name="name_example",
                        condition="condition_example",
                        rule_components=[
                            RuleComponentRequest(
                                type="type_example",
                                value={
                                    "key": None,
                                },
                                operator="operator_example",
                                params={
                                    "key": None,
                                },
                                condition="condition_example",
                                rule_components={
                                    "key": None,
                                },
                            ),
                        ],
                        on=RuleRequest(),
                    ),
                ],
                rulesets=[],
            ),
        ],
    ) # CheckPlanRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Create a Checkplan
        api_response = api_instance.create_checkplan(cloud_pk, project_pk, check_plan_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->create_checkplan: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **check_plan_request** | [**CheckPlanRequest**](CheckPlanRequest.md)|  |

### Return type

[**CheckPlan**](CheckPlan.md)

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

# **create_rule**
> Rule create_rule(check_plan_pk, cloud_pk, project_pk, ruleset_pk, rule_request)

Create a Rule

TCreate a Rule  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.rule_request import RuleRequest
from bimdata_api_client.model.rule import Rule
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    project_pk = 1 # int | A unique integer value identifying this project.
    ruleset_pk = 1 # int | A unique integer value identifying this ruleset.
    rule_request = RuleRequest(
        name="name_example",
        condition="condition_example",
        rule_components=[
            RuleComponentRequest(
                type="type_example",
                value={
                    "key": None,
                },
                operator="operator_example",
                params={
                    "key": None,
                },
                condition="condition_example",
                rule_components={
                    "key": None,
                },
            ),
        ],
        on=RuleRequest(),
    ) # RuleRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Create a Rule
        api_response = api_instance.create_rule(check_plan_pk, cloud_pk, project_pk, ruleset_pk, rule_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->create_rule: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **ruleset_pk** | **int**| A unique integer value identifying this ruleset. |
 **rule_request** | [**RuleRequest**](RuleRequest.md)|  |

### Return type

[**Rule**](Rule.md)

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

# **create_rule_component**
> RuleComponent create_rule_component(check_plan_pk, cloud_pk, project_pk, rule_pk, ruleset_pk)

Create a RuleComponent

TCreate a RuleComponent  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.rule_component_request import RuleComponentRequest
from bimdata_api_client.model.rule_component import RuleComponent
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    project_pk = 1 # int | A unique integer value identifying this project.
    rule_pk = 1 # int | A unique integer value identifying this rule.
    ruleset_pk = 1 # int | A unique integer value identifying this ruleset.
    rule_component_request = RuleComponentRequest(
        type="type_example",
        value={
            "key": None,
        },
        operator="operator_example",
        params={
            "key": None,
        },
        condition="condition_example",
        rule_components={
            "key": None,
        },
    ) # RuleComponentRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Create a RuleComponent
        api_response = api_instance.create_rule_component(check_plan_pk, cloud_pk, project_pk, rule_pk, ruleset_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->create_rule_component: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Create a RuleComponent
        api_response = api_instance.create_rule_component(check_plan_pk, cloud_pk, project_pk, rule_pk, ruleset_pk, rule_component_request=rule_component_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->create_rule_component: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **rule_pk** | **int**| A unique integer value identifying this rule. |
 **ruleset_pk** | **int**| A unique integer value identifying this ruleset. |
 **rule_component_request** | [**RuleComponentRequest**](RuleComponentRequest.md)|  | [optional]

### Return type

[**RuleComponent**](RuleComponent.md)

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

# **create_ruleset**
> Ruleset create_ruleset(check_plan_pk, cloud_pk, project_pk, ruleset_request)

Create a Ruleset

TCreate a Ruleset  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.ruleset import Ruleset
from bimdata_api_client.model.ruleset_request import RulesetRequest
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    project_pk = 1 # int | A unique integer value identifying this project.
    ruleset_request = RulesetRequest(
        parent_ruleset_id=1,
        name="name_example",
        description="description_example",
        rules=[
            RuleRequest(
                name="name_example",
                condition="condition_example",
                rule_components=[
                    RuleComponentRequest(
                        type="type_example",
                        value={
                            "key": None,
                        },
                        operator="operator_example",
                        params={
                            "key": None,
                        },
                        condition="condition_example",
                        rule_components={
                            "key": None,
                        },
                    ),
                ],
                on=RuleRequest(),
            ),
        ],
        rulesets=[
            RulesetRequest(),
        ],
    ) # RulesetRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Create a Ruleset
        api_response = api_instance.create_ruleset(check_plan_pk, cloud_pk, project_pk, ruleset_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->create_ruleset: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **ruleset_request** | [**RulesetRequest**](RulesetRequest.md)|  |

### Return type

[**Ruleset**](Ruleset.md)

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

# **delete_checker**
> delete_checker(cloud_pk, id, model_pk, project_pk)

Delete a checker of a model

A checker is a link between a checkplan and a model. A checker can launch a check multiple time and store all the results  Required scopes: check:write, ifc:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
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
    api_instance = checker_api.CheckerApi(api_client)
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this ifc checker.
    model_pk = 1 # int | A unique integer value identifying this model.
    project_pk = 1 # int | A unique integer value identifying this project.

    # example passing only required values which don't have defaults set
    try:
        # Delete a checker of a model
        api_instance.delete_checker(cloud_pk, id, model_pk, project_pk)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->delete_checker: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this ifc checker. |
 **model_pk** | **int**| A unique integer value identifying this model. |
 **project_pk** | **int**| A unique integer value identifying this project. |

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

# **delete_checker_result**
> delete_checker_result(checker_pk, cloud_pk, id, model_pk, project_pk)

Delete a CheckerResult

Delete a CheckerResult  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
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
    api_instance = checker_api.CheckerApi(api_client)
    checker_pk = 1 # int | A unique integer value identifying this ifc checker.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this checker result.
    model_pk = 1 # int | A unique integer value identifying this model.
    project_pk = 1 # int | A unique integer value identifying this project.

    # example passing only required values which don't have defaults set
    try:
        # Delete a CheckerResult
        api_instance.delete_checker_result(checker_pk, cloud_pk, id, model_pk, project_pk)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->delete_checker_result: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **checker_pk** | **int**| A unique integer value identifying this ifc checker. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this checker result. |
 **model_pk** | **int**| A unique integer value identifying this model. |
 **project_pk** | **int**| A unique integer value identifying this project. |

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

# **delete_checkplan**
> delete_checkplan(cloud_pk, id, project_pk)

Delete a Checkplan

Delete a Checkplan  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
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
    api_instance = checker_api.CheckerApi(api_client)
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this check plan.
    project_pk = 1 # int | A unique integer value identifying this project.

    # example passing only required values which don't have defaults set
    try:
        # Delete a Checkplan
        api_instance.delete_checkplan(cloud_pk, id, project_pk)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->delete_checkplan: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this check plan. |
 **project_pk** | **int**| A unique integer value identifying this project. |

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

# **delete_rule**
> delete_rule(check_plan_pk, cloud_pk, id, project_pk, ruleset_pk)

Delete a Rule

Delete a Rule  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this rule.
    project_pk = 1 # int | A unique integer value identifying this project.
    ruleset_pk = 1 # int | A unique integer value identifying this ruleset.

    # example passing only required values which don't have defaults set
    try:
        # Delete a Rule
        api_instance.delete_rule(check_plan_pk, cloud_pk, id, project_pk, ruleset_pk)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->delete_rule: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this rule. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **ruleset_pk** | **int**| A unique integer value identifying this ruleset. |

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

# **delete_rule_component**
> delete_rule_component(check_plan_pk, cloud_pk, id, project_pk, rule_pk, ruleset_pk)

Delete a RuleComponent

Delete a RuleComponent  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this rule component.
    project_pk = 1 # int | A unique integer value identifying this project.
    rule_pk = 1 # int | A unique integer value identifying this rule.
    ruleset_pk = 1 # int | A unique integer value identifying this ruleset.

    # example passing only required values which don't have defaults set
    try:
        # Delete a RuleComponent
        api_instance.delete_rule_component(check_plan_pk, cloud_pk, id, project_pk, rule_pk, ruleset_pk)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->delete_rule_component: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this rule component. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **rule_pk** | **int**| A unique integer value identifying this rule. |
 **ruleset_pk** | **int**| A unique integer value identifying this ruleset. |

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

# **delete_ruleset**
> delete_ruleset(check_plan_pk, cloud_pk, id, project_pk)

Delete a Ruleset

Delete a Ruleset  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this ruleset.
    project_pk = 1 # int | A unique integer value identifying this project.

    # example passing only required values which don't have defaults set
    try:
        # Delete a Ruleset
        api_instance.delete_ruleset(check_plan_pk, cloud_pk, id, project_pk)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->delete_ruleset: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this ruleset. |
 **project_pk** | **int**| A unique integer value identifying this project. |

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

# **get_checker**
> IfcChecker get_checker(cloud_pk, id, model_pk, project_pk)

Retrieve a checker of a model

A checker is a link between a checkplan and a model. A checker can launch a check multiple time and store all the results  Required scopes: check:read, ifc:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.ifc_checker import IfcChecker
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
    api_instance = checker_api.CheckerApi(api_client)
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this ifc checker.
    model_pk = 1 # int | A unique integer value identifying this model.
    project_pk = 1 # int | A unique integer value identifying this project.

    # example passing only required values which don't have defaults set
    try:
        # Retrieve a checker of a model
        api_response = api_instance.get_checker(cloud_pk, id, model_pk, project_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->get_checker: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this ifc checker. |
 **model_pk** | **int**| A unique integer value identifying this model. |
 **project_pk** | **int**| A unique integer value identifying this project. |

### Return type

[**IfcChecker**](IfcChecker.md)

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

# **get_checker_result**
> CheckerResult get_checker_result(checker_pk, cloud_pk, id, model_pk, project_pk)

Retrieve one CheckerResult

Retrieve one CheckerResult  Required scopes: check:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.checker_result import CheckerResult
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
    api_instance = checker_api.CheckerApi(api_client)
    checker_pk = 1 # int | A unique integer value identifying this ifc checker.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this checker result.
    model_pk = 1 # int | A unique integer value identifying this model.
    project_pk = 1 # int | A unique integer value identifying this project.

    # example passing only required values which don't have defaults set
    try:
        # Retrieve one CheckerResult
        api_response = api_instance.get_checker_result(checker_pk, cloud_pk, id, model_pk, project_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->get_checker_result: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **checker_pk** | **int**| A unique integer value identifying this ifc checker. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this checker result. |
 **model_pk** | **int**| A unique integer value identifying this model. |
 **project_pk** | **int**| A unique integer value identifying this project. |

### Return type

[**CheckerResult**](CheckerResult.md)

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

# **get_checker_results**
> [CheckerResult] get_checker_results(checker_pk, cloud_pk, model_pk, project_pk)

Retrieve all CheckerResults

Retrieve all CheckerResults  Required scopes: check:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.checker_result import CheckerResult
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
    api_instance = checker_api.CheckerApi(api_client)
    checker_pk = 1 # int | A unique integer value identifying this ifc checker.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    model_pk = 1 # int | A unique integer value identifying this model.
    project_pk = 1 # int | A unique integer value identifying this project.

    # example passing only required values which don't have defaults set
    try:
        # Retrieve all CheckerResults
        api_response = api_instance.get_checker_results(checker_pk, cloud_pk, model_pk, project_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->get_checker_results: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **checker_pk** | **int**| A unique integer value identifying this ifc checker. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **model_pk** | **int**| A unique integer value identifying this model. |
 **project_pk** | **int**| A unique integer value identifying this project. |

### Return type

[**[CheckerResult]**](CheckerResult.md)

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

# **get_checkers**
> [IfcChecker] get_checkers(cloud_pk, model_pk, project_pk)

Retrieve all checkers of a model

A checker is a link between a checkplan and a model. A checker can launch a check multiple time and store all the results  Required scopes: check:read, ifc:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.ifc_checker import IfcChecker
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
    api_instance = checker_api.CheckerApi(api_client)
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    model_pk = 1 # int | A unique integer value identifying this model.
    project_pk = 1 # int | A unique integer value identifying this project.

    # example passing only required values which don't have defaults set
    try:
        # Retrieve all checkers of a model
        api_response = api_instance.get_checkers(cloud_pk, model_pk, project_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->get_checkers: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **model_pk** | **int**| A unique integer value identifying this model. |
 **project_pk** | **int**| A unique integer value identifying this project. |

### Return type

[**[IfcChecker]**](IfcChecker.md)

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

# **get_checkplan**
> CheckPlan get_checkplan(cloud_pk, id, project_pk)

Retrieve one Checkplan

Retrieve one Checkplan  Required scopes: check:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.check_plan import CheckPlan
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
    api_instance = checker_api.CheckerApi(api_client)
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this check plan.
    project_pk = 1 # int | A unique integer value identifying this project.

    # example passing only required values which don't have defaults set
    try:
        # Retrieve one Checkplan
        api_response = api_instance.get_checkplan(cloud_pk, id, project_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->get_checkplan: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this check plan. |
 **project_pk** | **int**| A unique integer value identifying this project. |

### Return type

[**CheckPlan**](CheckPlan.md)

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

# **get_checkplans**
> [CheckPlan] get_checkplans(cloud_pk, project_pk)

Retrieve all Checkplans

Retrieve all Checkplans  Required scopes: check:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.check_plan import CheckPlan
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
    api_instance = checker_api.CheckerApi(api_client)
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    project_pk = 1 # int | A unique integer value identifying this project.

    # example passing only required values which don't have defaults set
    try:
        # Retrieve all Checkplans
        api_response = api_instance.get_checkplans(cloud_pk, project_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->get_checkplans: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **project_pk** | **int**| A unique integer value identifying this project. |

### Return type

[**[CheckPlan]**](CheckPlan.md)

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

# **get_rule**
> Rule get_rule(check_plan_pk, cloud_pk, id, project_pk, ruleset_pk)

Retrieve one Rule

Retrieve one Rule  Required scopes: check:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.rule import Rule
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this rule.
    project_pk = 1 # int | A unique integer value identifying this project.
    ruleset_pk = 1 # int | A unique integer value identifying this ruleset.

    # example passing only required values which don't have defaults set
    try:
        # Retrieve one Rule
        api_response = api_instance.get_rule(check_plan_pk, cloud_pk, id, project_pk, ruleset_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->get_rule: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this rule. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **ruleset_pk** | **int**| A unique integer value identifying this ruleset. |

### Return type

[**Rule**](Rule.md)

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

# **get_rule_component**
> RuleComponent get_rule_component(check_plan_pk, cloud_pk, id, project_pk, rule_pk, ruleset_pk)

Retrieve one RuleComponent

Retrieve one RuleComponent  Required scopes: check:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.rule_component import RuleComponent
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this rule component.
    project_pk = 1 # int | A unique integer value identifying this project.
    rule_pk = 1 # int | A unique integer value identifying this rule.
    ruleset_pk = 1 # int | A unique integer value identifying this ruleset.

    # example passing only required values which don't have defaults set
    try:
        # Retrieve one RuleComponent
        api_response = api_instance.get_rule_component(check_plan_pk, cloud_pk, id, project_pk, rule_pk, ruleset_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->get_rule_component: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this rule component. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **rule_pk** | **int**| A unique integer value identifying this rule. |
 **ruleset_pk** | **int**| A unique integer value identifying this ruleset. |

### Return type

[**RuleComponent**](RuleComponent.md)

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

# **get_rule_components**
> [RuleComponent] get_rule_components(check_plan_pk, cloud_pk, project_pk, rule_pk, ruleset_pk)

Retrieve all RuleComponents

Retrieve all RuleComponents  Required scopes: check:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.rule_component import RuleComponent
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    project_pk = 1 # int | A unique integer value identifying this project.
    rule_pk = 1 # int | A unique integer value identifying this rule.
    ruleset_pk = 1 # int | A unique integer value identifying this ruleset.

    # example passing only required values which don't have defaults set
    try:
        # Retrieve all RuleComponents
        api_response = api_instance.get_rule_components(check_plan_pk, cloud_pk, project_pk, rule_pk, ruleset_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->get_rule_components: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **rule_pk** | **int**| A unique integer value identifying this rule. |
 **ruleset_pk** | **int**| A unique integer value identifying this ruleset. |

### Return type

[**[RuleComponent]**](RuleComponent.md)

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

# **get_rules**
> [Rule] get_rules(check_plan_pk, cloud_pk, project_pk, ruleset_pk)

Retrieve all Rules

Retrieve all Rules  Required scopes: check:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.rule import Rule
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    project_pk = 1 # int | A unique integer value identifying this project.
    ruleset_pk = 1 # int | A unique integer value identifying this ruleset.

    # example passing only required values which don't have defaults set
    try:
        # Retrieve all Rules
        api_response = api_instance.get_rules(check_plan_pk, cloud_pk, project_pk, ruleset_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->get_rules: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **ruleset_pk** | **int**| A unique integer value identifying this ruleset. |

### Return type

[**[Rule]**](Rule.md)

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

# **get_ruleset**
> Ruleset get_ruleset(check_plan_pk, cloud_pk, id, project_pk)

Retrieve one Ruleset

Retrieve one Ruleset  Required scopes: check:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.ruleset import Ruleset
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this ruleset.
    project_pk = 1 # int | A unique integer value identifying this project.

    # example passing only required values which don't have defaults set
    try:
        # Retrieve one Ruleset
        api_response = api_instance.get_ruleset(check_plan_pk, cloud_pk, id, project_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->get_ruleset: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this ruleset. |
 **project_pk** | **int**| A unique integer value identifying this project. |

### Return type

[**Ruleset**](Ruleset.md)

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

# **get_rulesets**
> [Ruleset] get_rulesets(check_plan_pk, cloud_pk, project_pk)

Retrieve all Rulesets

Retrieve all Rulesets  Required scopes: check:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.ruleset import Ruleset
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    project_pk = 1 # int | A unique integer value identifying this project.

    # example passing only required values which don't have defaults set
    try:
        # Retrieve all Rulesets
        api_response = api_instance.get_rulesets(check_plan_pk, cloud_pk, project_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->get_rulesets: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **project_pk** | **int**| A unique integer value identifying this project. |

### Return type

[**[Ruleset]**](Ruleset.md)

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

# **launch_new_check**
> launch_new_check(cloud_pk, id, model_pk, project_pk)

Launch a new check on the model

A nex check will be played with the current state of elements, properties, etc.  Required scopes: check:write, ifc:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.ifc_checker_request import IfcCheckerRequest
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
    api_instance = checker_api.CheckerApi(api_client)
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this ifc checker.
    model_pk = 1 # int | A unique integer value identifying this model.
    project_pk = 1 # int | A unique integer value identifying this project.
    ifc_checker_request = IfcCheckerRequest(
        name="name_example",
        checkplan_id=1,
    ) # IfcCheckerRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Launch a new check on the model
        api_instance.launch_new_check(cloud_pk, id, model_pk, project_pk)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->launch_new_check: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Launch a new check on the model
        api_instance.launch_new_check(cloud_pk, id, model_pk, project_pk, ifc_checker_request=ifc_checker_request)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->launch_new_check: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this ifc checker. |
 **model_pk** | **int**| A unique integer value identifying this model. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **ifc_checker_request** | [**IfcCheckerRequest**](IfcCheckerRequest.md)|  | [optional]

### Return type

void (empty response body)

### Authorization

[ApiKey](../README.md#ApiKey), [BIMData_Connect](../README.md#BIMData_Connect), [BIMData_Connect](../README.md#BIMData_Connect), [Bearer](../README.md#Bearer)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | No response body |  -  |
**400** | A required field is missing in the body |  -  |
**401** | The authentication failed. Your token may be expired, missing or malformed |  -  |
**403** | You don&#39;t have the authorization to access this resource. Check if the resource is exclusive to users or app (eg: /user is exclusive to users) or if your user has the right to access this resource. |  -  |
**404** | The resource does not exist or you don&#39;t have the right to see if the resource exists |  -  |
**500** | Something really bad happened. Check if your route is correct. By example: /cloud/[object Object]/project may raise a 500. An alert is automatically sent to us, we&#39;ll look at it shortly. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_checker**
> IfcChecker update_checker(cloud_pk, id, model_pk, project_pk)

Update some fields of a checker of a model

A checker is a link between a checkplan and a model. A checker can launch a check multiple time and store all the results  Required scopes: check:write, ifc:read

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.ifc_checker import IfcChecker
from bimdata_api_client.model.patched_ifc_checker_request import PatchedIfcCheckerRequest
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
    api_instance = checker_api.CheckerApi(api_client)
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this ifc checker.
    model_pk = 1 # int | A unique integer value identifying this model.
    project_pk = 1 # int | A unique integer value identifying this project.
    patched_ifc_checker_request = PatchedIfcCheckerRequest(
        name="name_example",
        checkplan_id=1,
    ) # PatchedIfcCheckerRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update some fields of a checker of a model
        api_response = api_instance.update_checker(cloud_pk, id, model_pk, project_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->update_checker: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update some fields of a checker of a model
        api_response = api_instance.update_checker(cloud_pk, id, model_pk, project_pk, patched_ifc_checker_request=patched_ifc_checker_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->update_checker: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this ifc checker. |
 **model_pk** | **int**| A unique integer value identifying this model. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **patched_ifc_checker_request** | [**PatchedIfcCheckerRequest**](PatchedIfcCheckerRequest.md)|  | [optional]

### Return type

[**IfcChecker**](IfcChecker.md)

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

# **update_checker_result**
> CheckerResult update_checker_result(checker_pk, cloud_pk, id, model_pk, project_pk)

Update some fields of a CheckerResult

Update some fields of a CheckerResult  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.patched_checker_result_request import PatchedCheckerResultRequest
from bimdata_api_client.model.checker_result import CheckerResult
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
    api_instance = checker_api.CheckerApi(api_client)
    checker_pk = 1 # int | A unique integer value identifying this ifc checker.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this checker result.
    model_pk = 1 # int | A unique integer value identifying this model.
    project_pk = 1 # int | A unique integer value identifying this project.
    patched_checker_result_request = PatchedCheckerResultRequest(
        status="C",
        result="result_example",
        collisions="collisions_example",
        error_detail="error_detail_example",
    ) # PatchedCheckerResultRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update some fields of a CheckerResult
        api_response = api_instance.update_checker_result(checker_pk, cloud_pk, id, model_pk, project_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->update_checker_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update some fields of a CheckerResult
        api_response = api_instance.update_checker_result(checker_pk, cloud_pk, id, model_pk, project_pk, patched_checker_result_request=patched_checker_result_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->update_checker_result: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **checker_pk** | **int**| A unique integer value identifying this ifc checker. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this checker result. |
 **model_pk** | **int**| A unique integer value identifying this model. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **patched_checker_result_request** | [**PatchedCheckerResultRequest**](PatchedCheckerResultRequest.md)|  | [optional]

### Return type

[**CheckerResult**](CheckerResult.md)

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

# **update_checkplan**
> CheckPlan update_checkplan(cloud_pk, id, project_pk)

Update some fields of a Checkplan

Update some fields of a Checkplan  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.patched_check_plan_request import PatchedCheckPlanRequest
from bimdata_api_client.model.check_plan import CheckPlan
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
    api_instance = checker_api.CheckerApi(api_client)
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this check plan.
    project_pk = 1 # int | A unique integer value identifying this project.
    patched_check_plan_request = PatchedCheckPlanRequest(
        name="name_example",
        description="description_example",
        rulesets=[
            RulesetRequest(
                parent_ruleset_id=1,
                name="name_example",
                description="description_example",
                rules=[
                    RuleRequest(
                        name="name_example",
                        condition="condition_example",
                        rule_components=[
                            RuleComponentRequest(
                                type="type_example",
                                value={
                                    "key": None,
                                },
                                operator="operator_example",
                                params={
                                    "key": None,
                                },
                                condition="condition_example",
                                rule_components={
                                    "key": None,
                                },
                            ),
                        ],
                        on=RuleRequest(),
                    ),
                ],
                rulesets=[],
            ),
        ],
    ) # PatchedCheckPlanRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update some fields of a Checkplan
        api_response = api_instance.update_checkplan(cloud_pk, id, project_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->update_checkplan: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update some fields of a Checkplan
        api_response = api_instance.update_checkplan(cloud_pk, id, project_pk, patched_check_plan_request=patched_check_plan_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->update_checkplan: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this check plan. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **patched_check_plan_request** | [**PatchedCheckPlanRequest**](PatchedCheckPlanRequest.md)|  | [optional]

### Return type

[**CheckPlan**](CheckPlan.md)

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

# **update_rule**
> Rule update_rule(check_plan_pk, cloud_pk, id, project_pk, ruleset_pk)

Update some fields of a Rule

Update some fields of a Rule  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.rule import Rule
from bimdata_api_client.model.patched_rule_request import PatchedRuleRequest
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this rule.
    project_pk = 1 # int | A unique integer value identifying this project.
    ruleset_pk = 1 # int | A unique integer value identifying this ruleset.
    patched_rule_request = PatchedRuleRequest(
        name="name_example",
        condition="condition_example",
        rule_components=[
            RuleComponentRequest(
                type="type_example",
                value={
                    "key": None,
                },
                operator="operator_example",
                params={
                    "key": None,
                },
                condition="condition_example",
                rule_components={
                    "key": None,
                },
            ),
        ],
        on=RuleRequest(
            name="name_example",
            condition="condition_example",
            rule_components=[
                RuleComponentRequest(
                    type="type_example",
                    value={
                        "key": None,
                    },
                    operator="operator_example",
                    params={
                        "key": None,
                    },
                    condition="condition_example",
                    rule_components={
                        "key": None,
                    },
                ),
            ],
            on=RuleRequest(),
        ),
    ) # PatchedRuleRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update some fields of a Rule
        api_response = api_instance.update_rule(check_plan_pk, cloud_pk, id, project_pk, ruleset_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->update_rule: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update some fields of a Rule
        api_response = api_instance.update_rule(check_plan_pk, cloud_pk, id, project_pk, ruleset_pk, patched_rule_request=patched_rule_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->update_rule: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this rule. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **ruleset_pk** | **int**| A unique integer value identifying this ruleset. |
 **patched_rule_request** | [**PatchedRuleRequest**](PatchedRuleRequest.md)|  | [optional]

### Return type

[**Rule**](Rule.md)

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

# **update_rule_component**
> RuleComponent update_rule_component(check_plan_pk, cloud_pk, id, project_pk, rule_pk, ruleset_pk)

Update some fields of a RuleComponent

Update some fields of a RuleComponent  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.patched_rule_component_request import PatchedRuleComponentRequest
from bimdata_api_client.model.rule_component import RuleComponent
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this rule component.
    project_pk = 1 # int | A unique integer value identifying this project.
    rule_pk = 1 # int | A unique integer value identifying this rule.
    ruleset_pk = 1 # int | A unique integer value identifying this ruleset.
    patched_rule_component_request = PatchedRuleComponentRequest(
        type="type_example",
        value={
            "key": None,
        },
        operator="operator_example",
        params={
            "key": None,
        },
        condition="condition_example",
        rule_components={
            "key": None,
        },
    ) # PatchedRuleComponentRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update some fields of a RuleComponent
        api_response = api_instance.update_rule_component(check_plan_pk, cloud_pk, id, project_pk, rule_pk, ruleset_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->update_rule_component: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update some fields of a RuleComponent
        api_response = api_instance.update_rule_component(check_plan_pk, cloud_pk, id, project_pk, rule_pk, ruleset_pk, patched_rule_component_request=patched_rule_component_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->update_rule_component: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this rule component. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **rule_pk** | **int**| A unique integer value identifying this rule. |
 **ruleset_pk** | **int**| A unique integer value identifying this ruleset. |
 **patched_rule_component_request** | [**PatchedRuleComponentRequest**](PatchedRuleComponentRequest.md)|  | [optional]

### Return type

[**RuleComponent**](RuleComponent.md)

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

# **update_ruleset**
> Ruleset update_ruleset(check_plan_pk, cloud_pk, id, project_pk)

Update some fields of a Ruleset

Update some fields of a Ruleset  Required scopes: check:write

### Example

* Api Key Authentication (ApiKey):
* OAuth Authentication (BIMData_Connect):
* OAuth Authentication (BIMData_Connect):
* Api Key Authentication (Bearer):

```python
import time
import bimdata_api_client
from bimdata_api_client.api import checker_api
from bimdata_api_client.model.patched_ruleset_request import PatchedRulesetRequest
from bimdata_api_client.model.ruleset import Ruleset
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
    api_instance = checker_api.CheckerApi(api_client)
    check_plan_pk = 1 # int | A unique integer value identifying this check plan.
    cloud_pk = 1 # int | A unique integer value identifying this cloud.
    id = 1 # int | A unique integer value identifying this ruleset.
    project_pk = 1 # int | A unique integer value identifying this project.
    patched_ruleset_request = PatchedRulesetRequest(
        parent_ruleset_id=1,
        name="name_example",
        description="description_example",
        rules=[
            RuleRequest(
                name="name_example",
                condition="condition_example",
                rule_components=[
                    RuleComponentRequest(
                        type="type_example",
                        value={
                            "key": None,
                        },
                        operator="operator_example",
                        params={
                            "key": None,
                        },
                        condition="condition_example",
                        rule_components={
                            "key": None,
                        },
                    ),
                ],
                on=RuleRequest(),
            ),
        ],
        rulesets=[
            RulesetRequest(
                parent_ruleset_id=1,
                name="name_example",
                description="description_example",
                rules=[
                    RuleRequest(
                        name="name_example",
                        condition="condition_example",
                        rule_components=[
                            RuleComponentRequest(
                                type="type_example",
                                value={
                                    "key": None,
                                },
                                operator="operator_example",
                                params={
                                    "key": None,
                                },
                                condition="condition_example",
                                rule_components={
                                    "key": None,
                                },
                            ),
                        ],
                        on=RuleRequest(),
                    ),
                ],
                rulesets=[],
            ),
        ],
    ) # PatchedRulesetRequest |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Update some fields of a Ruleset
        api_response = api_instance.update_ruleset(check_plan_pk, cloud_pk, id, project_pk)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->update_ruleset: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Update some fields of a Ruleset
        api_response = api_instance.update_ruleset(check_plan_pk, cloud_pk, id, project_pk, patched_ruleset_request=patched_ruleset_request)
        pprint(api_response)
    except bimdata_api_client.ApiException as e:
        print("Exception when calling CheckerApi->update_ruleset: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **check_plan_pk** | **int**| A unique integer value identifying this check plan. |
 **cloud_pk** | **int**| A unique integer value identifying this cloud. |
 **id** | **int**| A unique integer value identifying this ruleset. |
 **project_pk** | **int**| A unique integer value identifying this project. |
 **patched_ruleset_request** | [**PatchedRulesetRequest**](PatchedRulesetRequest.md)|  | [optional]

### Return type

[**Ruleset**](Ruleset.md)

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

