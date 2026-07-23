// Blackwall atmosphere: a continuous fullscreen fragment shader (raw WebGL,
// no libraries) that runs only while the hidden "blackwall" theme is active.
//
// Behaviour contract:
// - Never initialises when prefers-reduced-motion is set (CSS scanlines are
//   the fallback) or when WebGL is unavailable.
// - Starts when <html data-theme="blackwall"> appears, tears down when the
//   theme is left (nav toggle exits to light/dark).
// - Adaptive quality: device-pixel-ratio is capped and the render scale
//   steps down when frames run slow, back up when there is headroom.
// - Pauses while the tab is hidden.
(function () {
    "use strict";

    var canvas = document.getElementById("blackwall-canvas");
    if (!canvas) return;

    var reduced = window.matchMedia &&
        window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduced) return;

    var VERT = [
        "attribute vec2 a_pos;",
        "void main() { gl_Position = vec4(a_pos, 0.0, 1.0); }"
    ].join("\n");

    // Domain-warped fbm noise, red-tinted, with per-channel offsets for
    // chromatic aberration, occasional horizontal tears, and a vignette.
    var FRAG = [
        "precision highp float;",
        "uniform vec2 u_res;",
        "uniform float u_time;",
        "",
        "float hash(vec2 p) {",
        "    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123);",
        "}",
        "float noise(vec2 p) {",
        "    vec2 i = floor(p), f = fract(p);",
        "    f = f * f * (3.0 - 2.0 * f);",
        "    return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), f.x),",
        "               mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), f.x), f.y);",
        "}",
        "float fbm(vec2 p) {",
        "    float v = 0.0;",
        "    float a = 0.5;",
        "    for (int i = 0; i < 5; i++) { v += a * noise(p); p *= 2.03; a *= 0.5; }",
        "    return v;",
        "}",
        "float field(vec2 p, float t) {",
        "    vec2 q = vec2(fbm(p * 1.5 + t), fbm(p * 1.5 - t * 0.7));",
        "    vec2 r = vec2(fbm(p * 2.0 + q * 1.8 + vec2(1.7, 9.2) + t * 0.6),",
        "                  fbm(p * 2.0 + q * 1.8 + vec2(8.3, 2.8) - t * 0.4));",
        "    return fbm(p * 2.2 + r * 2.0);",
        "}",
        "void main() {",
        "    vec2 uv = gl_FragCoord.xy / u_res;",
        "    vec2 p = uv * vec2(u_res.x / u_res.y, 1.0);",
        "    float t = u_time * 0.05;",
        "",
        "    // Chromatic aberration: sample the warped field per channel.",
        "    float fr = field(p + vec2(0.014, 0.0), t);",
        "    float fg = field(p, t);",
        "    float fb = field(p - vec2(0.014, 0.0), t);",
        "",
        "    vec3 col;",
        "    col.r = pow(fr, 1.6) * 0.85;",
        "    col.g = pow(fg, 2.6) * 0.10;",
        "    col.b = pow(fb, 2.3) * 0.12;",
        "",
        "    // Occasional horizontal tear across the field.",
        "    float band = step(0.996, noise(vec2(uv.y * 90.0, floor(u_time * 6.0))));",
        "    col *= 1.0 - band * 0.55;",
        "    col += band * vec3(0.30, 0.02, 0.04);",
        "",
        "    // Vignette so content in the middle stays readable.",
        "    float vig = smoothstep(1.15, 0.25, length(uv - 0.5));",
        "    col *= vig * 0.9;",
        "",
        "    gl_FragColor = vec4(col, 1.0);",
        "}"
    ].join("\n");

    var gl = null;
    var program = null;
    var rafId = null;
    var startTime = 0;
    var uRes = null;
    var uTime = null;

    // Adaptive render scale: 1 = full (capped) resolution.
    var SCALES = [1.0, 0.75, 0.5, 0.35];
    var scaleIdx = 0;
    var frameCount = 0;
    var slowFrames = 0;
    var lastFrameTime = 0;

    function compile(type, source) {
        var shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);
        if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
            gl.deleteShader(shader);
            return null;
        }
        return shader;
    }

    function resize() {
        if (!gl) return;
        var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
        var scale = SCALES[scaleIdx] * dpr;
        var w = Math.max(1, Math.floor(window.innerWidth * scale));
        var h = Math.max(1, Math.floor(window.innerHeight * scale));
        if (canvas.width !== w || canvas.height !== h) {
            canvas.width = w;
            canvas.height = h;
            gl.viewport(0, 0, w, h);
        }
    }

    function adapt(now) {
        // Track slow frames over a window; step the scale down when the
        // device can't keep up, back up when it clearly can.
        if (lastFrameTime) {
            var dt = now - lastFrameTime;
            if (dt > 26) slowFrames++;
        }
        lastFrameTime = now;
        frameCount++;
        if (frameCount >= 90) {
            if (slowFrames > 30 && scaleIdx < SCALES.length - 1) {
                scaleIdx++;
                resize();
            } else if (slowFrames < 5 && scaleIdx > 0) {
                scaleIdx--;
                resize();
            }
            frameCount = 0;
            slowFrames = 0;
        }
    }

    function frame(now) {
        if (!gl) return;
        rafId = window.requestAnimationFrame(frame);
        if (document.hidden) return;
        adapt(now);
        gl.uniform2f(uRes, canvas.width, canvas.height);
        gl.uniform1f(uTime, (now - startTime) / 1000);
        gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }

    function start() {
        if (gl) return;
        gl = canvas.getContext("webgl", {
            alpha: false,
            antialias: false,
            powerPreference: "low-power"
        });
        if (!gl) { gl = null; return; }

        var vs = compile(gl.VERTEX_SHADER, VERT);
        var fs = compile(gl.FRAGMENT_SHADER, FRAG);
        if (!vs || !fs) { gl = null; return; }

        program = gl.createProgram();
        gl.attachShader(program, vs);
        gl.attachShader(program, fs);
        gl.linkProgram(program);
        if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
            gl = null;
            program = null;
            return;
        }
        gl.useProgram(program);

        var buffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
        gl.bufferData(gl.ARRAY_BUFFER,
            new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
        var aPos = gl.getAttribLocation(program, "a_pos");
        gl.enableVertexAttribArray(aPos);
        gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);

        uRes = gl.getUniformLocation(program, "u_res");
        uTime = gl.getUniformLocation(program, "u_time");

        scaleIdx = 0;
        frameCount = 0;
        slowFrames = 0;
        lastFrameTime = 0;
        startTime = window.performance ? performance.now() : Date.now();
        resize();
        rafId = window.requestAnimationFrame(frame);
    }

    function stop() {
        if (rafId !== null) {
            window.cancelAnimationFrame(rafId);
            rafId = null;
        }
        if (gl) {
            var lose = gl.getExtension("WEBGL_lose_context");
            if (lose) lose.loseContext();
        }
        gl = null;
        program = null;
    }

    function sync() {
        var active = document.documentElement.getAttribute("data-theme") === "blackwall";
        if (active) start();
        else stop();
    }

    window.addEventListener("resize", resize);

    var observer = new MutationObserver(sync);
    observer.observe(document.documentElement, {
        attributes: true,
        attributeFilter: ["data-theme"]
    });

    // The pre-paint script may have applied blackwall before this ran.
    sync();
})();
