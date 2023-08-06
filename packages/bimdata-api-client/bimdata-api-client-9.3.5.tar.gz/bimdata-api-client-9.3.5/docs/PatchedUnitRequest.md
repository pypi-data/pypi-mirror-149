# PatchedUnitRequest

Adds nested create feature

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | IfcDerivedUnit, IfcContextDependentUnit, IfcConversionBasedUnit, IfcSIUnit or IfcMonetaryUnit | [optional] 
**name** | **str, none_type** | Name of the unit (ex: DEGREE) | [optional] 
**unit_type** | **str, none_type** | IFC type of the unit or user defined type (ex: PLANEANGLEUNIT for DEGREE and RADIAN) | [optional] 
**prefix** | **str, none_type** | Litteral prefix for scale (ex: MILLI, KILO, etc..) | [optional] 
**dimensions** | **[float], none_type** | List of 7 units dimensions | [optional] 
**conversion_factor** | **float, none_type** | Factor of conversion and base unit id (ex: DEGREE from RADIAN with factor 0.0174532925199433) | [optional] 
**conversion_baseunit** | [**UnitRequest**](UnitRequest.md) |  | [optional] 
**elements** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}, none_type** | List of constitutive unit elements by id with corresponding exponent (ex: [meterID/1, secondID/-1] for velocity) | [optional] 
**is_default** | **bool** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


