# Folder


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [readonly] 
**type** | **str** | DEPRECATED: Use &#39;nature&#39; instead. Value is \&quot;Folder\&quot;. It is usefull to parse the tree and discriminate folders and files | [readonly] 
**nature** | **str** | Value is \&quot;Folder\&quot;. It is usefull to parse the tree and discriminate folders and files | [readonly] 
**name** | **str** | Name of the folder | 
**created_at** | **datetime** | Creation date | [readonly] 
**updated_at** | **datetime** | Date of the last update | [readonly] 
**created_by** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [readonly] 
**groups_permissions** | [**[FolderGroupPermission]**](FolderGroupPermission.md) |  | [readonly] 
**user_permission** | **int** | Aggregate of group user permissions and folder default permission | [readonly] 
**children** | [**[RecursiveFolderChildren]**](RecursiveFolderChildren.md) |  | [readonly] 
**parent_id** | **int, none_type** |  | [optional] 
**default_permission** | **int** | Permission for a Folder | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


