# OralEyeApi.CameraApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cameraAutofocusPost**](CameraApi.md#cameraAutofocusPost) | **POST** /camera/autofocus | Set auto-focus on/off
[**cameraCapturePost**](CameraApi.md#cameraCapturePost) | **POST** /camera/capture | Capture raw image
[**cameraDownloadRawGet**](CameraApi.md#cameraDownloadRawGet) | **GET** /camera/download_raw | Download raw file of a capture
[**cameraExposurePost**](CameraApi.md#cameraExposurePost) | **POST** /camera/exposure | Set exposure time
[**cameraManualFocusPost**](CameraApi.md#cameraManualFocusPost) | **POST** /camera/manual_focus | Set manual focus distance
[**cameraMetadataGet**](CameraApi.md#cameraMetadataGet) | **GET** /camera/metadata | Retrieve metadata of a capture
[**cameraPreviewStartPost**](CameraApi.md#cameraPreviewStartPost) | **POST** /camera/preview/start | Start camera preview
[**cameraPreviewStopPost**](CameraApi.md#cameraPreviewStopPost) | **POST** /camera/preview/stop | Stop camera preview
[**cameraPreviewVideoFeedGet**](CameraApi.md#cameraPreviewVideoFeedGet) | **GET** /camera/preview/video_feed | Get MJPEG video feed



## cameraAutofocusPost

> LightsControlPost200Response cameraAutofocusPost(cameraAutofocusPostRequest)

Set auto-focus on/off

### Example

```javascript
import OralEyeApi from 'oral_eye_api';

let apiInstance = new OralEyeApi.CameraApi();
let cameraAutofocusPostRequest = new OralEyeApi.CameraAutofocusPostRequest(); // CameraAutofocusPostRequest | 
apiInstance.cameraAutofocusPost(cameraAutofocusPostRequest, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cameraAutofocusPostRequest** | [**CameraAutofocusPostRequest**](CameraAutofocusPostRequest.md)|  | 

### Return type

[**LightsControlPost200Response**](LightsControlPost200Response.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## cameraCapturePost

> File cameraCapturePost()

Capture raw image

### Example

```javascript
import OralEyeApi from 'oral_eye_api';

let apiInstance = new OralEyeApi.CameraApi();
apiInstance.cameraCapturePost((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

**File**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/octet-stream


## cameraDownloadRawGet

> File cameraDownloadRawGet(jobId, light)

Download raw file of a capture

### Example

```javascript
import OralEyeApi from 'oral_eye_api';

let apiInstance = new OralEyeApi.CameraApi();
let jobId = "jobId_example"; // String | 
let light = "light_example"; // String | 
apiInstance.cameraDownloadRawGet(jobId, light, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **jobId** | **String**|  | 
 **light** | **String**|  | 

### Return type

**File**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/octet-stream, application/json


## cameraExposurePost

> LightsControlPost200Response cameraExposurePost(cameraExposurePostRequest)

Set exposure time

### Example

```javascript
import OralEyeApi from 'oral_eye_api';

let apiInstance = new OralEyeApi.CameraApi();
let cameraExposurePostRequest = new OralEyeApi.CameraExposurePostRequest(); // CameraExposurePostRequest | 
apiInstance.cameraExposurePost(cameraExposurePostRequest, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cameraExposurePostRequest** | [**CameraExposurePostRequest**](CameraExposurePostRequest.md)|  | 

### Return type

[**LightsControlPost200Response**](LightsControlPost200Response.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## cameraManualFocusPost

> LightsControlPost200Response cameraManualFocusPost(cameraManualFocusPostRequest)

Set manual focus distance

### Example

```javascript
import OralEyeApi from 'oral_eye_api';

let apiInstance = new OralEyeApi.CameraApi();
let cameraManualFocusPostRequest = new OralEyeApi.CameraManualFocusPostRequest(); // CameraManualFocusPostRequest | 
apiInstance.cameraManualFocusPost(cameraManualFocusPostRequest, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cameraManualFocusPostRequest** | [**CameraManualFocusPostRequest**](CameraManualFocusPostRequest.md)|  | 

### Return type

[**LightsControlPost200Response**](LightsControlPost200Response.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: application/json
- **Accept**: application/json


## cameraMetadataGet

> CameraMetadataGet200Response cameraMetadataGet(jobId, light)

Retrieve metadata of a capture

### Example

```javascript
import OralEyeApi from 'oral_eye_api';

let apiInstance = new OralEyeApi.CameraApi();
let jobId = "jobId_example"; // String | 
let light = "light_example"; // String | 
apiInstance.cameraMetadataGet(jobId, light, (error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **jobId** | **String**|  | 
 **light** | **String**|  | 

### Return type

[**CameraMetadataGet200Response**](CameraMetadataGet200Response.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## cameraPreviewStartPost

> LightsControlPost200Response cameraPreviewStartPost()

Start camera preview

### Example

```javascript
import OralEyeApi from 'oral_eye_api';

let apiInstance = new OralEyeApi.CameraApi();
apiInstance.cameraPreviewStartPost((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**LightsControlPost200Response**](LightsControlPost200Response.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## cameraPreviewStopPost

> LightsControlPost200Response cameraPreviewStopPost()

Stop camera preview

### Example

```javascript
import OralEyeApi from 'oral_eye_api';

let apiInstance = new OralEyeApi.CameraApi();
apiInstance.cameraPreviewStopPost((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**LightsControlPost200Response**](LightsControlPost200Response.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: application/json


## cameraPreviewVideoFeedGet

> File cameraPreviewVideoFeedGet()

Get MJPEG video feed

Streams MJPEG video feed from the camera

### Example

```javascript
import OralEyeApi from 'oral_eye_api';

let apiInstance = new OralEyeApi.CameraApi();
apiInstance.cameraPreviewVideoFeedGet((error, data, response) => {
  if (error) {
    console.error(error);
  } else {
    console.log('API called successfully. Returned data: ' + data);
  }
});
```

### Parameters

This endpoint does not need any parameter.

### Return type

**File**

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: multipart/x-mixed-replace

