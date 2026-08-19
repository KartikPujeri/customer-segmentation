import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Set up matplotlib style for clean, professional visualizations
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

def load_and_clean_data(filepath):
    print("Loading transaction data...")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found at {filepath}")
        
    df = pd.read_csv(filepath)
    
    # Basic data info
    print(f"Loaded {len(df)} transactions.")
    
    # Check for missing values
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print("Missing values found and handled:")
        print(missing)
        df = df.dropna()
    else:
        print("No missing values detected.")
        
    # Check for anomalies (e.g. negative or zero transaction amounts)
    invalid_records = df[df['TransactionAmount'] <= 0]
    if len(invalid_records) > 0:
        print(f"Removing {len(invalid_records)} invalid transactions with amounts <= 0.")
        df = df[df['TransactionAmount'] > 0]
        
    # Standardize data types
    df['TransactionDate'] = pd.to_datetime(df['TransactionDate'])
    df['CustomerID'] = df['CustomerID'].astype(str)
    
    return df

def perform_feature_engineering(df):
    print("Performing feature engineering at customer level...")
    # Aggregate transaction-level data to customer-level data
    customer_df = df.groupby('CustomerID').agg(
        TotalPurchaseAmount=('TransactionAmount', 'sum'),
        NumberOfPurchases=('TransactionAmount', 'count'),
        AveragePurchaseValue=('TransactionAmount', 'mean')
    ).reset_index()
    
    # Round metrics to 2 decimal places for clarity
    customer_df['TotalPurchaseAmount'] = customer_df['TotalPurchaseAmount'].round(2)
    customer_df['AveragePurchaseValue'] = customer_df['AveragePurchaseValue'].round(2)
    
    print(f"Engineered features for {len(customer_df)} unique customers.")
    return customer_df

def plot_feature_distributions(customer_df, output_dir):
    print("Generating feature distributions...")
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Total Purchase Amount Distribution
    axes[0].hist(customer_df['TotalPurchaseAmount'], bins=30, color='#3498db', edgecolor='black', alpha=0.7)
    axes[0].set_title('Distribution of Total Purchase Amount ($)', fontweight='bold')
    axes[0].set_xlabel('Total Amount ($)')
    axes[0].set_ylabel('Number of Customers')
    
    # Number of Purchases Distribution
    axes[1].hist(customer_df['NumberOfPurchases'], bins=20, color='#2ecc71', edgecolor='black', alpha=0.7)
    axes[1].set_title('Distribution of Number of Purchases', fontweight='bold')
    axes[1].set_xlabel('Number of Purchases (Frequency)')
    axes[1].set_ylabel('Number of Customers')
    
    # Average Purchase Value Distribution
    axes[2].hist(customer_df['AveragePurchaseValue'], bins=30, color='#e74c3c', edgecolor='black', alpha=0.7)
    axes[2].set_title('Distribution of Average Purchase Value ($)', fontweight='bold')
    axes[2].set_xlabel('Average Purchase Value ($/Ticket)')
    axes[2].set_ylabel('Number of Customers')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'feature_distributions.png'), dpi=300)
    plt.close()
    print("Distributions saved as plots/feature_distributions.png")

def run_elbow_method(scaled_features, output_dir):
    print("Running Elbow Method to find optimal K...")
    wcss = []
    k_range = range(1, 11)
    
    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        kmeans.fit(scaled_features)
        wcss.append(kmeans.inertia_)
        
    plt.figure(figsize=(8, 5))
    plt.plot(k_range, wcss, marker='o', color='#8e44ad', linewidth=2, markersize=8)
    plt.title('Elbow Method For Optimal K', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Clusters (K)', fontsize=12)
    plt.ylabel('WCSS (Within-Cluster Sum of Squares)', fontsize=12)
    plt.xticks(k_range)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Annotate elbow point (which should clearly show k=3)
    plt.annotate('Elbow Point (k=3)', xy=(3, wcss[2]), xytext=(4.5, wcss[2] + (wcss[0]-wcss[2])*0.2),
                 arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6))
                 
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'elbow_method.png'), dpi=300)
    plt.close()
    print("Elbow curve saved as plots/elbow_method.png")

def run_kmeans_clustering(customer_df, k=3):
    print(f"Running K-Means clustering with k={k}...")
    
    # Select features for clustering
    features = ['TotalPurchaseAmount', 'NumberOfPurchases', 'AveragePurchaseValue']
    X = customer_df[features]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Fit model
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    customer_df['ClusterID'] = kmeans.fit_predict(X_scaled)
    
    # Dynamically assign meaningful names to clusters
    # We will identify clusters based on average TotalPurchaseAmount
    cluster_means = customer_df.groupby('ClusterID')['TotalPurchaseAmount'].mean().sort_values()
    
    # Map clusters: lowest mean = Low-Value, middle = Regular, highest = High-Value
    cluster_mapping = {
        cluster_means.index[0]: 'Low-Value Customers',
        cluster_means.index[1]: 'Regular Customers',
        cluster_means.index[2]: 'High-Value Customers'
    }
    
    customer_df['CustomerSegment'] = customer_df['ClusterID'].map(cluster_mapping)
    print("K-Means completed. Segment mapping based on TotalPurchaseAmount:")
    for cid, sname in cluster_mapping.items():
        avg_spend = customer_df[customer_df['ClusterID'] == cid]['TotalPurchaseAmount'].mean()
        count = len(customer_df[customer_df['ClusterID'] == cid])
        print(f" - Cluster {cid} -> {sname} (Size: {count}, Avg Spend: ${avg_spend:.2f})")
        
    return customer_df

def plot_customer_segments(customer_df, output_dir):
    print("Generating segment visualization plots...")
    colors = {
        'High-Value Customers': '#2ecc71', # Green
        'Regular Customers': '#3498db',    # Blue
        'Low-Value Customers': '#e74c3c'   # Red
    }
    
    # 2D Scatter Plot: Total Spend vs Frequency
    plt.figure(figsize=(10, 7))
    for segment, color in colors.items():
        subset = customer_df[customer_df['CustomerSegment'] == segment]
        plt.scatter(
            subset['NumberOfPurchases'],
            subset['TotalPurchaseAmount'],
            c=color,
            label=segment,
            alpha=0.7,
            edgecolors='w',
            s=80
        )
        
    plt.title('Customer Segments: Total Spend vs Frequency', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Purchases (Frequency)', fontsize=12)
    plt.ylabel('Total Purchase Amount ($) (Monetary)', fontsize=12)
    plt.legend(frameon=True, facecolor='white', edgecolor='none')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'customer_segments_scatter.png'), dpi=300)
    plt.close()
    
    # 2D Scatter Plot: Frequency vs Average Purchase Value
    plt.figure(figsize=(10, 7))
    for segment, color in colors.items():
        subset = customer_df[customer_df['CustomerSegment'] == segment]
        plt.scatter(
            subset['NumberOfPurchases'],
            subset['AveragePurchaseValue'],
            c=color,
            label=segment,
            alpha=0.7,
            edgecolors='w',
            s=80
        )
        
    plt.title('Customer Segments: Avg Spend per Visit vs Frequency', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Number of Purchases (Frequency)', fontsize=12)
    plt.ylabel('Average Purchase Value ($/Ticket)', fontsize=12)
    plt.legend(frameon=True, facecolor='white', edgecolor='none')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'customer_segments_avg_vs_freq.png'), dpi=300)
    plt.close()
    
    # Box plots for checking feature variation across segments
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    features = ['TotalPurchaseAmount', 'NumberOfPurchases', 'AveragePurchaseValue']
    titles = ['Total Purchase Amount ($)', 'Number of Purchases', 'Average Purchase Value ($)']
    
    segment_order = ['Low-Value Customers', 'Regular Customers', 'High-Value Customers']
    box_colors = ['#e74c3c', '#3498db', '#2ecc71']
    
    for i, feature in enumerate(features):
        data_to_plot = [customer_df[customer_df['CustomerSegment'] == seg][feature] for seg in segment_order]
        bp = axes[i].boxplot(data_to_plot, labels=segment_order, patch_artist=True, medianprops=dict(color='black'))
        
        for patch, color in zip(bp['boxes'], box_colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.6)
            
        axes[i].set_title(titles[i], fontweight='bold')
        axes[i].set_xticklabels(['Low-Value', 'Regular', 'High-Value'])
        axes[i].grid(True, linestyle='--', alpha=0.5)
        
    plt.suptitle('Customer Segment Feature Profiles', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'segment_profiles.png'), dpi=300)
    plt.close()
    
    print("Plots saved to plots/ directory.")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Make sure output directory exists
    output_dir = os.path.join(script_dir, "..", "plots")
    os.makedirs(output_dir, exist_ok=True)
    
    # Load raw transactions
    raw_data_path = os.path.join(script_dir, "..", "datasets", "customer_transactions.csv")
    df = load_and_clean_data(raw_data_path)
    
    # Feature engineering at customer level
    customer_df = perform_feature_engineering(df)
    
    # Plot feature distributions
    plot_feature_distributions(customer_df, output_dir)
    
    # Prepare features for Elbow Method
    features = ['TotalPurchaseAmount', 'NumberOfPurchases', 'AveragePurchaseValue']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(customer_df[features])
    
    # Run Elbow Method
    run_elbow_method(X_scaled, output_dir)
    
    # Run K-Means Clustering
    customer_df = run_kmeans_clustering(customer_df, k=3)
    
    # Plot final customer segments
    plot_customer_segments(customer_df, output_dir)
    
    # Save the clustered dataset for Power BI
    output_csv = os.path.join(script_dir, "..", "datasets", "customer_segments.csv")
    customer_df.to_csv(output_csv, index=False)
    print(f"\nFinal segmented customer file saved as '{output_csv}' for Power BI analysis.")
    
    # Show segment statistics summary
    summary_stats = customer_df.groupby('CustomerSegment').agg(
        CustomerCount=('CustomerID', 'count'),
        AvgTotalSpend=('TotalPurchaseAmount', 'mean'),
        AvgNumPurchases=('NumberOfPurchases', 'mean'),
        AvgTicketValue=('AveragePurchaseValue', 'mean')
    ).round(2).reindex(['Low-Value Customers', 'Regular Customers', 'High-Value Customers'])
    
    print("\nSegment Profiles Summary:")
    print(summary_stats)

if __name__ == "__main__":
    main()
