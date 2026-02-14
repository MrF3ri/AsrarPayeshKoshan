import os
from datetime import date, datetime
from functools import wraps

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from . import db
from .home import Home
from .models import (
    AboutCompany,
    Banner,
    CompanyBranch,
    CompanyCertificate,
    CompanyStat,
    ContactMessage,
    News,
    PageSEO,
    RelatedLink,
    Service,
    Slider,
    TeamMember,
)

routeapi = Blueprint("routeapi", __name__)

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")


def _to_bool(value):
    return str(value).lower() in {"1", "true", "on", "yes"}


def _to_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_date(value):
    if not value:
        return date.today()
    return datetime.strptime(value, "%Y-%m-%d").date()


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if not session.get("is_admin"):
            flash("برای دسترسی به پنل باید وارد شوید.", "warning")
            return redirect(url_for("routeapi.admin_login"))
        return view_func(*args, **kwargs)

    return wrapper


# -----------------------
# PUBLIC PAGES
# -----------------------
@routeapi.route("/")
@routeapi.route("/home")
def home():
    return Home()


@routeapi.route("/ourteam")
def ourteam():
    team_members = (
        TeamMember.query.filter_by(active=True).order_by(TeamMember.display_order).all()
    )

    return render_template(
        "ourteam.html",
        team_members=team_members,
        page_id="ourteam",
    )


@routeapi.route("/about")
def about():
    about_item = AboutCompany.query.filter_by(active=True).first()

    stats = CompanyStat.query.filter_by(active=True).order_by(CompanyStat.display_order).all()
    company_certificate = CompanyCertificate.query.filter_by(active=True).order_by(
        CompanyCertificate.display_order
    ).all()
    seo = PageSEO.query.filter_by(page_key="about").first()

    return render_template(
        "about.html",
        about=about_item,
        stats=stats,
        seo=seo,
        page_id="about",
        companyCertificate=company_certificate,
    )


@routeapi.route("/news/<int:news_id>")
def news_detail(news_id):
    item = News.query.get_or_404(news_id)
    item.views = (item.views or 0) + 1
    db.session.commit()
    latest_news = (
        News.query.filter(News.id != item.id, News.active.is_(True))
        .order_by(News.published_date.desc())
        .limit(5)
        .all()
    )
    return render_template(
        "news_detail.html",
        news=item,
        latest_news=latest_news,
        page_id="news-detail",
    )


@routeapi.route("/services/<int:service_id>")
def service_detail(service_id):
    item = Service.query.get_or_404(service_id)
    related_services = (
        Service.query.filter(Service.id != item.id, Service.active.is_(True)).limit(6).all()
    )
    return render_template(
        "service_detail.html",
        service=item,
        related_services=related_services,
        page_id="service-detail",
    )


@routeapi.route("/contact", methods=["GET", "POST"])
def contact():
    branches = CompanyBranch.query.filter_by(active=True).all()

    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if not full_name or not email or not message:
            flash("نام، ایمیل و پیام اجباری هستند.", "danger")
        else:
            db.session.add(
                ContactMessage(
                    full_name=full_name,
                    email=email,
                    phone=phone,
                    subject=subject,
                    message=message,
                )
            )
            db.session.commit()
            flash("پیام شما با موفقیت ثبت شد.", "success")
            return redirect(url_for("routeapi.contact"))

    return render_template("contact.html", branches=branches, page_id="contact")


# -----------------------
# ADMIN CMS (single admin)
# -----------------------
@routeapi.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("is_admin"):
        return redirect(url_for("routeapi.admin_dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["is_admin"] = True
            flash("ورود با موفقیت انجام شد.", "success")
            return redirect(url_for("routeapi.admin_dashboard"))
        flash("نام کاربری یا رمز عبور اشتباه است.", "danger")

    return render_template("admin/login.html", page_id="admin-login")


@routeapi.route("/admin/logout")
@admin_required
def admin_logout():
    session.clear()
    flash("با موفقیت خارج شدید.", "info")
    return redirect(url_for("routeapi.admin_login"))


@routeapi.route("/admin")
@admin_required
def admin_dashboard():
    return render_template(
        "admin/dashboard.html",
        page_id="admin-dashboard",
        news_items=News.query.order_by(News.id.desc()).all(),
        service_items=Service.query.order_by(Service.id.desc()).all(),
        slider_items=Slider.query.order_by(Slider.display_order.asc()).all(),
        banner_items=Banner.query.order_by(Banner.id.desc()).all(),
        team_items=TeamMember.query.order_by(TeamMember.display_order.asc()).all(),
        link_items=RelatedLink.query.order_by(RelatedLink.id.desc()).all(),
        branch_items=CompanyBranch.query.order_by(CompanyBranch.id.desc()).all(),
        stat_items=CompanyStat.query.order_by(CompanyStat.display_order.asc()).all(),
        cert_items=CompanyCertificate.query.order_by(CompanyCertificate.display_order.asc()).all(),
        about_item=AboutCompany.query.first(),
        contact_messages=ContactMessage.query.order_by(ContactMessage.id.desc()).all(),
    )


@routeapi.route("/admin/news/save", methods=["POST"])
@admin_required
def admin_news_save():
    item_id = request.form.get("id")
    item = News.query.get(item_id) if item_id else News()
    item.title = request.form.get("title", "").strip()
    item.short_description = request.form.get("short_description", "").strip()
    item.full_description = request.form.get("full_description", "").strip()
    item.image_url = request.form.get("image_url", "").strip()
    item.attachment_url = request.form.get("attachment_url", "").strip() or None
    item.published_date = _to_date(request.form.get("published_date"))
    item.active = _to_bool(request.form.get("active"))
    if not item_id:
        db.session.add(item)
    db.session.commit()
    flash("خبر ذخیره شد.", "success")
    return redirect(url_for("routeapi.admin_dashboard"))


@routeapi.route("/admin/news/delete/<int:item_id>", methods=["POST"])
@admin_required
def admin_news_delete(item_id):
    db.session.delete(News.query.get_or_404(item_id))
    db.session.commit()
    flash("خبر حذف شد.", "info")
    return redirect(url_for("routeapi.admin_dashboard"))


@routeapi.route("/admin/services/save", methods=["POST"])
@admin_required
def admin_services_save():
    item_id = request.form.get("id")
    item = Service.query.get(item_id) if item_id else Service()
    item.title = request.form.get("title", "").strip()
    item.short_description = request.form.get("short_description", "").strip()
    item.full_description = request.form.get("full_description", "").strip()
    item.image_url = request.form.get("image_url", "").strip()
    item.detail_link = request.form.get("detail_link", "").strip() or None
    item.active = _to_bool(request.form.get("active"))
    if not item_id:
        db.session.add(item)
    db.session.commit()
    flash("خدمت ذخیره شد.", "success")
    return redirect(url_for("routeapi.admin_dashboard"))


@routeapi.route("/admin/services/delete/<int:item_id>", methods=["POST"])
@admin_required
def admin_services_delete(item_id):
    db.session.delete(Service.query.get_or_404(item_id))
    db.session.commit()
    flash("خدمت حذف شد.", "info")
    return redirect(url_for("routeapi.admin_dashboard"))


@routeapi.route("/admin/about/save", methods=["POST"])
@admin_required
def admin_about_save():
    item = AboutCompany.query.first() or AboutCompany(company_name="")
    item.company_name = request.form.get("company_name", "").strip()
    item.slogan = request.form.get("slogan", "").strip()
    item.short_description = request.form.get("short_description", "").strip()
    item.full_description = request.form.get("full_description", "").strip()
    item.mission = request.form.get("mission", "").strip()
    item.vision = request.form.get("vision", "").strip()
    item.values = request.form.get("values", "").strip()
    item.founded_year = _to_int(request.form.get("founded_year"), None)
    item.registration_number = request.form.get("registration_number", "").strip()
    item.national_id = request.form.get("national_id", "").strip()
    item.logo_url = request.form.get("logo_url", "").strip()
    item.about_image_url = request.form.get("about_image_url", "").strip()
    item.active = _to_bool(request.form.get("active"))
    if not item.id:
        db.session.add(item)
    db.session.commit()
    flash("اطلاعات درباره ما ذخیره شد.", "success")
    return redirect(url_for("routeapi.admin_dashboard"))


@routeapi.route("/admin/simple/<string:section>/save", methods=["POST"])
@admin_required
def admin_simple_save(section):
    section_map = {
        "sliders": (Slider, ["title", "description", "image_url", "link", "display_order"]),
        "banners": (Banner, ["title", "image_url", "link"]),
        "team": (TeamMember, ["name", "position", "image_url", "display_order"]),
        "links": (RelatedLink, ["title", "description", "url", "image_url"]),
        "branches": (CompanyBranch, ["name", "address", "phone", "mobile", "fax", "logo_url"]),
        "stats": (CompanyStat, ["title", "value", "icon", "display_order"]),
        "certs": (CompanyCertificate, ["title", "issuer", "issue_year", "image_url", "description", "display_order"]),
    }
    if section not in section_map:
        flash("بخش نامعتبر است.", "danger")
        return redirect(url_for("routeapi.admin_dashboard"))

    model, fields = section_map[section]
    item_id = request.form.get("id")
    item = model.query.get(item_id) if item_id else model()

    for field in fields:
        value = request.form.get(field, "").strip()
        if field in {"display_order", "issue_year"}:
            value = _to_int(value)
        setattr(item, field, value)

    if hasattr(item, "active"):
        item.active = _to_bool(request.form.get("active"))

    if not item_id:
        db.session.add(item)

    db.session.commit()
    flash("اطلاعات ذخیره شد.", "success")
    return redirect(url_for("routeapi.admin_dashboard"))


@routeapi.route("/admin/simple/<string:section>/delete/<int:item_id>", methods=["POST"])
@admin_required
def admin_simple_delete(section, item_id):
    section_map = {
        "sliders": Slider,
        "banners": Banner,
        "team": TeamMember,
        "links": RelatedLink,
        "branches": CompanyBranch,
        "stats": CompanyStat,
        "certs": CompanyCertificate,
        "messages": ContactMessage,
    }
    model = section_map.get(section)
    if not model:
        flash("بخش نامعتبر است.", "danger")
        return redirect(url_for("routeapi.admin_dashboard"))

    db.session.delete(model.query.get_or_404(item_id))
    db.session.commit()
    flash("رکورد حذف شد.", "info")
    return redirect(url_for("routeapi.admin_dashboard"))
