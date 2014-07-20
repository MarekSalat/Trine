(function (e, t, n) {
    (function (e) {
        typeof define == "function" && define.amd ? define(["jquery"], e) : jQuery && !jQuery.fn.sparkline && e(jQuery)
    })(function (r) {
        "use strict";
        var i = {}, s, o, u, f, l, h, p, d, v, m, g, y, w, E, S, x, T, N, C, k, L, A, O, M, _, D, P, H, B, j, F, I, q = 0;
        s = function () {
            return{common: {type: "line", lineColor: "#00f", fillColor: "#cdf", defaultPixelsPerValue: 3, width: "auto", height: "auto", composite: !1, tagValuesAttribute: "values", tagOptionsPrefix: "spark", enableTagOptions: !1, enableHighlight: !0, highlightLighten: 1.4, tooltipSkipNull: !0, tooltipPrefix: "", tooltipSuffix: "", disableHiddenCheck: !1, numberFormatter: !1, numberDigitGroupCount: 3, numberDigitGroupSep: ",", numberDecimalMark: ".", disableTooltips: !1, disableInteraction: !1}, line: {spotColor: "#f80", highlightSpotColor: "#5f5", highlightLineColor: "#f22", spotRadius: 1.5, minSpotColor: "#f80", maxSpotColor: "#f80", lineWidth: 1, normalRangeMin: n, normalRangeMax: n, normalRangeColor: "#ccc", drawNormalOnTop: !1, chartRangeMin: n, chartRangeMax: n, chartRangeMinX: n, chartRangeMaxX: n, tooltipFormat: new u('<span style="color: {{color}}">&#9679;</span> {{prefix}}{{y}}{{suffix}}')}, bar: {barColor: "#3366cc", negBarColor: "#f44", stackedBarColor: ["#3366cc", "#dc3912", "#ff9900", "#109618", "#66aa00", "#dd4477", "#0099c6", "#990099"], zeroColor: n, nullColor: n, zeroAxis: !0, barWidth: 4, barSpacing: 1, chartRangeMax: n, chartRangeMin: n, chartRangeClip: !1, colorMap: n, tooltipFormat: new u('<span style="color: {{color}}">&#9679;</span> {{prefix}}{{value}}{{suffix}}')}, tristate: {barWidth: 4, barSpacing: 1, posBarColor: "#6f6", negBarColor: "#f44", zeroBarColor: "#999", colorMap: {}, tooltipFormat: new u('<span style="color: {{color}}">&#9679;</span> {{value:map}}'), tooltipValueLookups: {map: {"-1": "Loss", 0: "Draw", 1: "Win"}}}, discrete: {lineHeight: "auto", thresholdColor: n, thresholdValue: 0, chartRangeMax: n, chartRangeMin: n, chartRangeClip: !1, tooltipFormat: new u("{{prefix}}{{value}}{{suffix}}")}, bullet: {targetColor: "#f33", targetWidth: 3, performanceColor: "#33f", rangeColors: ["#d3dafe", "#a8b6ff", "#7f94ff"], base: n, tooltipFormat: new u("{{fieldkey:fields}} - {{value}}"), tooltipValueLookups: {fields: {r: "Range", p: "Performance", t: "Target"}}}, pie: {offset: 0, sliceColors: ["#3366cc", "#dc3912", "#ff9900", "#109618", "#66aa00", "#dd4477", "#0099c6", "#990099"], borderWidth: 0, borderColor: "#000", tooltipFormat: new u('<span style="color: {{color}}">&#9679;</span> {{value}} ({{percent.1}}%)')}, box: {raw: !1, boxLineColor: "#000", boxFillColor: "#cdf", whiskerColor: "#000", outlierLineColor: "#333", outlierFillColor: "#fff", medianColor: "#f00", showOutliers: !0, outlierIQR: 1.5, spotRadius: 1.5, target: n, targetColor: "#4a2", chartRangeMax: n, chartRangeMin: n, tooltipFormat: new u("{{field:fields}}: {{value}}"), tooltipFormatFieldlistKey: "field", tooltipValueLookups: {fields: {lq: "Lower Quartile", med: "Median", uq: "Upper Quartile", lo: "Left Outlier", ro: "Right Outlier", lw: "Left Whisker", rw: "Right Whisker"}}}}
        }, D = '.jqstooltip { position: absolute;left: 0px;top: 0px;visibility: hidden;background: rgb(0, 0, 0) transparent;background-color: rgba(0,0,0,0.6);filter:progid:DXImageTransform.Microsoft.gradient(startColorstr=#99000000, endColorstr=#99000000);-ms-filter: "progid:DXImageTransform.Microsoft.gradient(startColorstr=#99000000, endColorstr=#99000000)";color: white;font: 10px arial, san serif;text-align: left;white-space: nowrap;padding: 5px;border: 1px solid white;z-index: 10000;}.jqsfield { color: white;font: 10px arial, san serif;text-align: left;}', o = function () {
            var e, t;
            return e = function () {
                this.init.apply(this, arguments)
            }, arguments.length > 1 ? (arguments[0] ? (e.prototype = r.extend(new arguments[0], arguments[arguments.length - 1]), e._super = arguments[0].prototype) : e.prototype = arguments[arguments.length - 1], arguments.length > 2 && (t = Array.prototype.slice.call(arguments, 1, -1), t.unshift(e.prototype), r.extend.apply(r, t))) : e.prototype = arguments[0], e.prototype.cls = e, e
        }, r.SPFormatClass = u = o({fre: /\{\{([\w.]+?)(:(.+?))?\}\}/g, precre: /(\w+)\.(\d+)/, init: function (e, t) {
            this.format = e, this.fclass = t
        }, render: function (e, t, r) {
            var i = this, s = e, o, u, a, f, l;
            return this.format.replace(this.fre, function () {
                var e;
                return u = arguments[1], a = arguments[3], o = i.precre.exec(u), o ? (l = o[2], u = o[1]) : l = !1, f = s[u], f === n ? "" : a && t && t[a] ? (e = t[a], e.get ? t[a].get(f) || f : t[a][f] || f) : (v(f) && (r.get("numberFormatter") ? f = r.get("numberFormatter")(f) : f = E(f, l, r.get("numberDigitGroupCount"), r.get("numberDigitGroupSep"), r.get("numberDecimalMark"))), f)
            })
        }}), r.spformat = function (e, t) {
            return new u(e, t)
        }, f = function (e, t, n) {
            return e < t ? t : e > n ? n : e
        }, l = function (e, n) {
            var r;
            return n === 2 ? (r = t.floor(e.length / 2), e.length % 2 ? e[r] : (e[r - 1] + e[r]) / 2) : e.length % 2 ? (r = (e.length * n + n) / 4, r % 1 ? (e[t.floor(r)] + e[t.floor(r) - 1]) / 2 : e[r - 1]) : (r = (e.length * n + 2) / 4, r % 1 ? (e[t.floor(r)] + e[t.floor(r) - 1]) / 2 : e[r - 1])
        }, h = function (e) {
            var t;
            switch (e) {
                case"undefined":
                    e = n;
                    break;
                case"null":
                    e = null;
                    break;
                case"true":
                    e = !0;
                    break;
                case"false":
                    e = !1;
                    break;
                default:
                    t = parseFloat(e), e == t && (e = t)
            }
            return e
        }, p = function (e) {
            var t, n = [];
            for (t = e.length; t--;)n[t] = h(e[t]);
            return n
        }, d = function (e, t) {
            var n, r, i = [];
            for (n = 0, r = e.length; n < r; n++)e[n] !== t && i.push(e[n]);
            return i
        }, v = function (e) {
            return!isNaN(parseFloat(e)) && isFinite(e)
        }, E = function (e, t, n, i, s) {
            var o, u;
            e = (t === !1 ? parseFloat(e).toString() : e.toFixed(t)).split(""), o = (o = r.inArray(".", e)) < 0 ? e.length : o, o < e.length && (e[o] = s);
            for (u = o - n; u > 0; u -= n)e.splice(u, 0, i);
            return e.join("")
        }, m = function (e, t, n) {
            var r;
            for (r = t.length; r--;) {
                if (n && t[r] === null)continue;
                if (t[r] !== e)return!1
            }
            return!0
        }, g = function (e) {
            var t = 0, n;
            for (n = e.length; n--;)t += typeof e[n] == "number" ? e[n] : 0;
            return t
        }, w = function (e) {
            return r.isArray(e) ? e : [e]
        }, y = function (t) {
            var n;
            e.createStyleSheet ? e.createStyleSheet().cssText = t : (n = e.createElement("style"), n.type = "text/css", e.getElementsByTagName("head")[0].appendChild(n), n[typeof e.body.style.WebkitAppearance == "string" ? "innerText" : "innerHTML"] = t)
        }, r.fn.simpledraw = function (t, i, s, o) {
            var u, f;
            if (s && (u = this.data("_jqs_vcanvas")))return u;
            if (r.fn.sparkline.canvas === !1)return!1;
            if (r.fn.sparkline.canvas === n) {
                var l = e.createElement("canvas");
                if (!l.getContext || !l.getContext("2d")) {
                    if (!e.namespaces || !!e.namespaces.v)return r.fn.sparkline.canvas = !1, !1;
                    e.namespaces.add("v", "urn:schemas-microsoft-com:vml", "#default#VML"), r.fn.sparkline.canvas = function (e, t, n, r) {
                        return new F(e, t, n)
                    }
                } else r.fn.sparkline.canvas = function (e, t, n, r) {
                    return new j(e, t, n, r)
                }
            }
            return t === n && (t = r(this).innerWidth()), i === n && (i = r(this).innerHeight()), u = r.fn.sparkline.canvas(t, i, this, o), f = r(this).data("_jqs_mhandler"), f && f.registerCanvas(u), u
        }, r.fn.cleardraw = function () {
            var e = this.data("_jqs_vcanvas");
            e && e.reset()
        }, r.RangeMapClass = S = o({init: function (e) {
            var t, n, r = [];
            for (t in e)e.hasOwnProperty(t) && typeof t == "string" && t.indexOf(":") > -1 && (n = t.split(":"), n[0] = n[0].length === 0 ? -Infinity : parseFloat(n[0]), n[1] = n[1].length === 0 ? Infinity : parseFloat(n[1]), n[2] = e[t], r.push(n));
            this.map = e, this.rangelist = r || !1
        }, get: function (e) {
            var t = this.rangelist, r, i, s;
            if ((s = this.map[e]) !== n)return s;
            if (t)for (r = t.length; r--;) {
                i = t[r];
                if (i[0] <= e && i[1] >= e)return i[2]
            }
            return n
        }}), r.range_map = function (e) {
            return new S(e)
        }, x = o({init: function (e, t) {
            var n = r(e);
            this.$el = n, this.options = t, this.currentPageX = 0, this.currentPageY = 0, this.el = e, this.splist = [], this.tooltip = null, this.over = !1, this.displayTooltips = !t.get("disableTooltips"), this.highlightEnabled = !t.get("disableHighlight")
        }, registerSparkline: function (e) {
            this.splist.push(e), this.over && this.updateDisplay()
        }, registerCanvas: function (e) {
            var t = r(e.canvas);
            this.canvas = e, this.$canvas = t, t.mouseenter(r.proxy(this.mouseenter, this)), t.mouseleave(r.proxy(this.mouseleave, this)), t.click(r.proxy(this.mouseclick, this))
        }, reset: function (e) {
            this.splist = [], this.tooltip && e && (this.tooltip.remove(), this.tooltip = n)
        }, mouseclick: function (e) {
            var t = r.Event("sparklineClick");
            t.originalEvent = e, t.sparklines = this.splist, this.$el.trigger(t)
        }, mouseenter: function (t) {
            r(e.body).unbind("mousemove.jqs"), r(e.body).bind("mousemove.jqs", r.proxy(this.mousemove, this)), this.over = !0, this.currentPageX = t.pageX, this.currentPageY = t.pageY, this.currentEl = t.target, !this.tooltip && this.displayTooltips && (this.tooltip = new T(this.options), this.tooltip.updatePosition(t.pageX, t.pageY)), this.updateDisplay()
        }, mouseleave: function () {
            r(e.body).unbind("mousemove.jqs");
            var t = this.splist, n = t.length, i = !1, s, o;
            this.over = !1, this.currentEl = null, this.tooltip && (this.tooltip.remove(), this.tooltip = null);
            for (o = 0; o < n; o++)s = t[o], s.clearRegionHighlight() && (i = !0);
            i && this.canvas.render()
        }, mousemove: function (e) {
            this.currentPageX = e.pageX, this.currentPageY = e.pageY, this.currentEl = e.target, this.tooltip && this.tooltip.updatePosition(e.pageX, e.pageY), this.updateDisplay()
        }, updateDisplay: function () {
            var e = this.splist, t = e.length, n = !1, i = this.$canvas.offset(), s = this.currentPageX - i.left, o = this.currentPageY - i.top, u, a, f, l, c;
            if (!this.over)return;
            for (f = 0; f < t; f++)a = e[f], l = a.setRegionHighlight(this.currentEl, s, o), l && (n = !0);
            if (n) {
                c = r.Event("sparklineRegionChange"), c.sparklines = this.splist, this.$el.trigger(c);
                if (this.tooltip) {
                    u = "";
                    for (f = 0; f < t; f++)a = e[f], u += a.getCurrentRegionTooltip();
                    this.tooltip.setContent(u)
                }
                this.disableHighlight || this.canvas.render()
            }
            l === null && this.mouseleave()
        }}), T = o({sizeStyle: "position: static !important;display: block !important;visibility: hidden !important;float: left !important;padding: 5px 5px 15px 5px;min-height: 30px;min-width: 30px;", init: function (t) {
            var n = t.get("tooltipClassname", "jqstooltip"), i = this.sizeStyle, s;
            this.container = t.get("tooltipContainer") || e.body, this.tooltipOffsetX = t.get("tooltipOffsetX", 10), this.tooltipOffsetY = t.get("tooltipOffsetY", 12), r("#jqssizetip").remove(), r("#jqstooltip").remove(), this.sizetip = r("<div/>", {id: "jqssizetip", style: i, "class": n}), this.tooltip = r("<div/>", {id: "jqstooltip", "class": n}).appendTo(this.container), s = this.tooltip.offset(), this.offsetLeft = s.left, this.offsetTop = s.top, this.hidden = !0, r(window).unbind("resize.jqs scroll.jqs"), r(window).bind("resize.jqs scroll.jqs", r.proxy(this.updateWindowDims, this)), this.updateWindowDims()
        }, updateWindowDims: function () {
            this.scrollTop = r(window).scrollTop(), this.scrollLeft = r(window).scrollLeft(), this.scrollRight = this.scrollLeft + r(window).width(), this.updatePosition()
        }, getSize: function (e) {
            this.sizetip.html(e).appendTo(this.container), this.width = this.sizetip.width() + 12, this.height = this.sizetip.height() + 12, this.sizetip.remove()
        }, setContent: function (e) {
            if (!e) {
                this.tooltip.css("visibility", "hidden"), this.hidden = !0;
                return
            }
            this.getSize(e), this.tooltip.html(e).css({width: this.width, height: this.height, visibility: "visible"}), this.hidden && (this.hidden = !1, this.updatePosition())
        }, updatePosition: function (e, t) {
            if (e === n) {
                if (this.mousex === n)return;
                e = this.mousex - this.offsetLeft, t = this.mousey - this.offsetTop
            } else this.mousex = e -= this.offsetLeft, this.mousey = t -= this.offsetTop;
            if (!this.height || !this.width || this.hidden)return;
            t -= this.height + this.tooltipOffsetY, e += this.tooltipOffsetX, t < this.scrollTop && (t = this.scrollTop), e < this.scrollLeft ? e = this.scrollLeft : e + this.width > this.scrollRight && (e = this.scrollRight - this.width), this.tooltip.css({left: e, top: t})
        }, remove: function () {
            this.tooltip.remove(), this.sizetip.remove(), this.sizetip = this.tooltip = n, r(window).unbind("resize.jqs scroll.jqs")
        }}), P = function () {
            y(D)
        }, r(P), I = [], r.fn.sparkline = function (t, i) {
            return this.each(function () {
                var s = new r.fn.sparkline.options(this, i), o = r(this), u, f;
                u = function () {
                    var i, u, f, l, h, p, d;
                    if (t === "html" || t === n) {
                        d = this.getAttribute(s.get("tagValuesAttribute"));
                        if (d === n || d === null)d = o.html();
                        i = d.replace(/(^\s*<!--)|(-->\s*$)|\s+/g, "").split(",")
                    } else i = t;
                    u = s.get("width") === "auto" ? i.length * s.get("defaultPixelsPerValue") : s.get("width");
                    if (s.get("height") === "auto") {
                        if (!s.get("composite") || !r.data(this, "_jqs_vcanvas"))l = e.createElement("span"), l.innerHTML = "a", o.html(l), f = r(l).innerHeight() || r(l).height(), r(l).remove(), l = null
                    } else f = s.get("height");
                    s.get("disableInteraction") ? h = !1 : (h = r.data(this, "_jqs_mhandler"), h ? s.get("composite") || h.reset() : (h = new x(this, s), r.data(this, "_jqs_mhandler", h)));
                    if (s.get("composite") && !r.data(this, "_jqs_vcanvas")) {
                        r.data(this, "_jqs_errnotify") || (alert("Attempted to attach a composite sparkline to an element with no existing sparkline"), r.data(this, "_jqs_errnotify", !0));
                        return
                    }
                    p = new (r.fn.sparkline[s.get("type")])(this, i, s, u, f), p.render(), h && h.registerSparkline(p)
                };
                if (r(this).html() && !s.get("disableHiddenCheck") && r(this).is(":hidden") || !r(this).parents("body").length) {
                    if (!s.get("composite") && r.data(this, "_jqs_pending"))for (f = I.length; f; f--)I[f - 1][0] == this && I.splice(f - 1, 1);
                    I.push([this, u]), r.data(this, "_jqs_pending", !0)
                } else u.call(this)
            })
        }, r.fn.sparkline.defaults = s(), r.sparkline_display_visible = function () {
            var e, t, n, i = [];
            for (t = 0, n = I.length; t < n; t++)e = I[t][0], r(e).is(":visible") && !r(e).parents().is(":hidden") ? (I[t][1].call(e), r.data(I[t][0], "_jqs_pending", !1), i.push(t)) : !r(e).closest("html").length && !r.data(e, "_jqs_pending") && (r.data(I[t][0], "_jqs_pending", !1), i.push(t));
            for (t = i.length; t; t--)I.splice(i[t - 1], 1)
        }, r.fn.sparkline.options = o({init: function (e, t) {
            var n, s, o, u;
            this.userOptions = t = t || {}, this.tag = e, this.tagValCache = {}, s = r.fn.sparkline.defaults, o = s.common, this.tagOptionsPrefix = t.enableTagOptions && (t.tagOptionsPrefix || o.tagOptionsPrefix), u = this.getTagSetting("type"), u === i ? n = s[t.type || o.type] : n = s[u], this.mergedOptions = r.extend({}, o, n, t)
        }, getTagSetting: function (e) {
            var t = this.tagOptionsPrefix, r, s, o, u;
            if (t === !1 || t === n)return i;
            if (this.tagValCache.hasOwnProperty(e))r = this.tagValCache.key; else {
                r = this.tag.getAttribute(t + e);
                if (r === n || r === null)r = i; else if (r.substr(0, 1) === "[") {
                    r = r.substr(1, r.length - 2).split(",");
                    for (s = r.length; s--;)r[s] = h(r[s].replace(/(^\s*)|(\s*$)/g, ""))
                } else if (r.substr(0, 1) === "{") {
                    o = r.substr(1, r.length - 2).split(","), r = {};
                    for (s = o.length; s--;)u = o[s].split(":", 2), r[u[0].replace(/(^\s*)|(\s*$)/g, "")] = h(u[1].replace(/(^\s*)|(\s*$)/g, ""))
                } else r = h(r);
                this.tagValCache.key = r
            }
            return r
        }, get: function (e, t) {
            var r = this.getTagSetting(e), s;
            return r !== i ? r : (s = this.mergedOptions[e]) === n ? t : s
        }}), r.fn.sparkline._base = o({disabled: !1, init: function (e, t, i, s, o) {
            this.el = e, this.$el = r(e), this.values = t, this.options = i, this.width = s, this.height = o, this.currentRegion = n
        }, initTarget: function () {
            var e = !this.options.get("disableInteraction");
            (this.target = this.$el.simpledraw(this.width, this.height, this.options.get("composite"), e)) ? (this.canvasWidth = this.target.pixelWidth, this.canvasHeight = this.target.pixelHeight) : this.disabled = !0
        }, render: function () {
            return this.disabled ? (this.el.innerHTML = "", !1) : !0
        }, getRegion: function (e, t) {
        }, setRegionHighlight: function (e, t, r) {
            var i = this.currentRegion, s = !this.options.get("disableHighlight"), o;
            return t > this.canvasWidth || r > this.canvasHeight || t < 0 || r < 0 ? null : (o = this.getRegion(e, t, r), i !== o ? (i !== n && s && this.removeHighlight(), this.currentRegion = o, o !== n && s && this.renderHighlight(), !0) : !1)
        }, clearRegionHighlight: function () {
            return this.currentRegion !== n ? (this.removeHighlight(), this.currentRegion = n, !0) : !1
        }, renderHighlight: function () {
            this.changeHighlight(!0)
        }, removeHighlight: function () {
            this.changeHighlight(!1)
        }, changeHighlight: function (e) {
        }, getCurrentRegionTooltip: function () {
            var e = this.options, t = "", i = [], s, o, a, f, l, h, p, d, v, m, g, y, b, w;
            if (this.currentRegion === n)return"";
            s = this.getCurrentRegionFields(), g = e.get("tooltipFormatter");
            if (g)return g(this, e, s);
            e.get("tooltipChartTitle") && (t += '<div class="jqs jqstitle">' + e.get("tooltipChartTitle") + "</div>\n"), o = this.options.get("tooltipFormat");
            if (!o)return"";
            r.isArray(o) || (o = [o]), r.isArray(s) || (s = [s]), p = this.options.get("tooltipFormatFieldlist"), d = this.options.get("tooltipFormatFieldlistKey");
            if (p && d) {
                v = [];
                for (h = s.length; h--;)m = s[h][d], (w = r.inArray(m, p)) != -1 && (v[w] = s[h]);
                s = v
            }
            a = o.length, b = s.length;
            for (h = 0; h < a; h++) {
                y = o[h], typeof y == "string" && (y = new u(y)), f = y.fclass || "jqsfield";
                for (w = 0; w < b; w++)if (!s[w].isNull || !e.get("tooltipSkipNull"))r.extend(s[w], {prefix: e.get("tooltipPrefix"), suffix: e.get("tooltipSuffix")}), l = y.render(s[w], e.get("tooltipValueLookups"), e), i.push('<div class="' + f + '">' + l + "</div>")
            }
            return i.length ? t + i.join("\n") : ""
        }, getCurrentRegionFields: function () {
        }, calcHighlightColor: function (e, n) {
            var r = n.get("highlightColor"), i = n.get("highlightLighten"), s, o, u, a;
            if (r)return r;
            if (i) {
                s = /^#([0-9a-f])([0-9a-f])([0-9a-f])$/i.exec(e) || /^#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(e);
                if (s) {
                    u = [], o = e.length === 4 ? 16 : 1;
                    for (a = 0; a < 3; a++)u[a] = f(t.round(parseInt(s[a + 1], 16) * o * i), 0, 255);
                    return"rgb(" + u.join(",") + ")"
                }
            }
            return e
        }}), N = {changeHighlight: function (e) {
            var t = this.currentRegion, n = this.target, i = this.regionShapes[t], s;
            i && (s = this.renderRegion(t, e), r.isArray(s) || r.isArray(i) ? (n.replaceWithShapes(i, s), this.regionShapes[t] = r.map(s, function (e) {
                return e.id
            })) : (n.replaceWithShape(i, s), this.regionShapes[t] = s.id))
        }, render: function () {
            var e = this.values, t = this.target, n = this.regionShapes, i, s, o, u;
            if (!this.cls._super.render.call(this))return;
            for (o = e.length; o--;) {
                i = this.renderRegion(o);
                if (i)if (r.isArray(i)) {
                    s = [];
                    for (u = i.length; u--;)i[u].append(), s.push(i[u].id);
                    n[o] = s
                } else i.append(), n[o] = i.id; else n[o] = null
            }
            t.render()
        }}, r.fn.sparkline.line = C = o(r.fn.sparkline._base, {type: "line", init: function (e, t, n, r, i) {
            C._super.init.call(this, e, t, n, r, i), this.vertices = [], this.regionMap = [], this.xvalues = [], this.yvalues = [], this.yminmax = [], this.hightlightSpotId = null, this.lastShapeId = null, this.initTarget()
        }, getRegion: function (e, t, r) {
            var i, s = this.regionMap;
            for (i = s.length; i--;)if (s[i] !== null && t >= s[i][0] && t <= s[i][1])return s[i][2];
            return n
        }, getCurrentRegionFields: function () {
            var e = this.currentRegion;
            return{isNull: this.yvalues[e] === null, x: this.xvalues[e], y: this.yvalues[e], color: this.options.get("lineColor"), fillColor: this.options.get("fillColor"), offset: e}
        }, renderHighlight: function () {
            var e = this.currentRegion, t = this.target, r = this.vertices[e], i = this.options, s = i.get("spotRadius"), o = i.get("highlightSpotColor"), u = i.get("highlightLineColor"), a, f;
            if (!r)return;
            s && o && (a = t.drawCircle(r[0], r[1], s, n, o), this.highlightSpotId = a.id, t.insertAfterShape(this.lastShapeId, a)), u && (f = t.drawLine(r[0], this.canvasTop, r[0], this.canvasTop + this.canvasHeight, u), this.highlightLineId = f.id, t.insertAfterShape(this.lastShapeId, f))
        }, removeHighlight: function () {
            var e = this.target;
            this.highlightSpotId && (e.removeShapeId(this.highlightSpotId), this.highlightSpotId = null), this.highlightLineId && (e.removeShapeId(this.highlightLineId), this.highlightLineId = null)
        }, scanValues: function () {
            var e = this.values, n = e.length, r = this.xvalues, i = this.yvalues, s = this.yminmax, o, u, a, f, l;
            for (o = 0; o < n; o++)u = e[o], a = typeof e[o] == "string", f = typeof e[o] == "object" && e[o]instanceof Array, l = a && e[o].split(":"), a && l.length === 2 ? (r.push(Number(l[0])), i.push(Number(l[1])), s.push(Number(l[1]))) : f ? (r.push(u[0]), i.push(u[1]), s.push(u[1])) : (r.push(o), e[o] === null || e[o] === "null" ? i.push(null) : (i.push(Number(u)), s.push(Number(u))));
            this.options.get("xvalues") && (r = this.options.get("xvalues")), this.maxy = this.maxyorg = t.max.apply(t, s), this.miny = this.minyorg = t.min.apply(t, s), this.maxx = t.max.apply(t, r), this.minx = t.min.apply(t, r), this.xvalues = r, this.yvalues = i, this.yminmax = s
        }, processRangeOptions: function () {
            var e = this.options, t = e.get("normalRangeMin"), r = e.get("normalRangeMax");
            t !== n && (t < this.miny && (this.miny = t), r > this.maxy && (this.maxy = r)), e.get("chartRangeMin") !== n && (e.get("chartRangeClip") || e.get("chartRangeMin") < this.miny) && (this.miny = e.get("chartRangeMin")), e.get("chartRangeMax") !== n && (e.get("chartRangeClip") || e.get("chartRangeMax") > this.maxy) && (this.maxy = e.get("chartRangeMax")), e.get("chartRangeMinX") !== n && (e.get("chartRangeClipX") || e.get("chartRangeMinX") < this.minx) && (this.minx = e.get("chartRangeMinX")), e.get("chartRangeMaxX") !== n && (e.get("chartRangeClipX") || e.get("chartRangeMaxX") > this.maxx) && (this.maxx = e.get("chartRangeMaxX"))
        }, drawNormalRange: function (e, r, i, s, o) {
            var u = this.options.get("normalRangeMin"), a = this.options.get("normalRangeMax"), f = r + t.round(i - i * ((a - this.miny) / o)), l = t.round(i * (a - u) / o);
            this.target.drawRect(e, f, s, l, n, this.options.get("normalRangeColor")).append()
        }, render: function () {
            var e = this.options, i = this.target, s = this.canvasWidth, o = this.canvasHeight, u = this.vertices, a = e.get("spotRadius"), f = this.regionMap, l, h, p, d, v, m, g, y, w, E, x, T, N, k, L, A, O, M, _, D, P, H, B, j, F;
            if (!C._super.render.call(this))return;
            this.scanValues(), this.processRangeOptions(), B = this.xvalues, j = this.yvalues;
            if (!this.yminmax.length || this.yvalues.length < 2)return;
            d = v = 0, l = this.maxx - this.minx === 0 ? 1 : this.maxx - this.minx, h = this.maxy - this.miny === 0 ? 1 : this.maxy - this.miny, p = this.yvalues.length - 1, a && (s < a * 4 || o < a * 4) && (a = 0);
            if (a) {
                P = e.get("highlightSpotColor") && !e.get("disableInteraction");
                if (P || e.get("minSpotColor") || e.get("spotColor") && j[p] === this.miny)o -= t.ceil(a);
                if (P || e.get("maxSpotColor") || e.get("spotColor") && j[p] === this.maxy)o -= t.ceil(a), d += t.ceil(a);
                if (P || (e.get("minSpotColor") || e.get("maxSpotColor")) && (j[0] === this.miny || j[0] === this.maxy))v += t.ceil(a), s -= t.ceil(a);
                if (P || e.get("spotColor") || e.get("minSpotColor") || e.get("maxSpotColor") && (j[p] === this.miny || j[p] === this.maxy))s -= t.ceil(a)
            }
            o--, e.get("normalRangeMin") !== n && !e.get("drawNormalOnTop") && this.drawNormalRange(v, d, o, s, h), g = [], y = [g], k = L = null, A = j.length;
            for (F = 0; F < A; F++)w = B[F], x = B[F + 1], E = j[F], T = v + t.round((w - this.minx) * (s / l)), N = F < A - 1 ? v + t.round((x - this.minx) * (s / l)) : s, L = T + (N - T) / 2, f[F] = [k || 0, L, F], k = L, E === null ? F && (j[F - 1] !== null && (g = [], y.push(g)), u.push(null)) : (E < this.miny && (E = this.miny), E > this.maxy && (E = this.maxy), g.length || g.push([T, d + o]), m = [T, d + t.round(o - o * ((E - this.miny) / h))], g.push(m), u.push(m));
            O = [], M = [], _ = y.length;
            for (F = 0; F < _; F++)g = y[F], g.length && (e.get("fillColor") && (g.push([g[g.length - 1][0], d + o]), M.push(g.slice(0)), g.pop()), g.length > 2 && (g[0] = [g[0][0], g[1][1]]), O.push(g));
            _ = M.length;
            for (F = 0; F < _; F++)i.drawShape(M[F], e.get("fillColor"), e.get("fillColor")).append();
            e.get("normalRangeMin") !== n && e.get("drawNormalOnTop") && this.drawNormalRange(v, d, o, s, h), _ = O.length;
            for (F = 0; F < _; F++)i.drawShape(O[F], e.get("lineColor"), n, e.get("lineWidth")).append();
            if (a && e.get("valueSpots")) {
                D = e.get("valueSpots"), D.get === n && (D = new S(D));
                for (F = 0; F < A; F++)H = D.get(j[F]), H && i.drawCircle(v + t.round((B[F] - this.minx) * (s / l)), d + t.round(o - o * ((j[F] - this.miny) / h)), a, n, H).append()
            }
            a && e.get("spotColor") && j[p] !== null && i.drawCircle(v + t.round((B[B.length - 1] - this.minx) * (s / l)), d + t.round(o - o * ((j[p] - this.miny) / h)), a, n, e.get("spotColor")).append(), this.maxy !== this.minyorg && (a && e.get("minSpotColor") && (w = B[r.inArray(this.minyorg, j)], i.drawCircle(v + t.round((w - this.minx) * (s / l)), d + t.round(o - o * ((this.minyorg - this.miny) / h)), a, n, e.get("minSpotColor")).append()), a && e.get("maxSpotColor") && (w = B[r.inArray(this.maxyorg, j)], i.drawCircle(v + t.round((w - this.minx) * (s / l)), d + t.round(o - o * ((this.maxyorg - this.miny) / h)), a, n, e.get("maxSpotColor")).append())), this.lastShapeId = i.getLastShapeId(), this.canvasTop = d, i.render()
        }}), r.fn.sparkline.bar = k = o(r.fn.sparkline._base, N, {type: "bar", init: function (e, i, s, o, u) {
            var a = parseInt(s.get("barWidth"), 10), l = parseInt(s.get("barSpacing"), 10), v = s.get("chartRangeMin"), m = s.get("chartRangeMax"), g = s.get("chartRangeClip"), y = Infinity, w = -Infinity, E, x, T, N, C, L, A, O, M, _, D, P, H, B, j, F, I, q, R, U, z, W, X;
            k._super.init.call(this, e, i, s, o, u);
            for (L = 0, A = i.length; L < A; L++) {
                U = i[L], E = typeof U == "string" && U.indexOf(":") > -1;
                if (E || r.isArray(U))j = !0, E && (U = i[L] = p(U.split(":"))), U = d(U, null), x = t.min.apply(t, U), T = t.max.apply(t, U), x < y && (y = x), T > w && (w = T)
            }
            this.stacked = j, this.regionShapes = {}, this.barWidth = a, this.barSpacing = l, this.totalBarWidth = a + l, this.width = o = i.length * a + (i.length - 1) * l, this.initTarget(), g && (H = v === n ? -Infinity : v, B = m === n ? Infinity : m), C = [], N = j ? [] : C;
            var V = [], $ = [];
            for (L = 0, A = i.length; L < A; L++)if (j) {
                F = i[L], i[L] = R = [], V[L] = 0, N[L] = $[L] = 0;
                for (I = 0, q = F.length; I < q; I++)U = R[I] = g ? f(F[I], H, B) : F[I], U !== null && (U > 0 && (V[L] += U), y < 0 && w > 0 ? U < 0 ? $[L] += t.abs(U) : N[L] += U : N[L] += t.abs(U - (U < 0 ? w : y)), C.push(U))
            } else U = g ? f(i[L], H, B) : i[L], U = i[L] = h(U), U !== null && C.push(U);
            this.max = P = t.max.apply(t, C), this.min = D = t.min.apply(t, C), this.stackMax = w = j ? t.max.apply(t, V) : P, this.stackMin = y = j ? t.min.apply(t, C) : D, s.get("chartRangeMin") !== n && (s.get("chartRangeClip") || s.get("chartRangeMin") < D) && (D = s.get("chartRangeMin")), s.get("chartRangeMax") !== n && (s.get("chartRangeClip") || s.get("chartRangeMax") > P) && (P = s.get("chartRangeMax")), this.zeroAxis = M = s.get("zeroAxis", !0), D <= 0 && P >= 0 && M ? _ = 0 : M == 0 ? _ = D : D > 0 ? _ = D : _ = P, this.xaxisOffset = _, O = j ? t.max.apply(t, N) + t.max.apply(t, $) : P - D, this.canvasHeightEf = M && D < 0 ? this.canvasHeight - 2 : this.canvasHeight - 1, D < _ ? (W = j && P >= 0 ? w : P, z = (W - _) / O * this.canvasHeight, z !== t.ceil(z) && (this.canvasHeightEf -= 2, z = t.ceil(z))) : z = this.canvasHeight, this.yoffset = z, r.isArray(s.get("colorMap")) ? (this.colorMapByIndex = s.get("colorMap"), this.colorMapByValue = null) : (this.colorMapByIndex = null, this.colorMapByValue = s.get("colorMap"), this.colorMapByValue && this.colorMapByValue.get === n && (this.colorMapByValue = new S(this.colorMapByValue))), this.range = O
        }, getRegion: function (e, r, i) {
            var s = t.floor(r / this.totalBarWidth);
            return s < 0 || s >= this.values.length ? n : s
        }, getCurrentRegionFields: function () {
            var e = this.currentRegion, t = w(this.values[e]), n = [], r, i;
            for (i = t.length; i--;)r = t[i], n.push({isNull: r === null, value: r, color: this.calcColor(i, r, e), offset: e});
            return n
        }, calcColor: function (e, t, i) {
            var s = this.colorMapByIndex, o = this.colorMapByValue, u = this.options, a, f;
            return this.stacked ? a = u.get("stackedBarColor") : a = t < 0 ? u.get("negBarColor") : u.get("barColor"), t === 0 && u.get("zeroColor") !== n && (a = u.get("zeroColor")), o && (f = o.get(t)) ? a = f : s && s.length > i && (a = s[i]), r.isArray(a) ? a[e % a.length] : a
        }, renderRegion: function (e, i) {
            var s = this.values[e], o = this.options, u = this.xaxisOffset, a = [], f = this.range, l = this.stacked, h = this.target, p = e * this.totalBarWidth, d = this.canvasHeightEf, v = this.yoffset, g, y, w, E, S, x, T, N, C, k;
            s = r.isArray(s) ? s : [s], T = s.length, N = s[0], E = m(null, s), k = m(u, s, !0);
            if (E)return o.get("nullColor") ? (w = i ? o.get("nullColor") : this.calcHighlightColor(o.get("nullColor"), o), g = v > 0 ? v - 1 : v, h.drawRect(p, g, this.barWidth - 1, 0, w, w)) : n;
            S = v;
            for (x = 0; x < T; x++) {
                N = s[x];
                if (l && N === u) {
                    if (!k || C)continue;
                    C = !0
                }
                f > 0 ? y = t.floor(d * (t.abs(N - u) / f)) + 1 : y = 1, N < u || N === u && v === 0 ? (g = S, S += y) : (g = v - y, v -= y), w = this.calcColor(x, N, e), i && (w = this.calcHighlightColor(w, o)), a.push(h.drawRect(p, g, this.barWidth - 1, y - 1, w, w))
            }
            return a.length === 1 ? a[0] : a
        }}), r.fn.sparkline.tristate = L = o(r.fn.sparkline._base, N, {type: "tristate", init: function (e, t, i, s, o) {
            var u = parseInt(i.get("barWidth"), 10), a = parseInt(i.get("barSpacing"), 10);
            L._super.init.call(this, e, t, i, s, o), this.regionShapes = {}, this.barWidth = u, this.barSpacing = a, this.totalBarWidth = u + a, this.values = r.map(t, Number), this.width = s = t.length * u + (t.length - 1) * a, r.isArray(i.get("colorMap")) ? (this.colorMapByIndex = i.get("colorMap"), this.colorMapByValue = null) : (this.colorMapByIndex = null, this.colorMapByValue = i.get("colorMap"), this.colorMapByValue && this.colorMapByValue.get === n && (this.colorMapByValue = new S(this.colorMapByValue))), this.initTarget()
        }, getRegion: function (e, n, r) {
            return t.floor(n / this.totalBarWidth)
        }, getCurrentRegionFields: function () {
            var e = this.currentRegion;
            return{isNull: this.values[e] === n, value: this.values[e], color: this.calcColor(this.values[e], e), offset: e}
        }, calcColor: function (e, t) {
            var n = this.values, r = this.options, i = this.colorMapByIndex, s = this.colorMapByValue, o, u;
            return s && (u = s.get(e)) ? o = u : i && i.length > t ? o = i[t] : n[t] < 0 ? o = r.get("negBarColor") : n[t] > 0 ? o = r.get("posBarColor") : o = r.get("zeroBarColor"), o
        }, renderRegion: function (e, n) {
            var r = this.values, i = this.options, s = this.target, o, u, a, f, l, c;
            o = s.pixelHeight, a = t.round(o / 2), f = e * this.totalBarWidth, r[e] < 0 ? (l = a, u = a - 1) : r[e] > 0 ? (l = 0, u = a - 1) : (l = a - 1, u = 2), c = this.calcColor(r[e], e);
            if (c === null)return;
            return n && (c = this.calcHighlightColor(c, i)), s.drawRect(f, l, this.barWidth - 1, u - 1, c, c)
        }}), r.fn.sparkline.discrete = A = o(r.fn.sparkline._base, N, {type: "discrete", init: function (e, i, s, o, u) {
            A._super.init.call(this, e, i, s, o, u), this.regionShapes = {}, this.values = i = r.map(i, Number), this.min = t.min.apply(t, i), this.max = t.max.apply(t, i), this.range = this.max - this.min, this.width = o = s.get("width") === "auto" ? i.length * 2 : this.width, this.interval = t.floor(o / i.length), this.itemWidth = o / i.length, s.get("chartRangeMin") !== n && (s.get("chartRangeClip") || s.get("chartRangeMin") < this.min) && (this.min = s.get("chartRangeMin")), s.get("chartRangeMax") !== n && (s.get("chartRangeClip") || s.get("chartRangeMax") > this.max) && (this.max = s.get("chartRangeMax")), this.initTarget(), this.target && (this.lineHeight = s.get("lineHeight") === "auto" ? t.round(this.canvasHeight * .3) : s.get("lineHeight"))
        }, getRegion: function (e, n, r) {
            return t.floor(n / this.itemWidth)
        }, getCurrentRegionFields: function () {
            var e = this.currentRegion;
            return{isNull: this.values[e] === n, value: this.values[e], offset: e}
        }, renderRegion: function (e, n) {
            var r = this.values, i = this.options, s = this.min, o = this.max, u = this.range, a = this.interval, l = this.target, c = this.canvasHeight, h = this.lineHeight, p = c - h, d, v, m, g;
            return v = f(r[e], s, o), g = e * a, d = t.round(p - p * ((v - s) / u)), m = i.get("thresholdColor") && v < i.get("thresholdValue") ? i.get("thresholdColor") : i.get("lineColor"), n && (m = this.calcHighlightColor(m, i)), l.drawLine(g, d, g, d + h, m)
        }}), r.fn.sparkline.bullet = O = o(r.fn.sparkline._base, {type: "bullet", init: function (e, r, i, s, o) {
            var u, a, f;
            O._super.init.call(this, e, r, i, s, o), this.values = r = p(r), f = r.slice(), f[0] = f[0] === null ? f[2] : f[0], f[1] = r[1] === null ? f[2] : f[1], u = t.min.apply(t, r), a = t.max.apply(t, r), i.get("base") === n ? u = u < 0 ? u : 0 : u = i.get("base"), this.min = u, this.max = a, this.range = a - u, this.shapes = {}, this.valueShapes = {}, this.regiondata = {}, this.width = s = i.get("width") === "auto" ? "4.0em" : s, this.target = this.$el.simpledraw(s, o, i.get("composite")), r.length || (this.disabled = !0), this.initTarget()
        }, getRegion: function (e, t, r) {
            var i = this.target.getShapeAt(e, t, r);
            return i !== n && this.shapes[i] !== n ? this.shapes[i] : n
        }, getCurrentRegionFields: function () {
            var e = this.currentRegion;
            return{fieldkey: e.substr(0, 1), value: this.values[e.substr(1)], region: e}
        }, changeHighlight: function (e) {
            var t = this.currentRegion, n = this.valueShapes[t], r;
            delete this.shapes[n];
            switch (t.substr(0, 1)) {
                case"r":
                    r = this.renderRange(t.substr(1), e);
                    break;
                case"p":
                    r = this.renderPerformance(e);
                    break;
                case"t":
                    r = this.renderTarget(e)
            }
            this.valueShapes[t] = r.id, this.shapes[r.id] = t, this.target.replaceWithShape(n, r)
        }, renderRange: function (e, n) {
            var r = this.values[e], i = t.round(this.canvasWidth * ((r - this.min) / this.range)), s = this.options.get("rangeColors")[e - 2];
            return n && (s = this.calcHighlightColor(s, this.options)), this.target.drawRect(0, 0, i - 1, this.canvasHeight - 1, s, s)
        }, renderPerformance: function (e) {
            var n = this.values[1], r = t.round(this.canvasWidth * ((n - this.min) / this.range)), i = this.options.get("performanceColor");
            return e && (i = this.calcHighlightColor(i, this.options)), this.target.drawRect(0, t.round(this.canvasHeight * .3), r - 1, t.round(this.canvasHeight * .4) - 1, i, i)
        }, renderTarget: function (e) {
            var n = this.values[0], r = t.round(this.canvasWidth * ((n - this.min) / this.range) - this.options.get("targetWidth") / 2), i = t.round(this.canvasHeight * .1), s = this.canvasHeight - i * 2, o = this.options.get("targetColor");
            return e && (o = this.calcHighlightColor(o, this.options)), this.target.drawRect(r, i, this.options.get("targetWidth") - 1, s - 1, o, o)
        }, render: function () {
            var e = this.values.length, t = this.target, n, r;
            if (!O._super.render.call(this))return;
            for (n = 2; n < e; n++)r = this.renderRange(n).append(), this.shapes[r.id] = "r" + n, this.valueShapes["r" + n] = r.id;
            this.values[1] !== null && (r = this.renderPerformance().append(), this.shapes[r.id] = "p1", this.valueShapes.p1 = r.id), this.values[0] !== null && (r = this.renderTarget().append(), this.shapes[r.id] = "t0", this.valueShapes.t0 = r.id), t.render()
        }}), r.fn.sparkline.pie = M = o(r.fn.sparkline._base, {type: "pie", init: function (e, n, i, s, o) {
            var u = 0, a;
            M._super.init.call(this, e, n, i, s, o), this.shapes = {}, this.valueShapes = {}, this.values = n = r.map(n, Number), i.get("width") === "auto" && (this.width = this.height);
            if (n.length > 0)for (a = n.length; a--;)u += n[a];
            this.total = u, this.initTarget(), this.radius = t.floor(t.min(this.canvasWidth, this.canvasHeight) / 2)
        }, getRegion: function (e, t, r) {
            var i = this.target.getShapeAt(e, t, r);
            return i !== n && this.shapes[i] !== n ? this.shapes[i] : n
        }, getCurrentRegionFields: function () {
            var e = this.currentRegion;
            return{isNull: this.values[e] === n, value: this.values[e], percent: this.values[e] / this.total * 100, color: this.options.get("sliceColors")[e % this.options.get("sliceColors").length], offset: e}
        }, changeHighlight: function (e) {
            var t = this.currentRegion, n = this.renderSlice(t, e), r = this.valueShapes[t];
            delete this.shapes[r], this.target.replaceWithShape(r, n), this.valueShapes[t] = n.id, this.shapes[n.id] = t
        }, renderSlice: function (e, r) {
            var i = this.target, s = this.options, o = this.radius, u = s.get("borderWidth"), a = s.get("offset"), f = 2 * t.PI, l = this.values, h = this.total, p = a ? 2 * t.PI * (a / 360) : 0, d, v, m, g, y;
            g = l.length;
            for (m = 0; m < g; m++) {
                d = p, v = p, h > 0 && (v = p + f * (l[m] / h));
                if (e === m)return y = s.get("sliceColors")[m % s.get("sliceColors").length], r && (y = this.calcHighlightColor(y, s)), i.drawPieSlice(o, o, o - u, d, v, n, y);
                p = v
            }
        }, render: function () {
            var e = this.target, r = this.values, i = this.options, s = this.radius, o = i.get("borderWidth"), u, a;
            if (!M._super.render.call(this))return;
            o && e.drawCircle(s, s, t.floor(s - o / 2), i.get("borderColor"), n, o).append();
            for (a = r.length; a--;)r[a] && (u = this.renderSlice(a).append(), this.valueShapes[a] = u.id, this.shapes[u.id] = a);
            e.render()
        }}), r.fn.sparkline.box = _ = o(r.fn.sparkline._base, {type: "box", init: function (e, t, n, i, s) {
            _._super.init.call(this, e, t, n, i, s), this.values = r.map(t, Number), this.width = n.get("width") === "auto" ? "4.0em" : i, this.initTarget(), this.values.length || (this.disabled = 1)
        }, getRegion: function () {
            return 1
        }, getCurrentRegionFields: function () {
            var e = [
                {field: "lq", value: this.quartiles[0]},
                {field: "med", value: this.quartiles[1]},
                {field: "uq", value: this.quartiles[2]}
            ];
            return this.loutlier !== n && e.push({field: "lo", value: this.loutlier}), this.routlier !== n && e.push({field: "ro", value: this.routlier}), this.lwhisker !== n && e.push({field: "lw", value: this.lwhisker}), this.rwhisker !== n && e.push({field: "rw", value: this.rwhisker}), e
        }, render: function () {
            var e = this.target, r = this.values, i = r.length, s = this.options, o = this.canvasWidth, u = this.canvasHeight, a = s.get("chartRangeMin") === n ? t.min.apply(t, r) : s.get("chartRangeMin"), f = s.get("chartRangeMax") === n ? t.max.apply(t, r) : s.get("chartRangeMax"), h = 0, p, d, v, m, g, y, w, E, S, x, T;
            if (!_._super.render.call(this))return;
            if (s.get("raw"))s.get("showOutliers") && r.length > 5 ? (d = r[0], p = r[1], m = r[2], g = r[3], y = r[4], w = r[5], E = r[6]) : (p = r[0], m = r[1], g = r[2], y = r[3], w = r[4]); else {
                r.sort(function (e, t) {
                    return e - t
                }), m = l(r, 1), g = l(r, 2), y = l(r, 3), v = y - m;
                if (s.get("showOutliers")) {
                    p = w = n;
                    for (S = 0; S < i; S++)p === n && r[S] > m - v * s.get("outlierIQR") && (p = r[S]), r[S] < y + v * s.get("outlierIQR") && (w = r[S]);
                    d = r[0], E = r[i - 1]
                } else p = r[0], w = r[i - 1]
            }
            this.quartiles = [m, g, y], this.lwhisker = p, this.rwhisker = w, this.loutlier = d, this.routlier = E, T = o / (f - a + 1), s.get("showOutliers") && (h = t.ceil(s.get("spotRadius")), o -= 2 * t.ceil(s.get("spotRadius")), T = o / (f - a + 1), d < p && e.drawCircle((d - a) * T + h, u / 2, s.get("spotRadius"), s.get("outlierLineColor"), s.get("outlierFillColor")).append(), E > w && e.drawCircle((E - a) * T + h, u / 2, s.get("spotRadius"), s.get("outlierLineColor"), s.get("outlierFillColor")).append()), e.drawRect(t.round((m - a) * T + h), t.round(u * .1), t.round((y - m) * T), t.round(u * .8), s.get("boxLineColor"), s.get("boxFillColor")).append(), e.drawLine(t.round((p - a) * T + h), t.round(u / 2), t.round((m - a) * T + h), t.round(u / 2), s.get("lineColor")).append(), e.drawLine(t.round((p - a) * T + h), t.round(u / 4), t.round((p - a) * T + h), t.round(u - u / 4), s.get("whiskerColor")).append(), e.drawLine(t.round((w - a) * T + h), t.round(u / 2), t.round((y - a) * T + h), t.round(u / 2), s.get("lineColor")).append(), e.drawLine(t.round((w - a) * T + h), t.round(u / 4), t.round((w - a) * T + h), t.round(u - u / 4), s.get("whiskerColor")).append(), e.drawLine(t.round((g - a) * T + h), t.round(u * .1), t.round((g - a) * T + h), t.round(u * .9), s.get("medianColor")).append(), s.get("target") && (x = t.ceil(s.get("spotRadius")), e.drawLine(t.round((s.get("target") - a) * T + h), t.round(u / 2 - x), t.round((s.get("target") - a) * T + h), t.round(u / 2 + x), s.get("targetColor")).append(), e.drawLine(t.round((s.get("target") - a) * T + h - x), t.round(u / 2), t.round((s.get("target") - a) * T + h + x), t.round(u / 2), s.get("targetColor")).append()), e.render()
        }}), H = o({init: function (e, t, n, r) {
            this.target = e, this.id = t, this.type = n, this.args = r
        }, append: function () {
            return this.target.appendShape(this), this
        }}), B = o({_pxregex: /(\d+)(px)?\s*$/i, init: function (e, t, n) {
            if (!e)return;
            this.width = e, this.height = t, this.target = n, this.lastShapeId = null, n[0] && (n = n[0]), r.data(n, "_jqs_vcanvas", this)
        }, drawLine: function (e, t, n, r, i, s) {
            return this.drawShape([
                [e, t],
                [n, r]
            ], i, s)
        }, drawShape: function (e, t, n, r) {
            return this._genShape("Shape", [e, t, n, r])
        }, drawCircle: function (e, t, n, r, i, s) {
            return this._genShape("Circle", [e, t, n, r, i, s])
        }, drawPieSlice: function (e, t, n, r, i, s, o) {
            return this._genShape("PieSlice", [e, t, n, r, i, s, o])
        }, drawRect: function (e, t, n, r, i, s) {
            return this._genShape("Rect", [e, t, n, r, i, s])
        }, getElement: function () {
            return this.canvas
        }, getLastShapeId: function () {
            return this.lastShapeId
        }, reset: function () {
            alert("reset not implemented")
        }, _insert: function (e, t) {
            r(t).html(e)
        }, _calculatePixelDims: function (e, t, n) {
            var i;
            i = this._pxregex.exec(t), i ? this.pixelHeight = i[1] : this.pixelHeight = r(n).height(), i = this._pxregex.exec(e), i ? this.pixelWidth = i[1] : this.pixelWidth = r(n).width()
        }, _genShape: function (e, t) {
            var n = q++;
            return t.unshift(n), new H(this, n, e, t)
        }, appendShape: function (e) {
            alert("appendShape not implemented")
        }, replaceWithShape: function (e, t) {
            alert("replaceWithShape not implemented")
        }, insertAfterShape: function (e, t) {
            alert("insertAfterShape not implemented")
        }, removeShapeId: function (e) {
            alert("removeShapeId not implemented")
        }, getShapeAt: function (e, t, n) {
            alert("getShapeAt not implemented")
        }, render: function () {
            alert("render not implemented")
        }}), j = o(B, {init: function (t, i, s, o) {
            j._super.init.call(this, t, i, s), this.canvas = e.createElement("canvas"), s[0] && (s = s[0]), r.data(s, "_jqs_vcanvas", this), r(this.canvas).css({display: "inline-block", width: t, height: i, verticalAlign: "top"}), this._insert(this.canvas, s), this._calculatePixelDims(t, i, this.canvas), this.canvas.width = this.pixelWidth, this.canvas.height = this.pixelHeight, this.interact = o, this.shapes = {}, this.shapeseq = [], this.currentTargetShapeId = n, r(this.canvas).css({width: this.pixelWidth, height: this.pixelHeight})
        }, _getContext: function (e, t, r) {
            var i = this.canvas.getContext("2d");
            return e !== n && (i.strokeStyle = e), i.lineWidth = r === n ? 1 : r, t !== n && (i.fillStyle = t), i
        }, reset: function () {
            var e = this._getContext();
            e.clearRect(0, 0, this.pixelWidth, this.pixelHeight), this.shapes = {}, this.shapeseq = [], this.currentTargetShapeId = n
        }, _drawShape: function (e, t, r, i, s) {
            var o = this._getContext(r, i, s), u, a;
            o.beginPath(), o.moveTo(t[0][0] + .5, t[0][1] + .5);
            for (u = 1, a = t.length; u < a; u++)o.lineTo(t[u][0] + .5, t[u][1] + .5);
            r !== n && o.stroke(), i !== n && o.fill(), this.targetX !== n && this.targetY !== n && o.isPointInPath(this.targetX, this.targetY) && (this.currentTargetShapeId = e)
        }, _drawCircle: function (e, r, i, s, o, u, a) {
            var f = this._getContext(o, u, a);
            f.beginPath(), f.arc(r, i, s, 0, 2 * t.PI, !1), this.targetX !== n && this.targetY !== n && f.isPointInPath(this.targetX, this.targetY) && (this.currentTargetShapeId = e), o !== n && f.stroke(), u !== n && f.fill()
        }, _drawPieSlice: function (e, t, r, i, s, o, u, a) {
            var f = this._getContext(u, a);
            f.beginPath(), f.moveTo(t, r), f.arc(t, r, i, s, o, !1), f.lineTo(t, r), f.closePath(), u !== n && f.stroke(), a && f.fill(), this.targetX !== n && this.targetY !== n && f.isPointInPath(this.targetX, this.targetY) && (this.currentTargetShapeId = e)
        }, _drawRect: function (e, t, n, r, i, s, o) {
            return this._drawShape(e, [
                [t, n],
                [t + r, n],
                [t + r, n + i],
                [t, n + i],
                [t, n]
            ], s, o)
        }, appendShape: function (e) {
            return this.shapes[e.id] = e, this.shapeseq.push(e.id), this.lastShapeId = e.id, e.id
        }, replaceWithShape: function (e, t) {
            var n = this.shapeseq, r;
            this.shapes[t.id] = t;
            for (r = n.length; r--;)n[r] == e && (n[r] = t.id);
            delete this.shapes[e]
        }, replaceWithShapes: function (e, t) {
            var n = this.shapeseq, r = {}, i, s, o;
            for (s = e.length; s--;)r[e[s]] = !0;
            for (s = n.length; s--;)i = n[s], r[i] && (n.splice(s, 1), delete this.shapes[i], o = s);
            for (s = t.length; s--;)n.splice(o, 0, t[s].id), this.shapes[t[s].id] = t[s]
        }, insertAfterShape: function (e, t) {
            var n = this.shapeseq, r;
            for (r = n.length; r--;)if (n[r] === e) {
                n.splice(r + 1, 0, t.id), this.shapes[t.id] = t;
                return
            }
        }, removeShapeId: function (e) {
            var t = this.shapeseq, n;
            for (n = t.length; n--;)if (t[n] === e) {
                t.splice(n, 1);
                break
            }
            delete this.shapes[e]
        }, getShapeAt: function (e, t, n) {
            return this.targetX = t, this.targetY = n, this.render(), this.currentTargetShapeId
        }, render: function () {
            var e = this.shapeseq, t = this.shapes, n = e.length, r = this._getContext(), i, s, o;
            r.clearRect(0, 0, this.pixelWidth, this.pixelHeight);
            for (o = 0; o < n; o++)i = e[o], s = t[i], this["_draw" + s.type].apply(this, s.args);
            this.interact || (this.shapes = {}, this.shapeseq = [])
        }}), F = o(B, {init: function (t, n, i) {
            var s;
            F._super.init.call(this, t, n, i), i[0] && (i = i[0]), r.data(i, "_jqs_vcanvas", this), this.canvas = e.createElement("span"), r(this.canvas).css({display: "inline-block", position: "relative", overflow: "hidden", width: t, height: n, margin: "0px", padding: "0px", verticalAlign: "top"}), this._insert(this.canvas, i), this._calculatePixelDims(t, n, this.canvas), this.canvas.width = this.pixelWidth, this.canvas.height = this.pixelHeight, s = '<v:group coordorigin="0 0" coordsize="' + this.pixelWidth + " " + this.pixelHeight + '"' + ' style="position:absolute;top:0;left:0;width:' + this.pixelWidth + "px;height=" + this.pixelHeight + 'px;"></v:group>', this.canvas.insertAdjacentHTML("beforeEnd", s), this.group = r(this.canvas).children()[0], this.rendered = !1, this.prerender = ""
        }, _drawShape: function (e, t, r, i, s) {
            var o = [], u, a, f, l, h, p, d;
            for (d = 0, p = t.length; d < p; d++)o[d] = "" + t[d][0] + "," + t[d][1];
            return u = o.splice(0, 1), s = s === n ? 1 : s, a = r === n ? ' stroked="false" ' : ' strokeWeight="' + s + 'px" strokeColor="' + r + '" ', f = i === n ? ' filled="false"' : ' fillColor="' + i + '" filled="true" ', l = o[0] === o[o.length - 1] ? "x " : "", h = '<v:shape coordorigin="0 0" coordsize="' + this.pixelWidth + " " + this.pixelHeight + '" ' + ' id="jqsshape' + e + '" ' + a + f + ' style="position:absolute;left:0px;top:0px;height:' + this.pixelHeight + "px;width:" + this.pixelWidth + 'px;padding:0px;margin:0px;" ' + ' path="m ' + u + " l " + o.join(", ") + " " + l + 'e">' + " </v:shape>", h
        }, _drawCircle: function (e, t, r, i, s, o, u) {
            var a, f, l;
            return t -= i, r -= i, a = s === n ? ' stroked="false" ' : ' strokeWeight="' + u + 'px" strokeColor="' + s + '" ', f = o === n ? ' filled="false"' : ' fillColor="' + o + '" filled="true" ', l = '<v:oval  id="jqsshape' + e + '" ' + a + f + ' style="position:absolute;top:' + r + "px; left:" + t + "px; width:" + i * 2 + "px; height:" + i * 2 + 'px"></v:oval>', l
        }, _drawPieSlice: function (e, r, i, s, o, u, a, f) {
            var l, h, p, d, v, m, g, y;
            if (o === u)return"";
            u - o === 2 * t.PI && (o = 0, u = 2 * t.PI), h = r + t.round(t.cos(o) * s), p = i + t.round(t.sin(o) * s), d = r + t.round(t.cos(u) * s), v = i + t.round(t.sin(u) * s);
            if (h === d && p === v) {
                if (u - o < t.PI)return"";
                h = d = r + s, p = v = i
            }
            return h === d && p === v && u - o < t.PI ? "" : (l = [r - s, i - s, r + s, i + s, h, p, d, v], m = a === n ? ' stroked="false" ' : ' strokeWeight="1px" strokeColor="' + a + '" ', g = f === n ? ' filled="false"' : ' fillColor="' + f + '" filled="true" ', y = '<v:shape coordorigin="0 0" coordsize="' + this.pixelWidth + " " + this.pixelHeight + '" ' + ' id="jqsshape' + e + '" ' + m + g + ' style="position:absolute;left:0px;top:0px;height:' + this.pixelHeight + "px;width:" + this.pixelWidth + 'px;padding:0px;margin:0px;" ' + ' path="m ' + r + "," + i + " wa " + l.join(", ") + ' x e">' + " </v:shape>", y)
        }, _drawRect: function (e, t, n, r, i, s, o) {
            return this._drawShape(e, [
                [t, n],
                [t, n + i],
                [t + r, n + i],
                [t + r, n],
                [t, n]
            ], s, o)
        }, reset: function () {
            this.group.innerHTML = ""
        }, appendShape: function (e) {
            var t = this["_draw" + e.type].apply(this, e.args);
            return this.rendered ? this.group.insertAdjacentHTML("beforeEnd", t) : this.prerender += t, this.lastShapeId = e.id, e.id
        }, replaceWithShape: function (e, t) {
            var n = r("#jqsshape" + e), i = this["_draw" + t.type].apply(this, t.args);
            n[0].outerHTML = i
        }, replaceWithShapes: function (e, t) {
            var n = r("#jqsshape" + e[0]), i = "", s = t.length, o;
            for (o = 0; o < s; o++)i += this["_draw" + t[o].type].apply(this, t[o].args);
            n[0].outerHTML = i;
            for (o = 1; o < e.length; o++)r("#jqsshape" + e[o]).remove()
        }, insertAfterShape: function (e, t) {
            var n = r("#jqsshape" + e), i = this["_draw" + t.type].apply(this, t.args);
            n[0].insertAdjacentHTML("afterEnd", i)
        }, removeShapeId: function (e) {
            var t = r("#jqsshape" + e);
            this.group.removeChild(t[0])
        }, getShapeAt: function (e, t, n) {
            var r = e.id.substr(8);
            return r
        }, render: function () {
            this.rendered || (this.group.innerHTML = this.prerender, this.rendered = !0)
        }})
    })
})(document, Math)