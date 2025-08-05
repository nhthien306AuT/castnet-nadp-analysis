# PROJECT: CHEMICAL EXPOSURE
## Project Structure
### 1.Raw data from Castnet(dry deposition) & Nadp(wet deposition): 
https://drive.google.com/file/d/1TXg5GOMSxpksGC-PUoPYI_Tegq7OGNcs/view?usp=drive_link
### 2.Code structure
- ReadDatacsv.py : read and group data by castnet & nadp separately, get coordinates for map visualization. 
- Overview: 
    + GroupSiteID.py: group by siteid (how many samples per siteid)
    + GroupVar.py: group by variable (how many samples per variable)
- Statistics:
    + TimeStatistics.py: statistics of missing time periods for each sideID
    + SampleLossStatistics_100km.py: statistics of nearby siteID missing samples at the same time (range: 100km-cluster)
    + SampleLossStatistics_All: statistics of nearby siteID missing samples at the same time (range: map)
- Chart:
    - Line: 
        + LineGraphAllMap.py: visualize data with 2 options: yearly & monthly.Firstly, Yearly option will visualize data from 2000 to 2024 for each deposition. Second, monthly will visualize data about 12 months of each year (2000-2024).
        + LineGraphByState.py: same as LineGrapAllMap but it will visualize by state. It also have 2 options: yearly & monthly.
    - Map: 
        + GeopraphicChart.py: it will visualize the concentration of each chemical over many years.
    - Butterfly: 
        + ButterflyChart.py: large-scale sample loss frequency statistics (2 range options: all & 100km).
    - Pie: 
        + PieChart.py: average concentration & distribution of each variable.
    - Ranking: ranking of sample loss and non-sample loss siteids.
- folder:
    - Excel_Result: where to store the excel result files after code execution.
    - assests: where to store html charts in order to visualize on custom dashboard.
    - requirements: where version & libraries used are stored.
### 3.Data Analyst
- Ask step:
    + 1. What impact are these chemicals having on the environment ?
    + 2. What is the close relationship between these chemicals and climate change ?
    + 3. What causes widespread natural disasters to occur today?
    + 4. What thresolds are likely to cause potential and widespread ecological disruption ?
- Prepare step:
    + Data source: I got that dataset from someone else on social media - ( can download directly on castnet & nadp web).
    + 2 castnet files contain 10 columns, 1,227,750 rows, 242 siteids and 12 variables. 1 Nadp file contains 13 columns and 1,616,879 rows, 339 siteids and 8 variables.
    + Data type: SITE_ID (string), DATEON & DATEOFF (datetime in american format), LATITUDE & LONGITUDE & CONC (float),  YEAR & WEEK (integer)
    + ROCCC criteria:
        + Reliable: the dataset is provided by Castnet & Nadp.
        + Original: this is first-party collected directly from Castnet & Nadp system.
        + Comprehensive: The dataset includes detailed information of each sample. 
        + Cited: The dataset is publicly available on Castnet & Nadp website.
- Prepare step: 
    + Data was cleaned when I received it. 
    + I just handle NaN or Null values a little to avoid confusion with sodium (ReadDatacsv.py).
- Analyze step:
    + Review the code structure section above.
- Share step:
    + Question 1: What impact are these chemicals having on the environment ?
        + SO₂ and HNO₃ contribute to acid rain, which lowers the pH of soil and aquatic systems. 
        + NO₃ and NH₄ promote eutrophication, leading to oxygen depletion in lakes and rivers. 
        + In contrast, ions like Ca and Mg may buffer acidic inputs, helping to stabilize pH levels.
        + High sodium(Na) concentrations cause saltwater intrusion, affecting groundwater.
        + NH₃: Causes air pollution, toxic to aquatic organisms when dissolved in water.
        + SO₄: Result of acid rain and SO₂ oxidation. Contributes to soil/water acidification.
        + K: Nutritional role for plants; excess causes nutritional imbalance.
        + Cl: Affects salinity; high concentrations are harmful to freshwater organisms.
        + TNO₃: total of NO₃.
        + Tab 2: "Spatiotemporal Trends"
            + According to chart, we can see the SO₂, SO₄ NH₄, NO₃, concentrations in midwest and south Ameria tend to decrease over the years, but previously they maintained high concentrations across the board.  
            + HNO₃, TNO₃ we can see the concentration in west, midwest, south tend to decrease over the years, but previously they maintained high concentrations across the board. 
            + Ca, K, Mg: The concentrations were generally uniformly low.
            + Cl, Na: The concentrations are low deep inland, only high at the coast.
            + NH₃: The concentration in west tend to increase slightly over the years.
        + Tab 1: "Chemical Trends" 
            + Castnet: yearly average per chemical across the map.
                + Between 2001 and 2003, the concentration of chlorine dropped dramatically from 5.66 to 0.02, reflecting a significant environmental shift. This sharp decline can be largely attributed to stricter environmental regulations implemented in the United States during that period. In particular, amendments to the Clean Air Act and the Safe Drinking Water Act led to tighter controls on chlorine-based compounds in industrial emissions and water treatment processes. Many facilities transitioned away from traditional chlorine disinfection methods in favor of safer alternatives such as chloramine and ozone. Additionally, enforcement of the Montreal Protocol—which aimed to phase out ozone-depleting substances, including several chlorine-containing chemicals—further reduced atmospheric chlorine levels. Together, these regulatory and technological changes likely drove the steep reduction observed in the data.
                + From 2007 to 2024, ammonia (NH₃) concentrations exhibited a wave-like fluctuation but remained relatively stable overall, consistently hovering between approximately 2.1 and 2.2.
                + Overall, most of the other measured chemical compounds showed a gradual decreasing trend over time, with concentrations stabilizing around or below 1. Notably, some pollutants such as sulfur dioxide (SO₂), sulfate (SO₄²⁻), and total nitrate (TNO₃) had significantly higher levels in earlier years, ranging from 2 to 4.5. These declines likely reflect the impact of long-term air quality regulations and emission control efforts, especially targeting industrial and combustion-related sources
            + Nadp: yearly average per chemical across the map.
                + Nitrate (NO₃) and sulfate (SO₄) concentrations were relatively high in the early 2000s, averaging around 1.6 and 1.5 respectively. However, both compounds experienced a substantial decline over the following two decades. By 2024, their levels had dropped by more than half compared to their initial values.
                + The remaining chemical compounds showed minimal change throughout the observation period, with concentrations remaining largely stable and without any notable upward or downward trends.
            + Monthly option (all map): 
                + Castnet chart: Most of the chemical compounds exhibited irregular fluctuations throughout the year, without any consistent or recognizable seasonal pattern. However, a few notable exceptions—specifically sulfur dioxide (SO₂), sulfate (SO₄²⁻), ammonia (NH₃), ammonium (NH₄⁺), and nitrate (NO₃⁻)—showed clearer seasonal behaviors, often resembling either a U-shaped or inverted U-shaped trend. Notably, SO₂ and SO₄ displayed an inverse relationship: when the concentration of SO₂ increased, SO₄ tended to decrease, and vice versa. The inverse relationship between SO₂ and SO₄²⁻ concentrations may be explained by atmospheric chemical processes. As sulfur dioxide is oxidized into sulfate under specific environmental conditions—such as higher humidity, temperature, and sunlight—SO₂ levels decrease while SO₄²⁻ levels rise. This transformation is a key pathway in the formation of secondary aerosols.
                + Nadp chart: Most chemical compounds exhibited only minor fluctuations throughout the year, without any distinct or consistent seasonal patterns. Among all the measured substances, sulfate (SO₄²⁻) and nitrate (NO₃⁻) consistently recorded higher concentrations compared to the other compounds. This suggests their dominant contribution to wet deposition chemistry, likely influenced by persistent sources such as fossil fuel combustion and agricultural emissions.
            + Average by State: states with prominent chemical concentrations.
                + SO₄: West Virginia(WV), Ohio(OH), Pennsylvania(PA), Indiana(IN), Kentucky(KY), Alabama(AL).
                + NO₃: Iowa(IA), Illinois(IL), Nebraska(), Indiana(IN), Ohio(OH), Pennsylvania(PA), New York(NY).
                + NH₄: Iowa(IA), Illinois(IL), Missouri(MO), Indiana(IN), North Carolina(NC).
                + SO₂: West Virginia(WV), Ohio(OH), Pennsylvania(PA), Missouri(MO), Alabama(AL), Tennessee(TN). 
                + Cl: Florida(FL), California(CA) ,Maine(ME), New York(NY). 
                + Na: Florida(FL), California(CA), New York(NY). 
                + Ca: Arizona(AZ), New Mexico(NM), Texas(TX), Utah(UT), Nevada(NV).
                + Mg: Arizona (AZ), New Mexico(NM), Nevada(NV).
    #### Conclusion: Key Factors Influencing Chemical Concentrations
    - Sulfur Dioxide(SO₂):
        + Main sources: Fossil fuel combustion (especially coal-fired power plants), industrial emissions.
        + Key factors:
            + High in industrialized regions (e.g., WV, OH, PA).
            + Decreases over time due to air quality regulations (e.g., Clean Air Act).
            + Seasonal variation tied to energy demand and atmospheric oxidation processes.
    - Sulfate (SO₄²):
        + Secondary pollutant: Formed via oxidation of SO₂ in the atmosphere.
        + Key factors:
            + Inversely related to SO₂ (oxidation leads to SO₄ increase).
            + Enhanced by humidity, sunlight, and atmospheric chemistry.
            + Major contributor to acid rain and wet deposition. 
    - Nitrate (NO₃):
        + Sources: Agricultural runoff, vehicle and industrial NOₓ emissions.
        + Key factors:
            + High in farming-intensive states (e.g., IA, IL, NE).
            + Declining due to emission controls and improved fertilizer management.
            + Contributes to acidification and eutrophication.
    - Ammonium (NH₄): 
        + Source: Atmospheric conversion of ammonia(NH₃).
        + Key factors:
            + Strongly linked to agricultural activity and livestock waste.
            + High in Midwest and Southeast (e.g., IA, NC).
            + Promotes eutrophication in water bodies.	
    - Ammonia (NH₃):
        + Direct emissions from fertilizers and livestock,
        + Key factors:
            + Gradually increasing in western states.
            + Volatile in the atmosphere; converts to NH₄.
            + Harmful to air quality and aquatic life when deposited.
    - Total Nitrate (TNO₃):
        + Combination of NO₃ from different sources
        + Key factors: Similar to NO₃ – agriculture, traffic, industry.
    - Chloride (Cl):
        + Sources: Sea salt aerosol, road salt, some industrial processes.
        + Key factors:
            + High along coastal states (e.g., FL, CA, ME)
            Low inland.
            + Affects freshwater ecosystems at high levels.
    - Sodium (Na):
        + Often co-occurs with Cl (from marine aerosol or road salt).
        + Key factors:
            + Elevated near coasts.
            + Minimal presence inland.
            + Not a major acidifying agent, but affects salinity balance.
    - Calcium (Ca) & Magnesium (Mg):
        + Source: Dust, soil particles, crustal materials.
        + Key factors:
            + High in arid, mineral-rich regions (e.g., AZ, NM, NV)
            + Act as pH buffers, neutralizing acid deposition.
            + Stable over time with minimal seasonal variation.
    - Potassium (K):
        + Sources: Soil dust, biomass burning, fertilizer.
        + Key factors:
            + Minor contributor.
            + Plays a nutritional role for plants, but excess can disrupt nutrient balance.
    + Question 2: What is the close relationship between these chemicals and climate change ? 
        + Firstly, we can navigate to tab 4: "Concentration", which displays a pie chart illustrating the relative proportions of each chemical compound.
        + In the CASTNET chart, the major contributors to total chemical concentration are: 
            SO₂, SO₄, NH₃, TNO₃, HNO₃, NO₃, and NH₄.
        + In the NADP chart, the dominant chemicals by proportion are: 
            SO₄, NO₃, NH₄, and CL.
        + Next, we will navigate to Frequency tab: the relationship will be explored in here.
        + CASTNET collects dry deposition samples on a weekly basis, operating continuously. However, it tends to miss samples during rainy or excessively humid conditions, as such weather interferes with accurate dry deposition measurements. As a result, missing data are more common during wet seasons.
        + NADP collects wet deposition samples, triggered by precipitation events (rain, snow, fog). During dry periods with little or no precipitation, no sample is collected, leading to increased missing data in dry seasons.
        + By examining the missing data charts, we can identify 2 notable findings:
            + On the left chart (showing missing samples across the entire map), there is a significant observation for the CASTNET dataset (blue): the frequency of simultaneous large-scale missing data events (defined as more than 5 site IDs missing at the same time) has increased substantially over time, with recurring peaks becoming more frequent.
            + On the right chart (focusing on localized missing events within a 100 km radius involving more than 2 site IDs), a different pattern emerges for the NADP dataset (orange): while the overall increase in missing frequency is moderate, three clear peaks can be identified in 2007, 2012, and 2020. Notably, CASTNET’s chart beside it also shows an upward trend in missing events, and its peaks consistently follow the peaks observed in NADP.
        *(skip 2024 due to insufficient data).
    ### First Relationship - Castnet VS Nadp: right chart (range: 100km) 
    - We can clearly observe a temporal pattern in the missing data trends:
    Whenever a NADP peak occurs, there is always a corresponding peak in CASTNET.
    ### Second Relationship - Chemical Trends VS Frequency
    - We observe a clear downward trend in the concentrations of all chemical compounds from 2000 to 2024, including those with the highest proportions (Line graph - yearly average per chemical across the map).
    - However, in stark contrast, the frequency of widespread missing samples has continued to rise and repeatedly reached new peaks over time.
    + Question 3: What causes widespread natural disasters to occur today?
        + Now, we will use these two relationships to find out the causes of large-scale natural disasters.
        + With the second relationship, we can clearly a constrasting trend. This is explained by: 
            + While pollutant concentrations such as SO₂ and NOₓ have significantly decreased due to environmental regulations,this also leads to a reduction in atmospheric aerosols, which previously reflected sunlight and had a cooling effect.
            + The resulting increase in solar radiation accelerates global warming, contributing to more frequent and severe weather events. 
        + With the first relationship, We will see the trend of the events that cause the sample.
            + To explain this relationship, we can understand that when the concentration and moisture in both the atmosphere and the soil drop rapidly below a critical threshold, and the average temperature increases significantly, the Earth tends to self-regulate through large-scale natural disasters. Therefore, the severity and frequency of these disasters seem to be proportional to the sample loss index shown in the chart on the right, item Nadp.
    + Question 4: What thresolds are likely to cause potential and widespread ecological disruption ?
        + Looking at the chart on the right in the NADP section, we see 3 prominent peaks occurring in 2007, 2012, and 2020 — all between 530 and 540. These peaks may represent a critical threshold, where atmospheric concentrations and humidity have bottomed out and average temperatures in the United States have reached the maximum that Earth can tolerate. The Earth will immediately trigger large-scale natural disasters as a mechanism to reset and restore the balance of these two important indicators.
    ==> If you want to verify large scale catastrophic natural events along with their frequency then you can rely on the peaks in the graph to the right of the castnet section. Then, open the excel file named: SampleLossStatistics-Range-All_result, and search by timestamps to determine the specific time range. Finally, you can bring the specific time segments to search on the internet for information about these large-scale events.
    - Finally, The ranking tab will show us the top missing and non-missing siteids. Used as an additional reference for the frequency tab.
- Act step:
    + So we can see the effects of each chemical, the close relationships and the tolerance threshold. And with the continuous increase like that, the frequency of large-scale natural disasters in the future will continue to be more frequent and more catastrophic. This will cause damage to the US economy every year in the hundreds of billions of dollars.
==> 1. Reduce the frequency of sample loss to reduce its threshold.
    2. Reduce average heat in the US.
    3. Increase humidity in air and soil.




