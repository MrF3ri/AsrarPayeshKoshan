from . import db

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
