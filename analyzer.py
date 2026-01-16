import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from utils import ensure_dir

class DataAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = self._load_data()
        self.stats = {}
        self.temp_charts = []
        # Apply premium styling
        sns.set_theme(style="darkgrid", palette="viridis")
        plt.rcParams['figure.facecolor'] = '#0e1117'
        plt.rcParams['axes.facecolor'] = '#1e2130'
        plt.rcParams['text.color'] = 'white'
        plt.rcParams['axes.labelcolor'] = 'white'
        plt.rcParams['xtick.color'] = 'white'
        plt.rcParams['ytick.color'] = 'white'

    def _load_data(self):
        ext = self.file_path.split('.')[-1].lower()
        if ext == 'csv':
            return pd.read_csv(self.file_path)
        elif ext in ['xlsx', 'xls']:
            return pd.read_excel(self.file_path)
        elif ext == 'json':
            return pd.read_json(self.file_path)
        else:
            raise ValueError("Unsupported file format")

    def get_summary_stats(self):
        """Calculates basic statistics for numeric columns."""
        numeric_df = self.df.select_dtypes(include=['number'])
        stats = {
            "total_records": len(self.df),
            "missing_values": self.df.isnull().sum().to_dict(),
            "numeric_stats": numeric_df.describe().to_dict() if not numeric_df.empty else {}
        }
        self.stats = stats
        return stats

    def generate_charts(self, output_dir="temp_charts"):
        """Generates basic charts and saves them as images."""
        ensure_dir(output_dir)
        self.temp_charts = []
        
        numeric_cols = self.df.select_dtypes(include=['number']).columns
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns

        # 1. Distribution Plot
        if len(numeric_cols) > 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(self.df[numeric_cols[0]], kde=True, color='#00d1ff', ax=ax)
            ax.set_title(f'Distribution Analysis: {numeric_cols[0]}', fontsize=16, color='#00d1ff')
            chart_path = os.path.join(output_dir, "dist_plot.png")
            fig.savefig(chart_path, transparent=True)
            plt.close(fig)
            self.temp_charts.append(chart_path)

        # 2. Modern Bar Chart
        if len(categorical_cols) > 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            count_data = self.df[categorical_cols[0]].value_counts().head(10)
            sns.barplot(x=count_data.index, y=count_data.values, palette="magma", ax=ax)
            ax.set_title(f'Top Categories: {categorical_cols[0]}', fontsize=16, color='#ff00c8')
            plt.xticks(rotation=45)
            chart_path = os.path.join(output_dir, "bar_chart.png")
            fig.savefig(chart_path, transparent=True)
            plt.close(fig)
            self.temp_charts.append(chart_path)

        # 3. Correlation Matrix
        if len(numeric_cols) > 1:
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(self.df[numeric_cols].corr(), annot=True, cmap='rocket', ax=ax)
            ax.set_title('Feature Correlation Heatmap', fontsize=16, color='#00ff88')
            chart_path = os.path.join(output_dir, "correlation.png")
            fig.savefig(chart_path, transparent=True)
            plt.close(fig)
            self.temp_charts.append(chart_path)

        return self.temp_charts

    def cleanup_charts(self):
        """Removes temporary chart images."""
        for chart in self.temp_charts:
            if os.path.exists(chart):
                os.remove(chart)
        self.temp_charts = []
