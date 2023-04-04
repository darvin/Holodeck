# holoimage_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**route_generate_image_image_get**](DefaultApi.md#route_generate_image_image_get) | **GET** /image | Route Generate Image
[**route_generate_image_verified_image_verified_get**](DefaultApi.md#route_generate_image_verified_image_verified_get) | **GET** /image_verified | Route Generate Image Verified
[**route_root_get**](DefaultApi.md#route_root_get) | **GET** / | Route Root


# **route_generate_image_image_get**
> Any route_generate_image_image_get(prompt, api_token)

Route Generate Image

### Example

```python
from __future__ import print_function
import time
import holoimage_client
from holoimage_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = holoimage_client.DefaultApi()
prompt = 'prompt_example' # str | 
api_token = 'api_token_example' # str | 

try:
    # Route Generate Image
    api_response = api_instance.route_generate_image_image_get(prompt, api_token)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->route_generate_image_image_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt** | **str**|  | 
 **api_token** | **str**|  | 

### Return type

[**Any**](Any.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **route_generate_image_verified_image_verified_get**
> Any route_generate_image_verified_image_verified_get(prompt, api_token, max_attempts=max_attempts)

Route Generate Image Verified

### Example

```python
from __future__ import print_function
import time
import holoimage_client
from holoimage_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = holoimage_client.DefaultApi()
prompt = 'prompt_example' # str | 
api_token = 'api_token_example' # str | 
max_attempts = 3 # int |  (optional) (default to 3)

try:
    # Route Generate Image Verified
    api_response = api_instance.route_generate_image_verified_image_verified_get(prompt, api_token, max_attempts=max_attempts)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->route_generate_image_verified_image_verified_get: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **prompt** | **str**|  | 
 **api_token** | **str**|  | 
 **max_attempts** | **int**|  | [optional] [default to 3]

### Return type

[**Any**](Any.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **route_root_get**
> Any route_root_get()

Route Root

### Example

```python
from __future__ import print_function
import time
import holoimage_client
from holoimage_client.rest import ApiException
from pprint import pprint

# Create an instance of the API class
api_instance = holoimage_client.DefaultApi()

try:
    # Route Root
    api_response = api_instance.route_root_get()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->route_root_get: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**Any**](Any.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

