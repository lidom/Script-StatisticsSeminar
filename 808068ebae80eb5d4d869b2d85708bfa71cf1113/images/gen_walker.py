import sys
# Timeline (one 9 s loop): 0-35% data rains into the head, 36% it wakes up,
# 40-92% it shuffles off to the right, 92-100% it fades out and resets.
T = 9
def steps(start, end, n, a, b):
    """Alternate between values a and b in n steps from start% to end%."""
    out = []
    for i in range(n + 1):
        p = start + (end - start) * i / n
        out.append((p, a if i % 2 == 0 else b))
    return out

def kf(name, frames):
    body = "\n".join(f"  {p:.1f}% {{ {v} }}" for p, v in frames)
    return f"@keyframes {name} {{\n{body}\n}}"

leg1 = [(0, "transform: rotate(0deg)"), (40, "transform: rotate(0deg)")] + \
       [(p, f"transform: rotate({v}deg)") for p, v in steps(42, 90, 12, 22, -22)] + \
       [(92, "transform: rotate(0deg)"), (100, "transform: rotate(0deg)")]
leg2 = [(0, "transform: rotate(0deg)"), (40, "transform: rotate(0deg)")] + \
       [(p, f"transform: rotate({v}deg)") for p, v in steps(42, 90, 12, -22, 22)] + \
       [(92, "transform: rotate(0deg)"), (100, "transform: rotate(0deg)")]
sway = [(0, "transform: rotate(0deg)"), (40, "transform: rotate(0deg)")] + \
       [(p, f"transform: rotate({v}deg)") for p, v in steps(42, 90, 12, 4, -2)] + \
       [(92, "transform: rotate(0deg)"), (100, "transform: rotate(0deg)")]
css = f"""
/* Self-contained accent colour, so the SVG does not depend on a cached site stylesheet */
.accent  {{ color: var(--bs-primary, #388e00); }}
.walker  {{ animation: walk {T}s linear infinite; }}
.body    {{ animation: sway {T}s linear infinite; transform-box: fill-box; transform-origin: 50% 100%; }}
.leg1    {{ animation: leg1 {T}s linear infinite; transform-box: fill-box; transform-origin: 50% 0%; }}
.leg2    {{ animation: leg2 {T}s linear infinite; transform-box: fill-box; transform-origin: 50% 0%; }}
.rain    {{ animation: rain {T}s linear infinite; }}
.rain.r2 {{ animation-name: rain2; }}
.rain.r3 {{ animation-name: rain3; }}
.stream  {{ animation: stream {T}s linear infinite; stroke-dasharray: 2 5; }}
.brain   {{ animation: brain {T}s linear infinite; }}
.eye     {{ animation: eye {T}s steps(1) infinite; }}
.zap     {{ animation: zap {T}s steps(1) infinite; }}
{kf("walk", [(0, "transform: translateX(0); opacity: 1"), (40, "transform: translateX(0); opacity: 1"),
             (90, "transform: translateX(250px); opacity: 1"), (95, "transform: translateX(262px); opacity: 0"),
             (99, "transform: translateX(0); opacity: 0"), (100, "transform: translateX(0); opacity: 1")])}
{kf("sway", sway)}
{kf("leg1", leg1)}
{kf("leg2", leg2)}
{kf("rain",  [(0, "transform: translateY(-150px)"), (35, "transform: translateY(45px)"), (100, "transform: translateY(45px)")])}
{kf("rain2", [(0, "transform: translateY(-170px)"), (35, "transform: translateY(50px)"), (100, "transform: translateY(50px)")])}
{kf("rain3", [(0, "transform: translateY(-140px)"), (35, "transform: translateY(48px)"), (100, "transform: translateY(48px)")])}
{kf("stream", [(0, "stroke-dashoffset: 0; opacity: 0.6"), (35, "stroke-dashoffset: -40; opacity: 0.6"),
               (40, "stroke-dashoffset: -46; opacity: 0"), (97, "opacity: 0"), (100, "stroke-dashoffset: 0; opacity: 0.6")])}
{kf("brain", [(0, "opacity: 0"), (35, "opacity: 0.35"), (92, "opacity: 0.35"), (100, "opacity: 0")])}
{kf("eye", [(0, "fill: transparent"), (36, "fill: currentColor"), (95, "fill: transparent")])}
{kf("zap", [(0, "opacity: 0"), (36, "opacity: 1"), (40, "opacity: 0")])}
@media (prefers-reduced-motion: reduce) {{
  .stats-monster * {{ animation: none !important; }}
  .rain {{ transform: translateY(-75px); }}
}}
"""

def column(x, tokens, cls):
    spans = "".join(f'<tspan x="{x}" dy="13">{t}</tspan>' for t in tokens)
    return f'<text class="rain {cls}" x="{x}" y="0" text-anchor="middle" font-size="9.5">{spans}</text>'

svg = f'''<svg viewBox="0 0 430 215" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Animation: streams of data rain into the head of a Frankenstein monster; its head fills up, its eye lights up, and it shuffles off like a zombie, arms stretched out">
  <style>{css}</style>
  <defs>
    <clipPath id="sky"><rect x="0" y="0" width="140" height="41"/></clipPath>
  </defs>
  <!-- ground -->
  <path d="M10 204 H420" stroke="currentColor" stroke-width="1.5" stroke-dasharray="1 6" stroke-linecap="round"/>
  <!-- data streams raining into the head -->
  <g class="accent" fill="currentColor" font-family="Fira Mono, monospace" clip-path="url(#sky)">
    <g stroke="currentColor" stroke-width="1.5" fill="none">
      <path class="stream" d="M54 0 V41"/>
      <path class="stream" d="M68 0 V41"/>
      <path class="stream" d="M82 0 V41"/>
    </g>
    {column(47, ["0","1","1","0","1","0","0","1","1","0","1"], "r1")}
    {column(68, ["x̄","β","σ","p","θ","n","ε","μ","λ","ρ","t"], "r2")}
    {column(92, ["NA","3.1","42",".05","Inf","-1","NaN","0.9","7","1e3"], "r3")}
  </g>
  <g class="walker">
    <!-- legs -->
    <g fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round">
      <path class="leg1" d="M60 156 V202 H70"/>
      <path class="leg2" d="M74 156 V202 H84"/>
    </g>
    <g class="body" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <!-- hair: a histogram -->
      <g class="accent" fill="currentColor" stroke="none">
        <rect x="44" y="41" width="6" height="5"/><rect x="51" y="37" width="6" height="9"/>
        <rect x="58" y="33" width="6" height="13"/><rect x="65" y="31" width="6" height="15"/>
        <rect x="72" y="34" width="6" height="12"/><rect x="79" y="38" width="6" height="8"/>
        <rect x="86" y="42" width="6" height="4"/>
      </g>
      <!-- head, filling up with data -->
      <rect class="brain accent" x="42" y="46" width="52" height="50" rx="5" fill="currentColor" stroke="none"/>
      <rect x="42" y="46" width="52" height="50" rx="5"/>
      <!-- forehead suture -->
      <path d="M48 56 H88 M54 52 V60 M64 52 V60 M74 52 V60 M84 52 V60" stroke-width="1.8"/>
      <!-- x-bar eye, lights up once the data is in -->
      <path d="M74 66 H88"/>
      <circle class="eye accent" cx="81" cy="74" r="4.5" fill="transparent" stroke="currentColor"/>
      <!-- mouth: jagged -->
      <path d="M70 87 L74 84 L78 88 L82 84 L86 88 L90 85" stroke-width="2"/>
      <!-- bolts on both sides of the head -->
      <g stroke-width="2">
        <rect x="36" y="76" width="6" height="4" rx="1"/>
        <rect x="94" y="76" width="6" height="4" rx="1"/>
        <rect x="32" y="73" width="4" height="10" rx="1.5" fill="currentColor"/>
        <rect x="100" y="73" width="4" height="10" rx="1.5" fill="currentColor"/>
      </g>
      <g class="zap accent" stroke="currentColor" stroke-width="2">
        <path d="M30 73 L25 68 M29 78 L22 78 M30 83 L25 88 M106 73 L111 68 M107 78 L114 78 M106 83 L111 88"/>
      </g>
      <!-- neck -->
      <path d="M58 96 V104 M74 96 V104"/>
      <!-- torso -->
      <rect x="52" y="104" width="30" height="52" rx="4"/>
      <path d="M58 116 L62 114 M58 128 L62 126 M58 140 L62 138" stroke-width="1.5"/>
      <!-- zombie arms -->
      <path d="M78 112 H124 M76 120 H120"/>
      <path d="M124 112 l5 -3 M124 112 l6 0 M124 112 l5 3 M120 120 l5 -2 M120 120 l5 2" stroke-width="1.8"/>
    </g>
  </g>
</svg>'''
open(sys.argv[1], "w").write(svg)
