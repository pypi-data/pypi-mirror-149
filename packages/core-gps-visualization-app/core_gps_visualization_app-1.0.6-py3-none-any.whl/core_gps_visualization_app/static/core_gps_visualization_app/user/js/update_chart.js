
/**
 * on validate click
 * Update configuration objects
 */
var onValidate = function(event){
    //document.getElementById('visualization').innerHTML = "";
    $("#visualization").html("<img src='../../../static/core_gps_visualization_app/user/img/loading.gif' alt='loading bar'/>");
    showVisuLoadingSpinner();
    x_parameter = $("#select-x-dropdown-form :selected").attr("value");
    y_parameter = $("#select-y-dropdown-form :selected").attr("value");
    data_sources = $("#select-documents-checkbox-form :checked").map(function() {return this.value}).get();
    $.ajax({
        url:"validate-button",
        type : "POST",
        data : {
            x_parameter,
            y_parameter,
            data_sources
        },
        success: function(data) {
           updateChart();
        },
    error:function() {
        console.log("Error");
        $('#charts').html("Uh oh! An error has occurred. Please check back later...");
        }
    });
}

/**
 * on change of dropdown
 * Update selected time range
 */
var updateChart = function(event){
    $.ajax({
        url:"update-chart",
        success: function(data) {
            console.log("Success");
            $("#visualization").html(data.script);
            hideVisuLoadingSpinner();
        },
    error:function() {
        console.log("Error");
        }
    });
}

// .ready() called.
$(function() {
    // bind change event to validate button
    $("#validate").on("click", onValidate);
});