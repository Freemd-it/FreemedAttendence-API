# face_detection

----------------

Face detection sample APIs for freemed attendence API server.

----------------

## healthcheck

```
GET {{api}}/
```

healthcheck

----------------

### Request

> 

### Examples:

> 

----------------

## fileupload

```
POST {{api}}/fileupload
```

fileupload

----------------

### Request

> 
> **Body**
> 
> |Key|Value|Type|Description|
> |---|---|---|---|
> |user_file||file||
> 

### Examples:

> 

----------------

## facedetect/draw

```
POST {{API_HOST}}/facedetect/draw
```

facedetect/draw

----------------

### Request

> 

### Examples:

> 

----------------

## facedetect/bboxes

```
POST {{API_HOST}}/facedetect/bboxes
```

facedetect/bboxes

----------------

### Request

> 
> **Body**
> 
> |Key|Value|Type|Description|
> |---|---|---|---|
> |user_file||file||
> 

### Examples:

> 

----------------

----------------

Built with [Postdown][PyPI].

Author: [Titor](https://github.com/TitorX)

[PyPI]:    https://pypi.python.org/pypi/Postdown
