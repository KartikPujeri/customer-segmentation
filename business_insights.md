# Business Insights Report: Customer Segmentation & Purchase Analytics

## Executive Summary
This report analyzes the customer purchasing behavior of **1,000 unique customers** based on a historical dataset of **6,584 transactions** spanning a one-year period (June 2025 – June 2026). Total revenue generated during this period was **$881,311.51**.

Using the **K-Means Clustering** algorithm, we grouped customers based on three behavioral features:
1. **Total Purchase Amount (Monetary)**: How much money the customer spent in total.
2. **Number of Purchases (Frequency)**: How many times the customer made a purchase.
3. **Average Purchase Value (Monetary)**: The average ticket size per purchase.

The algorithm successfully identified **three distinct customer segments**: **Low-Value Customers**, **Regular Customers**, and **High-Value Customers**.

---

## Segment Profiles & Revenue Contribution

The Pareto Principle (80/20 rule) is highly visible in our customer base: **just 11.4% of our customers generate 66.6% of our total revenue**.

| Customer Segment | Customer Count | Share of Customers (%) | Avg. Number of Purchases | Avg. Ticket Value ($) | Avg. Total Spend ($) | Estimated Total Segment Spend ($) | Estimated Share of Revenue (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **High-Value Customers** (VIPs) | 114 | 11.4% | 19.65 | $265.25 | $5,147.69 | $586,836.66 | 66.6% |
| **Regular Customers** (Loyal Spenders) | 328 | 32.8% | 8.86 | $84.91 | $758.17 | $248,679.76 | 28.2% |
| **Low-Value Customers** (Budget Spenders) | 558 | 55.8% | 2.58 | $31.13 | $82.07 | $45,795.06 | 5.2% |
| **Total / Average** | **1,000** | **100%** | **6.58** | **$88.13** | **$881.31** | **$881,311.48** | **100%** |

---

## Key Business Insights

### 1. The Power of VIPs (High-Value Customers)
* High-Value Customers spend an average of **$5,147.69** annually.
* Although they represent only **11.4%** of the customer base, they account for **two-thirds ($586,836.66)** of our total sales.
* They shop frequently (nearly **20 times a year**) and have a high average transaction size of **$265.25**.
* *Action:* Retaining this group is the absolute highest business priority. A 5% churn in this segment is equivalent to losing over $29,000 in sales.

### 2. The Potential of the Core (Regular Customers)
* Regular Customers make up **32.8%** of our customer base and contribute **28.2% ($248,679.76)** of revenue.
* They have moderate frequency (avg. **8.86 purchases**) and spend a solid **$84.91** per transaction.
* *Action:* This is our "growth engine." Moving a portion of these customers into the High-Value segment through upselling and incentives will significantly drive bottom-line growth.

### 3. The Volume of Budget Spenders (Low-Value Customers)
* Low-Value Customers represent the largest customer group at **55.8%**, yet they generate only **5.2% ($45,795.06)** of sales.
* They make very few purchases (avg. **2.58 purchases** per year) and spend low amounts (avg. **$31.13** per ticket).
* *Action:* We must avoid spending significant marketing resources on this segment. Instead, target them with low-cost, automated email campaigns and clearance sales.

---

## Actionable Recommendations & Marketing Strategies

### Category A: High-Value Customers (VIP Retention)
* **Objective:** Maximize loyalty and eliminate churn.
* **Loyalty Program:** Introduce a tiered VIP club with exclusive benefits (e.g., free express shipping, priority support, and early access to new arrivals).
* **Personalized Marketing:** Match them with dedicated account/personal shopping assistance. Send personalized thank-you notes or premium gifts on their birthdays.
* **Exclusive Previews:** Host private shopping hours or online early-access events for high-ticket item releases.

### Category B: Regular Customers (Value Expansion)
* **Objective:** Increase purchase frequency and average ticket size.
* **Cross-Selling & Recommendations:** Use purchase history to recommend complementary items (e.g., recommending a matching belt if they buy jeans).
* **Threshold Incentives:** Introduce promotions like "Spend $100 and get free shipping" or "Get $15 off on purchases above $120" to push their average transaction size of $84.91 closer to the next bracket.
* **Subscription / Refill Programs:** If applicable, offer subscription boxes or automated re-orders with a small discount (5-10%) to build recurring frequency.

### Category C: Low-Value Customers (Re-engagement & Efficiency)
* **Objective:** Maintain low-cost exposure and drive transactional clearance.
* **Automated Email Journeys:** Set up triggers for "we miss you" discount codes (e.g., 10% off) when they haven't purchased in 90 days.
* **Flash Sales & Clearance:** Direct this group to end-of-season sales, clearance collections, or bulk-buy deals. They are highly price-sensitive.
* **Minimize Acquisition Costs:** Avoid retargeting this group with expensive paid social media ads. Rely heavily on low-cost owned media (email and push notifications).
