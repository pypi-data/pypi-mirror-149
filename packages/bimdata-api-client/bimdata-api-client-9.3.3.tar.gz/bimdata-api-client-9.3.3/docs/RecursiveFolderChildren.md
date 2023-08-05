# RecursiveFolderChildren


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**parent_id** | **int, none_type** |  | [readonly] 
**type** | **str** | DEPRECATED: Use &#39;nature&#39; instead. Values can be &#39;Folder&#39;, &#39;Document&#39; or &#39;Ifc&#39;. It is usefull to parse the tree and discriminate folders and files | [readonly] 
**nature** | **str** | Values can be &#39;Folder&#39;, &#39;Document&#39; or &#39;Model&#39;. It is usefull to parse the tree and discriminate folders and files | [readonly] 
**model_type** | **str, none_type** | Model&#39;s type. Values can be IFC, DWG, DXF, GLTF, PDF, JPEG, PNG, OBJ, DAE, BFX | [readonly] 
**name** | **str** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 
**model_id** | **int, none_type** |  | [readonly] 
**ifc_id** | **int, none_type** | DEPRECATED: Use &#39;model_id&#39; instead | [readonly] 
**groups_permissions** | [**[FolderGroupPermission], none_type**](FolderGroupPermission.md) | Groups permissions of folder | [readonly] 
**default_permission** | **int** | Default permissions of folder | [readonly] 
**user_permission** | **int** | Aggregate of group user permissions and folder default permission | [readonly] 
**created_by** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [optional] 
**creator** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [optional] 
**file_name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**size** | **int** |  | [optional] 
**file** | **str** |  | [optional] 
**children** | [**[RecursiveFolderChildren], none_type**](RecursiveFolderChildren.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


