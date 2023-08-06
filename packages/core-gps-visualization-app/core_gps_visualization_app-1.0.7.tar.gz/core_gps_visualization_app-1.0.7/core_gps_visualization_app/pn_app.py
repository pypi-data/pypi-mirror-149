import panel as pn

#from core_gps_visualization_app.test import Chart
from core_gps_visualization_app.charts import Chart


def app(doc):
    chart = Chart()
    row = pn.Row(pn.Column(chart.param), chart.update_plot)
    row.server_doc(doc)

