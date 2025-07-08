import pandas as pd
from Path import DatasetPaths
class DataLoader:
    def __init__(self):
    
        self.dataframes = {}
        self.readAll()

    def readAll(self):
        for label, paths in DatasetPaths.items():
            print(f"📂 Reading file: {label}")
            dfs = []
            for path in paths:
                print(f"  ↳ {path}")
                df = pd.read_csv(path, low_memory=False,
                                 na_values=["", "NaN", "NAN", "null", "NULL"],
                                 keep_default_na=False)
                dfs.append(df)
            self.dataframes[label] = pd.concat(dfs, ignore_index=True)
            print(f"✅ {label}: {len(self.dataframes[label]):,} rows | {self.dataframes[label].shape[1]} columns")
    
    def getCoordinates(self):
        all_data = []
        for label in self.get_labels():
            df = self.get(label)
            if {"SITE_ID", "LATITUDE", "LONGITUDE"}.issubset(df.columns):
                all_data.append(df[["SITE_ID", "LATITUDE", "LONGITUDE"]])

        if all_data:
            merged = pd.concat(all_data).drop_duplicates(subset="SITE_ID").set_index("SITE_ID")
            return merged
        else:
            return pd.DataFrame(columns=["LATITUDE", "LONGITUDE"])
    
    
    def get(self, label):
        return self.dataframes.get(label)

    def get_labels(self):
        return list(self.dataframes.keys())
    
   





   

   

