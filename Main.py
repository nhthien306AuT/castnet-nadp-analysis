from ReadDatacsv import DataLoader
from GroupSiteID import GroupID
from GroupVar import GroupVars
from TimeStatistics import TimeCheck
from SampleLossStatistics_All import MissingPatternAnalyzerAll
from SampleLossStatistics_100km import MissingPatternAnalyzer_100km
from LineGraphAllMap import ChartPlotterAllMap
from LineGraphByState import ChartPlotterByState
from GeographicChart import ChemicalMapVisualizer
from Dashboard import ChemicalDashboardApp
from ButterflyChart import DualButterflyChartPlotter
from Ranking import MissingDataRanker
from PieChart import ChemicalPieVisualizer

if __name__ == "__main__":
# Read dataset & get coordinates(by siteid) from file csv
    # loader = DataLoader()
    # coor = loader.getCoordinates()

# Overview: group by siteID
    # id=GroupID(loader)
    # id.countSiteID()
    # id.export()

# Overview: group by variables
    # var=GroupVars(loader)
    # var.countVar()
    # var.export()

# Statistics of missing time periods for each sideID
    # check=TimeCheck(loader)
    # check.analyze()
    # check.export()
    
# Statistics of nearby siteID missing samples at the same time (range: 100km-cluster)
    # range100= MissingPatternAnalyzer_100km(check,coor)
    # range100.analyze100km()
    # range100.export()

# Statistics of nearby siteID missing samples at the same time (range: map)
    # rangeAll = MissingPatternAnalyzerAll(check,coor)
    # rangeAll.analyzeCause()
    # rangeAll.export()

# Line graph (range: map)
    # chartAllMap=ChartPlotterAllMap(loader)
    # chartAllMap.drawAllYearly()
    # chartAllMap.drawAllMonthly()

# Line graph (range: state)
    # chartByState=ChartPlotterByState(loader,coor)
    # chartByState.drawYearlyByState()
    # chartByState.drawMonthlyByState()

# Geographic chart over time (range: map)
    # geo = ChemicalMapVisualizer(loader,coor)
    # geo.drawGeoChart()
    
# Butterfly chart each year
    # butterfly = DualButterflyChartPlotter()
    # butterfly.plotButterflyChart()
    # butterfly.export()

# Ranking top siteids
    # rank=MissingDataRanker()
    # rank.draw()
    # rank.export()

# Pie Chart (Chemicals) -All
    # Pie= ChemicalPieVisualizer(loader)
    # Pie.drawPie()
    # Pie.export()

# Dashboard of all HTML files
    dashboard = ChemicalDashboardApp()
    dashboard.run()

    
