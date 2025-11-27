from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    # Lazy import to avoid circular import
    from app.models import BlackListedToken

    jti = jwt_payload["jti"]
    return BlackListedToken.query.filter_by(jti=jti).first() is not None