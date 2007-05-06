(function(ns) {
	var current = (function (e) {
		if( e.nodeName.toLowerCase() == 'script' ) return e;
			return arguments.callee(e.lastChild)
	})(document);

	ns.onload = function() {

		var logoUrl = current.src.replace(/main\.js$/, 'logo.jpg');
		var pages = ns.manager.pages;
		for (var i = 0, len = pages.length; i < len; i ++) {
			var parent = pages[i].element;

			// Print Header
			var divElem = document.createElement('div');
			divElem.className = 'print-only print-top-logo';
			var imageElem = document.createElement('img');
			imageElem.src = logoUrl;
			divElem.appendChild(imageElem);
			parent.insertBefore(divElem, parent.firstChild);
		}
	};
})(window.JSP);
