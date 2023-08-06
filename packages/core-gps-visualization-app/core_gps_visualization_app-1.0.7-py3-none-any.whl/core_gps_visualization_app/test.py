import panel as pn
import holoviews as hv
import holoviews.operation.datashader as hd
import pandas as pd
import numpy as np
from collections import OrderedDict as odict
from holoviews.operation import decimate
import datashader as ds

hv.extension('bokeh')

import param


class Chart(param.Parameterized):
    plots_types = param.Selector(default="Scatter", objects=["Scatter", "Line", "Box"])
    #update = param.Action(lambda x: x.param.trigger('update'), label='Click here!')
    N = param.Selector(default="1.0", objects=["1.0", "3.0", "10.0"])

    def __init__(self, **params):
        super().__init__(**params)

    @param.depends('N')
    def update_plot(self, **kwargs):
        np.random.seed(1)
        print('click')
        self.N = self.N
        points = hv.Points(np.random.multivariate_normal((0, -2), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)))
        points2 = hv.Points(np.random.multivariate_normal((0, 2), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
                           label="Points2")
        points3 = hv.Points(np.random.multivariate_normal((3, 0), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
                           label="Points3")
        points4 = hv.Points(np.random.multivariate_normal((4, 4), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
                           label="Points4")
        # points5 = hv.Points(np.random.multivariate_normal((5, 2), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points5")
        # points6 = hv.Points(np.random.multivariate_normal((3, 6), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points6")
        # points7 = hv.Points(np.random.multivariate_normal((7, 4), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points7")
        # points8 = hv.Points(np.random.multivariate_normal((0, 8), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points8")
        # points9 = hv.Points(np.random.multivariate_normal((9, 0), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points9")
        # points10 = hv.Points(np.random.multivariate_normal((4, 10), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points10")
        # points11 = hv.Points(np.random.multivariate_normal((11, 2), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points11")
        # points12 = hv.Points(np.random.multivariate_normal((3, 12), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points12")
        # points13 = hv.Points(np.random.multivariate_normal((13, 4), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points13")
        # points14 = hv.Points(np.random.multivariate_normal((0, 14), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points14")
        # points15 = hv.Points(np.random.multivariate_normal((15, 0), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points15")
        # points16 = hv.Points(np.random.multivariate_normal((4, 16), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points16")
        # points17 = hv.Points(np.random.multivariate_normal((17, 2), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points17")
        # points18 = hv.Points(np.random.multivariate_normal((3, 18), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points18")
        # points19 = hv.Points(np.random.multivariate_normal((19, 4), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points19")
        # points20 = hv.Points(np.random.multivariate_normal((4, 20), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points20")
        # points21 = hv.Points(np.random.multivariate_normal((21, 2), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points21")
        # points22 = hv.Points(np.random.multivariate_normal((3, 22), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points22")
        # points23 = hv.Points(np.random.multivariate_normal((23, 4), [[0.1, 0.1], [0.1, float(self.N)]], (1000000,)),
        #                    label="Points23")

        #hd.dynspread.max_px = 5
        #hd.dynspread.threshold = 0.5
        #overlaid_chart = hd.datashade(hv.NdOverlay({points.label: points, points2.label: points2, points3.label: points3,
         #                                           points4.label: points4})).opts(width=1400, height=700)
        from datashader.colors import Sets1to3  # default datashade() and shade() color cycle

        overlaid_chart = hd.spread(hd.datashade(hv.NdOverlay({points.label: points, points2.label: points2, points3.label: points3,
                                                    points4.label: points4}, kdims='k'), aggregator=ds.by('k', ds.count()), color_key=Sets1to3 + ['#a3d0e4', '#89003e', '#38b29f']), px=4)

        # points5.label: points5, points6.label: points6, points7.label: points7,
        # points8.label: points8, points9.label: points9, points10.label: points10, points11.label: points11,
        # points12.label: points12, points13.label: points13, points14.label: points14, points15.label: points15,
        # points16.label: points16, points17.label: points17, points18.label: points18, points19.label: points19,
        # points20.label: points20, points21.label: points21, points22.label: points22, points23.label: points23
        # 'test5', 'test6', 'test7', 'test8',
        # 'test9', 'test10', 'test11', 'test12', 'test13', 'test14', 'test15', 'test16',
        # 'test17', 'test18', 'test19', 'test20', 'test21', 'test22', 'test23'
        #
        #color_key = list(enumerate(Sets1to3[0:4]))
        color_key = [(name, color) for name, color in zip(['test1', 'test2', 'test3', 'test4'], Sets1to3 + ['#a3d0e4', '#89003e', '#38b29f', '#9c4578', '#3e1515', '#8f329f', '#f0535a',
                              '#a3b0e4', '#ff5393', '#d57aa8', '#ee846d', '#96858f'])]
        color_points = hv.NdOverlay({k: hv.Points([0, 0], label=str(k)).opts(color=v, size=0) for k, v in color_key})

        #opts = dict(tools=["hover"], width=1400, height=700, legend_position='left', show_legend=True,
        #            legend_limit=100, show_frame=False)


        return (overlaid_chart * color_points).opts(hv.opts.RGB(height=500, width=750, show_grid=True, title='is this working'))


# Try columndata source update
def random_walk(n, f=5000):
    """Random walk in a 2D space, smoothed with a filter of length f"""
    xs = np.convolve(np.random.normal(0, 0.1, size=n), np.ones(f)/f).cumsum()
    ys = np.convolve(np.random.normal(0, 0.1, size=n), np.ones(f)/f).cumsum()
    xs += 0.1*np.sin(0.1*np.array(range(n-1+f))) # add wobble on x axis
    xs += np.random.normal(0, 0.005, size=n-1+f) # add measurement noise
    ys += np.random.normal(0, 0.005, size=n-1+f)
    return np.column_stack([xs, ys])