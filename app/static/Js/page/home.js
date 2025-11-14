// نمایش تاریخ شمسی
function gregorianToJalali(gy, gm, gd) {
    var g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334];
    var jy = (gy <= 1600) ? 0 : 979;
    gy -= (gy <= 1600) ? 621 : 1600;
    var gy2 = (gm > 2) ? (gy + 1) : gy;
    var days = 365 * gy + Math.floor((gy2 + 3) / 4) - Math.floor((gy2 + 99) / 100) + Math.floor((gy2 + 399) / 400) - 80 + gd + g_d_m[gm - 1];
    jy += 33 * Math.floor(days / 12053); days %= 12053;
    jy += 4 * Math.floor(days / 1461); days %= 1461;
    jy += Math.floor(days / 365);
    var jd = days % 365 + 1;
    var jm = (jd <= 186) ? Math.ceil(jd / 31) : Math.ceil((jd - 6) / 30);
    var jd_day = (jd <= 186) ? (jd % 31 == 0 ? 31 : jd % 31) : ((jd - 186) % 30 == 0 ? 30 : (jd - 186) % 30);
    return [jy, jm, jd_day];
}

const today = new Date();
const jalali = gregorianToJalali(today.getFullYear(), today.getMonth() + 1, today.getDate());
const monthNames = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"];
const weekdays = ["یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه"];
const dayName = weekdays[today.getDay()];
document.getElementById("today-date").innerText = `${dayName} ${jalali[2]} ${monthNames[jalali[1] - 1]} ${jalali[0]}`;
// بارگذاری JSON
fetch('/static/Js/data/home.json')
    .then(res => res.json())
    .then(data => {
        // عنوان صفحه
        document.getElementById("page-title").innerText = data.home.title;

        // پر کردن منو
        const menuList = document.getElementById("menu-list");
        data.home.urls.forEach(item => {
            if (item.length > 1) {
                // منوی کشویی
                const li = document.createElement("li");
                li.classList.add("dropdown");

                const a = document.createElement("a");
                a.href = "#";
                a.classList.add("dropdown-toggle");
                a.setAttribute("data-toggle", "dropdown");
                a.innerHTML = item[0];
                li.appendChild(a);

                const ul = document.createElement("ul");
                ul.classList.add("dropdown-menu");

                for (let i = 1; i < item.length; i++) {
                    const liSub = document.createElement("li");
                    const aSub = document.createElement("a");
                    aSub.href = item[i].link;
                    aSub.textContent = item[i].title;
                    liSub.appendChild(aSub);
                    ul.appendChild(liSub);
                }

                li.appendChild(ul);
                menuList.appendChild(li);
            } else {
                // منوی ساده
                const li = document.createElement("li");
                const a = document.createElement("a");
                a.href = item[0].link;
                a.textContent = item[0].title;
                li.appendChild(a);
                menuList.appendChild(li);
            }
        });

        // پر کردن فوتر
        const footerContainer = document.getElementById("footer-dynamic");

        // آخرین ارسالی‌ها
        const colLatest = document.createElement("div");
        colLatest.className = "col-lg-4 col-sm-6 py-3 order-lg-1 order-1 pl-lg-2";
        colLatest.innerHTML = `<h5 class="IRANSansWeb_Medium">آخرین ارسالی ها :</h5>`;
        const ulLatest = document.createElement("ul");
        data.home.footer.latest.forEach(f => {
            const li = document.createElement("li");
            const a = document.createElement("a");
            a.href = f.link;
            a.textContent = f.title;
            li.appendChild(a);
            ulLatest.appendChild(li);
        });
        colLatest.appendChild(ulLatest);
        footerContainer.appendChild(colLatest);

        // لینک‌های سریع
        const colQuick = document.createElement("div");
        colQuick.className = "col-lg-2 col-sm-6 py-3 order-lg-1 order-1";
        colQuick.innerHTML = `<h5 class="IRANSansWeb_Medium">لینک های سریع :</h5>`;
        const ulQuick = document.createElement("ul");
        data.home.footer.quickLinks.forEach(f => {
            const li = document.createElement("li");
            const a = document.createElement("a");
            a.href = f.link;
            a.textContent = f.title;
            li.appendChild(a);
            ulQuick.appendChild(li);
        });
        colQuick.appendChild(ulQuick);
        footerContainer.appendChild(colQuick);

        // پیوندها
        const colLinks = document.createElement("div");
        colLinks.className = "col-lg-2 col-sm-6 py-3 order-lg-2 order-3";
        colLinks.innerHTML = `<h5 class="IRANSansWeb_Medium">پیوندها :</h5>`;
        const ulLinks = document.createElement("ul");
        data.home.footer.links.forEach(f => {
            const li = document.createElement("li");
            const a = document.createElement("a");
            a.href = f.link;
            a.textContent = f.title;
            li.appendChild(a);
            ulLinks.appendChild(li);
        });
        colLinks.appendChild(ulLinks);
        footerContainer.appendChild(colLinks);

        // ارتباط با ما
        const colContact = document.createElement("div");
        colContact.className = "col-lg-4 col-sm-6 pr-lg-4 py-3 IRANSansWeb_FaNum order-lg-3 order-2";
        const c = data.home.footer.contact;
        colContact.innerHTML = `<h5 class="IRANSansWeb_Medium">ارتباط با ما :</h5>
                <p><i class="fas fa-2x fa-map-marker-alt ml-2"></i>آدرس : ${c.address}</p>
                <p><i class="fas fa-2x fa-phone ml-2"></i>تلفن : ${c.phone}</p>
                <p><i class="fas fa-2x fa-mobile-alt ml-2"></i>تلفن همراه : ${c.mobile}</p>
                <p><i class="fas fa-2x fa-fax ml-2"></i>نمابر : ${c.fax}</p>`;
        footerContainer.appendChild(colContact);

    })
    .catch(err => console.error("خطا در دریافت داده‌ها:", err));
