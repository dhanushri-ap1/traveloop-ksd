# ✈️ Traveloop

> A cinematic desktop travel companion app for exploring India — built with Electron, Flask, and an AI-powered chatbot.

---

## 📌 What is This?

**Traveloop** is a desktop application that lets users discover Indian travel destinations, plan their trips, chat with an AI travel assistant, and save their travel memories — all in one place. It combines a native desktop shell (Electron) with a Python backend for authentication, a MySQL database, and an AI chatbot powered by the Groq API.

---

## 🛠️ Tech Stack

### 🖥️ Frontend / Desktop Shell
| Tool | Version | Purpose |
|------|---------|---------|
| **Electron** | ^35.1.2 | Desktop app wrapper |
| **HTML / CSS / JS** | — | All UI pages |
| **Leaflet.js** | 1.9.4 | Interactive travel map |
| **Google Fonts** | — | Playfair Display, Plus Jakarta Sans, DM Mono |
| **globals.css** | — | Shared design system |

### 🐍 Backend (Auth Server)
| Tool | Version | Purpose |
|------|---------|---------|
| **Flask** | latest | Web server & routing |
| **flask-mysqldb** | — | MySQL ORM bridge |
| **flask-bcrypt** | — | Password hashing |
| **bcrypt** | 4.1.3 | Bcrypt hashing utility |
| **PyJWT** | 2.8.0 | JWT token generation |
| **python-dotenv** | 1.0.1 | Environment variable management |
| **uuid** | built-in | Unique user ID generation |

### 🗄️ Database
| Tool | Version | Purpose |
|------|---------|---------|
| **MySQL** | — | User data storage |
| **mysql-connector-python** | 8.3.0 | Python MySQL driver |

### 🤖 AI Chatbot
| Tool | Details | Purpose |
|------|---------|---------|
| **Groq API** | `llama-3.3-70b-versatile` | Fast LLM inference |
| **OpenAI-compatible endpoint** | `api.groq.com/openai/v1/chat/completions` | Chat completions |

### 📦 Build & Packaging
| Tool | Version | Purpose |
|------|---------|---------|
| **electron-builder** | ^24.13.3 | Package app to `dist/` |
| **electron-packager** | ^17.1.2 | Cross-platform packaging |

---

## 🗂️ Project Structure

```
traveloop-ksd/
│
├── server.py                  # Flask backend (auth routes)
├── requirements.txt           # Python dependencies
│
├── static/
│   ├── main.js                # Electron entry point — creates BrowserWindow & app menu
│   ├── preload.js             # Electron context bridge (security layer)
│   ├── renderer.js            # Frontend logic
│   ├── globals.css            # Shared stylesheet
│   ├── package.json           # Electron config & build scripts
│   │
│   ├── auth.html              # Login / Signup page (root route)
│   ├── login.html             # Login page
│   ├── homepage.html          # Dashboard (post-login, cinematic video bg)
│   ├── index.html             # App index
│   │
│   ├── pr.html                # 🤖 AI Chatbot — "Memorify" (Groq LLM)
│   ├── mapping3.html          # 🗺️ Interactive map (Leaflet.js)
│   ├── todolist.html          # ✅ Trip to-do list & budget planner
│   ├── scrapbook.html         # 📸 Travel memories / scrapbook
│   │
│   ├── goa.html               # 🏖️ Destination page — Goa
│   ├── manali.html            # 🏔️ Destination page — Manali
│   ├── ladakh.html            # 🏔️ Destination page — Ladakh
│   ├── rishikesh.html         # 🌊 Destination page — Rishikesh
│   ├── delhi.html             # 🕌 Destination page — Delhi
│   ├── darjeeling.html        # 🍵 Destination page — Darjeeling
│   ├── kolkata.html           # 🎨 Destination page — Kolkata
│   ├── bangalore.html         # 💻 Destination page — Bangalore
│   └── ahmedabad.html         # 🏛️ Destination page — Ahmedabad
│
├── bg-vid.mp4                 # Background video for homepage
├── Traveloop.png              # App logo
└── [other image assets]       # chatbot.jpg, botbg2.jpg, ind.jpg, etc.
```

---

## ✨ Features

### 🔐 Authentication
- User signup with first name, last name, email, and password
- Passwords hashed with **bcrypt** before storing
- Login with session management via Flask's `session`
- UUIDs used as user IDs (`CHAR(36)` in MySQL)
- Flash messages for error/success feedback

### 🏠 Homepage / Dashboard
- Cinematic full-screen video background (`bg-vid.mp4`)
- Personalised greeting using the logged-in user's name
- Feature cards linking to all major sections

### 🤖 AI Chatbot — *Memorify*
- Powered by **Groq API** with `llama-3.3-70b-versatile`
- Travel-specific system prompt and persona
- **Mood modes**: Explorer 🧭 · Budget 💰 · Luxury 💎
- Quick-chip suggestions:
  - Best beaches, Things to do in Goa, Hidden gems in India
  - Rajasthan itinerary, Budget SE Asia tips, Mountain trips, and more
- Send with `Enter`, new line with `Shift+Enter`

### 🗺️ Interactive Map
- Built with **Leaflet.js** on OpenStreetMap tiles
- Destination markers with custom popups
- Click markers to explore destination info

### ✅ Trip To-Do List & Budget Planner
- Add and manage travel tasks/itinerary items
- Budget tracking features

### 📸 Scrapbook / Memories
- Visual memory cards for saved trips
- Calendar and shared plans layout

### 🏙️ Destination Pages
9 dedicated destination pages with travel info, attractions, and tips:
**Goa · Manali · Ladakh · Rishikesh · Delhi · Darjeeling · Kolkata · Bangalore · Ahmedabad**

---

## ⚙️ Setup & Running

### Prerequisites
- Node.js & npm
- Python 3.x
- MySQL server running locally

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
# Also install: pip install flask flask-mysqldb flask-bcrypt
```

### 2. Set up MySQL database
```sql
CREATE DATABASE traveloop;
USE traveloop;

CREATE TABLE users (
  id CHAR(36) PRIMARY KEY,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  email VARCHAR(255) UNIQUE,
  password_hash VARCHAR(255)
);
```

### 3. Configure environment variables
Create a `.env` file or update `server.py`:
```
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=traveloop
```

### 4. Run the Flask backend
```bash
python server.py
```
Flask runs at `http://localhost:5000`

### 5. Install Electron dependencies
```bash
cd static
npm install
```

### 6. Add your Groq API key
In `static/pr.html`, replace:
```js
let apiKey = 'paste your api key here';
```
with your actual key from [console.groq.com](https://console.groq.com)

### 7. Run the Electron app
```bash
cd static
npm start
```

### 8. Build for distribution (optional)
```bash
cd static
npm run build
# Output → static/dist/
```

---

## 🔒 Security Notes

> ⚠️ Before deploying or sharing this project, fix these:

- **Hardcoded MySQL password** in `server.py` — move to `.env` and use `python-dotenv`
- **Hardcoded Groq API key** in `pr.html` — move to a backend proxy or environment variable
- **Flask secret key** `'your_secret_key'` — replace with a strong random key

---

## 🗺️ App Navigation (Electron Menu)

The Electron app has a native menu bar with:

```
File        → Open / Save / Exit
Menu        → Home · Map · ChatBot · To-Do-List · Snaps · Log-in
Edit        → Undo · Redo · Cut · Copy · Paste
Help        → About
```

---

## 📄 License

ISC

---

*Built with ✈️ wanderlust and a lot of HTML.*
