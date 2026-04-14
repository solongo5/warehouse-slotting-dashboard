# Warehouse Slotting Optimization Tool

End-to-end warehouse analytics solution designed to identify SKU misalignment, prioritize relocation actions, and improve picking efficiency and space utilization.

Built using Python, SQL, and Streamlit with simulated operational data.

*Note: This project is based on a real warehouse optimization use case. All data has been anonymized and simulated due to confidentiality requirements.*
---

## 📌 Problem

Warehouse slotting directly impacts picking efficiency, labor cost, and throughput.

In many operations:
- High-demand SKUs are not placed in optimal (Prime) locations  
- Low-priority SKUs occupy valuable picking space  
- No clear prioritization exists for relocation decisions  

This results in:
- Increased travel time  
- Lower picking productivity  
- Inefficient space utilization  

---

## 🎯 Objective

Develop a data-driven tool to:

- Identify misaligned SKUs  
- Prioritize high-impact relocation opportunities  
- Improve warehouse efficiency using ABC classification and movement data  
- Simulate potential operational gains  

---

## ⚙️ Approach

### 1. Data Processing
- SKU-level movement data (~400K records simulated)
- Inventory location mapping
- ABC classification based on demand

### 2. Logic & Analysis
- Defined **slotting mismatch**:
  - Current Location ≠ Optimal Location  
- Identified **high-priority SKUs**:
  - A-class + high movement  
- Ranked relocation candidates based on:
  - Movement frequency (proxy for operational impact)

### 3. KPI Framework
- Total SKUs  
- Misaligned SKUs  
- Misalignment %  
- High-priority segment %  
- Estimated picking time saved  
- Estimated labor cost impact  

### 4. Simulation (Illustrative)
- Assumed:
  - 10 minutes weekly efficiency gain per misaligned SKU  
  - $25/hour labor rate  
- Used to estimate operational impact (not real production data)

---

## 📊 Key Results

- **120 SKUs analyzed**
- **26 SKUs (21.7%) identified as misaligned**
- High-impact opportunities concentrated in:
  - A-class SKUs outside Prime zones  
  - C-class SKUs occupying Prime space  

### Estimated Impact (Illustrative)
- ~4.3 hours/week picking time reduction  
- ~$108/week labor cost savings  

---

## 💡 Key Insights

- A small subset of SKUs drives most operational impact  
- Misplacement of high-movement SKUs creates disproportionate inefficiency  
- Prime storage space is often under-optimized  

---

## 🚀 Solution

The tool provides:

- 🔍 Filterable analysis (ABC class, movement thresholds)  
- 📊 KPI dashboard for quick performance assessment  
- 📈 Ranked relocation recommendations  
- ⚡ Identification of highest-impact moves  
- 📉 Before vs. after optimization simulation  

---

## 🖥️ Dashboard Preview

Key components:
- KPI summary panel  
- Top 10 priority relocation actions  
- A-class critical SKU analysis  
- Before vs. after optimization comparison  
- Zone utilization and ABC distribution charts  

---

## 🧠 Business Value

This solution demonstrates how data can:

- Improve warehouse picking efficiency  
- Reduce operational labor effort  
- Enable data-driven slotting decisions  
- Support scalable warehouse optimization strategies  

---

## ⚠️ Notes

⚠️ Data & Confidentiality

This project is inspired by a real-world warehouse optimization initiative.  
Due to data privacy and confidentiality constraints, all datasets used here are fully simulated and do not represent actual company data.  

The analytical approach, KPI framework, and optimization logic reflect real operational scenarios.
---

## 🛠️ Tech Stack

- Python (Pandas)
- Streamlit
- SQL (data modeling)
- Altair (visualization)

---

## 📌 Author

Solongo Boldtseren  
MSBA Candidate – University of Washington  

Focus: Supply Chain Analytics | Operations Optimization | Data-Driven Decision Making
