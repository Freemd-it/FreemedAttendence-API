#-*- coding:utf-8 -*-
import os
from flask import Blueprint, render_template, request, current_app, Response
from flask_restful import Api
import json
from . import aws, model_api
from . import util

bp = Blueprint("facedetect_api", __name__)


@bp.route("/")
def healthcheck():
    return json.dumps({"message": "server live!"})


@bp.route("/upload")
def render_file():
    return render_template("upload.html")


# s3로 이미지 파일을 업로드하는 API
@bp.route("/fileupload", methods=("GET", "POST"))
def fileupload():
    response = Response(mimetype="application/json")

    if "user_file" not in request.files:
        response.status_code = 400
        response.data = json.dumps({"message": "file upload fail",
                                    "exception msg": "No user_file key in request.files"})
        return response

    file = request.files["user_file"]
    file_url, err = aws.upload_file_to_s3(fileobj=file)

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


# s3로 이미지 파일을 업로드 한 뒤, 얼굴 검출을 실행하고, 결과 이미지를 다시 s3에 업로드하는 API
@bp.route("/facedetect", methods=("GET", "POST"))
def facedetect():
    # 요청을 통해 전달된 이미지를 받아 s3 상에 업로드
    if "user_file" not in request.files:
        return "No user_file key in request.files"
    fileobj = request.files["user_file"]
    aws.upload_file_to_s3(fileobj=fileobj, filedir="origin", filename=fileobj.filename)

    # s3 상에 업로드 된 url을 전달하여 얼굴 검출을 실행한 뒤, 얼굴 영역이 표시된 이미지를 받아온다.
    file_url = "origin/%s" % fileobj.filename
    facedtected_image = model_api.facedetect_from_url(file_url)

    # 얼굴 영역이 표시된 이미지를 임시 폴더에 저장한다.
    filename = util.current_time_str() + ".jpg"
    filepath = os.path.join(util.tmp_dir(), filename)
    facedtected_image.save(filepath)

    # s3 상에 임시 이미지 파일을 업로드 한 뒤, 삭제해준다.
    aws.upload_file_to_s3(filepath=filepath, filedir="facedetected", filename=filename)
    os.remove(filepath)

    # s3 상에 저장된 얼굴 영역이 표시된 이미지 url을 json에 담아서 리턴한다.
    s3_url = os.path.join(aws.get_aws_bucketurl(), "facedetected", filename)
    return render_template("result.html", s3_url=s3_url)

api = Api(bp)
