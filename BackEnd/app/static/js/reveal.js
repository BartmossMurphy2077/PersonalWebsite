// Progressive scroll-reveal: fade/slide elements in as they enter the viewport.
// Runs only when IntersectionObserver and motion are available; otherwise the
// content stays fully visible (the .reveal class is only added here).
(function () {
    "use strict";

    var SELECTOR = ".project-card, .timeline-item, .photo-item, .featured-card";
    var reduced = window.matchMedia &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    document.addEventListener("DOMContentLoaded", function () {
        var nodes = document.querySelectorAll(SELECTOR);
        if (!nodes.length) return;

        if (reduced || !("IntersectionObserver" in window)) {
            return; // leave content visible, no animation
        }

        nodes.forEach(function (node) { node.classList.add("reveal"); });

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });

        nodes.forEach(function (node) { observer.observe(node); });
    });
})();
