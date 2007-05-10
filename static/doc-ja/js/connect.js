map(
	function(selected){
		connect(selected, "onmouseover", function(){add_permalink(this);});
	},
	$$("a[id]")
)

c = true;
