from flask import Blueprint, jsonify , render_template
from .models import *
from .home import Home

routeapi = Blueprint("routeapi", __name__)

@routeapi.route("/")
@routeapi.route("/home")
def get_products():
    return Home()
