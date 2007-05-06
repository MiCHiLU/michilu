Behavior.register(
	'a[id]',
	function(el){
		el.onmouseover = function(){
			addPermalink(this);
		}
	}
);

/*
Behavior.register(
	'a[id]',
	function(el){
		el.onmouseout = function(){
			togglePermalink(this);
		}
	}
);
*/

Behavior.apply()

c = true;
