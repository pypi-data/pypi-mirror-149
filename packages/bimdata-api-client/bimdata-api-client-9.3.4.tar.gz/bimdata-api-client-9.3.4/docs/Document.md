# Document


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [readonly] 
**created_by** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [readonly] 
**project** | **int** |  | [readonly] 
**name** | **str** | Shown name of the file | 
**file** | **str** |  | 
**tags** | [**[Tag]**](Tag.md) |  | [readonly] 
**visas** | [**[Visa]**](Visa.md) |  | [readonly] 
**created_at** | **datetime** | Creation date | [readonly] 
**updated_at** | **datetime** | Date of the last update | [readonly] 
**model_id** | **int, none_type** |  | [readonly] 
**model_type** | **str, none_type** | Model&#39;s type. Values can be IFC, DWG, DXF, GLTF, PDF, JPEG, PNG, OBJ, DAE, BFX | [readonly] 
**ifc_id** | **int, none_type** | DEPRECATED: Use &#39;model_id&#39; instead. | [readonly] 
**user_permission** | **int** | Aggregate of group user permissions and folder default permission | [readonly] 
**parent_id** | **int, none_type** |  | [optional] 
**file_name** | **str** | Full name of the file | [optional] 
**description** | **str, none_type** | Description of the file | [optional] 
**size** | **int, none_type** | Size of the file. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


