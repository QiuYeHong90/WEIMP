/**
 * Created by jjn on 2017/3/17.
 */


!function (t, e, o) {
    "object" == typeof exports ? module.exports = e(require("jquery")) : "function" == typeof define && define.amd ? define(["jquery"], e) : o[t] = e(o.jQuery)
}("SlsModal", function (t) {
    if (!t)return void console.error("请引入jQuery");
    var e = function () {
        var t, e, o = document.createElement("DIV");
        return o.style.cssText = "position:absolute; top:-1000px; width:100px; height:100px; overflow:hidden;", t = document.body.appendChild(o).clientWidth, o.style.overflowY = "scroll", e = o.clientWidth, document.body.removeChild(o), t - e
    }, o = function () {
        this.container = null, this.version = "1.0.0", this.options = {
            onShowBefore: function () {
            },
            onShowAfter: function () {
            },
            onCloseBefore: function () {
            },
            onCloseAfter: function () {
            },
            onClickClose: function () {
            },
            onClickBg: function () {
            },
            onClickBtn: function () {
            },
            isClickClose: !0,
            isClickBtn: !0,
            isClickBg: !0,
            isAutoClose: !0,
            isShowClose: !0,
            header: "标题是啥呢？",
            body: "您想说点什么呢？",
            footer: "",
            btns: [{text: "取消", type: "default"}, {text: "确定", type: "info"}],
            width: "520px",
            offsetTop: !1,
            top: !1
        }, this.defaults = t.extend(!0, {}, this.options), this.init = function (e) {
            return e && "object" == typeof e ? (this.opts = e, this.defaults = t.extend(!0, {}, this.options, e)) : this.opts = {}, this
        }, this.createHtml = function () {
            var t = "";
            if (t += '<div class="sls-modal-container">', t += '<div class="sls-modal-bg"></div>', t += '<div class="sls-modal-content">', this.defaults.header && (t += '<div class="sls-modal-header">', t += this.defaults.header, t += this.defaults.isShowClose ? '<span class="sls-modal-close">×</span>' : "", t += "</div>"), t += '<div class="sls-modal-body">', t += this.defaults.body, t += "</div>", this.defaults.footer || this.defaults.btns && this.defaults.btns.constructor === Array && this.defaults.btns.length) {
                if (t += '<div class="sls-modal-footer">', this.defaults.footer) t += this.defaults.footer; else for (var e = this.defaults.btns, o = 0; o < e.length; o++) {
                    var s = "sls-self-btn-" + e[o].className || "";
                    t += '<span class="sls-modal-btn ' + (e[o].type ? "sls-modal-btn-" + e[o].type : "") + " " + s + '" data-index="' + o + '">', t += e[o].text, t += "</span>"
                }
                t += "</div>"
            }
            return t += "</div>", t += "</div>"
        }
    };
    return o.prototype = {
        constructor: o, setCss: function () {
            var e = {
                container: {
                    width: t(window).width() + "px",
                    height: t(window).height() + "px",
                    position: "fixed",
                    top: "0",
                    left: "0",
                    display: "none",
                    zIndex: "9999999"
                },
                bg: {
                    width: "100%",
                    height: "100%",
                    position: "fixed",
                    top: "0",
                    left: "0",
                    background: "#000",
                    opacity: "0.75"
                },
                content: {
                    width: "420px",
                    height: "auto",
                    background: "#FFF",
                    borderRadius: "3px",
                    marginLeft: "auto",
                    marginRight: "auto",
                    zIndex: "101"
                },
                header: {
                    width: "100%",
                    height: "52px",
                    lineHeight: "52px",
                    textAlign: "center",
                    position: "relative",
                    fontSize: "16px",
                    fontWeight: 700,
                    color: "#333",
                    borderTopLeftRadius: "3px",
                    borderTopRightRadius: "3px"
                },
                close: {
                    display: "inline-block",
                    position: "absolute",
                    top: "0",
                    right: "0",
                    width: "42px",
                    height: "42px",
                    textAlign: "center",
                    lineHeight: "42px",
                    color: "#bbb",
                    fontSize: "24px",
                    cursor: "pointer",
                    fontWeight: "bold"
                },
                body: {padding: "20px"},
                footer: {
                    width: "100%",
                    height: "62px",
                    lineHeight: "62px",
                    textAlign: "right",
                    padding: "0px 20px",
                    borderBottomLeftRadius: "3px",
                    borderBottomRightRadius: "3px"
                },
                btn: {
                    display: "inlineBlock",
                    whiteSpace: "nowrap",
                    cursor: "pointer",
                    border: "1px solid #c0ccda",
                    color: "#1f2d3d",
                    textAlign: "center",
                    outline: "none",
                    margin: 0,
                    padding: "10px 15px",
                    fontSize: "14px",
                    borderRadius: "4px",
                    marginRight: "16px",
                    mozUserSelect: "none",
                    webkitUserSelect: "none",
                    msUserSelect: "none",
                    background: "#fff"
                },
                "btn-info": {color: "#fff", backgroundColor: "#31b0d5", borderColor: "#269abc"},
                "btn-warning": {color: "#fff", backgroundColor: "#ec971f", borderColor: "#d58512"},
                "btn-danger": {color: "#fff", backgroundColor: "#d9534f", borderColor: "#d43f3a"},
                "btn-success": {color: "#fff", backgroundColor: "#449d44", borderColor: "#255625"}
            };
            e = t.extend(!0, {}, e, this.opts.css);
            var o = this.defaults.width || null;
            o && (e.content.width = o);
            for (attr in e)e.hasOwnProperty(attr) && t(".sls-modal-" + attr).css(e[attr]);
            return this
        }, setCenter: function () {
            var e = this.defaults.offsetTop ? parseInt(this.defaults.offsetTop) : 0, o = t(this.container).find(".sls-modal-content"), s = parseInt(o.css("height")), i = parseInt(o.css("width")), n = -(i / 2) + "px", l = -(s / 2 + e) + "px", r = "50%";
            return this.defaults.top !== !1 && "number" == typeof this.defaults.top && (r = this.defaults.top + "px", l = "0px"), o.css({
                position: "absolute",
                top: r,
                left: "50%",
                marginTop: l,
                marginLeft: n
            }), this
        }, render: function () {
            return t("body").append(this.createHtml()), this.container = t(".sls-modal-container").get(0), this
        }, show: function (e) {
            return t(".sls-modal-container").length || e ? (this.setCss().showEvent(), this) : (this.render().setCss().showEvent().resizeEvent(), this.defaults.isAutoClose && (this.closeBtnEvent(), this.btnEvent(), this.bgCloseEvent()), this)
        }, showEvent: function () {
            if (t("html").height() > t(window).height()) {
                var o = e();
                t("body").css({overflow: "hidden", paddingRight: o + "px"})
            }
            return this.defaults.onShowBefore && this.defaults.onShowBefore.call(this), t(".sls-modal-container").show(), this.setCenter(), this.defaults.onShowAfter && this.defaults.onShowAfter.call(this), this
        }, close: function () {
            var e = t(".sls-modal-container");
            return e.length ? (e.remove(), t("body").css({overflowY: "auto", paddingRight: "0px"}), this) : this
        }, closeBtnEvent: function () {
            var e = this;
            return t(".sls-modal-close").on("click", function () {
                e.defaults.isClickClose ? (e.defaults.onCloseBefore && e.defaults.onCloseBefore.call(e, this), e.close(), e.defaults.onCloseAfter && e.defaults.onCloseAfter.call(e, this)) : e.defaults.onClickClose && e.defaults.onClickClose.call(e, this)
            }), this
        }, btnEvent: function () {
            var e = this;
            return t(".sls-modal-btn").on("click", function () {
                e.defaults.isClickBtn ? (e.defaults.onCloseBefore && e.defaults.onCloseBefore.call(e, this, t(this).data("index")), e.close(), e.defaults.onCloseAfter && e.defaults.onCloseAfter.call(e, this, t(this).data("index"))) : e.defaults.onClickBtn && e.defaults.onClickBtn.call(e, this, t(this).data("index"))
            }), this
        }, bgCloseEvent: function () {
            var e = this;
            return t(".sls-modal-bg").on("click", function (t) {
                t.stopPropagation(), t.preventDefault(), e.defaults.isClickBg ? (e.defaults.onCloseBefore && e.defaults.onCloseBefore.call(e, this), e.close(), e.defaults.onCloseAfter && e.defaults.onCloseAfter.call(e, this)) : e.defaults.onClickBg && e.defaults.onClickBg.call(e, this)
            }), this
        }, resizeEvent: function () {
            var e = this;
            return t(window).resize(function () {
                e.show(!0)
            }), e
        }
    }, new o
}, this);