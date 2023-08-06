
/**
 * on change of dropdown
 * Update selected chart
 */
var onChartChanged = function(event){
    document.getElementById("visualization").style.visibility = "visible";
    showVisuLoadingSpinner();
    plot_selected = $("#select-chart-dropdown-form :selected").attr("value");
    console.log(plot_selected);
    $.ajax({
        url : 'select-chart-dropdown-form',
        type : "POST",
        data : {
            plot_selected,
        },
        success: function(data){
            hideVisuLoadingSpinner();
            // Refresh plots after they were updated
            $("#visualization").html(data.script);
        },
        error: function(data){
            console.log("Error");
        }
    });
}

// .ready() called.
$(function() {
    // bind change event to dropdown box
    $("#select-chart-dropdown-form").on("change", onChartChanged);
});