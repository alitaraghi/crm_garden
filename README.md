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

## Design decisions & business rules

### Data model and ownership

Each core model (`Client`, `Project`, and `Task`) has an explicit `owner` field that points to the Django user model.  
This makes it easy to enforce per-user data isolation in queries and views, so each user only sees and manages their own CRM data.

Clients, projects, and tasks are linked in a simple hierarchy:

- A user has many clients.
- A client has many projects.
- A project has many tasks.

This structure is intentionally straightforward so that it clearly demonstrates relational modeling and query patterns in Django.

### Status and priority

Projects and tasks use explicit status and priority choices instead of free-text fields.  
This keeps the data consistent and allows for simple filtering and reporting in list views and on the dashboard.

Examples:

- Project statuses: planned, in progress, on hold, completed, cancelled.
- Task statuses: to do, in progress, done, blocked.
- Task priorities: low, medium, high.

### Business rules

Some small but realistic business rules are implemented to make the CRM behave more like a real-world tool:

- Projects with a status of `completed` or `cancelled` cannot be deleted from the UI.  
  This prevents accidentally deleting historical records for finished work.

- Overdue tasks (tasks with a due date in the past and not marked as done) are visually highlighted in tables.  
  This helps the user quickly see which items need attention.

These rules are intentionally simple but show how domain logic can be enforced both in the view layer and in the templates.

### Testing

The project includes a small but focused test suite:

- Ownership tests for list views (clients, projects, tasks) to ensure a user only sees their own data.
- Dashboard tests to verify that counts and overdue tasks are calculated from the correct queryset.
- View tests for project deletion rules and task creation, confirming that:
  - Protected projects are not deleted.
  - Newly created tasks are automatically linked to the correct project and owner.

The goal is to demonstrate a pragmatic approach to testing: covering critical paths and business rules rather than aiming for 100% cove

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
##  Project Status
This project is under active development as part of a personal learning and portfolio journey.
New features are added incrementally with a focus on clean code, small commits, and clear documentation.