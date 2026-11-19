# -*- coding: utf-8 -*-
"""Erzeugt alle HTML-Seiten der Website. Aufruf:  python _build/build.py
Texte und Seiten stehen unten in diesem Skript; Kopf- und Fusszeile werden nur hier gepflegt."""
import json, os, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOMAIN = "https://www.gartenservice-jaszewski.de"

FIRMA = "Jaszewski Garten- & Landschaftsbau"
INHABER = "Mariusz Jaszewski"
STR, PLZ, ORT = "Schöninger Straße 17", "38173", "Sickte"
TEL1, TEL1_L = "0176 52046681", "+4917652046681"
TEL2, TEL2_L = "0152 55343799", "+4915255343799"
WA = "4917652046681"
MAIL = "gartenservice-jaszewski@gmx.de"
MAPS = "https://www.google.com/maps/dir/?api=1&destination=Sch%C3%B6ninger+Stra%C3%9Fe+17%2C+38173+Sickte"

ORTE = ["Sickte", "Braunschweig", "Wolfenbüttel", "Cremlingen", "Königslutter am Elm", "Schöppenstedt",
        "Veltheim (Ohe)", "Erkerode", "Evessen", "Dettum", "Destedt", "Weddel"]
ORT_LINKS = {"Braunschweig": "gartenbau-braunschweig.html", "Wolfenbüttel": "gartenbau-wolfenbuettel.html"}

IMG = {  # Dateiname: (Breite, Hoehe)
    "pool-terrasse-plattenbelag": (878, 673), "hauseingang-rampe-treppe-palisaden": (650, 487),
    "terrasse-grossformatplatten": (1440, 972), "einfahrt-pflaster-carport": (655, 582),
    "hofpflaster-wege-am-haus": (658, 493), "eingangstreppe-blockstufen": (750, 504),
    "rollrasen-terrasse-neubau": (652, 489), "gartenweg-bepflanzung": (750, 750),
    "sitzplatz-im-garten": (947, 950), "erdarbeiten-minibagger": (948, 952),
    "winterdienst-schneeraeumung": (956, 954), "team-jaszewski": (1200, 1200),
    "garten-staudenbeet-1200": (1200, 800), "heckenschnitt-1200": (1200, 800),
    
}


def pic(name, alt, sizes="100vw", lazy=True, cls=""):
    """Stimmungsbild in drei Groessen (720/1200/2000 px)."""
    l = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    ss = ", ".join(f"assets/img/{name}-{w}.webp {w}w" for w in (720, 1200, 2000))
    return f'<img src="assets/img/{name}-1200.webp" srcset="{ss}" sizes="{sizes}" alt="{esc(alt)}" width="2000" height="1333"{l}{c}>'


ICON = {
    "arrow": '<svg class="arr" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.100 2h3a2 2 0 0 1 2 1.700c.1 1 .4 1.900.7 2.800a2 2 0 0 1-.5 2.100L8.100 9.900a16 16 0 0 0 6 6l1.300-1.300a2 2 0 0 1 2.100-.4c.9.3 1.800.6 2.800.7a2 2 0 0 1 1.700 2z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10" stroke-width="1.4"/><path d="m8 12.500 2.700 2.700L16 9.500"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.600 15.100L2 22l5-1.300A10 10 0 1 0 12 2zm0 18.200a8.200 8.200 0 0 1-4.200-1.200l-.3-.2-3 .8.8-2.900-.2-.3A8.200 8.200 0 1 1 12 20.200zm4.500-6.100c-.2-.1-1.500-.7-1.700-.8-.2-.1-.4-.1-.6.1-.2.2-.6.8-.8 1-.1.2-.3.2-.5.1-.2-.1-1-.4-2-1.200-.7-.6-1.200-1.400-1.400-1.700-.1-.2 0-.4.1-.5l.4-.4c.1-.1.2-.3.2-.4.1-.2 0-.3 0-.4l-.8-1.800c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.6.3-.2.2-.8.8-.8 2s.800 2.300 1 2.400c.1.2 1.700 2.600 4.100 3.600.6.200 1 .4 1.400.5.6.2 1.100.2 1.500.1.500-.1 1.500-.6 1.700-1.200.2-.6.2-1.100.1-1.200 0-.100-.200-.200-.500-.300z"/></svg>',
    "chev": '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.600" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m2.500 4.500 3.500 3.500 3.500-3.500"/></svg>',
    "talk": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.600" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.800 7L4 20l1.100-4.600A8 8 0 1 1 21 12z"/></svg>',
    "calc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.600" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8.500 7.500h7M8.500 12h.01M12 12h.01M15.500 12h.01M8.500 16h.01M12 16h.01M15.500 16h.01"/></svg>',
    "tool": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.600" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.700 6.300a4 4 0 0 0 5 5L11 20a2.100 2.100 0 0 1-3-3l8.700-8.700zM14.700 6.300 17 4l3 3-2.300 2.300"/></svg>',
    "team": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.600" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="3.500"/><path d="M2.500 20a6.500 6.500 0 0 1 13 0M16 4.800a3.500 3.500 0 0 1 0 6.400M18 14.200a6.500 6.500 0 0 1 3.500 5.800"/></svg>',
    "bagger": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3.5 17h9a2 2 0 0 1 0 4h-9a2 2 0 0 1 0-4z"/><path d="M4 17v-4h8.5v4"/><path d="M6 13V8.5h4l1.6 4.5"/><path d="M12.5 13l4.2-8 4.3 5.5"/><path d="M21 10.500v4h-3.800l1.300-2.700"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.600" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19c0-9 5-14 15-14 0 10-5 15-14 15M5 19l7-7"/></svg>',
    "home": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.600" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3 11 9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></svg>',
}

LOGO = ('<svg viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="32" fill="#49ad4c"/>'
        '<rect x="30" y="12" width="8.500" height="8.500" rx="1" fill="#f5f0e6"/>'
        '<path d="M30 25h8.500v21.500a9.500 9.500 0 0 1-9.500 9.500h-3.500v-6.500h2.500a2 2 0 0 0 2-2z" fill="#f5f0e6"/></svg>')

LEISTUNGEN = [
    # slug, Navi-Name, Kurztext, Bild
    ("gartengestaltung", "Gartengestaltung", "Neuanlage und Umgestaltung – vom ersten Spatenstich bis zum fertigen Garten.", "garten-staudenbeet-1200"),
    ("pflasterarbeiten", "Pflasterarbeiten", "Einfahrten, Höfe und Wege, die tragen, entwässern und gut aussehen.", "hofpflaster-wege-am-haus"),
    ("terrassenbau", "Terrassen & Treppen", "Terrassen, Sitzplätze, Stufen und Eingänge aus Stein und Platten.", "terrasse-grossformatplatten"),
    ("gartenpflege", "Gartenpflege", "Regelmäßige Pflege für Privatgärten, Wohnanlagen und Gewerbeobjekte.", "heckenschnitt-1200"),
    ("zaunbau", "Zaunbau", "Zäune, Tore und Sichtschutz – sauber gesetzt und dauerhaft stabil.", "einfahrt-pflaster-carport"),
    ("winterdienst", "Winterdienst", "Räumen und Streuen – schnell, zuverlässig und sicher.", "winterdienst-schneeraeumung"),
]


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def img(name, alt, lazy=True, cls=""):
    w, h = IMG[name]
    l = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    v = "?v=2" if name in ("einfahrt-pflaster-carport", "team-jaszewski") else ""
    return f'<img src="assets/img/{name}.webp{v}" alt="{esc(alt)}" width="{w}" height="{h}"{l}{c}>'


def brand(tag="a"):
    return (f'<a class="brand" href="index.html" aria-label="{esc(FIRMA)} – Startseite">{LOGO}'
            f'<span class="brand-t"><b>Jaszewski</b><span>Garten- &amp; Landschaftsbau</span></span></a>')


def header(current):
    def cur(s):
        return ' aria-current="page"' if s == current else ""
    drop = "".join(f'<a href="{s}.html">{n}{ICON["arrow"]}</a>' for s, n, _, _ in LEISTUNGEN)
    sub = "".join(f'<a href="{s}.html">{n}</a>' for s, n, _, _ in LEISTUNGEN)
    return f'''<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<header class="top"><div class="wrap top-in">
{brand()}
<nav aria-label="Hauptnavigation"><ul class="nav">
<li class="has-drop"><a class="n" href="leistungen.html"{cur("leistungen")}>Leistungen {ICON["chev"]}</a><div class="drop">{drop}</div></li>
<li><a class="n" href="referenzen.html"{cur("referenzen")}>Referenzen</a></li>
<li><a class="n" href="ueber-uns.html"{cur("ueber-uns")}>Über uns</a></li>
<li><a class="n" href="einsatzgebiet.html"{cur("einsatzgebiet")}>Einsatzgebiet</a></li>
<li><a class="n" href="kontakt.html"{cur("kontakt")}>Kontakt</a></li>
</ul></nav>
<div class="top-cta">
<a class="btn btn-primary" href="tel:{TEL1_L}">{ICON["phone"]}{TEL1}</a>
<button class="burger" aria-label="Menü öffnen" aria-expanded="false" aria-controls="mobilmenue"><span></span><span></span></button>
</div></div></header>
<div class="mobile" id="mobilmenue">
<a class="m" href="leistungen.html">Leistungen</a><div class="sub">{sub}</div>
<a class="m" href="referenzen.html">Referenzen</a>
<a class="m" href="ueber-uns.html">Über uns</a>
<a class="m" href="einsatzgebiet.html">Einsatzgebiet</a>
<a class="m" href="kontakt.html">Kontakt</a>
<a class="btn btn-light" href="tel:{TEL1_L}">{ICON["phone"]}{TEL1} anrufen</a>
</div>'''


def footer():
    ls = "".join(f'<li><a href="{s}.html">{n}</a></li>' for s, n, _, _ in LEISTUNGEN)
    return f'''<footer class="foot"><div class="wrap">
<div class="foot-g">
<div>{brand()}<p style="margin-top:22px;max-width:34ch">Familienbetrieb für Garten- und Landschaftsbau aus Sickte. Seit 2007 gestalten, pflastern und pflegen wir Außenanlagen in der Region Braunschweig und Wolfenbüttel.</p></div>
<div><h4>Leistungen</h4><ul>{ls}</ul></div>
<div><h4>Unternehmen</h4><ul>
<li><a href="referenzen.html">Referenzen</a></li><li><a href="ueber-uns.html">Über uns</a></li>
<li><a href="einsatzgebiet.html">Einsatzgebiet</a></li>
<li><a href="gartenbau-braunschweig.html">Gartenbau Braunschweig</a></li>
<li><a href="gartenbau-wolfenbuettel.html">Gartenbau Wolfenbüttel</a></li>
<li><a href="kontakt.html">Kontakt</a></li></ul></div>
<div><h4>Kontakt</h4><ul>
<li>{STR}<br>{PLZ} {ORT}</li>
<li><a href="tel:{TEL1_L}">{TEL1}</a></li><li><a href="tel:{TEL2_L}">{TEL2}</a></li>
<li><a href="mailto:{MAIL}">{MAIL}</a></li></ul></div>
</div>
<div class="foot-b"><span>© <span id="jahr">{datetime.date.today().year}</span> {FIRMA} · Inhaber {INHABER}</span>
<nav aria-label="Rechtliches"><a href="impressum.html">Impressum</a><a href="datenschutz.html">Datenschutz</a></nav>
<span class="credit">Website von <a href="https://timokochitsolutions.de" target="_blank" rel="noopener">Timo Koch IT Solutions</a></span></div>
</div></footer>
<div class="callbar"><a class="p" href="tel:{TEL1_L}">{ICON["phone"]}Anrufen</a><a href="https://wa.me/{WA}" target="_blank" rel="noopener">{ICON["wa"]}WhatsApp</a><a href="kontakt.html">{ICON["mail"]}Anfrage</a></div>
<div class="fab"><a class="btn btn-primary" href="kontakt.html">Angebot anfragen{ICON["arrow"]}</a></div>
<script src="assets/js/main.js?v=4" defer></script>'''


def business_schema():
    return {
        "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "@id": DOMAIN + "/#firma",
        "name": FIRMA, "alternateName": "Gartenservice Jaszewski", "url": DOMAIN + "/",
        "image": DOMAIN + "/assets/img/og.jpg", "telephone": TEL1_L, "email": MAIL,
        "foundingDate": "2007", "founder": {"@type": "Person", "name": INHABER},
        "address": {"@type": "PostalAddress", "streetAddress": STR, "postalCode": PLZ,
                    "addressLocality": ORT, "addressRegion": "Niedersachsen", "addressCountry": "DE"},
        "areaServed": [{"@type": "City", "name": o} for o in ORTE],
        "knowsAbout": ["Gartengestaltung", "Pflasterarbeiten", "Terrassenbau", "Gartenpflege", "Zaunbau", "Winterdienst"],
    }


def crumbs_schema(trail):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": DOMAIN + "/" + ("" if u == "index.html" else u)}
        for i, (n, u) in enumerate(trail)]}


def faq_schema(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def page(slug, title, desc, body, current="", schemas=None, noindex=False, dark_top=False, extra_head="", base=""):
    url = DOMAIN + "/" + ("" if slug == "index" else slug + ".html")
    sch = [business_schema()] + (schemas or [])
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in sch)
    robots = '<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow">'
    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="{esc(FIRMA)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/assets/img/og.jpg">
<meta name="theme-color" content="#1c3527">
<meta name="format-detection" content="telephone=no">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/serif.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
{base}{extra_head}<link rel="stylesheet" href="assets/css/style.css?v=14">
<script>document.documentElement.classList.add('js')</script>
{ld}
</head>
<body{' class="dark-top"' if dark_top else ""}>
{header(current)}
<main id="inhalt">
{body}
</main>
{footer()}
</body>
</html>
'''
    with open(os.path.join(ROOT, slug + ".html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    return slug, noindex


# ---------- Bausteine ----------

def eyebrow(t):
    return f'<span class="eyebrow">{t}</span>'


def checks(items, two=False):
    c = "checks two" if two else "checks"
    return f'<ul class="{c}">' + "".join(f"<li>{ICON['check']}<span>{i}</span></li>" for i in items) + "</ul>"


def faq_block(items, title="Häufige Fragen", ey="Gut zu wissen"):
    d = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)
    return f'''<section class="sec"><div class="wrap">
<div class="center rv" style="margin-bottom:clamp(36px,5vw,60px)">{eyebrow(ey)}<h2>{title}</h2></div>
<div class="faq rv">{d}</div></div></section>'''


def crumbs(trail):
    out = []
    for i, (n, u) in enumerate(trail):
        out.append(f'<a href="{u}">{n}</a>' if i < len(trail) - 1 else f"<b>{n}</b>")
    return '<nav class="crumbs" aria-label="Brotkrumen">' + "<span>/</span>".join(out) + "</nav>"


def steps():
    s = [("Anfrage", "Sie rufen an, schreiben per WhatsApp oder nutzen das Formular. Ein paar Sätze zu Ihrem Vorhaben genügen."),
         ("Termin vor Ort", "Wir schauen uns Grundstück und Gegebenheiten gemeinsam an und besprechen Ihre Wünsche in Ruhe."),
         ("Angebot", "Sie erhalten eine individuelle Kalkulation für Ihr Vorhaben – nachvollziehbar und ohne Überraschungen."),
         ("Ausführung", "Wir setzen das Projekt mit eigenem Team und eigenen Maschinen um und bleiben dabei Ihr Ansprechpartner.")]
    li = "".join(f'<li class="rv" style="--d:{i*.08:.2f}s"><span class="n">0{i+1}</span><h3>{t}</h3><p>{p}</p></li>' for i, (t, p) in enumerate(s))
    return f'''<section class="sec dark"><div class="wrap">
<div class="head"><div class="rv">{eyebrow("So läuft es ab")}<h2>In vier Schritten zu <em>Ihrer neuen Außenanlage</em></h2></div>
<p class="lead rv">Offene Kommunikation gehört für uns dazu: Sie wissen vor, während und nach dem Projekt, woran Sie sind.</p></div>
<ol class="steps" style="list-style:none;margin:0;padding:0">{li}</ol></div></section>'''


def contact(preselect="", light=False, h="Erzählen Sie uns von <em>Ihrem Vorhaben</em>", id_="anfrage"):
    opts = ["Gartengestaltung / Neuanlage", "Pflasterarbeiten", "Terrasse / Treppe", "Gartenpflege", "Zaunbau", "Winterdienst", "Sonstiges"]
    o = '<option value="">Bitte wählen</option>' + "".join(
        f'<option{" selected" if x == preselect else ""}>{x}</option>' for x in opts)
    cls = "sec light" if light else "sec dark"
    return f'''<section class="{cls}" id="{id_}"><div class="wrap contact">
<div class="rv">{eyebrow("Kontakt")}<h2>{h}</h2>
<p class="lead">Am schnellsten geht es per Telefon oder WhatsApp. Wir melden uns zurück, vereinbaren einen Termin bei Ihnen vor Ort und erstellen Ihnen ein individuelles Angebot.</p>
<div class="c-list">
<a href="tel:{TEL1_L}"><span class="ic">{ICON["phone"]}</span><span><small>Telefon</small><b>{TEL1}</b></span></a>
<a href="tel:{TEL2_L}"><span class="ic">{ICON["phone"]}</span><span><small>Mobil</small><b>{TEL2}</b></span></a>
<a href="mailto:{MAIL}"><span class="ic">{ICON["mail"]}</span><span><small>E-Mail</small><b style="font-size:1.05rem;word-break:break-all">{MAIL}</b></span></a>
<a href="{MAPS}" target="_blank" rel="noopener"><span class="ic">{ICON["pin"]}</span><span><small>Adresse</small><b>{STR}, {PLZ} {ORT}</b></span></a>
</div></div>
<form class="form anfrage rv" data-wa="{WA}" data-mail="{MAIL}" novalidate>
<h3>Anfrage in einer Minute</h3>
<p>Füllen Sie kurz aus, worum es geht – wir melden uns bei Ihnen.</p>
<div class="fg">
<div class="f"><label for="{id_}-name">Name *</label><input id="{id_}-name" name="name" autocomplete="name" required></div>
<div class="f"><label for="{id_}-tel">Telefon *</label><input id="{id_}-tel" name="telefon" type="tel" autocomplete="tel" required></div>
<div class="f"><label for="{id_}-ort">Ort</label><input id="{id_}-ort" name="ort" autocomplete="address-level2" placeholder="z. B. Sickte"></div>
<div class="f"><label for="{id_}-l">Leistung</label><select id="{id_}-l" name="leistung">{o}</select></div>
<div class="f full"><label for="{id_}-n">Ihr Vorhaben</label><textarea id="{id_}-n" name="nachricht" placeholder="Was möchten Sie umsetzen? Ungefähre Fläche, Wunschtermin …"></textarea></div>
</div>
<p class="err" role="alert">Bitte tragen Sie Name und Telefonnummer ein.</p>
<div class="form-btns">
<button type="button" class="btn btn-wa" data-send="wa">{ICON["wa"]}Per WhatsApp senden</button>
<button type="button" class="btn btn-primary" data-send="mail">{ICON["mail"]}Per E-Mail senden</button>
</div>
<small class="hint">Beim Absenden öffnet sich WhatsApp bzw. Ihr E-Mail-Programm mit der fertigen Nachricht. Auf dieser Website werden dabei keine Daten gespeichert. Mehr dazu in der <a href="datenschutz.html">Datenschutzerklärung</a>.</small>
</form></div></section>'''


def band(h="Lassen Sie uns über Ihren Garten sprechen", p="Ein Anruf genügt – wir kommen zu Ihnen und schauen uns alles vor Ort an."):
    return f'''<section class="sec-tight"><div class="wrap"><div class="band rv">
<div><h2>{h}</h2><p>{p}</p></div>
<div class="cta-row"><a class="btn btn-primary" href="tel:{TEL1_L}">{ICON["phone"]}{TEL1}</a><a class="btn btn-ghost" href="kontakt.html">Anfrage senden{ICON["arrow"]}</a></div>
</div></div></section>'''


def svc_cards(skip=None):
    out = []
    for i, (s, n, t, im) in enumerate(LEISTUNGEN):
        if s == skip:
            continue
        out.append(f'<a class="svc-c rv" style="--d:{(i%3)*.08:.2f}s" href="{s}.html">{img(im, n + " – " + FIRMA)}'
                   f'<span class="no">0{i+1}</span><span class="go">{ICON["arrow"]}</span><h3>{n}</h3><p>{t}</p></a>')
    return '<div class="svc">' + "".join(out) + "</div>"


def areas(dark=False):
    li = "".join(f'<li><a href="{ORT_LINKS[o]}">{o}</a></li>' if o in ORT_LINKS else f"<li>{o}</li>" for o in ORTE)
    return f'<ul class="areas">{li}</ul>'


GAL = [
    ("terrasse-grossformatplatten", "Erhöhte Terrasse mit Großformatplatten", "w"),
    ("einfahrt-pflaster-carport", "Gepflasterte Einfahrt mit Carport-Zufahrt", ""),
    ("pool-terrasse-plattenbelag", "Poolumrandung mit Plattenbelag", "h"),
    ("eingangstreppe-blockstufen", "Eingangstreppe aus Blockstufen", "h"),
    ("hofpflaster-wege-am-haus", "Hof- und Wegepflaster am Haus", ""),
    ("rollrasen-terrasse-neubau", "Rollrasen und Terrasse am Neubau", ""),
    ("hauseingang-rampe-treppe-palisaden", "Hauseingang mit Rampe und Stufen", ""),
]


def gallery(n=None):
    items = GAL[:n] if n else GAL
    return '<div class="gal">' + "".join(
        f'<figure class="{c} rv"><a class="lb" href="assets/img/{i}.webp{"?v=2" if i == "einfahrt-pflaster-carport" else ""}" data-cap="{esc(t)}" aria-label="{esc(t)} vergrößern">{img(i, t + " – Referenz von " + FIRMA)}</a><figcaption><span>{t}</span></figcaption></figure>'
        for i, t, c in items) + "</div>"


# ---------- Startseite ----------

HOME_FAQ = [
    ("In welchen Orten sind Sie tätig?", "Unser Betrieb sitzt in Sickte. Von hier aus arbeiten wir in Braunschweig, Wolfenbüttel, Cremlingen, Königslutter, Schöppenstedt und den umliegenden Orten. Liegt Ihr Grundstück etwas weiter entfernt, fragen Sie einfach an."),
    ("Wie komme ich zu einem Angebot?", "Sie melden sich telefonisch, per WhatsApp oder über das Formular. Wir vereinbaren einen Termin bei Ihnen vor Ort, schauen uns das Vorhaben an und kalkulieren individuell – bevor irgendwelche Arbeiten beginnen."),
    ("Übernehmen Sie auch einzelne, kleinere Arbeiten?", "Ja. Wir bauen komplette Außenanlagen, aber genauso eine einzelne Eingangstreppe, eine neue Einfahrt oder einen Zaun. Sprechen Sie uns auf Ihr Vorhaben an."),
    ("Kann ich die Pflege nach der Neuanlage ebenfalls bei Ihnen beauftragen?", "Gern. Unser Pflegeservice betreut Gärten und Grünanlagen auch dauerhaft, damit die Anlage so schön bleibt, wie sie übergeben wurde."),
    ("Bieten Sie auch Winterdienst an?", "Ja, wir räumen und streuen in der kalten Jahreszeit – für Privatgrundstücke ebenso wie für Wohnanlagen und Gewerbeflächen."),
]

seal = ('<div class="seal" aria-hidden="true"><svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="60" fill="#1c3527"/>'
        '<defs><path id="k" d="M60 60m-44 0a44 44 0 1 1 88 0a44 44 0 1 1-88 0"/></defs>'
        '<text font-family="Manrope,sans-serif" font-size="8.400" font-weight="700" fill="#f5f0e6" textLength="270" lengthAdjust="spacing">'
        '<textPath href="#k" textLength="270" lengthAdjust="spacing">FAMILIENBETRIEB · SEIT 2007 · AUS SICKTE · </textPath></text></svg><i>J</i></div>')

marq_items = ["Gartengestaltung", "Pflasterarbeiten", "Terrassenbau", "Treppen & Eingänge", "Zaunbau", "Rollrasen", "Grünanlagenpflege", "Winterdienst"]
marq = "".join(f"<span>{m}</span>" for m in marq_items) * 2

home = f'''
<section class="hero2">
{pic("pflasterkreis-mauer-hecken", "Gepflasterter Platz mit Natursteinmauer, Palisaden und geschnittenen Hecken", lazy=False, cls="hero2-bg")}
<div class="wrap hero2-in">
<div class="hero2-txt">
{eyebrow("Familienbetrieb aus Sickte · seit 2007")}
<h1><span>Garten- &amp;</span> <span>Landschafts&shy;bau,</span> <span><em>der bleibt.</em></span></h1>
<p class="lead">Wir gestalten Gärten, pflastern Einfahrten und bauen Terrassen, Treppen und Zäune – in Sickte, Braunschweig, Wolfenbüttel und der ganzen Umgebung. Persönlich beraten, sauber ausgeführt.</p>
<div class="cta-row">
<a class="btn btn-light" href="#anfrage">Angebot anfragen{ICON["arrow"]}</a>
<a class="btn btn-outline-light" href="tel:{TEL1_L}">{ICON["phone"]}{TEL1}</a>
</div>
</div>
</div>
<div class="wrap"><ul class="hero2-facts">
<li><b>Seit 2007</b><span>Erfahrung im Garten- und Landschaftsbau</span></li>
<li><b>Vor Ort</b><span>Persönliche Beratung bei Ihnen</span></li>
<li><b>Aus einer Hand</b><span>Planung, Bau und Pflege</span></li>
</ul></div>
</section>

<div class="marq" aria-hidden="true"><div class="marq-t">{marq}</div></div>

<section class="sec"><div class="wrap">
<div class="head"><div class="rv">{eyebrow("Unsere Leistungen")}<h2>Alles für Ihre Außenanlage – <em>aus einer Hand</em></h2></div>
<p class="lead rv">Von der Neuanlage bis zur laufenden Pflege: Sie haben einen Ansprechpartner für das gesamte Grundstück.</p></div>
{svc_cards()}
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap split">
<div class="split-img rv"><div class="frame sq">{img("team-jaszewski", "Das Team von " + FIRMA + " vor dem Firmenbanner")}</div>
<div class="note"><b>2007</b>Seitdem als Familienbetrieb im Garten- und Landschaftsbau tätig.</div></div>
<div class="rv">{eyebrow("Über uns")}<h2>Ein Familienbetrieb, der <em>zu seinem Wort steht</em></h2>
<p class="lead">Seit 2007 legen wir Gärten neu an, gestalten Hausgärten um und pflegen Grünanlagen. Qualität und ein gutes Miteinander im Team sind uns dabei genauso wichtig wie ein fairer Preis.</p>
{checks(["Persönliche Beratung bei Ihnen vor Ort", "Individuelle Kalkulation für Ihr Vorhaben", "Eigene Maschinen und fachgerechte Ausrüstung", "Betreuung auch nach der Fertigstellung"])}
<a class="link" href="ueber-uns.html">Mehr über uns{ICON["arrow"]}</a></div>
</div></section>

{steps()}

<section class="sec"><div class="wrap">
<div class="head"><div class="rv">{eyebrow("Referenzen")}<h2>Arbeiten, die <em>für sich sprechen</em></h2></div>
<div class="rv"><p class="lead" style="margin-bottom:20px">Ein Auszug aus Projekten, die wir für unsere Kunden umgesetzt haben.</p><a class="link" href="referenzen.html">Alle Referenzen ansehen{ICON["arrow"]}</a></div></div>
{gallery(5)}
</div></section>

<section class="quote">
{pic("garten-terrasse-rasen", "Hausgarten mit Rasen, Staudenbeet und heller Plattenterrasse mit Sitzgruppe", cls="quote-bg")}
<div class="wrap rv">{eyebrow("Unser Anspruch")}
<p class="q">Der einfachste Weg, seinen Garten <em>zu lieben.</em></p>
<p class="lead">Sie sagen uns, wie Sie draußen leben möchten. Wir kümmern uns um alles andere – von der ersten Idee bis zur laufenden Pflege.</p>
<div class="cta-row"><a class="btn btn-light" href="#anfrage">Vorhaben besprechen{ICON["arrow"]}</a><a class="btn btn-outline-light" href="leistungen.html">Leistungen ansehen</a></div>
</div></section>

<section class="sec"><div class="wrap">
<div class="center rv" style="margin-bottom:clamp(36px,5vw,60px)">{eyebrow("Darauf können Sie sich verlassen")}<h2>Warum Kunden sich für <em>Jaszewski</em> entscheiden</h2></div>
<ul class="feat">
<li class="rv"><div class="ic">{ICON["talk"]}</div><h3>Beratung vor Ort</h3><p>Wir kommen zu Ihnen, hören zu und entwickeln die Lösung gemeinsam mit Ihnen am Grundstück.</p></li>
<li class="rv" style="--d:.08s"><div class="ic">{ICON["calc"]}</div><h3>Individuelle Kalkulation</h3><p>Sie erhalten ein Angebot, das zu Ihrem Vorhaben passt – verständlich aufgeschlüsselt.</p></li>
<li class="rv" style="--d:.16s"><div class="ic">{ICON["team"]}</div><h3>Erfahrenes Team</h3><p>Eingespielte Leute mit Kompetenz, die seit vielen Jahren zusammen auf der Baustelle stehen.</p></li>
<li class="rv"><div class="ic">{ICON["bagger"]}</div><h3>Eigene Maschinen</h3><p>Fachgerechte Ausrüstung im eigenen Haus – das spart Zeit und hält die Kosten im Rahmen.</p></li>
<li class="rv" style="--d:.08s"><div class="ic">{ICON["leaf"]}</div><h3>Pflegeservice</h3><p>Auf Wunsch betreuen wir Ihre Anlage dauerhaft, damit sie auch in Jahren noch Freude macht.</p></li>
<li class="rv" style="--d:.16s"><div class="ic">{ICON["home"]}</div><h3>Faires Preis-Leistungs-Verhältnis</h3><p>Saubere Arbeit zu einem Preis, der in einem gesunden Verhältnis zur Leistung steht.</p></li>
</ul></div></section>

<section class="sec" style="padding-top:0"><div class="wrap split rev">
<div class="split-img rv"><div class="frame wide">{img("rollrasen-terrasse-neubau", "Neu angelegter Rollrasen mit Terrasse an einem Neubau")}</div></div>
<div class="rv">{eyebrow("Einsatzgebiet")}<h2>Zuhause in Sickte, unterwegs <em>in der ganzen Region</em></h2>
<p class="lead">Kurze Wege zu Ihnen: Von Sickte aus sind wir schnell in Braunschweig, Wolfenbüttel und den Orten rund um den Elm.</p>
{areas()}
<p style="margin-top:28px"><a class="link" href="einsatzgebiet.html">Zum Einsatzgebiet{ICON["arrow"]}</a></p></div>
</div></section>

{faq_block(HOME_FAQ)}
{contact()}
'''

PAGES = []
PAGES.append(page("index", "Garten- und Landschaftsbau Sickte | Jaszewski – seit 2007",
     "Garten- und Landschaftsbau Jaszewski aus Sickte: Gartengestaltung, Pflaster, Terrassen, Zaunbau und Pflege für Braunschweig und Wolfenbüttel. Jetzt anfragen.",
     home, dark_top=True,
     extra_head='<link rel="preload" as="image" href="assets/img/pflasterkreis-mauer-hecken-1200.webp" imagesrcset="assets/img/pflasterkreis-mauer-hecken-720.webp 720w, assets/img/pflasterkreis-mauer-hecken-1200.webp 1200w, assets/img/pflasterkreis-mauer-hecken-2000.webp 2000w" imagesizes="100vw" fetchpriority="high">\n',
     schemas=[faq_schema(HOME_FAQ), {"@context": "https://schema.org", "@type": "WebSite", "name": FIRMA, "url": DOMAIN + "/"}]))


# ---------- Leistungsseiten ----------

def service(slug, h1, title, desc, lead, hero_img, hero_alt, intro_h, intro, list_h, items, img2, img2_alt, sec_h, sec_p, sec_checks, faq, preselect):
    name = next(n for s, n, _, _ in LEISTUNGEN if s == slug)
    trail = [("Start", "index.html"), ("Leistungen", "leistungen.html"), (name, slug + ".html")]
    rel = "".join(f'<a href="{s}.html">{n}{ICON["arrow"]}</a>' for s, n, _, _ in LEISTUNGEN if s != slug)
    body = f'''
<section class="phero"><div class="wrap phero-g">
<div>{crumbs(trail)}{eyebrow("Leistung")}
<h1>{h1}</h1><p class="lead">{lead}</p>
<div class="cta-row"><a class="btn btn-primary" href="#anfrage">Angebot anfragen{ICON["arrow"]}</a><a class="btn btn-ghost" href="tel:{TEL1_L}">{ICON["phone"]}{TEL1}</a></div></div>
<div class="phero-img">{img(hero_img, hero_alt, lazy=False)}</div>
</div></section>

<section class="sec" style="padding-top:clamp(40px,6vw,80px)"><div class="wrap cols">
<div class="rv"><h2>{intro_h}</h2>{"".join(f"<p>{p}</p>" for p in intro)}</div>
<div class="rv"><h3 style="margin-bottom:6px">{list_h}</h3>{checks(items)}</div>
</div></section>

<section class="sec" style="padding-top:0"><div class="wrap split rev">
<div class="split-img rv"><div class="frame wide">{img(img2, img2_alt)}</div></div>
<div class="rv">{eyebrow("Unsere Arbeitsweise")}<h2>{sec_h}</h2><p class="lead">{sec_p}</p>{checks(sec_checks)}
<a class="link" href="referenzen.html">Referenzen ansehen{ICON["arrow"]}</a></div>
</div></section>

{steps()}
{faq_block(faq, title="Fragen zu " + name)}

<section class="sec" style="padding-top:0"><div class="wrap">
<div class="rv" style="margin-bottom:34px">{eyebrow("Weitere Leistungen")}<h2 style="font-size:clamp(1.7rem,3vw,2.5rem)">Das übernehmen wir <em>ebenfalls</em></h2></div>
<div class="rel rv">{rel}</div></div></section>
{contact(preselect)}
'''
    sch = [crumbs_schema(trail), faq_schema(faq), {
        "@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": name,
        "description": desc, "provider": {"@id": DOMAIN + "/#firma"},
        "areaServed": [{"@type": "City", "name": o} for o in ORTE], "url": DOMAIN + "/" + slug + ".html"}]
    PAGES.append(page(slug, title, desc, body, current="leistungen", schemas=sch))


service("gartengestaltung",
    "Gartengestaltung &amp; <em>Neuanlage</em>",
    "Gartengestaltung & Neuanlage in Sickte, Braunschweig | Jaszewski",
    "Garten neu anlegen oder umgestalten: Jaszewski Garten- & Landschaftsbau aus Sickte plant und baut Ihren Garten – Rasen, Pflanzung, Wege, Sitzplätze. Beratung vor Ort.",
    "Ob Neubaugrundstück oder ein Garten, der in die Jahre gekommen ist: Wir machen daraus einen Ort, an dem Sie gern draußen sind – geplant mit Ihnen, gebaut von uns.",
    "garten-staudenbeet-1200", "Angelegter Garten mit Rasenfläche und Staudenbeet",
    "Von Grund auf neu – oder <em>endlich anders</em>",
    ["Ein Garten soll zu den Menschen passen, die ihn nutzen. Deshalb beginnt jede Gartengestaltung bei uns mit einem Gespräch auf Ihrem Grundstück: Wie wird der Garten genutzt, wo steht die Sonne, was soll bleiben, was darf weg?",
     "Bei einer Neuanlage übernehmen wir alle Schritte – Erdarbeiten und Geländemodellierung, Wege und Sitzplätze, Rasen und Bepflanzung. Bei einer Umgestaltung arbeiten wir mit dem, was da ist, und setzen gezielt neue Akzente.",
     "Weil Planung, Bau und spätere Pflege bei uns in einer Hand liegen, greift alles ineinander. Sie haben einen Ansprechpartner und müssen keine Gewerke koordinieren."],
    "Das gehört dazu",
    ["Neuanlage von Hausgärten und Vorgärten", "Umgestaltung bestehender Gärten", "Erdarbeiten und Geländemodellierung", "Rasen: Rollrasen und Ansaat",
     "Pflanzungen, Hecken und Beete", "Wege, Sitzplätze und Einfassungen", "Rückbau und Entsorgung alter Anlagen"],
    "erdarbeiten-minibagger", "Erdarbeiten mit dem Minibagger bei einer Garten-Neuanlage",
    "Mit eigenen Maschinen <em>zügig ans Ziel</em>",
    "Unsere Maschinen und Geräte stehen bei uns auf dem Hof. Das macht uns flexibel in der Planung und hält die Bauzeit kurz.",
    ["Gemeinsame Planung statt Lösungen von der Stange", "Individuelle Kalkulation vor Baubeginn", "Auf Wunsch anschließend Pflege durch unser Team"],
    [("Was kostet eine Gartengestaltung?", "Das hängt von Größe, Zustand und Ihren Wünschen ab. Wir schauen uns das Grundstück an und kalkulieren Ihr Vorhaben individuell – so wissen Sie vor Beginn, womit Sie rechnen können."),
     ("Wann ist die beste Zeit für eine Neuanlage?", "Erd- und Pflasterarbeiten sind fast ganzjährig möglich, solange der Boden nicht gefroren ist. Für Pflanzungen und Rasen eignen sich Frühjahr und Herbst besonders gut. Wer früh anfragt, kann den Wunschtermin besser treffen."),
     ("Rollrasen oder Rasensaat – was empfehlen Sie?", "Rollrasen ist nach wenigen Wochen belastbar und sieht sofort fertig aus. Eine Ansaat ist günstiger, braucht aber mehr Zeit und Pflege. Wir beraten Sie, was zu Ihrem Garten passt."),
     ("Kann ich Teile meines alten Gartens behalten?", "Ja. Bei einer Umgestaltung binden wir vorhandene Bäume, Hecken oder Wege gern ein, wenn sie in das neue Konzept passen.")],
    "Gartengestaltung / Neuanlage")

service("pflasterarbeiten",
    "Pflasterarbeiten für <em>Einfahrt, Hof und Wege</em>",
    "Pflasterarbeiten Sickte, Braunschweig, Wolfenbüttel | Jaszewski",
    "Einfahrt pflastern, Hof oder Gartenweg neu anlegen: Pflasterarbeiten vom Fachbetrieb Jaszewski aus Sickte – tragfähiger Unterbau, saubere Fugen. Jetzt Angebot anfragen.",
    "Eine gepflasterte Fläche hält Jahrzehnte – wenn der Unterbau stimmt. Wir pflastern Einfahrten, Höfe, Stellplätze und Wege fachgerecht vom Aushub bis zur letzten Fuge.",
    "hofpflaster-wege-am-haus", "Neu gepflasterte Hoffläche und Wege an einem Wohnhaus",
    "Pflaster, das <em>liegen bleibt</em>",
    ["Die Einfahrt ist die Visitenkarte eines Hauses und muss täglich einiges aushalten. Entscheidend ist, was man später nicht mehr sieht: ein ausreichend starker, verdichteter Unterbau und ein Gefälle, das Regenwasser zuverlässig ableitet.",
     "Wir übernehmen den kompletten Aufbau – Aushub, Tragschicht, Randeinfassung, Verlegung und Verfugung. Ob Betonstein, Naturstein oder Rasengitter für versickerungsfähige Flächen: Sie wählen die Optik, wir sorgen für die Technik.",
     "Auch alte, abgesackte oder vermooste Flächen nehmen wir auf und bauen sie neu auf."],
    "Typische Pflasterarbeiten",
    ["Einfahrten und Zufahrten", "Hofflächen und Stellplätze", "Garten- und Hauszuwege", "Carport- und Garagenvorplätze",
     "Randsteine, Einfassungen und Entwässerungsrinnen", "Rasengitter und versickerungsfähige Beläge", "Sanierung abgesackter Pflasterflächen"],
    "einfahrt-pflaster-carport", "Gepflasterte Einfahrt mit Zufahrt zum Carport",
    "Sauber gearbeitet – <em>vom Unterbau bis zur Fuge</em>",
    "Gerade Linien, gleichmäßige Fugen und Anschlüsse, die passen: Bei Pflaster zeigt sich Sorgfalt im Detail.",
    ["Unterbau passend zur Belastung der Fläche", "Gefälle und Entwässerung von Anfang an mitgedacht", "Saubere Anschlüsse an Haus, Garage und Straße"],
    [("Was kostet es, eine Einfahrt pflastern zu lassen?", "Der Preis richtet sich nach Fläche, Untergrund, Material und dem nötigen Unterbau. Nach einem Termin vor Ort erhalten Sie eine individuelle Kalkulation für Ihr Vorhaben."),
     ("Wie lange dauern Pflasterarbeiten?", "Eine übliche Einfahrt ist meist in wenigen Arbeitstagen fertig. Größe, Unterbau und Wetter spielen eine Rolle – einen realistischen Zeitrahmen nennen wir Ihnen mit dem Angebot."),
     ("Welches Pflaster eignet sich für die Einfahrt?", "Für befahrene Flächen empfehlen wir ausreichend starke Steine und einen Verband, der Kräfte gut verteilt. Welche Formate und Farben infrage kommen, besprechen wir gern mit Mustern vor Ort."),
     ("Entfernen Sie auch das alte Pflaster?", "Ja. Aufnehmen, Abfahren und Entsorgen des alten Belags gehören auf Wunsch zum Auftrag.")],
    "Pflasterarbeiten")

service("terrassenbau",
    "Terrassen, Treppen &amp; <em>Eingänge</em>",
    "Terrassenbau & Treppen in Sickte, Braunschweig | Jaszewski",
    "Terrasse bauen lassen, Eingangstreppe erneuern oder Poolumrandung anlegen: Jaszewski Garten- & Landschaftsbau aus Sickte baut mit Platten, Blockstufen und Naturstein.",
    "Die Terrasse ist das Wohnzimmer im Freien. Wir bauen Terrassen, Sitzplätze, Stufenanlagen und Hauseingänge, die gut aussehen und lange halten.",
    "terrasse-grossformatplatten", "Erhöhte Terrasse mit großformatigen Platten und Stufen",
    "Draußen sitzen, <em>ohne Kompromisse</em>",
    ["Großformatige Platten, klare Kanten, ein Belag ohne Stolperstellen: Eine gut gebaute Terrasse erkennt man auf den ersten Blick. Damit sie auch nach vielen Wintern noch eben liegt, bauen wir auf einem tragfähigen, frostsicheren Unterbau.",
     "Höhenunterschiede lösen wir mit Blockstufen, Palisaden oder Mauern. So entstehen aus Hanglagen und hohen Hauseingängen bequeme, sichere Zugänge – auf Wunsch auch als Rampe.",
     "Auch besondere Aufgaben wie die Umrandung eines Pools oder der Belag unter einer Terrassenüberdachung gehören zu unserem Alltag."],
    "Das bauen wir für Sie",
    ["Terrassen aus Keramik-, Beton- und Natursteinplatten", "Sitzplätze im Garten", "Eingangstreppen und Blockstufen", "Rampen und barrierearme Zugänge",
     "Poolumrandungen", "Palisaden, Stützmauern und Einfassungen", "Erneuerung alter Terrassenbeläge"],
    "eingangstreppe-blockstufen", "Neue Eingangstreppe aus hellen Blockstufen",
    "Stufen und Eingänge, <em>die einladen</em>",
    "Der Hauseingang wird jeden Tag benutzt. Entsprechend genau arbeiten wir bei Stufenhöhen, Auftritten und Anschlüssen.",
    ["Gleichmäßige Stufen für sicheres Gehen", "Materialien passend zu Haus und Pflaster", "Saubere Anschlüsse an Tür, Sockel und Fläche"],
    [("Welcher Belag eignet sich für eine Terrasse?", "Keramikplatten sind pflegeleicht und farbbeständig, Betonstein ist vielseitig und preislich attraktiv, Naturstein wirkt besonders lebendig. Wir zeigen Ihnen die Unterschiede und empfehlen, was zu Haus und Nutzung passt."),
     ("Können Sie eine erhöhte Terrasse bauen?", "Ja. Liegt die Terrassentür über Geländeniveau, bauen wir die Fläche auf und fassen sie mit Palisaden, Mauersteinen oder Stufen ein."),
     ("Bauen Sie auch barrierearme Zugänge?", "Ja, wir legen Rampen und flache Stufenanlagen an, damit der Hauseingang auch mit Rollator, Kinderwagen oder Rollstuhl gut erreichbar ist."),
     ("Erneuern Sie auch nur die Eingangstreppe?", "Selbstverständlich. Auch einzelne Arbeiten wie eine neue Treppe oder ein neuer Terrassenbelag sind bei uns in guten Händen.")],
    "Terrasse / Treppe")

service("gartenpflege",
    "Gartenpflege &amp; <em>Grünanlagenpflege</em>",
    "Gartenpflege Sickte, Braunschweig, Wolfenbüttel | Jaszewski",
    "Gartenpflege und Grünanlagenpflege vom Fachbetrieb: Rasen, Hecke, Beete und Objektpflege für Privatgärten, Wohnanlagen und Gewerbe. Jaszewski aus Sickte – jetzt anfragen.",
    "Ein Garten macht nur Freude, wenn er gepflegt ist. Wir übernehmen das – einmalig oder regelmäßig, im Privatgarten genauso wie an Wohnanlagen und Gewerbeobjekten.",
    "heckenschnitt-1200", "Gärtner beim Schneiden einer Hecke mit der Heckenschere",
    "Auch morgen noch einen <em>schönen Garten genießen</em>",
    ["Rasen mähen, Hecken schneiden, Beete sauber halten – was nach wenig klingt, kostet übers Jahr viel Zeit. Unser Pflegeservice nimmt Ihnen diese Arbeit ab und sorgt dafür, dass Ihre Anlage durchgehend gepflegt aussieht.",
     "Sie entscheiden, wie viel Unterstützung Sie möchten: einen gründlichen Durchgang im Frühjahr und Herbst oder eine feste, regelmäßige Betreuung über die ganze Saison.",
     "Für Hausverwaltungen, Eigentümergemeinschaften und Unternehmen übernehmen wir die Objektpflege der gesamten Außenanlage – verlässlich und mit festem Ansprechpartner."],
    "Unser Pflegeservice",
    ["Rasenpflege: Mähen, Vertikutieren, Düngen", "Hecken-, Strauch- und Gehölzschnitt", "Beetpflege und Unkrautentfernung", "Frühjahrs- und Herbstdurchgang",
     "Laubbeseitigung", "Pflege von Wegen und Pflasterflächen", "Objektpflege für Wohnanlagen und Gewerbe"],
    "garten-staudenbeet-1200", "Gepflegte Rasenfläche mit sauber gefasstem Staudenbeet",
    "Pflege mit <em>Plan und festen Terminen</em>",
    "Wir stimmen mit Ihnen ab, was wann gemacht wird. So bleibt Ihr Garten das ganze Jahr in Form.",
    ["Einmalige Einsätze oder regelmäßige Betreuung", "Eigene Geräte, fachgerechter Schnitt", "Grünschnitt wird auf Wunsch mitgenommen"],
    [("Wie oft sollte der Garten gepflegt werden?", "Das hängt von Größe, Bepflanzung und Ihrem Anspruch ab. Manche Kunden buchen zwei gründliche Durchgänge im Jahr, andere eine regelmäßige Pflege in der Saison. Wir empfehlen Ihnen einen sinnvollen Rhythmus."),
     ("Übernehmen Sie auch einmalige Einsätze?", "Ja, zum Beispiel einen Heckenschnitt, das Herrichten eines verwilderten Gartens oder einen Frühjahrsputz."),
     ("Pflegen Sie auch Außenanlagen von Mietshäusern und Firmen?", "Ja. Die Garten- und Objektpflege für Wohnanlagen und Gewerbe gehört zu unseren Schwerpunkten – auf Wunsch kombiniert mit dem Winterdienst."),
     ("Nehmen Sie den Grünschnitt mit?", "Auf Wunsch kümmern wir uns um Abfuhr und Entsorgung von Schnittgut und Laub.")],
    "Gartenpflege")

service("zaunbau",
    "Zaunbau – <em>Zäune, Tore und Sichtschutz</em>",
    "Zaunbau Sickte, Braunschweig, Wolfenbüttel | Jaszewski",
    "Zaun setzen lassen: Doppelstabmattenzaun, Sichtschutz und Tore vom Garten- und Landschaftsbau Jaszewski aus Sickte. Fundamente, Montage und Anschluss an Pflaster aus einer Hand.",
    "Ein Zaun gibt dem Grundstück einen klaren Rahmen. Wir setzen Zäune, Tore und Sichtschutz gerade, stabil und passend zur übrigen Außenanlage.",
    "einfahrt-pflaster-carport", "Grundstück mit Stabmattenzaun entlang der gepflasterten Einfahrt",
    "Ein klarer Rahmen <em>für Ihr Grundstück</em>",
    ["Sicherheit für Kinder und Haustiere, Schutz vor Blicken oder einfach eine saubere Grundstücksgrenze: Die Gründe für einen neuen Zaun sind unterschiedlich. Wir beraten Sie zu Höhe, Material und Verlauf und setzen den Zaun fachgerecht.",
     "Dauerhaft gerade steht ein Zaun nur mit ordentlichen Fundamenten. Deshalb setzen wir die Pfosten in Beton und richten die Anlage sorgfältig in Flucht und Höhe aus – auch bei Gefälle.",
     "Praktisch: Weil wir auch pflastern und Gärten anlegen, passen Zaun, Tor, Einfahrt und Bepflanzung am Ende zusammen."],
    "Unsere Leistungen im Zaunbau",
    ["Doppelstabmattenzäune", "Sichtschutzzäune", "Gartentore und Einfahrtstore", "Pfostenfundamente in Beton",
     "Anpassung an Gefälle und Geländeverlauf", "Abbau und Entsorgung alter Zäune", "Hecken als grüne Alternative"],
    "hofpflaster-wege-am-haus", "Sauber eingefasste Hoffläche an der Grundstücksgrenze",
    "Zaun, Tor und Einfahrt <em>aus einem Guss</em>",
    "Wenn ein Betrieb Zaun und Pflaster gemeinsam plant, passen Höhen, Anschlüsse und Torbreiten von Anfang an.",
    ["Beratung zu Höhe, Material und Verlauf", "Stabile Fundamente, exakt ausgerichtet", "Abstimmung mit Pflaster und Bepflanzung"],
    [("Welcher Zaun passt zu meinem Grundstück?", "Doppelstabmatten sind robust, langlebig und pflegeleicht. Wenn Sichtschutz wichtig ist, kommen geschlossene Elemente oder eine Hecke infrage. Wir zeigen Ihnen vor Ort, was sinnvoll ist."),
     ("Was kostet ein neuer Zaun?", "Entscheidend sind Länge, Höhe, Material, Tore und der Untergrund. Nach dem Aufmaß bei Ihnen erhalten Sie eine individuelle Kalkulation."),
     ("Entfernen Sie den alten Zaun?", "Ja, Abbau und Entsorgung der alten Anlage übernehmen wir auf Wunsch mit."),
     ("Muss ich beim Zaunbau etwas mit dem Nachbarn klären?", "Bei Zäunen an der Grundstücksgrenze empfiehlt es sich, vorab mit den Nachbarn zu sprechen. Für die zulässige Höhe und Art gelten das niedersächsische Nachbarrecht und gegebenenfalls örtliche Vorgaben – im Zweifel gibt Ihre Gemeinde Auskunft.")],
    "Zaunbau")

service("winterdienst",
    "Winterdienst – <em>Räumen und Streuen</em>",
    "Winterdienst Sickte, Braunschweig, Wolfenbüttel | Jaszewski",
    "Winterdienst vom Fachbetrieb: Schnee räumen und streuen für Privatgrundstücke, Wohnanlagen und Gewerbe rund um Sickte, Braunschweig und Wolfenbüttel. Jetzt für die Saison anfragen.",
    "Wenn es schneit oder friert, müssen Wege und Zufahrten sicher sein. Wir räumen und streuen – schnell, zuverlässig und professionell.",
    "winterdienst-schneeraeumung", "Schneeräumung mit Räumschild auf einer gepflasterten Fläche",
    "Sicher durch den Winter – <em>ohne früh aufzustehen</em>",
    ["Eigentümer sind in der Regel dafür verantwortlich, dass Gehwege und Zugänge bei Schnee und Glätte geräumt und gestreut sind. Wer das nicht selbst leisten kann oder will, gibt die Aufgabe an uns ab.",
     "Mit eigener Räumtechnik halten wir Gehwege, Zufahrten, Höfe und Parkflächen frei. Sie müssen sich um nichts kümmern und kommen morgens sicher vom Grundstück.",
     "Besonders für Hausverwaltungen, Vermieter und Betriebe lohnt sich die Kombination mit unserer Garten- und Objektpflege: ein Ansprechpartner für die Außenanlage – das ganze Jahr."],
    "Das übernehmen wir",
    ["Schneeräumung auf Gehwegen und Zuwegen", "Räumen von Zufahrten, Höfen und Parkflächen", "Streuen bei Schnee- und Eisglätte", "Einsatz eigener Räumtechnik",
     "Betreuung über die gesamte Wintersaison", "Für Privat, Wohnanlagen und Gewerbe"],
    "einfahrt-pflaster-carport", "Einfahrt und Zuwegung eines Wohnhauses",
    "Rechtzeitig für die <em>Saison vormerken</em>",
    "Die Touren für den Winter planen wir im Voraus. Wer sich früh meldet, sichert sich seinen Platz.",
    ["Feste Vereinbarung für die Saison", "Ganzjährige Betreuung mit der Objektpflege kombinierbar", "Ein Ansprechpartner für Ihre Außenanlage"],
    [("Für wen bieten Sie Winterdienst an?", "Für private Grundstücke, Mehrfamilienhäuser und Wohnanlagen sowie für Gewerbeflächen in Sickte und Umgebung."),
     ("Wann sollte ich den Winterdienst anfragen?", "Am besten im Spätsommer oder Herbst, bevor die Saison beginnt. Dann können wir Ihr Objekt fest in die Tourenplanung aufnehmen."),
     ("Wer ist für das Räumen verantwortlich?", "In der Regel der Eigentümer; Details wie Zeiten und Umfang regelt die Satzung Ihrer Gemeinde. Die Aufgabe lässt sich auf einen Dienstleister übertragen."),
     ("Lässt sich der Winterdienst mit der Gartenpflege kombinieren?", "Ja. Viele Kunden lassen ihre Außenanlage ganzjährig von uns betreuen – im Sommer die Pflege, im Winter Räumen und Streuen.")],
    "Winterdienst")


# ---------- Leistungen (Übersicht) ----------
trail = [("Start", "index.html"), ("Leistungen", "leistungen.html")]
PAGES.append(page("leistungen", "Leistungen: Gartenbau, Pflaster, Terrassen, Pflege | Jaszewski Sickte",
    "Alle Leistungen von Jaszewski Garten- & Landschaftsbau im Überblick: Gartengestaltung, Pflasterarbeiten, Terrassen und Treppen, Gartenpflege, Zaunbau und Winterdienst.",
    f'''
<section class="phero simple"><div class="wrap phero-g"><div>{crumbs(trail)}{eyebrow("Leistungen")}
<h1>Alles auf einen Blick – <em>von der Neuanlage bis zur Pflege</em></h1>
<p class="lead">Wir kümmern uns um die gesamte Außenanlage: planen, bauen, pflastern, einfrieden und pflegen. Wählen Sie eine Leistung für mehr Details.</p></div></div></section>
<section class="sec" style="padding-top:clamp(30px,4vw,50px)"><div class="wrap">{svc_cards()}</div></section>
<section class="sec" style="padding-top:0"><div class="wrap cols">
<div class="rv"><h2>Ein Betrieb für <em>das ganze Grundstück</em></h2>
<p>Viele Vorhaben greifen ineinander: Zur neuen Einfahrt gehört oft ein Zaun, zur Terrasse der passende Rasen, zur fertigen Anlage die laufende Pflege. Bei uns bekommen Sie das aus einer Hand – abgestimmt und ohne Reibungsverluste zwischen verschiedenen Firmen.</p>
<p>Unser Schwerpunkt liegt auf Neuanlagen, der Umgestaltung von Hausgärten, Garten- und Objektpflege, Pflanzungen sowie dem Bau von Terrassen und Sitzplätzen.</p></div>
<div class="rv"><h3 style="margin-bottom:6px">Außerdem für Sie da</h3>
{checks(["Rollrasen und Rasenneuanlage", "Hecken- und Gehölzpflanzungen", "Poolumrandungen", "Rampen und barrierearme Hauseingänge", "Palisaden, Einfassungen und kleine Mauern", "Erdarbeiten mit eigenem Minibagger"])}</div>
</div></section>
{steps()}
{contact()}
''', current="leistungen", schemas=[crumbs_schema(trail)]))


# ---------- Referenzen ----------
trail = [("Start", "index.html"), ("Referenzen", "referenzen.html")]
PAGES.append(page("referenzen", "Referenzen: Terrassen, Einfahrten, Gärten | Jaszewski Sickte",
    "Referenzen von Jaszewski Garten- & Landschaftsbau: gepflasterte Einfahrten, Terrassen, Eingangstreppen, Poolumrandungen und Rollrasen aus der Region Braunschweig / Wolfenbüttel.",
    f'''
<section class="phero simple"><div class="wrap phero-g"><div>{crumbs(trail)}{eyebrow("Referenzen")}
<h1>Jüngste Arbeiten – <em>gebaut in der Region</em></h1>
<p class="lead">Bilder sagen mehr als jede Beschreibung. Hier sehen Sie eine Auswahl an Projekten, die wir für private Bauherren umgesetzt haben.</p></div></div></section>
<section class="sec" style="padding-top:clamp(30px,4vw,50px)"><div class="wrap">{gallery()}</div></section>
{band("Ihr Projekt könnte das nächste sein", "Zeigen Sie uns Ihr Grundstück – wir sagen Ihnen, was möglich ist.")}
{contact()}
''', current="referenzen", schemas=[crumbs_schema(trail)]))


# ---------- Über uns ----------
trail = [("Start", "index.html"), ("Über uns", "ueber-uns.html")]
PAGES.append(page("ueber-uns", "Über uns: Familienbetrieb seit 2007 | Jaszewski Sickte",
    "Jaszewski Garten- & Landschaftsbau ist ein Familienbetrieb aus Sickte. Seit 2007 stehen wir für saubere Arbeit, offene Kommunikation und persönliche Beratung vor Ort.",
    f'''
<section class="phero"><div class="wrap phero-g">
<div>{crumbs(trail)}{eyebrow("Über uns")}
<h1>Familienbetrieb aus Sickte – <em>seit 2007</em></h1>
<p class="lead">Hinter Jaszewski Garten- &amp; Landschaftsbau steht ein Team, das sein Handwerk gern macht – und das merkt man den Ergebnissen an.</p>
<div class="cta-row"><a class="btn btn-primary" href="kontakt.html">Kontakt aufnehmen{ICON["arrow"]}</a><a class="btn btn-ghost" href="tel:{TEL1_L}">{ICON["phone"]}{TEL1}</a></div></div>
<div class="phero-img sq">{img("team-jaszewski", "Das Team von " + FIRMA + " in Arbeitskleidung vor dem Firmenbanner", lazy=False)}</div>
</div></section>
<section class="sec" style="padding-top:clamp(40px,6vw,80px)"><div class="wrap cols">
<div class="rv"><h2>Unsere <em>Geschichte</em></h2>
<p>Wir sind ein Familienunternehmen und seit 2007 im Garten- und Landschaftsbau tätig. Was mit Gartenpflege und kleineren Aufträgen begann, ist über die Jahre zu einem Betrieb gewachsen, der komplette Außenanlagen plant und baut.</p>
<p>Heute liegen unsere Schwerpunkte auf Neuanlagen, der Umgestaltung von Hausgärten, der Garten- und Objektpflege, Pflanzungen sowie dem Bau von Terrassen und Sitzplätzen.</p></div>
<div class="rv"><h2>Wie wir <em>arbeiten</em></h2>
<p>Qualität steht bei uns an erster Stelle – genauso wie ein gutes Arbeitsklima im Team. Beides gehört zusammen: Wer gern zur Arbeit kommt, arbeitet sorgfältiger.</p>
<p>Wir legen Wert auf offene Kommunikation. Sie erfahren von uns vor, während und nach dem Projekt, was ansteht. Und weil wir gut mit eigenen Maschinen ausgestattet sind, können wir zügig und kostengünstig arbeiten.</p></div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><ul class="feat">
<li class="rv"><div class="ic">{ICON["team"]}</div><h3>Familienbetrieb</h3><p>Inhabergeführt von {INHABER}. Sie sprechen direkt mit den Menschen, die Ihr Projekt umsetzen.</p></li>
<li class="rv" style="--d:.08s"><div class="ic">{ICON["talk"]}</div><h3>Offene Kommunikation</h3><p>Klare Absprachen und ein fester Ansprechpartner über die gesamte Bauzeit.</p></li>
<li class="rv" style="--d:.16s"><div class="ic">{ICON["bagger"]}</div><h3>Gut ausgestattet</h3><p>Eigene Maschinen und Geräte für Erdarbeiten, Pflaster, Pflege und Winterdienst.</p></li>
</ul></div></section>
{steps()}
{contact()}
''', current="ueber-uns", schemas=[crumbs_schema(trail)]))


# ---------- Einsatzgebiet + Ortsseiten ----------
trail = [("Start", "index.html"), ("Einsatzgebiet", "einsatzgebiet.html")]
PAGES.append(page("einsatzgebiet", "Einsatzgebiet: Sickte, Braunschweig, Wolfenbüttel | Jaszewski Gartenbau",
    "Jaszewski Garten- & Landschaftsbau arbeitet in Sickte, Braunschweig, Wolfenbüttel, Cremlingen, Königslutter, Schöppenstedt und Umgebung. Prüfen Sie, ob wir auch zu Ihnen kommen.",
    f'''
<section class="phero simple"><div class="wrap phero-g"><div>{crumbs(trail)}{eyebrow("Einsatzgebiet")}
<h1>Gartenbau in Sickte <em>und rund um den Elm</em></h1>
<p class="lead">Unser Betrieb liegt in Sickte, zwischen Braunschweig und Wolfenbüttel. Von hier aus sind wir in der ganzen Region für Sie unterwegs.</p></div></div></section>
<section class="sec" style="padding-top:clamp(30px,4vw,50px)"><div class="wrap split">
<div class="rv"><h2>Hier sind wir <em>regelmäßig im Einsatz</em></h2>
<p class="lead">Kurze Anfahrt bedeutet: schnelle Termine vor Ort und flexible Abstimmung während der Bauphase.</p>
{areas()}
<p class="muted" style="margin-top:26px">Ihr Ort ist nicht dabei? Rufen Sie uns trotzdem an – je nach Vorhaben kommen wir auch gern etwas weiter.</p></div>
<div class="split-img rv"><div class="frame wide">{img("terrasse-grossformatplatten", "Terrasse mit Großformatplatten – Projekt in der Region")}</div></div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="rel rv">
<a href="gartenbau-braunschweig.html">Gartenbau in Braunschweig{ICON["arrow"]}</a>
<a href="gartenbau-wolfenbuettel.html">Gartenbau in Wolfenbüttel{ICON["arrow"]}</a>
<a href="leistungen.html">Alle Leistungen{ICON["arrow"]}</a></div></div></section>
{contact()}
''', current="einsatzgebiet", schemas=[crumbs_schema(trail)]))


def ortsseite(slug, ort, title, desc, lead, h2a, pa, h2b, pb, faq, bild, bild_alt):
    trail = [("Start", "index.html"), ("Einsatzgebiet", "einsatzgebiet.html"), (ort, slug + ".html")]
    body = f'''
<section class="phero"><div class="wrap phero-g">
<div>{crumbs(trail)}{eyebrow("Einsatzgebiet · " + ort)}
<h1>Garten- und Landschaftsbau <em>in {ort}</em></h1><p class="lead">{lead}</p>
<div class="cta-row"><a class="btn btn-primary" href="#anfrage">Angebot anfragen{ICON["arrow"]}</a><a class="btn btn-ghost" href="tel:{TEL1_L}">{ICON["phone"]}{TEL1}</a></div></div>
<div class="phero-img">{img(bild, bild_alt, lazy=False)}</div>
</div></section>
<section class="sec" style="padding-top:clamp(40px,6vw,80px)"><div class="wrap cols">
<div class="rv"><h2>{h2a}</h2>{"".join(f"<p>{p}</p>" for p in pa)}</div>
<div class="rv"><h2>{h2b}</h2>{"".join(f"<p>{p}</p>" for p in pb)}</div>
</div></section>
<section class="sec" style="padding-top:0"><div class="wrap">
<div class="head"><div class="rv">{eyebrow("Leistungen in " + ort)}<h2>Das übernehmen wir <em>für Sie in {ort}</em></h2></div>
<p class="lead rv">Jede Leistung führt zu einer eigenen Seite mit allen Details.</p></div>
{svc_cards()}</div></section>
{steps()}
{faq_block(faq, title="Fragen aus " + ort)}
{contact()}
'''
    PAGES.append(page(slug, title, desc, body, current="einsatzgebiet", schemas=[crumbs_schema(trail), faq_schema(faq)]))


ortsseite("gartenbau-braunschweig", "Braunschweig",
    "Gartenbau Braunschweig: Pflaster, Terrassen, Gartenpflege | Jaszewski",
    "Garten- und Landschaftsbau für Braunschweig: Jaszewski aus Sickte gestaltet Gärten, pflastert Einfahrten, baut Terrassen und Zäune und pflegt Grünanlagen. Termin vor Ort anfragen.",
    "Von unserem Betrieb in Sickte sind es nur wenige Kilometer bis Braunschweig. Für Hausbesitzer, Vermieter und Betriebe in der Stadt sind wir ein Fachbetrieb mit kurzen Wegen.",
    "Ihr Gartenbauer <em>vor den Toren der Stadt</em>",
    ["Ob Reihenhausgarten im östlichen Ringgebiet, Neubaugrundstück am Stadtrand oder Einfamilienhaus in den südöstlichen Stadtteilen: In Braunschweig sind die Grundstücke so unterschiedlich wie ihre Besitzer. Wir schauen uns die Situation vor Ort an und entwickeln eine Lösung, die zu Fläche und Budget passt.",
     "Gerade auf kleineren Stadtgrundstücken zählt eine durchdachte Planung: Wo entsteht der Sitzplatz, wie viel Fläche wird befestigt, wie bleibt der Garten pflegeleicht? Darüber sprechen wir, bevor der erste Stein bewegt wird."],
    "Kurze Wege, <em>verlässliche Termine</em>",
    ["Sickte grenzt südöstlich an das Braunschweiger Stadtgebiet. Für Sie bedeutet das: Wir sind schnell bei Ihnen – zum Beratungstermin genauso wie während der Bauphase.",
     "Für Hausverwaltungen und Gewerbekunden in Braunschweig übernehmen wir die laufende Pflege der Außenanlagen und auf Wunsch den Winterdienst – ganzjährig aus einer Hand."],
    [("Kommen Sie für einen Beratungstermin nach Braunschweig?", "Ja. Wir vereinbaren einen Termin bei Ihnen vor Ort, schauen uns das Grundstück an und besprechen Ihr Vorhaben."),
     ("In welchen Braunschweiger Stadtteilen arbeiten Sie?", "Im gesamten Stadtgebiet. Besonders kurz ist unser Weg in die östlichen und südöstlichen Stadtteile, die direkt an die Samtgemeinde Sickte angrenzen."),
     ("Übernehmen Sie in Braunschweig auch die Pflege von Wohnanlagen?", "Ja, wir betreuen Außenanlagen von Mehrfamilienhäusern und Gewerbeobjekten – inklusive Winterdienst, wenn gewünscht.")],
    "einfahrt-pflaster-carport", "Gepflasterte Einfahrt an einem Einfamilienhaus")

ortsseite("gartenbau-wolfenbuettel", "Wolfenbüttel",
    "Gartenbau Wolfenbüttel: Gartengestaltung, Pflaster, Zaunbau | Jaszewski",
    "Garten- und Landschaftsbau für Wolfenbüttel und den Landkreis: Jaszewski aus Sickte übernimmt Gartengestaltung, Pflasterarbeiten, Terrassenbau, Zaunbau und Gartenpflege.",
    "Sickte gehört zum Landkreis Wolfenbüttel – wir sind hier zu Hause. Ob in der Kernstadt oder in den Dörfern ringsum: Wir kennen die Region und sind schnell bei Ihnen.",
    "Aus dem Landkreis, <em>für den Landkreis</em>",
    ["Zwischen Oker, Asse und Elm gibt es viele gewachsene Grundstücke mit altem Baumbestand, aber auch immer neue Baugebiete. Entsprechend breit ist die Bandbreite unserer Arbeit: von der kompletten Neuanlage am Neubau bis zur behutsamen Umgestaltung eines alten Gartens.",
     "Wir beraten Sie persönlich vor Ort und kalkulieren Ihr Vorhaben individuell. So wissen Sie von Anfang an, was auf Sie zukommt."],
    "Ein Ansprechpartner <em>für alle Arbeiten draußen</em>",
    ["Einfahrt, Terrasse, Zaun, Rasen und Bepflanzung greifen ineinander. Wenn alles von einem Betrieb kommt, passen Höhen, Anschlüsse und Zeitplan zusammen.",
     "Auch nach der Fertigstellung sind wir für Sie da: Unser Pflegeservice betreut Gärten und Grünanlagen in Wolfenbüttel und den umliegenden Gemeinden dauerhaft."],
    [("Arbeiten Sie auch in den Ortsteilen und Dörfern rund um Wolfenbüttel?", "Ja. Wir sind im gesamten Landkreis unterwegs – unter anderem in Sickte, Cremlingen, Dettum, Evessen, Erkerode und Schöppenstedt."),
     ("Wie schnell können Sie sich mein Grundstück ansehen?", "Rufen Sie uns an oder schreiben Sie per WhatsApp – den Termin stimmen wir direkt mit Ihnen ab. Durch die kurze Anfahrt sind wir flexibel."),
     ("Bieten Sie in Wolfenbüttel Winterdienst an?", "Ja, für Privatgrundstücke, Wohnanlagen und Gewerbeflächen. Am besten melden Sie sich vor Saisonbeginn.")],
    "rollrasen-terrasse-neubau", "Neu angelegter Garten mit Rollrasen an einem Neubau")


# ---------- Kontakt ----------
trail = [("Start", "index.html"), ("Kontakt", "kontakt.html")]
PAGES.append(page("kontakt", "Kontakt | Jaszewski Garten- & Landschaftsbau Sickte",
    f"Kontakt zu Jaszewski Garten- & Landschaftsbau in Sickte: Telefon {TEL1}, WhatsApp oder Anfrageformular. Wir vereinbaren einen Termin bei Ihnen vor Ort.",
    f'''
<section class="phero simple"><div class="wrap phero-g"><div>{crumbs(trail)}{eyebrow("Kontakt")}
<h1>Sprechen wir über <em>Ihren Garten</em></h1>
<p class="lead">Rufen Sie an, schreiben Sie uns oder nutzen Sie das Formular. Wir melden uns und vereinbaren einen Termin bei Ihnen vor Ort.</p>
<div class="cta-row" style="margin-top:8px"><a class="btn btn-primary" href="tel:{TEL1_L}">{ICON["phone"]}{TEL1}</a><a class="btn btn-wa" href="https://wa.me/{WA}" target="_blank" rel="noopener">{ICON["wa"]}WhatsApp schreiben</a></div>
</div></div></section>
{contact(light=True, h="So erreichen <em>Sie uns</em>")}
''', current="kontakt", schemas=[crumbs_schema(trail)]))


# ---------- Rechtliches ----------
def legal(slug, title, h1, inner):
    trail = [("Start", "index.html"), (h1, slug + ".html")]
    PAGES.append(page(slug, title, h1 + " von " + FIRMA + ", " + ORT + ".",
        f'<section class="phero simple"><div class="wrap">{crumbs(trail)}<h1 style="font-size:clamp(2.2rem,4.600vw,3.600rem)">{h1}</h1></div></section>'
        f'<section class="sec" style="padding-top:20px"><div class="wrap"><div class="prose">{inner}</div></div></section>',
        noindex=True))


legal("impressum", "Impressum | " + FIRMA, "Impressum", f'''
<h2>Angaben gemäß § 5 DDG</h2>
<p>{FIRMA}<br>Inhaber: {INHABER}<br>{STR}<br>{PLZ} {ORT}</p>
<h2>Kontakt</h2>
<p>Telefon: <a href="tel:{TEL1_L}">{TEL1}</a><br>Mobil: <a href="tel:{TEL2_L}">{TEL2}</a><br>E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></p>
<h2>Redaktionell verantwortlich</h2>
<p>{INHABER}, Anschrift wie oben.</p>
<h2>Verbraucherstreitbeilegung</h2>
<p>Wir sind nicht bereit oder verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
<h2>Haftung für Inhalte und Links</h2>
<p>Die Inhalte dieser Seiten wurden mit Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität können wir jedoch keine Gewähr übernehmen. Für Inhalte externer Links sind ausschließlich deren Betreiber verantwortlich.</p>
<h2>Urheberrecht</h2>
<p>Die auf dieser Website veröffentlichten Texte und Bilder unterliegen dem deutschen Urheberrecht. Eine Verwendung außerhalb der Grenzen des Urheberrechts bedarf der vorherigen Zustimmung.</p>
''')

legal("datenschutz", "Datenschutz | " + FIRMA, "Datenschutzerklärung", f'''
<h2>1. Verantwortlicher</h2>
<p>{FIRMA}, Inhaber {INHABER}, {STR}, {PLZ} {ORT}<br>Telefon: {TEL1} · E-Mail: <a href="mailto:{MAIL}">{MAIL}</a></p>
<h2>2. Aufruf der Website (Server-Logfiles)</h2>
<p>Beim Aufruf dieser Website verarbeitet der Hosting-Anbieter technisch notwendige Daten (u. a. IP-Adresse, Datum und Uhrzeit, aufgerufene Seite, Browsertyp), um die Seite auszuliefern und den sicheren Betrieb zu gewährleisten. Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Die Daten werden nicht mit anderen Datenquellen zusammengeführt.</p>
<h2>3. Cookies, Tracking und externe Inhalte</h2>
<p>Diese Website setzt keine Cookies und verwendet keine Analyse- oder Werbedienste. Schriften und Bilder werden vom eigenen Server geladen; es werden keine Inhalte von Drittanbietern eingebunden.</p>
<h2>4. Kontaktaufnahme</h2>
<p>Wenn Sie uns per Telefon oder E-Mail kontaktieren, verarbeiten wir Ihre Angaben zur Bearbeitung der Anfrage (Art. 6 Abs. 1 lit. b bzw. f DSGVO). Die Daten werden gelöscht, sobald sie für den Zweck nicht mehr erforderlich sind und keine gesetzlichen Aufbewahrungspflichten entgegenstehen.</p>
<p>Das Anfrageformular auf dieser Website überträgt keine Daten an unseren Server. Es erstellt lediglich eine vorformulierte Nachricht, die Sie selbst über Ihr E-Mail-Programm oder über WhatsApp absenden.</p>
<h2>5. WhatsApp</h2>
<p>Wenn Sie uns über WhatsApp schreiben, erfolgt die Kommunikation über den Dienst der WhatsApp Ireland Limited, Merrion Road, Dublin 4, Irland. Dabei gelten die Datenschutzbestimmungen von WhatsApp. Die Nutzung ist freiwillig; Sie können uns jederzeit auch telefonisch oder per E-Mail erreichen.</p>
<h2>6. Ihre Rechte</h2>
<p>Sie haben das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit sowie Widerspruch gegen die Verarbeitung Ihrer personenbezogenen Daten. Außerdem können Sie sich bei einer Datenschutz-Aufsichtsbehörde beschweren, zum Beispiel bei der Landesbeauftragten für den Datenschutz Niedersachsen.</p>
''')


PAGES.append(page("404", "Seite nicht gefunden | " + FIRMA, "Diese Seite gibt es nicht (mehr).",
    f"""<section class="phero simple" style="padding-bottom:var(--sec)"><div class="wrap">{eyebrow("Fehler 404")}
<h1>Hier wächst <em>leider nichts.</em></h1>
<p class="lead">Die aufgerufene Seite gibt es nicht oder sie ist umgezogen. Über die Startseite oder unsere Leistungen finden Sie sicher, was Sie suchen.</p>
<div class="cta-row"><a class="btn btn-primary" href="index.html">Zur Startseite{ICON["arrow"]}</a><a class="btn btn-ghost" href="leistungen.html">Leistungen</a><a class="btn btn-ghost" href="kontakt.html">Kontakt</a></div>
</div></section>""", noindex=True, base='<base href="/">\n'))

HTACCESS = r"""# Jaszewski Garten- & Landschaftsbau (Apache)
ErrorDocument 404 /404.html
Options -Indexes

<IfModule mod_rewrite.c>
RewriteEngine On

# Nach dem Livegang aktivieren: immer https + www
# RewriteCond %{HTTPS} off [OR]
# RewriteCond %{HTTP_HOST} !^www\. [NC]
# RewriteRule ^ https://www.gartenservice-jaszewski.de%{REQUEST_URI} [L,R=301]

# Alte Wix-Adressen dauerhaft weiterleiten
RewriteRule ^dienstleistungen/?$ /leistungen.html [L,R=301]
RewriteRule ^kontakt/?$ /kontakt.html [L,R=301]
RewriteRule ^impressum/?$ /impressum.html [L,R=301]
RewriteRule ^(ueber-uns|\xC3\xBCber-uns)/?$ /ueber-uns.html [L,R=301]
RewriteCond %{THE_REQUEST} \s/index\.html[\s?]
RewriteRule ^index\.html$ / [L,R=301]

# Arbeitsordner nicht ausliefern
RewriteRule ^(_build|_quellen)/ - [F,L]
</IfModule>

<IfModule mod_deflate.c>
AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml application/xml text/plain
</IfModule>

<IfModule mod_expires.c>
ExpiresActive On
ExpiresByType text/html "access plus 1 hour"
ExpiresByType text/css "access plus 1 year"
ExpiresByType application/javascript "access plus 1 year"
ExpiresByType image/webp "access plus 1 year"
ExpiresByType image/jpeg "access plus 1 year"
ExpiresByType image/svg+xml "access plus 1 year"
ExpiresByType font/woff2 "access plus 1 year"
</IfModule>

<IfModule mod_headers.c>
Header set X-Content-Type-Options "nosniff"
Header set Referrer-Policy "strict-origin-when-cross-origin"
Header set X-Frame-Options "SAMEORIGIN"
</IfModule>
"""
with open(os.path.join(ROOT, ".htaccess"), "w", encoding="utf-8", newline="\n") as f:
    f.write(HTACCESS)

# ---------- Sitemap, robots, Favicon ----------
today = datetime.date.today().isoformat()
urls = "".join(
    f"<url><loc>{DOMAIN}/{'' if s == 'index' else s + '.html'}</loc><lastmod>{today}</lastmod>"
    f"<priority>{'1.0' if s == 'index' else '0.8'}</priority></url>\n" for s, ni in PAGES if not ni)
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
    f.write(f"User-agent: *\nAllow: /\nDisallow: /_build/\nDisallow: /_quellen/\n\nSitemap: {DOMAIN}/sitemap.xml\n")
with open(os.path.join(ROOT, "assets", "img", "favicon.svg"), "w", encoding="utf-8", newline="\n") as f:
    f.write(LOGO.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ').replace(' aria-hidden="true"', ""))

print(len(PAGES), "Seiten erzeugt:", ", ".join(s for s, _ in PAGES))
