from io import BytesIO

import flask
import requests
from flask import send_file, Response

import cornhub
from cornhub import pornhub




@cornhub.app.route("/", methods=["GET", "POST"])
def index():
    video_items = pornhub.get_section("video")
    return flask.render_template("index.html", video_items=video_items)


@cornhub.app.route("/recommended")
def recommended():
    video_items = pornhub.get_section("recommended")
    return flask.render_template("index.html", video_items=video_items)


@cornhub.app.route("/video")
def video():
    section_code = flask.request.args.get("o")

    if section_code is None:
        flask.redirect("index")

    video_items = pornhub.get_section(section_code)
    return flask.render_template("index.html", video_items=video_items)


@cornhub.app.route("/view_video.php")
def view_video():
    viewkey = flask.request.args.get("viewkey", type=str)
    video_item = pornhub.get_video(viewkey=viewkey)
    return flask.render_template("video.html", video_item=video_item)


@cornhub.app.route("/search")
def search():
    pass


@cornhub.app.route("/proxy-file/<path:url>")
def proxy_file(url):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        content_type = response.headers["Content-Type"]
        return Response(response.iter_content(chunk_size=10*1024), content_type=content_type)
    except requests.exceptions.RequestException as e:
        return str(e), 404


@cornhub.app.errorhandler(404)
def page_not_found(e):
    return flask.render_template("404.html"), 404
