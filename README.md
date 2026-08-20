# 🧵 Dunyo Textile

> Zamonaviy va professional tekstil mahsulotlari uchun ishlab chiqilgan Django asosidagi E-commerce platforma.

**Dunyo Textile** — tekstil mahsulotlarini onlayn ko‘rsatish, mahsulotlarni rang va o‘lcham bo‘yicha boshqarish, savatchaga qo‘shish, buyurtma berish va administrator paneli orqali saytni boshqarish imkonini beruvchi to‘liq web-platforma.

---

## ✨ Asosiy imkoniyatlar

### 🛍️ E-commerce

* Mahsulotlar katalogi
* Kategoriyalar va subkategoriyalar
* Mahsulot qidiruvi
* Mahsulot detail sahifasi
* Mahsulot rasmlari galeriyasi
* Mahsulot ranglarini boshqarish
* Har bir rang uchun alohida rasmlar
* Rangga bog‘langan o‘lchamlar
* Har bir o‘lcham uchun alohida stock
* Mahsulot chegirmalari
* Eski va yangi narxlarni ko‘rsatish
* Wishlist
* Session-based shopping cart
* Savatchadagi mahsulot miqdorini o‘zgartirish
* Savatchadan mahsulotni o‘chirish
* Avtomatik subtotal va umumiy summa hisoblash
* Checkout
* Buyurtmalarni boshqarish

---

## 🎨 Product Variants

Loyihaning muhim qismlaridan biri — mahsulotlarni **rang va o‘lcham bo‘yicha boshqarish**.

Masalan:

```text
T-Shirt
│
├── Black
│   ├── S → 10 dona
│   ├── M → 15 dona
│   └── L → 8 dona
│
├── Gray
│   ├── S → 5 dona
│   ├── M → 12 dona
│   └── L → 4 dona
│
└── Red
    ├── S → 7 dona
    ├── M → 10 dona
    └── L → 6 dona
```

Har bir rang uchun:

* rang nomi
* HEX color code
* alohida gallery
* o‘ziga tegishli size va stock

saqlanadi.

Foydalanuvchi detail sahifasida boshqa rangni tanlaganda:

* mahsulot rasmi o‘zgaradi;
* shu rangga tegishli gallery chiqadi;
* shu rangga tegishli o‘lchamlar ko‘rsatiladi;
* tanlangan rang va o‘lcham cart'ga saqlanadi.

---

# 🛒 Shopping Cart

Cart session asosida ishlaydi.

Savatchada:

* mahsulot
* rang
* o‘lcham
* miqdor
* mahsulot narxi
* subtotal
* umumiy summa

ko‘rsatiladi.

Cart bir xil mahsulotning turli variantlarini ham alohida saqlay oladi.

Masalan:

```text
T-Shirt / Black / M
T-Shirt / Gray  / M
T-Shirt / Red   / L
```

uchta alohida cart item sifatida ishlashi mumkin.

---

# ❤️ Wishlist

Foydalanuvchilar mahsulotlarni wishlist'ga qo‘shishi yoki olib tashlashi mumkin.

Wishlist:

* mahsulotni saqlash
* mahsulotni olib tashlash
* active/inactive heart icon
* AJAX orqali ishlash

imkoniyatlarini o‘z ichiga oladi.

---

# ⭐ Product Reviews

Foydalanuvchilar mahsulotlar uchun review qoldirishlari mumkin.

Review tizimida:

* foydalanuvchi
* mahsulot
* baho
* izoh
* active status

saqlanadi.

Administrator review'larni nazorat qilishi mumkin.

---

# 📦 Orders

Checkout orqali buyurtma yaratish mumkin.

Buyurtma tarkibida:

* customer information
* mahsulotlar
* rang
* o‘lcham
* quantity
* price
* total
* order status

saqlanadi.

---

# 🛠️ Admin Dashboard

Loyiha professional dashboard bilan ta'minlangan.

Administrator orqali saytning asosiy qismlarini boshqarish mumkin:

### Products

* Product list
* Product create
* Product update
* Product delete
* Product detail
* Product colors
* Product gallery
* Product sizes
* Stock management

### Categories

* Category CRUD
* Subcategory CRUD

### Orders

* Buyurtmalarni ko‘rish
* Buyurtma ma'lumotlarini ko‘rish
* Status boshqaruvi

### Users

* Foydalanuvchilarni boshqarish
* Rollar va permissions

### Branches

* Filiallar
* Manzil
* Telefon
* Ish vaqti
* Latitude
* Longitude

---

# ⚙️ Website Settings

Administrator uchun alohida **Settings** panel ishlab chiqilgan.

```text
Settings
│
├── General
├── Contact
├── Social Media
├── Map
├── SEO
└── System
```

## General

* Website name
* Website description
* Logo
* Favicon

## Contact

* Phone
* Email
* Address
* Working hours

## Social Media

* Telegram
* Instagram
* Facebook
* YouTube
* TikTok

## Map

* Latitude
* Longitude
* Store location
* Interactive Yandex Map

## SEO

* Meta title
* Meta description
* Meta keywords

## System

* Default language
* Default currency
* Timezone
* Products per page
* Orders per page
* Dashboard theme
* Maintenance mode
* Registration status

---

# 🗺️ Yandex Maps

Filial va sayt manzilini ko‘rsatish uchun **Yandex Maps API** ishlatilgan.

Xaritada:

* marker
* zoom
* fullscreen
* geolocation
* location search
* marker drag & drop
* latitude/longitude synchronization

funksiyalari mavjud.

Administrator marker joylashuvini xarita orqali o‘zgartirishi mumkin.

---

# 🔐 Authentication & Security

Loyihada Django authentication tizimidan foydalanilgan.

Administrator Settings bo‘limiga faqat:

```python
is_superuser = True
```

bo‘lgan foydalanuvchilar kira oladi.

Shuningdek:

* CSRF protection
* Login protection
* Permission checking
* Session-based cart
* Django authentication

ishlatilgan.

---

# 🖥️ Frontend

Frontend zamonaviy va responsive dizayn asosida ishlab chiqilgan.

Texnologiyalar:

* HTML5
* CSS3
* JavaScript
* Bootstrap
* Bootstrap Icons
* Django Templates

Responsive dizayn:

```text
Desktop
Tablet
Mobile
```

qurilmalar uchun moslashtirilgan.

---

# ⚡ JavaScript

Frontend'da JavaScript orqali interaktiv funksiyalar amalga oshirilgan.

Masalan:

* Product image switching
* Color switching
* Dynamic gallery
* Dynamic sizes
* Quantity control
* Image zoom
* Accordion
* Wishlist interaction
* Cart AJAX actions
* Map interaction

---

# 🧩 Project Structure

Loyihaning asosiy strukturasi:

```text
Dunyo-Textile/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── main/
│   ├── models/
│   ├── views/
│   ├── forms/
│   ├── templates/
│   ├── static/
│   │   └── main/
│   │       ├── css/
│   │       └── js/
│   └── urls.py
│
├── dashboard/
│   ├── views/
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── settings.py
│   │   └── ...
│   │
│   ├── templates/
│   │   └── dashboard/
│   │       ├── base.html
│   │       ├── product/
│   │       ├── order/
│   │       └── settings/
│   │           ├── index.html
│   │           ├── general.html
│   │           ├── contact.html
│   │           ├── social.html
│   │           ├── map.html
│   │           ├── seo.html
│   │           └── system.html
│   │
│   └── static/
│       └── dashboard/
│           ├── css/
│           └── js/
│
├── media/
│   └── products/
│
├── static/
│
├── templates/
│
├── manage.py
├── requirements.txt
├── .env
└── README.md
```

---

# 🧱 Database Models

Asosiy modellardan ba'zilari:

```text
Product
│
├── ProductColor
│   └── ProductGallery
│
├── ProductSize
│
├── Category
│
├── SubCategory
│
├── Order
│   └── OrderItem
│
├── ProductReview
│
├── Wishlist
│
├── Branch
│
└── SiteSettings
```

`SiteSettings` singleton model sifatida ishlaydi va faqat bitta settings yozuvini saqlaydi.

```python
self.pk = 1
```

orqali settings yagona instance sifatida boshqariladi.

---

# 🚀 Installation

## 1. Repository'ni clone qilish

```bash
git clone <repository-url>
```

Loyiha papkasiga o'ting:

```bash
cd Dunyo-Textile
```

---

## 2. Virtual environment yaratish

Linux / macOS:

```bash
python3 -m venv .venv
```

Windows:

```bash
python -m venv .venv
```

Aktivlashtirish:

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

---

# 📦 Dependencies

Kerakli package'larni o‘rnatish:

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

`.env` fayl yarating:

```env
SECRET_KEY=your-secret-key

DEBUG=True

ALLOWED_HOSTS=127.0.0.1,localhost

DATABASE_URL=

YANDEX_MAPS_API_KEY=
```

Production muhitida `DEBUG=False` qilish tavsiya etiladi.

---

# 🗄️ Database

Migrationlarni bajaring:

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

---

# 👤 Superuser yaratish

Admin panel uchun:

```bash
python manage.py createsuperuser
```

Username, email va password kiriting.

---

# ▶️ Development Server

Serverni ishga tushirish:

```bash
python manage.py runserver
```

Keyin:

```text
http://127.0.0.1:8000/
```

manziliga kiring.

Dashboard:

```text
http://127.0.0.1:8000/dashboard/
```

---

# 🧪 Testing

Testlarni ishga tushirish:

```bash
python manage.py test
```

Alohida app testlari:

```bash
python manage.py test main
```

---

# 📸 Media Files

Development muhitida media fayllar:

```text
media/
```

papkasida saqlanadi.

Mahsulot gallery rasmlari:

```text
media/products/gallery/
```

Logo:

```text
media/settings/logo/
```

Favicon:

```text
media/settings/favicon/
```

---

# 🌍 Localization

Loyiha ko‘p tilli ishlashga tayyorlangan.

Asosiy til:

```text
Uzbek
```

Django translation tizimi orqali boshqa tillarni ham qo‘shish mumkin.

---

# 💰 Currency

Default currency:

```text
UZS
```

Masalan:

```text
250 000 UZS
```

---

# 🛡️ Production Recommendations

Production serverga joylashtirishdan oldin:

* `DEBUG=False`
* kuchli `SECRET_KEY`
* `ALLOWED_HOSTS` ni to‘g‘ri sozlash
* HTTPS ishlatish
* PostgreSQL ishlatish
* Static files'ni collect qilish
* Media files'ni to‘g‘ri konfiguratsiya qilish
* Yandex Maps API key'ni environment variable orqali saqlash

tavsiya qilinadi.

Static files:

```bash
python manage.py collectstatic
```

---

# 🧰 Technologies

| Technology          | Purpose            |
| ------------------- | ------------------ |
| Python              | Backend            |
| Django              | Web Framework      |
| Django Templates    | Frontend rendering |
| SQLite / PostgreSQL | Database           |
| HTML5               | Markup             |
| CSS3                | Styling            |
| JavaScript          | Interactivity      |
| Bootstrap           | UI                 |
| Bootstrap Icons     | Icons              |
| Yandex Maps API     | Maps               |
| Pillow              | Image processing   |

---

# 📈 Future Improvements

Kelajakda quyidagi imkoniyatlarni qo‘shish mumkin:

* Online payment integration
* Telegram Bot notifications
* SMS notifications
* Advanced product filtering
* Product comparison
* Advanced analytics
* Sales statistics
* Customer dashboard
* Order tracking
* Multi-language admin
* Multi-currency support
* Redis caching
* Celery background tasks
* Docker deployment
* Nginx + Gunicorn
* PostgreSQL optimization

---

# 👨‍💻 Development

Loyiha Django architecture asosida modulli qilib ishlab chiqilgan.

Backend:

```text
Django
        ↓
Views
        ↓
Models
        ↓
Templates
        ↓
JavaScript
```

Admin:

```text
Dashboard
    ↓
Settings
    ↓
Products
    ↓
Orders
    ↓
Users
    ↓
Branches
```

---

# 📄 License

Ushbu loyiha shaxsiy/commercial loyiha sifatida ishlab chiqilgan.

Barcha huquqlar loyiha egasiga tegishli.

---

# ⭐ Dunyo Textile

**Dunyo Textile** — tekstil mahsulotlarini zamonaviy va qulay tarzda boshqarish hamda sotish uchun yaratilgan to‘liq Django E-commerce platforma.

> Built with Django & ❤️
