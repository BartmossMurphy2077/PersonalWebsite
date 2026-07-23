// Home-page interactions: rotating typewriter subtitle + mini terminal widget.
(function () {
    "use strict";

    // ---- Typewriter ----
    var twEl = document.getElementById("typewriter-text");
    if (twEl) {
        var lines = [];
        try { lines = JSON.parse(twEl.dataset.lines || "[]"); } catch (e) { lines = []; }
        if (lines.length) {
            var lineIdx = 0, charIdx = 0, deleting = false;

            function tick() {
                var current = lines[lineIdx];
                if (!deleting) {
                    charIdx++;
                    twEl.textContent = current.slice(0, charIdx);
                    if (charIdx === current.length) {
                        deleting = true;
                        return window.setTimeout(tick, 1600);
                    }
                } else {
                    charIdx--;
                    twEl.textContent = current.slice(0, charIdx);
                    if (charIdx === 0) {
                        deleting = false;
                        lineIdx = (lineIdx + 1) % lines.length;
                    }
                }
                window.setTimeout(tick, deleting ? 45 : 80);
            }
            tick();
        }
    }

    // ---- Terminal widget ----
    var terminal = document.getElementById("terminal");
    var input = document.getElementById("terminal-input");
    var body = document.getElementById("terminal-body");
    if (terminal && input && body) {
        var responses = {};
        try { responses = JSON.parse(terminal.dataset.responses || "{}"); } catch (e) { responses = {}; }

        var locked = false; // disables input during the icebreak sequence

        function print(text, className) {
            var line = document.createElement("div");
            line.className = "terminal-line" + (className ? " " + className : "");
            line.textContent = text;
            body.appendChild(line);
            body.scrollTop = body.scrollHeight;
        }

        function setTheme(theme) {
            if (window.PortfolioTheme) window.PortfolioTheme.set(theme, true);
        }

        // The hidden cyberpunk unlock: prints a fake ICE-breach sequence, then
        // flashes into the blackwall theme. Nods to the BartmossMurphy2077 handle.
        function runIcebreak() {
            if (!window.PortfolioTheme) {
                print("theme engine unavailable", "muted");
                return;
            }
            locked = true;
            var lines = [
                ["BREACHING ICE...", "muted"],
                ["ARASAKA DAEMON.SYS .............. NEUTRALIZED", "accent"],
                ["BLACKWALL HANDSHAKE ............. OK", "accent"],
                ["FLATLINE PROTOCOL ............... BYPASSED", "accent"],
                ["> Rache Bartmoss and Spider Murphy was here", "accent"],
                ["THEME PACK DECRYPTED: BLACKWALL", "accent"]
            ];
            var i = 0;
            (function step() {
                if (i < lines.length) {
                    print(lines[i][0], lines[i][1]);
                    i++;
                    window.setTimeout(step, 190);
                } else {
                    window.PortfolioTheme.flash("blackwall", function () {
                        print("// welcome to the net, choom.", "accent");
                        locked = false;
                    });
                }
            })();
        }

        function handleTheme(arg) {
            if (arg === "light" || arg === "dark") {
                setTheme(arg);
                print("theme set: " + arg);
            } else if (arg === "icebreak" || arg === "blackwall" || arg === "netrunner") {
                // "netrunner" kept as a legacy alias from before the rename.
                runIcebreak();
            } else if (!arg) {
                print("usage: theme <light|dark>", "muted");
            } else {
                print("unknown theme: " + arg, "muted");
            }
        }

        function run(raw) {
            var cmd = raw.trim();
            print("guest@hugo:~$ " + cmd);
            if (!cmd) return;
            if (cmd === "clear") { body.innerHTML = ""; return; }
            if (cmd === "ls") {
                print(Object.keys(responses).join("  ") || "(no commands)", "muted");
                return;
            }
            if (cmd === "theme" || cmd.indexOf("theme ") === 0) {
                handleTheme(cmd.slice(5).trim());
                return;
            }
            if (cmd === "help") {
                if (responses.help) print(responses.help);
                print("tip: 'theme dark' / 'theme light' switch the look. some themes are hidden.", "muted");
                return;
            }
            if (Object.prototype.hasOwnProperty.call(responses, cmd)) {
                print(responses[cmd]);
            } else {
                print("command not found: " + cmd + " (try 'help' or 'ls')", "muted");
            }
        }

        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter" && !locked) {
                run(input.value);
                input.value = "";
            }
        });

        terminal.addEventListener("click", function () { if (!locked) input.focus(); });

        // One-time breadcrumb: nudge first-time visitors toward the shell
        // (and, eventually, the hidden theme) without spoiling the command.
        try {
            if (!localStorage.getItem("bw-hint-seen")) {
                print("// first login detected. this shell keeps secrets - start with 'help'.", "muted");
                localStorage.setItem("bw-hint-seen", "1");
            }
        } catch (e) { /* private mode: skip the hint */ }
    }
})();
