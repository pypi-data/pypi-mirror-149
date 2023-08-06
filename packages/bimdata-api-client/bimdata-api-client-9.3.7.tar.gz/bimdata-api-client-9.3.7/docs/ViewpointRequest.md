# ViewpointRequest

Adds nested create feature

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**index** | **int, none_type** |  | [optional] 
**guid** | **str** |  | [optional] 
**orthogonal_camera** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [optional] 
**perspective_camera** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [optional] 
**lines** | [**[LineRequest], none_type**](LineRequest.md) |  | [optional] 
**clipping_planes** | [**[ClippingPlaneRequest], none_type**](ClippingPlaneRequest.md) |  | [optional] 
**snapshot** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [optional] 
**components** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [optional] 
**pins** | **[[float]], none_type** | Non standard field. Pins is a list of points representing annotation positions | [optional] 
**temp_id** | **int, none_type** | Only used when using POST on the full-topic route to bind viewpoint with comment | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


