$(document).ready(function(){
	$("a[@id]").mouseover(function(){
		elm = $(this);
		if (typeof(elm.attr("href")) == "undefined"){
			elm.attr({href:"#" + elm.attr("id")});
		}
	});
});
