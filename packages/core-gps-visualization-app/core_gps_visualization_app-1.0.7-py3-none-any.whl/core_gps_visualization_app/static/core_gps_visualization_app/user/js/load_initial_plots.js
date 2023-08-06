var showVisuLoadingSpinner = function() {
    document.getElementById('visualization-panel-transparent-bgd').style.visibility = "visible";
    document.getElementById('visualization-panel-transparent-bgd').style.height = "50px";
    document.getElementById('visualization-panel-loading').style.visibility = "visible";
}

var hideVisuLoadingSpinner = function() {
    document.getElementById('visualization-panel-transparent-bgd').style.visibility = "hidden";
    document.getElementById('visualization-panel-transparent-bgd').style.height = "0px";
    document.getElementById('visualization-panel-loading').style.visibility = "hidden";
}

var loadInitialPlots = function(event){
   //document.getElementById('visualization').innerHTML = "";
   $("#visualization").html("<img src='../../../static/core_gps_visualization_app/user/img/loading.gif' alt='loading bar'/>");
   showVisuLoadingSpinner();
   $.ajax({
    url:"load-initial-plots",
    success: function(data) {
        console.log("Success");
        $("#visualization").html(data.script);
        hideVisuLoadingSpinner();
     },
    error:function(){
           console.log("Error");
    }
    });
 }

 // .ready() called.
$(function() {
   loadInitialPlots();
});