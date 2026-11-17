import os

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from dao.index import db, init_db
from router.index import auth_bp, traducao_bp, troca_bp

jwt = JWTManager()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("JWT_SECRET_KEY", "pji2-dev-secret-key-1234567890"),
        JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY", "pji2-dev-secret-key-1234567890"),
        SQLALCHEMY_DATABASE_URI=os.getenv("https://jfhotcskugamxktspzlh.supabase.co", "sqlite:///pji2.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    init_db(app)
    jwt.init_app(app)

    with app.app_context():
        from model import Cliente, Item, Produto, Traducao, Troca, Usuario  # noqa: F401

        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(traducao_bp)
    app.register_blueprint(troca_bp)

    @app.get("/")
    def index():
        return jsonify(
            {
                "message": "API PJI2 com SQLAlchemy, JWT e paginação",
                "endpoints": [
                    "/auth/register",
                    "/auth/login",
                    "/traducao",
                    "/troca",
                ],
            }
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
