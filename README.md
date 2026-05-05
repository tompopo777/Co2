# 🌱🌎 Carbon Emission Inventory System

A Django-based system designed to help organizations manage carbon emission inventory data, supporting standardized carbon accounting, compliance, and audit reporting.

## 🚀 Features

- Record and manage carbon emission inventory data  
- Online data entry (records, images, text)  
- Emission calculation based on GHG Protocol, ISO 14064-1, and ISO 14067  
- Import and export data via CSV  
- Generate reports for audit and compliance  
- Centralized system for tracking emission-related information  

## 🛠 Tech Stack

- Python
- Django
- MariaDB
- Pandas (data processing)
- HTML / CSS / JavaScript / Bootstrap

## 📁 Project Structure

```text
carbon-emission-inventory-system/
├── apps/                 # Django apps, templates, static files, and business logic
├── core/                 # Django settings, URLs, and WSGI configuration
├── media/                # Project media/images
├── nginx/                # Nginx configuration for deployment
├── Dockerfile            # Docker image setup
├── env.sample            # Example environment variables
├── gunicorn-cfg.py       # Gunicorn production server config
├── manage.py             # Django command-line utility
├── requirements.txt      # Python dependencies
└── README.md
```

## 📸 Screenshots

### 📊 Dashboard
<p align="center">
  <img src="media/Images/dashboard_1.png" width="800" alt="dashboard_1.png"/>
</p>
<p align="center">
  <img src="media/Images/dashboard_2.png" width="800" alt="dashboard_2.png"/>
</p>

### 📝 Emission Entry Form
<p align="center">
  <img src="media/Images/emission_entry_form.png" width="800" alt="emission_entry_form.png"/>
</p>

### 📈 Summary Table
<p align="center">
  <img src="media/Images/emission_calculation.png" width="800" alt="emission_calculation.png"/>
</p>

### 📄 Report Generation and Export
<p align="center">
  <img src="media/Images/gen_report_1.png" width="800" alt="gen_report_1.png"/>
</p>

<p align="center">
  <img src="media/Images/gen_report_2.png" width="800" alt="gen_report_2.png"/>
</p>
