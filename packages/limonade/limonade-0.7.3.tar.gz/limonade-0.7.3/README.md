# Limonade

Limonade is a library meant to simplify handling of list mode data from different sources. To make this possible a 
framework of data storage is defined. All details of the data are defined by configuration of the detector and the plot 
using configuration files written in json.

Once in Limonade format, the data can be retrieved and histogrammed using powerful selection tools in the plot module. 
With Limonade you can
- Select events by time interval
- Define extra data, such as coordinates or boolean flags
- Define gates for any data for any channel and define (anti)coincidence logic for them.
- Chain-load multiple data files
- Create 1d- and 2d-histograms of any data.
