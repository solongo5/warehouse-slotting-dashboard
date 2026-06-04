# Warehouse Slotting Optimization Tool

🔗 Live Demo: https://warehouse-slotting-dashboard-d7mn4sgqs5bx9fdnp2wmei.streamlit.app

💻 GitHub: https://github.com/solongo5/warehouse-slotting-dashboard

Interactive warehouse slotting optimization dashboard built with SQL, Python, and Streamlit to identify inventory misalignment, prioritize relocation opportunities, and support data-driven warehouse decision making.

> **Note:** This project is based on a real warehouse optimization use case. All data has been anonymized and simulated due to confidentiality requirements.

---

# Business Problem

Warehouse slotting directly impacts picking efficiency, labor utilization, and throughput.

In many warehouse environments:

* High-demand SKUs are not stored in optimal locations
* Prime picking locations are occupied by lower-priority inventory
* Relocation decisions are often reactive rather than data-driven
* No standardized prioritization exists for warehouse re-slotting

These conditions can increase picker travel time, reduce productivity, and limit warehouse efficiency.

---

# Objective

Develop a data-driven warehouse slotting solution to:

* Identify inventory location misalignment
* Classify inventory based on business importance and movement velocity
* Prioritize relocation opportunities
* Recommend optimal warehouse zones
* Support warehouse decision-making through interactive dashboards

---

# Methodology

## 1. Data Preparation

Warehouse inventory, location, and movement data were processed using Azure SQL and Python.

Key datasets included:

* Inventory master data
* Warehouse location assignments
* Material movement history
* Stock quantities
* Warehouse zone definitions

---

## 2. ABC Classification

SKUs were classified according to outbound inventory contribution.

### A Class

Highest-value inventory contributing the largest share of outbound volume.

### B Class

Moderate-value inventory.

### C Class

Lower-value inventory with reduced operational impact.

This classification helps prioritize warehouse space allocation based on business value.

---

## 3. Speed Classification

Movement velocity was calculated using historical outbound transactions.

### Fast

40+ issue events

### Medium

10–39 issue events

### Slow

Fewer than 10 issue events

This approach identifies which products are picked most frequently.

---

## 4. Slotting Logic

ABC classification and movement velocity were combined to determine recommended warehouse placement.

| ABC | Speed  | Recommended Zone |
| --- | ------ | ---------------- |
| A   | Fast   | Prime            |
| A   | Medium | Prime            |
| B   | Fast   | Prime            |
| B   | Medium | Secondary        |
| C   | Slow   | Reserve          |

This allows warehouse space to be aligned with operational demand and picking frequency.

---

# Key Results

Using simulated warehouse inventory and movement data modeled after a real distribution center use case:

* 281 finished-goods SKUs analyzed
* 5,617 warehouse storage bins represented
* 423K historical movement records simulated
* 59 relocation candidates identified (21.0% of inventory)
* 11 A-class SKUs found outside Prime picking zones
* 37 lower-priority SKUs occupying Prime warehouse space
* Estimated 9.8 labor hours saved per week through targeted re-slotting
* Estimated labor impact of approximately $246 per week (based on a $25/hr labor rate)

These findings demonstrate how inventory segmentation and slotting optimization can identify high-impact relocation opportunities without requiring a full warehouse redesign.

---

# Dashboard Features

## Executive KPI Dashboard

Tracks:

* Total SKUs analyzed
* Relocation candidates
* Relocation percentage
* Total warehouse storage bins
* Historical movement records
* Facility size (sq ft)
* Estimated labor savings
* Estimated labor cost impact

---

## Relocation Prioritization

Identifies:

* High-priority relocation candidates
* A-class inventory outside Prime zones
* Prime-space utilization opportunities

Includes:

* Top relocation opportunities
* Priority-based ranking
* Actionable relocation recommendations

---

## Warehouse Bin Map

Interactive warehouse visualization displaying:

* Prime, Secondary, and Cold storage zones
* Inventory distribution by classification
* Available and occupied locations
* Relocation opportunities

Provides a visual representation of warehouse slotting decisions.

---

## Optimization Insights

Highlights:

* Inventory placement inefficiencies
* Prime zone utilization opportunities
* High-impact relocation candidates
* Estimated operational improvements

---

# Technology Stack

### Data Engineering

* Azure SQL
* SQL Views
* Data Modeling

### Analytics

* Python
* Pandas
* NumPy

### Visualization

* Streamlit
* Plotly
* Interactive Dashboards

### Supply Chain Techniques

* ABC Analysis
* Velocity Analysis
* Slotting Optimization
* Warehouse Analytics
* Inventory Segmentation

---

# Project Architecture

1. Extract inventory and movement data
2. Calculate ABC classifications
3. Calculate movement velocity classifications
4. Generate slotting recommendations
5. Identify relocation candidates
6. Prioritize opportunities by operational impact
7. Visualize insights through interactive dashboards

---

# Business Impact

The solution provides a repeatable framework for warehouse slotting analysis and relocation prioritization.

Potential operational benefits include:

* Improved placement of high-priority inventory
* Better utilization of Prime picking locations
* Reduced picker travel distance
* Increased visibility into warehouse slotting inefficiencies
* Data-driven relocation prioritization
* Estimated labor savings through targeted inventory re-slotting

Rather than recommending large-scale warehouse redesigns, the solution focuses on identifying the relatively small percentage of SKUs that create the greatest operational impact.

---

# Repository Structure

```text
warehouse-slotting-dashboard/
│
├── app.py
├── data.csv
├── requirements.txt
├── README.md
│
└── dashboard.png
```

---

# Disclaimer

This project is intended for portfolio and educational purposes only.

The original business use case was adapted from a warehouse optimization project. All data, identifiers, and operational details have been anonymized and simulated to protect confidential information.
