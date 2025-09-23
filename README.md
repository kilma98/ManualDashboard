# La Ferme Urbaine – Measurement Dashboard

This project is a web application for monitoring environmental measurements (temperature, humidity, water temperature) collected from users. It provides a **FastAPI backend**, a **PostgreSQL database**, and a **Streamlit dashboard** for admins to visualize the data per user.

---

## Features

- Store temperature, humidity, and water temperature measurements per user.
- REST API endpoints to create and retrieve measurements.
- Streamlit dashboard with graphs for each user.
- User authentication and role-based access (admin vs regular user).

---

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Frontend Dashboard**: Streamlit
- **Authentication**: JWT tokens
- **Environment management**: `.env` file for configuration

---

## Setup

### 1. Clone repository

```bash
git clone <repository_url>
cd ManualDashboard
