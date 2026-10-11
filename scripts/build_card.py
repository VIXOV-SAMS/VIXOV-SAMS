"""Build the neofetch-style profile cards (dark_mode.svg / light_mode.svg).

Usage: python3 scripts/build_card.py path/to/photo
"""
import sys
from html import escape
from ascii import to_ascii

THEMES = {
    "dark_mode.svg": dict(bg="#161b22", border="#30363d", text="#c9d1d9", key="#ffa657",
                          val="#a5d6ff", art="#c9d1d9", dim="#616e7f", accent="#7ee787", invert=False),
    "light_mode.svg": dict(bg="#f6f8fa", border="#d0d7de", text="#24292f", key="#953800",
                           val="#0a3069", art="#24292f", dim="#c2cfde", accent="#116329", invert=True),
}

W = 56  # width of the info column in characters

# (key, value) rows; None = blank line; ("#", title) = section header
INFO = [
    ("#", "ibrahim@VIXOV-SAMS"),
    ("Host", "Midway High School, Midway ISD"),
    ("Location", "Waco, Texas, USA"),
    ("Grade", "12th (Senior)"),
    ("Uptime", "Always learning..."),
    ("Kernel", "Offensive Security"),
    None,
    ("Role.Current", "Penetration Tester"),
    ("Role.Bounty", "Bug Bounty Hunter"),
    ("Role.Team", "Purple Teaming"),
    ("Mission", "Attack -> Report -> Fix -> Harden"),
    None,
    ("Languages.Code", "Python, JavaScript"),
    ("Languages.Web", "HTML, CSS"),
    None,
    ("Focus.Web", "Web App Security, OWASP Top 10"),
    ("Focus.Network", "Recon, Network Pentesting"),
    ("Focus.Defense", "Detection, Hardening, Remediation"),
    ("Tools.Dev", "Git, VS Code"),
    None,
    ("#", "Contact"),
    ("GitHub", "VIXOV-SAMS"),
    ("LinkedIn", "Ibrahim Samsudeen"),
    None,
    ("#", "Motto"),
    ("Quote", "\"Break it so nobody else can.\""),
]


def info_line(row, t):
    if row is None:
        return ""
    k, v = row
    if k == "#":
        dashes = "-" * (W - len(v) - 3)
        return (f'<tspan fill="{t["accent"]}">{escape(v)}</tspan> '
                f'<tspan fill="{t["dim"]}">{dashes}</tspan>')
    dots = " " + "." * max(2, W - len(k) - len(v) - 4) + " "
    return (f'<tspan fill="{t["key"]}">{escape(k)}</tspan>:'
            f'<tspan fill="{t["dim"]}">{dots}</tspan>'
            f'<tspan fill="{t["val"]}">{escape(v)}</tspan>')


def build(photo):
    for name, t in THEMES.items():
        art = to_ascii(photo, cols=53, rows=27, box=(225, 150, 640, 640))
        rows = max(len(art), len(INFO))
        lh, top = 20, 30
        height = top + rows * lh + 10
        out = [
            f'<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,\'Courier New\',monospace" '
            f'width="1040px" height="{height}px" font-size="16px">',
            '<style>@font-face{font-family:ConsolasFallback;src:local(\'Consolas\');size-adjust:109%}'
            'text,tspan{white-space:pre}</style>',
            f'<rect width="1040px" height="{height}px" fill="{t["bg"]}" rx="15" stroke="{t["border"]}"/>',
            f'<text x="15" y="{top}" fill="{t["art"]}" font-size="14px">',
        ]
        for i, line in enumerate(art):
            out.append(f'<tspan x="15" y="{top + i * lh}">{escape(line)}</tspan>')
        out.append("</text>")
        out.append(f'<text x="480" y="{top}" fill="{t["text"]}">')
        for i, row in enumerate(INFO):
            out.append(f'<tspan x="480" y="{top + i * lh}">{info_line(row, t)}</tspan>')
        out.append("</text></svg>")
        with open(name, "w") as f:
            f.write("\n".join(out) + "\n")
        print("wrote", name)


if __name__ == "__main__":
    build(sys.argv[1])
