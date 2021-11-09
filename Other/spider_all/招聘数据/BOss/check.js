var securityPageName = "securityCheck";
(function () {
    var image = new Image;
    var url = window.location.href;
    var lenSrcReferer = url.split("srcReferer").length - 1;
    image.src = "https://t.zhipin.com/f.gif?pk=" + securityPageName + "&len=" + lenSrcReferer + "&r=" + document.referrer
})();
(function () {
    var pageInterNum = 0;
    var pageStartTime = (new Date).getTime();
    var UA = window.navigator.userAgent;
    var isIE;
    if (UA.indexOf("MSIE ") > -1) {
        isIE = true
    }

    function init(frame) {
        var COOKIE_DOMAIN = function () {
            var hostName = location.hostname;
            if (hostName === "localhost" || /^(\d+\.){3}\d+$/.test(hostName)) {
                return hostName
            }
            return "." + hostName.split(".").slice(-2).join(".")
        }();
        var seriesLoadScript = function (scriptUrl, callback) {
            var url = scriptUrl;
            var script = document.createElement("script");
            script.setAttribute("type", "text/javascript");
            script.setAttribute("charset", "UTF-8");
            script.onload = script.onreadystatechange = function () {
                if (!isIE || this.readyState == "loaded" || this.readyState == "complete") {
                    callback()
                }
            };
            script.setAttribute("src", scriptUrl);
            if (frame.tagName != "IFRAME") {
                frame.appendChild(script)
            } else if (frame.contentDocument) {
                if (frame.contentDocument.body) {
                    frame.contentDocument.body.appendChild(script)
                } else {
                    frame.contentDocument.documentElement.appendChild(script)
                }
            } else if (frame.document) {
                if (frame.document.body) {
                    frame.document.body.appendChild(script)
                } else {
                    frame.document.documentElement.appendChild(script)
                }
            }
        };
        var getQueryString = function (name) {
            var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
            var r = window.location.search.substr(1).match(reg);
            if (r != null) return unescape(r[2]);
            return null
        };
        var Cookie = {
            get: function (name) {
                var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
                if (arr = document.cookie.match(reg)) {
                    return unescape(arr[2])
                } else {
                    return null
                }
            }, set: function (name, value, time, domain, path) {
                var str = name + "=" + encodeURIComponent(value);
                if (time) {
                    var date = new Date(time).toGMTString();
                    str += ";expires=" + date
                }
                str = domain ? str + ";domain=" + domain : str;
                str = path ? str + ";path=" + path : str;
                document.cookie = str
            }
        };
        var urlFilter = {
            config: {
                url: "",
                whiteHostList: ["m.zhipin.com", "www.zhipin.com", "pre-www.zhipin.com"],
                blackPathList: ["security-check.html", "security-check1.html"]
            }, setStrategy: function () {
                var url = urlFilter.config.url;
                switch (true) {
                    case urlFilter.isBlackHost(url) || urlFilter.hasBlackPath(url):
                        urlFilter.config.url = "/";
                        break
                }
                return urlFilter.config.url
            }, isAbsolutePathStartable: function (url) {
                return url.indexOf("//") < 0 && url.indexOf("/") === 0
            }, isBlackHost: function (url) {
                var isBlackHost = false;
                var rule = /^(https?)?(:?\/\/+)([^\/?]*)(.*)?$/;
                url.replace(rule, function (res, $1, $2, $3, $4) {
                    isBlackHost = !urlFilter.isHostInWhiteList($3);
                    console.error("hostname", $3, "isBlackHost", isBlackHost);
                    return isBlackHost ? "/" : url
                });
                return isBlackHost
            }, hasBlackPath: function (url) {
                var isBlackPath = false;
                var blackPathList = urlFilter.config.blackPathList;
                for (var i = 0; i < blackPathList.length; i++) {
                    if (url.indexOf(blackPathList[i]) > -1) {
                        isBlackPath = true;
                        break
                    }
                }
                return isBlackPath
            }, isHostInWhiteList: function (hostname) {
                return urlFilter.config.whiteHostList.indexOf(hostname) > -1
            }, filter: function (url) {
                urlFilter.config.url = decodeURIComponent(url || "/");
                return urlFilter.setStrategy()
            }
        };
        var jumpReplace = function (url) {
            var filterUrl = urlFilter.filter(url);
            window.location.replace(filterUrl)
        };
        var jumpPage = function (srcReferer, callbackUrl) {
            if (callbackUrl || srcReferer.indexOf("security-check.html") > -1) {
                jumpReplace(callbackUrl)
            } else {
                jumpReplace(srcReferer)
            }
            var image = new Image;
            image.src = "https://t.zhipin.com/f.gif?pk=" + securityPageName + "&ca=securityCheckJump_" + Math.round(((new Date).getTime() - pageStartTime) / 1e3) + "&r=" + document.referrer
        };
        var url = window.location.href;
        var seed = getQueryString("seed") || "";
        var ts = getQueryString("ts");
        var fileName = getQueryString("name");
        var callbackUrl = getQueryString("callbackUrl");
        var srcReferer = getQueryString("srcReferer") || "";
        if (fileName === "null" || !seed || !fileName || !callbackUrl) {
            var fileImage = new Image;
            fileImage.src = "https://t.zhipin.com/f.gif?pk=" + securityPageName + "&ca=securityCheckUrlFile&url=" + window.location.href
        }
        if (seed && ts && fileName) {
            var interTimer = setInterval(function () {
                pageInterNum++;
                if (pageInterNum > 5) {
                    clearInterval(interTimer)
                }
                var image = new Image;
                image.src = "https://t.zhipin.com/f.gif?pk=" + securityPageName + "&ca=securityCheckTimer_" + Math.round(((new Date).getTime() - pageStartTime) / 1e3) + "&r=" + document.referrer
            }, 1e4);
            seriesLoadScript("security-js/" + fileName + ".js", function () {
                var expiredate = (new Date).getTime() + 32 * 60 * 60 * 1e3 * 2;
                var code = "";
                var nativeParams = {};
                var ABC = window.ABC || frame.contentWindow.ABC;
                try {
                    code = (new ABC).z(seed, parseInt(ts) + (480 + (new Date).getTimezoneOffset()) * 60 * 1e3)
                } catch (e) {
                }
                if (code && callbackUrl) {
                    Cookie.set("__zp_stoken__", code, expiredate, COOKIE_DOMAIN, "/");
                    if (typeof window.wst != "undefined" && typeof wst.postMessage == "function") {
                        nativeParams = {
                            name: "setWKCookie",
                            params: {
                                url: COOKIE_DOMAIN,
                                name: "__zp_stoken__",
                                value: encodeURIComponent(code),
                                expiredate: expiredate,
                                path: "/"
                            }
                        };
                        window.wst.postMessage(JSON.stringify(nativeParams))
                    }
                    jumpPage(srcReferer, callbackUrl)
                } else {
                    var nocodeImage = new Image;
                    nocodeImage.src = "https://t.zhipin.com/f.gif?pk=" + securityPageName + "&ca=securityCheckNoCode_" + Math.round(((new Date).getTime() - pageStartTime) / 1e3) + "&r=" + document.referrer;
                    jumpReplace("/")
                }
            })
        }
    }

    var ie = !!(window.attachEvent && !window.opera);
    var wk = /webkit\/(\d+)/i.test(navigator.userAgent) && RegExp.$1 < 525;
    var fn = [];
    var run = function () {
        for (var i = 0; i < fn.length; i++) fn[i]()
    };

    function ready(f) {
        if (!ie && !wk && document.addEventListener) return document.addEventListener("DOMContentLoaded", f, false);
        if (fn.push(f) > 1) return;
        if (ie) (function () {
            try {
                document.documentElement.doScroll("left");
                run()
            } catch (err) {
                setTimeout(arguments.callee, 0)
            }
        })(); else if (wk) var t = setInterval(function () {
            if (/^(loaded|complete)$/.test(document.readyState)) clearInterval(t), run()
        }, 0)
    }

    ready(function () {
        var na = window.navigator.userAgent.toLowerCase();
        if (na.match(/micromessenger/i) == "micromessenger" || na.match(/wkwebview/i) == "wkwebview") {
            init(document.getElementsByTagName("head").item(0));
            return
        }
        var frame = document.createElement("iframe");
        frame.style.height = 0;
        frame.style.width = 0;
        frame.style.margin = 0;
        frame.style.padding = 0;
        frame.style.border = "0 none";
        frame.name = "zhipinFrame";
        frame.src = "about:blank";
        if (frame.attachEvent) {
            frame.attachEvent("onload", function () {
                init(frame)
            })
        } else {
            frame.onload = function () {
                init(frame)
            }
        }
        (document.body || document.documentElement).appendChild(frame)
    })
})();
var
    _hmt = _hmt || [];
(function () {
    var hm = document.createElement("script");
    hm.src = "https://hm.baidu.com/hm.js?194df3105ad7148dcf2b98a91b5e727a";
    var s = document.getElementsByTagName("script")[0];
    s.parentNode.insertBefore(hm, s)
})();
