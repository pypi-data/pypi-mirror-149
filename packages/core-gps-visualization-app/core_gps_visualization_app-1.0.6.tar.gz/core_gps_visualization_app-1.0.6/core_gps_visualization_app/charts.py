from core_gps_visualization_app.tasks import build_visualization_data
from core_gps_visualization_app.components.plots.operations import plot_layout_by_time_range
from core_gps_visualization_app.utils import data_utils as utils
from core_gps_visualization_app.data_config import info_id_legend

import logging
import param
import holoviews as hv

logger = logging.getLogger(__name__)
hv.extension('bokeh')

# Init legend
legend_name = info_id_legend['legendName']
legend_path = info_id_legend['legendPath']
results = utils.query_data(legend_path)
for i in range(len(results)):
    results[i] = legend_name + ': ' + str(results[i])


class Chart(param.Parameterized):
    plot_selected = param.Selector(default="Scatter", objects=["Scatter", "Line"])
    time_selected = param.Selector(default="Seconds", objects=["Seconds", "Minutes", "Hours", "Days"])
    legend = param.ListSelector(default=results, objects=results)

    def __init__(self, **params):
        super().__init__(**params)

    @param.depends('plot_selected', 'time_selected', 'legend')
    def update_plot(self):
        self.plot_selected = self.plot_selected
        self.time_selected = self.time_selected
        self.legend = self.legend
        visualization_data = build_visualization_data(self.legend)
        if visualization_data is None:
            visualization_data = []
        if len(visualization_data) == 0:
            return '# No charts for this configuration...'
        chart = plot_layout_by_time_range(visualization_data, self.plot_selected, self.time_selected)

        return chart
