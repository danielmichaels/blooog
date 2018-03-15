from flask import Blueprint
'''
This creates the blueprint for blog
'''
blog = Blueprint('blog', __name__)

from . import routes
