from flask import Blueprint, render_template, abort
from .models import (
    AboutCompany,
    CompanyStat,
    PageSEO,
    TeamMember,
    CompanyCertificate,
    News,
    Service
)
from .home import Home
from . import db

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


@routeapi.route("/news")
def news_list():
    news_items = (
        News.query
        .filter_by(active=True)
        .order_by(News.published_date.desc())
        .all()
    )
    return render_template("news_list.html", news_items=news_items, page_id="news")


@routeapi.route("/news/<int:news_id>")
def news_detail(news_id):
    news = News.query.get_or_404(news_id)
    news.views = (news.views or 0) + 1
    db.session.commit()

    latest_news = (
        News.query
        .filter(News.active.is_(True), News.id != news.id)
        .order_by(News.published_date.desc())
        .limit(5)
        .all()
    )

    return render_template("news_detail.html", news=news, latest_news=latest_news, page_id="news")


@routeapi.route("/services")
def services_list():
    services = Service.query.filter_by(active=True).all()
    return render_template("services.html", services=services, page_id="services")


@routeapi.route("/services/<int:service_id>")
def service_detail(service_id):
    service = Service.query.get_or_404(service_id)
    related_services = Service.query.filter(Service.active.is_(True), Service.id != service.id).limit(4).all()
    return render_template("service_detail.html", service=service, related_services=related_services, page_id="services")
