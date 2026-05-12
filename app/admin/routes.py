import os
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime

from . import admin_bp
from .decorators import admin_required
from .forms import *
from .. import db
from ..models import *

# ============================================
# احراز هویت (Login/Logout)
# ============================================

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            flash('به پنل مدیریت خوش آمدید!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            flash('نام کاربری یا رمز عبور اشتباه است.', 'danger')
    
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('شما از سیستم خارج شدید.', 'info')
    return redirect(url_for('admin.login'))

# ============================================
# داشبورد اصلی
# ============================================

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    # آمار کلی
    total_news = News.query.count()
    total_services = Service.query.count()
    total_team = TeamMember.query.count()
    total_sliders = Slider.query.count()
    total_banners = Banner.query.count()
    total_branches = CompanyBranch.query.count()
    
    # آخرین اخبار
    recent_news = News.query.order_by(News.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_news=total_news,
                         total_services=total_services,
                         total_team=total_team,
                         total_sliders=total_sliders,
                         total_banners=total_banners,
                         total_branches=total_branches,
                         recent_news=recent_news)

# ============================================
# مدیریت اخبار (News)
# ============================================

def save_file(file, folder='images'):
    """ذخیره فایل آپلود شده"""
    if file and file.filename:
        filename = secure_filename(file.filename)
        # افزودن timestamp به نام فایل برای یکتا شدن
        name, ext = os.path.splitext(filename)
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{name}{ext}"
        
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', folder)
        os.makedirs(upload_folder, exist_ok=True)
        
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # برگرداندن مسیر نسبی
        return f'/uploads/{folder}/{filename}'
    return None

@admin_bp.route('/news')
@login_required
@admin_required
def news_index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = News.query.order_by(News.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    news_list = pagination.items
    
    return render_template('admin/news/index.html', 
                         news_list=news_list, 
                         pagination=pagination)


@admin_bp.route('/news/create', methods=['GET', 'POST'])
@login_required
@admin_required
def news_create():
    form = NewsForm()
    
    if form.validate_on_submit():
        # ذخیره تصویر
        image_path = None
        if form.image.data:
            image_path = save_file(form.image.data, 'news')
        elif form.image_url.data:
            image_path = form.image_url.data
        
        # تبدیل تاریخ از رشته به شیء datetime
        published_date_str = form.published_date.data
        try:
            # فرمت input datetime-local: 'YYYY-MM-DDThh:mm'
            published_date = datetime.strptime(published_date_str, '%Y-%m-%dT%H:%M')
        except (ValueError, TypeError):
            try:
                # اگر فرمت دیگری بود امتحان کن
                published_date = datetime.strptime(published_date_str, '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                # در غیر این صورت از زمان حال استفاده کن
                published_date = datetime.now()
        
        news = News(
            title=form.title.data,
            short_description=form.short_description.data,
            full_description=form.full_description.data,
            image_url=image_path,
            attachment_url=form.attachment_url.data,
            published_date=published_date,  # حالا از نوع datetime است
            views=form.views.data,
            active=form.active.data
        )
        
        db.session.add(news)
        db.session.commit()
        
        flash('خبر با موفقیت اضافه شد.', 'success')
        return redirect(url_for('admin.news_index'))
    else:
        # نمایش خطاهای فرم به کاربر
        for field, errors in form.errors.items():
            field_label = getattr(form, field).label.text
            for error in errors:
                flash(f'خطا در فیلد "{field_label}": {error}', 'danger')
    
    return render_template('admin/news/create.html', form=form)

@admin_bp.route('/news/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def news_edit(id):
    news = News.query.get_or_404(id)
    form = NewsForm(obj=news)
    
    if form.validate_on_submit():
        # بروزرسانی تصویر اگر جدید آپلود شده
        if form.image.data:
            image_path = save_file(form.image.data, 'news')
            news.image_url = image_path
        elif form.image_url.data:
            news.image_url = form.image_url.data
        
        news.title = form.title.data
        news.short_description = form.short_description.data
        news.full_description = form.full_description.data
        news.attachment_url = form.attachment_url.data
        try:
            news.published_date = datetime.strptime(form.published_date.data, '%Y-%m-%dT%H:%M')
        except (ValueError, TypeError):
            try:
                news.published_date = datetime.strptime(form.published_date.data, '%Y-%m-%d %H:%M:%S')
            except (ValueError, TypeError):
                news.published_date = datetime.now()
        news.views = form.views.data
        news.active = form.active.data
        
        db.session.commit()
        
        flash('خبر با موفقیت ویرایش شد.', 'success')
        return redirect(url_for('admin.news_index'))
    
    return render_template('admin/news/edit.html', form=form, news=news)

@admin_bp.route('/news/delete/<int:id>')
@login_required
@admin_required
def news_delete(id):
    news = News.query.get_or_404(id)
    db.session.delete(news)
    db.session.commit()
    
    flash('خبر با موفقیت حذف شد.', 'success')
    return redirect(url_for('admin.news_index'))

@admin_bp.route('/news/toggle/<int:id>')
@login_required
@admin_required
def news_toggle(id):
    news = News.query.get_or_404(id)
    news.active = not news.active
    db.session.commit()
    
    status = "فعال" if news.active else "غیرفعال"
    flash(f'خبر با موفقیت {status} شد.', 'success')
    return redirect(url_for('admin.news_index'))

# ============================================
# مدیریت خدمات (Services)
# ============================================

@admin_bp.route('/services')
@login_required
@admin_required
def services_index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = Service.query.order_by(Service.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    services_list = pagination.items
    
    return render_template('admin/services/index.html', 
                         services_list=services_list, 
                         pagination=pagination)

@admin_bp.route('/services/create', methods=['GET', 'POST'])
@login_required
@admin_required
def services_create():
    form = ServiceForm()
    
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            image_path = save_file(form.image.data, 'services')
        elif form.image_url.data:
            image_path = form.image_url.data
        
        service = Service(
            title=form.title.data,
            short_description=form.short_description.data,
            full_description=form.full_description.data,
            image_url=image_path,
            detail_link=form.detail_link.data,
            active=form.active.data
        )
        
        db.session.add(service)
        db.session.commit()
        
        flash('خدمت با موفقیت اضافه شد.', 'success')
        return redirect(url_for('admin.services_index'))
    
    return render_template('admin/services/create.html', form=form)

@admin_bp.route('/services/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def services_edit(id):
    service = Service.query.get_or_404(id)
    form = ServiceForm(obj=service)
    
    if form.validate_on_submit():
        if form.image.data:
            image_path = save_file(form.image.data, 'services')
            service.image_url = image_path
        elif form.image_url.data:
            service.image_url = form.image_url.data
        
        service.title = form.title.data
        service.short_description = form.short_description.data
        service.full_description = form.full_description.data
        service.detail_link = form.detail_link.data
        service.active = form.active.data
        
        db.session.commit()
        
        flash('خدمت با موفقیت ویرایش شد.', 'success')
        return redirect(url_for('admin.services_index'))
    
    return render_template('admin/services/edit.html', form=form, service=service)

@admin_bp.route('/services/delete/<int:id>')
@login_required
@admin_required
def services_delete(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    
    flash('خدمت با موفقیت حذف شد.', 'success')
    return redirect(url_for('admin.services_index'))

@admin_bp.route('/services/toggle/<int:id>')
@login_required
@admin_required
def services_toggle(id):
    service = Service.query.get_or_404(id)
    service.active = not service.active
    db.session.commit()
    
    status = "فعال" if service.active else "غیرفعال"
    flash(f'خدمت با موفقیت {status} شد.', 'success')
    return redirect(url_for('admin.services_index'))

# ============================================
# مدیریت تیم (Team Members)
# ============================================

@admin_bp.route('/team')
@login_required
@admin_required
def team_index():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = TeamMember.query.order_by(TeamMember.display_order).paginate(
        page=page, per_page=per_page, error_out=False
    )
    team_list = pagination.items
    
    return render_template('admin/team/index.html', 
                         team_list=team_list, 
                         pagination=pagination)

@admin_bp.route('/team/create', methods=['GET', 'POST'])
@login_required
@admin_required
def team_create():
    form = TeamMemberForm()
    
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            image_path = save_file(form.image.data, 'team')
        elif form.image_url.data:
            image_path = form.image_url.data
        
        member = TeamMember(
            name=form.name.data,
            position=form.position.data,
            image_url=image_path,
            display_order=form.display_order.data,
            active=form.active.data
        )
        
        db.session.add(member)
        db.session.flush()  # برای گرفتن ID
        
        # اضافه کردن اطلاعات تماس
        if form.email.data:
            contact = TeamContact(member_id=member.id, type="email", value=form.email.data)
            db.session.add(contact)
        
        if form.phone.data:
            contact = TeamContact(member_id=member.id, type="phone", value=form.phone.data)
            db.session.add(contact)
        
        if form.linkedin.data:
            contact = TeamContact(member_id=member.id, type="linkedin", value=form.linkedin.data)
            db.session.add(contact)
        
        db.session.commit()
        
        flash('عضو تیم با موفقیت اضافه شد.', 'success')
        return redirect(url_for('admin.team_index'))
    
    return render_template('admin/team/create.html', form=form)

@admin_bp.route('/team/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def team_edit(id):
    member = TeamMember.query.get_or_404(id)
    form = TeamMemberForm(obj=member)
    
    # پر کردن فرم با اطلاعات تماس موجود
    if request.method == 'GET':
        for contact in member.contacts:
            if contact.type == 'email':
                form.email.data = contact.value
            elif contact.type == 'phone':
                form.phone.data = contact.value
            elif contact.type == 'linkedin':
                form.linkedin.data = contact.value
    
    if form.validate_on_submit():
        if form.image.data:
            image_path = save_file(form.image.data, 'team')
            member.image_url = image_path
        elif form.image_url.data:
            member.image_url = form.image_url.data
        
        member.name = form.name.data
        member.position = form.position.data
        member.display_order = form.display_order.data
        member.active = form.active.data
        
        # بروزرسانی اطلاعات تماس
        # حذف تماس‌های قبلی
        for contact in member.contacts:
            db.session.delete(contact)
        
        # اضافه کردن تماس‌های جدید
        if form.email.data:
            contact = TeamContact(member_id=member.id, type="email", value=form.email.data)
            db.session.add(contact)
        
        if form.phone.data:
            contact = TeamContact(member_id=member.id, type="phone", value=form.phone.data)
            db.session.add(contact)
        
        if form.linkedin.data:
            contact = TeamContact(member_id=member.id, type="linkedin", value=form.linkedin.data)
            db.session.add(contact)
        
        db.session.commit()
        
        flash('عضو تیم با موفقیت ویرایش شد.', 'success')
        return redirect(url_for('admin.team_index'))
    
    return render_template('admin/team/edit.html', form=form, member=member)

@admin_bp.route('/team/delete/<int:id>')
@login_required
@admin_required
def team_delete(id):
    member = TeamMember.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    
    flash('عضو تیم با موفقیت حذف شد.', 'success')
    return redirect(url_for('admin.team_index'))

# ============================================
# مدیریت اسلایدرها (Sliders)
# ============================================

@admin_bp.route('/sliders')
@login_required
@admin_required
def sliders_index():
    sliders = Slider.query.order_by(Slider.display_order).all()
    return render_template('admin/sliders/index.html', sliders=sliders)

@admin_bp.route('/sliders/create', methods=['GET', 'POST'])
@login_required
@admin_required
def sliders_create():
    form = SliderForm()
    
    if form.validate_on_submit():
        image_path = save_file(form.image.data, 'sliders') if form.image.data else form.image_url.data
        
        slider = Slider(
            title=form.title.data,
            description=form.description.data,
            image_url=image_path,
            link=form.link.data,
            display_order=form.display_order.data,
            active=form.active.data
        )
        
        db.session.add(slider)
        db.session.commit()
        
        flash('اسلایدر با موفقیت اضافه شد.', 'success')
        return redirect(url_for('admin.sliders_index'))
    
    return render_template('admin/sliders/create.html', form=form)

@admin_bp.route('/sliders/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def sliders_edit(id):
    slider = Slider.query.get_or_404(id)
    form = SliderForm(obj=slider)
    
    if form.validate_on_submit():
        if form.image.data:
            image_path = save_file(form.image.data, 'sliders')
            slider.image_url = image_path
        elif form.image_url.data:
            slider.image_url = form.image_url.data
        
        slider.title = form.title.data
        slider.description = form.description.data
        slider.link = form.link.data
        slider.display_order = form.display_order.data
        slider.active = form.active.data
        
        db.session.commit()
        
        flash('اسلایدر با موفقیت ویرایش شد.', 'success')
        return redirect(url_for('admin.sliders_index'))
    
    return render_template('admin/sliders/edit.html', form=form, slider=slider)

@admin_bp.route('/sliders/delete/<int:id>')
@login_required
@admin_required
def sliders_delete(id):
    slider = Slider.query.get_or_404(id)
    db.session.delete(slider)
    db.session.commit()
    
    flash('اسلایدر با موفقیت حذف شد.', 'success')
    return redirect(url_for('admin.sliders_index'))

# ============================================
# مدیریت بنرها (Banners)
# ============================================

@admin_bp.route('/banners')
@login_required
@admin_required
def banners_index():
    banners = Banner.query.all()
    return render_template('admin/banners/index.html', banners=banners)

@admin_bp.route('/banners/create', methods=['GET', 'POST'])
@login_required
@admin_required
def banners_create():
    form = BannerForm()
    
    if form.validate_on_submit():
        image_path = save_file(form.image.data, 'banners') if form.image.data else form.image_url.data
        
        banner = Banner(
            title=form.title.data,
            image_url=image_path,
            link=form.link.data,
            active=form.active.data
        )
        
        db.session.add(banner)
        db.session.commit()
        
        flash('بنر با موفقیت اضافه شد.', 'success')
        return redirect(url_for('admin.banners_index'))
    
    return render_template('admin/banners/create.html', form=form)

@admin_bp.route('/banners/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def banners_edit(id):
    banner = Banner.query.get_or_404(id)
    form = BannerForm(obj=banner)
    
    if form.validate_on_submit():
        if form.image.data:
            image_path = save_file(form.image.data, 'banners')
            banner.image_url = image_path
        elif form.image_url.data:
            banner.image_url = form.image_url.data
        
        banner.title = form.title.data
        banner.link = form.link.data
        banner.active = form.active.data
        
        db.session.commit()
        
        flash('بنر با موفقیت ویرایش شد.', 'success')
        return redirect(url_for('admin.banners_index'))
    
    return render_template('admin/banners/edit.html', form=form, banner=banner)

@admin_bp.route('/banners/delete/<int:id>')
@login_required
@admin_required
def banners_delete(id):
    banner = Banner.query.get_or_404(id)
    db.session.delete(banner)
    db.session.commit()
    
    flash('بنر با موفقیت حذف شد.', 'success')
    return redirect(url_for('admin.banners_index'))

# ============================================
# مدیریت شعبات (Branches)
# ============================================

@admin_bp.route('/branches')
@login_required
@admin_required
def branches_index():
    branches = CompanyBranch.query.all()
    return render_template('admin/branches/index.html', branches=branches)

@admin_bp.route('/branches/create', methods=['GET', 'POST'])
@login_required
@admin_required
def branches_create():
    form = BranchForm()
    
    if form.validate_on_submit():
        logo_path = save_file(form.logo.data, 'logos') if form.logo.data else form.logo_url.data
        
        branch = CompanyBranch(
            name=form.name.data,
            address=form.address.data,
            phone=form.phone.data,
            mobile=form.mobile.data,
            fax=form.fax.data,
            logo_url=logo_path,
            active=form.active.data
        )
        
        db.session.add(branch)
        db.session.flush()
        
        # اضافه کردن شبکه‌های اجتماعی
        if form.instagram.data:
            social = CompanySocial(branch_id=branch.id, type="instagram", url=form.instagram.data)
            db.session.add(social)
        if form.linkedin.data:
            social = CompanySocial(branch_id=branch.id, type="linkedin", url=form.linkedin.data)
            db.session.add(social)
        if form.telegram.data:
            social = CompanySocial(branch_id=branch.id, type="telegram", url=form.telegram.data)
            db.session.add(social)
        
        db.session.commit()
        
        flash('شعبه با موفقیت اضافه شد.', 'success')
        return redirect(url_for('admin.branches_index'))
    
    return render_template('admin/branches/create.html', form=form)

@admin_bp.route('/branches/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def branches_edit(id):
    branch = CompanyBranch.query.get_or_404(id)
    form = BranchForm(obj=branch)
    
    # پر کردن فرم با اطلاعات شبکه‌های اجتماعی موجود
    if request.method == 'GET':
        for social in branch.social_links:
            if social.type == 'instagram':
                form.instagram.data = social.url
            elif social.type == 'linkedin':
                form.linkedin.data = social.url
            elif social.type == 'telegram':
                form.telegram.data = social.url
    
    if form.validate_on_submit():
        if form.logo.data:
            logo_path = save_file(form.logo.data, 'logos')
            branch.logo_url = logo_path
        elif form.logo_url.data:
            branch.logo_url = form.logo_url.data
        
        branch.name = form.name.data
        branch.address = form.address.data
        branch.phone = form.phone.data
        branch.mobile = form.mobile.data
        branch.fax = form.fax.data
        branch.active = form.active.data
        
        # بروزرسانی شبکه‌های اجتماعی
        for social in branch.social_links:
            db.session.delete(social)
        
        if form.instagram.data:
            social = CompanySocial(branch_id=branch.id, type="instagram", url=form.instagram.data)
            db.session.add(social)
        if form.linkedin.data:
            social = CompanySocial(branch_id=branch.id, type="linkedin", url=form.linkedin.data)
            db.session.add(social)
        if form.telegram.data:
            social = CompanySocial(branch_id=branch.id, type="telegram", url=form.telegram.data)
            db.session.add(social)
        
        db.session.commit()
        
        flash('شعبه با موفقیت ویرایش شد.', 'success')
        return redirect(url_for('admin.branches_index'))
    
    return render_template('admin/branches/edit.html', form=form, branch=branch)

@admin_bp.route('/branches/delete/<int:id>')
@login_required
@admin_required
def branches_delete(id):
    branch = CompanyBranch.query.get_or_404(id)
    db.session.delete(branch)
    db.session.commit()
    
    flash('شعبه با موفقیت حذف شد.', 'success')
    return redirect(url_for('admin.branches_index'))

# ============================================
# مدیریت درباره ما (About Company)
# ============================================

@admin_bp.route('/about/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def about_edit():
    about = AboutCompany.query.first()
    if not about:
        about = AboutCompany()
        db.session.add(about)
    
    form = AboutForm(obj=about)
    
    if form.validate_on_submit():
        if form.logo.data:
            logo_path = save_file(form.logo.data, 'about')
            about.logo_url = logo_path
        elif form.logo_url.data:
            about.logo_url = form.logo_url.data
        
        if form.about_image.data:
            image_path = save_file(form.about_image.data, 'about')
            about.about_image_url = image_path
        elif form.about_image_url.data:
            about.about_image_url = form.about_image_url.data
        
        about.company_name = form.company_name.data
        about.slogan = form.slogan.data
        about.short_description = form.short_description.data
        about.full_description = form.full_description.data
        about.mission = form.mission.data
        about.vision = form.vision.data
        about.values = form.values.data
        about.founded_year = form.founded_year.data
        about.registration_number = form.registration_number.data
        about.national_id = form.national_id.data
        about.active = form.active.data
        
        db.session.commit()
        
        flash('اطلاعات درباره ما با موفقیت بروزرسانی شد.', 'success')
        return redirect(url_for('admin.about_edit'))
    
    return render_template('admin/about/edit.html', form=form, about=about)

# ============================================
# مدیریت آمار شرکت (Company Stats)
# ============================================

@admin_bp.route('/stats')
@login_required
@admin_required
def stats_index():
    stats = CompanyStat.query.order_by(CompanyStat.display_order).all()
    return render_template('admin/stats/index.html', stats=stats)

@admin_bp.route('/stats/create', methods=['GET', 'POST'])
@login_required
@admin_required
def stats_create():
    form = StatForm()
    
    if form.validate_on_submit():
        stat = CompanyStat(
            title=form.title.data,
            value=form.value.data,
            icon=form.icon.data,
            display_order=form.display_order.data,
            active=form.active.data
        )
        
        db.session.add(stat)
        db.session.commit()
        
        flash('آمار با موفقیت اضافه شد.', 'success')
        return redirect(url_for('admin.stats_index'))
    
    return render_template('admin/stats/create.html', form=form)

@admin_bp.route('/stats/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def stats_edit(id):
    stat = CompanyStat.query.get_or_404(id)
    form = StatForm(obj=stat)
    
    if form.validate_on_submit():
        stat.title = form.title.data
        stat.value = form.value.data
        stat.icon = form.icon.data
        stat.display_order = form.display_order.data
        stat.active = form.active.data
        
        db.session.commit()
        
        flash('آمار با موفقیت ویرایش شد.', 'success')
        return redirect(url_for('admin.stats_index'))
    
    return render_template('admin/stats/edit.html', form=form, stat=stat)

@admin_bp.route('/stats/delete/<int:id>')
@login_required
@admin_required
def stats_delete(id):
    stat = CompanyStat.query.get_or_404(id)
    db.session.delete(stat)
    db.session.commit()
    
    flash('آمار با موفقیت حذف شد.', 'success')
    return redirect(url_for('admin.stats_index'))

# ============================================
# مدیریت گواهینامه‌ها (Certificates)
# ============================================

@admin_bp.route('/certificates')
@login_required
@admin_required
def certificates_index():
    certificates = CompanyCertificate.query.order_by(CompanyCertificate.display_order).all()
    return render_template('admin/certificates/index.html', certificates=certificates)

@admin_bp.route('/certificates/create', methods=['GET', 'POST'])
@login_required
@admin_required
def certificates_create():
    form = CertificateForm()
    
    if form.validate_on_submit():
        image_path = save_file(form.image.data, 'certificates') if form.image.data else form.image_url.data
        
        certificate = CompanyCertificate(
            title=form.title.data,
            issuer=form.issuer.data,
            issue_year=form.issue_year.data,
            image_url=image_path,
            description=form.description.data,
            display_order=form.display_order.data,
            active=form.active.data
        )
        
        db.session.add(certificate)
        db.session.commit()
        
        flash('گواهینامه با موفقیت اضافه شد.', 'success')
        return redirect(url_for('admin.certificates_index'))
    
    return render_template('admin/certificates/create.html', form=form)

@admin_bp.route('/certificates/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def certificates_edit(id):
    certificate = CompanyCertificate.query.get_or_404(id)
    form = CertificateForm(obj=certificate)
    
    if form.validate_on_submit():
        if form.image.data:
            image_path = save_file(form.image.data, 'certificates')
            certificate.image_url = image_path
        elif form.image_url.data:
            certificate.image_url = form.image_url.data
        
        certificate.title = form.title.data
        certificate.issuer = form.issuer.data
        certificate.issue_year = form.issue_year.data
        certificate.description = form.description.data
        certificate.display_order = form.display_order.data
        certificate.active = form.active.data
        
        db.session.commit()
        
        flash('گواهینامه با موفقیت ویرایش شد.', 'success')
        return redirect(url_for('admin.certificates_index'))
    
    return render_template('admin/certificates/edit.html', form=form, certificate=certificate)

@admin_bp.route('/certificates/delete/<int:id>')
@login_required
@admin_required
def certificates_delete(id):
    certificate = CompanyCertificate.query.get_or_404(id)
    db.session.delete(certificate)
    db.session.commit()
    
    flash('گواهینامه با موفقیت حذف شد.', 'success')
    return redirect(url_for('admin.certificates_index'))

# ============================================
# مدیریت سئو (SEO)
# ============================================

@admin_bp.route('/seo/<string:page_key>', methods=['GET', 'POST'])
@login_required
@admin_required
def seo_edit(page_key):
    seo = PageSEO.query.filter_by(page_key=page_key).first()
    if not seo:
        seo = PageSEO(page_key=page_key)
        db.session.add(seo)
    
    form = SEOForm(obj=seo)
    
    if form.validate_on_submit():
        seo.meta_title = form.meta_title.data
        seo.meta_description = form.meta_description.data
        seo.meta_keywords = form.meta_keywords.data
        
        db.session.commit()
        
        flash(f'اطلاعات سئوی صفحه {page_key} با موفقیت بروزرسانی شد.', 'success')
        return redirect(url_for('admin.seo_edit', page_key=page_key))
    
    return render_template('admin/seo/edit.html', form=form, page_key=page_key)

# ============================================
# مدیریت کاربران ادمین
# ============================================

@admin_bp.route('/admins')
@login_required
@admin_required
def admins_index():
    admins = Admin.query.all()
    return render_template('admin/admins/index.html', admins=admins)

@admin_bp.route('/admins/create', methods=['GET', 'POST'])
@login_required
@admin_required
def admins_create():
    form = AdminCreateForm()
    
    if form.validate_on_submit():
        admin = Admin(
            username=form.username.data,
            email=form.email.data,
            full_name=form.full_name.data,
            is_active=True
        )
        admin.set_password(form.password.data)
        
        db.session.add(admin)
        db.session.commit()
        
        flash('کاربر ادمین با موفقیت اضافه شد.', 'success')
        return redirect(url_for('admin.admins_index'))
    
    return render_template('admin/admins/create.html', form=form)

@admin_bp.route('/admins/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admins_edit(id):
    admin = Admin.query.get_or_404(id)
    
    # جلوگیری از ویرایش خود شخص
    if admin.id == current_user.id:
        flash('شما نمی‌توانید حساب کاربری خودتان را ویرایش کنید.', 'warning')
        return redirect(url_for('admin.admins_index'))
    
    form = AdminEditForm(obj=admin)
    
    if form.validate_on_submit():
        admin.username = form.username.data
        admin.email = form.email.data
        admin.full_name = form.full_name.data
        admin.is_active = form.is_active.data
        
        if form.password.data:
            admin.set_password(form.password.data)
        
        db.session.commit()
        
        flash('کاربر ادمین با موفقیت ویرایش شد.', 'success')
        return redirect(url_for('admin.admins_index'))
    
    return render_template('admin/admins/edit.html', form=form, admin=admin)

@admin_bp.route('/admins/delete/<int:id>')
@login_required
@admin_required
def admins_delete(id):
    admin = Admin.query.get_or_404(id)
    
    # جلوگیری از حذف خود شخص
    if admin.id == current_user.id:
        flash('شما نمی‌توانید حساب کاربری خودتان را حذف کنید.', 'danger')
        return redirect(url_for('admin.admins_index'))
    
    db.session.delete(admin)
    db.session.commit()
    
    flash('کاربر ادمین با موفقیت حذف شد.', 'success')
    return redirect(url_for('admin.admins_index'))

# ============================================
# تنظیمات عمومی (Profile)
# ============================================

@admin_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@admin_required
def profile():
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        
        if form.password.data:
            current_user.set_password(form.password.data)
        
        db.session.commit()
        
        flash('پروفایل شما با موفقیت بروزرسانی شد.', 'success')
        return redirect(url_for('admin.profile'))
    
    return render_template('admin/profile.html', form=form)