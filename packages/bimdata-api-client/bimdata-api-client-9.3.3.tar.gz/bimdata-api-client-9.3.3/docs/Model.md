# Model


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | [readonly] 
**type** | **str** |  | [readonly] 
**creator** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [readonly] 
**status** | **str** |  | 
**created_at** | **datetime** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**document_id** | **int, none_type** |  | [readonly] 
**document** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [readonly] 
**structure_file** | **str, none_type** |  | [readonly] 
**systems_file** | **str, none_type** |  | [readonly] 
**map_file** | **str, none_type** |  | [readonly] 
**gltf_file** | **str, none_type** |  | [readonly] 
**bvh_tree_file** | **str, none_type** |  | [readonly] 
**viewer_360_file** | **str, none_type** |  | [readonly] 
**xkt_file** | **str, none_type** |  | [readonly] 
**project_id** | **int** |  | [readonly] 
**errors** | **[str], none_type** | List of errors that happened during IFC processing | [readonly] 
**warnings** | **[str], none_type** | List of warnings that happened during IFC processing | [readonly] 
**name** | **str, none_type** |  | [optional] 
**source** | **str** |  | [optional] 
**world_position** | **[float], none_type** | [x,y,z] array of the position of the local_placement in world coordinates | [optional] 
**size_ratio** | **float, none_type** | How many meters a unit represents | [optional] 
**archived** | **bool** |  | [optional] 
**version** | **str, none_type** | This field is only for information. Updating it won&#39;t impact the export. | [optional] 
**north_vector** | **[[float]], none_type** | This field is only for information. Updating it won&#39;t impact the export. | [optional] 
**recommanded_2d_angle** | **float, none_type** | This is the angle in clockwise degree to apply on the 2D to optimise the horizontality of objects. This field is only for information. Updating it won&#39;t impact the export. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


