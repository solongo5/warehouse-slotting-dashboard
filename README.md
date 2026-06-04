# Warehouse Slotting Optimization Tool

🔗 Live Demo: https://warehouse-slotting-dashboard-d7mn4sgqs5bx9fdnp2wmei.streamlit.app

💻 GitHub: https://github.com/solongo5/warehouse-slotting-dashboard

This project is an interactive warehouse slotting optimization tool built with Azure SQL, Python, and Streamlit. The goal was to identify inventory-location misalignment, prioritize relocation opportunities, and help warehouse teams make better slotting decisions using data.

The project is based on a real warehouse optimization use case. All data has been anonymized and simulated for confidentiality.

## Why I Built This
With 9+ years of experience in supply chain and procurement, I've seen how warehouse layouts and inventory placement decisions can directly impact operational efficiency. I built this project to combine my warehouse operations background with analytics and demonstrate how inventory segmentation and movement data can be used to identify practical relocation opportunities and improve warehouse performance.


## The Problem

In many warehouses, inventory locations evolve over time as products are added, moved, and replenished. As a result, high-volume SKUs are not always stored in the most efficient picking locations, while lower-priority items may occupy valuable space near shipping and picking areas.

These issues can increase picker travel time, reduce productivity, and make relocation decisions difficult to prioritize.

## My Approach

I combined ABC inventory classification with SKU movement velocity to evaluate whether products were stored in appropriate warehouse zones.

The workflow included:

* Processing inventory, location, and movement data in Azure SQL
* Classifying SKUs based on outbound volume (ABC analysis)
* Calculating movement velocity using historical issue transactions
* Recommending warehouse zones based on inventory importance and activity levels
* Identifying inventory that should be relocated
* Visualizing results through an interactive Streamlit dashboard

## Slotting Logic

Inventory was classified using both business importance and movement frequency.

| ABC Class | Velocity | Recommended Zone |
| --------- | -------- | ---------------- |
| A         | Fast     | Prime            |
| A         | Medium   | Prime            |
| B         | Fast     | Prime            |
| B         | Medium   | Secondary        |
| C         | Slow     | Reserve          |

This approach helps ensure that the most frequently picked and highest-impact products are stored in the most accessible warehouse locations.

## Results

Using simulated data modeled after a real warehouse environment:

* 281 finished-goods SKUs analyzed
* 5,617 warehouse storage bins evaluated
* 423,000 historical movement records processed
* 59 relocation candidates identified (21% of inventory)
* 11 A-class SKUs found outside Prime picking zones
* 37 lower-priority SKUs occupying Prime warehouse space
* Estimated labor savings of 9.8 hours per week
* Estimated labor cost reduction of approximately $246 per week

The analysis showed that a relatively small number of inventory moves could improve slotting efficiency without requiring a major warehouse redesign.

## Dashboard Features

### Executive Summary

Provides a high-level view of:

* SKU counts
* Relocation opportunities
* Warehouse capacity metrics
* Movement history
* Estimated labor savings

### Relocation Prioritization

Highlights:

* High-priority relocation candidates
* A-class inventory outside Prime zones
* Prime-space utilization opportunities
* Recommended actions ranked by impact

### Warehouse Bin Map

Interactive warehouse visualization showing:

* Prime, Secondary, and Reserve storage zones
* Inventory distribution
* Occupied and available locations
* Potential relocation opportunities

## Technology Stack

**Data & Analytics**

* Azure SQL
* SQL Views
* Python
* Pandas
* NumPy

**Visualization**

* Streamlit
* Plotly

**Supply Chain Methods**

* ABC Analysis
* Velocity Analysis
* Warehouse Slotting Optimization
* Inventory Segmentation

## Repository Structure

warehouse-slotting-dashboard/

├── app.py

├── data.csv

├── requirements.txt

└── README.md

## Disclaimer

This project was created for portfolio and educational purposes. The original business scenario was adapted from a warehouse optimization project, and all data and operational details have been anonymized and simulated.
