from flask import Blueprint, render_template
from .models import (
    AboutCompany,
    CompanyStat,
    PageSEO,
    TeamMember,
    CompanyCertificate
)
from .home import Home

routeapi = Blueprint("routeapi", __name__)

# -----------------------
# HOME
# -----------------------
@routeapi.route("/")
@routeapi.route("/home")
def home():
    return Home()

# -----------------------
# OUR TEAM
# -----------------------
@routeapi.route("/ourteam")
def ourteam():
    team_members = (
        TeamMember.query
        .filter_by(active=True)
        .order_by(TeamMember.display_order)
        .all()
    )

    return render_template(
        "ourteam.html",
        team_members=team_members,
        page_id="ourteam"
    )

# -----------------------
# ABOUT
# -----------------------
@routeapi.route("/about")
def about():
    about = AboutCompany.query.filter_by(active=True).first()

    stats = (
        CompanyStat.query
        .filter_by(active=True)
        .order_by(CompanyStat.display_order)
        .all()
    )
    companyCertificate = CompanyCertificate.query.filter_by(active=True).all()
    seo = PageSEO.query.filter_by(page_key="about").first()

    return render_template(
        "about.html",
        about=about,
        stats=stats,
        seo=seo,
        page_id="about",
        companyCertificate=companyCertificate
    )
