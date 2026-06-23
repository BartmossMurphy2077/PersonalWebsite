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

        function print(text, className) {
            var line = document.createElement("div");
            line.className = "terminal-line" + (className ? " " + className : "");
            line.textContent = text;
            body.appendChild(line);
            body.scrollTop = body.scrollHeight;
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
            if (Object.prototype.hasOwnProperty.call(responses, cmd)) {
                print(responses[cmd]);
            } else {
                print("command not found: " + cmd + " (try 'help' or 'ls')", "muted");
            }
        }

        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                run(input.value);
                input.value = "";
            }
        });

        terminal.addEventListener("click", function () { input.focus(); });
    }
})();
