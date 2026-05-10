# MyOS — Personal Life Operating System
> A Python + FastAPI web application that serves as your personal OS — managing your finances, time, health, life admin, and learning in one place.

---

## 1. Project Overview

**Name:** MyOS  
**Stack:** Python, FastAPI, PostgreSQL, SQLAlchemy, Pydantic  
**Type:** REST API backend + Web frontend  
**Auth:** JWT (single user for now, multi-user ready architecture)  
**Goal:** A personal dashboard that gives you a 30-second snapshot of your life — money, focus, health, learning, and admin — all in one place.

---

## 2. Modules

### 2.1 Finance
Track income, expenses, budgets, and spending trends.

**Features:**
- Log transactions (income / expense) with category, amount, date, and notes
- Define monthly budgets per category
- Dashboard summary — total spent this month, remaining budget per category
- Spending trends — monthly breakdown by category
- Categories — food, rent, transport, entertainment, subscriptions, etc.

**Key entities:** `Transaction`, `Category`, `Budget`

---

### 2.2 Life Admin
Never forget a renewal, subscription, or important document deadline.

**Features:**

**Subscriptions tracker:**
- Track all subscriptions (Netflix, Spotify, gym, etc.)
- Store name, cost, billing cycle (monthly/yearly), renewal date
- Alert when a subscription renews within 7 days
- Total monthly/yearly subscription cost summary

**Document vault:**
- Store document metadata (passport, insurance, ID, visa, etc.)
- Track expiry dates
- Alert when a document expires within 30 days

**Wishlist / Purchase planner:**
- Add items you want to buy with estimated price
- Mark as saved toward or purchased
- Priority levels (low / medium / high)

**Key entities:** `Subscription`, `Document`, `WishlistItem`

---

### 2.3 Focus (Pomodoro)
Beat phone addiction and track your deep work time.

**Features:**
- Start a Pomodoro session (25 min work / 5 min break, configurable)
- Tag sessions with a project or task label
- Log completed sessions with start time, end time, and duration
- Daily and weekly deep work summary
- Set a daily focus goal (e.g. 4 Pomodoros per day) and track progress

**Key entities:** `PomodoroSession`, `FocusGoal`

---

### 2.4 Health
Simple daily tracking for water and sleep.

**Features:**

**Water tracker:**
- Log water intake entries throughout the day (amount in ml)
- Set daily water goal
- Progress bar toward daily goal
- Weekly average intake

**Sleep tracker:**
- Log sleep entries (bed time, wake time, quality rating 1-5, notes)
- Calculate sleep duration automatically
- Weekly average sleep duration and quality

**Key entities:** `WaterEntry`, `SleepEntry`

---

### 2.5 Learning
Track what you're learning and retain it better.

**Features:**

**Flashcards (Spaced Repetition):**
- Create decks and cards (front / back)
- Review cards and rate confidence (easy / medium / hard)
- Spaced repetition algorithm — show hard cards more often
- Track review history and deck progress

**Book Tracker:**
- Add books (title, author, genre)
- Track status (want to read / reading / finished)
- Log reading sessions with pages read
- Add notes and highlights per book

**Course / Skill Tracker:**
- Add courses or skills you're learning
- Track progress percentage
- Log study sessions with duration and notes

**Key entities:** `Deck`, `Card`, `CardReview`, `Book`, `ReadingSession`, `Course`, `StudySession`

---

## 3. Dashboard (Home Screen)

The main screen surfaces the most important snapshot from each module:

| Widget | What it shows |
|---|---|
| Finance | Spent this month vs budget |
| Focus | Today's Pomodoros vs daily goal |
| Water | Today's intake vs goal |
| Sleep | Last night's sleep duration and quality |
| Life Admin | Subscriptions renewing this week + documents expiring soon |
| Learning | Current book progress + cards due for review today |

---

## 4. Data Model (High Level)

```
users
├── transactions         (finance)
├── categories           (finance)
├── budgets              (finance)
├── subscriptions        (life admin)
├── documents            (life admin)
├── wishlist_items       (life admin)
├── pomodoro_sessions    (focus)
├── focus_goals          (focus)
├── water_entries        (health)
├── sleep_entries        (health)
├── decks                (learning - flashcards)
│   └── cards
│       └── card_reviews
├── books                (learning)
│   └── reading_sessions
└── courses              (learning)
    └── study_sessions
```

---

## 5. API Structure

```
/auth
  POST /register
  POST /login
  POST /refresh

/dashboard
  GET /                  → summary of all modules

/finance
  GET    /transactions
  POST   /transactions
  PUT    /transactions/{id}
  DELETE /transactions/{id}
  GET    /budgets
  POST   /budgets
  GET    /categories

/life-admin
  GET    /subscriptions
  POST   /subscriptions
  PUT    /subscriptions/{id}
  DELETE /subscriptions/{id}
  GET    /documents
  POST   /documents
  GET    /wishlist
  POST   /wishlist
  PUT    /wishlist/{id}

/focus
  GET    /sessions
  POST   /sessions/start
  PUT    /sessions/{id}/complete
  GET    /goals
  POST   /goals

/health
  GET    /water
  POST   /water
  GET    /sleep
  POST   /sleep

/learning
  GET    /decks
  POST   /decks
  GET    /decks/{id}/cards
  POST   /decks/{id}/cards
  GET    /cards/due          → cards due for review today
  POST   /cards/{id}/review
  GET    /books
  POST   /books
  POST   /books/{id}/sessions
  GET    /courses
  POST   /courses
  POST   /courses/{id}/sessions
```

---

## 6. Tech Stack Details

| Layer | Technology | Reason |
|---|---|---|
| Language | Python 3.11+ | Daily work language, faster to build |
| Framework | FastAPI | Modern, async, auto docs, Pydantic native |
| Database | PostgreSQL | Relational, production grade |
| ORM | SQLAlchemy 2.0 | Industry standard for Python |
| Validation | Pydantic v2 | Already familiar from work |
| Auth | JWT (python-jose) | Already built one before in Java |
| Migrations | Alembic | Standard with SQLAlchemy |
| Testing | Pytest | Standard Python testing |
| Containerization | Docker | On your learning roadmap, good first real use |

---

## 7. Project Structure

```
myos/
├── app/
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Settings and env vars
│   ├── database.py              # DB connection and session
│   ├── models/                  # SQLAlchemy models
│   │   ├── finance.py
│   │   ├── life_admin.py
│   │   ├── focus.py
│   │   ├── health.py
│   │   └── learning.py
│   ├── schemas/                 # Pydantic schemas (request/response)
│   │   ├── finance.py
│   │   ├── life_admin.py
│   │   ├── focus.py
│   │   ├── health.py
│   │   └── learning.py
│   ├── routers/                 # API route handlers
│   │   ├── finance.py
│   │   ├── life_admin.py
│   │   ├── focus.py
│   │   ├── health.py
│   │   ├── learning.py
│   │   └── dashboard.py
│   ├── services/                # Business logic layer
│   │   ├── finance.py
│   │   ├── life_admin.py
│   │   ├── focus.py
│   │   ├── health.py
│   │   └── learning.py
│   └── auth/                    # JWT auth
│       ├── router.py
│       ├── service.py
│       └── dependencies.py
├── alembic/                     # Database migrations
├── tests/                       # Pytest tests
├── .env                         # Environment variables
├── docker-compose.yml           # Docker setup
├── Dockerfile
└── requirements.txt
```

---

## 8. Architecture Pattern

**Layered architecture** — the same pattern you learned in Spring Boot, applied in Python:

```
Request → Router (controller) → Service (business logic) → Repository/ORM (data) → Database
```

- **Router** — handles HTTP, validates input via Pydantic schemas, calls service
- **Service** — all business logic lives here (budget calculations, spaced repetition, streaks)
- **Model** — SQLAlchemy database models
- **Schema** — Pydantic models for request/response validation

This is the same separation of concerns as your Spring Boot layered architecture — just Python names instead of Java names.

---

## 9. Build Order (Recommended)

Build one module at a time, end to end, before moving to the next. This way you always have something working.

1. **Project setup** — FastAPI, PostgreSQL, Docker, JWT auth
2. **Finance module** — most useful, good first real module
3. **Life Admin** — subscriptions first, then documents, then wishlist
4. **Focus / Pomodoro** — simpler logic, quick win
5. **Health** — water and sleep, very straightforward
6. **Learning** — most complex (spaced repetition algorithm), save for last
7. **Dashboard** — wire everything together into the home screen
8. **Frontend** — simple web UI on top of the API

---

## 10. Spaced Repetition Algorithm (Learning Module)

This is the most interesting logic in the app. The idea is simple:

- When you review a card, you rate it: **Easy / Medium / Hard**
- **Easy** → show again in 7 days
- **Medium** → show again in 3 days
- **Hard** → show again tomorrow
- Cards with no review or overdue reviews appear in today's queue

Start with this simple version. Later you can implement the SM-2 algorithm (the algorithm Anki uses) which adjusts intervals dynamically based on your history.

---

## 11. Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/myos
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## 12. Future Ideas (Post MVP)

- Mobile app (React Native or Flutter) — same API, new frontend
- Multi-user support — scope all queries by user_id (already in the architecture)
- Notifications — email or push alerts for document expiry, subscription renewals
- Data export — export finance data to CSV
- AI insights — weekly summary of spending patterns, focus trends, sleep quality
- Browser extension — quick add transactions or start a Pomodoro from anywhere
