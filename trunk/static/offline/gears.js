var resorce = "/django/doc-ja.json";

function update () {
	store.checkForUpdate();
}

function update_store (force) {
	$.getJSON(resorce, function(JSON){
		updating_store(JSON, force);
	});
}

function restore () {
	localServer.removeManagedStore(store.name);
	update();
}


var localServer = google.gears.factory.create('beta.localserver', '1.0');
var media_store = localServer.createStore('test-media_store');
var store = localServer.createManagedStore('test-store');
store.manifestUrl = "/static/offline/manifest.json";

//$("head > script", document).each(function(){alert($(this).attr("src"))})
function junk () {
	var protocol = window.location.protocol;
	var startswith = protocol + "\/\/" + window.location.hostname;
	$("img", document).each(function(){
		var src = $(this).attr("src");
		if (src.slice(0, protocol.length) != protocol){
		} else if (src.slice(0, startswith.length) == startswith){
			src = src.match(startswith+"(:\\d+)?(.*)")[2];
		} else {
			return;
		}
		alert(src);
	});
}

function valid_url (url) {
	var protocol = window.location.protocol;
	var startswith = protocol + "\/\/" + window.location.hostname;

	if (url.slice(0, protocol.length) != protocol){
	} else if (url.slice(0, startswith.length) == startswith){
		url = url.match(startswith+"(:\\d+)?(.*)")[2];
	} else {
		return false;
	}
	return url;
}

function updating_store (JSON, force) {
	if (JSON.length) {
		JSON = JSON[0];
	};
	for (var key in JSON){
		var url = valid_url(key);
		if (force) {
			media_store.capture(url, function(){});
		} else if (! url ||
			(media_store.isCaptured(url) &&
			Date.parse(JSON[key]) <= Date.parse(
				media_store.getHeader(url, "Last-Modified")))) {
				//pass
		} else {
			media_store.capture(url, function(){});
		};
	};
};

function _junk () {
	var resource_name = window.location.pathname.match("/doc-ja(.+)")[1];
	$.get("/django/doc-ja" + resource_name, function(source){
		document.title = source.match("<title>(.*?)<\/title>")[1]
			.replace(/(&lt;|&gt;|&quot;|&amp;)/g, function(key,value){
				return {
					'&lt;': '<',
					'&gt;': '>',
					'&quot;':'\"',
					'&amp;': '&'
				}[key];
			});
		$('<link></link>')
			.attr({
				type: "text/css",
				rel: "stylesheet",
				href: "/static/doc-ja/css/site.css"
			})
			.appendTo("html > head");
		$(document.body).html(source.match("<body>((.|\r?\n)*)<\/body>")[1]);
		$.each(source.match("<head>((.|\r?\n)*?)<\/head>")[1]
			.match(/<script(.|\r?\n)*?<\/script>/g), function(key,value){
				var src = valid_url(value.match('src="(.*?)"')[1]);
				if (src) {
					$.getScript(src);
				};
		});
	});
}

$(function(){
	update();
	update_store();
});
