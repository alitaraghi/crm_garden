# CRM Garden

CRM Garden is a small but realistic **client & project CRM** built with Django.  
It is designed as a portfolio project to demonstrate full‑stack Django skills and a basic understanding of the software development lifecycle (SDLC).

## Project Overview

The main idea behind CRM Garden is that each client is like a plant in a garden.  
The application helps a solo developer or small team to keep track of clients, their projects, and the tasks that need to be completed for each project.

The initial goal is to provide:

- A clean data model for clients, projects, and tasks.
- A simple, usable web UI built with Django and Bootstrap.
- Basic authentication and per‑user data isolation.

## Features

Current features:

- User‑owned clients (each user sees only their own data).
- Full CRUD for clients (list, create, view, update, delete).
- Admin interface for managing clients, projects, and tasks.

Planned features (MVP):

- Projects linked to clients, with status and dates.
- Tasks linked to projects, with status and priority.
- Simple dashboard/overview page with basic statistics.
- Basic filters on lists (by status, priority, etc.).
- A small test suite for critical views and permissions.

Possible future enhancements:

- More advanced reporting and dashboard widgets.
- Simple automation (e.g. marking projects as completed when all tasks are done).
- Better onboarding and user management.

## Tech Stack

- Python
- Django
- SQLite for local development (can be swapped to PostgreSQL in production)
- Bootstrap for basic styling

## Getting Started

### Prerequisites

- Python 3.x
- `pip` for installing dependencies

### Installation

```bash
git clone https://github.com/alitaraghi/crm_garden.git
cd crm_garden

python -m venv .venv
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

pip install -r requirements.txt
Running the project
Apply migrations and create a superuser:
```
```bash
python manage.py migrate
python manage.py createsuperuser
Run the development server:
```
```bash
python manage.py runserver
Then open http://127.0.0.1:8000/clients/ in your browser and log in with your superuser account.
```
Project Status
This project is under active development as part of a personal learning and portfolio journey.
New features are added incrementally with a focus on clean code, small commits, and clear documentation.