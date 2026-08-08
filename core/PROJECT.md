# GlavRyba AI

## Статус проекта

Текущая версия:
- Version: 1.0.0
- Build: 001

---

## Цель

GlavRyba AI — единая система управления сетью ресторанов.

Система включает:

- Telegram Bot
- PostgreSQL
- AI Assistant
- Аналитика
- Финансы
- Склады
- Персонал
- IIKO
- Dashboard

---

# Архитектура

Telegram
↓
Routers
↓
Handlers
↓
Services
↓
Repositories
↓
PostgreSQL

---

# Структура проекта

bot/
config/
core/
database/
modules/
docs/
logs/
tests/

---

# Правила проекта

1. SQL только в Repository.
2. Вся логика только в Service.
3. Handler только принимает запрос.
4. Один модуль — одна ответственность.
5. После каждого Sprint проект должен запускаться.

---

# Sprint

✅ Sprint 0
- Git
- GitHub
- PostgreSQL
- Logger
- Version

🔄 Sprint 1
- BaseRepository
- Middleware
- Dependency Injection

⏳ Sprint 2
- Restaurants

⏳ Sprint 3
- Staff

⏳ Sprint 4
- Warehouse

⏳ Sprint 5
- Finance

⏳ Sprint 6
- Analytics

⏳ Sprint 7
- IIKO

⏳ Sprint 8
- AI

---

# Основная ветка

main

# Ветка разработки

develop