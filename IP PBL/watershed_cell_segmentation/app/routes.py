from flask import Blueprint, render_template, request, jsonify, current_app
from pathlib import Path
import uuid, cv2, numpy as np
from .processing import process_image, kernel_experiment

bp = Blueprint("main", __name__)

@bp.get("/")
def home():
    return render_template("index.html")

@bp.get("/processing")
def processing_page():
    return render_template("processing.html")

@bp.get("/segmentation")
def segmentation_page():
    return render_template("segmentation.html")

@bp.get("/analysis")
def analysis_page():
    return render_template("analysis.html")

@bp.get("/about")
def about_page():
    return render_template("about.html")

@bp.post("/api/process")
def api_process():
    if "image" not in request.files:
        return jsonify(error="No image uploaded"), 400
    f = request.files["image"]
    if not f.filename:
        return jsonify(error="No filename supplied"), 400
    ext = Path(f.filename).suffix.lower()
    if ext not in {".jpg",".jpeg",".png",".bmp"}:
        return jsonify(error="Supported formats: JPG, JPEG, PNG, BMP"), 400

    data = np.frombuffer(f.read(), np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        return jsonify(error="Invalid image file"), 400

    params = {
        "noise": request.form.get("noise", "none"),
        "filter": request.form.get("filter", "median"),
        "kernel": int(request.form.get("kernel", 3)),
        "threshold": request.form.get("threshold", "otsu"),
        "morph": request.form.get("morph", "opening"),
    }
    try:
        result = process_image(image, params, current_app.config["UPLOAD_FOLDER"])
        return jsonify(result)
    except Exception as e:
        return jsonify(error=str(e)), 500

@bp.post("/api/kernel-experiment")
def api_kernel_experiment():
    if "image" not in request.files:
        return jsonify(error="No image uploaded"), 400
    data = np.frombuffer(request.files["image"].read(), np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if image is None:
        return jsonify(error="Invalid image"), 400
    try:
        return jsonify(kernel_experiment(image, current_app.config["UPLOAD_FOLDER"]))
    except Exception as e:
        return jsonify(error=str(e)), 500
