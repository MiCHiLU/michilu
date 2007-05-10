lib_urls = {
	"jQuery": "/static/lib/jQuery/jquery-1.1.2.js",
	"jQuery_pack": "/static/lib/jQuery/jquery-1.1.2.pack.js",

	"MochiKit": "/static/lib/MochiKit/packed/MochiKit.js",
	"MochiKit_selected": "/static/lib/MochiKit/packed/selected.js",

	"Async":		"/static/lib/MochiKit/Async.js",
	"Base":			"/static/lib/MochiKit/Base.js",
	"Color":		"/static/lib/MochiKit/Color.js",
	"Controls":		"/static/lib/MochiKit/Controls.js",
	"DOM":			"/static/lib/MochiKit/DOM.js",
	"DateTime":		"/static/lib/MochiKit/DateTime.js",
	"DragAndDrop":	"/static/lib/MochiKit/DragAndDrop.js",
	"Format":		"/static/lib/MochiKit/Format.js",
	"Iter":			"/static/lib/MochiKit/Iter.js",
	"Logging":		"/static/lib/MochiKit/Logging.js",
	"LoggingPane":	"/static/lib/MochiKit/LoggingPane.js",
	"MochiKit":		"/static/lib/MochiKit/MochiKit.js",
	"MockDOM":		"/static/lib/MochiKit/MockDOM.js",
	"Position":		"/static/lib/MochiKit/Position.js",
	"Selector":		"/static/lib/MochiKit/Selector.js",
	"Signal":		"/static/lib/MochiKit/Signal.js",
	"Sortable":		"/static/lib/MochiKit/Sortable.js",
	"Style":		"/static/lib/MochiKit/Style.js",
	"Test":			"/static/lib/MochiKit/Test.js",
	"Visual": 		"/static/lib/MochiKit/Visual.js",

	//"debug": 		"/static/lib/debug.js",
	"":""
};

var load_lists = [];
try{
	load_lists = load_lists.concat(load);
}catch(e){}
/*
if (debug) {
	load_lists.push("debug");
}
*/

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

//js_load(lib_urls["jQuery_pack"]);
loading(load_lists);


