from . import aws
from PIL import Image, ImageDraw
from io import BytesIO
from mtcnn.src import detect_faces



def facedetect_from_url(image_url):
    s3 = aws.get_aws_resource()
    bucket = s3.Bucket('freemed-attendence')
    object = bucket.Object(image_url)
    img = Image.open(BytesIO(object.get()['Body'].read())).convert('RGB')
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
