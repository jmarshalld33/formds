$(document).ready(function(){

	// Makes rows selectable
    $('.selectable').on('click', function () {
    	var td = $(this).find('td');
        td.toggleClass('selected');
    });
    
    // Removes rows
	$("#removeRows").on('click', function(){
		$('td').not('.selected, .rounded-foot-left, .rounded-foot-right').remove();
		$('td').removeClass('selected');
	}); 
	
	// Check for browser type for table copy
	var ua = window.navigator.userAgent
	var msie = ua.indexOf ( "MSIE " )
	if ( msie > 0 ) {    // If Internet Explorer then copy to clipboard
		$('#btnExport').on('click', function() {
		   var thisTable = document.getElementById("exportToExcel").innerHTML;
		   window.clipboardData.setData("Text", thisTable);
		   var objExcel = new ActiveXObject ("Excel.Application");
		   objExcel.visible = true;
		
		   var objWorkbook = objExcel.Workbooks.Add;
		   var objWorksheet = objWorkbook.Worksheets(1);
		   objWorksheet.Paste;
		});
	}else {  // If another browser then export
		$("#btnExport").click(function(e) {
		    window.open('data:application/vnd.ms-excel,' + encodeURIComponent($('#exportToExcel').html()));
		    e.preventDefault();
		});
	}
	
	// Copy table to clipboard... IE only
/*	
	$('#btnExport').on('click', function() {
	   var thisTable = document.getElementById("exportToExcel").innerHTML;
	   window.clipboardData.setData("Text", thisTable);
	   var objExcel = new ActiveXObject ("Excel.Application");
	   objExcel.visible = true;
	   var objWorkbook = objExcel.Workbooks.Add;
	   var objWorksheet = objWorkbook.Worksheets(1);
	   objWorksheet.Paste;
	});
*/	
	// Disables ability to select text in the table
	var element = document.getElementsByTagName('table')[0];
    if (typeof element.onselectstart != 'undefined') {
        element.onselectstart = function() { return false; };
    } else if (typeof element.style.MozUserSelect != 'undefined') {
        element.style.MozUserSelect = 'none';
    } else {
        element.onmousedown = function() { return false; };
    }
});
