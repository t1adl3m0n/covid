import arcpy
arcpy.analysis.Frequency("capstoneStates", r"D:\capstone\capstone\capDatePatternCategoryFreq.csv", "PATTERN;CATEGORY;DATE", None)
