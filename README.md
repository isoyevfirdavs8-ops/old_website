# Dunyo Textile
 
To'qimachilik mahsulotlarini onlayn sotish uchun to'liq funksional **e-commerce** platforma. Django asosida qurilgan, boshqaruv paneli, onlayn to'lov tizimlari va ikki tilli interfeys bilan jihozlangan.
 
## Xususiyatlari
 
- 🛍️ **Mahsulotlar katalogi** — rang va o'lcham bo'yicha variantlar tizimi (`ProductColor` → `ProductSize`)
- 🌍 **Ikki tillilik** — O'zbek va Rus tillarida kontent (`name` / `name_ru` maydonlari orqali)
- 💳 **Onlayn to'lovlar** — Click va Payme to'lov tizimlari bilan integratsiya
- 🗺️ **Filiallar xaritasi** — Yandex Maps orqali eng yaqin filialni topish
- 📊 **Boshqaruv paneli** — buyurtmalar, mahsulotlar va statistikani boshqarish uchun to'liq admin dashboard, Chart.js orqali vizualizatsiya
- 🌓 **Dark mode** — ilova bo'ylab qorong'i rejim, custom context processor orqali
- ⚡ **Optimallashtirilgan so'rovlar** — `select_related`/`prefetch_related` va `aggregate` orqali N+1 muammosi bartaraf etilgan
- 🔍 **SEO** — slug asosidagi URL'lar va sitemap
## Texnologiyalar
 
| Qatlam | Texnologiya |
|---|---|
| Backend | Django |
| Frontend | Bootstrap 5, Chart.js |
| Baza | PostgreSQL / SQLite |
| To'lov | Click, Payme (JSON-RPC / prepare-complete oqimlari) |
| Xarita | Yandex Maps API |
 
## Loyiha tuzilishi
 
```
dunyo_textile/
├── config/              # Loyiha sozlamalari (settings, urls)
├── catalog/             # Mahsulotlar, kategoriyalar, variantlar
├── orders/              # Buyurtmalar va to'lovlar
├── branches/            # Filiallar va xarita
├── dashboard/           # Boshqaruv paneli
├── static/              # CSS, JS, rasm fayllari
├── templates/           # HTML shablonlar
└── manage.py
```
 
## O'rnatish
 
### 1. Repozitoriyani klonlash
 
```bash
git clone https://github.com/isoyevfirdavs8-ops/old_website.git
cd old_website
```
 
### 2. Virtual environment yaratish
 
```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
```
 
### 3. Kerakli kutubxonalarni o'rnatish
 
```bash
pip install -r requirements.txt
```
 
### 4. Muhit o'zgaruvchilarini sozlash
 
Loyiha papkasida `.env` fayl yarating va quyidagilarni to'ldiring:
 
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-database-url
CLICK_MERCHANT_ID=your-click-merchant-id
PAYME_MERCHANT_ID=your-payme-merchant-id
YANDEX_MAPS_API_KEY=your-yandex-maps-key
```
 
### 5. Bazani sozlash
 
```bash
python manage.py migrate
python manage.py createsuperuser
```
 
### 6. Serverni ishga tushirish
 
```bash
python manage.py runserver
```
 
Loyiha `http://127.0.0.1:8000` manzilida ochiladi, boshqaruv paneli esa `http://127.0.0.1:8000/admin`.
 
## Skrinshotlar
 
*(Bu yerga loyihaning asosiy sahifalari, boshqaruv paneli va mobil ko'rinishining skrinshotlarini qo'shing)*
 
## Muallif
 
**Firdavs Isoyev**
Backend Developer (Django) — Toshkent, O'zbekiston
GitHub: [@isoyevfirdavs8-ops](https://github.com/isoyevfirdavs8-ops)
 
## Litsenziya
 
Bu loyiha shaxsiy/tijorat maqsadida ishlab chiqilgan. Foydalanish huquqlari muallif bilan kelishilgan holda belgilanadi.
 