import pandas as pd
import numpy as np
import os
import sys

print("📊 MLOps Automated Statistical Data Drift Monitor Activated...\n")

BASELINE_DATA = "server_metrics.csv"

def evaluate_statistical_drift_index():
    # SECURITY PROFILE: Preventing file path manipulation attacks
    if not os.path.exists(BASELINE_DATA):
        print("❌ Analytical Fault: Baseline training matrix trace (server_metrics.csv) unavailable.")
        return {"drift_status": "CRITICAL_ERROR", "drift_index": -1.0}
        
    try:
        # 1. Ingest historical vectors matrix as mathematical baseline reference
        baseline_df = pd.read_csv(BASELINE_DATA)
        total_records = len(baseline_df)
        
        # Safety bound check for minimum required statistical population density
        if total_records < 20:
            print(f"⚠️ Data density too low ({total_records} records). Need at least 20 records to establish statistical bounds.")
            return {"drift_status": "INSUFFICIENT_DATA", "drift_index": 0.0}

        # 2. Extracting core baseline control dimensions (Calculated Feature Bounds)
        # Hum CPU aur Latency metrics ka average aur variance check kar rahe hain
        cpu_mean_baseline = baseline_df["CPU_Usage"].mean()
        cpu_std_baseline = baseline_df["CPU_Usage"].std()
        
        # Handling edge case where standard deviation is absolute zero to prevent division by zero runtime error
        if pd.isna(cpu_std_baseline) or cpu_std_baseline == 0:
            cpu_std_baseline = 1.0

        # 3. Reading the last 15 live rows to simulate current streaming traffic distribution
        live_window_df = baseline_df.tail(15)
        live_mean_cpu = live_window_df["CPU_Usage"].mean()
        
        # 4. Applying Population Statistical Shift Equation (Z-Score Standard Deviation Boundary)
        statistical_deviation = abs(live_mean_cpu - cpu_mean_baseline) / cpu_std_baseline
        drift_score = round(float(statistical_deviation), 4)
        
        # Threshold criteria alignment: Deviations crossing 1.8 Sigmas trigger immediate training flags
        DRIFT_THRESHOLD_SIGMA = 1.8
        
        print(f"📁 Analyzing dataset footprint. Total logged arrays: {total_records}")
        print(f"📊 Reference Training CPU Mean: {cpu_mean_baseline:.2f} | Current Active Window Mean: {live_mean_cpu:.2f}")
        print(f"📐 Calculated Statistical Variance Coefficient (Drift Delta Index): {drift_score}")
        
        if drift_score >= DRIFT_THRESHOLD_SIGMA:
            print("\n⚠️ [ALERT] Severe Structural Data Drift Tracked in Production Pipeline Feature Matrix!")
            print("🔄 MLOps Automation Flag Triggered: Immediate Model Retraining Mandate Requested.")
            return {"drift_status": "DRIFT DETECTED", "drift_index": drift_score}
        else:
            print("\n✅ System Distribution Alignment Stable. Live stream parameters match original model training profiles.")
            return {"drift_status": "STABLE", "drift_index": drift_score}
            
    except Exception as e:
        print(f"🚨 Security/Runtime Exception trapped downstream: {str(e)}")
        return {"drift_status": "PIPELINE_ERROR", "drift_index": -1.0}

if __name__ == "__main__":
    evaluate_statistical_drift_index()