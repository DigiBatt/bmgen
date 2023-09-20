from flask import Flask, request
from flask_cors import CORS
from bmgen import bmgen
from io import StringIO

app = Flask(
    "bmgen",
    static_url_path="/",
    static_folder="web/client",
)
CORS(app)


@app.route("/api/<target>/<format>/", methods=["POST"])
def generate(target, format):
    f = request.files["program"]
    out = StringIO()
    f.seek(0)
    try:
        bmgen.generate(f, target, format, None, out)
        out.seek(0)
        return out
    except Exception as e:
        return (str(e), 400)
