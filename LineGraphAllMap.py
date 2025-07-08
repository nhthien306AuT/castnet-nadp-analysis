import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import os

class ChartPlotterAllMap:

    def __init__(self, loader):
        self.loader = loader
        self.dataframes = loader.dataframes

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
    
    def export_html(self, fig, label, filename, folder_name="assets"):

        folder = os.path.join(folder_name, label.lower())
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, filename)
        fig.write_html(file_path, include_plotlyjs='cdn')

        print(f"✅ Saved HTML: {file_path}")

    def ChartYearly(self, label, title):
        if label not in self.dataframes:
            raise ValueError(f"❌ Can't find data of label: '{label}' in DataLoader.")

        df = self.dataframes[label]

        required_cols = {'YEAR', 'VARIABLE', 'CONC'}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"❌ File '{label}' missing column {required_cols}")

        grouped = df.groupby(['YEAR', 'VARIABLE'])['CONC'].mean().reset_index()
        grouped['YEAR'] = grouped['YEAR'].astype(int)

        chemicals = grouped['VARIABLE'].drop_duplicates().tolist()

        color_palette = px.colors.qualitative.Dark24 + px.colors.qualitative.Plotly
        color_map = {chem: color_palette[i % len(color_palette)] for i, chem in enumerate(chemicals)}

        fig = go.Figure()
        legend_shown = set()

        for chem in chemicals:
            chem_data = grouped[grouped['VARIABLE'] == chem]
            segments = self.split_by_gap(chem_data)

            for seg in segments:
                fig.add_trace(go.Scatter(
                    x=seg['YEAR'],
                    y=seg['CONC'],
                    mode='lines',
                    name=chem if chem not in legend_shown else None,
                    line=dict(width=3, color=color_map[chem]),
                    legendgroup=chem,
                    showlegend=chem not in legend_shown
                ))
            legend_shown.add(chem)

        fig.update_layout(
            title=title,
            xaxis_title='Year',
            yaxis_title='Average Concentration',
            hovermode='x unified',
            legend_title='Chemical',
            template='plotly_white',
            height=650
        )
        filename = f"{label.lower()}_Yearly_chart.html"
        self.export_html(fig, label, filename)

    def ChartMonthly(self, label, title):
        if label not in self.dataframes:
            raise ValueError(f"❌ Can't find data of label: '{label}' in DataLoader.")

        df = self.dataframes[label]

        if 'MONTH' not in df.columns:
            if 'DATEON' in df.columns:
                df['DATEON'] = pd.to_datetime(df['DATEON'], errors='coerce')
                df = df.dropna(subset=['DATEON'])
                df['MONTH'] = df['DATEON'].dt.month
            else:
                raise ValueError("❌ Can't determine MONTH: no DATEON column found.")
            
        required_cols = {'YEAR','MONTH', 'VARIABLE', 'CONC'}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"❌ File '{label}' missing column {required_cols}")

        grouped = df.groupby(['YEAR','MONTH', 'VARIABLE'])['CONC'].mean().reset_index()
        grouped['YEAR'] = grouped['YEAR'].astype(int)
        grouped['MONTH'] = grouped['MONTH'].astype(int)

        chemicals = grouped['VARIABLE'].drop_duplicates().tolist()

        color_palette = px.colors.qualitative.Dark24 + px.colors.qualitative.Plotly
        color_map = {chem: color_palette[i % len(color_palette)] for i, chem in enumerate(chemicals)}
        years = sorted(grouped['YEAR'].unique()) 

        for year in years:
            year_data = grouped[grouped['YEAR'] == year]
            fig = go.Figure()
            legend_shown = set()

            for chem in chemicals:
                chem_data = year_data[year_data['VARIABLE'] == chem].sort_values('MONTH')

                fig.add_trace(go.Scatter(
                    x=chem_data['MONTH'],
                    y=chem_data['CONC'],
                    mode='lines+markers',
                    name=chem if chem not in legend_shown else None,
                    line=dict(width=3, color=color_map[chem]),
                    legendgroup=chem,
                    showlegend=chem not in legend_shown
                ))
                legend_shown.add(chem)

            fig.update_layout(
                title=f"{label.upper()} - Monthly Concentration in {year}",
                xaxis_title='Month',
                yaxis_title='Average Concentration',
                xaxis=dict(tickmode='linear', tick0=1, dtick=1),
                hovermode='x unified',
                legend_title='Chemical',
                template='plotly_white',
                height=650
            )

          
            filename = f"{label.lower()}_{year}_Monthly.html"
            self.export_html(fig, label, filename)

    def drawAllMonthly(self):
        self.ChartMonthly('castnet', 'CASTNET - Monthly Average per Chemical across The Map')
        self.ChartMonthly('nadp', 'NADP - Monthly Average per Chemical across The Map')

    def drawAllYearly(self):
        self.ChartYearly('castnet', 'CASTNET - Yearly Average per Chemical across The Map')
        self.ChartYearly('nadp', 'NADP - Yearly Average per Chemical across The Map')



