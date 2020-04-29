import arcpy
arcpy.management.SelectLayerByAttribute("CO_time_series_confirmed_state_20200406", "NEW_SELECTION", "COUNTY = 'Arapahoe'", None)
