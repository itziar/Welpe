! function(e) {
    function a(a) {
        return void 0 !== document.getElementsByClassName ? (a || (a = {}), this.buttonStyles = "<style>.yj-yam-spittle{max-width:20px !important;width:100% !important;border:0 !important;margin:2px 0 0 !important;vertical-align: baseline !important;}span.yj-share-copy{position: relative !important;top: -2px !important;-webkit-font-smoothing: antialiased !important;-moz-osx-font-smoothing:grayscale !important;}span.yj-share-copy:hover {color: #fff !important;text-decoration: none !important;}.yj-default-share-button {display:inline-block !important;font-family:Helvetica !important; text-decoration: none !important;text-align: center !important;font-size: 1em !important; padding: 5px 10px !important;background-color: #0072c6 !important;border: 1px solid #005899 !important;color: #fff !important;-moz-border-radius:3px !important;-webkit-border-radius:3px !important;border-radius:3px !important;}</style>", a.hasOwnProperty("defaultMessage") && (b.defaultMessage = a.defaultMessage), a.hasOwnProperty("classSelector") && (b.buttonClassSelector = a.classSelector), a.hasOwnProperty("pageUrl") && (b.pageUrl = encodeURIComponent(a.pageUrl)), this.init = function(e) {
            e.hasOwnProperty("classSelector") ? this.bindButtonClickByClass() : this.createButton(b)
        }, this.createButton = function() {
            var e = document.getElementById(b.containerIdSelector);
            null == e ? console.log("Please specify an element with id='yj-share-button' or pass options as specified in developer.yammer.com") : (e.innerHTML = this.buttonStyles + '<a href="#" class="' + b.buttonClassSelector + '"><img class="yj-yam-spittle" src="https://c64.assets-yammer.com/assets/yammer_spittle_white.png" alt="Yammer Spittle Icon"/> <span class="yj-share-copy">Share</span></a>', this.bindButtonClickByClass())
        }, this.bindButtonClickByClass = function() {
            var e = this;
            this.addEvent(b.buttonClassSelector, "click", function() {
                e.openYammerShare()
            })
        }, this.openYammerShare = function() {
            e.platform.yammerShareOpenPopup()
        }, this.addEvent = function(e, a, d) {
            for (var b = document.getElementsByClassName(e), l = 0, i = b.length; i > l; l++) b[l].addEventListener(a, d, !1)
        }, this.init(a)) : void 0
    }

    function d(e) {
        e || (e = b);
        var a = screen.width / 2 - 300,
            d = screen.height / 2 - 175;
        window.open(b.popurl + "&status=" + encodeURIComponent(e.defaultMessage + " " + e.pageUrl), "YammerShare", "status=0,toolbar=0,location=0,menubar=0,directories=0,resizable=1,scrollbars=0,width=600,height=350,top=" + d + ",left=" + a)
    }
    var b = {
        popurl: "https://www.yammer.com/messages/new?login=true&trk_event=yammer_share",
        defaultMessage: "Via Alexia portal:",
        pageUrl: encodeURIComponent(document.URL),
        containerIdSelector: "yj-share-button",
        buttonClassSelector: "yj-default-share-button"
    };
    e.platform = e.platform || {}, e.platform.yammerShare = a, e.platform.yammerShareOpenPopup = d
}(window.yam = window.yam || {});