# clean_and_visualize.py
import os
import re
import pandas as pd
import matplotlib.pyplot as plt

def parse_to_numeric_midpoint(range_str):
    if pd.isna(range_str):
        return None
    # Extract numbers from strings like "$50K - $80K" or "100000"
    numbers = [int(s) for s in re.findall(r'\d+', str(range_str))]
    if len(numbers) == 2:
        return sum(numbers) / 2
    elif len(numbers) == 1:
        # If it's already a full number like 50000, keep it, otherwise scale it if it's shorthand
        val = numbers[0]
        return val if val > 1000 else val
    return None

def assign_salary_bucket(midpoint):
    if midpoint is None:
        return "Unknown"
    # Mapping numbers cleanly into 4 highly-populated structural tiers
    if midpoint <= 45:
        return "Low Tier ($30K - $45K)"
    elif midpoint <= 75:
        return "Mid Tier ($46K - $75K)"
    elif midpoint <= 110:
        return "High Tier ($76K - $110K)"
    else:
        return "Premium Tier ($111K+)"

def run_data_engineering_pipeline():
    print("=========================================================")
    print("🧹 CAREERCOMPASS DATA CLEANING & VISUALIZATION WORKSPACE")
    print("=========================================================\n")
    
    csv_filename = "job_descriptions.csv" 
    if not os.path.exists(csv_filename):
        print(f"❌ ERROR: '{csv_filename}' not found in root folder.")
        return

    print("[1/4] Ingesting raw Kaggle CSV file...")
    df = pd.read_csv(csv_filename)
    print(f"• Raw dataset loaded with {len(df):,} records.")

    # Drop rows missing critical target metrics to prevent vector corruption
    initial_len = len(df)
    df = df.dropna(subset=['Job Title', 'skills', 'Salary Range', 'Experience']).reset_index(drop=True)
    print(f"• Dropped {initial_len - len(df):,} incomplete rows.")

    print("\n[2/4] Executing regex text cleaning & normalization...")
    # Convert ranges to midpoints and clean up layout strings
    df['salary_midpoint'] = df['Salary Range'].apply(parse_to_numeric_midpoint)
    
    # Remove rows where salary parsing failed
    df = df.dropna(subset=['salary_midpoint']).reset_index(drop=True)
    
    # Assign our highly-stable macro categorical buckets
    df['salary_bucket'] = df['salary_midpoint'].apply(assign_salary_bucket)
    
    # Routed both transformations through the .str accessor to prevent AttributeError crashes
    df['cleaned_title'] = df['Job Title'].fillna("").astype(str).str.strip().str.lower()
    df['cleaned_skills'] = df['skills'].fillna("").astype(str).str.replace(',', ' ').str.strip().str.lower()

    print("\n[3/4] Exporting pristine data layer to disk...")
    cleaned_csv_path = "cleaned_job_descriptions.csv"
    df.to_csv(cleaned_csv_path, index=False)
    print(f"✓ Success: Saved cleanly structured data file to '{cleaned_csv_path}'")

    print("\n[4/4] Generating Class Distribution Chart...")
    # Count how many rows sit inside each of our 4 new categories
    bucket_counts = df['salary_bucket'].value_counts()
    
    # Generate an explicit analytical chart layout to inspect class balances
    plt.figure(figsize=(10, 6))
    colors = ['#4f46e5', '#7c3aed', '#06b6d4', '#10b981'] # Sleek CareerCompass theme colors
    
    bucket_counts.plot(kind='bar', color=colors, edgecolor='black', alpha=0.85)
    plt.title('Salary Macro-Bucket Class Distribution Profile', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Target Salary Brackets (Classification Labels)', fontsize=12, labelpad=10)
    plt.ylabel('Total Job Rows in Dataset', fontsize=12, labelpad=10)
    
    # 🌟 FIXED: Removed 'hspace' so it runs seamlessly
    plt.xticks(rotation=15)
    
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    
    # Save chart profile graph straight to folder path
    chart_path = "salary_distribution_profile.png"
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"✓ Success: Visualization profile saved directly to '{chart_path}'")
    
    print("\n=========================================================")
    print("🎉 DATA CLEANING COMPLETE! CHANNELS READY FOR TRAINING")
    print("=========================================================")

if __name__ == "__main__":
    run_data_engineering_pipeline()