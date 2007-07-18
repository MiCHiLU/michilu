
$(function(){
    $("#header").after(
        '<div id="toc" style="display: none;"><\/div>' +
	'<div id="navi-cntl">' +
            '<span id="navi-switch">見出し<\/span>' +
            '<a href="..\/index\/" class="jump_toc">Django オンラインドキュメント和訳<\/a>' +
        '<\/div>'
    );
	
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
            position:"fixed", top:"20px", left:"70%", height:"100%", width:"30%",
            background: "black"
        });
        $("a.toc_jump").click(function(){
            $("#toc").toggle("normal");
        });

        $("#navi-cntl").css({
            position:"fixed", top:"0%", left:"70%", height:"20px", width:"30%",
            background: "black"
        }).show();

        $("#navi-switch").click(function(){
            $("#toc").toggle("normal");
        }).css({
            background: "white"
        });
});

// jqueryオブジェクトの中身をダンプする関数
function jdump($obj) {
	var dumphtml = [];
	if($.browser.msie) {
		for(var i = 0; i < $obj.length; i++) {
			dumphtml.push('[' + i + '] ');
			dumphtml.push($obj[i].outerHTML.replace(/^[\r\n\t]+/, ''));
			dumphtml.push("\n");
		}
	} else {
		for(var i = 0; i < $obj.length; i++) {
			dumphtml.push('[' + i + '] '
				+ '<' + $obj[i].nodeName.toLowerCase());
			for(var j = 0; j < $obj[i].attributes.length; j++) {
				dumphtml.push(' ' + $obj[i].attributes[j].nodeName + '="' 
					+ $obj[i].attributes[j].nodeValue + '"');
			}
			dumphtml.push('>' + $obj[i].innerHTML);
			dumphtml.push('<\/' + $obj[i].nodeName.toLowerCase() + '>');
			dumphtml.push("\n");
		}
	}
	alert(dumphtml.join(''));
}

