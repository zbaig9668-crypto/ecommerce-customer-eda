# E-commerce Customer Behavior & Purchase Pattern Analysis

This project explores customer engagement and yearly purchase spending using the supplied e-commerce customer dataset. It includes a Jupyter notebook for exploratory data analysis and a Streamlit dashboard for interactive exploration.

## Files
- `ecommerce_customers.csv` — source dataset (500 rows, 8 columns)
- `ecommerce_customer_analysis.ipynb` — step-by-step analysis, charts, question answers, and conclusion
- `app.py` — Streamlit dashboard
- `requirements.txt` — Python dependencies

## Three key findings
1. The dataset contains **500 customers** and **8 columns**.
2. Average yearly spending is **$499.31**.
3. The strongest numeric relationship with yearly spending is **Length of Membership** (based on absolute Pearson correlation).

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Live app
Add your deployed Streamlit URL here after deployment: `PASTE_YOUR_STREAMLIT_APP_LINK_HERE`

## Dataset
The CSV was provided for this project and is included in the repository as `ecommerce_customers.csv`.
