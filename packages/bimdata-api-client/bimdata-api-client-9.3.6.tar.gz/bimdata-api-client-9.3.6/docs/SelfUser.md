# SelfUser


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [readonly] 
**email** | **str** |  | 
**firstname** | **str** |  | 
**lastname** | **str** |  | 
**created_at** | **datetime** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**organizations** | [**[Organization]**](Organization.md) |  | [readonly] 
**clouds** | [**[CloudRole]**](CloudRole.md) |  | [readonly] 
**projects** | [**[ProjectRole]**](ProjectRole.md) |  | [readonly] 
**provider** | **str** |  | [readonly] 
**sub** | **str, none_type** | sub from Keycloak | [readonly] 
**profile_picture** | **str, none_type** |  | [readonly] 
**provider_sub** | **str, none_type** | sub from original identity provider | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


