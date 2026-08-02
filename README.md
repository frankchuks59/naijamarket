# 🇳🇬 NaijaMarket - Nigeria's Local Marketplace

> **Live Demo:** https://naijamarket-vapn.onrender.com

A full-stack marketplace platform connecting buyers and sellers across Nigeria's 36 states. Built with Django, Bootstrap, and PostgreSQL.

---

## ✨ Features

### For Buyers
- 🔍 Search products by name, category, and location
- 📍 View seller locations across all 36 states
- 🚚 Filter by delivery availability
- 📱 Mobile-responsive design

### For Sellers
- 🏪 Create seller profile with business information
- 📦 Add/edit/delete product listings
- 📊 Dashboard with sales analytics
- ⭐ Featured/verified product badges

### For Admins
- 👑 Full admin dashboard for product management
- ✅ Verify sellers and products
- 🌟 Feature products on homepage
- 📈 Platform analytics

### Security Features
- 🔐 User authentication with OTP verification
- 🔄 Password reset via email
- 🛡️ CSRF protection, secure sessions
- 👥 Role-based access control (Buyer/Seller/Admin)

### AI-Powered
- 🤖 NaijaAI Business Advisor chatbot
- 📍 Location recommendations for new businesses
- 📊 Market analysis and pricing guidance

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Django 4.2, Python |
| **Frontend** | Bootstrap 5, HTML, CSS, JavaScript |
| **Database** | PostgreSQL (Production), SQLite (Development) |
| **Deployment** | Render.com |
| **Static Files** | WhiteNoise |
| **Security** | OTP, Password Reset, CSRF Protection |
| **Version Control** | Git, GitHub |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip
- PostgreSQL (for production)

### Installation

```bash
# Clone the repository
- 🐙 GitHub: [github.com/frankchuks59](https://github.com/frankchuks59)
git clone https://github.com/frankchuks59/naijamarket.git
cd naijamarket

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
