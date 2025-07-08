import pandas as pd
from ReadDatacsv import DataLoader
import os

class TimeCheck:
    def __init__(self, loader):
        self.loader = loader
        self.TimeResults = {}

    def analyze(self):
        for label in self.loader.get_labels():
            df = self.loader.get(label)

            if not {"SITE_ID", "DATEON", "DATEOFF"}.issubset(df.columns):
                print(f"⚠️ Ignore {label} because missing necessary column.")
                continue

            df["DATEON"] = pd.to_datetime(df["DATEON"], errors="coerce")
            df["DATEOFF"] = pd.to_datetime(df["DATEOFF"], errors="coerce")

            result = []
            for site, group in df.groupby("SITE_ID"):
                min_date = group["DATEON"].min()
                max_date = group["DATEOFF"].max()

                if pd.isna(min_date) or pd.isna(max_date):
                    continue

                full_weeks = pd.date_range(start=min_date, end=max_date, freq="7D")
                actual_weeks = group["DATEON"].dropna().sort_values().drop_duplicates()
                missing = full_weeks.difference(actual_weeks)

                result.append({
                    "SITE_ID": site,
                    "START_DATE": min_date.date(),
                    "END_DATE": max_date.date(),
                    "MISSING_COUNT": len(missing),
                    "MISSING_DATES": ", ".join([d.strftime("%Y-%m-%d") for d in missing]) if not missing.empty else "None"
                })

            self.TimeResults[label] = pd.DataFrame(result)
            time_df = self.TimeResults[label]
            print(f"📊 Processed TimeStatistics successfully: {label} ✅")
          

    def export(self, filename="TimeStatistics_result.xlsx"):
        if not self.TimeResults:
            print("⚠️ No data for export")
            return
       
        current_dir = os.path.dirname(os.path.abspath(__file__))
        export_dir = os.path.join(current_dir, "Excel_Result")
        os.makedirs(export_dir, exist_ok=True)
        export_path = os.path.join(export_dir, filename)

        with pd.ExcelWriter(export_path, engine="openpyxl") as writer:
            for label, df in self.TimeResults.items():
                df.to_excel(writer, sheet_name=label[:31], index=False)
        print(f"\n✅ Export successfully: {export_path}")

