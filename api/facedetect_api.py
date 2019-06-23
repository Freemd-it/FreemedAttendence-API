#-*- coding:utf-8 -*-
import os
from flask import Blueprint, render_template, request, current_app, Response
from flask_restful import Api

import json
from . import aws, mtcnn_api
from . import util

bp = Blueprint("facedetect_api", __name__)


@bp.route("/")
def healthcheck():
    return json.dumps({"message": "server live!"})


@bp.route("/upload")
def render_file():
    return render_template("upload.html")


# s3로 이미지 파일을 업로드하는 API
@bp.route("/fileupload", methods=["POST"])
def fileupload():
    response = Response(mimetype="application/json")

    if "user_file" not in request.files:
        response.status_code = 400
        response.data = json.dumps({"message": "file upload fail",
                                    "exception msg": "No user_file key in request.files"})
        return response

    fileobj = request.files["user_file"]
    savepath = fileobj.filename
    file_url, err = aws.upload_fileobj_to_s3(fileobj=fileobj, savepath=savepath)

    # 파일 업로드 실패 시에 에러 메세지를 담은 리스폰스를 떨궈준다.
    if err:
        print("Exception :%s", err)
        response.status_code = 500
        response.data = json.dumps({"message": "file upload fail",
                                    "exception msg": err})
        return response

    # 정상적으로 파일 업로드 성공 시 파일 url을 담은 리스폰스를 떨궈준다.
    response.status_code = 200
    response.data = json.dumps({"code": response.status_code,
                                "message": "file upload success",
                                "url": file_url})
    return response


# 1. s3로 이미지 파일을 업로드
# 2. 얼굴 검출을 실행
# 3. 얼굴 검출 결과를 리턴
@bp.route("/facedetect/bboxes", methods=["POST"])
def facedetect():
    response = Response(mimetype="application/json")

    if "user_file" not in request.files:
        response.status_code = 400
        response.data = json.dumps({"message": "file upload fail",
                                    "exception msg": "No user_file key in request.files"})
        return response

    file_obj = request.files["user_file"]
    savepath = '{0}/{1}'.format('origin', file_obj.filename)
    file_url, err = aws.upload_fileobj_to_s3(fileobj=file_obj, savepath=savepath)

    # 파일 업로드 실패 시에 에러 메세지를 담은 리스폰스를 떨궈준다.
    if err:
        print("Exception :%s", err)
        response.status_code = 500
        response.data = json.dumps({"message": "file upload fail",
                                    "exception msg": err})
        return response

    bboxes = mtcnn_api.detect(savepath)
    response.status_code = 200
    response.data = json.dumps({
                                "code": response.status_code,
                                "message": "face detection success",
                                "num_faces": str(len(bboxes)),
                                "bboxes": bboxes
                              })
    return response


# 1. s3로 이미지 파일을 업로드
# 2. 얼굴 검출을 실행
# 3. 얼굴 영역을 원본 이미지에 표시하고 s3 상에 업로드
@bp.route("/facedetect/draw", methods=["POST"])
def facedetect_and_draw():
    response = Response(mimetype="application/json")

    if "user_file" not in request.files:
        response.status_code = 400
        response.data = json.dumps({"message": "file upload fail",
                                    "exception msg": "No user_file key in request.files"})
        return response

    file_obj = request.files["user_file"]
    savepath = '{0}/{1}'.format('origin', file_obj.filename)
    file_url, err = aws.upload_fileobj_to_s3(fileobj=file_obj, savepath=savepath)

    # 파일 업로드 실패 시에 에러 메세지를 담은 리스폰스를 떨궈준다.
    if err:
        print("Exception :%s", err)
        response.status_code = 500
        response.data = json.dumps({"message": "file upload fail",
                                    "exception msg": err})
        return response

    facedtected_image = mtcnn_api.detect_and_draw(savepath)

    # 얼굴 영역이 표시된 이미지를 임시 폴더에 저장한다.
    filename = 'detected_{0}'.format(file_obj.filename)
    filepath = os.path.join(util.tmp_dir(), filename)
    facedtected_image.save(filepath)

    savepath = '{0}/{1}'.format("facedetected", filename)

    # s3 상에 임시 이미지 파일을 업로드 한 뒤, 삭제해준다.
    file_url, err = aws.upload_file_to_s3(filepath=filepath, savepath=savepath)
    os.remove(filepath)

    # 파일 업로드 실패 시에 에러 메세지를 담은 리스폰스를 떨궈준다.
    if err:
        print("Exception :%s", err)
        response.status_code = 500
        response.data = json.dumps({"message": "file upload fail",
                                    "exception msg": err})
        return response

    response.status_code = 200
    response.data = json.dumps({
        "code": response.status_code,
        "message": "face detection success",
        "facedetected_image": file_url
    })

    return response

api = Api(bp)
