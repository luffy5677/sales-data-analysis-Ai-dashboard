# Sales Data Analysis and AI-Powered Insights Dashboard

A beginner-friendly end-to-end sales analytics portfolio project using Python, Pandas, NumPy-compatible data workflows, Plotly, Streamlit, SQLite SQL, and an optional LLM narrative feature. The core dashboard and rule-based insights work without an API key.

## Business problem

Sales teams need a quick way to understand revenue, profit, order volume, product/category performance, regional results, customer segments, and discount patterns. This project cleans a realistic sample dataset, calculates KPIs, provides interactive filters, and translates calculated results into cautious business recommendations.

## Technology stack

- Python 3.10+
- Pandas and NumPy (NumPy is a transitive/common analytical dependency; core calculations use Pandas)
- Matplotlib and Seaborn listed for further exploratory analysis
- Plotly for interactive charts
- Streamlit for the dashboard
- SQLite SQL for reusable business queries
- Optional OpenAI-compatible chat-completions API for narrative summaries
- pytest for automated tests

## Dataset

`sales_data.csv` contains 1,500 generated source rows and includes intentional exact duplicate rows and missing values for cleaning practice. Fields: Order ID, Order Date, Product Name, Product Category, Sales Amount, Quantity, Profit, Region, Customer Name, Customer Segment, Discount, Payment Method. The dashboard cleans the data before analysis. The exact number of usable rows can vary with the deterministic generator's injected data-quality issues.

The sample is synthetic and must not be presented as real company sales.

## Project architecture

```text
Sales_Data_Analysis_AI_Dashboard/
├── app.py
├── requirements.txt
├── README.md
├── sales_data.csv
├── .env.example
├── .gitignore
├── data/
│   └── generate_dataset.py
├── src/
│   ├── __init__.py
│   ├── data_cleaning.py
│   ├── sales_analysis.py
│   ├── visualizations.py
│   └── ai_insights.py
├── sql/
│   └── sales_analysis_queries.sql
├── reports/
│   └── sample_business_insights.md
├── tests/
│   └── test_analysis.py
└── screenshots/
    └── README.md
```

## Windows installation

Open PowerShell in the project folder.

### 1. Install Python

Install Python 3.10 or newer from the official Python website and enable **Add Python to PATH** during setup.

### 2. Create and activate a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt instead:
```bat
.venv\Scripts\activate.bat
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Generate or refresh the dataset

```powershell
python data\generate_dataset.py
```

This writes `sales_data.csv` in the project root. The generator uses a fixed seed so it is reproducible.

### 5. Run the dashboard

```powershell
streamlit run app.py
```

Streamlit prints a local URL, usually `http://localhost:8501`. Open it in your browser.

### 6. Run tests

```powershell
python -m pytest -q
```

## Dashboard guide

- **Overview:** KPI cards, monthly revenue, monthly revenue/profit, yearly table, latest month-over-month growth.
- **Products & Categories:** top products, profit by category, lowest-profit products, discount-band profit.
- **Regions & Customers:** regional revenue and customer-segment revenue.
- **AI Insights:** calculated rule-based findings and recommendations; optional LLM-written summary button.
- **Data & Export:** inspect filtered rows and download filtered data or a KPI summary as CSV.
- Sidebar filters: date range, region, category, customer segment, and product. Charts and KPIs use the filtered data.

Revenue is the sum of Sales Amount. Profit is the sum of Profit. Orders are distinct Order IDs. Average order value is revenue divided by distinct orders. Profit margin is profit divided by revenue; when revenue is zero it safely returns 0%.

## SQL queries with SQLite

### Option A: DB Browser for SQLite

1. Install DB Browser for SQLite.
2. Create a database named `sales.db`.
3. Import `sales_data.csv` as a table named `sales`.
4. Ensure the column names remain unchanged and `Order Date` uses `YYYY-MM-DD`.
5. Open `sql/sales_analysis_queries.sql`, copy a query into the Execute SQL tab, and run it.

Import the raw CSV to explore source-data issues, or import a cleaned export from the dashboard for cleaner reporting.

### Option B: Python quick import

From the project root:
```powershell
python -c "import sqlite3,pandas as pd; c=sqlite3.connect('sales.db'); pd.read_csv('sales_data.csv').to_sql('sales',c,if_exists='replace',index=False); c.close(); print('Imported sales_data.csv into sales.db')"
```
Then use a SQLite client to execute the queries in `sql/sales_analysis_queries.sql`.

Queries included: total revenue/profit, monthly trends, top 10 products, regional performance, customer segmentation, profitable categories, and low-performing products.

## Optional LLM setup

The app's calculated rule-based insights work without any API key. To enable the optional LLM summary:

1. Copy `.env.example` to `.env`.
2. Add a valid provider API key to `LLM_API_KEY`, and set `LLM_MODEL` / `LLM_BASE_URL` if needed.
3. Install the optional client:
   ```powershell
   pip install openai
   ```
4. Restart Streamlit and click **Generate optional LLM executive summary** in AI Insights.

Never commit `.env` or real secrets. `.gitignore` excludes `.env`. The optional call sends aggregated insight text to the configured provider. Provider pricing, model access, and network availability are outside this project's control. If the client is missing, key is absent, or request fails, the app continues to provide rule-based insights.

## Common errors

- **`python` or `py` not found:** reinstall Python and enable PATH, then reopen the terminal.
- **`streamlit` not found:** activate `.venv` and run `pip install -r requirements.txt`.
- **PowerShell script execution disabled:** use Command Prompt activation command shown above, or follow your organization's approved policy.
- **Missing columns:** preserve the required CSV column names; see `src/data_cleaning.py`.
- **No rows match filters:** reset filters or broaden the date range.
- **LLM unavailable:** rule-based mode still works; check API key, model, client installation, network, and provider permissions.
- **Port in use:** run `streamlit run app.py --server.port 8502`.

## Upload to GitHub

1. Create an empty repository on GitHub.
2. From the project folder:
   ```powershell
   git init
   git add .
   git commit -m "Build sales analytics and AI insights dashboard"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
   git push -u origin main
   ```
3. Replace the placeholder repository URL with your own repository URL.
4. Never commit `.env`, API keys, private customer data, or confidential business data.

## Business meaning of the main analyses

- **Revenue / profit:** shows sales volume and the money remaining after the costs represented by the Profit field.
- **Orders / units / average order value:** shows transaction volume, product volume, and average sales per distinct order.
- **Monthly / yearly trends and growth:** helps spot seasonality and changes over time; compare like-for-like periods when possible.
- **Product and category rankings:** helps identify sales leaders and profit contributors.
- **Regional performance:** supports geographic comparison and follow-up questions about market coverage.
- **Customer segments:** shows which segment contributes revenue and profit.
- **Discount vs. profit:** helps inspect whether higher-discount transactions coincide with lower profit; correlation is not causation.
- **Low-performing products:** identifies products for investigation, not automatic removal.

## Resume-ready project materials

### Project description
Built an end-to-end Sales Data Analysis and AI-Powered Insights Dashboard using Python, Pandas, SQL, Plotly, and Streamlit to clean sales data, calculate business KPIs, explore product/region/customer performance, and generate rule-based recommendations with optional LLM-written summaries.

### Resume bullet points
Use these only after you run the project and can discuss it honestly:
- Developed a Streamlit dashboard with interactive date, region, category, segment, and product filters.
- Built a Pandas data-cleaning pipeline to remove exact duplicates, parse dates, validate numeric fields, and handle missing values.
- Implemented reusable KPI and trend calculations for revenue, profit, distinct orders, units sold, average order value, and profit margin.
- Wrote SQLite queries for monthly sales, product rankings, regional performance, customer segments, and profitability analysis.
- Added a rule-based insight engine and optional LLM narrative integration with environment-variable-based secret handling.

No measured business impact is claimed because the dataset is synthetic.

### GitHub repository description
Interactive sales analytics dashboard built with Python, Pandas, Plotly, Streamlit, SQLite SQL, and optional LLM-powered executive summaries.

### LinkedIn project description
Created a portfolio project that turns synthetic sales data into an interactive business dashboard. It includes data cleaning, KPI calculations, product/category/region/customer analysis, SQL reporting, CSV downloads, and a rule-based insights engine with optional LLM-generated narrative summaries. Built to demonstrate practical analytics workflow and responsible AI integration.

### Two-minute interview explanation
“I built a Sales Data Analysis and AI-Powered Insights Dashboard to demonstrate an end-to-end analytics workflow. I generated a realistic synthetic sales dataset with more than a thousand rows, including missing values and duplicate records, so I could practice data-quality handling. I used Pandas to validate columns, parse dates, convert numeric fields, remove exact duplicates, and handle missing descriptive values. Then I calculated core business KPIs such as revenue, profit, distinct orders, units sold, average order value, and profit margin.

For visualization, I used Streamlit for the dashboard interface and Plotly for interactive charts. Users can filter by date, region, product category, customer segment, and product. The dashboard updates KPI cards and charts based on those filters and lets users download filtered data. I also wrote SQLite queries for monthly trends, top products, regional performance, customer segmentation, and low-profit products.

For the AI component, I started with a rule-based insight engine so the project works without an API key. It highlights month-over-month changes, leading regions and categories, and low-profit products. There is also an optional LLM integration to turn calculated findings into a management-friendly narrative. I keep the calculated metrics separate from the generated explanation and handle API failures without breaking the dashboard. The project helped me practice data cleaning, analytical thinking, visualization, SQL, dashboard development, and responsible use of generative AI.”

### Ten interview questions and sample answers

1. **What problem does the project solve?**  
   It turns sales rows into KPIs, trends, and comparisons so a user can explore performance without manually building every report.

2. **Why did you use Pandas?**  
   Pandas provides practical tools for data validation, missing-value handling, date parsing, grouping, aggregation, and CSV input/output.

3. **How do you calculate average order value?**  
   Total revenue divided by the number of distinct Order IDs. The code returns zero when there are no orders.

4. **Why count distinct Order IDs?**  
   One order may contain multiple product rows. Counting rows could overstate the number of orders.

5. **How do you handle missing values?**  
   Rows missing core fields needed for calculations are removed; missing descriptive values become “Unknown”; missing discounts default to zero. This policy is documented and can be adjusted to a real business's rules.

6. **What is the difference between revenue and profit?**  
   Revenue is the sales amount. Profit reflects the profitability value supplied in the dataset. The project assumes the source Profit field is already calculated.

7. **What does month-over-month growth mean?**  
   (Current-month revenue − previous-month revenue) divided by previous-month revenue, multiplied by 100. It is undefined when previous-month revenue is zero.

8. **Why use Streamlit and Plotly?**  
   Streamlit makes it quick to build an interactive Python dashboard; Plotly supports hover details and interactive charts.

9. **How is generative AI used responsibly here?**  
   Deterministic metrics and rule-based findings are calculated first. The optional LLM only writes a narrative based on those findings, is labeled separately, and is not required for the app to work.

10. **What would you improve for production?**  
    Add real-source validation, automated data-quality reports, role-based access, a database-backed pipeline, scheduled refreshes, stronger monitoring, and business-specific definitions for returns, cost, and order status.

## Limitations and verification

- Data is synthetic and not representative of a real company.
- The Profit field is generated for demonstration; real projects need a documented cost/profit definition.
- The dashboard has not been browser-tested in this environment. Run the commands above locally.
- Automated tests are included; test results should be confirmed in your local Python environment.
- The optional LLM feature requires a separately installed `openai` client, valid provider credentials, model access, and internet connectivity.
