import pandas as pd
from collections import defaultdict
from haversine import haversine
import os
import networkx as nx

class MissingPatternAnalyzer_100km:
    def __init__(self, check, coor):
        self.check = check
        self.coord_dict = self.buildCoor(coor)
        
    def buildCoor(self, coor):
        return {
            site: (row["LATITUDE"], row["LONGITUDE"])
            for site, row in coor.iterrows()
        }
    
    def find_spatial_clusters(self, sites, dis=100):
        G = nx.Graph()
        G.add_nodes_from(sites)

        for i, site_a in enumerate(sites):
            lat_a, lon_a = self.coord_dict.get(site_a, (None, None))
            if lat_a is None: continue

            for site_b in sites[i + 1:]:
                lat_b, lon_b = self.coord_dict.get(site_b, (None, None))
                if lat_b is None: continue

                if haversine((lat_a, lon_a), (lat_b, lon_b)) <= dis:
                    G.add_edge(site_a, site_b)
        return [sorted(list(comp)) for comp in nx.connected_components(G) if len(comp) > 1]
    
    def analyze100km(self, dis=100):
        self.allClusters = {}

        for label, df in self.check.TimeResults.items():
            print(f"🔍 Processing label: {label}")
            date_site_map = defaultdict(set)
            all_clusters = []

            for _, row in df.iterrows():
                site = row["SITE_ID"]
                if row["MISSING_DATES"] == "None":
                    continue
                for date in row["MISSING_DATES"].split(", "):
                    date_site_map[date].add(site)


            for date, sites in date_site_map.items():
                clusters = self.find_spatial_clusters(list(sites), dis)
                for cluster in clusters:
                    all_clusters.append({
                        "DATE": pd.to_datetime(date).date(),
                        "SITES": ", ".join(cluster)
                    })
            result = (
                pd.DataFrame(all_clusters)
                .drop_duplicates(subset=["DATE", "SITES"])
                .sort_values(["DATE", "SITES"])
            )
            self.allClusters[label]=result
            print(f"Processed SampleLoss_100km Successfully: {label} ✅")
            print(result)

    def export(self, filename="SampleLossStatistics-Range-100km-cluster_result.xlsx"):
        if not self.allClusters:
            print("⚠️ No data for export")
            return
       
        current_dir = os.path.dirname(os.path.abspath(__file__))
        export_dir = os.path.join(current_dir, "Excel_Result")
        os.makedirs(export_dir, exist_ok=True)
        export_path = os.path.join(export_dir, filename)

        with pd.ExcelWriter(export_path, engine="openpyxl") as writer:
            for label, df in self.allClusters.items():
                df.to_excel(writer, sheet_name=label[:31], index=False)
        print(f"\n✅ Export successfully: {export_path}")

