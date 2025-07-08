import pandas as pd
from collections import defaultdict
import os

class MissingPatternAnalyzerAll:
    def __init__(self, check, coor):
        self.check = check  
        self.coor = coor
        self.cluster = {}

    def analyzeCause(self):

        for label, df in self.check.TimeResults.items():
            print(f"\n🔍 Analyzing missing data: {label}")
            date_site_map = defaultdict(set)  

            for _, row in df.iterrows():
                site = row["SITE_ID"]
                if row["MISSING_DATES"] == "None":
                    continue
                for date_str in row["MISSING_DATES"].split(", "):
                    date_site_map[date_str].add(site)

            rows = []
            for date, sites in date_site_map.items():
                if len(sites) > 1:
                    site_list = sorted(sites)
                    rows.append({
                        "DATE": date,
                        "SITE_IDS": ", ".join(site_list)
                    })

            result_df = pd.DataFrame(rows)
            result_df["DATE"] = pd.to_datetime(result_df["DATE"]).dt.date
            result_df["SITE_COUNT"] = result_df["SITE_IDS"].apply(lambda x: len(x.split(", ")))
            result_df = result_df[["DATE", "SITE_COUNT", "SITE_IDS"]].sort_values("DATE")
            self.cluster[label] = result_df
            print(f"Processed SampleLoss Successfully: {label} ✅")


    def export(self, filename="SampleLossStatistics-Range-All_result.xlsx"):
        if not self.cluster:
            print("⚠️ No data for export")
            return
       
        current_dir = os.path.dirname(os.path.abspath(__file__))
        export_dir = os.path.join(current_dir, "Excel_Result")
        os.makedirs(export_dir, exist_ok=True)
        export_path = os.path.join(export_dir, filename)

        with pd.ExcelWriter(export_path, engine="openpyxl") as writer:
            for label, df in self.cluster.items():
                df.to_excel(writer, sheet_name=label[:31], index=False)
        print(f"\n✅ Export successfully: {export_path}")

