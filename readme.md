# **Dev Test – AI Data Engineer Role**

We want to see how you approach **data ingestion, modeling, and making metrics accessible**. The goal is not a production system, but a clear demonstration of your thinking, SQL skills, and ability to use automation (n8n).

---

## **Part 1 – Ingestion (Foundation)**

**Dataset provided:** [`ads_spend.csv`](https://drive.google.com/file/d/1RXj_3txgmyX2Wyt9ZwM7l4axfi5A6EC-/view) with columns:

```
date, platform, account, campaign, country, device, spend, clicks, impressions, conversions

```

Download link: [https://drive.google.com/file/d/1RXj\_3txgmyX2Wyt9ZwM7l4axfi5A6EC-/view](https://drive.google.com/file/d/1RXj_3txgmyX2Wyt9ZwM7l4axfi5A6EC-/view)

**Requirements:**

* Use **n8n** to orchestrate ingestion of this dataset into a **warehouse table** (DuckDB, BigQuery, or another you prefer).  
* Include **basic metadata** (load\_date, source\_file\_name) so we can see provenance.  
* Show that the data persists after refresh.

---

## **Part 2 – KPI Modeling (SQL)**

Build queries (or dbt models if you prefer) to compute:

* **CAC** \= spend / conversions  
* **ROAS** \= (revenue / spend), where **assume revenue \= conversions × 100**

**Analysis:**

* Compare **last 30 days vs prior 30 days**.  
* Show results in a compact table with absolute values \+ deltas (% change).

---

## **Part 3 – Analyst Access**

Expose the metrics in one simple way:

* Either: provide a **SQL script** with parameters (date ranges)  
* Or: create a **tiny API endpoint** `/metrics?start&end` returning JSON

---

## **Part 4 – Agent Demo (Bonus, Optional)**

Show how a natural-language question like:

“Compare CAC and ROAS for last 30 days vs prior 30 days.”

could map to your query and produce an answer.

* Can be a **template, a simple mapping, or a README example**.  
* Doesn’t need to be full NL→SQL.

---

## **Deliverables**

When finished, please submit:

1. **n8n access** (URL \+ read-only user or exported workflow JSON)  
2. **GitHub Repo URL** (public) with:  
   * Ingestion workflow  
   * SQL/dbt models  
   * README with setup instructions  
3. **Results** (screenshot of table or API output)  
4. **Loom Video** (max 5 minutes) explaining your approach and key decisions

---

## **Deadline**

Submit within **3 days** of receiving this challenge.