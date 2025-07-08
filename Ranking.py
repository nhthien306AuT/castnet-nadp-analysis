import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class MissingDataRanker:
    def __init__(self, folder="Excel_Result", keyword="Time"):
        self.excel = pd.ExcelFile(self._find_file(folder, keyword))
        self.results = {}

    def _find_file(self, folder, keyword):
        for f in os.listdir(folder):
            if keyword in f and f.endswith(".xlsx"):
                return os.path.join(folder, f)
        raise FileNotFoundError("No matching Excel file found.")

    def _process(self, sheet):
        df = self.excel.parse(sheet)
        df['START_DATE'] = pd.to_datetime(df['START_DATE'])
        df['END_DATE'] = pd.to_datetime(df['END_DATE'])
        df['MISSING_COUNT'] = pd.to_numeric(df['MISSING_COUNT'], errors='coerce').fillna(0).astype(int)
        df['MONTHS'] = ((df['END_DATE'] - df['START_DATE']) / pd.Timedelta(days=30.44)).round().astype(int)
        top = df.sort_values('MISSING_COUNT', ascending=False).head(10)[['SITE_ID', 'MONTHS', 'MISSING_COUNT']]
        none = df[df['MISSING_COUNT'] == 0][['SITE_ID', 'MISSING_COUNT']].head(10)
        note = f"Total: {len(df[df['MISSING_COUNT'] == 0])} site without sample loss."
        return top, none, note

    def create(self):
        for sheet in ['castnet', 'nadp']:
            top, none, note = self._process(sheet)
            self.results[sheet] = (top, none, note)

        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "table"}, {"type": "table"}]] * 2,
            subplot_titles=[
                "CASTNET - Loss", "CASTNET - No Loss",
                "NADP - Loss", "NADP - No Loss"
            ],
            column_widths=[0.5, 0.5],
            horizontal_spacing=0.2, vertical_spacing=0.1
        )

        for i, sheet in enumerate(['castnet', 'nadp']):
            top, none, note = self.results[sheet]
            for j, df in enumerate([top, none]):
                if j == 1:
                    df = pd.concat([df, pd.DataFrame([[note] + [''] * (df.shape[1] - 1)], columns=df.columns)], ignore_index=True)
                fig.add_trace(go.Table(
                    header=dict(values=list(df.columns), fill_color='lightblue', align='left', font=dict(size=12)),
                    cells=dict(values=[df[c] for c in df.columns], fill_color='lavender', align='left', font=dict(size=11))
                ), row=i+1, col=j+1)

        fig.update_layout( margin=dict(t=40, b=30))
        self.fig = fig 
        fig.show()
    def export(self, filename="sample_loss_result.html"):
        os.makedirs("assets", exist_ok=True)  
        path = os.path.join("assets", filename)
        self.fig.write_html(path)
        print(f"✅ Exported to: {path}")

    def draw(self):
        self.create()