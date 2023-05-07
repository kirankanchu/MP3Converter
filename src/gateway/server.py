import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

import logging
from flask import Flask

server = Flask(__name__)
server.logger.setLevel(logging.DEBUG)

mongo_video = PyMongo(server, uri="mongodb://host.minikube.internal:27017/videos")

mongo_mp3 = PyMongo(server, uri="mongodb://host.minikube.internal:27017/mp3s")

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err


@server.route("/upload", methods=["POST"])
def upload():
    server.logger.info( '34')
    access, err = validate.token(request)
    server.logger.info( '36')
    if err:
        print(err)
        return err
    server.logger.info( '40')
    access = json.loads(access)
    server.logger.info( '42')
    if access["admin"]:
        server.logger.info( '44')
        if len(request.files) > 1 or len(request.files) < 1:
            return "exactly 1 file required", 400
        server.logger.info( '47')
        for _, f in request.files.items():
            server.logger.info( '49')
            err = util.upload(f, fs_videos, channel, access)
            server.logger.info( '51')
            if err:
                server.logger.info( err)
                return err
            server.logger.info( '55')

        return "success!", 200
    else:
        return "not authorized", 401


@server.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    if access["admin"]:
        fid_string = request.args.get("fid")

        if not fid_string:
            return "fid is required", 400

        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=f"{fid_string}.mp3")
        except Exception as err:
            print(err)
            return "internal server error", 500

    return "not authorized", 401


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080, debug=True)
