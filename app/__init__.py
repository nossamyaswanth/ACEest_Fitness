from flask import Flask
from .routes import bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app

# for direct run (optional)
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5050)
