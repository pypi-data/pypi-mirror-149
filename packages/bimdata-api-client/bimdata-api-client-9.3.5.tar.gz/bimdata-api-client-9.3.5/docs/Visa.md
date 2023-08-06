# Visa


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [readonly] 
**validations** | [**[VisaValidation]**](VisaValidation.md) |  | [readonly] 
**validations_in_error** | **[int]** | Validation IDs where one or more validators have no longer access to the visa document. | [readonly] 
**creator** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [readonly] 
**document_id** | **int** |  | [readonly] 
**status** | **str** |  | [readonly] 
**comments** | [**[VisaComment]**](VisaComment.md) |  | [readonly] 
**created_at** | **datetime** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**description** | **str, none_type** | Description of the visa | [optional] 
**deadline** | **date, none_type** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


