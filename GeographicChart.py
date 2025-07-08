import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

class ChemicalMapVisualizer:
    def __init__(self, loader, coor):
        self.loader = loader
        self.coor = coor
        
    def export(self, fig, label, var, folder_name="assets"):

        folder = os.path.join(folder_name, label.lower())
        filename = f"{label.lower()}_{var}_map.html".replace(" ", "_")
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        fig.write_html(path, include_plotlyjs='cdn')
        
        print(f"✅ Saved HTML: {filename}")

    def plot_Geo_Chart(self, label):

        df = self.loader.get(label)
        if df is None:
            raise ValueError(f"❌ Dataset '{self.label}' not found in DataLoader.")
        
        if {"SITE_ID", "VARIABLE", "DATEON", "CONC"}.issubset(df.columns):
            df = df.copy()
            df["DATE"] = pd.to_datetime(df["DATEON"], errors="coerce")
            df["YEAR"] = df["DATE"].dt.year
           
            df.drop(columns=[col for col in ["LATITUDE", "LONGITUDE"] if col in df.columns], inplace=True)
            grouped = df.groupby(["SITE_ID", "VARIABLE", "YEAR"]).agg({"CONC": "mean"}).reset_index()
            grouped = grouped.merge(self.coor, left_on="SITE_ID", right_index=True, how="left")
        else:
            raise ValueError("❌ Missing required columns in the dataset.")
        
        variables = grouped["VARIABLE"].dropna().unique()

        for var in variables:
    
            df_var = grouped[grouped["VARIABLE"] == var].copy()
            global_min = df_var["CONC"].min()
            global_max = df_var["CONC"].max()

            if df_var.empty:
                print(f"⚠️ No data found for {var}")
                continue

            df_var["YEAR"] = df_var["YEAR"].astype(int).astype(str)
            df_var = df_var.sort_values("YEAR")

            valid_df = df_var[df_var["CONC"].notna()]

            if valid_df.empty:
                max_info = "🔴 Max: N/A"
                min_info = "🟢 Min: N/A"
            else:
                max_row = valid_df.loc[valid_df["CONC"].idxmax()]
                min_row = valid_df.loc[valid_df["CONC"].idxmin()]
                max_info = f"🔴 Max: {max_row['CONC']:.2f} on {max_row['YEAR']} of {max_row['SITE_ID']} - ({max_row['LATITUDE']},{max_row['LONGITUDE']})"
                min_info = f"🟢 Min: {min_row['CONC']:.2f} on {min_row['YEAR']} of {min_row['SITE_ID']} - ({min_row['LATITUDE']},{min_row['LONGITUDE']})"

            fig = px.scatter_geo(
                df_var,
                lat="LATITUDE",
                lon="LONGITUDE",
                color="CONC",
                hover_name="SITE_ID",
                hover_data={"CONC": True,"YEAR": True,"LATITUDE": True,"LONGITUDE": True },
                animation_frame="YEAR",
                color_continuous_scale="Turbo",
                range_color=[global_min, global_max],
                title=f"{label.upper()} - {var} Concentration Over Time<br><sup>{max_info}<br>{min_info}</sup>",
                template="plotly_dark",
                height=700,
            )

            fig.update_geos(
                scope="world",
                showland=True,
                landcolor="#f5deb3",         
                oceancolor="#87cefa",        
                showocean=True,
                lakecolor="#87cefa",        
                showlakes=True,
                bgcolor="white"
            )
            fig.update_layout(
                legend_title="Concentration",
                coloraxis_colorbar_title="μg/m³"
            )
            filename = f"{label.lower()}_{var}_map.html".replace(" ", "_")
            self.export(fig, label, filename)

    def drawGeoChart(self):
        for label in ['castnet', 'nadp']:
            self.plot_Geo_Chart(label)
