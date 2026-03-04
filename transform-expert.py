#!/usr/bin/env python3
"""Transform expert-deposition.html from custom CSS to shadcn UI."""
import re

with open('/tmp/case-opening-flow/expert-deposition.html', 'r') as f:
    content = f.read()

# ============================================================
# 1. Replace style block + tailwind config (lines 7-174)
# ============================================================
style_start = content.find('<style>\n*{box-sizing')
style_end = content.find("</head>\n<body>")
if style_start < 0:
    # Try alternate
    style_start = content.find('<style>')

new_head_end = """<style>
@media print {
  .sidebar-area { display: none !important; }
  .main-area { overflow: visible !important; }
  [data-card-body] { display: block !important; }
  .tab-pane { display: block !important; }
}
#tooltip-overlay {
  position: absolute; z-index: 9999;
  background: white; border: 1px solid #e5e5e5;
  border-radius: 0.5rem; box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  padding: 12px 14px; min-width: 260px; max-width: 340px;
  font-size: 13px; color: #0a0a0a; line-height: 1.5;
  pointer-events: none;
}
#tooltip-overlay strong {
  display: block; font-size: 11px; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.4px;
  color: #171717; margin-bottom: 6px;
}
#tooltip-overlay ul { padding-left: 14px; margin: 4px 0 0; }
#tooltip-overlay li { margin-bottom: 3px; }
.info-popover { display: none; }
</style>
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  theme: {
    extend: {
      colors: {
        background: '#fafafa', foreground: '#0a0a0a', card: '#ffffff', 'card-foreground': '#0a0a0a',
        primary: '#171717', 'primary-foreground': '#fafafa', secondary: '#f5f5f5', 'secondary-foreground': '#171717',
        muted: '#f5f5f5', 'muted-foreground': '#737373', accent: '#f5f5f5', 'accent-foreground': '#171717',
        destructive: '#ef4444', border: '#e5e5e5', input: '#e5e5e5', ring: '#0a0a0a',
      },
      borderRadius: { lg: '0.625rem', md: '0.5rem', sm: '0.375rem' }
    }
  }
}
</script>
</head>
<body class="bg-background text-foreground font-sans antialiased">"""

content = content[:style_start] + new_head_end + content[style_end + len("</head>\n<body>"):]

# ============================================================
# 2. Replace nav + hamburger + wrapper + sidebar + main + header + phase bar + legend
# ============================================================
nav_start = content.find('<!-- TOP NAV BAR -->')
part_a_marker = '<!-- ============================================================ PART A -->'
part_a_idx = content.find(part_a_marker)

new_nav_section = """<!-- TOP NAV -->
<nav class="sticky top-0 z-50 h-14 border-b border-border bg-card">
  <div class="max-w-[1460px] mx-auto h-full flex items-center justify-between px-6">
    <span class="text-sm font-semibold text-muted-foreground tracking-wide">BJB Performance Plan</span>
    <div class="hidden md:flex items-center gap-1">
      <a href="index.html" class="px-3 py-1.5 text-sm font-medium text-muted-foreground rounded-md hover:bg-accent hover:text-accent-foreground transition-colors no-underline">Case Opening</a>
      <a href="treatment-monitoring.html" class="px-3 py-1.5 text-sm font-medium text-muted-foreground rounded-md hover:bg-accent hover:text-accent-foreground transition-colors no-underline">Treatment Monitoring</a>
      <a href="written-discovery.html" class="px-3 py-1.5 text-sm font-medium text-muted-foreground rounded-md hover:bg-accent hover:text-accent-foreground transition-colors no-underline">Written Discovery</a>
      <a href="expert-deposition.html" class="px-3 py-1.5 text-sm font-medium text-foreground bg-accent rounded-md no-underline" style="border-bottom: 2px solid #10b981">Expert &amp; Deposition</a>
    </div>
    <button id="nav-hamburger" class="md:hidden text-foreground" onclick="document.getElementById('mobile-nav').classList.toggle('hidden')">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
    </button>
  </div>
  <div id="mobile-nav" class="hidden md:hidden bg-card border-t border-border px-4 pb-3">
    <a href="index.html" class="block px-3 py-2 text-sm font-medium text-muted-foreground rounded-md hover:bg-accent no-underline">Case Opening</a>
    <a href="treatment-monitoring.html" class="block px-3 py-2 text-sm font-medium text-muted-foreground rounded-md hover:bg-accent no-underline">Treatment Monitoring</a>
    <a href="written-discovery.html" class="block px-3 py-2 text-sm font-medium text-muted-foreground rounded-md hover:bg-accent no-underline">Written Discovery</a>
    <a href="expert-deposition.html" class="block px-3 py-2 text-sm font-medium text-foreground bg-accent rounded-md no-underline">Expert &amp; Deposition</a>
  </div>
</nav>

<div class="flex h-[calc(100vh-3.5rem)]">
<!-- SIDEBAR -->
<aside class="sidebar-area hidden md:flex w-64 flex-col border-r border-border bg-card overflow-y-auto shrink-0">
  <div class="px-5 pt-6 pb-4 border-b border-border">
    <h2 class="text-xs font-bold text-foreground tracking-wide uppercase">Expert &amp; Deposition</h2>
    <p class="text-[11px] text-muted-foreground mt-0.5">Litify Dev Spec v1.0</p>
  </div>
  <div class="py-3">
    <div class="px-5 py-1.5 text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Part A &mdash; Process</div>
    <a class="sidebar-link block px-5 py-1.5 text-xs font-semibold text-foreground cursor-pointer hover:bg-accent" onclick="navTo('partA')">Overview</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('ph1')">Phase 1: Non-Party Depositions</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('ph2')">Phase 2: Defendant Depositions</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('ph3')">Phase 3: Expert Retention</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('ph4')">Phase 4: Report Follow-Up</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('ph5')">Phase 5: Amended Reports</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('ph6')">Phase 6: Client Depo &amp; Scoring</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('ph7')">Phase 7: IME Management</a>
  </div>
  <div class="py-3 border-t border-border">
    <div class="px-5 py-1.5 text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Part B &mdash; Metrics</div>
    <a class="sidebar-link block px-5 py-1.5 text-xs font-semibold text-foreground cursor-pointer hover:bg-accent" onclick="navTo('partB')">Overview</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('exec-scorecard')">Executive Scorecard</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('core-metrics')">15 Core Metrics</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('kpi-library')">KPI Library</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('sla-ladders')">SLA Enforcement</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('epi')">Expert Performance Index</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('risk-flags')">Risk Flags</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('dpi')">Defense Pressure Index</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('eli')">Expert Leverage Index</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('pressure-gap')">Pressure Gap</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('drs-panel')">Resistance Signals</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('settlement-engine')">Settlement Prediction</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('tri')">Trial Readiness</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('strategic-view')">Strategic Intelligence</a>
  </div>
  <div class="py-3 border-t border-border">
    <div class="px-5 py-1.5 text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Part C &mdash; Dev Spec</div>
    <a class="sidebar-link block px-5 py-1.5 text-xs font-semibold text-foreground cursor-pointer hover:bg-accent" onclick="navTo('partC')">Overview</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('partC');setTab('tab-fields')">Litify Fields</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('partC');setTab('tab-flows')">Flows</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('partC');setTab('tab-rules')">Validation Rules</a>
  </div>
  <div class="py-3 border-t border-border">
    <div class="px-5 py-1.5 text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Navigation</div>
    <a class="block px-5 py-1.5 text-xs text-muted-foreground hover:bg-accent hover:text-foreground no-underline" href="index.html">&larr; Case Opening</a>
    <a class="block px-5 py-1.5 text-xs text-muted-foreground hover:bg-accent hover:text-foreground no-underline" href="treatment-monitoring.html">&larr; Treatment Monitoring</a>
    <a class="block px-5 py-1.5 text-xs text-muted-foreground hover:bg-accent hover:text-foreground no-underline" href="written-discovery.html">&larr; Written Discovery</a>
  </div>
  <div class="py-3 border-t border-border">
    <div class="px-5 py-1.5 text-[10px] font-bold uppercase tracking-wider text-muted-foreground">Sign-Off</div>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-foreground" onclick="navTo('approval')">Approval &amp; Notes</a>
  </div>
</aside>

<!-- MAIN CONTENT -->
<main class="main-area flex-1 overflow-y-auto">
<div class="max-w-5xl px-8 py-10">

<!-- PAGE HEADER -->
<div class="border-b-2 border-[#10b981] pb-8 mb-8">
  <h1 class="text-2xl font-bold text-foreground">BJB Expert &amp; Deposition &mdash; Litify Dev Specification</h1>
  <p class="text-sm text-muted-foreground mt-1">Expert Retention &nbsp;|&nbsp; Depositions &nbsp;|&nbsp; Report Management &nbsp;|&nbsp; IME Coordination</p>
  <span class="inline-block mt-3 px-3 py-0.5 text-xs border border-border rounded-full text-muted-foreground bg-muted">v1.0 &nbsp;&bull;&nbsp; February 2026</span>
</div>

<!-- PHASE BAR -->
<div class="flex flex-wrap gap-2 mb-8">
  <button class="px-3 py-1.5 text-xs font-medium rounded-md border border-border bg-card text-foreground hover:bg-accent transition-colors" onclick="navTo('ph1')">1 &mdash; Non-Party Depos</button>
  <button class="px-3 py-1.5 text-xs font-medium rounded-md border border-border bg-card text-foreground hover:bg-accent transition-colors" onclick="navTo('ph2')">2 &mdash; Defendant Depos</button>
  <button class="px-3 py-1.5 text-xs font-medium rounded-md border border-border bg-card text-foreground hover:bg-accent transition-colors" onclick="navTo('ph3')">3 &mdash; Expert Retention</button>
  <button class="px-3 py-1.5 text-xs font-medium rounded-md border border-border bg-card text-foreground hover:bg-accent transition-colors" onclick="navTo('ph4')">4 &mdash; Report Follow-Up</button>
  <button class="px-3 py-1.5 text-xs font-medium rounded-md border border-border bg-card text-foreground hover:bg-accent transition-colors" onclick="navTo('ph5')">5 &mdash; Amended Reports</button>
  <button class="px-3 py-1.5 text-xs font-medium rounded-md border border-border bg-card text-foreground hover:bg-accent transition-colors" onclick="navTo('ph6')">6 &mdash; Client Depo</button>
  <button class="px-3 py-1.5 text-xs font-medium rounded-md border border-border bg-card text-foreground hover:bg-accent transition-colors" onclick="navTo('ph7')">7 &mdash; IME Mgmt</button>
  <button class="px-3 py-1.5 text-xs font-medium rounded-md border border-purple-300 bg-purple-50 text-purple-700 hover:bg-purple-100 transition-colors" onclick="window.location.href='written-discovery.html'">Written Discovery</button>
  <button class="px-3 py-1.5 text-xs font-medium rounded-md border border-blue-300 bg-blue-50 text-blue-700 hover:bg-blue-100 transition-colors" onclick="window.location.href='index.html'">Case Opening</button>
</div>

<!-- LEGEND -->
<div class="rounded-lg border border-border bg-card p-5 mb-8 flex flex-wrap gap-6">
  <div>
    <h4 class="text-[11px] font-bold uppercase tracking-wider text-muted-foreground mb-2">Roles</h4>
    <div class="flex flex-wrap gap-2">
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-blue-100 text-blue-800">Para / Legal Asst</span>
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-violet-100 text-violet-800">Attorney</span>
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-green-100 text-green-800">System Auto</span>
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-orange-100 text-orange-800">Management</span>
    </div>
  </div>
  <div>
    <h4 class="text-[11px] font-bold uppercase tracking-wider text-muted-foreground mb-2">Status</h4>
    <div class="flex flex-wrap gap-2">
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-red-100 text-red-800">Required</span>
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-yellow-100 text-yellow-800">C / NA / D</span>
      <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-green-100 text-green-800">Auto</span>
    </div>
  </div>
</div>

"""

content = content[:nav_start] + new_nav_section + content[part_a_idx:]

# ============================================================
# 3. Global component pattern replacements
# ============================================================

# part-header
content = content.replace('<div class="part-header">', '<div class="bg-primary text-primary-foreground px-6 py-4 rounded-t-lg">')
# section.part
content = content.replace('<section class="part"', '<section class="mb-12"')

# phase-card
content = content.replace('<div class="phase-card open"', '<div class="rounded-lg border border-border bg-card shadow-sm mb-4"')
content = content.replace('<div class="phase-card"', '<div class="rounded-lg border border-border bg-card shadow-sm mb-4"')

# phase-card-header -> button
content = content.replace(
    '<div class="phase-card-header" onclick="toggleCard(this)">',
    '<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors">'
)

# Close header divs to buttons, and phase-card-body -> data-card-body hidden
content = re.sub(
    r'</div>\n<div class="phase-card-body">',
    '</button>\n<div class="border-t border-border px-5 py-5 hidden" data-card-body>',
    content
)

# phase-num
content = content.replace('<span class="phase-num">', '<span class="w-7 h-7 rounded-full bg-[#10b981] text-white text-xs font-bold flex items-center justify-center">')

# toggle-icon -> SVG chevron
content = content.replace(
    '<span class="toggle-icon">&#8964;</span>',
    '<svg class="w-4 h-4 text-muted-foreground transition-transform" data-chevron fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>'
)

# phase-sla
content = content.replace('<span class="phase-sla">', '<span class="text-[11px] font-medium text-muted-foreground bg-muted px-2 py-0.5 rounded">')

# div with flex style inside button headers
content = content.replace('<div style="display:flex;gap:8px;align-items:center">', '<div class="flex items-center gap-2">')

# Badges
content = content.replace('class="badge badge-para"', 'class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-blue-100 text-blue-800"')
content = content.replace('class="badge badge-atty"', 'class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-violet-100 text-violet-800"')
content = content.replace('class="badge badge-sys"', 'class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-green-100 text-green-800"')
content = content.replace('class="badge badge-mgmt"', 'class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-orange-100 text-orange-800"')
content = content.replace('class="badge badge-req"', 'class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-red-100 text-red-800"')
content = content.replace('class="badge badge-cna"', 'class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-yellow-100 text-yellow-800"')
content = content.replace('class="badge badge-auto"', 'class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-green-100 text-green-800"')

# Info/warn/gate/formula boxes
content = content.replace('<div class="info-box">', '<div class="rounded-lg border border-blue-200 bg-blue-50 p-4 text-sm text-blue-900 mb-3">')
content = content.replace('<div class="warn-box">', '<div class="rounded-lg border border-yellow-200 bg-yellow-50 p-4 text-sm text-yellow-900 mb-3">')
content = content.replace('<div class="gate-box">', '<div class="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-900 mb-3">')
content = content.replace('<div class="formula-box">', '<div class="rounded-lg border border-green-200 bg-green-50 p-4 text-sm text-green-900 font-mono mb-3">')

# table-wrap
content = content.replace('<div class="table-wrap">', '<div class="rounded-md border border-border overflow-x-auto my-3">')
content = content.replace('<div class="table-wrap"><table>', '<div class="rounded-md border border-border overflow-x-auto my-3"><table>')

# Tables
content = content.replace('<table>', '<table class="w-full text-sm">')
content = content.replace('<thead><tr>', '<thead><tr class="border-b border-border bg-muted">')
content = re.sub(r'<th>', '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">', content)
content = re.sub(r'<th style="([^"]*?)">', r'<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider" style="\1">', content)

# task-row -> hover
content = content.replace('<tr class="task-row">', '<tr class="border-b border-border hover:bg-muted/50">')

# td
content = content.replace('<td>', '<td class="px-4 py-3">')
content = re.sub(r'<td style="([^"]*?)">', r'<td class="px-4 py-3" style="\1">', content)
content = re.sub(r'<td class="(band-\w+)">', r'<td class="px-4 py-3 \1">', content)

# Band colors
content = content.replace('band-green', 'bg-green-100 text-green-800')
content = content.replace('band-yellow', 'bg-yellow-100 text-yellow-800')
content = content.replace('band-red', 'bg-red-100 text-red-800')
content = content.replace('band-orange', 'bg-orange-100 text-orange-800')
content = content.replace('band-blue', 'bg-blue-100 text-blue-800')

# Ladder
content = content.replace('<div class="ladder">', '<div class="flex flex-col gap-1 my-3">')
content = content.replace('<div class="ladder-rung">', '<div class="flex items-stretch rounded-md border border-border overflow-hidden text-sm">')
content = content.replace('<div class="ladder-rung rung-atty">', '<div class="flex items-stretch rounded-md border border-border overflow-hidden text-sm bg-violet-50">')
content = content.replace('<div class="ladder-rung rung-auto">', '<div class="flex items-stretch rounded-md border border-border overflow-hidden text-sm bg-green-50">')
content = content.replace('<div class="rung-num">', '<div class="bg-primary text-primary-foreground min-w-[44px] flex items-center justify-center font-bold text-sm shrink-0">')
content = re.sub(r'<div class="rung-num" style="([^"]*?)">', r'<div class="min-w-[44px] flex items-center justify-center font-bold text-sm shrink-0 text-white" style="\1">', content)
content = content.replace('<div class="rung-body">', '<div class="flex-1 px-3 py-2 relative pr-8">')
content = content.replace('<div class="rung-title">', '<div class="font-semibold text-foreground mb-0.5">')
content = content.replace('<div class="rung-sla">', '<div class="text-[11px] text-muted-foreground mb-0.5">')
content = content.replace('<div class="rung-action">', '<div class="text-[11px] text-muted-foreground">')
content = content.replace('<span class="rung-who">', '<span class="inline-block ml-1">')

# Exit box
content = content.replace('<div class="exit-box">', '<div class="rounded-lg border border-yellow-200 bg-yellow-50 p-3 mt-2 text-xs text-yellow-900">')
content = re.sub(r'<div class="exit-box" style="[^"]*?">', '<div class="rounded-lg border border-red-200 bg-red-50 p-3 mt-2 text-xs text-red-900">', content)

# Sub-section
content = content.replace('<div class="sub-section">', '<div class="my-6">')
content = re.sub(r'<div class="sub-section" id="([^"]*?)">', r'<div class="my-6" id="\1">', content)

# Pillar
content = content.replace('<div class="pillar-grid">', '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 my-3">')
content = content.replace('<div class="pillar-card">', '<div class="rounded-lg border border-border bg-card p-4">')
content = content.replace('<span class="pillar-high">', '<span class="block text-xs p-2 bg-green-100 text-green-800 rounded mb-1">')
content = content.replace('<span class="pillar-low">', '<span class="block text-xs p-2 bg-red-100 text-red-800 rounded">')
content = re.sub(r'<p class="pillar-api">', '<p class="text-[11px] text-muted-foreground mb-2">', content)

# Info button -> shadcn SVG
content = content.replace(
    '<button class="info-btn" title="More detail">&#9432;</button>',
    '<button class="inline-flex items-center justify-center w-5 h-5 rounded-full text-muted-foreground hover:text-foreground hover:bg-accent transition-colors cursor-help absolute right-2 top-1/2 -translate-y-1/2" title="More detail"><svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="2"/><path stroke-width="2" d="M12 16v-4m0-4h.01"/></svg></button>'
)

# info-popover -> add hidden
content = content.replace('<div class="info-popover">', '<div class="info-popover hidden">')

# Tabs
content = content.replace('<div class="tabs-nav">', '<div class="flex border-b border-border mb-6 gap-0">')
content = content.replace('<button class="tab-btn active"', '<button class="px-4 py-2.5 text-sm font-medium border-b-2 border-foreground text-foreground -mb-px"')
content = content.replace('<button class="tab-btn"', '<button class="px-4 py-2.5 text-sm font-medium border-b-2 border-transparent text-muted-foreground hover:text-foreground -mb-px"')

# Tab panes
content = content.replace('<div class="tab-pane active"', '<div class="tab-pane block"')
content = content.replace('<div class="tab-pane"', '<div class="tab-pane hidden"')

# Step items
content = content.replace('<ol class="step-list">', '<ol class="space-y-0">')
content = content.replace('<li class="step-item">', '<li class="flex gap-3 py-3 border-b border-border last:border-b-0">')
content = content.replace('<span class="step-num-circle">', '<span class="inline-flex items-center justify-center min-w-[24px] h-6 bg-primary text-primary-foreground rounded-full text-[11px] font-bold shrink-0 mt-0.5">')
content = content.replace('<div class="step-content">', '<div class="flex-1">')
content = content.replace('<div class="step-title">', '<div class="font-semibold text-sm text-foreground">')
content = content.replace('<div class="step-detail">', '<div class="text-xs text-muted-foreground mt-0.5">')

# ============================================================
# 5. Fix approval sections (both instances)
# ============================================================
content = content.replace(
    '<div class="approval-section">\n  <h3>Management Approval Checklist</h3>',
    '<div class="rounded-lg border-2 border-border bg-card p-6 my-8">\n  <h3 class="text-base font-bold text-foreground mb-4 pb-2 border-b-2 border-border">Management Approval Checklist</h3>\n  <p class="text-xs text-muted-foreground mb-4">Approved by Ryan Broderick</p>'
)
content = content.replace('<div class="approval-row">', '<div class="flex items-center gap-3 py-3 border-b border-border text-sm">')
content = content.replace('<span class="approval-date"', '<span class="text-[11px] text-muted-foreground ml-auto"')
content = content.replace('<textarea class="notes-area"', '<textarea class="w-full min-h-[100px] border border-input rounded-md px-3 py-2 text-sm resize-y mt-3 focus:outline-none focus:ring-2 focus:ring-ring"')
content = content.replace('<h3 style="margin-top:24px">Notes</h3>', '<h3 class="text-base font-bold text-foreground mt-6">Notes</h3>')

# ============================================================
# 6. Update JavaScript blocks
# ============================================================

# toggleCard - both instances
old_toggle = """function toggleCard(header){
  var card=header.parentElement;
  card.classList.toggle('open');
}"""
new_toggle = """function toggleCard(btn){
  var card=btn.closest('[class*="rounded-lg"]');
  if(!card)card=btn.parentElement;
  var body=card.querySelector('[data-card-body]');
  var chevron=card.querySelector('[data-chevron]');
  if(body)body.classList.toggle('hidden');
  if(chevron)chevron.classList.toggle('rotate-180');
}"""
content = content.replace(old_toggle, new_toggle)

# Info btn selector
content = content.replace("var btn=e.target.closest('.info-btn');", "var btn=e.target.closest('[title=\"More detail\"]');")

# navTo - scroll main-area (both instances)
old_nav = """function navTo(id){
  var el=document.getElementById(id);
  if(el){
    var rect=el.getBoundingClientRect();
    var top=rect.top+window.pageYOffset-10;
    setTimeout(function(){window.scrollTo(0,top);},0);
  }
}"""
new_nav = """function navTo(id){
  var el=document.getElementById(id);
  if(el){
    var main=document.querySelector('.main-area');
    if(main){main.scrollTop=el.offsetTop-main.offsetTop-10;}
    else{el.scrollIntoView({behavior:'smooth',block:'start'});}
  }
}"""
content = content.replace(old_nav, new_nav)

# setTab - shadcn pill classes (both instances)
old_tab = """function setTab(id,btn){
  var panes=document.querySelectorAll('.tab-pane');
  panes.forEach(function(p){p.classList.remove('active')});
  var target=document.getElementById(id);
  if(target)target.classList.add('active');
  if(btn){
    var btns=document.querySelectorAll('.tab-btn');
    btns.forEach(function(b){b.classList.remove('active')});
    btn.classList.add('active');
  }
}"""
new_tab = """function setTab(id,btn){
  var panes=document.querySelectorAll('.tab-pane');
  panes.forEach(function(p){p.classList.remove('block');p.classList.add('hidden')});
  var target=document.getElementById(id);
  if(target){target.classList.remove('hidden');target.classList.add('block');}
  if(btn){
    var btns=btn.parentElement.querySelectorAll('button');
    btns.forEach(function(b){
      b.className='px-4 py-2.5 text-sm font-medium border-b-2 border-transparent text-muted-foreground hover:text-foreground -mb-px';
    });
    btn.className='px-4 py-2.5 text-sm font-medium border-b-2 border-foreground text-foreground -mb-px';
  }
}"""
content = content.replace(old_tab, new_tab)

# Remove back-to-top
content = content.replace('<button id="back-to-top" onclick="window.scrollTo(0,0)">&#8593;</button>', '')
content = content.replace("""// Back to top visibility
window.addEventListener('scroll',function(){
  var btn=document.getElementById('back-to-top');
  if(window.scrollY>300){btn.classList.add('visible');}
  else{btn.classList.remove('visible');}
});""", '')

# Scroll spy 1
old_spy1 = """  var links=document.querySelectorAll('.sidebar-link');
  var sections=['partA','ph1','ph2','ph3','ph4','ph5','ph6','ph7','partB','exec-scorecard','core-metrics','kpi-library','sla-ladders','epi','risk-flags','dpi','eli','pressure-gap','drs-panel','settlement-engine','tri','strategic-view','partC','approval'];
  function onScroll(){
    var y=window.scrollY+120;
    var current='';
    sections.forEach(function(id){
      var el=document.getElementById(id);
      if(el&&el.offsetTop<=y)current=id;
    });
    links.forEach(function(l){
      l.classList.remove('active');
      var oc=l.getAttribute('onclick')||'';
      if(oc.indexOf("'"+current+"'")>-1)l.classList.add('active');
    });
  }
  window.addEventListener('scroll',onScroll);"""

new_spy1 = """  var links=document.querySelectorAll('.sidebar-link');
  var sections=['partA','ph1','ph2','ph3','ph4','ph5','ph6','ph7','partB','exec-scorecard','core-metrics','kpi-library','sla-ladders','epi','risk-flags','dpi','eli','pressure-gap','drs-panel','settlement-engine','tri','strategic-view','partC','approval'];
  var main=document.querySelector('.main-area');
  function onScroll(){
    var y=(main?main.scrollTop:window.scrollY)+120;
    var current='';
    sections.forEach(function(id){
      var el=document.getElementById(id);
      if(el){var top=main?el.offsetTop-main.offsetTop:el.offsetTop;if(top<=y)current=id;}
    });
    links.forEach(function(l){
      l.classList.remove('bg-accent','text-foreground','font-semibold');
      var oc=l.getAttribute('onclick')||'';
      if(oc.indexOf("'"+current+"'")>-1)l.classList.add('bg-accent','text-foreground','font-semibold');
    });
  }
  if(main)main.addEventListener('scroll',onScroll);
  else window.addEventListener('scroll',onScroll);"""
content = content.replace(old_spy1, new_spy1)

# Scroll spy 2
old_spy2 = """  var links=document.querySelectorAll('.sidebar-link');
  var sections=['partA','ph1','ph2','ph3','ph4','ph5','ph6','ph7','partB','scorecard','core-metrics','kpi-library','sla-ladders','epi','risk-flags','dpi','eli','pressure-gap','defense-signals','settlement-engine','trial-readiness','strategic-view','partC','approval'];
  function onScroll(){
    var y=window.scrollY+120;
    var current='';
    sections.forEach(function(id){
      var el=document.getElementById(id);
      if(el&&el.offsetTop<=y)current=id;
    });
    links.forEach(function(l){
      l.classList.remove('active');
      var oc=l.getAttribute('onclick')||'';
      if(oc.indexOf("'"+current+"'")>-1)l.classList.add('active');
    });
  }
  window.addEventListener('scroll',onScroll);"""

new_spy2 = """  var links=document.querySelectorAll('.sidebar-link');
  var sections=['partA','ph1','ph2','ph3','ph4','ph5','ph6','ph7','partB','scorecard','core-metrics','kpi-library','sla-ladders','epi','risk-flags','dpi','eli','pressure-gap','defense-signals','settlement-engine','trial-readiness','strategic-view','partC','approval'];
  var main=document.querySelector('.main-area');
  function onScroll(){
    var y=(main?main.scrollTop:window.scrollY)+120;
    var current='';
    sections.forEach(function(id){
      var el=document.getElementById(id);
      if(el){var top=main?el.offsetTop-main.offsetTop:el.offsetTop;if(top<=y)current=id;}
    });
    links.forEach(function(l){
      l.classList.remove('bg-accent','text-foreground','font-semibold');
      var oc=l.getAttribute('onclick')||'';
      if(oc.indexOf("'"+current+"'")>-1)l.classList.add('bg-accent','text-foreground','font-semibold');
    });
  }
  if(main)main.addEventListener('scroll',onScroll);
  else window.addEventListener('scroll',onScroll);"""
content = content.replace(old_spy2, new_spy2)

# Remove sidebar close handler
content = content.replace("""// Close sidebar on overlay click (mobile)
document.addEventListener('click',function(e){
  var sidebar=document.getElementById('sidebar');
  var ham=document.getElementById('hamburger');
  if(sidebar.classList.contains('open')&&!sidebar.contains(e.target)&&e.target!==ham){
    sidebar.classList.remove('open');
  }
});""", '')

content = content.replace("""// Close mobile nav on outside click
document.addEventListener('click',function(e){
  var mn=document.getElementById('mobile-nav');
  var nb=document.getElementById('nav-hamburger');
  if(mn&&!mn.classList.contains('hidden')&&!mn.contains(e.target)&&e.target!==nb&&!nb.contains(e.target)){
    mn.classList.add('hidden');
  }
});""", '')

# ============================================================
# 7. Fix closing layout tags
# ============================================================
content = content.replace('</main><!-- end main -->\n</div><!-- end wrapper -->', '</div><!-- end max-w -->\n</main><!-- end main -->\n</div><!-- end flex layout -->')

# Fix h2 in part-headers
content = re.sub(
    r'(<div class="bg-primary text-primary-foreground px-6 py-4 rounded-t-lg">)\s*\n\s*<h2>([^<]+)</h2>\s*\n\s*<p>([^<]+)</p>',
    r'\1\n  <h2 class="text-lg font-bold">\2</h2>\n  <p class="text-sm text-primary-foreground/70 mt-0.5">\3</p>',
    content
)

# Fix sub-section h3
content = re.sub(r'<div class="my-6">\n\s*<h3>([^<]+)</h3>', r'<div class="my-6">\n    <h3 class="text-sm font-bold text-foreground mb-3 pb-1.5 border-b-2 border-border">\1</h3>', content)
content = re.sub(r'<div class="my-6">\n\s*<h4>([^<]+)</h4>', r'<div class="my-6">\n    <h4 class="text-sm font-semibold text-foreground mt-4 mb-2">\1</h4>', content)

# Fix standalone h4 tags
content = re.sub(r'(?<!\n  )<h4>([^<]+)</h4>', r'<h4 class="text-sm font-semibold text-foreground mt-4 mb-2">\1</h4>', content)

# Fix double class attributes from regex chain
content = re.sub(r'class="([^"]*)" class="([^"]*)"', r'class="\1 \2"', content)

# Write output
with open('/tmp/case-opening-flow/expert-deposition.html', 'w') as f:
    f.write(content)

lines = content.count('\n') + 1
print(f"Done! Written {lines} lines, {len(content)} chars")
