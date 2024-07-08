import json
from io import BytesIO, StringIO

from flask import Flask, request, send_file
from flask_cors import CORS

from bmgen import bmgen

app = Flask(
    "bmgen",
    static_url_path="/",
    static_folder="web/client/public",
)
CORS(app)


@app.route("/api/generate/<target>/<format>/", methods=["POST"])
def generate(target, format):
    f = request.files["program"]
    config = None
    if "config" in request.files:
        config = json.load(request.files["config"])
    out = StringIO()
    f.seek(0)
    try:
        bmgen.generate(f, target, format, None, out, config=config)
        out.seek(0)
        return {"program": out.read()}
    except Exception as e:
        return {"error": str(e)}


@app.route("/api/download/<target>/<format>/", methods=["POST"])
def download(target, format):
    f = request.files["program"]
    config = None
    if "config" in request.files:
        config = json.load(request.files["config"])
    out = BytesIO()
    f.seek(0)
    try:
        bmgen.generate(f, target, format, None, out, config=config)
        out.seek(0)
        return send_file(out, mimetype="application/octet-stream")
    except Exception as e:
        return {"error": str(e)}
