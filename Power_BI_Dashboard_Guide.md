# Power BI Dashboard Creation Guide: Customer Purchase Analytics

This guide provides step-by-step instructions for building a professional and interactive Power BI Dashboard using the generated dataset: `datasets/customer_segments.csv` and `datasets/customer_transactions.csv`.

---

## Step 1: Import the Data

1. Open **Power BI Desktop**.
2. On the **Home** ribbon, click **Get Data** and select **Text/CSV**.
3. Locate and select [customer_segments.csv](file:///c:/Users/KARTHIK/Desktop/ds_project/datasets/customer_segments.csv) and click **Load**.
4. Repeat the process to import the raw transaction log [customer_transactions.csv](file:///c:/Users/KARTHIK/Desktop/ds_project/datasets/customer_transactions.csv) if you wish to analyze product category trends by segment.

---

## Step 2: Establish Data Modeling Relationships (Optional but Recommended)

To analyze product categories and transaction dates by customer segments, connect the two datasets:
1. Click the **Model view** tab on the left sidebar.
2. Drag the `CustomerID` column from the `customer_segments` table and drop it onto the `CustomerID` column of the `customer_transactions` table.
3. This creates a **1-to-many (1:*) relationship** from `customer_segments` (dimension table) to `customer_transactions` (fact table).
4. Double-check that the filter direction is set to **Single (customer_segments filters customer_transactions)**.

---

## Step 3: Create Key Business Measures (DAX)

Create a dedicated table or add these measures to your `customer_segments` table for consistent reporting:

* **Total Customers:**
  ```dax
  Total Customers = COUNT('customer_segments'[CustomerID])
  ```
* **Total Revenue:**
  ```dax
  Total Revenue = SUM('customer_segments'[TotalPurchaseAmount])
  ```
* **Average Spend Per Customer:**
  ```dax
  Average Customer Spend = AVERAGE('customer_segments'[TotalPurchaseAmount])
  ```
* **Average Number of Purchases (Frequency):**
  ```dax
  Average Purchase Frequency = AVERAGE('customer_segments'[NumberOfPurchases])
  ```
* **Average Ticket Size (Value per Visit):**
  ```dax
  Average Ticket Size = AVERAGE('customer_segments'[AveragePurchaseValue])
  ```

---

## Step 4: Design the Dashboard Layout

Create a clean canvas. We recommend using a modern Dark Mode style or a Sleek Light Mode style with clean borders and consistent coloring.

### Section A: KPI Summary Cards (Top Row)
Add four **Card** visuals to represent high-level metrics across the entire customer base.
1. **Total Customers** (formatted as a whole number)
2. **Total Revenue** (formatted as currency: `$881.31K`)
3. **Avg. Purchase Frequency** (formatted as a decimal: `6.58`)
4. **Avg. Ticket Size** (formatted as currency: `$88.13`)

### Section B: Segment Share & Value (Middle Row)
1. **Donut Chart - Customer Distribution**
   * *Legend:* `CustomerSegment`
   * *Values:* `Total Customers` (Measure) or `CustomerID` count.
   * *Aesthetic Tip:* Use colors matching segment values (e.g., Green for High-Value, Blue for Regular, Red/Coral for Low-Value). Show both category and percentage.
2. **Clustered Column Chart - Metric Profiles by Segment**
   * *X-axis:* `CustomerSegment`
   * *Y-axis:* Add both `Average Purchase Frequency` and `Average Ticket Size` to compare purchase habits side-by-side.
3. **Bar Chart - Revenue by Customer Segment**
   * *Y-axis:* `CustomerSegment`
   * *X-axis:* `Total Revenue` (Measure)
   * *Tip:* Enable **Data labels** so viewers can see immediately that High-Value customers contributed $586.84K of revenue.

### Section C: Cluster Visualization & Trends (Bottom Row)
1. **Scatter Plot - K-Means Cluster Reproduction**
   * *X-axis:* `NumberOfPurchases`
   * *Y-axis:* `TotalPurchaseAmount`
   * *Legend:* `CustomerSegment`
   * *Values:* `CustomerID` (drag to Detail field)
   * *Result:* This will recreate the identical K-Means cluster scatter plot natively inside Power BI, allowing users to hover over individual customers.
2. **Treemap or Column Chart - Purchases by Product Category** (Requires the raw transaction data import from Step 2)
   * *Category/Group:* `ProductCategory` (from the transactions table)
   * *Values:* `TransactionAmount` (Sum)
   * *Details:* Since the relationship is built, slicing the dashboard by clicking a segment in the donut chart will automatically filter this chart to show what categories the VIPs or Regulars buy most!

### Section D: Slicers (Interaction Panel)
1. Add a **Slicer** visual using the field `CustomerSegment`. Set the slicer type to **Tile** or **Vertical List**.
2. Slicing by `CustomerSegment` lets the user filter the entire report instantly to view individual group statistics.

---

## Step 5: Colors and Theme Customization

To align with the Python-generated charts and ensure premium visuals:
* Set up a custom palette in **View -> Themes -> Customize Current Theme**:
  * **High-Value Customers:** `#2ECC71` (vibrant green for high value)
  * **Regular Customers:** `#3498DB` (reliable blue for regular)
  * **Low-Value Customers:** `#E74C3C` (red/coral representing lower margins)
* Increase font sizes for card callouts to `32pt` and set labels to `9pt`.
* Add visual borders with a corner radius of `8px` to give cards a modern, containerized dashboard feel.
