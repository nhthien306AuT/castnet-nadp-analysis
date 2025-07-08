import pandas as pd
import os

class GroupID:
    def __init__(self, loader):
        self.loader = loader
        self.labels = self.loader.get_labels()
        self.results = {}

    def countSample(self, label):
        df = self.loader.get(label)
        if "SITE_ID" not in df.columns:
            print(f"⚠️ File '{label}' doesn't have SITE_ID column")
            return None

        counts = df.groupby("SITE_ID").size().reset_index(name="Sample_count")
        print(f"📊 File: {label} → {len(counts)} site | Total of samples: {counts['Sample_count'].sum():,}")
        print(counts)
        return counts

    def countSiteID(self):
        for label in self.labels:
            print(f"\n🔍 Processing file: {label}")
            
            df_summary = self.countSample(label)
            if df_summary is not None:
                self.results[label] = df_summary
        
    
   
    def export(self, filename="GroupID_result.xlsx"):
        if not self.results:
            print("⚠️ No data for export")
            return
       
        current_dir = os.path.dirname(os.path.abspath(__file__))
        export_dir = os.path.join(current_dir, "Excel_Result")
        os.makedirs(export_dir, exist_ok=True)
        export_path = os.path.join(export_dir, filename)

        with pd.ExcelWriter(export_path, engine="openpyxl") as writer:
            for label, df in self.results.items():
                df.to_excel(writer, sheet_name=label[:31], index=False)
        print(f"\n✅ Export successfully: {export_path}")
