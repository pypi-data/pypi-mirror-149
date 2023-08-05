# ApplicationServiceAssignment

An ApplicationServiceAssignment allows an Environment of an Application to access an ApplicationService. Essentially, ApplicationSerivceAssignment models a link between an Environment and an ApplicationService. For example, a collection of these with the same Environment would model the set of ApplicationServices that environment can access. Alternatively, a collection of these with the same ApplicationService would model the set of Environments that can access that ApplicationService. ApplicationServiceAssignments apply to the Organisation of the ApplicationService being assigned. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**app_id** | **str** | The identifier of the Application to which this service is being assigned.  | 
**environment_name** | **str** | The name of the Environment to which this ApplicationService is being assigned.  | 
**org_id** | **str** | The organisation owning the Application to which the ApplicationService is being assigned.  | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


