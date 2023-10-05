from flask import Flask
from .routes import AuthRoutes
from .routes import PublicationsRoutes
from .routes import UserRoutes
from .routes import OrganizationRoutes


app = Flask(__name__)
def init_app(config):
  app.config.from_object(config)

  app.register_blueprint(AuthRoutes.main, url_prefix="/auth")
  app.register_blueprint(PublicationsRoutes.main, url_prefix="/publication")
  app.register_blueprint(UserRoutes.main, url_prefix="/user")
  app.register_blueprint(OrganizationRoutes.main, url_prefix="/org")

  return app