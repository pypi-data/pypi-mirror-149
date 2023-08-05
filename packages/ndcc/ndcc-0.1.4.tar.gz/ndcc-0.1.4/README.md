# ndcc - NFL Draft Capital Comparator

A simple CLI App to compare the value of up to 32 NFL draft pick collections
with one another. This can be useful when trying to determine which team in the draft 
has the most draft capital, or by how much a team increased or decreased their capital 
with their draft day (pick) trades. The most obvious use case however is to determine 
who won a pick trade according to different value charts.

For now, these are the charts one can choose between to determine value:

* [Jimmy Johnson](https://www.drafttek.com/nfl-trade-value-chart.asp)
* [Rich Hill](https://www.drafttek.com/NFL-Trade-Value-Chart-Rich-Hill.asp)
* [Fitzgerald/Spielberger](https://overthecap.com/draft-trade-value-chart/) 
* [Kevin Meers (Harvard Sports Analysis)](https://harvardsportsanalysis.wordpress.com/2011/11/30/how-to-value-nfl-draft-picks/)
* [PFF WAR](https://www.pff.com/news/draft-pff-data-study-breaking-down-every-nfl-teams-draft-capital-jacksonville-jaguars)
* [Michael Lopez (blended curve)](https://statsbylopez.netlify.app/post/rethinking-draft-curve/) 

To account for drafts with a lot of compensatory picks, each chart is "prolonged" to 270 picks, 
using estimates on what the remaining values would be. 

## installation

```
pip install ndcc
```

## usage

```
python -m ndcc
```


## adding charts

To add another chart, simply add a column in charts.csv, fill in
the values and add the column name and chart name you want to be
presented with to the checkboxlist_dialog in input.get_selected_charts().
