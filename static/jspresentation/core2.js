    var parentTag = "div"
    var childTag = "div"
	var ns = {};

	if (document.addEventListener) {
		ns.attach = function(e, n, f) {
			e.addEventListener(n, f, false);
		};
	}
	else {
		ns.attach = function(e, n, f) {
			e.attachEvent('on' + n, f);
		};
	}

	if (document.removeEventListener) {
		ns.detach = function(e, n, f) {
			e.removeEventListener(n, f, false);
		};
	}
	else {
		ns.detach = function(e, n, f) {
			e.detachEvent('on' + n, f);
		};
	}

	ns.isIE = /MSIE/.test(navigator.userAgent);

	ns.stopEvent = window.stopEvent = function(event) {
		if (event.preventDefault) {
			event.preventDefault();
			event.stopPropagation();
		}
		else {
			event.returnValue = false;
			event.cancelBubble = true;
		}
	};

	ns.actions = [];
	ns._observe = function(name) { // optimized (scope)
		if(this[name]) return this[name]();
		return true;
	};
	ns.action = function(observer) {
		var elmPresen = document.body.getElementsByTagName(parentTag)[0];
		var childs = elmPresen.childNodes;
		var index = 0;
		//for (var i = 0, len = childs.length; i < len; i ++) if(childs[i].nodeName.toLowerCase() == childTag) index++;
		for (var i = 0, len = childs.length; i < len; i ++) index++;
		ns.actions[index - 1] = observer;
		observer.observe = ns._observe;
	};

	ns.PageManager = function() { this.initialize.apply(this, arguments) };
	ns.PageManager.prototype = {
		initialize: function() {
			this.index = 0;
			this.pages = [];
		},
		force: function(i) {
			this.index = i;

			for (var j = 0; j < this.pages.length; j ++) {
				this.pages[j].update(0);
			}
			this.pages[this.index].update(1);
		},
		go: function(i) {
			if (this.index == i) return;
			if (this.to == i) return;
			if (i < 0) return;
			if (this.pages.length < i) return;

			this.to = i;
			this.from = this.index;
			this.dir = (this.to - this.from) / Math.abs(this.to - this.from);
			if (!this.interval) {
				var self = this;
				this.interval = setInterval(function() { self.update() }, 10);
				this.update();
			}
		},
		next: function() {
//			if (this.pages[this.index].hasAction()) return this.pages[this.index].action();
			var i = this.index + 1;
			if (i < 0) return;
			if (this.pages.length < i) return;
			this.to = i;
			this.from = this.index;
			this.dir = (this.to - this.from) / Math.abs(this.to - this.from);
			this.update();
		},
		prev: function() {
			var i = this.index - 1;
			if (i < 0) return;
			if (this.pages.length < i) return;
			this.to = i;
			this.from = this.index;
			this.dir = (this.to - this.from) / Math.abs(this.to - this.from);
			this.update();
		},
		update: function() {
			if (this.dir < 0) {
				if(this.pages[this.index + this.dir].show() == false) return;
				this.index += this.dir;
				document.cookie = 'page=' + this.index;
			}
			else {
				if(this.pages[this.index].hide() == false) return;
				this.index += this.dir;
				if (this.pages[this.index])
					this.pages[this.index].update(1);
				document.cookie = 'page=' + this.index;
			}
			if (this.index == this.to && this.interval) {
				clearInterval(this.interval);
				delete this.interval;
			}
		},
		push: function(page) {
			this.pages.push(page);
			return this.pages;
		},
		last: function() {
			return this.pages[this.pages.length - 1];
		},
		first: function() {
			return this.pages[0];
		}
	};

	ns.Timer = {
		counter: 0,
		timers: {},
		loop: function() {
			var timers = ns.Timer.timers;
			for (var i in timers) timers[i]();
		},
		add: function(f) {
			this.timers[++this.counter] = f;
			if (!this.interval) for (var i in this.timers) { 
				this.interval = setInterval(this.loop, 40);
				break;
			}
			return this.counter;
		},
		remove: function(id) {
			delete this.timers[id];
			for (var i in this.timers) return;
			if (this.interval) {
				clearInterval(this.interval);
				delete this.interval;
			}
		}
	}

/*

	ns.Action = {};
	ns.Action.Flash = function(element) {
		var style1 = element.style;
		var style2 = element.firstChild.style;
		var fontSize = 50;
		var opacity = 0;
		style2.fontSize = fontSize + '%';
		if (isIE) style1.filter = 'alpha(opacity=' + Math.round(opacity * 100) + ')';
		else      style1.opacity = opacity;
		var isIE = ns.isIE;
		var interval = ns.Timer.add(function() {
			fontSize += 10;
			opacity += 0.2;
			style2.fontSize = fontSize + '%';
			if (isIE) style1.filter = 'alpha(opacity=' + Math.round(opacity * 100) + ')';
			else      style1.opacity = opacity;
			if(fontSize == 100) ns.Timer.remove(interval);
		})
	};

*/

	ns.Page = function() { this.initialize.apply(this, arguments) };
	ns.Page.count = 0;
	ns.Page.prototype = {
		initialize: function(opts) {
			this.actionObserver = ns.actions[ns.Page.count] || {observe:function(){}};

			this.actionObserver.observe('initializing');

			this.display = true;
			this.boerder = false;
			this.opacity = 1;
			this.element = opts.element;
			this.style = opts.element.style;
			this.opts = opts;

			this.element.className += ' page';
			this.style.zIndex = 100000 - ns.Page.count * 10;

			this.myIndex = ns.Page.count;

			if (ns.Page.count == 0) this.element.className += ' first-child';

			if (ns.Page.count % 2)  this.element.className += ' even';
			else                    this.element.className += ' odd';

			ns.Page.count++

/*
			this.actions = [];
			var childs = this.element.childNodes;
			for (var i = 0, len = childs.length; i < len; i ++) {
				var child = childs[i]
				var className = child.className || '';
				var result = className.match(/^(.*)Action$/)
				var action;
				if (result && (action = ns.Action[result[i]])) {
					with ({ action: action, element: child }) {
						this.actions.push(function() { action(element) });
					}
				}
			}
*/
			this.actionObserver.observe('initialized');

		},

/*
		action: function() {
			(this.actions.shift()||function(){}).apply(this);
		},
		hasAction: function() {
			return !! this.actions.length;
		},
*/

		hide: function() {
			if(this.actionObserver.observe('startHide') == false) return false;
			this.gain = this.hideGain;
			this.to = 0;
			if (!this.interval) {
				var self = this;
				this.interval = ns.Timer.add(function() { self.update(self.gain(self.opacity)) });
			}
		},
		hideGain: function(x) {
			return x - (0.02 * x + 0.18);
		},
		show: function() {
			if(this.actionObserver.observe('startShow') == false) return false;
			this.gain = this.showGain;
			this.to = 1;
			if (!this.interval) {
				var self = this;
				this.interval = ns.Timer.add(function() { self.update(self.gain(self.opacity)) });
			}
		},
		showGain: function(x) {
			return x + (0.02 * x + 0.18);
		},
		update: function(o) {
			style = this.style;
			isIE = ns.isIE;
			if (o < 0.01) {
				this.opacity = 0;
				if (this.border) {
					this.border = false;
					style.border = '';
				}
				this.actionObserver.observe('finishHide');
				if (this.display) { 
					this.display = false;
					style.display = 'none';
				}
				if(isIE) style.filter = '';
				else     style.opacity = '';
			}
			else {
				if (!this.display) {
					this.display = true;
					style.display = '';
				}
				if (o > 0.99) {
					o = this.opacity = 1;
					if (this.border) {
						this.border = false;
						style.border = '';
					}
					if(isIE) style.filter = '';
					else     style.opacity = '';
					var deleteNext = true;
					this.actionObserver.observe('finishShow');
				}
				else {
					this.opacity = o;
					if(isIE) style.filter = 'alpha(opacity=' + Math.round(this.opacity * 100) + ')';
					else     style.opacity = this.opacity;
					if (!this.border) {
						this.border = true;
						style.border = '1px solid #888';
					}
				}
				style.top = (1 - o) * 25 + '%';
				style.left = (1 - o) * 25 + '%';
				style.width = (o * 100) / 2 + 50 + '%';
				style.height = (o * 100) / 2 + 50 + '%';
				style.fontSize = (o * 100) / 2 + 50 + '%';

				if (deleteNext && ns.manager) {
					var p = ns.manager.pages[this.myIndex+1];
					if(p && p.display) p.update(0);
				}
			}
			if (this.opacity == this.to && this.interval) {
				ns.Timer.remove(this.interval);
				delete this.interval;
			}
		}
	};

	ns.loadHandler = function() {
	var _div = document.createElement('div');

/*
	document.body.appendChild(_div);
	_div.style.position = 'absolute';
	_div.style.top = '0px';
	_div.style.left = '0px';
	_div.style.background = 'transparent';
	_div.style.width = '100%';
	_div.style.height = '100%';
	_div.style.zIndex = '1000000';
*/
		var presenElems = document.body.childNodes;

		var presenElem;
		for (var i = 0, len = presenElems.length; i < len; i ++) {
			presenElem = presenElems[i];
			if (presenElem.nodeName.toLowerCase() == parentTag) break;
		}
		presenElem.id = 'jspresentation';
		var childs = presenElem.childNodes;
		var manager = new ns.PageManager();
		for (var i = 0, len = childs.length; i < len; i ++) {
			var child = childs[i];
			if (child.nodeName.toLowerCase() == childTag) {
    		//if (child.nodeName.toLowerCase() == "") {
				var page = new ns.Page({element: child, manager: manager});
				page.update(0);
				manager.push(page);
			}
		}
		manager.pages[0].update(1);
		ns.manager = manager;
		(ns.onload || function(){})();

		var styleElem = document.getElementById('presentation-style-sheet');
		ns.sheet = styleElem.sheet || styleElem.styleSheet;
		var rules = ns.sheet.cssRules || ns.sheet.rules;

		ns.styles = {};
		for (var i = 0, len = rules.length; i < len; i ++) {
			var rule = rules[i];
			var selector = rule.selectorText || '';
			if (selector.match(/^\s*.page\s*$/i)) {
				ns.styles.page = rule.style;
			}
			else if (selector.match(/^\s*#jspresentation\s*$/i)) {
				ns.styles.presen = rule.style;
			}
			else if (selector.match(/^\s*body\s*$/i)) {
				ns.styles.body = rule.style;
			}
		}

		ns.body = document.body;
		ns.html = document.documentElement;

		ns.resizeHandler();

		if (window.opera) { setTimeout(ns.resizeHandler, 0); }
		ns.styles.body.display = '';
		setTimeout(function() { try { force(eval(document.cookie.match(/page=(\d+)/)[1]), 0) } catch (e) {}  },0);
	};

	ns.resizeHandler = function() {
		ns.screenWidth = ns.html.clientWidth;
		ns.styles.page.width = ns.screenWidth + 'px';
		if (/Gecko|MSIE/.test(navigator.userAgent)) {
			ns.styles.page.height = ns.html.clientHeight + 'px';
		}
		else {
			ns.styles.page.height = '100%';
		}

		// TODO: ダミーオブジェクトによるフォント決定手法
		ns.styles.body.fontSize = ns.html.clientHeight / 5 + '%';
	};

	window.force = ns.froce = function(i) { ns.manager.force(i) };

	window.go = ns.go = function(i) { ns.manager.go(i) };

	window.next = ns.next = function() { ns.manager.next() };

	window.prev = ns.prev = function() { ns.manager.prev() };

	ns.contextmenuHandler = function(e) {
		e = e || window.event;
		ns.stopEvent(e);
	}

	ns.clickHandler = function(e) {
		e = e || window.event;
		if (e.button == 0) {
			ns.next();
			ns.stopEvent(e);
		}
		else {
			ns.prev();
			ns.stopEvent(e);
		}
	}

	ns.keypressHandler = function(e) {
		e = e || window.event;
		switch (e.charCode||e.keyCode) {
			case 37:
			ns.prev();
			ns.stopEvent(e);
			break;
			case 39:
			ns.next();
			ns.stopEvent(e);
			break;
			case 38: case 40:
			ns.stopEvent(e);
			break;
		}
	};

	ns.keydownHandler = function(e) {
		e = e || window.event;
		if (/MSIE/.test(navigator.userAgent)) ns.keypressHandler(e);
	};

	ns.keyupHandler = function() {
	};

	ns.unloadHandler = function() {
		ns.detach(window, 'load', ns.loadHandler);
		ns.detach(window, 'resize', ns.resizeHandler);
		ns.detach(window, 'unload', ns.unloadHandler);
		ns.detach(document, 'click', ns.clickHandler);
		ns.detach(document, 'keypress', ns.keypressHandler);
		ns.detach(document, 'keydown', ns.keydownHandler);
		ns.detach(document, 'keyup', ns.keyupHandler);
		ns.detach(document, 'contextmenu', ns.contextmenuHandler);
	};

	ns.attach(window, 'load', ns.loadHandler);
	ns.attach(window, 'resize', ns.resizeHandler);
	ns.attach(window, 'unload', ns.unloadHandler);
	ns.attach(document, 'click', ns.clickHandler);
	ns.attach(document, 'keypress', ns.keypressHandler);
	ns.attach(document, 'keydown', ns.keydownHandler);
	ns.attach(document, 'keyup', ns.keyupHandler);
	ns.attach(document, 'contextmenu', ns.contextmenuHandler);

	JSP = ns;
