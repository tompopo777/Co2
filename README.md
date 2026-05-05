# Carbon Emission Inventory System

A Django-based web application designed to help organizations record, manage, and report carbon emission inventory data, supporting standardized carbon accounting and audit processes.

## Features

- Record and manage carbon emission inventory data  
- Online data entry with support for records, images, and text  
- Emission calculation based on:
  - GHG Protocol  
  - ISO 14064-1  
  - ISO 14067  
- Import and export data via CSV  
- Generate emission reports for auditing and compliance  
- Centralized system for tracking and organizing emission-related information  

## Tech Stack

- Python
- Django
- MariaDB
- Pandas
- HTML / CSS / JavaScript / Bootstrap

## Project Structure

```text
carbon-emission-inventory-system/
├── apps/                 # Django apps, templates, static files, and business logic
├── core/                 # Django settings, URLs, and WSGI configuration
├── media/                # Project media/images
├── nginx/                # Nginx configuration for deployment
├── Dockerfile            # Docker image setup
├── docker-compose.yml    # Container orchestration setup
├── env.sample            # Example environment variables
├── gunicorn-cfg.py       # Gunicorn production server config
├── manage.py             # Django command-line utility
├── requirements.txt      # Python dependencies
└── README.md
