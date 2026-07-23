// Theme manager: light <-> dark via the nav toggle, plus a hidden "blackwall"
// theme unlocked from the home terminal. Preference persists in localStorage.
// A pre-paint inline script in <head> applies the stored theme before this runs
// to avoid a flash of the wrong theme.
(function () {
    "use strict";

    var root = document.documentElement;
    var KEY = "theme";
    var VALID = ["light", "dark", "blackwall"];

    function stored() {
        try {
            var t = localStorage.getItem(KEY);
            if (t === "netrunner") {
                // Legacy id from before the Blackwall rename.
                t = "blackwall";
                localStorage.setItem(KEY, t);
            }
            return t;
        } catch (e) { return null; }
    }
    function save(theme) {
        try { localStorage.setItem(KEY, theme); } catch (e) { /* ignore */ }
    }
    function systemPref() {
        return (window.matchMedia &&
            window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
    }
    function current() {
        return root.getAttribute("data-theme") || "light";
    }
    function updateToggle(theme) {
        var btn = document.getElementById("theme-toggle");
        if (!btn) return;
        var goLight = theme !== "light";
        btn.textContent = goLight ? "\u2600" : "\u263E"; // sun / moon
        var label = goLight ? "Switch to light mode" : "Switch to dark mode";
        btn.setAttribute("aria-label", label);
        btn.setAttribute("title", label);
    }
    function apply(theme, persist) {
        if (VALID.indexOf(theme) === -1) theme = "light";
        root.setAttribute("data-theme", theme);
        if (persist !== false) save(theme);
        updateToggle(theme);
    }

    // Public hook for the terminal widget (home.js).
    window.PortfolioTheme = {
        set: apply,
        current: current,
        // Run a brief full-screen flash, swapping the theme mid-flash so the
        // new look is revealed as the flash fades.
        flash: function (theme, done) {
            var body = document.body;
            apply(theme, true);
            body.classList.add("theme-flash");
            window.setTimeout(function () {
                body.classList.remove("theme-flash");
                if (typeof done === "function") done();
            }, 600);
        }
    };

    document.addEventListener("DOMContentLoaded", function () {
        updateToggle(current());

        var btn = document.getElementById("theme-toggle");
        if (btn) {
            btn.addEventListener("click", function () {
                // Toggle only swaps light <-> dark; this also exits blackwall.
                apply(current() === "light" ? "dark" : "light", true);
            });
        }

        // Follow the OS preference only while the user hasn't picked a theme.
        if (window.matchMedia) {
            var mq = window.matchMedia("(prefers-color-scheme: dark)");
            var onChange = function () { if (!stored()) apply(systemPref(), false); };
            if (mq.addEventListener) mq.addEventListener("change", onChange);
            else if (mq.addListener) mq.addListener(onChange);
        }
    });
})();
