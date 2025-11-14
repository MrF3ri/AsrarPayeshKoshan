from flask import render_template
from .models import Slider, Banner, Service, News, TeamMember, CompanyBranch, RelatedLink

def Home():
    sliders = Slider.query.filter_by(active=True).order_by(Slider.display_order).all()
    banners = Banner.query.filter_by(active=True).all()
    services = Service.query.filter_by(active=True).all()
    news_list = News.query.filter_by(active=True).order_by(News.published_date.desc()).limit(6).all()
    team = TeamMember.query.filter_by(active=True).order_by(TeamMember.display_order).all()
    branches = CompanyBranch.query.filter_by(active=True).all()
    related_links = RelatedLink.query.filter_by(active=True).all()
    print(sliders[0].image_url)
    print(banners)
    print("=========================")
    return render_template(
        "home.html",
        sliders=sliders,
        banners=banners,
        services=services,
        news_list=news_list,
        team=team,
        branches=branches,
        related_links=related_links    
    )
