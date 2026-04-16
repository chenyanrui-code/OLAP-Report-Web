# Python Report Builder - Visual Analytics Platform

A powerful drag-and-dropBI platform built with Flask and Dash. Create stunning data visualizations without any frontend knowledge.

[简体中文](./README_zh.md) | English

## Live Demo

**URL**: http://106.14.116.252:5000/auth/login

- Email: `123456@qq.com`
- Password: `123456`

---

## Features

| Module | Functionality |
|--------|--------------|
| **User Authentication** | Register, login, session management, independent workspace per user |
| **Data Source Management** | MySQL, PostgreSQL, Excel file upload, connection testing, password encryption |
| **Data Model** | Select tables and fields from data sources, save as virtual datasets |
| **Dashboard** | Drag-and-drop canvas, free layout with resizeable charts |
| **Chart Configuration** | Select data model → choose dimensions/metrics → pick chart type → real-time rendering |
| **Chart Types** | Bar, Line, Area, Pie, Donut, Scatter, Bubble, Histogram, Box Plot, Sunburst, 3D Scatter, Geo Scatter (20+ types) |
| **Layout Persistence** | Each user's dashboard layout is auto-saved to database |

---

## Quick Start

### 1. Requirements

- Python 3.7+

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Application

```bash
python run.py
```

### 4. Access System

Open browser: `http://localhost:5000`

---

## Project Structure

```
PythonReprot/
├── app/
│   ├── __init__.py        # App initialization
│   ├── auth/            # User authentication
│   ├── data_sources/    # Data source management
│   ├── data_models/     # Data model management
│   ├── dashboards/      # Dashboard module
│   ├── charts/          # Chart configuration
│   ├── users/          # User management
│   ├── templates/      # HTML templates
│   └── static/         # Static files
├── config.py           # Configuration
├── requirements.txt   # Dependencies
├── run.py             # Startup script
└── README.md
```

---

## User Guide

### 1. Registration & Login
- Click "Register" to create an account
- Login with registered email and password

### 2. Data Source Management
- Go to "Data Sources" in menu
- Click "Add Data Source"
- Choose type (MySQL/PostgreSQL/Excel)
- Fill in connection info or upload Excel
- Click "Save"

### 3. Create Data Model
- Go to "Data Models" in menu
- Click "Add Data Model"
- Select data source and table
- Check needed fields
- Click "Save"

### 4. Dashboard Design
- Go to "Dashboards" in menu
- Click "Create Dashboard"
- Click "Edit" to enter editor
- Click "+ Add Chart" button
- Choose chart type, data model, dimensions and metrics
- Drag to resize and reposition
- Layout auto-saves

### 5. Chart Configuration
- In dashboard editor, click chart's "Edit" button
- Modify chart name, type, data model, dimensions or metrics
- Preview in real-time
- Click "Save"

---

## Tech Stack

- **Backend**: Flask
- **Visualization**: Dash (Plotly)
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy
- **File Upload**: Flask-Uploads
- **Forms**: Flask-WTF
- **Encryption**: Passlib

---

## Notes

1. **Security**: Change `SECRET_KEY` in `config.py` for production
2. **Performance**: Use PostgreSQL for large datasets
3. **Deployment**: Use Gunicorn + Nginx for production
4. **Extension**: Add more chart types in `app/charts/forms.py`

---

## License

MIT License

---

**Author**: chenyanrui (陈彦睿)