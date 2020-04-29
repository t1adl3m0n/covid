import arcpy
arcpy.stpm.CreateSpaceTimeCubeDefinedLocations("KansasProject", r"D:\data\covid\MyProject\covidKS20200417.nc", "FIPS1", "NO_TEMPORAL_AGGREGATION", "DATE", "1 Days", "END_TIME", None, "COUNT SPACE_TIME_NEIGHBORS", None, "KS_time_series20200417", "FIPS")
