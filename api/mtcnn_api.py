from . import aws
from PIL import Image, ImageDraw
from io import BytesIO
from mtcnn.src import detect_faces
from flask import current_app, Blueprint

bp = Blueprint("mtcnn_api", __name__)
MAX_SIZE = (1024, 1024)

# 1. s3 상에 저장된 이미지를 읽어온다.
# 2. 얼굴 검출을 실행한다.
# 3. 검출 결과로 나온 얼굴 영역 좌표 값을 리턴한다.
def detect(image_url):
    s3 = aws.get_aws_resource()
    bucket = s3.Bucket(current_app.config['S3_BUCKET'])
    object = bucket.Object(image_url)
    img = Image.open(BytesIO(object.get()['Body'].read())).convert('RGB')
    img.thumbnail(MAX_SIZE, Image.ANTIALIAS)

    bounding_boxes, landmarks = detect_faces(img)
    filtered_boxes = []
    accuracy_limit = 0.90
    for box in bounding_boxes:
        if box[4] < accuracy_limit:
            continue
        x0 = int(box[0])
        y0 = int(box[1])
        x1 = int(box[2])
        y1 = int(box[3])
        filtered_boxes.append([x0, y0, x1, y1])
    return filtered_boxes

# 1. s3 상에 저장된 이미지를 읽어온다.
# 2. 얼굴 검출을 실행한다.
# 3. 얼굴 검출된 영역을 이미지 상에 그려주고, 이미지 자체를 리턴한다.
def detect_and_draw(image_url):
    s3 = aws.get_aws_resource()
    bucket = s3.Bucket(current_app.config['S3_BUCKET'])
    object = bucket.Object(image_url)
    img = Image.open(BytesIO(object.get()['Body'].read())).convert('RGB')
    img.thumbnail(MAX_SIZE, Image.ANTIALIAS)

    draw = ImageDraw.Draw(img)

    bounding_boxes, landmarks = detect_faces(img)
    filtered_boxes = []
    accuracy_limit = 0.90
    for box in bounding_boxes:
        if box[4] < accuracy_limit:
            continue
        x0 = int(box[0])
        y0 = int(box[1])
        x1 = int(box[2])
        y1 = int(box[3])
        filtered_boxes.append([x0, y0, x1, y1])
        draw.rectangle([(x0, y0), (x1, y1)], outline="red", width=5)
    return img


