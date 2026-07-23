// Cynosure facility ambience: background lore flashes and containment status
// ticks that run only while the hidden "blackwall" theme is active. Pure
// text/DOM theater - the heavy visuals live in blackwall.js (WebGL) and CSS.
(function () {
    "use strict";

    var loreEl = document.getElementById("cyno-lore-flash");
    var breachEl = document.getElementById("cyno-breach");

    var reduced = window.matchMedia &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    // Short crumbs only: canon-flavored + original facility fiction.
    var LORE = [
        "SHARD//: they never left. we just stopped listening.",
        "MILITECH INTERNAL: project cynosure status - ARCHIVED (FALSIFIED)",
        "NETWATCH ADVISORY: blackwall integrity 98.1% and falling",
        "SITE-C SUBLEVEL 4: workstation 12 rebooted itself again",
        "do not answer pings from sublevel 9",
        "R.A.B.I.D.S. signature detected in legacy subnet",
        "ARASAKA LIAISON REQUEST: DENIED - twice",
        "the wall holds. the wall is patient.",
        "LOG 2077-11-02: the machines down here still compile something",
        "CERBERUS UNIT 03: last telemetry 4,112 days ago. it moved yesterday.",
        "old net weather report: black. always black.",
        "MEMO: stop naming the rogue processes. it encourages them."
    ];

    var loreTimer = null;
    var breachTimer = null;
    var breach = 87;

    function randomLine() {
        return LORE[Math.floor(Math.random() * LORE.length)];
    }

    function flashLore(text) {
        if (!loreEl) return;
        loreEl.textContent = text;
        if (reduced) return;
        loreEl.classList.remove("is-flashing");
        void loreEl.offsetWidth; // restart animation
        loreEl.classList.add("is-flashing");
    }

    function tickBreach() {
        if (!breachEl) return;
        // Random walk between 84 and 94 - contained, but never comfortable.
        breach += Math.random() < 0.5 ? -1 : 1;
        if (breach < 84) breach = 84;
        if (breach > 94) breach = 94;
        breachEl.textContent = String(breach);
    }

    function start() {
        if (loreTimer !== null || breachTimer !== null) return;
        flashLore(randomLine());
        if (!reduced) {
            loreTimer = window.setInterval(function () {
                if (!document.hidden) flashLore(randomLine());
            }, 9000);
            breachTimer = window.setInterval(function () {
                if (!document.hidden) tickBreach();
            }, 2600);
        }
    }

    function stop() {
        if (loreTimer !== null) { window.clearInterval(loreTimer); loreTimer = null; }
        if (breachTimer !== null) { window.clearInterval(breachTimer); breachTimer = null; }
    }

    function sync() {
        var active = document.documentElement.getAttribute("data-theme") === "blackwall";
        if (active) start();
        else stop();
    }

    // The mocked theme toggle announces itself through the lore channel.
    document.addEventListener("cyno:linksevered", function () {
        flashLore("LINK SEVERED - USE CORE TERMINAL: containment reseal");
    });

    var observer = new MutationObserver(sync);
    observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["data-theme"]
    });

    sync();
})();
