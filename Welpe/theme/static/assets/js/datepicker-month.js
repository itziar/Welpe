$(document).ready(function(){
    $('#sandbox-container input.month-filter ').datepicker({
            format: "yyyy-mm",
            minViewMode: 1,
            todayBtn: "linked",
            clearBtn: true,
            autoclose: true,
            todayHighlight: true,
            orientation: "top auto"
    });
 });