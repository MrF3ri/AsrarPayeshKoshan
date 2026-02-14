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

const todayElement = document.getElementById("today-date");
if (todayElement) {
    const today = new Date();
    const jalali = gregorianToJalali(today.getFullYear(), today.getMonth() + 1, today.getDate());
    const monthNames = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"];
    const weekdays = ["یکشنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه", "شنبه"];
    todayElement.innerText = `${weekdays[today.getDay()]} ${jalali[2]} ${monthNames[jalali[1] - 1]} ${jalali[0]}`;
}

const footerContainer = document.getElementById("footer-dynamic");
if (footerContainer) {
    fetch('/static/Js/data/home.json')
        .then(res => res.json())
        .then(data => {
            const isHome = document.body.id === 'home';
            if (isHome && document.getElementById("page-title")) {
                document.getElementById("page-title").innerText = data.home.title;
            }

            const colLatest = document.createElement("div");
            colLatest.className = "col-lg-4 col-sm-6 py-3";
            colLatest.innerHTML = `<h5 class="IRANSansWeb_Medium">آخرین ارسالی ها :</h5>`;
            const ulLatest = document.createElement("ul");
            data.home.footer.latest.forEach(f => {
                const li = document.createElement("li");
                li.innerHTML = `<a href="${f.link}">${f.title}</a>`;
                ulLatest.appendChild(li);
            });
            colLatest.appendChild(ulLatest);
            footerContainer.appendChild(colLatest);

            const colQuick = document.createElement("div");
            colQuick.className = "col-lg-2 col-sm-6 py-3";
            colQuick.innerHTML = `<h5 class="IRANSansWeb_Medium">لینک های سریع :</h5>`;
            const ulQuick = document.createElement("ul");
            data.home.footer.quickLinks.forEach(f => {
                const li = document.createElement("li");
                li.innerHTML = `<a href="${f.link}">${f.title}</a>`;
                ulQuick.appendChild(li);
            });
            colQuick.appendChild(ulQuick);
            footerContainer.appendChild(colQuick);

            const colContact = document.createElement("div");
            colContact.className = "col-lg-6 col-sm-12 py-3";
            const c = data.home.footer.contact;
            colContact.innerHTML = `<h5 class="IRANSansWeb_Medium">ارتباط با ما :</h5>
                    <p>آدرس : ${c.address}</p>
                    <p>تلفن : ${c.phone}</p>
                    <p>تلفن همراه : ${c.mobile}</p>
                    <p>نمابر : ${c.fax}</p>`;
            footerContainer.appendChild(colContact);
        })
        .catch(err => console.error("خطا در دریافت داده‌ها:", err));
}
