from datetime import datetime
import os
from PIL import Image, ExifTags

def current_time_str():
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def project_home():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def tmp_dir():
    return os.path.join(project_home(), 'data/tmp')

def get_pil_image(image_dir, image_file):
    img = Image.open(os.path.join(image_dir, image_file))
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation': break
    exif = dict(img._getexif().items())

    if exif[orientation] == 3:
        img = img.rotate(180, expand=True)
    elif exif[orientation] == 6:
        img = img.rotate(270, expand=True)
    elif exif[orientation] == 8:
        img = img.rotate(90, expand=True)
    return img

if __name__ == '__main__':
    print(project_home())
