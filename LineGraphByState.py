import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
from shapely.geometry import Point
from Path import ShapePaths
import os

class ChartPlotterByState:
    STATE_FULL_NAMES = {
    'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida',
    'GA': 'Georgia', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois',
    'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana',
    'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan',
    'MN': 'Minnesota', 'MO': 'Missouri', 'MS': 'Mississippi', 'MT': 'Montana',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire',
    'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York',
    'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
    'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota',
    'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia',
    'VT': 'Vermont', 'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia',
    'WY': 'Wyoming'
}

    def __init__(self, loader, coor,shapefile_path=ShapePaths["USStates"]):
        self.loader = loader
        self.dataframes = loader.dataframes
        self.coor = coor.reset_index().rename(columns={'LAT': 'LATITUDE', 'LON': 'LONGITUDE'})      
        self.shapefile_path = shapefile_path

    def split_by_gap(self, df, year_col='YEAR', threshold=1):
        df = df.sort_values(year_col).reset_index(drop=True)
        segments = []
        current_segment = [df.iloc[0]]

        for i in range(1, len(df)):
            prev_year = df.iloc[i - 1][year_col]
            curr_year = df.iloc[i][year_col]
            if curr_year - prev_year <= threshold:
                current_segment.append(df.iloc[i])
            else:
                segments.append(pd.DataFrame(current_segment))
                current_segment = [df.iloc[i]]
        if current_segment:
            segments.append(pd.DataFrame(current_segment))
        return segments

    def assign_state_by_shapefile(self, df):
        print("🔄 Gán STATE bằng shapefile...")
        usa = gpd.read_file(self.shapefile_path)
        usa = usa[~usa['STUSPS'].isin(['AK', 'HI', 'PR'])]  

        gdf = gpd.GeoDataFrame(
            df,
            geometry=[Point(xy) for xy in zip(df['LONGITUDE'], df['LATITUDE'])],
            crs="EPSG:4326"
        )

        gdf_joined = gpd.sjoin(gdf, usa[['STUSPS', 'geometry']], how="left", predicate='within')
        df['STATE'] = gdf_joined['STUSPS'].values
        return df

          
    def prepare_data_with_state(self, label):
        if label not in self.dataframes:
            raise ValueError(f"❌ not found data '{label}'.")

        df = self.dataframes[label]
        if 'STATE' not in df.columns:
            if 'LATITUDE' not in df.columns or 'LONGITUDE' not in df.columns:
                df = df.merge(self.coor[['SITE_ID', 'LATITUDE', 'LONGITUDE']], on='SITE_ID', how='left')
            df = self.assign_state_by_shapefile(df)
        return df
    
    def export_html(self, fig, label, filename, folder_name="assets"):

        folder = os.path.join(folder_name, label.lower())  
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        fig.write_html(path, include_plotlyjs='cdn')

        print(f"✅ Saved HTML: {path}")

    def ChartYearlyByState(self, label, title):
        df = self.prepare_data_with_state(label)

        required_cols = {'STATE', 'YEAR', 'VARIABLE', 'CONC'}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"❌ File '{label}' is missed columns: {required_cols}")

        grouped = df.groupby(['STATE', 'YEAR', 'VARIABLE'])['CONC'].mean().reset_index()
        grouped['YEAR'] = grouped['YEAR'].astype(int)

        chemicals = grouped['VARIABLE'].drop_duplicates().tolist()
        states = grouped['STATE'].dropna().unique()

        color_palette = px.colors.qualitative.Dark24 + px.colors.qualitative.Plotly
        color_map = {chem: color_palette[i % len(color_palette)] for i, chem in enumerate(chemicals)}

        for state in sorted(states):
            state_data = grouped[grouped['STATE'] == state]
            fig = go.Figure()
            legend_shown = set()

            for chem in chemicals:
                chem_data = state_data[state_data['VARIABLE'] == chem]
                if chem_data.empty:
                    continue

                segments = self.split_by_gap(chem_data)

                for seg in segments:
                    fig.add_trace(go.Scatter(
                        x=seg['YEAR'],
                        y=seg['CONC'],
                        mode='lines+markers',
                        name=chem if chem not in legend_shown else None,
                        line=dict(width=2.5, color=color_map[chem]),
                        legendgroup=chem,
                        showlegend=chem not in legend_shown
                    ))
                legend_shown.add(chem)
            full_state = self.STATE_FULL_NAMES.get(state, state)
            fig.update_layout(
                title=f"{title} - {full_state}" if title else f"{label.upper()} - {full_state}",
                xaxis_title='Year',
                yaxis_title='Avg Concentration',
                hovermode='x unified',
                legend_title='Chemical',
                template='plotly_white',
                height=650
            )

            filename = f"{label.lower()}_{state}_Yearly_chart.html"
            self.export_html(fig, label, filename)

    def drawYearlyByState(self):
        self.ChartYearlyByState('castnet', 'CASTNET - Yearly Average per Chemical by State')
        self.ChartYearlyByState('nadp','NADP - Yearly Average per Chemical by State')

##########################################################################################
    
    def ChartMonthlyByState(self, label, title_prefix):
        df = self.prepare_data_with_state(label)

        if 'MONTH' not in df.columns:
            if 'DATEON' in df.columns:
                df['DATEON'] = pd.to_datetime(df['DATEON'], errors='coerce')
                df = df.dropna(subset=['DATEON'])
                df['MONTH'] = df['DATEON'].dt.month
            else:
                raise ValueError("❌ Can't determine MONTH: no DATEON column found.")

        required_cols = {'STATE', 'YEAR', 'MONTH', 'VARIABLE', 'CONC'}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"❌ File '{label}' is missed columns: {required_cols}")
        grouped = df.groupby(['STATE', 'YEAR', 'MONTH', 'VARIABLE'])['CONC'].mean().reset_index()
        grouped['MONTH'] = grouped['MONTH'].astype(int)
        grouped['YEAR'] = grouped['YEAR'].astype(int)

        chemicals = grouped['VARIABLE'].drop_duplicates().tolist()
        states = grouped['STATE'].dropna().unique()
        years = grouped['YEAR'].drop_duplicates().sort_values().tolist()

        color_palette = px.colors.qualitative.Dark24 + px.colors.qualitative.Plotly
        color_map = {chem: color_palette[i % len(color_palette)] for i, chem in enumerate(chemicals)}

        for state in sorted(states):
            state_data = grouped[grouped['STATE'] == state]

            for year in years:
                year_data = state_data[state_data['YEAR'] == year]
                if year_data.empty:
                    continue

                fig = go.Figure()
                legend_shown = set()

                for chem in chemicals:
                    chem_data = year_data[year_data['VARIABLE'] == chem]
                    if chem_data.empty:
                        continue

                    segments = self.split_by_gap(chem_data, year_col='MONTH', threshold=1)

                    for seg in segments:
                        fig.add_trace(go.Scatter(
                            x=seg['MONTH'],
                            y=seg['CONC'],
                            mode='lines+markers',
                            name=chem if chem not in legend_shown else None,
                            line=dict(width=2.5, color=color_map[chem]),
                            legendgroup=chem,
                            showlegend=chem not in legend_shown
                        ))
                    legend_shown.add(chem)

                full_state = self.STATE_FULL_NAMES.get(state, state)
                fig.update_layout(
                    title=f"{title_prefix} - {full_state} - {year}",
                    xaxis_title='Month',
                    yaxis=dict(title='Avg Concentration'),
                    hovermode='x unified',
                    legend_title='Chemical',
                    template='plotly_white',
                    height=650
                )

                filename = f"{label.lower()}_{state}_{year}_Monthly_chart.html"
                self.export_html(fig, label, filename)
                
    def drawMonthlyByState(self):
        self.ChartMonthlyByState('castnet', 'CASTNET - Monthly Avg per Chemical by state')
        self.ChartMonthlyByState('nadp', 'NADP - Monthly Avg per Chemical by state')

