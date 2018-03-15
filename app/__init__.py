# ---- IMPORTS ----#
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_misaka import Misaka
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_simplemde import SimpleMDE
import flask_whooshalchemy as wa
from flask_moment import Moment

# ----- INSTANTIATIONS -----#

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
toolbar = DebugToolbarExtension()
login_manager = LoginManager()
login_manager.login_view = 'blog.login'
simplemde = SimpleMDE()
moment = Moment()
csrf = CSRFProtect()


# ----- INSTANTIATIONS -----#


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config['default'])
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # app.config['SQLALCHEMY_ECHO'] = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SIMPLEMDE_USE_CDN'] = True
    app.config['SIMPLEMDE_JS_IIFE'] = True

    # ------ APPLICATION FACTORY ----- #

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    toolbar.init_app(app)
    login_manager.init_app(app)
    simplemde.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    Misaka(app, fenced_code=True, strikethrough=True, tables=True,
           highlight=True, autolink=True, no_intra_emphasis=True,
           underline=True, smartypants=True, qoute=True)

    from app.models import Entries  # import local for whoosh index
    wa.whoosh_index(app, Entries)

    # ------- BLUEPRINTS --------------#
    from .blog import blog as blog
    app.register_blueprint(blog)
    ''' Blueprint was required after making the application factory.
    As the app instance is created and configured at run time and thus the 'app'
    has already created, you cannot access the 'app' after this. I.e. the app in app.route
    is inaccessible: blueprints mitigate this.
    '''

    return app
