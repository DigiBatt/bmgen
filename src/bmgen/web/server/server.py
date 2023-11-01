from flask import Flask, request, send_file
from flask_cors import CORS
from bmgen import bmgen
from io import StringIO
import json

app = Flask(
    "bmgen",
    static_url_path="/",
    static_folder="web/client/public",
)
CORS(app)


@app.route("/api/<target>/<format>/", methods=["POST"])
def generate(target, format):
    f = request.files["program"]
    config = None
    if "config" in request.files:
        config = json.load(request.files["config"])
        print(config)
    out = StringIO()
    f.seek(0)
    try:
        bmgen.generate(f, target, format, None, out, config=config)
        out.seek(0)
        return {"program": out.read()}
    except Exception as e:
        return {"error": str(e)}
