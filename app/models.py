from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime  # این رو اضافه کنید

class Admin(UserMixin, db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # تغییر این خط
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'
    
    def get_full_name(self):
        return self.full_name or self.username
class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.Text)
    full_description = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    attachment_url = db.Column(db.String(255))  # فایل ضمیمه، ممکنه None باشد
    published_date = db.Column(db.Date, nullable=False)
    views = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.Text)
    full_description = db.Column(db.Text)  # توضیحات کامل برای صفحه جزئیات
    image_url = db.Column(db.String(255))
    detail_link = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class TeamMember(db.Model):
    __tablename__ = "team_members"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))
    image_url = db.Column(db.String(255))
    display_order = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    contacts = db.relationship('TeamContact', backref='member', cascade='all, delete-orphan')

class TeamContact(db.Model):
    __tablename__ = "team_contacts"
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('team_members.id'))
    type = db.Column(db.String(50))  # email, phone, linkedin
    value = db.Column(db.String(255))

class RelatedLink(db.Model):
    __tablename__ = "related_links"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)  # توضیح کوتاه، ممکنه None باشد
    url = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Slider(db.Model):
    __tablename__ = "sliders"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)  # توضیح کوتاه، ممکنه None باشد
    image_url = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255))  # ممکنه None باشد
    display_order = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
class Banner(db.Model):
    __tablename__ = "banners"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    image_url = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class CompanyBranch(db.Model):
    __tablename__ = "company_branches"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    mobile = db.Column(db.String(50))
    fax = db.Column(db.String(50))
    logo_url = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    social_links = db.relationship('CompanySocial', backref='branch', cascade='all, delete-orphan')

class CompanySocial(db.Model):
    __tablename__ = "company_socials"
    id = db.Column(db.Integer, primary_key=True)
    branch_id = db.Column(db.Integer, db.ForeignKey('company_branches.id'))
    type = db.Column(db.String(50))  # instagram, linkedin, twitter, ...
    url = db.Column(db.String(255))

class AboutCompany(db.Model):
    __tablename__ = "about_company"

    id = db.Column(db.Integer, primary_key=True)

    company_name = db.Column(db.String(255), nullable=False)
    slogan = db.Column(db.String(255))

    short_description = db.Column(db.Text)
    full_description = db.Column(db.Text)

    mission = db.Column(db.Text)
    vision = db.Column(db.Text)
    values = db.Column(db.Text)  # لیست ارزش‌ها (متن ساده یا JSON-string)

    founded_year = db.Column(db.Integer)
    registration_number = db.Column(db.String(100))
    national_id = db.Column(db.String(100))

    logo_url = db.Column(db.String(255))
    about_image_url = db.Column(db.String(255))

    active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )

class CompanyStat(db.Model):
    __tablename__ = "company_stats"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # مثال: پروژه‌ها
    value = db.Column(db.String(50), nullable=False)  # مثال: +120
    icon = db.Column(db.String(100))  # optional (css class / icon name)

    display_order = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)

class CompanyCertificate(db.Model):
    __tablename__ = "company_certificates"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)
    issuer = db.Column(db.String(255))
    issue_year = db.Column(db.Integer)

    image_url = db.Column(db.String(255))
    description = db.Column(db.Text)

    display_order = db.Column(db.Integer, default=0)
    active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class PageSEO(db.Model):
    __tablename__ = "page_seo"

    id = db.Column(db.Integer, primary_key=True)
    page_key = db.Column(db.String(50), unique=True)  # مقدار: "about"

    meta_title = db.Column(db.String(255))
    meta_description = db.Column(db.String(500))
    meta_keywords = db.Column(db.String(500))