#!/usr/bin/env python3
"""Build arbitration-mediation.html from template patterns."""

# ─── helpers ───
def info_btn(title, detail):
    return (f'<button class="inline-flex items-center justify-center w-5 h-5 rounded-full text-muted-foreground hover:text-foreground hover:bg-accent transition-colors cursor-help ml-1 shrink-0" title="More detail">'
            f'<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="2"/><path stroke-width="2" d="M12 16v-4m0-4h.01"/></svg></button>'
            f'<div class="info-popover"><strong>{title}</strong>{detail}</div>')

def badge(label, color):
    colors = {
        'para': 'bg-blue-100 text-blue-800',
        'attorney': 'bg-purple-100 text-purple-800',
        'system': 'bg-green-100 text-green-800',
        'mgmt': 'bg-orange-100 text-orange-800',
        'required': 'bg-red-100 text-red-800',
        'cnad': 'bg-yellow-100 text-yellow-800',
        'auto': 'bg-green-100 text-green-800',
    }
    return f'<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold {colors[color]}">{label}</span>'

def task_row(num, task, info_title, info_detail, assigned_badge, status_badge, sla):
    return (f'      <tr class="border-b border-border last:border-b-0 hover:bg-muted/50">'
            f'<td class="px-4 py-3 text-sm text-foreground">{num}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{task}{info_btn(info_title, info_detail)}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{assigned_badge}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{status_badge}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{sla}</td></tr>')

def table_header():
    return ('<tr class="border-b border-border bg-muted">'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">#</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Task</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Assigned To</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Badge</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">SLA</th></tr>')

def kpi_table_header():
    return ('<tr class="border-b border-border bg-muted">'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">#</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">KPI</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Owner</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">SLA</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Green</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Yellow</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Red</th></tr>')

def kpi_row(num, kpi, owner, sla, green, yellow, red):
    return (f'      <tr class="border-b border-border last:border-b-0 hover:bg-muted/50">'
            f'<td class="px-4 py-3 text-sm text-foreground">{num}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{kpi}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{owner}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{sla}</td>'
            f'<td class="px-4 py-3 text-sm"><span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold bg-green-100 text-green-800">{green}</span></td>'
            f'<td class="px-4 py-3 text-sm"><span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold bg-yellow-100 text-yellow-800">{yellow}</span></td>'
            f'<td class="px-4 py-3 text-sm"><span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] font-semibold bg-red-100 text-red-800">{red}</span></td></tr>')

def field_table_header():
    return ('<tr class="border-b border-border bg-muted">'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Field API Name</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Label</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Type</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Object</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Purpose</th></tr>')

def field_row(api, label, ftype, obj, purpose):
    return (f'      <tr class="border-b border-border last:border-b-0 hover:bg-muted/50">'
            f'<td class="px-4 py-3 text-xs font-mono text-foreground">{api}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{label}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{ftype}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{obj}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{purpose}</td></tr>')

def flow_table_header():
    return ('<tr class="border-b border-border bg-muted">'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Flow Name</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Type</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Trigger</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Actions</th></tr>')

def flow_row(name, ftype, trigger, actions):
    return (f'      <tr class="border-b border-border last:border-b-0 hover:bg-muted/50">'
            f'<td class="px-4 py-3 text-sm font-medium text-foreground">{name}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{ftype}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{trigger}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{actions}</td></tr>')

def rule_table_header():
    return ('<tr class="border-b border-border bg-muted">'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Rule Name</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Object</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Condition</th>'
            '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Error Message</th></tr>')

def rule_row(name, obj, cond, msg):
    return (f'      <tr class="border-b border-border last:border-b-0 hover:bg-muted/50">'
            f'<td class="px-4 py-3 text-sm font-mono text-foreground">{name}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{obj}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{cond}</td>'
            f'<td class="px-4 py-3 text-sm text-foreground">{msg}</td></tr>')

ACCENT = '#14b8a6'
PAGE_ID = 'arbitration-mediation'

# ─── Build HTML ───
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BJB Arbitration &amp; Mediation &mdash; Litify Dev Specification</title>
<style>
#tooltip-overlay{{position:absolute;z-index:9999;background:#fff;border:1px solid #e5e5e5;border-radius:0.5rem;box-shadow:0 4px 16px rgba(0,0,0,0.12);padding:12px 14px;min-width:260px;max-width:340px;font-size:12px;color:#0a0a0a;line-height:1.5;pointer-events:none}}
#tooltip-overlay strong{{display:block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.4px;color:#171717;margin-bottom:6px}}
#tooltip-overlay ul{{padding-left:14px;margin:4px 0 0}}
#tooltip-overlay li{{margin-bottom:3px}}
.info-popover{{display:none}}
@media print{{aside,nav{{display:none!important}}main{{padding:20px!important}}[data-card-body]{{display:block!important}}.tab-pane{{display:block!important}}.bg-primary{{background:#171717!important;color:#fafafa!important;-webkit-print-color-adjust:exact}}}}
</style>
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {{
  theme: {{
    extend: {{
      colors: {{
        background: '#fafafa', foreground: '#0a0a0a', card: '#ffffff', 'card-foreground': '#0a0a0a',
        primary: '#171717', 'primary-foreground': '#fafafa', secondary: '#f5f5f5', 'secondary-foreground': '#171717',
        muted: '#f5f5f5', 'muted-foreground': '#737373', accent: '#f5f5f5', 'accent-foreground': '#171717',
        destructive: '#ef4444', border: '#e5e5e5', input: '#e5e5e5', ring: '#0a0a0a',
        sidebar: '#fafafa', 'sidebar-foreground': '#171717', 'sidebar-accent': '#f5f5f5',
      }},
      borderRadius: {{ lg: '0.625rem', md: '0.5rem', sm: '0.375rem' }}
    }}
  }}
}}
</script>
</head>
<body class="bg-background text-foreground font-[-apple-system,BlinkMacSystemFont,'Inter',sans-serif] text-sm leading-relaxed">
<!-- TOP NAV -->
<nav class="sticky top-0 z-50 h-14 border-b border-border bg-card">
  <div class="max-w-[1460px] mx-auto h-full flex items-center justify-between px-6">
    <span class="text-sm font-semibold text-muted-foreground tracking-wide">BJB Performance Plan</span>
    <div class="hidden md:flex items-center gap-1">
      <a href="index.html" class="px-3 py-1.5 text-sm font-medium text-muted-foreground rounded-md hover:bg-accent hover:text-accent-foreground transition-colors no-underline">Case Opening</a>
      <a href="treatment-monitoring.html" class="px-3 py-1.5 text-sm font-medium text-muted-foreground rounded-md hover:bg-accent hover:text-accent-foreground transition-colors no-underline">Treatment Monitoring</a>
      <a href="written-discovery.html" class="px-3 py-1.5 text-sm font-medium text-muted-foreground rounded-md hover:bg-accent hover:text-accent-foreground transition-colors no-underline">Written Discovery</a>
      <a href="expert-deposition.html" class="px-3 py-1.5 text-sm font-medium text-muted-foreground rounded-md hover:bg-accent hover:text-accent-foreground transition-colors no-underline">Expert &amp; Deposition</a>
      <a href="arbitration-mediation.html" class="px-3 py-1.5 text-sm font-medium text-foreground bg-accent rounded-md no-underline" style="border-bottom: 2px solid {ACCENT}">Arb &amp; Mediation</a>
      <a href="trial.html" class="px-3 py-1.5 text-sm font-medium text-muted-foreground rounded-md hover:bg-accent hover:text-accent-foreground transition-colors no-underline">Trial</a>
    </div>
    <button id="nav-hamburger" class="md:hidden text-foreground" onclick="document.getElementById('mobile-nav').classList.toggle('hidden')">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
    </button>
  </div>
  <div id="mobile-nav" class="hidden md:hidden bg-card border-t border-border px-4 pb-3">
    <a href="index.html" class="block px-3 py-2 text-sm font-medium text-muted-foreground rounded-md no-underline">Case Opening</a>
    <a href="treatment-monitoring.html" class="block px-3 py-2 text-sm font-medium text-muted-foreground rounded-md no-underline">Treatment Monitoring</a>
    <a href="written-discovery.html" class="block px-3 py-2 text-sm font-medium text-muted-foreground rounded-md no-underline">Written Discovery</a>
    <a href="expert-deposition.html" class="block px-3 py-2 text-sm font-medium text-muted-foreground rounded-md no-underline">Expert &amp; Deposition</a>
    <a href="arbitration-mediation.html" class="block px-3 py-2 text-sm font-medium text-foreground bg-accent rounded-md no-underline">Arb &amp; Mediation</a>
    <a href="trial.html" class="block px-3 py-2 text-sm font-medium text-muted-foreground rounded-md no-underline">Trial</a>
  </div>
</nav>
<div class="flex h-[calc(100vh-3.5rem)]">
<aside class="hidden md:flex w-64 flex-col border-r border-border bg-card overflow-y-auto shrink-0">
  <div class="px-5 pt-6 pb-4 border-b border-border">
    <h2 class="text-xs font-bold text-foreground tracking-wide uppercase">BJB Arb &amp; Mediation</h2>
    <p class="text-[11px] text-muted-foreground mt-1">Litify Dev Spec v4.0</p>
  </div>
  <div class="py-3">
    <div class="px-5 py-1.5 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Part A &mdash; Process</div>
    <a class="sidebar-link block px-5 py-1.5 text-xs font-semibold text-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('partA')">Overview</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('ph1')">Phase 1: Court Notice</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('ph2')">Phase 2: Case Prep</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('ph3')">Phase 3: De Novo</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('ph4')">Phase 4: Mediation</a>
  </div>
  <div class="py-3">
    <div class="px-5 py-1.5 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Part B &mdash; Scoring Pack</div>
    <a class="sidebar-link block px-5 py-1.5 text-xs font-semibold text-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('partB')">Overview</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('tpi')">1. Trial Probability (TPI)</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('wev')">2. Verdict Range (WEV)</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('tss')">3. Trial Strength (TSS)</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('atv')">4. Adjusted Trial Value</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('sls')">5. Settlement Leverage (SLS)</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('ctt')">6. Cost-to-Try (CTT)</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('trs')">7. Trial Readiness (TRS)</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('eri')">8. Economic Risk (ERI)</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('ccs')">9. Confidence (CCS)</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('leadership-dash')">Leadership Dashboard</a>
  </div>
  <div class="py-3">
    <div class="px-5 py-1.5 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Part C &mdash; Metrics</div>
    <a class="sidebar-link block px-5 py-1.5 text-xs font-semibold text-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('partC')">Overview</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('metrics-sla')">SLA &amp; Timeliness</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('metrics-readiness')">Readiness &amp; Coverage</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('metrics-denovo')">Decision Latency</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('metrics-quality')">Quality &amp; Rework</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('metrics-dashboard')">Dashboard Views</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('metrics-gates')">Hard Gates</a>
  </div>
  <div class="py-3">
    <div class="px-5 py-1.5 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Part D &mdash; Dev Spec</div>
    <a class="sidebar-link block px-5 py-1.5 text-xs font-semibold text-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('partD')">Overview</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('partD');setTab('tab-fields',document.querySelector('.tab-btn'))">Litify Fields</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('partD');setTab('tab-flows',document.querySelector('.tab-btn'))">Flows</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('partD');setTab('tab-rules',document.querySelector('.tab-btn'))">Validation Rules</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('approval')">Approval &amp; Notes</a>
  </div>
</aside>

<main id="main-scroll" class="flex-1 overflow-y-auto">
<div class="max-w-7xl px-6 lg:px-10 py-10 mx-auto">

<!-- PAGE HEADER -->
<div class="mb-10 border-b-4 border-[{ACCENT}] pb-8">
  <h1 class="text-2xl font-bold text-foreground">BJB Arbitration &amp; Mediation &mdash; Litify Dev Specification</h1>
  <p class="text-sm text-muted-foreground mt-1">Court Notices &nbsp;|&nbsp; Case Prep &nbsp;|&nbsp; De Novo Management &nbsp;|&nbsp; Mediation Track</p>
  <span class="inline-block mt-3 px-3 py-0.5 text-xs border border-border rounded-full text-muted-foreground bg-muted">v4.0 &bull; February 2026</span>
</div>

<!-- PHASE BAR -->
<div class="flex gap-1.5 mb-8 flex-wrap">
  <button class="px-3 py-1.5 bg-card border border-border rounded-md text-xs font-semibold text-foreground hover:bg-accent transition-colors" onclick="navTo('ph1')">1 &mdash; Court Notice &amp; Calendaring</button>
  <button class="px-3 py-1.5 bg-card border border-border rounded-md text-xs font-semibold text-foreground hover:bg-accent transition-colors" onclick="navTo('ph2')">2 &mdash; Case Prep &amp; Statement</button>
  <button class="px-3 py-1.5 bg-card border border-border rounded-md text-xs font-semibold text-foreground hover:bg-accent transition-colors" onclick="navTo('ph3')">3 &mdash; De Novo Management</button>
  <button class="px-3 py-1.5 bg-card border border-border rounded-md text-xs font-semibold text-foreground hover:bg-accent transition-colors" onclick="navTo('ph4')">4 &mdash; Mediation Track</button>
  <button class="px-3 py-1.5 bg-blue-100 border border-blue-400 rounded-md text-xs font-semibold text-blue-800 transition-colors whitespace-nowrap" onclick="window.location.href='index.html'">&#9679; Case Opening</button>
  <button class="px-3 py-1.5 bg-purple-100 border border-purple-400 rounded-md text-xs font-semibold text-purple-800 transition-colors whitespace-nowrap" onclick="window.location.href='written-discovery.html'">&#9679; Written Discovery</button>
  <button class="px-3 py-1.5 bg-emerald-100 border border-emerald-400 rounded-md text-xs font-semibold text-emerald-800 transition-colors whitespace-nowrap" onclick="window.location.href='expert-deposition.html'">&#9679; Expert &amp; Deposition</button>
  <button class="px-3 py-1.5 bg-red-100 border border-red-400 rounded-md text-xs font-semibold text-red-800 transition-colors whitespace-nowrap" onclick="window.location.href='trial.html'">&#9679; Trial</button>
</div>
<!-- LEGEND -->
<div class="rounded-lg border border-border bg-card p-5 mb-8 flex flex-wrap gap-6">
  <div>
    <h4 class="text-[11px] font-bold uppercase tracking-wider text-muted-foreground mb-2">Roles</h4>
    <div class="flex flex-wrap gap-2">
      <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-blue-100 text-blue-700">Para / Legal Asst</span>
      <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-purple-100 text-purple-700">Attorney</span>
      <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-green-100 text-green-700">System Auto</span>
      <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-orange-100 text-orange-700">Management</span>
    </div>
  </div>
  <div>
    <h4 class="text-[11px] font-bold uppercase tracking-wider text-muted-foreground mb-2">Status</h4>
    <div class="flex flex-wrap gap-2">
      <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-red-100 text-red-700">Required</span>
      <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-yellow-100 text-yellow-700">C / NA / D</span>
      <span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-green-100 text-green-700">Auto</span>
    </div>
  </div>
</div>
'''

# ─── PART A ───
html += f'''<!-- ============================================================ PART A -->
<section class="mb-12" id="partA">
<div class="bg-primary text-primary-foreground px-6 py-4 rounded-t-lg mt-10">
  <h2 class="text-lg font-bold">Part A &mdash; Process Phases (1&ndash;4)</h2>
  <p class="text-sm text-primary-foreground/70 mt-0.5">Court Notices Through Mediation Track</p>
</div>

<!-- Phase 1: Court Notice & Calendaring -->
<div class="rounded-lg border border-border bg-card shadow-sm mb-4 overflow-hidden" id="ph1">
<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
  <h3 class="text-sm font-semibold text-foreground flex items-center gap-3"><span class="inline-flex items-center justify-center w-7 h-7 bg-[{ACCENT}] text-white rounded-full text-xs font-bold shrink-0">1</span> Court Notice &amp; Calendaring</h3>
  <div class="flex items-center gap-2 shrink-0">
    {badge("Para","para")} {badge("System","system")}
    <span class="text-xs font-semibold text-muted-foreground bg-secondary px-2 py-0.5 rounded">1 biz day / 1 hour</span>
    <svg data-chevron class="w-5 h-5 text-muted-foreground transition-transform shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
  </div>
</button>
<div data-card-body class="px-6 py-5 border-t border-border hidden">
  <div class="rounded-md border border-blue-200 bg-blue-50 p-4 text-sm text-blue-900 mb-4"><strong>Objective:</strong> Calendar arbitration notices and send automated client notifications within SLA windows.</div>
  <div class="rounded-md border border-border overflow-hidden overflow-x-auto">
  <table class="w-full text-sm">
    <thead>{table_header()}</thead>
    <tbody>
{task_row(1,"Calendar arbitration notice from the court","Court Notice Calendar","Once received, mark complete. Triggers SLA clock for all downstream tasks.",badge("Para","para"),badge("C/NA/D","cnad"),"1 business day from notice receipt")}
{task_row(2,"Arbitration notice to the client","Client Notice Automation","Choose location (virtual vs. in person), indicate if client must appear. System auto-sends letter/text/email.",badge("System","system"),badge("Auto","auto"),"1 hour from notice receipt")}
    </tbody>
  </table>
  </div>
  <div class="rounded-md border border-green-200 bg-green-50 p-4 text-sm text-green-900 mt-4"><strong>Exit Condition:</strong> Arbitration calendared, client notified &rarr; Case Prep begins.</div>
</div>
</div>

<!-- Phase 2: Case Prep & Statement -->
<div class="rounded-lg border border-border bg-card shadow-sm mb-4 overflow-hidden" id="ph2">
<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
  <h3 class="text-sm font-semibold text-foreground flex items-center gap-3"><span class="inline-flex items-center justify-center w-7 h-7 bg-[{ACCENT}] text-white rounded-full text-xs font-bold shrink-0">2</span> Case Prep &amp; Statement</h3>
  <div class="flex items-center gap-2 shrink-0">
    {badge("Para","para")} {badge("Atty","attorney")}
    <span class="text-xs font-semibold text-muted-foreground bg-secondary px-2 py-0.5 rounded">T-10 to T-5 biz days</span>
    <svg data-chevron class="w-5 h-5 text-muted-foreground transition-transform shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
  </div>
</button>
<div data-card-body class="px-6 py-5 border-t border-border hidden">
  <div class="rounded-md border border-blue-200 bg-blue-50 p-4 text-sm text-blue-900 mb-4"><strong>Objective:</strong> Verify all case artifacts, draft and approve arbitration statement, compile and send packet to arbitrator and defense counsel.</div>
  <div class="rounded-md border border-border overflow-hidden overflow-x-auto">
  <table class="w-full text-sm">
    <thead>{table_header()}</thead>
    <tbody>
{task_row(3,"Confirm all expert reports served, medical bills balance and lien balance","Case Prep Verification","File review, call/email to obtain updated bill balance and updated lien information. Verify all expert reports were served.",badge("Para","para"),badge("C/NA/D","cnad"),"1 hour from notice receipt")}
{task_row(4,"Draft arbitration statement to be sent to Atty for approval","Arb Statement Draft","Prepare arbitration statement and upload for attorney review. Draft must include all case facts, damages summary, and demand.",badge("Para","para"),badge("C/NA/D","cnad"),"4pm, 10 business days before arbitration")}
{task_row(5,"Review and approve arbitration statement or send back for edits","Attorney Review","Review and approve arbitration statement, mark complete, or mark edits needed for the paralegal to be notified.",badge("Atty","attorney"),badge("C/NA/D","cnad"),"4pm, 6 business days before arbitration")}
{task_row(6,"Compile arbitration packet and send to arbitrator","Packet Compilation","Compile arbitration packet and send to arbitrator and defense counsel. Log proof of service.",badge("Para","para"),badge("Required","required"),"4pm, 5 business days before arbitration")}
    </tbody>
  </table>
  </div>
  <div class="rounded-md border border-green-200 bg-green-50 p-4 text-sm text-green-900 mt-4"><strong>Exit Condition:</strong> Statement approved, packet sent &rarr; Arbitration proceeds.</div>
</div>
</div>

<!-- Phase 3: De Novo Management -->
<div class="rounded-lg border border-border bg-card shadow-sm mb-4 overflow-hidden" id="ph3">
<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
  <h3 class="text-sm font-semibold text-foreground flex items-center gap-3"><span class="inline-flex items-center justify-center w-7 h-7 bg-[{ACCENT}] text-white rounded-full text-xs font-bold shrink-0">3</span> De Novo Management</h3>
  <div class="flex items-center gap-2 shrink-0">
    {badge("Para","para")} {badge("Atty","attorney")} {badge("System","system")}
    <span class="text-xs font-semibold text-muted-foreground bg-secondary px-2 py-0.5 rounded">24 hrs &rarr; Day 9</span>
    <svg data-chevron class="w-5 h-5 text-muted-foreground transition-transform shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
  </div>
</button>
<div data-card-body class="px-6 py-5 border-t border-border hidden">
  <div class="rounded-md border border-blue-200 bg-blue-50 p-4 text-sm text-blue-900 mb-4"><strong>Objective:</strong> Secure attorney direction on Demand for Trial De Novo within the 30-day statutory window through escalating contact attempts.</div>
  <div class="rounded-md border border-border overflow-hidden overflow-x-auto">
  <table class="w-full text-sm">
    <thead>{table_header()}</thead>
    <tbody>
{task_row(7,"Requesting direction on Demand for Trial De Novo &mdash; Attempt 1","De Novo Attempt 1","Request direction from attorney on Demand for Trial De Novo. If no direction, mark &ldquo;Attempt Complete&rdquo; to start next attempt clock.",badge("Para","para"),badge("Required","required"),"24 hours after arbitration hearing")}
{task_row(8,"Requesting direction on Demand for Trial De Novo &mdash; Attempt 2","De Novo Attempt 2","Second request for attorney direction. Escalation path begins if no response.",badge("Para","para"),badge("Required","required"),"72 hours after arbitration hearing")}
{task_row(9,"Requesting direction on Demand for Trial De Novo &mdash; Attempt 3","De Novo Attempt 3","Final paralegal attempt before system escalation. Must be completed by end of Day 5.",badge("Para","para"),badge("Required","required"),"4pm, Day 5 after arbitration hearing")}
{task_row(10,"Escalate untimely filing of De Novo to Director of PI","System Escalation","Automated escalation to Director of PI when attorney direction has not been received by Day 7.",badge("System","system"),badge("Required","required"),"4pm, Day 7 after arbitration hearing")}
{task_row(11,"Gives direction on Demand for Trial De Novo","Attorney Direction","Attorney provides direction: File De Novo, Diary for confirmation, or NA. If not complete, automated notification to team lead and Director of PI.",badge("Atty","attorney"),badge("Required","required"),"4pm, Day 9 after arbitration hearing")}
{task_row(12,"Draft and file Demand for Trial De Novo, or diary to confirm award on Day 30","De Novo Filing","Draft the Demand for Trial De Novo and file with court, or diary to confirm the arbitration award on the 30th day. Schedule follow-up for confirmation.",badge("Para","para"),badge("Required","required"),"3 hours from attorney direction")}
    </tbody>
  </table>
  </div>
  <div class="rounded-md border border-green-200 bg-green-50 p-4 text-sm text-green-900 mt-4"><strong>Exit Condition:</strong> De Novo filed with court, or arbitration award diaried for confirmation on Day 30.</div>
</div>
</div>

<!-- Phase 4: Mediation Track -->
<div class="rounded-lg border border-border bg-card shadow-sm mb-4 overflow-hidden" id="ph4">
<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
  <h3 class="text-sm font-semibold text-foreground flex items-center gap-3"><span class="inline-flex items-center justify-center w-7 h-7 bg-[{ACCENT}] text-white rounded-full text-xs font-bold shrink-0">4</span> Mediation Track</h3>
  <div class="flex items-center gap-2 shrink-0">
    {badge("Para","para")} {badge("Atty","attorney")} {badge("System","system")}
    <span class="text-xs font-semibold text-muted-foreground bg-secondary px-2 py-0.5 rounded">T-14 to T-5 biz days</span>
    <svg data-chevron class="w-5 h-5 text-muted-foreground transition-transform shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
  </div>
</button>
<div data-card-body class="px-6 py-5 border-t border-border hidden">
  <div class="rounded-md border border-blue-200 bg-blue-50 p-4 text-sm text-blue-900 mb-4"><strong>Objective:</strong> If mediation is directed, calendar the date, notify client, draft and approve mediation statement, and send packet.</div>
  <div class="rounded-md border border-border overflow-hidden overflow-x-auto">
  <table class="w-full text-sm">
    <thead>{table_header()}</thead>
    <tbody>
{task_row(13,"Get direction on mediation prep","Mediation Directive","If mediation is to be set, mark approved. If not happening, mark NA. If needed to postpone, set date for next reminder.",badge("Para","para"),badge("C/NA/D","cnad"),"1 business day from arbitration notice receipt")}
{task_row(14,"Calendar mediation date","Mediation Calendar","Calendar mediation date in the Litify calendar, mark complete.",badge("Para","para"),badge("C/NA/D","cnad"),"1 hour from attorney directive")}
{task_row(15,"Mediation notice to the client","Client Notice","System automatically sends letter/text/email to client with mediation notice upon directive confirmation.",badge("System","system"),badge("Auto","auto"),"Immediately upon mediation directive")}
{task_row(16,"Draft mediation statement to be sent to Atty for approval","Med Statement Draft","Prepare mediation statement and upload for attorney review and final edits.",badge("Para","para"),badge("C/NA/D","cnad"),"4pm, 2 weeks before mediation")}
{task_row(17,"Review and approve mediation statement or send back for edits","Attorney Review","Review and approve mediation statement, mark complete, or mark edits needed for the paralegal to be notified.",badge("Atty","attorney"),badge("C/NA/D","cnad"),"4pm, 6 business days before mediation")}
{task_row(18,"Compile mediation packet and send to mediator","Packet Send","Compile mediation packet and send to mediator and defense counsel. Log proof of service.",badge("Para","para"),badge("C/NA/D","cnad"),"4pm, 5 business days before mediation")}
    </tbody>
  </table>
  </div>
  <div class="rounded-md border border-green-200 bg-green-50 p-4 text-sm text-green-900 mt-4"><strong>Exit Condition:</strong> Mediation statement approved, packet sent &rarr; Mediation proceeds.</div>
</div>
</div>

</section>
'''

# ─── PART B: SCORING PACK ───
def scoring_card(num, sid, title, content_html):
    return f'''<div class="rounded-lg border border-border bg-card shadow-sm mb-4 overflow-hidden" id="{sid}">
<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
  <h3 class="text-sm font-semibold text-foreground flex items-center gap-3"><span class="inline-flex items-center justify-center w-7 h-7 bg-[{ACCENT}] text-white rounded-full text-xs font-bold shrink-0">{num}</span> {title}</h3>
  <svg data-chevron class="w-5 h-5 text-muted-foreground transition-transform shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
</button>
<div data-card-body class="px-6 py-5 border-t border-border hidden">
{content_html}
</div>
</div>
'''

def factor_table(factors, scale_label="Scale"):
    rows = ''.join(f'<tr class="border-b border-border last:border-b-0"><td class="px-4 py-2 text-sm text-foreground">{f[0]}</td><td class="px-4 py-2 text-sm text-muted-foreground">{f[1]}</td></tr>' for f in factors)
    return f'''<div class="rounded-md border border-border overflow-hidden overflow-x-auto my-3">
<table class="w-full text-sm"><thead><tr class="border-b border-border bg-muted"><th class="px-4 py-2 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">Factor</th><th class="px-4 py-2 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">{scale_label}</th></tr></thead><tbody>{rows}</tbody></table></div>'''

def band_badges(bands):
    colors = {'green':'bg-green-100 text-green-800','yellow':'bg-yellow-100 text-yellow-800','red':'bg-red-100 text-red-800'}
    return '<div class="flex flex-wrap gap-2 mt-3">' + ''.join(f'<span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold {colors[b[0]]}">{b[1]}: {b[2]}</span>' for b in bands) + '</div>'

html += '''<!-- ============================================================ PART B -->
<section class="mb-12" id="partB">
<div class="bg-primary text-primary-foreground px-6 py-4 rounded-t-lg mt-10">
  <h2 class="text-lg font-bold">Part B &mdash; Post-Arbitration Scoring Pack</h2>
  <p class="text-sm text-primary-foreground/70 mt-0.5">Attorney Scoring &mdash; Complete Within 24 Hours After Arbitration (5&ndash;8 minutes)</p>
</div>

'''

# TPI
html += scoring_card(1, 'tpi', 'Trial Probability Index (TPI) &mdash; 0 to 100',
    '<p class="text-sm text-foreground mb-2"><strong>Purpose:</strong> How likely is this case to reach trial?</p>'
    '<p class="text-sm text-muted-foreground mb-2">Rate each factor 0&ndash;20 (higher = more likely to go to trial):</p>'
    + factor_table([
        ('Defense rigidity (entrenched vs. moving)','0&ndash;20'),
        ('Authority gap (offer far below reasonable value vs. close)','0&ndash;20'),
        ('Liability dispute intensity (conceded vs. hard fight)','0&ndash;20'),
        ('Damages dispute intensity (minor gap vs. major causation/value fight)','0&ndash;20'),
        ('Venue / judge settlement pressure (settlement-driven vs. trial-prone)','0&ndash;20'),
    ])
    + '<div class="rounded-md bg-muted p-3 text-sm font-mono mt-3">TPI = sum of all factors (0&ndash;100)</div>'
    + band_badges([('green','0&ndash;30','Likely to settle'),('yellow','31&ndash;60','Uncertain / leverage window'),('red','61&ndash;100','High probability of trial')])
)

# WEV
html += scoring_card(2, 'wev', 'Verdict Range + Weighted Expected Verdict (WEV)',
    '<p class="text-sm text-foreground mb-2"><strong>Purpose:</strong> Provide a rational verdict forecast (not one number).</p>'
    '<p class="text-sm text-muted-foreground mb-3">Attorney enters three estimates:</p>'
    '<div class="flex gap-4 mb-3">'
    '<div class="flex-1 rounded-md border border-border p-3 text-center"><div class="text-xs text-muted-foreground uppercase">Low</div><div class="text-lg font-bold text-foreground">$___</div></div>'
    '<div class="flex-1 rounded-md border border-border p-3 text-center"><div class="text-xs text-muted-foreground uppercase">Most Likely</div><div class="text-lg font-bold text-foreground">$___</div></div>'
    '<div class="flex-1 rounded-md border border-border p-3 text-center"><div class="text-xs text-muted-foreground uppercase">High</div><div class="text-lg font-bold text-foreground">$___</div></div>'
    '</div>'
    '<div class="rounded-md bg-muted p-3 text-sm font-mono">WEV = (0.25 &times; Low) + (0.50 &times; Most Likely) + (0.25 &times; High)</div>'
)

# TSS
html += scoring_card(3, 'tss', 'Trial Strength Score (TSS) &mdash; 0 to 100',
    '<p class="text-sm text-foreground mb-2"><strong>Purpose:</strong> How strong is the case at trial on its merits?</p>'
    '<p class="text-sm text-muted-foreground mb-2">Rate each factor 0&ndash;10 (higher = stronger):</p>'
    + factor_table([
        ('Liability confidence','0&ndash;10'),
        ('Plaintiff credibility','0&ndash;10'),
        ('Witness support / corroboration','0&ndash;10'),
        ('Medical proof strength (objective + causation)','0&ndash;10'),
        ('Expert strength / readiness','0&ndash;10'),
        ('Defense impeachment exposure <em>(reverse: 10 = low exposure)</em>','0&ndash;10'),
        ('Theme clarity (jury story)','0&ndash;10'),
        ('Venue fit (how this injury/liability plays)','0&ndash;10'),
    ])
    + '<div class="rounded-md bg-muted p-3 text-sm font-mono mt-3">TSS = average of all factors &times; 10 (0&ndash;100)</div>'
)

# ATV
html += scoring_card(4, 'atv', 'Adjusted Trial Value (ATV)',
    '<p class="text-sm text-foreground mb-2"><strong>Purpose:</strong> The realistic economic value after adjusting for trial strength.</p>'
    '<div class="rounded-md bg-muted p-3 text-sm font-mono my-3">ATV = WEV &times; (TSS / 100)</div>'
    '<p class="text-sm text-muted-foreground">This is the number leadership can use for rational capital decisions.</p>'
)

# SLS
html += scoring_card(5, 'sls', 'Settlement Leverage Shift Score (SLS) &mdash; 0 to 20',
    '<p class="text-sm text-foreground mb-2"><strong>Purpose:</strong> Did arbitration improve or weaken our settlement leverage?</p>'
    '<p class="text-sm text-muted-foreground mb-2">Rate each factor 0&ndash;4:</p>'
    + factor_table([
        ('Defense offer movement meaningfully increased','0&ndash;4'),
        ('Neutral feedback favored plaintiff posture','0&ndash;4'),
        ('Defense revealed vulnerability or constraint','0&ndash;4'),
        ('Plaintiff presentation strengthened bargaining position','0&ndash;4'),
        ('Defense signaled trial readiness <em>(reverse: 4 = no)</em>','0&ndash;4'),
    ])
    + '<div class="rounded-md bg-muted p-3 text-sm font-mono mt-3">SLS = sum of all factors (0&ndash;20)</div>'
    + band_badges([('red','0&ndash;8','Leverage decreased'),('yellow','9&ndash;14','Neutral'),('green','15&ndash;20','Leverage increased')])
)

# CTT
html += scoring_card(6, 'ctt', 'Cost-to-Try Projection (CTT)',
    '<p class="text-sm text-foreground mb-2"><strong>Purpose:</strong> Know what it costs to get to verdict.</p>'
    '<p class="text-sm text-muted-foreground mb-3">Attorney enters estimates for:</p>'
    '<ul class="list-disc pl-5 text-sm text-foreground space-y-1 mb-3">'
    '<li>Remaining expert costs</li>'
    '<li>Depositions remaining + expected cost</li>'
    '<li>Trial prep time (hours)</li>'
    '<li>Expected trial length (days)</li>'
    '<li>Other hard costs (travel, exhibits, etc.)</li>'
    '</ul>'
    '<div class="rounded-md bg-muted p-3 text-sm font-mono my-3">CTT = total projected cost-to-go</div>'
    '<h4 class="text-sm font-semibold text-foreground mt-4 mb-2">CTT Ratio</h4>'
    '<div class="rounded-md bg-muted p-3 text-sm font-mono mb-3">CTT Ratio = CTT / ATV</div>'
    + band_badges([('green','&lt;10%','Strong economics'),('yellow','10&ndash;20%','Watch'),('red','&gt;20%','Expensive risk posture')])
)

# TRS
html += scoring_card(7, 'trs', 'Trial Readiness Score (TRS) &mdash; 0 to 20',
    '<p class="text-sm text-foreground mb-2"><strong>Purpose:</strong> Are we actually ready to try this case?</p>'
    '<p class="text-sm text-muted-foreground mb-2">Rate each factor 0&ndash;4:</p>'
    + factor_table([
        ('Discovery completeness','0&ndash;4'),
        ('Experts retained + ready','0&ndash;4'),
        ('Motions posture ready (key motions identified/queued)','0&ndash;4'),
        ('Witness prep plan defined','0&ndash;4'),
        ('Trial plan / outline reasonably formed','0&ndash;4'),
    ])
    + '<div class="rounded-md bg-muted p-3 text-sm font-mono mt-3">TRS = sum of all factors (0&ndash;20)</div>'
    + band_badges([('red','0&ndash;8','Not ready'),('yellow','9&ndash;14','Developing'),('green','15&ndash;20','Ready')])
)

# ERI
html += scoring_card(8, 'eri', 'Economic Risk Index (ERI) &mdash; 0 to 100',
    '<p class="text-sm text-foreground mb-2"><strong>Purpose:</strong> One number showing whether trying this case is economically smart.</p>'
    '<p class="text-sm text-muted-foreground mb-3">Weighted roll-up:</p>'
    + factor_table([
        ('TPI (trial probability)','40%'),
        ('CTT Ratio score (higher ratio = higher risk)','30%'),
        ('Collectability certainty (0&ndash;100)','15%'),
        ('Venue volatility (0&ndash;100)','15%'),
    ], scale_label="Weight")
    + '<div class="rounded-md bg-muted p-3 text-sm font-mono mt-3">ERI = weighted sum (0&ndash;100)</div>'
    + band_badges([('green','0&ndash;40','Economically favorable'),('yellow','41&ndash;70','Leadership decision required'),('red','71&ndash;100','High economic risk')])
)

# CCS
html += scoring_card(9, 'ccs', 'Confidence Calibration Score (CCS) &mdash; 1 to 5',
    '<p class="text-sm text-foreground mb-2"><strong>Purpose:</strong> Forces the attorney to disclose how confident they are in the forecast.</p>'
    '<div class="space-y-2 my-3">'
    '<div class="flex items-center gap-3 p-2 rounded-md border border-border"><span class="inline-flex items-center justify-center w-6 h-6 bg-red-100 text-red-800 rounded-full text-xs font-bold">1</span><span class="text-sm">Low confidence &mdash; major unknowns, forecast is a rough range</span></div>'
    '<div class="flex items-center gap-3 p-2 rounded-md border border-border"><span class="inline-flex items-center justify-center w-6 h-6 bg-orange-100 text-orange-800 rounded-full text-xs font-bold">2</span><span class="text-sm">Some confidence &mdash; several assumptions remain</span></div>'
    '<div class="flex items-center gap-3 p-2 rounded-md border border-border"><span class="inline-flex items-center justify-center w-6 h-6 bg-yellow-100 text-yellow-800 rounded-full text-xs font-bold">3</span><span class="text-sm">Moderate confidence &mdash; good visibility, normal uncertainty</span></div>'
    '<div class="flex items-center gap-3 p-2 rounded-md border border-border"><span class="inline-flex items-center justify-center w-6 h-6 bg-green-100 text-green-800 rounded-full text-xs font-bold">4</span><span class="text-sm">High confidence &mdash; facts mature, posture clear</span></div>'
    '<div class="flex items-center gap-3 p-2 rounded-md border border-border"><span class="inline-flex items-center justify-center w-6 h-6 bg-emerald-100 text-emerald-800 rounded-full text-xs font-bold">5</span><span class="text-sm">Very high confidence &mdash; strong predictability; minimal unknowns</span></div>'
    '</div>'
    '<div class="rounded-md border border-amber-200 bg-amber-50 p-3 text-sm text-amber-900"><strong>Required note when 1&ndash;2:</strong> &ldquo;What is the biggest unknown driving low confidence?&rdquo; (one sentence)</div>'
)

# Leadership Dashboard
html += f'''<div class="rounded-lg border border-border bg-card shadow-sm mb-4 overflow-hidden" id="leadership-dash">
<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
  <h3 class="text-sm font-semibold text-foreground flex items-center gap-3"><span class="inline-flex items-center justify-center w-7 h-7 bg-[{ACCENT}] text-white rounded-full text-xs font-bold shrink-0">&#9733;</span> Leadership Dashboard Output</h3>
  <svg data-chevron class="w-5 h-5 text-muted-foreground transition-transform shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
</button>
<div data-card-body class="px-6 py-5 border-t border-border hidden">
  <p class="text-sm text-muted-foreground mb-4">After the attorney submits the scoring pack, leadership sees:</p>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
    <div class="rounded-md border border-border p-3"><span class="text-xs font-bold uppercase text-muted-foreground">Trial Probability</span><p class="text-sm mt-1">TPI band + score (0&ndash;100)</p></div>
    <div class="rounded-md border border-border p-3"><span class="text-xs font-bold uppercase text-muted-foreground">Verdict Range</span><p class="text-sm mt-1">Low / Likely / High + WEV</p></div>
    <div class="rounded-md border border-border p-3"><span class="text-xs font-bold uppercase text-muted-foreground">Adjusted Trial Value</span><p class="text-sm mt-1">ATV = WEV &times; (TSS/100)</p></div>
    <div class="rounded-md border border-border p-3"><span class="text-xs font-bold uppercase text-muted-foreground">Cost-to-Try</span><p class="text-sm mt-1">CTT + CTT Ratio band</p></div>
    <div class="rounded-md border border-border p-3"><span class="text-xs font-bold uppercase text-muted-foreground">Economic Risk</span><p class="text-sm mt-1">ERI band (0&ndash;100)</p></div>
    <div class="rounded-md border border-border p-3"><span class="text-xs font-bold uppercase text-muted-foreground">Settlement Leverage</span><p class="text-sm mt-1">SLS band (0&ndash;20)</p></div>
    <div class="rounded-md border border-border p-3"><span class="text-xs font-bold uppercase text-muted-foreground">Trial Readiness</span><p class="text-sm mt-1">TRS band (0&ndash;20)</p></div>
    <div class="rounded-md border border-border p-3"><span class="text-xs font-bold uppercase text-muted-foreground">Confidence</span><p class="text-sm mt-1">CCS (1&ndash;5) + note if low</p></div>
  </div>
</div>
</div>

</section>
'''

# ─── PART C: METRICS ───
html += '''<!-- ============================================================ PART C -->
<section class="mb-12" id="partC">
<div class="bg-primary text-primary-foreground px-6 py-4 rounded-t-lg mt-10">
  <h2 class="text-lg font-bold">Part C &mdash; Metrics &amp; KPIs</h2>
  <p class="text-sm text-primary-foreground/70 mt-0.5">Arbitration/Mediation Stage Scorecard</p>
</div>

<div class="rounded-md border border-border bg-card p-5 mb-6">
  <h4 class="text-sm font-semibold text-foreground mb-2">Stage Health Score (0&ndash;100)</h4>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
    <div class="rounded-md bg-muted p-3 text-center"><div class="text-lg font-bold text-foreground">40</div><div class="text-[11px] text-muted-foreground">SLA &amp; Timeliness</div></div>
    <div class="rounded-md bg-muted p-3 text-center"><div class="text-lg font-bold text-foreground">25</div><div class="text-[11px] text-muted-foreground">Readiness &amp; Coverage</div></div>
    <div class="rounded-md bg-muted p-3 text-center"><div class="text-lg font-bold text-foreground">20</div><div class="text-[11px] text-muted-foreground">Decision Latency</div></div>
    <div class="rounded-md bg-muted p-3 text-center"><div class="text-lg font-bold text-foreground">15</div><div class="text-[11px] text-muted-foreground">Quality &amp; Rework</div></div>
  </div>
</div>

'''

# SLA & Timeliness
html += f'''<div class="rounded-lg border border-border bg-card shadow-sm mb-4 overflow-hidden" id="metrics-sla">
<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
  <h3 class="text-sm font-semibold text-foreground">A) SLA &amp; Timeliness (40 pts)</h3>
  <svg data-chevron class="w-5 h-5 text-muted-foreground transition-transform shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
</button>
<div data-card-body class="px-6 py-5 border-t border-border hidden">
  <div class="rounded-md border border-border overflow-hidden overflow-x-auto">
  <table class="w-full text-sm">
    <thead>{kpi_table_header()}</thead>
    <tbody>
{kpi_row(1,"On-Time Completion Rate (All Stage SLAs)","Stage Owner","Per task","&ge;90%","80&ndash;89%","&lt;80%")}
{kpi_row(2,"Court Notice &rarr; Calendar Timeliness","Para/Legal Asst","1 biz day","&ge;95%","90&ndash;94%","&lt;90%")}
{kpi_row(3,"Client Notice Automation Speed","Automation Owner","1 hour","&ge;98%","95&ndash;97%","&lt;95%")}
{kpi_row(4,"Case Prep 1-Hour Readiness Check","Para/Legal Asst","1 hour","&ge;90%","80&ndash;89%","&lt;80%")}
{kpi_row(5,"Arb Statement Draft On-Time","Para/Legal Asst","T-10 biz days","&ge;92%","85&ndash;91%","&lt;85%")}
{kpi_row(6,"Attorney Review/Approval On-Time","Attorney","T-6 biz days","&ge;90%","80&ndash;89%","&lt;80%")}
{kpi_row(7,"Packet Sent On-Time","Para/Legal Asst","T-5 biz days","&ge;95%","90&ndash;94%","&lt;90%")}
    </tbody>
  </table>
  </div>
</div>
</div>

'''

# Readiness & Coverage
html += f'''<div class="rounded-lg border border-border bg-card shadow-sm mb-4 overflow-hidden" id="metrics-readiness">
<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
  <h3 class="text-sm font-semibold text-foreground">B) Readiness &amp; Coverage (25 pts)</h3>
  <svg data-chevron class="w-5 h-5 text-muted-foreground transition-transform shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
</button>
<div data-card-body class="px-6 py-5 border-t border-border hidden">
  <div class="rounded-md border border-border overflow-hidden overflow-x-auto">
  <table class="w-full text-sm">
    <thead>{kpi_table_header()}</thead>
    <tbody>
{kpi_row(8,"Next-Action Coverage %","Para Lead","7 days","&ge;95%","90&ndash;94%","&lt;90%")}
{kpi_row(9,"Packet-Ready Coverage (Hard Gate)","Para Lead","T-5 biz days","&ge;90%","80&ndash;89%","&lt;80%")}
{kpi_row(10,"Missing Critical Artifact Count","Team Lead","&mdash;","&le;10","11&ndash;25","&gt;25")}
{kpi_row(11,"Upcoming Event Exposure (Unready &le;10 Biz Days)","Director Lit Ops","10 biz days","&le;5","6&ndash;15","&gt;15")}
    </tbody>
  </table>
  </div>
</div>
</div>

'''

# Decision Latency / De Novo
html += f'''<div class="rounded-lg border border-border bg-card shadow-sm mb-4 overflow-hidden" id="metrics-denovo">
<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
  <h3 class="text-sm font-semibold text-foreground">C) Decision Latency / De Novo Control (20 pts)</h3>
  <svg data-chevron class="w-5 h-5 text-muted-foreground transition-transform shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
</button>
<div data-card-body class="px-6 py-5 border-t border-border hidden">
  <div class="rounded-md border border-border overflow-hidden overflow-x-auto">
  <table class="w-full text-sm">
    <thead>{kpi_table_header()}</thead>
    <tbody>
{kpi_row(12,"De Novo Direction Latency (Median Hours)","Atty + Team Lead","&mdash;","&le;72 hrs","73&ndash;120 hrs","&gt;120 hrs")}
{kpi_row("13a","De Novo Direction by Attempt 1","Team Lead","24 hrs","&ge;60%","45&ndash;59%","&lt;45%")}
{kpi_row("13b","De Novo Direction by Attempt 3","Team Lead","Day 5","&ge;90%","80&ndash;89%","&lt;80%")}
{kpi_row(14,"Escalation Trigger Count","Director PI + Ops","Day 7","&le;2%","2&ndash;5%","&gt;5%")}
{kpi_row(15,"De Novo Filing Timeliness","Para/Legal Asst","3 hours","&ge;95%","90&ndash;94%","&lt;90%")}
{kpi_row(16,"Day 9 @ 4pm Breach Count (Critical)","Director PI","Day 9","0","1&ndash;2","&ge;3")}
    </tbody>
  </table>
  </div>
</div>
</div>

'''

# Quality & Rework
html += f'''<div class="rounded-lg border border-border bg-card shadow-sm mb-4 overflow-hidden" id="metrics-quality">
<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
  <h3 class="text-sm font-semibold text-foreground">D) Quality &amp; Rework (15 pts)</h3>
  <svg data-chevron class="w-5 h-5 text-muted-foreground transition-transform shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
</button>
<div data-card-body class="px-6 py-5 border-t border-border hidden">
  <div class="rounded-md border border-border overflow-hidden overflow-x-auto">
  <table class="w-full text-sm">
    <thead>{kpi_table_header()}</thead>
    <tbody>
{kpi_row(17,"Statement Rework Rate","Para Lead","&mdash;","&le;15%","16&ndash;25%","&gt;25%")}
{kpi_row(18,"Packet Defect Rate","Para Lead","&mdash;","&le;3%","4&ndash;6%","&gt;6%")}
{kpi_row(19,"Automation Failure Rate","Litify Admin","&mdash;","&le;1%","1&ndash;3%","&gt;3%")}
    </tbody>
  </table>
  </div>
</div>
</div>

'''

# Dashboard Views
html += '''<div class="rounded-lg border border-border bg-card shadow-sm mb-4 overflow-hidden" id="metrics-dashboard">
<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
  <h3 class="text-sm font-semibold text-foreground">E) Daily/Weekly Dashboard Views</h3>
  <svg data-chevron class="w-5 h-5 text-muted-foreground transition-transform shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
</button>
<div data-card-body class="px-6 py-5 border-t border-border hidden">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h4 class="text-sm font-semibold text-foreground mb-3">Daily &ldquo;Control Panel&rdquo;</h4>
      <ul class="list-disc pl-5 text-sm text-foreground space-y-1">
        <li>Events in next 10 business days (arb/med) with readiness status</li>
        <li>Overdue SLA tasks (sorted by time past due)</li>
        <li>De Novo clock cases (Day 1/3/5/7/9 buckets)</li>
        <li>Missing critical artifact list</li>
      </ul>
    </div>
    <div>
      <h4 class="text-sm font-semibold text-foreground mb-3">Weekly &ldquo;Leadership Summary&rdquo;</h4>
      <ul class="list-disc pl-5 text-sm text-foreground space-y-1">
        <li>On-time completion rate (trend)</li>
        <li>Packet-ready coverage (trend)</li>
        <li>De Novo direction latency (median + 90th percentile)</li>
        <li>Escalation triggers (% and count)</li>
        <li>Rework / defect rates</li>
      </ul>
    </div>
  </div>
</div>
</div>

'''

# Hard Gates
html += '''<div class="rounded-lg border border-border bg-card shadow-sm mb-4 overflow-hidden" id="metrics-gates">
<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
  <h3 class="text-sm font-semibold text-foreground">F) Hard Gates (Non-Negotiable)</h3>
  <svg data-chevron class="w-5 h-5 text-muted-foreground transition-transform shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
</button>
<div data-card-body class="px-6 py-5 border-t border-border hidden">
  <div class="rounded-md border border-red-200 bg-red-50 p-4 text-sm text-red-900 mb-3"><strong>Gate 1:</strong> Cannot mark &ldquo;Ready for Arbitration/Mediation&rdquo; unless &ldquo;Packet-Ready Coverage = Yes.&rdquo;</div>
  <div class="rounded-md border border-red-200 bg-red-50 p-4 text-sm text-red-900"><strong>Gate 2:</strong> Post-hearing: cannot exit the arbitration workflow without a De Novo disposition logged (File / Diary / NA / Defendant filed).</div>
</div>
</div>

</section>
'''

# ─── PART D: DEV SPEC ───
html += f'''<!-- ============================================================ PART D -->
<section class="mb-12" id="partD">
<div class="bg-primary text-primary-foreground px-6 py-4 rounded-t-lg mt-10">
  <h2 class="text-lg font-bold">Part D &mdash; Dev Spec</h2>
  <p class="text-sm text-primary-foreground/70 mt-0.5">Litify Fields, Flows &amp; Validation Rules</p>
</div>

<div class="rounded-lg border border-border bg-card p-5 mb-4">
  <div class="flex gap-2 mb-4 border-b border-border pb-3">
    <button class="tab-btn px-4 py-2 text-sm font-medium rounded-md bg-card text-foreground shadow-sm" onclick="setTab('tab-fields', this)">Litify Fields</button>
    <button class="tab-btn px-4 py-2 text-sm font-medium rounded-md text-muted-foreground hover:text-foreground transition-colors" onclick="setTab('tab-flows', this)">Flows</button>
    <button class="tab-btn px-4 py-2 text-sm font-medium rounded-md text-muted-foreground hover:text-foreground transition-colors" onclick="setTab('tab-rules', this)">Validation Rules</button>
  </div>

  <!-- Fields Tab -->
  <div id="tab-fields" class="tab-pane active">
    <div class="rounded-md border border-border overflow-hidden overflow-x-auto">
    <table class="w-full text-sm">
      <thead>{field_table_header()}</thead>
      <tbody>
{field_row("BJB__Arb_Court_Notice_Date__c","Arb Court Notice Date","Date","Matter","SLA clock start")}
{field_row("BJB__Arb_Calendar_Date__c","Arbitration Date","Date","Matter","Event date")}
{field_row("BJB__Arb_Statement_Status__c","Statement Status","Picklist","Matter","Draft/Approved/Edits Needed")}
{field_row("BJB__Arb_Packet_Sent__c","Packet Sent","Checkbox","Matter","Packet-Ready gate")}
{field_row("BJB__DeNovo_Direction__c","De Novo Direction","Picklist","Matter","File/Diary/NA/Def Filed")}
{field_row("BJB__DeNovo_Direction_Date__c","Direction Date","DateTime","Matter","Latency measurement")}
{field_row("BJB__DeNovo_Attempt_Count__c","Attempt Count","Number","Matter","Tracks 1/2/3 attempts")}
{field_row("BJB__DeNovo_Filed_Date__c","De Novo Filed Date","Date","Matter","Filing timeliness")}
{field_row("BJB__Med_Directive__c","Mediation Directive","Picklist","Matter","Approved/NA/Postpone")}
{field_row("BJB__Med_Calendar_Date__c","Mediation Date","Date","Matter","Event date")}
{field_row("BJB__Med_Statement_Status__c","Med Statement Status","Picklist","Matter","Draft/Approved/Edits")}
{field_row("BJB__Med_Packet_Sent__c","Med Packet Sent","Checkbox","Matter","Packet gate")}
{field_row("BJB__TPI_Score__c","Trial Probability Index","Number(3,0)","Matter","0&ndash;100")}
{field_row("BJB__WEV__c","Weighted Expected Verdict","Currency","Matter","Calculated")}
{field_row("BJB__TSS_Score__c","Trial Strength Score","Number(3,0)","Matter","0&ndash;100")}
{field_row("BJB__ATV__c","Adjusted Trial Value","Currency","Matter","WEV &times; (TSS/100)")}
{field_row("BJB__SLS_Score__c","Settlement Leverage Shift","Number(2,0)","Matter","0&ndash;20")}
{field_row("BJB__CTT__c","Cost-to-Try","Currency","Matter","Total projected")}
{field_row("BJB__CTT_Ratio__c","CTT Ratio","Percent","Matter","CTT/ATV")}
{field_row("BJB__TRS_Score__c","Trial Readiness Score","Number(2,0)","Matter","0&ndash;20")}
{field_row("BJB__ERI_Score__c","Economic Risk Index","Number(3,0)","Matter","0&ndash;100")}
{field_row("BJB__CCS_Score__c","Confidence Calibration","Number(1,0)","Matter","1&ndash;5")}
      </tbody>
    </table>
    </div>
  </div>

  <!-- Flows Tab -->
  <div id="tab-flows" class="tab-pane" style="display:none">
    <div class="rounded-md border border-border overflow-hidden overflow-x-auto">
    <table class="w-full text-sm">
      <thead>{flow_table_header()}</thead>
      <tbody>
{flow_row("Arb Client Notice Auto-Send","Record-Triggered","Court notice date populated","Send letter/text/email to client")}
{flow_row("Med Client Notice Auto-Send","Record-Triggered","Med directive = Approved","Send letter/text/email to client")}
{flow_row("De Novo Escalation Clock","Scheduled","Daily @ 4pm","Check Day 7 cases &rarr; escalate to Director")}
{flow_row("De Novo Attempt Reminder","Record-Triggered","Attempt count changes","Notify attorney at each attempt window")}
{flow_row("Scoring Pack Reminder","Record-Triggered","Arb date = today","Notify attorney to complete scoring within 24 hrs")}
{flow_row("Packet-Ready Validation","Before Save","Stage = Ready for Arb/Med","Validate all components complete")}
      </tbody>
    </table>
    </div>
  </div>

  <!-- Validation Rules Tab -->
  <div id="tab-rules" class="tab-pane" style="display:none">
    <div class="rounded-md border border-border overflow-hidden overflow-x-auto">
    <table class="w-full text-sm">
      <thead>{rule_table_header()}</thead>
      <tbody>
{rule_row("Require_Court_Notice_Date","Matter","Arb date populated AND court notice date blank","Court notice date required before arbitration date")}
{rule_row("Require_Packet_Ready","Matter","Stage = Ready AND packet not sent","Cannot mark ready until packet sent")}
{rule_row("Require_DeNovo_Disposition","Matter","Exiting arb workflow AND De Novo direction blank","De Novo disposition required")}
{rule_row("Require_Scoring_Pack","Matter","48 hrs post-arb AND any scoring field blank","Scoring pack must be completed within 24 hours")}
      </tbody>
    </table>
    </div>
  </div>
</div>
</section>
'''

# ─── APPROVAL ───
html += f'''<!-- ============================================================ APPROVAL -->
<section class="mb-12" id="approval">
<div class="bg-primary text-primary-foreground px-6 py-4 rounded-t-lg mt-10">
  <h2 class="text-lg font-bold">Approval &amp; Notes</h2>
  <p class="text-sm text-primary-foreground/70 mt-0.5">Management Sign-Off and Session Notes</p>
</div>

<div class="rounded-lg border-2 border-border bg-card p-6 mt-4">
  <h3 class="text-base font-bold text-foreground mb-1">Management Approval Checklist</h3>
  <p class="text-sm text-muted-foreground mb-4">Approved by Ryan Broderick</p>
  <div id="sync-status" class="text-[11px] text-muted-foreground mb-3">&#9203; Loading...</div>
  <div class="flex items-center gap-3 py-2.5 border-b border-border text-sm">
    <label class="flex items-center gap-2 cursor-pointer font-semibold text-foreground min-w-[280px]"><input type="checkbox" class="w-4 h-4 accent-primary" id="appr-a" data-key="partA"> Part A &mdash; Process Phases Approved</label>
    <span class="text-[11px] text-muted-foreground ml-auto" id="appr-a-date"></span>
  </div>
  <div class="flex items-center gap-3 py-2.5 border-b border-border text-sm">
    <label class="flex items-center gap-2 cursor-pointer font-semibold text-foreground min-w-[280px]"><input type="checkbox" class="w-4 h-4 accent-primary" id="appr-b" data-key="partB"> Part B &mdash; Scoring Pack Approved</label>
    <span class="text-[11px] text-muted-foreground ml-auto" id="appr-b-date"></span>
  </div>
  <div class="flex items-center gap-3 py-2.5 border-b border-border text-sm">
    <label class="flex items-center gap-2 cursor-pointer font-semibold text-foreground min-w-[280px]"><input type="checkbox" class="w-4 h-4 accent-primary" id="appr-c" data-key="partC"> Part C &mdash; Metrics &amp; KPIs Approved</label>
    <span class="text-[11px] text-muted-foreground ml-auto" id="appr-c-date"></span>
  </div>
  <div class="flex items-center gap-3 py-2.5 border-b border-border text-sm">
    <label class="flex items-center gap-2 cursor-pointer font-semibold text-foreground min-w-[280px]"><input type="checkbox" class="w-4 h-4 accent-primary" id="appr-d" data-key="partD"> Part D &mdash; Dev Spec (Fields, Flows, Rules) Approved</label>
    <span class="text-[11px] text-muted-foreground ml-auto" id="appr-d-date"></span>
  </div>
  <div class="flex items-center gap-3 py-2.5 border-b border-border text-sm">
    <label class="flex items-center gap-2 cursor-pointer font-semibold text-foreground min-w-[280px]"><input type="checkbox" class="w-4 h-4 accent-primary" id="appr-full" data-key="full"> Full Arbitration &amp; Mediation Specification Approved</label>
    <span class="text-[11px] text-muted-foreground ml-auto" id="appr-full-date"></span>
  </div>

  <h3 class="text-sm font-semibold text-foreground mt-6 mb-2">Notes</h3>
  <textarea class="w-full min-h-[100px] border border-border rounded-md p-3 text-sm resize-y focus:outline-none focus:ring-2 focus:ring-ring" id="mgmt-notes" placeholder="Add management notes, feedback, or change requests here..."></textarea>
</div>

</section>

</div><!-- end max-w-7xl -->
</main>
</div><!-- end flex -->

<script>
function toggleCard(header){{
  var card=header.parentElement;
  var body=card.querySelector('[data-card-body]');
  var chevron=card.querySelector('[data-chevron]');
  if(body)body.classList.toggle('hidden');
  if(chevron)chevron.classList.toggle('rotate-180');
}}

function setTab(id, btn) {{
  document.querySelectorAll('.tab-pane').forEach(function(p) {{
    p.classList.remove('active');
    p.style.display = 'none';
  }});
  var t = document.getElementById(id);
  if (t) {{
    t.classList.add('active');
    t.style.display = 'block';
  }}
  if (btn) {{
    btn.parentElement.querySelectorAll('.tab-btn').forEach(function(b) {{
      b.className = 'tab-btn px-4 py-2 text-sm font-medium rounded-md text-muted-foreground hover:text-foreground transition-colors';
    }});
    btn.className = 'tab-btn px-4 py-2 text-sm font-medium rounded-md bg-card text-foreground shadow-sm';
  }}
}}

(function(){{
  var tip=document.createElement('div');tip.id='tooltip-overlay';tip.style.display='none';document.body.appendChild(tip);
  var hideTimer=null;
  function show(btn){{clearTimeout(hideTimer);var pop=btn.nextElementSibling;if(!pop||!pop.classList.contains('info-popover'))return;tip.innerHTML=pop.innerHTML;tip.style.display='block';var r=btn.getBoundingClientRect();var tw=340;var left=r.right-tw;if(left<8)left=8;if(left+tw>window.innerWidth-8)left=window.innerWidth-tw-8;tip.style.left=left+'px';tip.style.top=(r.bottom+window.pageYOffset+6)+'px';}}
  function hide(){{hideTimer=setTimeout(function(){{tip.style.display='none';}},120);}}
  document.addEventListener('mouseover',function(e){{var btn=e.target.closest('button[title="More detail"]');if(btn)show(btn);}});
  document.addEventListener('mouseout',function(e){{var btn=e.target.closest('button[title="More detail"]');if(btn)hide();}});
}})();

function navTo(id){{
  var el=document.getElementById(id);var main=document.getElementById('main-scroll');
  if(el&&main){{var mR=main.getBoundingClientRect();var eR=el.getBoundingClientRect();main.scrollTo({{top:main.scrollTop+eR.top-mR.top-10,behavior:'smooth'}});}}
}}

(function(){{
  var sections=['partA','ph1','ph2','ph3','ph4','partB','tpi','wev','tss','atv','sls','ctt','trs','eri','ccs','leadership-dash','partC','metrics-sla','metrics-readiness','metrics-denovo','metrics-quality','metrics-dashboard','metrics-gates','partD','approval'];
  var links=document.querySelectorAll('.sidebar-link');
  var main=document.getElementById('main-scroll');if(!main)return;
  function spy(){{var current='';sections.forEach(function(id){{var el=document.getElementById(id);if(el){{var r=el.getBoundingClientRect();var mR=main.getBoundingClientRect();if(r.top-mR.top<=120)current=id;}}}});
  links.forEach(function(l){{l.classList.remove('bg-accent','text-accent-foreground');var oc=l.getAttribute('onclick')||'';if(oc.indexOf("'"+current+"'")>-1)l.classList.add('bg-accent','text-accent-foreground');}});}}
  main.addEventListener('scroll',spy);
}})();

document.addEventListener('click',function(e){{var mn=document.getElementById('mobile-nav');var nb=document.getElementById('nav-hamburger');if(mn&&!mn.classList.contains('hidden')&&!mn.contains(e.target)&&e.target!==nb&&!nb.contains(e.target))mn.classList.add('hidden');}});

document.addEventListener('DOMContentLoaded',function(){{
  ['ph1','tpi'].forEach(function(id){{var card=document.getElementById(id);if(card){{var body=card.querySelector('[data-card-body]');if(body)body.classList.remove('hidden');var chev=card.querySelector('[data-chevron]');if(chev)chev.classList.add('rotate-180');}}}});
}});
</script>
<script type="module">
import {{ neon }} from 'https://esm.sh/@neondatabase/serverless';

const sql = neon('postgresql://neondb_owner:npg_rwK4vVmAyzG5@ep-mute-cloud-aik2rpsg.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require');
const PAGE_ID = '{PAGE_ID}';
const statusEl = document.getElementById('sync-status');
const notesEl = document.getElementById('mgmt-notes');
const checkboxes = document.querySelectorAll('#approval input[type="checkbox"][data-key]');

function setStatus(text, color) {{
  if (statusEl) {{ statusEl.textContent = text; statusEl.style.color = color || '#737373'; }}
}}

let saveTimer = null;
function debounceSave(ms = 500) {{
  clearTimeout(saveTimer);
  saveTimer = setTimeout(saveState, ms);
}}

async function ensureTable() {{
  await sql`CREATE TABLE IF NOT EXISTS spec_approvals (
    page_id TEXT PRIMARY KEY,
    checkboxes JSONB NOT NULL DEFAULT '{{}}',
    notes TEXT DEFAULT '',
    updated_at TIMESTAMPTZ DEFAULT now()
  )`;
}}

function gatherState() {{
  const cbState = {{}};
  checkboxes.forEach(cb => {{
    const key = cb.dataset.key;
    const dateSpan = document.getElementById(cb.id + '-date');
    cbState[key] = {{
      checked: cb.checked,
      date: dateSpan ? dateSpan.textContent : ''
    }};
  }});
  return {{ checkboxes: cbState, notes: notesEl ? notesEl.value : '' }};
}}

async function saveState() {{
  try {{
    setStatus('Saving...', '#737373');
    const state = gatherState();
    await sql`INSERT INTO spec_approvals (page_id, checkboxes, notes, updated_at)
      VALUES (${{PAGE_ID}}, ${{JSON.stringify(state.checkboxes)}}, ${{state.notes}}, now())
      ON CONFLICT (page_id) DO UPDATE SET
        checkboxes = ${{JSON.stringify(state.checkboxes)}},
        notes = ${{state.notes}},
        updated_at = now()`;
    setStatus('\\u2713 Saved', '#2e7d32');
  }} catch (e) {{
    console.error('Save failed:', e);
    setStatus('\\u26A0 Save failed', '#c62828');
  }}
}}

async function loadState() {{
  try {{
    await ensureTable();
    const rows = await sql`SELECT checkboxes, notes FROM spec_approvals WHERE page_id = ${{PAGE_ID}}`;
    if (rows.length > 0) {{
      const {{ checkboxes: cbData, notes }} = rows[0];
      if (cbData) {{
        checkboxes.forEach(cb => {{
          const key = cb.dataset.key;
          if (cbData[key]) {{
            cb.checked = cbData[key].checked || false;
            const dateSpan = document.getElementById(cb.id + '-date');
            if (dateSpan) dateSpan.textContent = cbData[key].date || '';
          }}
        }});
      }}
      if (notesEl && notes) notesEl.value = notes;
    }}
    setStatus('\\u2713 Synced', '#2e7d32');
  }} catch (e) {{
    console.error('Load failed:', e);
    setStatus('\\u26A0 Offline (local only)', '#c62828');
  }}
}}

checkboxes.forEach(cb => {{
  cb.addEventListener('change', () => {{
    const dateSpan = document.getElementById(cb.id + '-date');
    if (dateSpan) {{
      dateSpan.textContent = cb.checked ? 'Approved: ' + new Date().toLocaleString() : '';
    }}
    debounceSave(300);
  }});
}});

if (notesEl) {{
  notesEl.addEventListener('input', () => debounceSave(500));
}}

loadState();
</script>

</body>
</html>'''

with open('/tmp/case-opening-flow/arbitration-mediation.html', 'w') as f:
    f.write(html)

print(f'Written arbitration-mediation.html: {len(html)} bytes')
