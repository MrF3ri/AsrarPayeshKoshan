import random
from datetime import datetime, timedelta
from app import create_app, db
from app.models import (
    News, Service, TeamMember, TeamContact,
    RelatedLink, Slider, Banner,
    CompanyBranch, CompanySocial
)

app = create_app()
app.app_context().push()


# ---------------------------------------------------
# تابع تولید تاریخ میلادی تصادفی در 2 سال اخیر
# ---------------------------------------------------
def random_date():
    days_back = random.randint(0, 700)
    return datetime.now() - timedelta(days=days_back)


# ---------------------------------------------------
# تولید داده‌های فیک
# ---------------------------------------------------
def seed_news():
    images = [
        "Images/News/news1.png", "Images/News/news2.jpeg",
        "Images/News/news3.jpg", "Images/News/news4.png",
        "Images/News/5.jpg", "Images/News/6.jpg",
        "Images/News/658.jpg", "Images/News/pishkhn9811.jpg",
        "Images/News/samad9810.jpg", "Images/News/samad9811.jpg"
    ]

    for i in range(10):
        news = News(
            title=f"خبر شماره {i + 1}",
            short_description="این یک متن تستی برای نمایش اخبار در سایت است.",
            image_url=random.choice(images),
            attachment_url=None,
            published_date=random_date(),
            views=random.randint(10, 500),
            active=True
        )
        db.session.add(news)


def seed_services():
    images = [
        "Images/986.jpg", "Images/987.jpg", "Images/988.jpg",
        "Images/989.jpg", "Images/emono1.jpeg", "Images/manage-bg.jpg"
    ]

    for i in range(6):
        service = Service(
            title=f"خدمت شماره {i + 1}",
            short_description="توضیح کوتاه درباره این خدمت.",
            full_description="این بخش شامل توضیحات کامل خدمت است و می‌تواند متن طولانی‌تری باشد.",
            image_url=random.choice(images),
            detail_link=f"/service/{i + 1}",
            active=True
        )
        db.session.add(service)


def seed_team():
    images = ["Images/avatar.jpg", "Images/logo.png", "Images/logo2.png", "Images/News/news1.png"]
    positions = ["مدیرعامل", "توسعه‌دهنده ارشد", "کارشناس امنیت", "طراح UI/UX"]

    for i in range(4):
        member = TeamMember(
            name=f"عضو تیم شماره {i + 1}",
            position=positions[i],
            image_url=random.choice(images),
            display_order=i + 1,
            active=True
        )
        db.session.add(member)
        db.session.flush()  # تا ID تولید شود

        # دو راه ارتباطی برای هر عضو
        contacts = [
            TeamContact(member_id=member.id, type="email", value=f"user{i + 1}@example.com"),
            TeamContact(member_id=member.id, type="phone", value=f"0912{random.randint(1000000, 9999999)}")
        ]
        db.session.add_all(contacts)


def seed_related_links():
    images = ["Images/banner1.png", "Images/banner2.png", "Images/banner3.png", "Images/banner4.png"]

    for i in range(8):
        link = RelatedLink(
            title=f"لینک مرتبط {i + 1}",
            description="این یک لینک مرتبط تستی است.",
            url=f"https://example.com/{i + 1}",
            image_url=random.choice(images),
            active=True
        )
        db.session.add(link)


def seed_sliders():
    images = [
        "Images/Slides/Slide-1.jpg", "Images/Slides/Slide-2.jpg",
        "Images/Slides/Slide-3.png", "Images/Slides/Slide-11.png",
        "Images/Slides/Slide-2.png"
    ]

    for i in range(5):
        slider = Slider(
            title=f"اسلایدر {i + 1}",
            image_url=random.choice(images),
            link=f"/slider/{i + 1}",
            display_order=i + 1,
            active=True
        )
        db.session.add(slider)


def seed_banners():
    images = ["Images/banner1.png", "Images/banner2.png", "Images/banner3.png", "Images/banner4.png"]

    for i in range(4):
        banner = Banner(
            title=f"بنر تبلیغاتی {i + 1}",
            image_url=random.choice(images),
            link=f"/banner/{i + 1}",
            active=True
        )
        db.session.add(banner)


def seed_company_branches():
    for i in range(3):
        branch = CompanyBranch(
            name=f"شعبه شماره {i + 1}",
            address=f"آدرس تستی برای شعبه {i + 1}",
            phone=f"021{random.randint(10000000, 99999999)}",
            mobile=f"0912{random.randint(1000000, 9999999)}",
            fax=f"021{random.randint(10000000, 99999999)}",
            logo_url="Images/logo.png",
            active=True
        )
        db.session.add(branch)
        db.session.flush()

        socials = [
            CompanySocial(branch_id=branch.id, type="instagram", url="https://instagram.com/example"),
            CompanySocial(branch_id=branch.id, type="linkedin", url="https://linkedin.com/company/example"),
            CompanySocial(branch_id=branch.id, type="telegram", url="https://t.me/example")
        ]
        db.session.add_all(socials)


# ---------------------------------------------------
# اجرای نهایی سِید
# ---------------------------------------------------
def main():
    print("⏳ در حال درج داده‌های فیک ...")

    seed_news()
    seed_services()
    seed_team()
    seed_related_links()
    seed_sliders()
    seed_banners()
    seed_company_branches()

    db.session.commit()

    print("✅ عملیات با موفقیت انجام شد! Fake data با موفقیت وارد دیتابیس شد.")


if __name__ == "__main__":
    main()
