# ✈️ Traveloop

> A cinematic desktop travel companion app — plan trips, track budgets, chat with an AI, and build your traveller profile.

---

## 📌 What is This?

**Traveloop** is a desktop application built with Electron + Flask that helps users plan and remember their travels. It combines a native desktop shell with a Python auth backend, MySQL database, an AI-powered chatbot (via Groq), and a rich set of personal travel tools — all in one cohesive app.

---

## 🛠️ Tech Stack

### 🖥️ Frontend / Desktop Shell
| Tool | Version | Purpose |
|------|---------|---------|
| **Electron** | ^35.1.2 | Desktop app wrapper |
| **HTML / CSS / JS** | — | All UI pages |
| **Google Fonts** | — | Playfair Display, DM Sans, DM Mono |
| **IndexedDB** | browser built-in | Persistent image storage for Snaps |
| **localStorage** | browser built-in | Trip data, budget, wishlist, profile |

### 🐍 Backend (Auth Server)
| Tool | Version | Purpose |
|------|---------|---------|
| **Flask** | latest | Web server & routing |
| **flask-mysqldb** | — | MySQL bridge |
| **flask-bcrypt** | — | Password hashing |
| **bcrypt** | 4.1.3 | Bcrypt utility |
| **PyJWT** | 2.8.0 | JWT token generation |
| **python-dotenv** | 1.0.1 | `.env` config loading |
| **geopy** | latest | Geolocation utilities |
| **uuid** | built-in | Unique user ID generation |

### 🗄️ Database
| Tool | Version | Purpose |
|------|---------|---------|
| **MySQL** | — | User accounts storage |
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
├── server.py                  # Flask backend (auth + protected routes)
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (DB, JWT, PORT)
│
├── static/
│   ├── main.js                # Electron entry — BrowserWindow & app menu
│   ├── preload.js             # Electron context bridge
│   ├── renderer.js            # Frontend logic
│   ├── globals.css            # Shared stylesheet
│   ├── package.json           # Electron config & build scripts
│   │
│   ├── auth.html              # Login / Signup page (root route)
│   ├── login.html             # Login page
│   ├── dashboard.html         # 🆕 Full dashboard with sidebar layout
│   ├── profile.html           # 🆕 Traveller profile page
│   │
│   ├── pr.html                # 🤖 AI Chatbot — "Memorify" (Groq LLM)
│   ├── todolist.html          # ✅ Multi-city itinerary & budget planner
│   └── scrapbook.html         # 📸 Travel memories / Snaps
│
└── routes/templates           # (reserved for future Flask templates)
```

---

## ✨ What's New

### 🆕 Dashboard — Complete Redesign (`dashboard.html`)

The old homepage has been replaced with a full app-style dashboard with a **sidebar layout**.

**Sidebar navigation** — persistent left sidebar with:
- Traveloop branding and user avatar with first initial
- Dynamic greeting (`Good morning / afternoon / evening, [Name]`)
- Links to: Dashboard · Itinerary · Budget · Snaps · AI Guide · Analytics · Profile
- Live trip count badge on the Itinerary link
- Logout button

**Hero banner** — gradient coral/amber banner with animated floating globe emoji, a `✈ New Trip` CTA button, and an `Ask AI Guide` button.

**Quick Insights row** — 3 live stat cards that pull from `localStorage`:
- Next departure countdown (in days)
- Number of active/upcoming trips
- Average trip budget across all planned trips

**Stats row** — 4 animated metric cards with staggered fade-up animation:
- Total Trips · Destinations · Total Budget · Activities (wishlist count)

**Trip management panel** — shows all saved trips with:
- Coloured left-bar accent, emoji icon, destination, date range
- Auto-calculated status badges: `upcoming` / `planning` / `completed`
- Budget display per trip
- View · Edit · Delete buttons per trip

**New Trip modal** — opens on `✈ New Trip` click with fields for:
- Trip Name, Destination, Budget (₹), Start Date, End Date
- Saves to `localStorage` as `traveloop_trips`
- Edit mode pre-fills the form and replaces the old entry

**Budget Overview panel** — shows Total / Saved / Needed values with an animated savings progress bar and per-category bars (Flights · Hotels · Food & Fun · Transport).

**Popular Destinations panel** — 6 destination quick-pick cards (Tokyo, Paris, Bali, Dubai, Manali, Singapore). Clicking any pre-fills the destination field in the New Trip modal.

**Toast notifications** — bottom-right toast for all user actions.

---

### 🆕 Traveller Profile Page (`profile.html`)

A fully interactive personal travel profile page, accessible from the sidebar under `👤 Profile`.

**Cover hero** — gradient banner with:
- Animated floating globe + plane emoji
- User's display name (italic Playfair Display), bio, location chip, travel role
- Chips showing: Location · Member Since · Continents visited · Trip count
- Avatar circle (first initial) with animated green pulse dot
- Edit Profile button

**Floating stat cards** (overlap the cover, animate up on load):
- Countries Visited · On Wishlist · Places Stamped · Achievements Unlocked

**Countries Visited section** — badge grid split into two sub-grids:
- **Visited** — coral ribbon, flag, country, city, year, hover reveals a ✓ stamp overlay
- **Wishlist** — lavender dashed border, faded, shows `💜 Soon` instead of year
- Add Country modal: flag emoji, country name, city/region, year, status (visited / wishlist)

**World banner** — dark full-width banner showing all visited countries as flag + name chips, with a large country count on the right.

**Places Stamped** — 2-column grid of individual place stamps (e.g. Burj Khalifa, Senso-ji) with:
- Custom emoji, place name, country, date, status pill (Visited / Upcoming / Wishlist)
- Add Place modal to log new stamps

**Achievements system** — 8 badges that **auto-unlock** based on real app data:

| Badge | Unlocks When |
|-------|-------------|
| First Flight | 1+ trip planned |
| Asia Explorer | 3+ Asian countries visited |
| City Hopper | 5+ places stamped |
| Packed & Ready | 1+ trip planned |
| Cartographer | 10+ places stamped |
| Globe Trotter | 10+ countries visited |
| Frequent Flyer | 5+ trips planned |
| Passport Pro | 15+ countries visited |

Locked badges are greyed out. Clicking shows a `🔒 [requirement]` toast. Unlocked badges show a green ✓ badge in the corner.

**Travel Style bars** — animated width percentage bars for: Adventure & Outdoors · Food & Cuisine · Culture & Heritage · Beach & Leisure · Budget Travel.

**Edit Profile modal** — update name, location, travel role, and bio. All saved to `localStorage` under `traveloop_profile` and reflected live on the cover.

---

### 🔄 Updated Backend Routes (`server.py`)

New protected Flask routes added (all redirect to `/` if the user session is missing):

| Route | Function | Template served |
|-------|----------|-----------------|
| `/dashboard` | `dashboard()` | `dashboard.html` |
| `/chatbot` | `chatbot()` | `pr.html` |
| `/todo` | `todo()` | `todolist.html` |
| `/scrap` | `scrap()` | `scrapbook.html` |

The old `homepage.html` is replaced by `dashboard.html` as the post-login landing page.

---

### 🔄 Scrapbook — Flask Integration (`scrapbook.html`)

Now served via the `/scrap` Flask route with full Jinja2 template links:
- Navbar uses `{{ url_for('dashboard') }}`, `{{ url_for('todo') }}`, `{{ url_for('chatbot') }}`
- Image storage upgraded to **IndexedDB** (`MemoryDB` / `memories` store) — images persist across sessions as base64
- Per-card editable text description (auto-saves on input)
- Hover any card to reveal a red `×` delete button in the top-right corner

---

### 🔄 Environment Config — `.env` file added

The app now uses a proper `.env` file (loaded via `python-dotenv`) instead of hardcoded values in `server.py`:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=travelloop
DB_USER=root
DB_PASSWORD=your_password_here

JWT_SECRET=any_long_random_string_here
JWT_REFRESH_SECRET=another_long_random_string

PORT=4000
```

---

## ⚙️ Setup & Running

### Prerequisites
- Node.js & npm
- Python 3.x
- MySQL running locally

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
pip install flask flask-mysqldb flask-bcrypt geopy
```

### 2. Set up MySQL
```sql
CREATE DATABASE travelloop;
USE travelloop;

CREATE TABLE users (
  id CHAR(36) PRIMARY KEY,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  email VARCHAR(255) UNIQUE,
  password_hash VARCHAR(255)
);
```

### 3. Configure your `.env`
Edit the `.env` file in the project root and fill in your MySQL password and JWT secrets.

### 4. Run Flask backend
```bash
python server.py
# Runs at http://localhost:5000
```

### 5. Install Electron deps
```bash
cd static
npm install
```

### 6. Add your Groq API key
In `static/pr.html`, replace:
```js
let apiKey = 'paste your api key here';
```
with your key from [console.groq.com](https://console.groq.com)

### 7. Launch the app
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

## 🗺️ App Routes

```
/              →  auth.html        (login / signup)
/dashboard     →  dashboard.html   (main hub — post login)
/chatbot       →  pr.html          (AI travel assistant)
/todo          →  todolist.html    (itinerary & budget)
/scrap         →  scrapbook.html   (photo memories)
profile.html   →  (static, localStorage-powered — no Flask route needed)
```

---

## 🔒 Security Notes

> ⚠️ Fix these before sharing or pushing to GitHub:

- **MySQL password** is still visible in `server.py` — load it from `.env` using `os.getenv()`
- **Groq API key** is hardcoded in `pr.html` — move it to a Flask proxy endpoint
- **Flask secret key** is `'your_secret_key'` — replace with a strong random value
- **Add `.env` to `.gitignore`** — never commit real credentials

---

## 📄 License

ISC

---

*Built with ✈️ wanderlust and a lot of localStorage.*
