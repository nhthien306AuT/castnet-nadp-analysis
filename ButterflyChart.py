import os
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

class DualButterflyChartPlotter:
    def __init__(self, folder_path='Excel_Result'):
        self.folder_path = folder_path
        self.file_keywords = ['Range-All','Range-100km-cluster']
        self.sheet_names = ['castnet', 'nadp']

    def find_file_by_keyword(self, keyword):
        for f in os.listdir(self.folder_path):
            if keyword in f and f.endswith('.xlsx'):
                return os.path.join(self.folder_path, f)
        raise FileNotFoundError(f"No Excel file found for keyword '{keyword}' in {self.folder_path}")

    def load_counts_by_year(self, file_path):
        counts = {'castnet': defaultdict(int), 'nadp': defaultdict(int)}
        filter_site_count = 'Range-All' in file_path

        for sheet in self.sheet_names:
            try:
                df = pd.read_excel(file_path, sheet_name=sheet)
                df.columns = [col.strip().upper() for col in df.columns]
                if 'DATE' not in df.columns:
                    continue
                df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
                df = df.dropna(subset=['DATE'])

                if filter_site_count and 'SITE_COUNT' in df.columns:
                    df = df[df['SITE_COUNT'] >= 5]
                for date in df['DATE']:
                    year = date.year
                    counts[sheet][year] += 1
            except Exception as e:
                print(f"Error loading sheet {sheet} from {file_path}: {e}")
        return counts

    def plotButterflyChart(self):
        fig, axes = plt.subplots(1, 2, figsize=(18, 8))

        for i, keyword in enumerate(self.file_keywords):
            file_path = self.find_file_by_keyword(keyword)
            counts = self.load_counts_by_year(file_path)
            years = sorted(set(counts['castnet'].keys()) | set(counts['nadp'].keys()))
            castnet_vals = [counts['castnet'].get(year, 0) for year in years]
            nadp_vals = [counts['nadp'].get(year, 0) for year in years]
            y_positions = list(range(len(years)))

            ax = axes[i]
            ax.barh(y_positions, [-val for val in castnet_vals], color='skyblue', label='CASTNET')
            ax.barh(y_positions, nadp_vals, color='coral', label='NADP')
            ax.axvline(0, color='black', linewidth=1)
            ax.set_yticks(y_positions)
            ax.set_yticklabels([str(year) for year in years])

            for y, val in zip(y_positions, castnet_vals):
                if val > 0:
                    ax.text(-val*1, y, f'{val:,}', va='center', ha='right', fontsize=8)
            for y, val in zip(y_positions, nadp_vals):
                if val > 0:
                    ax.text(val*1, y, f'{val:,}', va='center', ha='left', fontsize=8)

            ax.set_title(f'Sample Loss Statistics-{keyword}', fontsize=13, fontweight='bold')
            label_text = 'Number of Weeks Loss Sample (siteid > 2)' if i == 1 else 'Number of Weeks Loss Sample (siteid > 5)'
            ax.set_xlabel(label_text)
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=2)
            ax.grid(axis='x', linestyle='--', alpha=0.5)
            xticks = ax.get_xticks()
            ax.set_xticklabels([f"{int(abs(x)):,}" for x in xticks])

        plt.tight_layout(rect=[0, 0.03, 1, 1])
        self.fig=fig  
      
    def export(self, filename="butterfly_chart.png"):

        os.makedirs("assets", exist_ok=True)  
        path = os.path.join("assets", filename)
        self.fig.savefig(path, dpi=300)
        print(f"✅ Exported PNG: {path}")
