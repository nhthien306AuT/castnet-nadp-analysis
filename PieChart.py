import plotly.graph_objects as go
import pandas as pd
from plotly.subplots import make_subplots
import os

class ChemicalPieVisualizer:
    def __init__(self, loader):
        self.loader = loader

    def drawPie(self):
        labels = self.loader.get_labels()

        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "domain"}, {"type": "domain"}]],
        )

        for i, label in enumerate(labels):
            df = self.loader.get(label)
            if df is None or "VARIABLE" not in df.columns or "CONC" not in df.columns:
                print(f"⚠️ Skipping {label} due to missing VARIABLE or CONC columns.")
                continue
            df = df.copy()
            df['CONC'] = pd.to_numeric(df['CONC'], errors='coerce') 
            grouped = df.groupby("VARIABLE")["CONC"].mean().dropna()
            if grouped.empty:
                print(f"⚠️ No valid data to plot for {label}")
                continue
            var_labels = grouped.index.tolist()
            values = grouped.values.tolist()
            values = [round(v, 2) for v in grouped.values.tolist()]
            total = sum(values)
            custom_labels = [
                f"{param}<br>Avg: {val:.2f}<br>{val/total:.1%}"
                for param, val in zip(var_labels, values)
            ]

            fig.add_trace(
                go.Pie(
                labels=var_labels,
                values=values,
                text=custom_labels,
                hoverinfo="label+percent+value",
                textinfo="label+percent+value",
                textfont=dict(size=12)), 
                row=1, col=i+1)

        fig.update_layout(
            title=dict(text="Average Concentration & Proportion of Each Variable",
                       x=0.5,
                       xanchor='center'),
            margin=dict(t=60, b=30, l=20, r=20),
            annotations=[
                *[
                    dict(
                        text=label.upper(),
                        x=0.2 if i == 0 else 0.79, 
                        y=1.04,
                        xref='paper', yref='paper',
                        showarrow=False,
                        font=dict(size=14)
                    )
                    for i, label in enumerate(labels)
                ],
                dict(
                    text="Unit: µg/m³",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0,
                    font=dict(size=12)
                )
            ]
        )
        fig.show()
        self.fig=fig
        
    def export(self, filename="Pie_Chart.html"):
        os.makedirs("assets", exist_ok=True)  
        path = os.path.join("assets", filename)
        self.fig.write_html(path)
        print(f"✅ Exported to: {path}")


