import json
import os
from io import BytesIO, StringIO

import click
from flask import Flask, request, send_file, send_from_directory
from flask_cors import CORS

from bmgen import bmgen, get_version
from bmgen.util.import_jsonld import import_jsonld

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


@app.route("/api/import/<format>/", methods=["POST"])
def importProgram(format):
    if format.lower() != "jsonld":
        return {"error": "unknown format"}
    f = request.files["program"]
    j = json.load(f)
    # config = None
    # if "config" in request.files:
    #     config = json.load(request.files["config"])
    try:
        program = import_jsonld(j)
        return program.toText()
    except Exception as e:
        return {"error": str(e)}


@app.route("/api/examples", methods=["GET"])
def list_examples():
    examples = os.listdir("examples")
    examples.sort()
    return examples


@app.route("/api/version", methods=["GET"])
def version():
    return get_version()


@click.command("bmgen-server")
@click.option("--host", default=None)
@click.option("--port", type=int, default=5000)
def run(host, port):
    app.run(host, port)


if __name__ == "__main__":
    run()
