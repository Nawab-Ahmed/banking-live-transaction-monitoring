# Banking Live Transaction Monitoring Dashboard

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.41-orange)](https://www.sqlite.org/index.html)
[![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-green)](https://powerbi.microsoft.com/)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)



## Project Overview
This project simulates how a bank’s operations team monitors live transaction health across multiple channels (ATM, Mobile, Branch, Internet Banking).  
It focuses on **SQL-driven KPIs**, clean **data modeling**, and **operational dashboards**, rather than ML or over-engineering.



## Table of Contents
- [Business Use Case](#-business-use-case)  
- [Architecture](#-architecture)  
- [Key KPIs](#-key-kpis)  
- [Data Model](#-data-model)  
- [Data Quality Checks](#-data-quality-checks)  
- [Dashboard Highlights](#-dashboard-highlights)  
- [How to Run](#-how-to-run)  


## Business Use Case
- Monitor transaction volume in **near real-time**  
- Identify **failure spikes** by hour or channel  
- Track **operational stability** and performance  
- Support **decision-making** for operations and risk teams  


## Architecture
- **Python:** Data generation, ingestion, quality checks  
- **SQLite:** Fact and dimension data model  
- **SQL Views:** KPI logic pushed to database layer  
- **Power BI:** Interactive dashboard via ODBC connection  


## Key KPIs
- Total Transactions  
- Total Transaction Amount  
- Success Rate & Failure Rate  
- Hourly Transaction Trend  
- Channel-wise Performance  


## Data Model
- `fact_transaction`  
- `dim_channel`  
- `dim_customer`  


## Data Quality Checks
- Null checks on critical fields  
- Status validation  
- Duplicate transaction detection  
- Foreign key integrity  


## Dashboard Highlights
- Hourly success vs failure trend  
- Channel-wise transaction amount  
- Failure concentration analysis  
- Filters for **channel** and **customer type**  


## How to Run
```bash
python src/generate_dimensions.py
python src/ingestion.py
python src/create_views.py
