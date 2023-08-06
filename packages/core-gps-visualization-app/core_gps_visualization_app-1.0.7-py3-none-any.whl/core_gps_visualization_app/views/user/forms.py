"""Visualization forms"""
from django import forms


class SelectXParameterDropDown(forms.Form):
    """Form to select X parameter for the chart

    """
    x_parameters = forms.ChoiceField(label='Select X', required=True, widget=forms.Select())

    def __init__(self, params, *args):
        super(SelectXParameterDropDown, self).__init__(*args)
        x_parameters = params
        self.initial['x_parameters'] = [x_parameters[0][0]]
        self.fields['x_parameters'].choices = x_parameters


class SelectYParameterDropDown(forms.Form):
    """Form to select Y parameter for the chart

    """
    y_parameters = forms.ChoiceField(label='Select Y', required=True, widget=forms.Select())

    def __init__(self, params, *args):
        super(SelectYParameterDropDown, self).__init__(*args)
        y_parameters = params
        self.initial['y_parameters'] = [y_parameters[0][0]]
        self.fields['y_parameters'].choices = y_parameters


class SelectDataSourceCheckBox(forms.Form):
    """Form to select data source to pull data from for the chart

    """
    data_source = forms.MultipleChoiceField(label='Select Data Source', required=False, widget=forms.CheckboxSelectMultiple())

    def __init__(self, source, *args):
        super(SelectDataSourceCheckBox, self).__init__(*args)
        self.initial['data_source'] = source
        self.fields['data_source'].choices = [(source[i], source[i]) for i in range(0, len(source))]

