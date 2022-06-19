
# Interactive Dashboard for SLA_Metrics with Python – Streamlit

SLA_Metrics Dashboard is built in Python and the Streamlit library to visualize Excel data.

## Acronynms:
* SLA: <i>Service Level Agreement</i>(%)
* MTBF: <i>Mean Time Between Failures</i>(hrs)
* MTTR: <i>Mean Time To Repair</i>(hrs)

## Python Packages:
* Tkinter
* Turtle
* pandas 
* plotly.express
* import streamlit 
*  streamlit_option_menu 
*  datetime 

---
## Demo
SLA_Metrics Dashboard:


## Screenshot of SLA_metrics spreadsheet.
![](images/sla_ss.png)
The SLA_metrics table involves two sheet the DATA and MTBF and MTTR

 ## Formulas used

 * SLA in percentage is given as <i>[=ROUNDUP((((24*DAY(EOMONTH(B3,0)))-(24*(SUMPRODUCT(H3))))/(24*DAY(EOMONTH(B3,0)))*100),2)]</i>

* MTBF and MTTR percentage is given as 
<i>[=AVERAGE(Data!K2:K5)] and [=AVERAGE(Data!L2:L5)]</i>
---

## Screenshoot of SLA_Metrics spreadsheet displayed on web page
![](images/sla_metrics%20table.png)

From the diagram above the interface involves the main table, the filtered data and the sidebar to the left for navigation.

---
## Screenshoot of SLA_metrics  calculated in percentages
![](images/Monthlysla.png)

From the sreenshoot above SLAs are filtered by Month and then displayed in a barchart. 

---
## Screenshoot of MTBF and MTTR calculated in hours
![](images/mttr%20and%20mtbf.png)

From the screenshoot above MTBF and MTTR are filtered by Month and then displayed in a barchart. 



