import arcpy
arcpy.management.CalculateField("CO_time_series_confirmed_state_20200406", "CO_time_series_confirmed_state_20200406.GEOID", "!Colorado_COVID19_Project.GEOID1!", "PYTHON3", '', "TEXT")
