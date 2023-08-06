"""Data config file"""


# Configure visualizations
# 1 XML file = All data (sorted) for a single parameter associated with a variable.

# Example1: Experience that measure temperature over time would have time as variable and temperature as parameter.
# Example2: Experience that measure Oxygen level in function of elevation would have
# oxygen as parameter and elevation as variable.

# If too much data for a single file, can be split in 'parts'

# In the path, '.' starts a dict
# In the path, '/' starts a list of dicts


# 'info_parameters' defines where to find the parameters names in the schema (ie. what can be a 'xName' or an 'yName')
# 'parameterPartPath' can be found when a single parameter is split in different documents
# (example: all data for a parameter named 'temperature' would be more than the 16MB document size limit on MongoDB
# So it is split in several documents)
info_parameters = {
    'parameterNamePath': 'data.parameterInfo.parameterName',
    'parameterUnitPath': 'data.parameterInfo.unit',
    'parameterPartPath': 'data.parameterInfo.part',
    'variablePath': 'data.parameterValues.time',
    'valuePath': 'data.parameterValues.value'
}

# One variable per instance is supported
# Schema doesn't need to define the variable name
variable = 'Time (UTC)'


# 'list_parameters' defines the 'parameterName' that will match with what can be found at the 'parameterNamePath'
# 'displayName' is what will be displayed on the visualization to describe the 'parameterName'
list_parameters = [
    {
        'parameterName': 'clkacc',
        'displayName': 'Clock Accuracy',
    },
    {
        'parameterName': 'clkbias',
        'displayName': 'Clock Bias',
    },
    {
        'parameterName': 'clkdrift',
        'displayName': 'Clock Drift',
    },
    {
        'parameterName': 'pdop',
        'displayName': 'PDOP',
    },
    {
        'parameterName': 'tm0rising',
        'displayName': 'TM0 Rising',
    },
    {
        'parameterName': 'tpqerr',
        'displayName': 'TP Qerr',
    },
    {
        'parameterName': 'elevation',
        'displayName': 'Elevation',
    },
    {
        'parameterName': 'azimuth',
        'displayName': 'Azimuth',
    },
    {
        'parameterName': 'cno',
        'displayName': 'CNO',
    },
    {
        'parameterName': 'residual',
        'displayName': 'Residual',
    },
    {
        'parameterName': 'counter',
        'displayName': 'Counter',
    },
    {
        'parameterName': 'timeoffset',
        'displayName': 'Time Offset',
    }]

# Path where the data source is indicated
# Several MongoDB docs might share the same data source
info_data_source = {'dataSourcePath': 'data.parameterIds.dataOriginID'}

# Path where the id used to legend charts is used
# Allow user to control which parameters to overlay in the charts
info_id_legend = {'legendName': 'Satellite', 'legendPath': 'data.parameterIds.satelliteID'}

# 'idName' will appear on the plot to define a group
ids_parameters = [
    {
        'idName': 'Satellite',
        'idPath': 'data.parameterIds.satelliteID',
    }]
