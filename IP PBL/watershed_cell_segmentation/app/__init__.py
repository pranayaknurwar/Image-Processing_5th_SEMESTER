from flask import Flask
from pathlib import Path

def create_app():
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 12 * 1024 * 1024
    app.config["UPLOAD_FOLDER"] = str(Path(app.root_path).parent / "uploads")
    Path(app.config["UPLOAD_FOLDER"]).mkdir(exist_ok=True)
    from .routes import bp
    app.register_blueprint(bp)
    return app
