from flask import Blueprint, jsonify
from .models import Slider, Banner, News, Service, TeamMember, RelatedLink, CompanyBranch
from . import db

public = Blueprint("public", __name__)

# -----------------------
# SLIDERS
# -----------------------
@public.get("/sliders")
def get_sliders():
    sliders = Slider.query.filter_by(active=True).order_by(Slider.display_order).all()
    return jsonify([
        {
            "id": s.id,
            "title": s.title,
            "image_url": s.image_url,
            "link": s.link
        }
        for s in sliders
    ])


# -----------------------
# BANNERS
# -----------------------
@public.get("/banners")
def get_banners():
    banners = Banner.query.filter_by(active=True).all()
    return jsonify([
        {
            "id": b.id,
            "title": b.title,
            "image_url": b.image_url,
            "link": b.link
        }
        for b in banners
    ])


# -----------------------
# NEWS
# -----------------------
@public.get("/news")
def get_news():
    news = News.query.filter_by(active=True).order_by(News.published_date.desc()).all()
    return jsonify([
        {
            "id": n.id,
            "title": n.title,
            "short_description": n.short_description,
            "image_url": n.image_url,
            "attachment_url": n.attachment_url,
            "published_date": n.published_date.isoformat(),
            "views": n.views
        }
        for n in news
    ])


# -----------------------
# SERVICES
# -----------------------
@public.get("/services")
def get_services():
    services = Service.query.filter_by(active=True).all()
    return jsonify([
        {
            "id": s.id,
            "title": s.title,
            "short_description": s.short_description,
            "image_url": s.image_url,
            "detail_link": s.detail_link
        }
        for s in services
    ])


# -----------------------
# TEAM MEMBERS + CONTACTS
# -----------------------
@public.get("/team")
def get_team():
    team = TeamMember.query.filter_by(active=True).order_by(TeamMember.display_order).all()
    return jsonify([
        {
            "id": t.id,
            "name": t.name,
            "position": t.position,
            "image_url": t.image_url,
            "contacts": [
                {
                    "type": c.type,
                    "value": c.value
                }
                for c in t.contacts
            ]
        }
        for t in team
    ])


# -----------------------
# RELATED LINKS
# -----------------------
@public.get("/related-links")
def get_related_links():
    links = RelatedLink.query.filter_by(active=True).all()
    return jsonify([
        {
            "id": l.id,
            "title": l.title,
            "description": l.description,
            "url": l.url,
            "image_url": l.image_url
        }
        for l in links
    ])


# -----------------------
# COMPANY BRANCHES + SOCIALS
# -----------------------
@public.get("/branches")
def get_branches():
    branches = CompanyBranch.query.filter_by(active=True).all()
    return jsonify([
        {
            "id": b.id,
            "name": b.name,
            "address": b.address,
            "phone": b.phone,
            "mobile": b.mobile,
            "fax": b.fax,
            "logo_url": b.logo_url,
            "social_links": [
                {
                    "type": s.type,
                    "url": s.url
                }
                for s in b.social_links
            ]
        }
        for b in branches
    ])
