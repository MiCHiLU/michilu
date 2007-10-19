$(function(){
	$("#header").after(
		'<div id="toc" style="display: none;"><\/div>' +
		'<div id="navi">' +
			'<span id="help-switch">?<\/span>' +
			'<span id="gears-info"><\/span>' +
		'<\/div>' +
		'<div id="help" style="display: none;">' +
			'<h3>ヘルプ<\/h3>' +
			'<ul>' +
				'<li><span class="key">j<\/span> :次項目へ<\/li>' +
				'<li><span class="key">k<\/span> :前項目へ<\/li>' +
				'<li><span class="key">f<\/span> :下へ<\/li>' +
				'<li><span class="key">b<\/span> :上へ<\/li>' +
				'<li><span class="key">gg<\/span> :最初へ<\/li>' +
				'<li><span class="key">G<\/span> :最後へ<\/li>' +
				'<li><span class="key">i<\/span> :見出しを表示する<\/li>' +
				'<li><span class="key">P<\/span> :パラグラフを表示する<\/li>' +
				'<li><span class="key">?<\/span> :ヘルプを表示する\/隠す' +
					'<span class="close">[x]<\/span>' +
				'<\/li>' +
				//'<li><span class="key">I<\/span> :情報を表示する<\/li>' +
				'<li><span class="gears">Google Gears<\/span> menu:<\/li>' +
				//'<li><span class="key">F<\/span> :検索<\/li>' +
				'<li><span class="key">R<\/span> :キャッシュを更新する<\/li>' +
			'<\/ul>' +
		'<\/div>'
	);

	$("#help").css({
		background: "#1F1F1F",
		opacity: 0.85,
		bottom: "0px",
		color: "#FFFFFF",
		left: "0px",
		overflow: "auto",
		position: "fixed",
		width: "100%",
		height: "100px"
	}).css("font-size", "14px");

	$("#help h3")
	.css("font-size", "22px")
	.css("text-align", "center");

	$("#help li").css({
		float: "left",
		margin: "0px 10px"
	}).css("list-style-type", "none");

	$("#help .key").css({
		color: "yellow"
	});

	$("#help .close").css({
		color: "red"
	});

	$("#help *")
	.css("font-family", "Arial,Helvetica,sans-serif");

	$("#navi").css({
		position:"fixed", top:"0px", right:"0px"
	});

	if ($.browser.msie) {
		$("#navi").css({
			position:"absolute", top:"0px", right:"0px"
		});
	};

	$("#help-switch").click(function(){
		help();
	}).css({
		position:"relative", top:"0px", right:"0px", height:"24px", width:"24px",
		color:"yellow", display:"block"
	}).css("font-size", "20px").css("font-weight", "bold").css("text-align", "right")
	.mouseover(function(){
		$("#help-switch").css({color:"orange"});
	})
	.mouseout(function(){
		$("#help-switch").css({color:"yellow"});
	});

	$("#help .gears").click(function(){
		window.open(gears_url);
	}).mouseover(function(){
		$("#help .gears").css({color:"orange"});
	}).mouseout(function(){
		$("#help .gears").css({color:"white"});
	});

	$("#help .close").click(function(){
		help();
	}).mouseover(function(){
		$("#help .close").css("font-weight", "bold");
	}).mouseout(function(){
		$("#help .close").css("font-weight", "normal");
	});

	$("#gears-info").css({
		position:"relative", top:"0px", right:"4px", height:"12px", width:"40px",
		color:"#669966", display:"block"
	}).css("font-size", "10px").css("font-weight", "bold").css("text-align", "right")
	.mouseover(function(){
		$("#gears-info").css({color:"#99cc99"});
	})
	.mouseout(function(){
		$("#gears-info").css({color:"#669966"});
	});

	function _count (val) {
		var target = $("#gears-info");
		target.text((target.text()*1+val).toString());
	};

	var count = {
		counter: 0,
		target: $("#gears-info"),
		counting: function(val){
			count.counter += val;
			count.display(count.counter);
		},
		up: function(){count.counting(1)},
		down: function(){count.counting(-1)},
		reset: function(){
			count.counting((count.counter = 0));
		},
		display: function(val){
			count.target.text((val || "updated").toString());
			if (count.target.text() == "updated") {
				$("#gears-info")
				.removeAttr("onmouseover").removeAttr("onmouseout").removeAttr("onclick")
				.css({color:"lightgreen"});
			};
		}
	};

	//$("h1,h2,h3,h4,h5,h6").each(function(){
	$("h1,h2").each(function(){
		$(this).attr({"class":"head"});
	});

	// H1～H6タグより目次を生成する
	var idcount = 1;
	var toc = '';
	var currentlevel = 0;
	$(".head").each(function(){
		this.id = "toc_" + idcount;
		idcount++;
		var level = 0;
		if(this.nodeName.toLowerCase() == "h1") {
			level = 1;
		} else if(this.nodeName.toLowerCase() == "h2") {
			level = 2;
		} else if(this.nodeName.toLowerCase() == "h3") {
			level = 3;
		} else if(this.nodeName.toLowerCase() == "h4") {
			level = 4;
		} else if(this.nodeName.toLowerCase() == "h5") {
			level = 5;
		} else if(this.nodeName.toLowerCase() == "h6") {
			level = 6;
		}
		while(currentlevel < level) {
			toc += "<ol>";
			currentlevel++;
		}
		while(currentlevel > level) {
			toc += "<\/ol>";
			currentlevel--;
		}
				var id = $("span[@id],a[@id]", this);
		if (id.length != 0){
					toc += '<li><a href="#' + id[0].id + '" class="toc_jump">' + $(this).text() + "<\/a><\/li>\n";
				};
	});
	while(currentlevel > 0) {
		toc += "<\/ol>";
		currentlevel--;
	}

	$("#toc").html(toc).css({
		position:"fixed", top:"0%", right:"24px", height:"100%", width:"30%",
		background: "#1F1F1F"
	});

	$("a[@id]").mouseover(function(){
		elm = $(this);
		if (typeof(elm.attr("href")) == "undefined"){
			elm.attr({href:"#" + elm.attr("id")});
		}
	});

	var offset = 0;
	var height = 0;
	$(window).keypress(function (e) {
		var code = e.keyCode != 0 ? e.keyCode : e.charCode;
		offset = window.pageYOffset != 0 ? window.pageYOffset : document.body.scrollTop;
		height = window.innerHeight != 0 ? window.innerHeight : document.body.clientHeight;
		//alert(code);
		switch(code) {
			case 106:	//j
				next();
				break;
			case 107:	//k
				before();
				break;
			case 102:	//f
				forward();
				break;
			case 98:	//b
				backward();
				break;
			case 103:	//gg
				first();
				break;
			case 71:	//G
				last();
				break;
			case 70:	//F
				if (check_gears()) {
					search();
				} else {
					//alert("Hint !\nGoogle Gearsをインストールすると詳細な検索機能が利用できます。" + gears_url);
				};
				break;
			case 105:	//i
				index();
				break;
			case 80:	//P
				param();
				break;
			case 63:	//?
				help();
				break;
			case 82:	//(F|M)?R
				if (check_gears()) {
					var force = false;
					var f_msg = "Force Reload ?\nデータのすべてをリロードしますか？";
					var m_msg = "Manifest Reload ?\nマニフェストをリロードしますか？";
					if (params.last_code == 70/*F*/ && confirm(f_msg)) {
						force = true;
						restore_manifest();
					} else if (params.last_code == 77/*M*/ && confirm(m_msg)) {
						restore_manifest();
					};
					checking_data(force);
				} else {
					alert("Hint !\nGoogle Gearsをインストールするとオフライン環境でも参照できます。" + gears_url);
				};
				break;
		};
		params.last_code = code;
	});

	function next () {
		for (var i=0; i < params.head.list.length; i++) {
			if ( offset < params.head.list[i].offsetTop) {
				window.scrollTo(0,params.head.list[i].offsetTop);
				break;
			};
		};
	};

	function before () {
		for (var i=0; i < params.head.list.length; i++) {
			if (!i) {
				continue;
			};
			if ( offset <= params.head.list[i].offsetTop) {
				window.scrollTo(0,params.head.list[i-1].offsetTop);
				break;
			};
		};
	};

	function forward () {
		window.scrollBy(0,height);
	};

	function backward () {
		window.scrollBy(0,-height);
	};

	function first () {
		if (params.last_code == 103) {
			params.head.index = 0;
			window.scrollTo(0,params.head.list[params.head.index].offsetTop);
		};
	};

	function last () {
		params.head.index = params.head.list.length - 1;
		window.scrollTo(0,params.head.list[params.head.index].offsetTop);
	};

	function search () {
	};

	function index () {
		$("#toc").toggle("normal");
	};

	function param () {
		var prefix = " \u00B6 ";	//¶
		$("span[@id]").each(function () {
			var text = $(this).text();
			if (text == "") {
				$(this).html('<a href="#'+this.id+'">'+prefix+'</a>');
			} else if (text == prefix) {
				$(this).html("");
			};
		});
	};

	function help () {
		$("#help").toggle();
	};

	var params = {};
	params.head = {};
	$("h1,h2,h3,h4,h5,h6").each(function(){
		$(this).addClass("head");
	});
	params.head.list = $(".head");
	params.last_code = undefined;


	// Google Gears

	var gears_url = "http://gears.google.com/";
	var localServer = data_store = media_store = 'undefined';
	var resorce = "/django/doc-ja.json";
	var gears_init = "/static/google/gears/gears_init.js";
	var manifest = "/django/doc-ja/resorce/manifest.json";
	var store_name = "test-data_store";
	var managed_store_name = "test-media_store";

	if (check_gears()) {
		$("#gears-info").text("go offline").click(function(){
			boot_localServer();
			store_manifest();
			checking_data();
		});
	} else {
		$("#gears-info").text("get Gears").click(function(){
			window.open(gears_url);
		});
	};

	var gears_url = "http://gears.google.com/";
	var localServer = data_store = media_store = 'undefined';
	var resorce = "/django/doc-ja.json";
	var gears_init = "/static/google/gears/gears_init.js";
	var manifest = "/django/doc-ja/resorce/manifest.json";
	var store_name = "test-data_store";
	var managed_store_name = "test-media_store";

	function is_type (type, target) {
		if (type != "string" && typeof(target) == "string") {
			try {
				target = eval(target.match("[_\\w\\-\\'\\.\\[\\]" + '\\"' + "]+")[0]);
			} catch (e) {
				return false;
			};
		};
		if (typeof(target) == type) {
			return true;
		};
		return false;
	};

	function is_object (target) {
		return is_type("object", target)
	};

	function check_gears () {
		if (is_object(window.google) && is_object("google.gears")) {
			return true;
		};
		return false;
	};

	function check_localServer () {
		if (check_gears() && is_object(localServer)) {
			return true;
		};
		return false;
	};

	function boot_localServer () {
		localServer = google.gears.factory.create('beta.localserver', '1.0');
		data_store = localServer.createStore(store_name);
	};

	function store_manifest () {
		media_store = localServer.createManagedStore(managed_store_name);
		media_store.manifestUrl = manifest;
		update_manifest();
	};

	function update_manifest () {
		media_store.checkForUpdate();
	};

	function restore_manifest () {
		if (!check_localServer()) {
			boot_localServer();
			store_manifest();
		};
		localServer.removeManagedStore(media_store.name);
		store_manifest();
		update_manifest();
	};

	function checking_data (force) {
		if (!check_localServer()) {
			boot_localServer();
		};
		$.getJSON(resorce, function(JSON){
			updating_data(JSON, force);
		});
	};

	function updating_data (JSON, force) {
		if (JSON.length) {
			JSON = JSON[0];
		};
		count.reset();
		for (var key in JSON){
			var url = valid_url(key);
			if (force) {
				count.up();
				data_store.capture(url, function(){count.down();});
			} else if (! url ||
				(data_store.isCaptured(url) &&
				Date.parse(JSON[key]) <= Date.parse(
					data_store.getHeader(url, "Last-Modified")))) {
					//pass
			} else {
				count.up();
				data_store.capture(url, function(){count.down();});
			};
		};
	};

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
});
