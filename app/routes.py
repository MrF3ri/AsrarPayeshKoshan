from flask import Blueprint, jsonify , render_template
from .models import *
from .home import Home
import requests

routeapi = Blueprint("routeapi", __name__)

@routeapi.route("/")
@routeapi.route("/home")
def get_products():
    return Home()

@routeapi.route("/ourteam")
def ourteam():
    response = requests.get("http://localhost:5000/api/team")
    team_members = response.json()
    return render_template("ourteam.html", team_members=team_members , page_id="ourteam")