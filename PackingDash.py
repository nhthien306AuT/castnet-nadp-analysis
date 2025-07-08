from Dashboard import ChemicalDashboardApp


if __name__ == "__main__":
    app = ChemicalDashboardApp()
    app.run()
# pyinstaller --noconsole --noconfirm --onefile --add-data "assets;assets" your_dashboard_file.py

