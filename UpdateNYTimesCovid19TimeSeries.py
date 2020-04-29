import arcpy
import os
import urllib.request
from datetime import datetime

NYTConvid19USCountyDataURL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

# Step 1 of 2: Please update the following path and table name
#   a temporary location where the data will be downloaded to. This file gets deleted at the end of this script
csvFileName = r'D:\data\covid\cases\us-counties.csv'  #e.g. r'c:\data\NYTimesCovid19TimeSeries\us-counties.csv'
#   path to an existing File Geodatabase or an enterprise database connection file (.sde)
outGDB = r'D:\data\covid\MyProject\MyProject.gdb'        #e.g. r'c:\data\NYTimesCovid19TimeSeries\NYT.gdb' or r'c:\data\NYTimesCovid19TimeSeries\myEnterpriseDB.sde'
#   name of a table - gets created when it does not exist
#     when a table with this name exist, all data gets deleted from the table and the schema of the table must match with the field-list provided later in this script
outTableName = 'NYTCovid19_TimeSeriesCases'

# Step 2 of 2: 
# please 
#       (a) download the following counties dataset and 
#           - https://www.arcgis.com/home/item.html?id=53935d5d1c8540539d290072fcda77c1
#             this dataset is NOT an authenticated county dataset rather updated to match how NYTime is reporting
#             more info about NYTimes geographic exceptions: https://github.com/nytimes/covid-19-data#geographic-exceptions
#       (b) store/save that in the same database that specified above in line #10 to 'outGDB' variable
# Note: Windows Task Scheduler can be used to execute this script in the background at a certain time every day to keep the table in updated in your geodatabase

# downloading csv file
print('Downloading NYTimes time series data from github from: ' + NYTConvid19USCountyDataURL)
urllib.request.urlretrieve(NYTConvid19USCountyDataURL, csvFileName)

# creating/updating a table in a geodatabase
fullTableName = r'{0}\{1}'.format(outGDB, outTableName)
field_mapping = 'date "date" true true false 8 Date 0 0,First,#,{0},date,-1,-1;'.format(csvFileName)
field_mapping += 'county "county" true true false 50 Text 0 0,First,#,{0},county,0,50;'.format(csvFileName)
field_mapping += 'state "state" true true false 30 Text 0 0,First,#,{0},state,0,20;'.format(csvFileName)
field_mapping += 'fips "fips" true true false 5 Text 0 0,First,#,{0},fips,-1,-1;'.format(csvFileName)
field_mapping += 'cases "cases" true true false 4 Long 0 0,First,#,{0},cases,-1,-1;'.format(csvFileName)
field_mapping += 'deaths "deaths" true true false 4 Long 0 0,First,#,{0},deaths,-1,-1'.format(csvFileName)

if not arcpy.Exists(r'{0}\{1}'.format(outGDB, outTableName)):
    arcpy.conversion.TableToTable(csvFileName, outGDB, outTableName, '', field_mapping, '')
    arcpy.management.AddIndex(fullTableName, "date", "indxDate", "NON_UNIQUE", "NON_ASCENDING")
    arcpy.management.AddIndex(fullTableName, "fips", "indxFips", "NON_UNIQUE", "NON_ASCENDING")
    print('Data copied to {0}. Indexes are created on date and fips fields at {1}'.format(fullTableName, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
else:
    arcpy.management.TruncateTable(fullTableName)
    arcpy.management.Append(csvFileName, fullTableName, "NO_TEST", field_mapping, '', '')
    print('Table: {0} is updated at {1}'.format(fullTableName, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

tableView = arcpy.management.MakeTableView(fullTableName, "NYT_View")

# post-processing county FIPS
print('Adding leading 0 in front of some fips that get dropped during conversion process')
expression = "fixFips(!fips!)"
codeblock = """
def fixFips(fips):
    if (fips != None):
        if (len(fips) == 4):
            return '0' + fips
        else:
            return fips"""
arcpy.management.CalculateField(tableView, "fips", expression, "PYTHON3", codeblock)

# there are some geomgrpahic expections in NYTimes time series data
# https://github.com/nytimes/covid-19-data#geographic-exceptions
# Updating records for NYC and Kansas City, MO with some made FIPS
# so they get joined correct with the US County data, that is adjusted for NYTimes time series data, from ...
print('Adding some made up FIPS for New York City, NY and Kansas City, MO')
arcpy.management.SelectLayerByAttribute(tableView, "NEW_SELECTION", "county = 'New York City' And state = 'New York'", None)
arcpy.management.CalculateField(tableView, "fips", "36999", "PYTHON3", '')
arcpy.management.SelectLayerByAttribute(tableView, "NEW_SELECTION", "county = 'Kansas City' And state = 'Missouri'", None)
arcpy.management.CalculateField(tableView, "fips", "29999", "PYTHON3", '')
arcpy.management.SelectLayerByAttribute(tableView, "CLEAR_SELECTION")
arcpy.management.SelectLayerByAttribute(tableView, "NEW_SELECTION", "county = 'Lac qui Parle' And state = 'Minnesota'", None)
if int(arcpy.GetCount_management(tableView)[0]) > 0:
    arcpy.management.CalculateField(tableView, "county", "Lake of the Woods", "PYTHON3", '')
arcpy.management.SelectLayerByAttribute(tableView, "NEW_SELECTION", "county = 'Unknown'", None)
if int(arcpy.GetCount_management(tableView)[0]) > 0:
    arcpy.management.DeleteRows(tableView)

#os.remove(csvFileName)
print("Finished successfully!")