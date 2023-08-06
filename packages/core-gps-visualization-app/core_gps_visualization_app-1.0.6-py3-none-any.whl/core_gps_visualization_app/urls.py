""" Url router for the gps visualization app
"""

from django.urls import re_path
import core_gps_visualization_app.views.user.ajax as user_ajax
import core_gps_visualization_app.views.user.views as user_views

urlpatterns = [
    re_path(r"^$", user_views.index,
            name="core_gps_visualization_index"),
    re_path(r"^load-initial-plots$", user_ajax.load_initial_plots,
            name="core_gps_visualization_load_initial_plots"),
    re_path(r"^validate-button", user_ajax.update_configurations,
            name='core_gps_visualization_update_configurations'),
    re_path(r"^update-chart", user_ajax.update_chart,
            name='core_gps_visualization_update_chart'),
]