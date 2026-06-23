// Terminal-boot page transition. Plays a brief scanline flash when leaving a
// same-origin page, and lets CSS fade the new page in on load.
(function () {
    "use strict";

    var REDUCED = window.matchMedia &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    function isInternalLink(anchor) {
        if (!anchor || !anchor.href) return false;
        if (anchor.target === "_blank") return false;
        if (anchor.hasAttribute("download")) return false;
        if (anchor.origin !== window.location.origin) return false;
        var href = anchor.getAttribute("href") || "";
        return !href.startsWith("#") && !href.startsWith("mailto:");
    }

    document.addEventListener("click", function (event) {
        if (REDUCED || event.defaultPrevented) return;
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;

        var anchor = event.target.closest("a");
        if (!isInternalLink(anchor)) return;
        if (anchor.pathname === window.location.pathname) return;

        event.preventDefault();
        document.body.classList.add("booting");
        window.setTimeout(function () {
            window.location.href = anchor.href;
        }, 320);
    });

    // Clear the overlay if the page is restored from the bfcache.
    window.addEventListener("pageshow", function () {
        document.body.classList.remove("booting");
    });
})();
