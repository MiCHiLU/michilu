lib_urls = {
	"MochiKit":"/static/lib/MochiKit/MochiKit.js",
	"Base":"/static/lib/MochiKit/Base.js",
	"Iter":"/static/lib/MochiKit/Iter.js",
	"DOM":"/static/lib/MochiKit/DOM.js",
	"Behavior":"/static/lib/behaviour.js",
	"cssQuery":"/static/lib/cssQuery/cssQuery-p.js",
	"modBehavior":"/static/lib/modifiedbehavior.js",
	"":""
};

var load_lists = ["cssQuery", "modBehavior", "Base", ];
try{
	load_lists = load_lists.concat(load);
}catch(e){}

function js_load(lib)
{
	if (document.documentElement){
		var l = document.createElement("script");
		l.id = lib;
		l.src = lib;
		l.type = "application/x-javascript";
		l.charset = "UTF-8";
		document.body.appendChild(l);
	} else {
		document.write('<script src="' + lib +
			'" type="application/x-javascript"></script>');
	}
}

function loading (load_lists)
{
	for ( var i=0; a = load_lists[i]; i++ ) {
		if (lib_urls[a]){
			a = lib_urls[a];
		}
		js_load(a);
	}
}

loading(load_lists);
