(function () {
    "use strict";
    function e(e) {
        function a(i, a) {
            var l, h;
            var m = i == window;
            var g = a && a.message !== undefined ? a.message : undefined;
            a = e.extend({}, e.blockUI.defaults, a || {});
            if (a.ignoreIfBlocked && e(i).data("blockUI.isBlocked"))return;
            a.overlayCSS = e.extend({}, e.blockUI.defaults.overlayCSS, a.overlayCSS || {});
            l = e.extend({}, e.blockUI.defaults.css, a.css || {});
            if (a.onOverlayClick)a.overlayCSS.cursor = "pointer";
            h = e.extend({}, e.blockUI.defaults.themedCSS, a.themedCSS || {});
            g = g === undefined ? a.message : g;
            if (m && o)f(window, {fadeOut: 0});
            if (g && typeof g != "string" && (g.parentNode || g.jquery)) {
                var y = g.jquery ? g[0] : g;
                var b = {};
                e(i).data("blockUI.history", b);
                b.el = y;
                b.parent = y.parentNode;
                b.display = y.style.display;
                b.position = y.style.position;
                if (b.parent)b.parent.removeChild(y)
            }
            e(i).data("blockUI.onUnblock", a.onUnblock);
            var w = a.baseZ;
            var E, S, x, T;
            if (n || a.forceIframe)E = e('<iframe class="blockUI" style="z-index:' + w++ + ';display:none;border:none;margin:0;padding:0;position:absolute;width:100%;height:100%;top:0;left:0" src="' + a.iframeSrc + '"></iframe>'); else E = e('<div class="blockUI" style="display:none"></div>');
            if (a.theme)S = e('<div class="blockUI blockOverlay ui-widget-overlay" style="z-index:' + w++ + ';display:none"></div>'); else S = e('<div class="blockUI blockOverlay" style="z-index:' + w++ + ';display:none;border:none;margin:0;padding:0;width:100%;height:100%;top:0;left:0"></div>');
            if (a.theme && m) {
                T = '<div class="blockUI ' + a.blockMsgClass + ' blockPage ui-dialog ui-widget ui-corner-all" style="z-index:' + (w + 10) + ';display:none;position:fixed">';
                if (a.title) {
                    T += '<div class="ui-widget-header ui-dialog-titlebar ui-corner-all blockTitle">' + (a.title || " ") + "</div>"
                }
                T += '<div class="ui-widget-content ui-dialog-content"></div>';
                T += "</div>"
            } else if (a.theme) {
                T = '<div class="blockUI ' + a.blockMsgClass + ' blockElement ui-dialog ui-widget ui-corner-all" style="z-index:' + (w + 10) + ';display:none;position:absolute">';
                if (a.title) {
                    T += '<div class="ui-widget-header ui-dialog-titlebar ui-corner-all blockTitle">' + (a.title || " ") + "</div>"
                }
                T += '<div class="ui-widget-content ui-dialog-content"></div>';
                T += "</div>"
            } else if (m) {
                T = '<div class="blockUI ' + a.blockMsgClass + ' blockPage" style="z-index:' + (w + 10) + ';display:none;position:fixed"></div>'
            } else {
                T = '<div class="blockUI ' + a.blockMsgClass + ' blockElement" style="z-index:' + (w + 10) + ';display:none;position:absolute"></div>'
            }
            x = e(T);
            if (g) {
                if (a.theme) {
                    x.css(h);
                    x.addClass("ui-widget-content")
                } else x.css(l)
            }
            if (!a.theme)S.css(a.overlayCSS);
            S.css("position", m ? "fixed" : "absolute");
            if (n || a.forceIframe)E.css("opacity", 0);
            var N = [E, S, x], C = m ? e("body") : e(i);
            e.each(N, function () {
                this.appendTo(C)
            });
            if (a.theme && a.draggable && e.fn.draggable) {
                x.draggable({handle: ".ui-dialog-titlebar", cancel: "li"})
            }
            var k = s && (!e.support.boxModel || e("object,embed", m ? null : i).length > 0);
            if (r || k) {
                if (m && a.allowBodyStretch && e.support.boxModel)e("html,body").css("height", "100%");
                if ((r || !e.support.boxModel) && !m) {
                    var L = v(i, "borderTopWidth"), A = v(i, "borderLeftWidth");
                    var O = L ? "(0 - " + L + ")" : 0;
                    var M = A ? "(0 - " + A + ")" : 0
                }
                e.each(N, function (e, t) {
                    var n = t[0].style;
                    n.position = "absolute";
                    if (e < 2) {
                        if (m)n.setExpression("height", "Math.max(document.body.scrollHeight, document.body.offsetHeight) - (jQuery.support.boxModel?0:" + a.quirksmodeOffsetHack + ') + "px"'); else n.setExpression("height", 'this.parentNode.offsetHeight + "px"');
                        if (m)n.setExpression("width", 'jQuery.support.boxModel && document.documentElement.clientWidth || document.body.clientWidth + "px"'); else n.setExpression("width", 'this.parentNode.offsetWidth + "px"');
                        if (M)n.setExpression("left", M);
                        if (O)n.setExpression("top", O)
                    } else if (a.centerY) {
                        if (m)n.setExpression("top", '(document.documentElement.clientHeight || document.body.clientHeight) / 2 - (this.offsetHeight / 2) + (blah = document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop) + "px"');
                        n.marginTop = 0
                    } else if (!a.centerY && m) {
                        var r = a.css && a.css.top ? parseInt(a.css.top, 10) : 0;
                        var i = "((document.documentElement.scrollTop ? document.documentElement.scrollTop : document.body.scrollTop) + " + r + ') + "px"';
                        n.setExpression("top", i)
                    }
                })
            }
            if (g) {
                if (a.theme)x.find(".ui-widget-content").append(g); else x.append(g);
                if (g.jquery || g.nodeType)e(g).show()
            }
            if ((n || a.forceIframe) && a.showOverlay)E.show();
            if (a.fadeIn) {
                var _ = a.onBlock ? a.onBlock : t;
                var D = a.showOverlay && !g ? _ : t;
                var P = g ? _ : t;
                if (a.showOverlay)S._fadeIn(a.fadeIn, D);
                if (g)x._fadeIn(a.fadeIn, P)
            } else {
                if (a.showOverlay)S.show();
                if (g)x.show();
                if (a.onBlock)a.onBlock()
            }
            c(1, i, a);
            if (m) {
                o = x[0];
                u = e(a.focusableElements, o);
                if (a.focusInput)setTimeout(p, 20)
            } else d(x[0], a.centerX, a.centerY);
            if (a.timeout) {
                var H = setTimeout(function () {
                    if (m)e.unblockUI(a); else e(i).unblock(a)
                }, a.timeout);
                e(i).data("blockUI.timeout", H)
            }
        }

        function f(t, n) {
            var r;
            var i = t == window;
            var s = e(t);
            var a = s.data("blockUI.history");
            var f = s.data("blockUI.timeout");
            if (f) {
                clearTimeout(f);
                s.removeData("blockUI.timeout")
            }
            n = e.extend({}, e.blockUI.defaults, n || {});
            c(0, t, n);
            if (n.onUnblock === null) {
                n.onUnblock = s.data("blockUI.onUnblock");
                s.removeData("blockUI.onUnblock")
            }
            var h;
            if (i)h = e("body").children().filter(".blockUI").add("body > .blockUI"); else h = s.find(">.blockUI");
            if (n.cursorReset) {
                if (h.length > 1)h[1].style.cursor = n.cursorReset;
                if (h.length > 2)h[2].style.cursor = n.cursorReset
            }
            if (i)o = u = null;
            if (n.fadeOut) {
                r = h.length;
                h.stop().fadeOut(n.fadeOut, function () {
                    if (--r === 0)l(h, a, n, t)
                })
            } else l(h, a, n, t)
        }

        function l(t, n, r, i) {
            var s = e(i);
            if (s.data("blockUI.isBlocked"))return;
            t.each(function (e, t) {
                if (this.parentNode)this.parentNode.removeChild(this)
            });
            if (n && n.el) {
                n.el.style.display = n.display;
                n.el.style.position = n.position;
                if (n.parent)n.parent.appendChild(n.el);
                s.removeData("blockUI.history")
            }
            if (s.data("blockUI.static")) {
                s.css("position", "static")
            }
            if (typeof r.onUnblock == "function")r.onUnblock(i, r);
            var o = e(document.body), u = o.width(), a = o[0].style.width;
            o.width(u - 1).width(u);
            o[0].style.width = a
        }

        function c(t, n, r) {
            var i = n == window, s = e(n);
            if (!t && (i && !o || !i && !s.data("blockUI.isBlocked")))return;
            s.data("blockUI.isBlocked", t);
            if (!i || !r.bindEvents || t && !r.showOverlay)return;
            var u = "mousedown mouseup keydown keypress keyup touchstart touchend touchmove";
            if (t)e(document).bind(u, r, h); else e(document).unbind(u, h)
        }

        function h(t) {
            if (t.type === "keydown" && t.keyCode && t.keyCode == 9) {
                if (o && t.data.constrainTabKey) {
                    var n = u;
                    var r = !t.shiftKey && t.target === n[n.length - 1];
                    var i = t.shiftKey && t.target === n[0];
                    if (r || i) {
                        setTimeout(function () {
                            p(i)
                        }, 10);
                        return false
                    }
                }
            }
            var s = t.data;
            var a = e(t.target);
            if (a.hasClass("blockOverlay") && s.onOverlayClick)s.onOverlayClick();
            if (a.parents("div." + s.blockMsgClass).length > 0)return true;
            return a.parents().children().filter("div.blockUI").length === 0
        }

        function p(e) {
            if (!u)return;
            var t = u[e === true ? u.length - 1 : 0];
            if (t)t.focus()
        }

        function d(e, t, n) {
            var r = e.parentNode, i = e.style;
            var s = (r.offsetWidth - e.offsetWidth) / 2 - v(r, "borderLeftWidth");
            var o = (r.offsetHeight - e.offsetHeight) / 2 - v(r, "borderTopWidth");
            if (t)i.left = s > 0 ? s + "px" : "0";
            if (n)i.top = o > 0 ? o + "px" : "0"
        }

        function v(t, n) {
            return parseInt(e.css(t, n), 10) || 0
        }

        e.fn._fadeIn = e.fn.fadeIn;
        var t = e.noop || function () {
        };
        var n = /MSIE/.test(navigator.userAgent);
        var r = /MSIE 6.0/.test(navigator.userAgent) && !/MSIE 8.0/.test(navigator.userAgent);
        var i = document.documentMode || 0;
        var s = e.isFunction(document.createElement("div").style.setExpression);
        e.blockUI = function (e) {
            a(window, e)
        };
        e.unblockUI = function (e) {
            f(window, e)
        };
        e.growlUI = function (t, n, r, i) {
            var s = e('<div class="growlUI"></div>');
            if (t)s.append("<h1>" + t + "</h1>");
            if (n)s.append("<h2>" + n + "</h2>");
            if (r === undefined)r = 3e3;
            var o = function (t) {
                t = t || {};
                e.blockUI({message: s, fadeIn: typeof t.fadeIn !== "undefined" ? t.fadeIn : 700, fadeOut: typeof t.fadeOut !== "undefined" ? t.fadeOut : 1e3, timeout: typeof t.timeout !== "undefined" ? t.timeout : r, centerY: false, showOverlay: false, onUnblock: i, css: e.blockUI.defaults.growlCSS})
            };
            o();
            var u = s.css("opacity");
            s.mouseover(function () {
                o({fadeIn: 0, timeout: 3e4});
                var t = e(".blockMsg");
                t.stop();
                t.fadeTo(300, 1)
            }).mouseout(function () {
                e(".blockMsg").fadeOut(1e3)
            })
        };
        e.fn.block = function (t) {
            if (this[0] === window) {
                e.blockUI(t);
                return this
            }
            var n = e.extend({}, e.blockUI.defaults, t || {});
            this.each(function () {
                var t = e(this);
                if (n.ignoreIfBlocked && t.data("blockUI.isBlocked"))return;
                t.unblock({fadeOut: 0})
            });
            return this.each(function () {
                if (e.css(this, "position") == "static") {
                    this.style.position = "relative";
                    e(this).data("blockUI.static", true)
                }
                this.style.zoom = 1;
                a(this, t)
            })
        };
        e.fn.unblock = function (t) {
            if (this[0] === window) {
                e.unblockUI(t);
                return this
            }
            return this.each(function () {
                f(this, t)
            })
        };
        e.blockUI.version = 2.65;
        e.blockUI.defaults = {message: "<h1>Please wait...</h1>", title: null, draggable: true, theme: false, css: {padding: 0, margin: 0, width: "30%", top: "40%", left: "35%", textAlign: "center", color: "#000", border: "3px solid #aaa", backgroundColor: "#fff", cursor: "wait"}, themedCSS: {width: "30%", top: "40%", left: "35%"}, overlayCSS: {backgroundColor: "#000", opacity: .6, cursor: "wait"}, cursorReset: "default", growlCSS: {width: "350px", top: "10px", left: "", right: "10px", border: "none", padding: "5px", opacity: .6, cursor: "default", color: "#fff", backgroundColor: "#000", "-webkit-border-radius": "10px", "-moz-border-radius": "10px", "border-radius": "10px"}, iframeSrc: /^https/i.test(window.location.href || "") ? "javascript:false" : "about:blank", forceIframe: false, baseZ: 1e3, centerX: true, centerY: true, allowBodyStretch: true, bindEvents: true, constrainTabKey: true, fadeIn: 200, fadeOut: 400, timeout: 0, showOverlay: true, focusInput: true, focusableElements: ":input:enabled:visible", onBlock: null, onUnblock: null, onOverlayClick: null, quirksmodeOffsetHack: 4, blockMsgClass: "blockMsg", ignoreIfBlocked: false};
        var o = null;
        var u = []
    }

    if (typeof define === "function" && define.amd && define.amd.jQuery) {
        define(["jquery"], e)
    } else {
        e(jQuery)
    }
})()