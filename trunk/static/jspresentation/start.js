//settings
charset = "UTF-8";
libBaseUrl = "/static/jspresentation/";

LIBs = {
    "css":  ["base.css", "document.css", "presentation.css", "print.css"],
    //"js":   ["core2.js","main.js"],
    "js":   ["core2_main.js"],
}

function loadLibs(libs, type) {
    for(i=0; (a = libs[i]); i++) {
        if(type == "css"){
            var lib = document.createElement("link");
            lib.id = a.split(".")[0] + "-style-sheet";
            lib.rel = "stylesheet";
            lib.type = "text/css";
            lib.href = libBaseUrl + a;
        }else if(type == "js"){
            var lib = document.createElement("script");
            lib.language = "javascript";
            lib.src = libBaseUrl + a;
        }
        document.body.appendChild(lib);
    }
}

function init() {

    for(i=0; (a = document.getElementsByTagName("link")[i]); i++) {
        if(a.getAttribute("rel").indexOf("style") != -1) {
            a.disabled = true;
        }
    }

    loadLibs(LIBs["css"], "css");
    loadLibs(LIBs["js"], "js");
}

//init();
