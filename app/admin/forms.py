from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, IntegerField, SelectField, DateTimeField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, URL, NumberRange, Email, EqualTo

# ---------- Login ----------
class LoginForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired()])
    password = PasswordField('رمز عبور', validators=[DataRequired()])

# ---------- News ----------
class NewsForm(FlaskForm):
    title = StringField('عنوان', validators=[DataRequired(), Length(max=255)])
    short_description = TextAreaField('توضیح کوتاه', validators=[Optional()])
    full_description = TextAreaField('متن کامل', validators=[Optional()])
    image = FileField('تصویر', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'فقط تصاویر مجاز هستند!')])
    image_url = StringField('آدرس تصویر (لینک)', validators=[Optional(), URL()])
    attachment_url = StringField('آدرس فایل ضمیمه', validators=[Optional(), URL()])
    published_date = StringField('تاریخ انتشار', validators=[DataRequired()])  # تغییر به StringField
    views = IntegerField('تعداد بازدید', validators=[Optional(), NumberRange(min=0)], default=0)
    active = BooleanField('فعال', default=True)

# ---------- Service ----------
class ServiceForm(FlaskForm):
    title = StringField('عنوان', validators=[DataRequired(), Length(max=255)])
    short_description = TextAreaField('توضیح کوتاه', validators=[Optional()])
    full_description = TextAreaField('توضیحات کامل', validators=[Optional()])
    image = FileField('تصویر', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    image_url = StringField('آدرس تصویر (لینک)', validators=[Optional(), URL()])
    detail_link = StringField('لینک جزئیات', validators=[Optional(), Length(max=255)])
    active = BooleanField('فعال', default=True)

# ---------- Team Member ----------
class TeamMemberForm(FlaskForm):
    name = StringField('نام و نام خانوادگی', validators=[DataRequired(), Length(max=100)])
    position = StringField('سمت', validators=[Optional(), Length(max=100)])
    image = FileField('تصویر', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    image_url = StringField('آدرس تصویر (لینک)', validators=[Optional(), URL()])
    display_order = IntegerField('ترتیب نمایش', validators=[Optional()], default=0)
    active = BooleanField('فعال', default=True)
    email = StringField('ایمیل', validators=[Optional(), Email()])
    phone = StringField('تلفن', validators=[Optional()])
    linkedin = StringField('لینکدین', validators=[Optional(), URL()])

# ---------- Slider ----------
class SliderForm(FlaskForm):
    title = StringField('عنوان', validators=[Optional(), Length(max=255)])
    description = TextAreaField('توضیحات', validators=[Optional()])
    image = FileField('تصویر', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif']), DataRequired()])
    image_url = StringField('آدرس تصویر (لینک)', validators=[Optional(), URL()])
    link = StringField('لینک', validators=[Optional(), URL(), Length(max=255)])
    display_order = IntegerField('ترتیب نمایش', validators=[Optional()], default=0)
    active = BooleanField('فعال', default=True)

# ---------- Banner ----------
class BannerForm(FlaskForm):
    title = StringField('عنوان', validators=[Optional(), Length(max=255)])
    image = FileField('تصویر', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif']), DataRequired()])
    image_url = StringField('آدرس تصویر (لینک)', validators=[Optional(), URL()])
    link = StringField('لینک', validators=[Optional(), URL(), Length(max=255)])
    active = BooleanField('فعال', default=True)

# ---------- Branch ----------
class BranchForm(FlaskForm):
    name = StringField('نام شعبه', validators=[DataRequired(), Length(max=255)])
    address = StringField('آدرس', validators=[Optional(), Length(max=255)])
    phone = StringField('تلفن', validators=[Optional(), Length(max=50)])
    mobile = StringField('موبایل', validators=[Optional(), Length(max=50)])
    fax = StringField('فکس', validators=[Optional(), Length(max=50)])
    logo = FileField('لوگو', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    logo_url = StringField('آدرس لوگو (لینک)', validators=[Optional(), URL()])
    active = BooleanField('فعال', default=True)
    instagram = StringField('اینستاگرام', validators=[Optional(), URL()])
    linkedin = StringField('لینکدین', validators=[Optional(), URL()])
    telegram = StringField('تلگرام', validators=[Optional(), URL()])

# ---------- About Company ----------
class AboutForm(FlaskForm):
    company_name = StringField('نام شرکت', validators=[DataRequired(), Length(max=255)])
    slogan = StringField('شعار', validators=[Optional(), Length(max=255)])
    short_description = TextAreaField('توضیح کوتاه', validators=[Optional()])
    full_description = TextAreaField('توضیحات کامل', validators=[Optional()])
    mission = TextAreaField('ماموریت', validators=[Optional()])
    vision = TextAreaField('چشم‌انداز', validators=[Optional()])
    values = TextAreaField('ارزش‌ها', validators=[Optional()])
    founded_year = IntegerField('سال تاسیس', validators=[Optional()])
    registration_number = StringField('شماره ثبت', validators=[Optional(), Length(max=100)])
    national_id = StringField('شناسه ملی', validators=[Optional(), Length(max=100)])
    logo = FileField('لوگو', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    logo_url = StringField('آدرس لوگو (لینک)', validators=[Optional(), URL()])
    about_image = FileField('تصویر درباره ما', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    about_image_url = StringField('آدرس تصویر (لینک)', validators=[Optional(), URL()])
    active = BooleanField('فعال', default=True)

# ---------- SEO ----------
class SEOForm(FlaskForm):
    meta_title = StringField('عنوان سئو', validators=[Optional(), Length(max=255)])
    meta_description = StringField('توضیحات متا', validators=[Optional(), Length(max=500)])
    meta_keywords = StringField('کلمات کلیدی', validators=[Optional(), Length(max=500)])

# ---------- Company Stat ----------
class StatForm(FlaskForm):
    title = StringField('عنوان', validators=[DataRequired(), Length(max=100)])
    value = StringField('مقدار', validators=[DataRequired(), Length(max=50)])
    icon = StringField('آیکون', validators=[Optional(), Length(max=100)])
    display_order = IntegerField('ترتیب نمایش', default=0)
    active = BooleanField('فعال', default=True)

# ---------- Certificate ----------
class CertificateForm(FlaskForm):
    title = StringField('عنوان', validators=[DataRequired(), Length(max=255)])
    issuer = StringField('صادرکننده', validators=[Optional(), Length(max=255)])
    issue_year = IntegerField('سال صدور', validators=[Optional()])
    image = FileField('تصویر', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'])])
    image_url = StringField('آدرس تصویر (لینک)', validators=[Optional(), URL()])
    description = TextAreaField('توضیحات', validators=[Optional()])
    display_order = IntegerField('ترتیب نمایش', default=0)
    active = BooleanField('فعال', default=True)

# ---------- Admin Create ----------
class AdminCreateForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    full_name = StringField('نام کامل', validators=[Optional(), Length(max=100)])
    password = PasswordField('رمز عبور', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('تکرار رمز عبور', validators=[DataRequired(), EqualTo('password')])

class AdminEditForm(FlaskForm):
    username = StringField('نام کاربری', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    full_name = StringField('نام کامل', validators=[Optional(), Length(max=100)])
    password = PasswordField('رمز عبور جدید (اختیاری)', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('تکرار رمز عبور جدید', validators=[EqualTo('password')])
    is_active = BooleanField('فعال', default=True)

class ProfileForm(FlaskForm):
    full_name = StringField('نام کامل', validators=[Optional(), Length(max=100)])
    email = StringField('ایمیل', validators=[DataRequired(), Email()])
    password = PasswordField('رمز عبور جدید (اختیاری)', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('تکرار رمز عبور جدید', validators=[EqualTo('password')])