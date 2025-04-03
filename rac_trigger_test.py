import pandas as pd
import os

def load_rac_csvs(base_path, num_racs=15):
    rac_data = {}
    for i in range(1, num_racs + 1):
        file_path = os.path.join(base_path, f"cube_data{i}.csv")
        if os.path.exists(file_path):
            rac_data[f"RAC{i}"] = pd.read_csv(file_path)
            print(f"✅ Loaded RAC{i} from {file_path}")
        else:
            print(f"❌ Missing RAC{i} at {file_path}")
    return rac_data

# CHANGE THIS to the actual path where your CSVs live
base_path = "/home/anthonyg"

rac_data = load_rac_csvs(base_path)

# Use actual RAC files
rac1_data = rac_data.get("RAC1")
rac2_data = rac_data.get("RAC2")

if rac1_data is not None and rac2_data is not None:
    threshold = 3
    activation_log = []

    for i in range(min(len(rac1_data), len(rac2_data))):
        rac1_row = rac1_data.iloc[i]
        rac2_row = rac2_data.iloc[i]

        rac1_active = rac1_row.filter(like='Node_').sum()
        rac1_triggered = rac1_active >= threshold

        rac2_active = rac2_row.filter(like='Node_').sum()
        rac2_triggered = rac1_triggered and rac2_active >= threshold

        activation_log.append({
            'Frame': i,
            'RAC1_ActiveBits': int(rac1_active),
            'RAC1_Triggered': rac1_triggered,
            'RAC2_ActiveBits': int(rac2_active),
            'RAC2_Triggered': rac2_triggered
        })

    df = pd.DataFrame(activation_log)
    print(df)
else:
    print("⚠️ RAC1 or RAC2 CSV not loaded. Check the file path or filenames.")
