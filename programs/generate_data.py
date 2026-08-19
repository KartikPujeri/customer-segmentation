import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_customer_transactions(num_customers=1000, seed=42):
    np.random.seed(seed)
    random.seed(seed)
    
    # Customer IDs
    customer_ids = [f"C{10000 + i}" for i in range(1, num_customers + 1)]
    
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Groceries', 'Beauty & Personal Care', 'Books']
    category_weights = [0.20, 0.25, 0.15, 0.20, 0.10, 0.10]
    
    start_date = datetime(2025, 6, 1)
    end_date = datetime(2026, 6, 1)
    date_range_days = (end_date - start_date).days
    
    transactions = []
    transaction_id_counter = 100000
    
    for customer_id in customer_ids:
        # Determine archetype
        archetype_roll = random.random()
        
        if archetype_roll < 0.55:
            # Low-Value / Budget Spender (55%)
            num_purchases = random.randint(1, 4)
            mean_amount = random.uniform(15, 45)
            std_amount = 5
        elif archetype_roll < 0.90:
            # Regular / Moderate Spender (35%)
            num_purchases = random.randint(5, 12)
            mean_amount = random.uniform(50, 110)
            std_amount = 15
        else:
            # High-Value / Premium Spender (10%)
            num_purchases = random.randint(10, 28)
            mean_amount = random.uniform(160, 350)
            std_amount = 50
            
        for _ in range(num_purchases):
            # Generate amount
            amount = np.random.normal(mean_amount, std_amount)
            # Ensure positive, min spend of $3.00
            amount = max(3.00, round(amount, 2))
            
            # Generate purchase date
            days_offset = random.randint(0, date_range_days)
            purchase_date = start_date + timedelta(days=days_offset)
            
            # Select category
            category = random.choices(categories, weights=category_weights)[0]
            
            transactions.append({
                'TransactionID': f"T{transaction_id_counter}",
                'CustomerID': customer_id,
                'TransactionDate': purchase_date.strftime('%Y-%m-%d'),
                'TransactionAmount': amount,
                'ProductCategory': category
            })
            transaction_id_counter += 1
            
    # Convert to DataFrame
    df = pd.DataFrame(transactions)
    
    # Shuffle transactions to simulate chronological processing
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    return df

if __name__ == "__main__":
    print("Generating synthetic customer transactions dataset...")
    df_transactions = generate_customer_transactions(num_customers=1000)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_filename = os.path.join(script_dir, "..", "datasets", "customer_transactions.csv")
    df_transactions.to_csv(output_filename, index=False)
    
    print(f"Dataset generated and saved to {output_filename}")
    print(f"Total Transactions: {len(df_transactions)}")
    print(f"Total Unique Customers: {df_transactions['CustomerID'].nunique()}")
    print(f"Date Range: {df_transactions['TransactionDate'].min()} to {df_transactions['TransactionDate'].max()}")
    print(f"Revenue Total: ${df_transactions['TransactionAmount'].sum():,.2f}")
    print("\nFirst 5 rows:")
    print(df_transactions.head())
