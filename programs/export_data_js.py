import pandas as pd
import json
import os

def export_data():
    print("Reading customer segments and transactions...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    segments_file = os.path.join(script_dir, "..", "datasets", "customer_segments.csv")
    transactions_file = os.path.join(script_dir, "..", "datasets", "customer_transactions.csv")
    
    if not os.path.exists(segments_file) or not os.path.exists(transactions_file):
        raise FileNotFoundError("CSV data files not found in the workspace.")
        
    df_segments = pd.read_csv(segments_file)
    df_transactions = pd.read_csv(transactions_file)
    
    # 1. Base KPIs
    total_customers = int(df_segments['CustomerID'].nunique())
    total_revenue = float(df_transactions['TransactionAmount'].sum())
    avg_frequency = float(df_segments['NumberOfPurchases'].mean())
    avg_ticket = float(df_segments['AveragePurchaseValue'].mean())
    
    # 2. Segment summary data
    segment_summary = df_segments.groupby('CustomerSegment').agg(
        Count=('CustomerID', 'count'),
        AvgSpend=('TotalPurchaseAmount', 'mean'),
        AvgFreq=('NumberOfPurchases', 'mean'),
        AvgTicket=('AveragePurchaseValue', 'mean'),
        TotalSpend=('TotalPurchaseAmount', 'sum')
    ).round(2).to_dict(orient='index')
    
    # Clean segment keys for JS safety
    segment_summary_clean = {}
    for k, v in segment_summary.items():
        segment_summary_clean[k] = v
        
    # 3. Categories spend by Segment
    # Merge transactions with segments to get category spend per segment
    df_merged = df_transactions.merge(df_segments[['CustomerID', 'CustomerSegment']], on='CustomerID', how='left')
    category_spend = df_merged.groupby(['CustomerSegment', 'ProductCategory'])['TransactionAmount'].sum().round(2).unstack(fill_value=0).to_dict(orient='index')
    
    # Overall category spend
    overall_category_spend = df_merged.groupby('ProductCategory')['TransactionAmount'].sum().round(2).to_dict()
    
    # 4. Scatter data for plotting (subset of 1000 customers)
    scatter_data = []
    for _, row in df_segments.iterrows():
        scatter_data.append({
            'id': str(row['CustomerID']),
            'segment': str(row['CustomerSegment']),
            'spend': float(row['TotalPurchaseAmount']),
            'freq': int(row['NumberOfPurchases']),
            'ticket': float(row['AveragePurchaseValue'])
        })
        
    # Combine into a single dashboard data dict
    dashboard_data = {
        'kpis': {
            'totalCustomers': total_customers,
            'totalRevenue': total_revenue,
            'avgFrequency': round(avg_frequency, 2),
            'avgTicket': round(avg_ticket, 2)
        },
        'segments': segment_summary_clean,
        'categorySpendBySegment': category_spend,
        'overallCategorySpend': overall_category_spend,
        'scatter': scatter_data
    }
    
    # Write to data.js
    output_js = os.path.join(script_dir, "..", "datasets", "data.js")
    with open(output_js, 'w', encoding='utf-8') as f:
        f.write("// Auto-generated data for customer segmentation dashboard\n")
        f.write("const dashboardData = ")
        json.dump(dashboard_data, f, indent=2)
        f.write(";\n")
        
    print(f"Structured dashboard data exported successfully to {output_js}")

if __name__ == "__main__":
    export_data()
