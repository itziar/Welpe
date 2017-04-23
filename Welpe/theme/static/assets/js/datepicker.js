$(document).ready(function(){
        $('#sandbox-container .input-daterange').datepicker({
            format: "yyyy-mm-dd",
			todayHighlight: true,
		    clearBtn: true,
		    orientation: "top auto",
		    todayBtn: "linked",
		    autoclose: true,
        });  
});