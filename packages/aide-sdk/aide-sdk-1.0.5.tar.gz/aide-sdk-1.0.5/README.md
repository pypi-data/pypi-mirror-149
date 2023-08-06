# AIDE SDK

## Introduction
This library allows you to build AI inference models to be run on the AIDE platform.

## Table of contents

* [Quickstart](#quickstart)
* [Packaging a model](#packaging--publishing)
  * [The Manifest file](#manifest-file)  
* [Accessing study data](#accessing-resources)
* [Saving output](#saving-output-data)
* [Logging & Model Failures](#logging)


### Quickstart
To get started:

```python3
from aide_sdk.application import AideApplication
from aide_sdk.inference.aideoperator import AideOperator
from aide_sdk.model.operatorcontext import OperatorContext
from aide_sdk.model.resource import Resource
from aide_sdk.utils.file_storage import FileStorage


class MyModel(AideOperator):

  def process(self, context: OperatorContext):
    origin_dicom = context.origin
    result = my_cool_stuff(origin_dicom)  # Your magic goes here
    
    file_manager = FileStorage(context)
    path = file_manager.save_dicom("my_results", result)
    
    result_dicom = Resource(format="dicom", content_type="result", file_path=path)
    context.add_resource(result_dicom)
    return context

AideApplication.start(operator=MyModel())
```

#### What we just did
The main application class is `AideApplication`. Once started, it will connect to the model's input queue and listen for new messages.
The single parameter required by Aide is the `operator` - this can be any object that implements the following method:

1. `process(context: OperatorContext)` - This is the operation method, it receives an OperatorContext as input, and should return it as output. The context object is a special object which allows access to input resources.


## Packaging & Publishing
Once your model is ready, it will need to be published onto the platform.
In order to do that, it'll need to be Dockerized.

### Docker image requirements
* The SDK needs to be installed on the image (using `pip install aide-sdk` or similar)
* The entrypoint to the container needs to run `AideApplication.start`.
* The following environment variables need to be set:
    * MANIFEST_PATH - the path to a [manifest](#manifest-file) file. 
  

### Manifest File

The manifest file provides the AIDE platform with the details it needs to use the model. It includes the following information:

* `model_name` - string
* `model_version` - string
* `model_description` - string, The description of your model.
* `predicate` - string, a valid [predicate string](#predicate-string).
* `mode` - string, a valid [mode string](#model-modes).

##### Model modes
The model mode determines how it'll be used by AIDE.
The mode string can have one of the following values:
  * `QA` - QA mode, when the model is still being tested.
  * `R` - Research mode.
  * `CU` - Clinical use.

##### Predicate String
The predicate string determines which inputs will be sent to the model.
It's a logical expression, evaluating to a boolean,

It's possible to use any comparison operator (`<`, `>`, `==`, `>=`, `<=`, `!=`) and combine using `AND` or `OR`.


The predicate supports evaluation against DICOM image metadata tags. Any DICOM tags that are wished to be evaluated against should be prefixed with the following: `DICOM_`. 

For example:
```json
DICOM_Modality == "MR" AND DICOM_SliceThickness <= 10
```
The above string will evaluate to true if the input DICOM "Modality" tag value is "MR" and the "SliceThickness" tag value is 10 or lower.

It is also possible to request specific resource types. For example:
```json
DICOM_Modality == "MR" AND DICOM_SliceThickness <= 10 AND resource.type == "nifty/origin"
```

Resource types are defined as format/content-type.

#### Manifest example
```json
{
  "model_name": "test_model",
  "model_version": "1.0.0",
  "model_description": "This is a test model",
  "mode": "QA",
  "predicate": "tetststs"
}
```

## Accessing Resources

The `process` method is called with an instance of `OperatorContext`, the reference for that object is shown below.

### Object Reference

#### OperatorContext

###### Properties
Property | Type | Description
--- | --- | ---
`origin` | Origin | The origin object contains the initial input information to this pipeline. 
`resources` | List[Resource] | The resources added by previous operators in the pipeline. 

###### Methods
Method | Return type | Description
--- | --- | ---
`get_resources_by_type(format: str, content_type: str)` | List[[Resource](#resource)] | Returns the resources of a specific type. 
`add_resource(resource: Resource)` | None | Add a new [Resource](#resource) to the resources list. This resource will be available to the next operators.
`set_error(error: str)` | None | Sets an error message in case the operator can't complete its operation. The execution will be marked as a failure.


#### Resource

###### Properties
Property | Type | Description
--- | --- | ---
`format` | str | The file format (e.g. nifti/dicom/etc) 
`content_type` | str | The content within this resource (eg "brain_scan", "white_matter")  
`file_path` | str | The file path of this resource. Returned by the file manager when saving. 
`namespace` | str | The UID of the operator that created this resource. Added automatically when saving resources.  


#### Origin(Resource)
The origin object is a special resource. It contains everything any resource contains, and additional information.

###### Properties
Property | Type | Description
--- | --- | ---
`format` | str | The file format (e.g. "dicom") 
`content_type` | str | The content within this resource (eg "origin")  
`file_path` | str | The path of this object. 
`namespace` | str | The UID of the operator that created this resource. Added automatically when saving resources.  
`received_timestamp` | datetime | The time and date on which the origin object was first received by AIDE.  
`patient_id` | str | The patient ID this data refers to.  


#### DicomOrigin(Origin)
This origin object is used when the original input data is a DICOM study.

###### Properties
Property | Type | Description
--- | --- | ---
`format` | str | The file format (e.g. "dicom") 
`content_type` | str | The content within this resource (eg "origin")  
`file_path` | str | The path of this object. 
`namespace` | str | The UID of the operator that created this resource. Added automatically when saving resources.  
`received_timestamp` | datetime | The time and date on which the origin object was first received by AIDE.  
`patient_id` | str | The patient ID this data refers to.  
`study_uid` | str | The DICOM Study ID.  
`series` | List[[DicomSeries](#dicomseries)] | The DICOM series in this study.  

###### Methods
Method | Return type | Description
--- | --- | ---
`get_series_by_id()` | [DicomSeries](#dicomseries) | Reads the dicom file and instantiates a pydicom `Dataset` from it.


#### DicomSeries
A DicomSeries object refers to a specific series of images.

###### Properties
Property | Type | Description
--- | --- | ---
`series_id` | str | The UID of this series.
`metadata` | dict | A dictionary containing series metadata.
`images` | List[[DicomImage](#DicomImage)] | A list of dicom images included in this series. 

#### DicomImage
This is a wrapper object around a PyDicom `Dataset` object.

###### Properties
Property | Type | Description
--- | --- | ---
`context_metadata` | dict | A dictionary containing the image metadata.
`image_path` | str | The path to the .dcm file.

###### Methods
Method | Return type | Description
--- | --- | ---
`load_dataset()` | pydicom.Dataset | Reads the dicom file and instantiates a pydicom `Dataset` from it.
`get_filename()` | str | Returns the dicom filename (e.g. "filename.dcm")
`get_context_metadata()` | str | Returns the image metadata, loading it if hasn't been loaded.
`reload_context_metadata()` | str | Reloads the context metadata from the file.


## Saving output Data

#### FileStorage

This helper class allows you to save files, with convenience methods to help save DICOM images and PDF files. 
To use it, instantiate it with an [OperatorContext](#operatorcontext) object.

###### Methods
Method | Return type | Description
--- | --- | ---
`save_file(file_bytes: bytes, file_name: str)` | str | Saves binary data to disk, and returns a path string with its location on disk. Requires binary data and a file name.
`load_file(file_path: str)` | bytes | Loads a file from disk, using a path string.
`save_dicom(folder_name: str, dataset: pydicom.Dataset)` | str | Saves a PyDicom `Dataset` to disk, and returns a path string with its location on disk. Requires a container folder name and the pydicom `Dataset`.
`save_encapsulated_pdf(folder_name: str, dataset: Dataset, pdf_file_path: str)` | str | Save a PDF file, encapsulated within a DICOM file. This function require a folder name, the `Dataset` the PDF relates to, and the pdf file path. Returns the dicom path.


## Logging
Logging is possible using the `aide_sdk.logger.logger.LogManager` class:
```python
from aide_sdk.logger.logger import LogManager

logger = LogManager.get_logger()
logger.info("info message")
logger.warn("warn message")
logger.error("error message")
logger.exception("exception message")
```

### Failures vs Errors
There are two ways in which operators can fail - either a response can't be reached, for example because of a lack of statistical significance, or an error occurred while attempting to run the operator.

Failures are still a valid result. To log an error response, use the [OperatorContext](#operatorcontext) `set_failure` method:
```python
context.set_failure("Couldn't reach conclusion")
return context
```

However, unexpected errors should raise an exception. It is possible to use the `ModelError` exception for this:
```python
from aide_sdk.utils.exceptions import ModelError

try:
  something()
except Exception:
  LogManager.get_logger().exception("Failed")
  raise ModelError("Unknown error while running model")
```