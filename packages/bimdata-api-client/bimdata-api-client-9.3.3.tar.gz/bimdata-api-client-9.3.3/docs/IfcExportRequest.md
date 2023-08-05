# IfcExportRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file_name** | **str** | The name of the exported IFC file. It MUST end with .ifc or the exported file won&#39;t be processed by BIMData | 
**classifications** | **str** | Exported IFC will include classifications from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include classifications(NONE) | [optional]  if omitted the server will use the default value of "UPDATED"
**zones** | **str** | Exported IFC will include zones from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include zones(NONE) | [optional]  if omitted the server will use the default value of "UPDATED"
**properties** | **str** | Exported IFC will include properties from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include properties(NONE) | [optional]  if omitted the server will use the default value of "UPDATED"
**systems** | **str** | Exported IFC will include systems from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include systems(NONE) | [optional]  if omitted the server will use the default value of "UPDATED"
**layers** | **str** | Exported IFC will include layers from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include layers(NONE) | [optional]  if omitted the server will use the default value of "UPDATED"
**materials** | **str** | Exported IFC will include materials from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include materials(NONE) | [optional]  if omitted the server will use the default value of "UPDATED"
**attributes** | **str** | Exported IFC will include attributes from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include attributes(NONE) | [optional]  if omitted the server will use the default value of "UPDATED"
**structure** | **str** | Exported IFC will include the structure from original IFC file (ORIGINAL), from latest API updates (UPDATED), or won&#39;t include structure(NONE) | [optional]  if omitted the server will use the default value of "UPDATED"
**uuids** | **[str]** | Exported IFC will only have those elements. If omitted, all elements will be exported | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


