# Warehouse Slotting Optimization Tool

Data-driven warehouse slotting optimization tool built with Python and Streamlit to identify SKU misalignment and relocation opportunities.

## Overview
This project demonstrates how warehouse inventory data can be analyzed to support slotting decisions and improve space utilization. The tool highlights SKUs that are not in their optimal locations and prioritizes relocation opportunities based on movement and SKU class.

## Problem
Warehouse slotting is often not fully aligned with SKU demand patterns, which can lead to inefficient placement, unnecessary travel, and poor use of prime storage zones.

## Approach
- Built a Streamlit-based decision support tool
- Used Python and Pandas to analyze SKU-level slotting data
- Compared current vs. optimal locations
- Flagged relocation candidates
- Prioritized high-movement A-class SKUs

## Key Features
- KPI summary for total SKUs, misaligned SKUs, and misalignment rate
- Relocation candidate identification
- Priority SKU filtering
- Simple interactive dashboard for operational review

## Files
- `kdp_slotting_optimization.py` — main Streamlit application
- `data.csv` — simulated dataset for public demonstration
- `README.md` — project documentation

## Tools Used
- Python
- Pandas
- Streamlit

## Data Note
This public version uses simulated/anonymized data. Original company data is confidential and not included.
