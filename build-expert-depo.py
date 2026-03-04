#!/usr/bin/env python3
"""Transform expert-deposition-original.html to shadcn/Tailwind patterns."""
import re

# Read original
with open('/tmp/case-opening-flow/expert-deposition-original.html', 'r') as f:
    orig = f.read()

# Read index.html for reference patterns
with open('/tmp/case-opening-flow/index.html', 'r') as f:
    ref = f.read()

# We'll build the new file from scratch, extracting content from the MORE DETAILED
# second copies in the original (phases 4-7 from lines ~591-808, Part B from ~1162-2107,
# Part C from ~2112-2263, approval from ~2268-2507)

lines = orig.split('\n')

# === HELPER: Convert a table to shadcn pattern ===
def question_item(key, num, text):
    return f'''<label class="flex gap-3 bg-muted border border-border rounded-md p-3 text-xs items-start cursor-pointer hover:bg-accent/30 transition-colors">
        <input type="checkbox" data-key="{key}" class="w-4 h-4 accent-primary mt-0.5 shrink-0">
        <span class="font-bold text-foreground min-w-[18px]">{num}.</span>
        <span class="flex-1">{text}</span>
      </label>'''

def convert_table(html):
    """Convert old-style tables to shadcn pattern."""
    # Wrap in rounded border div
    html = html.replace('<div class="table-wrap">\n', '')
    html = html.replace('<div class="table-wrap">', '')

    # Replace table classes
    html = re.sub(r'<table[^>]*>', '<table class="w-full text-sm">', html)

    # Replace thead/th
    html = re.sub(r'<thead><tr>', '<thead><tr class="border-b border-border bg-muted">', html)
    html = re.sub(r'<th(?:\s+[^>]*)?>',
                  '<th class="px-4 py-3 text-left text-xs font-medium text-muted-foreground uppercase tracking-wider">',
                  html)

    # Replace tbody rows
    html = re.sub(r'<tr class="task-row">', '<tr class="border-b border-border hover:bg-muted/50">', html)
    html = re.sub(r'<tr>(?=<td)', '<tr class="border-b border-border hover:bg-muted/50">', html)

    # Replace td
    html = re.sub(r'<td(?:\s+style="[^"]*")?>', '<td class="px-4 py-3">', html)
    html = re.sub(r'<td class="band-green">', '<td class="px-4 py-3 bg-green-100 text-green-800">', html)
    html = re.sub(r'<td class="band-yellow">', '<td class="px-4 py-3 bg-yellow-100 text-yellow-800">', html)
    html = re.sub(r'<td class="band-orange">', '<td class="px-4 py-3 bg-orange-100 text-orange-800">', html)
    html = re.sub(r'<td class="band-red">', '<td class="px-4 py-3 bg-red-100 text-red-800">', html)

    # Replace old badges
    html = html.replace('<span class="badge badge-para">', '<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-blue-100 text-blue-700">')
    html = html.replace('<span class="badge badge-atty">', '<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-purple-100 text-purple-700">')
    html = html.replace('<span class="badge badge-sys">', '<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-green-100 text-green-700">')
    html = html.replace('<span class="badge badge-mgmt">', '<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-orange-100 text-orange-700">')
    html = html.replace('<span class="badge badge-req">', '<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-red-100 text-red-700">')
    html = html.replace('<span class="badge badge-cna">', '<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-yellow-100 text-yellow-700">')
    html = html.replace('<span class="badge badge-auto">', '<span class="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-green-100 text-green-700">')

    # Replace info-btn with shadcn info button
    html = re.sub(
        r'<button class="info-btn" title="More detail">&#9432;</button>',
        '<button class="inline-flex items-center justify-center w-5 h-5 rounded-full text-muted-foreground hover:text-foreground hover:bg-accent transition-colors cursor-help" title="More detail"><svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="2"/><path stroke-width="2" d="M12 16v-4m0-4h.01"/></svg></button>',
        html
    )

    # Replace old td with position relative
    html = re.sub(r'<td style="position:relative;padding-right:36px">', '<td class="px-4 py-3 relative pr-10">', html)
    html = re.sub(r'<td class="px-4 py-3" style="position:relative;padding-right:36px">', '<td class="px-4 py-3 relative pr-10">', html)

    return html

def convert_content_block(html):
    """Apply all shadcn conversions to a content block."""
    html = convert_table(html)

    # Info boxes
    html = html.replace('<div class="info-box">', '<div class="rounded-md border border-blue-200 bg-blue-50 p-3 mb-4 text-sm">')

    # Warning boxes
    html = html.replace('<div class="warn-box">', '<div class="rounded-md border border-amber-200 bg-amber-50 p-3 mt-4 text-sm">')

    # Formula boxes
    html = html.replace('<div class="formula-box">', '<div class="rounded-md border border-green-200 bg-green-50 p-3 mb-4 text-sm font-mono">')

    # Gate/red boxes
    html = html.replace('<div class="gate-box">', '<div class="rounded-md border border-red-200 bg-red-50 p-3 mt-2 text-sm">')

    # Exit boxes
    html = re.sub(r'<div class="exit-box"(?:\s+style="[^"]*")?>', '<div class="rounded-md border border-amber-200 bg-amber-50 p-3 mt-4 text-sm">', html)
    # Exit boxes that are red (failure conditions)
    html = re.sub(r'<div class="exit-box" style="background:#fef2f2;border-color:#fecaca;margin-top:6px">', '<div class="rounded-md border border-red-200 bg-red-50 p-3 mt-2 text-sm">', html)

    # Sub-section headers
    html = re.sub(r'<div class="sub-section"(?:\s+id="([^"]*)")?>', lambda m: f'<div class="mt-6 mb-4"{f" id={chr(34)}{m.group(1)}{chr(34)}" if m.group(1) else ""}>', html)
    html = re.sub(r'<h3>(?!<)', lambda m: '<h3 class="text-sm font-bold text-foreground mb-3 pb-2 border-b border-border">', html)
    html = re.sub(r'<h4>(?!<)', lambda m: '<h4 class="text-sm font-semibold text-foreground mt-4 mb-2">', html)

    # Ladder rungs
    html = html.replace('<div class="ladder">', '<div class="flex flex-col gap-0.5 my-3">')
    html = re.sub(r'<div class="ladder-rung[^"]*">', '<div class="flex items-stretch gap-0 border border-border rounded-md overflow-hidden text-sm hover:bg-blue-50/50 transition-colors">', html)
    html = re.sub(r'<div class="rung-num"(?:\s+style="[^"]*")?>', '<div class="bg-primary text-primary-foreground min-w-[44px] flex items-center justify-center font-bold text-sm shrink-0">', html)
    html = html.replace('<div class="rung-body">', '<div class="flex-1 p-2 px-3 bg-card relative pr-10">')
    html = html.replace('<div class="rung-title">', '<div class="font-semibold text-foreground mb-0.5">')
    html = html.replace('<div class="rung-sla">', '<div class="text-[11px] text-muted-foreground mb-0.5">')
    html = html.replace('<div class="rung-action">', '<div class="text-[11px] text-muted-foreground">')
    html = html.replace('<span class="rung-who">', '<span class="ml-1">')

    # Pillar grid/cards
    html = html.replace('<div class="pillar-grid">', '<div class="grid grid-cols-1 md:grid-cols-3 gap-4 my-3">')
    html = html.replace('<div class="pillar-card">', '<div class="rounded-lg border border-border bg-card p-4">')
    html = re.sub(r'<p class="pillar-api">', '<p class="text-xs text-muted-foreground mb-2">', html)
    html = re.sub(r'<span class="pillar-high">', '<span class="block text-xs p-2 bg-green-50 text-green-800 rounded mb-1">', html)
    html = re.sub(r'<span class="pillar-low">', '<span class="block text-xs p-2 bg-red-50 text-red-800 rounded">', html)

    # Step lists
    html = html.replace('<ol class="step-list">', '<ol class="space-y-0">')
    html = html.replace('<li class="step-item">', '<li class="flex gap-3 py-3 border-b border-border last:border-b-0">')
    html = html.replace('<span class="step-num-circle">', '<span class="flex items-center justify-center min-w-[24px] h-6 bg-primary text-primary-foreground rounded-full text-xs font-bold shrink-0 mt-0.5">')
    html = html.replace('<div class="step-content">', '<div class="flex-1">')
    html = html.replace('<div class="step-title">', '<div class="font-semibold text-foreground text-sm">')
    html = html.replace('<div class="step-detail">', '<div class="text-xs text-muted-foreground mt-1">')

    # Wrap bare tables in rounded border
    html = re.sub(r'(<div class="(?:rounded-md border border-border overflow-hidden|table-wrap)">)?\s*(<table class="w-full text-sm">)',
                  lambda m: m.group(0) if m.group(1) else f'<div class="rounded-md border border-border overflow-hidden">{m.group(2)}', html)
    # Close the wrapping div after </table> if we added one
    # This is tricky - let's handle it differently

    return html

# ============================================================
# BUILD THE NEW FILE
# ============================================================

# Read part1 template we already created
with open('/tmp/case-opening-flow/expert-deposition-part1.html', 'r') as f:
    template = f.read()

# Extract content sections from original (using the MORE DETAILED second copies)

# --- PART A: Phases 1-3 from first copy (lines 307-438), Phases 4-7 from second copy (lines 591-808) ---
# Get phases 1-3 body content
ph1_content = '\n'.join(lines[306:330])  # Phase 1
ph2_content = '\n'.join(lines[332:357])  # Phase 2
ph3_content = '\n'.join(lines[358:438])  # Phase 3

# Get phases 4-7 from SECOND (more detailed) copy
ph4_content = '\n'.join(lines[590:682])  # Phase 4 (with 4A pursuit ladder + 4B review)
ph5_content = '\n'.join(lines[683:711])  # Phase 5 (with amendment triggers)
ph6_content = '\n'.join(lines[712:757])  # Phase 6 (with 6A prep + 6B execution)
ph7_content = '\n'.join(lines[758:806])  # Phase 7 (with 7A scheduling + 7B rebuttal)

all_phases = ph1_content + '\n' + ph2_content + '\n' + ph3_content + '\n' + ph4_content + '\n' + ph5_content + '\n' + ph6_content + '\n' + ph7_content

# --- PART B: From second copy (lines 1162-2107) ---
partb_content = '\n'.join(lines[1161:2109])

# --- PART C: From second copy (lines 2112-2265) ---
partc_content = '\n'.join(lines[2111:2265])

# --- APPROVAL: From second copy (lines 2268-) ---
# We'll build this fresh in shadcn style

# ============================================================
# Now apply transformations to extracted content
# ============================================================

def make_phase_card(num, title, badges_html, sla_text, body_html, card_id):
    """Create a shadcn phase card."""
    badge_str = badges_html
    body_converted = convert_content_block(body_html)
    return f'''
<div class="rounded-lg border border-border bg-card shadow-sm mb-4" id="{card_id}">
<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
  <h3 class="text-sm font-semibold text-foreground flex items-center gap-2"><span class="w-7 h-7 rounded-full bg-[#10b981] text-white text-xs font-bold flex items-center justify-center">{num}</span> {title}</h3>
  <div class="flex items-center gap-2 shrink-0">
    {badge_str}
    <span class="text-[11px] font-semibold text-muted-foreground bg-muted px-2 py-0.5 rounded">{sla_text}</span>
    <svg class="w-4 h-4 text-muted-foreground transition-transform" data-chevron fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
  </div>
</button>
<div class="border-t border-border px-5 py-5 hidden" data-card-body>
{body_converted}
</div>
</div>'''

def make_metric_card(icon, title, body_html, card_id):
    """Create a shadcn metric card for Part B."""
    body_converted = convert_content_block(body_html)
    return f'''
<div class="rounded-lg border border-border bg-card shadow-sm mb-4" id="{card_id}">
<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
  <h3 class="text-sm font-semibold text-foreground flex items-center gap-2"><span class="w-7 h-7 rounded-full bg-[#10b981] text-white text-xs font-bold flex items-center justify-center">{icon}</span> {title}</h3>
  <div class="flex items-center gap-2 shrink-0">
    <svg class="w-4 h-4 text-muted-foreground transition-transform" data-chevron fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
  </div>
</button>
<div class="border-t border-border px-5 py-5 hidden" data-card-body>
{body_converted}
</div>
</div>'''

# ============================================================
# Extract phase card bodies from original and rebuild
# ============================================================

# Instead of parsing each card individually (which is fragile), let's take the full
# sections and do bulk string replacements on the entire content

# Combine all content sections
full_content = '\n'.join(lines[300:588]) + '\n'  # Part A phases 1-3
full_content += '\n'.join(lines[590:808]) + '\n'  # Part A phases 4-7 (detailed)
full_content += '\n'.join(lines[1161:2109]) + '\n'  # Part B (detailed phase-cards)
full_content += '\n'.join(lines[2111:2265]) + '\n'  # Part C (detailed)

# Apply all content conversions
full_content = convert_content_block(full_content)

# Now convert phase-card structure to shadcn card structure
# Old: <div class="phase-card( open)?" id="xxx">
# New: <div class="rounded-lg border border-border bg-card shadow-sm mb-4" id="xxx">
full_content = re.sub(r'<div class="phase-card(?:\s+open)?" id="(\w+)">',
                       r'<div class="rounded-lg border border-border bg-card shadow-sm mb-4" id="\1">', full_content)

# Old: <div class="phase-card-header" onclick="toggleCard(this)">
# New: <button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
full_content = full_content.replace(
    '<div class="phase-card-header" onclick="toggleCard(this)">',
    '<button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">'
)

# Close the button (replace the closing div of phase-card-header)
# The header pattern is: <div class="phase-card-header"...>...<h3>...</h3>...<div style="display:flex...">...</div>\n</div>
# We need to replace the </div> that closes phase-card-header with </button>
# This is tricky - the toggle-icon span followed by </div>\n</div> pattern
full_content = re.sub(r'<span class="toggle-icon">&#8964;</span>\s*</div>\s*</div>',
    '<svg class="w-4 h-4 text-muted-foreground transition-transform" data-chevron fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>\n  </div>\n</button>',
    full_content)

# Also handle toggle-icon that's a direct child (not inside a div)
full_content = re.sub(r'<span class="toggle-icon">&#8964;</span>\s*</div>',
    '<svg class="w-4 h-4 text-muted-foreground transition-transform" data-chevron fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>\n</button>',
    full_content)

# Phase card body: old -> new
full_content = full_content.replace(
    '<div class="phase-card-body">',
    '<div class="border-t border-border px-5 py-5 hidden" data-card-body>'
)

# Phase numbers - replace old style
full_content = re.sub(r'<span class="phase-num">(\d+)</span>',
    r'<span class="w-7 h-7 rounded-full bg-[#10b981] text-white text-xs font-bold flex items-center justify-center">\1</span>',
    full_content)
# Phase nums with icons (Part B)
full_content = re.sub(r'<span class="phase-num">(&#\d+;|[^<]+)</span>',
    r'<span class="w-7 h-7 rounded-full bg-[#10b981] text-white text-xs font-bold flex items-center justify-center">\1</span>',
    full_content)

# Phase card h3 - add flex classes
full_content = re.sub(r'(<button[^>]*>)\s*<h3>',
    r'\1\n  <h3 class="text-sm font-semibold text-foreground flex items-center gap-2">',
    full_content)

# Phase SLA badges
full_content = re.sub(r'<span class="phase-sla">([^<]+)</span>',
    r'<span class="text-[11px] font-semibold text-muted-foreground bg-muted px-2 py-0.5 rounded">\1</span>',
    full_content)

# Fix inline style div wrappers for badge groups
full_content = re.sub(r'<div style="display:flex;gap:8px;align-items:center">',
    '<div class="flex items-center gap-2 shrink-0">', full_content)

# Part headers
full_content = re.sub(r'<div class="part-header">\s*<h2>([^<]+)</h2>\s*<p>([^<]+)</p>\s*</div>',
    r'<div class="bg-primary text-primary-foreground px-6 py-4 rounded-t-lg mt-10">\n  <h2 class="text-lg font-bold">\1</h2>\n  <p class="text-sm text-primary-foreground/70 mt-0.5">\2</p>\n</div>',
    full_content)

# Section parts
full_content = re.sub(r'<section class="part" id="(\w+)">', r'<section id="\1">', full_content)

# Tabs nav
full_content = re.sub(r'<div class="tabs-nav">',
    '<div class="flex gap-1 bg-muted p-1 rounded-lg mb-6">', full_content)

# Tab buttons - active
full_content = re.sub(r'<button class="tab-btn active"',
    '<button class="tab-btn px-4 py-2 text-sm font-medium rounded-md bg-card text-foreground shadow-sm"', full_content)
# Tab buttons - inactive
full_content = re.sub(r'<button class="tab-btn"(?!\s+px)',
    '<button class="tab-btn px-4 py-2 text-sm font-medium rounded-md text-muted-foreground hover:text-foreground transition-colors"', full_content)

# Tab panes
full_content = full_content.replace('<div class="tab-pane active"', '<div class="tab-pane active"')
full_content = full_content.replace('<div class="tab-pane"', '<div class="tab-pane" style="display:none"')

# Fix remaining table wraps that aren't yet wrapped
full_content = re.sub(r'<div class="table-wrap">\s*(<table)', r'<div class="rounded-md border border-border overflow-hidden">\1', full_content)

# Clean up any remaining old classes
full_content = re.sub(r'<div class="sub-section">\s*<h4', '<div class="mt-4 mb-3">\n    <h4', full_content)

# Fix h3/h4 inside sub-sections that already got converted
full_content = re.sub(r'<h3 class="text-sm font-bold text-foreground mb-3 pb-2 border-b border-border">(\d+[A-Z]?:)',
    r'<h3 class="text-sm font-bold text-foreground mb-3 pb-2 border-b border-border">\1', full_content)

# ============================================================
# BUILD FINAL HTML
# ============================================================

head = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>BJB Expert &amp; Deposition — Litify Dev Specification</title>
<script src="https://cdn.tailwindcss.com"></script>
<script>
tailwind.config = {
  theme: {
    extend: {
      colors: {
        background: '#fafafa',
        foreground: '#0a0a0a',
        card: '#ffffff',
        'card-foreground': '#0a0a0a',
        primary: '#171717',
        'primary-foreground': '#fafafa',
        secondary: '#f5f5f5',
        'secondary-foreground': '#171717',
        muted: '#f5f5f5',
        'muted-foreground': '#737373',
        accent: '#f5f5f5',
        'accent-foreground': '#171717',
        destructive: '#ef4444',
        border: '#e5e5e5',
        input: '#e5e5e5',
        ring: '#0a0a0a',
        sidebar: '#fafafa',
        'sidebar-foreground': '#171717',
        'sidebar-accent': '#f5f5f5',
      },
      borderRadius: {
        lg: '0.625rem',
        md: '0.5rem',
        sm: '0.375rem',
      }
    }
  }
}
</script>
<style>
#tooltip-overlay{position:absolute;z-index:9999;background:#fff;border:1px solid #e5e5e5;border-radius:0.5rem;box-shadow:0 4px 16px rgba(0,0,0,0.12);padding:12px 14px;min-width:260px;max-width:340px;font-size:12px;color:#0a0a0a;line-height:1.5;pointer-events:none}
#tooltip-overlay strong{display:block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:0.4px;color:#171717;margin-bottom:6px}
#tooltip-overlay ul{padding-left:14px;margin:4px 0 0}
#tooltip-overlay li{margin-bottom:3px}
.info-popover{display:none}
@media print{aside,.phase-bar,nav{display:none!important}main{padding:20px!important}[data-card-body]{display:block!important}.tab-pane{display:block!important}.bg-primary{background:#171717!important;color:#fafafa!important;-webkit-print-color-adjust:exact}}
</style>
</head>
<body class="bg-background text-foreground font-[-apple-system,BlinkMacSystemFont,'Inter',sans-serif] text-sm leading-relaxed">
<nav class="sticky top-0 z-50 h-14 border-b border-border bg-card">
  <div class="max-w-[1460px] mx-auto h-full flex items-center justify-between px-6">
    <span class="text-sm font-semibold text-muted-foreground tracking-wide">BJB Litify Spec</span>
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
    <a href="index.html" class="block px-3 py-2 text-sm font-medium text-muted-foreground rounded-md hover:bg-accent hover:text-accent-foreground transition-colors no-underline">Case Opening</a>
    <a href="treatment-monitoring.html" class="block px-3 py-2 text-sm font-medium text-muted-foreground rounded-md hover:bg-accent hover:text-accent-foreground transition-colors no-underline">Treatment Monitoring</a>
    <a href="written-discovery.html" class="block px-3 py-2 text-sm font-medium text-muted-foreground rounded-md hover:bg-accent hover:text-accent-foreground transition-colors no-underline">Written Discovery</a>
    <a href="expert-deposition.html" class="block px-3 py-2 text-sm font-medium text-foreground bg-accent rounded-md no-underline">Expert &amp; Deposition</a>
  </div>
</nav>
<div class="flex h-[calc(100vh-3.5rem)]">
<aside class="hidden md:flex w-64 flex-col border-r border-border bg-card overflow-y-auto shrink-0">
  <div class="px-5 pt-6 pb-4 border-b border-border">
    <h2 class="text-xs font-bold text-foreground tracking-wide uppercase">BJB Expert &amp; Deposition</h2>
    <p class="text-[11px] text-muted-foreground mt-1">Litify Dev Spec v4.0</p>
  </div>
  <div class="py-3">
    <div class="px-5 py-1.5 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Part A — Process</div>
    <a class="sidebar-link block px-5 py-1.5 text-xs font-semibold text-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('partA')">Overview</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-purple-600 cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('preDiscQuestions')">&#9733; Pre-Discovery Questions</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-purple-600 cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('preDepoQuestions')">&#9733; Pre-Deposition Questions</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('ph1')">Phase 1: Non-Party Depos</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('ph2')">Phase 2: Defendant Depos</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('ph3')">Phase 3: Expert Retention</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('ph4')">Phase 4: Report Follow-Up</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('ph5')">Phase 5: Amended Reports</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('ph6')">Phase 6: Client Depo</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('ph7')">Phase 7: IME Mgmt</a>
  </div>
  <div class="py-3">
    <div class="px-5 py-1.5 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Part B — Metrics</div>
    <a class="sidebar-link block px-5 py-1.5 text-xs font-semibold text-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('partB')">Overview</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('scorecard')">Executive Scorecard</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('core-metrics')">15 Core Metrics</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('kpi-library')">KPI Library</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('sla-ladders')">SLA Enforcement</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('epi')">Expert Performance Index</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('risk-flags')">Risk Flags</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('dpi')">Defense Pressure Index</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('eli')">Expert Leverage Index</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('pressure-gap')">Pressure Gap</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('defense-signals')">Resistance Signals</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('settlement-engine')">Settlement Prediction</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('trial-readiness')">Trial Readiness</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('strategic-view')">Strategic Intelligence</a>
  </div>
  <div class="py-3">
    <div class="px-5 py-1.5 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Part C — Dev Spec</div>
    <a class="sidebar-link block px-5 py-1.5 text-xs font-semibold text-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('partC')">Overview</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('partC');setTab('tab-fields')">Litify Fields</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('partC');setTab('tab-flows')">Flows</a>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('partC');setTab('tab-rules')">Validation Rules</a>
  </div>
  <div class="py-3">
    <div class="px-5 py-1.5 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Parallel Tracks</div>
    <a class="sidebar-link block px-5 py-1.5 text-xs font-semibold text-foreground hover:bg-accent hover:text-accent-foreground transition-colors no-underline" href="index.html">Case Opening &rarr;</a>
    <a class="sidebar-link block px-5 py-1.5 text-xs font-semibold text-foreground hover:bg-accent hover:text-accent-foreground transition-colors no-underline" href="treatment-monitoring.html">Treatment Monitoring &rarr;</a>
    <a class="sidebar-link block px-5 py-1.5 text-xs font-semibold text-foreground hover:bg-accent hover:text-accent-foreground transition-colors no-underline" href="written-discovery.html">Written Discovery &rarr;</a>
  </div>
  <div class="py-3">
    <div class="px-5 py-1.5 text-[10px] font-bold uppercase tracking-widest text-muted-foreground">Sign-Off</div>
    <a class="sidebar-link block px-5 pl-7 py-1.5 text-xs text-muted-foreground cursor-pointer hover:bg-accent hover:text-accent-foreground transition-colors" onclick="navTo('approval')">Approval &amp; Notes</a>
  </div>
</aside>
<main class="flex-1 overflow-y-auto" id="main-scroll">
<div class="max-w-5xl px-8 py-10">
<div class="border-b-2 border-[#10b981] pb-8 mb-8">
  <h1 class="text-2xl font-bold text-foreground">BJB Expert &amp; Deposition &mdash; Litify Dev Specification</h1>
  <p class="text-sm text-muted-foreground mt-1">Expert Retention &nbsp;|&nbsp; Depositions &nbsp;|&nbsp; Report Management &nbsp;|&nbsp; IME Coordination</p>
  <span class="inline-block mt-3 px-3 py-0.5 text-xs font-medium border border-border rounded-full text-muted-foreground">v4.0 &bull; February 2026</span>
</div>
<div class="flex gap-2 mb-9 flex-wrap">
  <button class="px-3 py-2 bg-card border border-border rounded-md text-xs font-semibold text-foreground hover:bg-primary hover:text-primary-foreground transition-colors whitespace-nowrap" onclick="navTo('ph1')">1 &mdash; Non-Party Depos</button>
  <button class="px-3 py-2 bg-card border border-border rounded-md text-xs font-semibold text-foreground hover:bg-primary hover:text-primary-foreground transition-colors whitespace-nowrap" onclick="navTo('ph2')">2 &mdash; Defendant Depos</button>
  <button class="px-3 py-2 bg-card border border-border rounded-md text-xs font-semibold text-foreground hover:bg-primary hover:text-primary-foreground transition-colors whitespace-nowrap" onclick="navTo('ph3')">3 &mdash; Expert Retention</button>
  <button class="px-3 py-2 bg-card border border-border rounded-md text-xs font-semibold text-foreground hover:bg-primary hover:text-primary-foreground transition-colors whitespace-nowrap" onclick="navTo('ph4')">4 &mdash; Report Follow-Up</button>
  <button class="px-3 py-2 bg-card border border-border rounded-md text-xs font-semibold text-foreground hover:bg-primary hover:text-primary-foreground transition-colors whitespace-nowrap" onclick="navTo('ph5')">5 &mdash; Amended Reports</button>
  <button class="px-3 py-2 bg-card border border-border rounded-md text-xs font-semibold text-foreground hover:bg-primary hover:text-primary-foreground transition-colors whitespace-nowrap" onclick="navTo('ph6')">6 &mdash; Client Depo</button>
  <button class="px-3 py-2 bg-card border border-border rounded-md text-xs font-semibold text-foreground hover:bg-primary hover:text-primary-foreground transition-colors whitespace-nowrap" onclick="navTo('ph7')">7 &mdash; IME Mgmt</button>
  <button class="px-3 py-2 bg-purple-100 border border-purple-400 rounded-md text-xs font-semibold text-purple-800 transition-colors whitespace-nowrap" onclick="window.location.href='written-discovery.html'">&#9679; Written Discovery</button>
  <button class="px-3 py-2 bg-blue-100 border border-blue-400 rounded-md text-xs font-semibold text-blue-800 transition-colors whitespace-nowrap" onclick="window.location.href='index.html'">&#9679; Case Opening</button>
</div>
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

approval = '''
<!-- ============================================================ APPROVAL & NOTES -->
<section id="approval">
<div class="bg-primary text-primary-foreground px-6 py-4 rounded-t-lg mt-10">
  <h2 class="text-lg font-bold">Approval &amp; Notes</h2>
  <p class="text-sm text-primary-foreground/70 mt-0.5">Management Sign-Off and Session Notes</p>
</div>
<div class="rounded-lg border-2 border-border bg-card p-6 mt-4">
  <h3 class="text-base font-bold text-foreground mb-1">Management Approval Checklist</h3>
  <p class="text-sm text-muted-foreground mb-4">Approved by Ryan Broderick</p>
  <div id="sync-status" class="text-[11px] text-muted-foreground mb-3">Loading...</div>
  <div class="flex items-center gap-3 py-2.5 border-b border-border text-sm">
    <label class="flex items-center gap-2 cursor-pointer font-semibold text-foreground min-w-[280px]"><input type="checkbox" id="appr-a" data-key="partA" class="w-4 h-4 accent-primary"> <span></span> Part A &mdash; Process Phases Approved</label>
    <span class="text-[11px] text-muted-foreground ml-auto" id="appr-a-date"></span>
  </div>
  <div class="flex items-center gap-3 py-2.5 border-b border-border text-sm">
    <label class="flex items-center gap-2 cursor-pointer font-semibold text-foreground min-w-[280px]"><input type="checkbox" id="appr-b" data-key="partB" class="w-4 h-4 accent-primary"> <span></span> Part B &mdash; Metrics &amp; Scorecard Approved</label>
    <span class="text-[11px] text-muted-foreground ml-auto" id="appr-b-date"></span>
  </div>
  <div class="flex items-center gap-3 py-2.5 border-b border-border text-sm">
    <label class="flex items-center gap-2 cursor-pointer font-semibold text-foreground min-w-[280px]"><input type="checkbox" id="appr-c" data-key="partC" class="w-4 h-4 accent-primary"> <span></span> Part C &mdash; Dev Spec Approved</label>
    <span class="text-[11px] text-muted-foreground ml-auto" id="appr-c-date"></span>
  </div>
  <div class="flex items-center gap-3 py-2.5 text-sm">
    <label class="flex items-center gap-2 cursor-pointer font-semibold text-foreground min-w-[280px]"><input type="checkbox" id="appr-full" data-key="full" class="w-4 h-4 accent-primary"> <span></span> Full Expert &amp; Deposition Specification Approved</label>
    <span class="text-[11px] text-muted-foreground ml-auto" id="appr-full-date"></span>
  </div>
  <h3 class="text-base font-bold text-foreground mb-3 mt-6 pt-4 border-t border-border">Notes</h3>
  <textarea id="mgmt-notes" class="w-full min-h-[100px] border border-border rounded-md p-3 text-sm resize-y focus:outline-none focus:ring-2 focus:ring-ring" placeholder="Add management notes, feedback, or change requests here..."></textarea>
</div>
</section>
'''

footer = '''
</div>
</main>
</div>

<button id="back-to-top" class="fixed bottom-6 right-6 bg-primary text-primary-foreground border-none w-10 h-10 rounded-full cursor-pointer text-lg hidden items-center justify-center shadow-lg z-50 hover:bg-primary/90 transition-colors" onclick="document.getElementById('main-scroll').scrollTo({top:0,behavior:'smooth'})">&#8593;</button>

<script>
function toggleCard(header){
  var card=header.parentElement;
  var body=card.querySelector('[data-card-body]');
  var chevron=card.querySelector('[data-chevron]');
  if(body)body.classList.toggle('hidden');
  if(chevron)chevron.classList.toggle('rotate-180');
}

(function(){
  var tip=document.createElement('div');tip.id='tooltip-overlay';tip.style.display='none';document.body.appendChild(tip);
  var hideTimer=null;
  function show(btn){clearTimeout(hideTimer);var pop=btn.nextElementSibling;if(!pop||!pop.classList.contains('info-popover'))return;tip.innerHTML=pop.innerHTML;tip.style.display='block';var r=btn.getBoundingClientRect();var tw=340;var left=r.right-tw;if(left<8)left=8;if(left+tw>window.innerWidth-8)left=window.innerWidth-tw-8;tip.style.left=left+'px';tip.style.top=(r.bottom+window.pageYOffset+6)+'px';}
  function hide(){hideTimer=setTimeout(function(){tip.style.display='none';},120);}
  document.addEventListener('mouseover',function(e){var btn=e.target.closest('button[title="More detail"]');if(btn)show(btn);});
  document.addEventListener('mouseout',function(e){var btn=e.target.closest('button[title="More detail"]');if(btn)hide();});
})();

function navTo(id){
  var el=document.getElementById(id);var main=document.getElementById('main-scroll');
  if(el&&main){var mR=main.getBoundingClientRect();var eR=el.getBoundingClientRect();main.scrollTo({top:main.scrollTop+eR.top-mR.top-10,behavior:'smooth'});}
}

function setTab(id,btn){
  document.querySelectorAll('.tab-pane').forEach(function(p){p.classList.remove('active');p.style.display='none';});
  var t=document.getElementById(id);if(t){t.classList.add('active');t.style.display='block';}
  if(btn){btn.parentElement.querySelectorAll('.tab-btn').forEach(function(b){b.className='tab-btn px-4 py-2 text-sm font-medium rounded-md text-muted-foreground hover:text-foreground transition-colors';});btn.className='tab-btn px-4 py-2 text-sm font-medium rounded-md bg-card text-foreground shadow-sm';}
}

document.querySelectorAll('.tab-pane').forEach(function(p){if(!p.classList.contains('active'))p.style.display='none';});

var mainScroll=document.getElementById('main-scroll');
if(mainScroll){mainScroll.addEventListener('scroll',function(){var btn=document.getElementById('back-to-top');btn.style.display=mainScroll.scrollTop>300?'flex':'none';});}

(function(){
  var links=document.querySelectorAll('.sidebar-link');
  var sections=['partA','preDiscQuestions','preDepoQuestions','ph1','ph2','ph3','ph4','ph5','ph6','ph7','partB','scorecard','core-metrics','kpi-library','sla-ladders','epi','risk-flags','dpi','eli','pressure-gap','defense-signals','settlement-engine','trial-readiness','strategic-view','partC','approval'];
  var main=document.getElementById('main-scroll');if(!main)return;
  function spy(){var current='';sections.forEach(function(id){var el=document.getElementById(id);if(el){var r=el.getBoundingClientRect();var mR=main.getBoundingClientRect();if(r.top-mR.top<=120)current=id;}});
  links.forEach(function(l){l.classList.remove('bg-accent','text-accent-foreground');var oc=l.getAttribute('onclick')||'';if(oc.indexOf("'"+current+"'")>-1)l.classList.add('bg-accent','text-accent-foreground');});}
  main.addEventListener('scroll',spy);
})();

document.addEventListener('click',function(e){var mn=document.getElementById('mobile-nav');var nb=document.getElementById('nav-hamburger');if(mn&&!mn.classList.contains('hidden')&&!mn.contains(e.target)&&e.target!==nb&&!nb.contains(e.target))mn.classList.add('hidden');});

function getCaseGrade() {
  return parseInt(localStorage.getItem('bjb-case-grade') || localStorage.getItem('bjb-case-tier') || '1');
}

function updateProgress(containerId, progressId) {
  var container = document.getElementById(containerId);
  var progress = document.getElementById(progressId);
  if (!container || !progress) return;
  var cbs = container.querySelectorAll('input[type="checkbox"][data-key]');
  var checked = 0;
  cbs.forEach(function(cb) { if (cb.checked) checked++; });
  progress.textContent = checked + ' / ' + cbs.length;
}

document.addEventListener('DOMContentLoaded',function(){
  ['ph1','scorecard'].forEach(function(id){var card=document.getElementById(id);if(card){var body=card.querySelector('[data-card-body]');if(body)body.classList.remove('hidden');var chev=card.querySelector('[data-chevron]');if(chev)chev.classList.add('rotate-180');}});

  var grade = getCaseGrade();
  document.querySelectorAll('[data-grade-required]').forEach(function(section) {
    var req = parseInt(section.getAttribute('data-grade-required'));
    var badge = section.querySelector('.grade-badge');
    if (grade < req) {
      if (badge) badge.textContent = 'Optional';
      section.classList.add('opacity-60');
    }
  });

  updateProgress('preDiscQuestions', 'preDiscProgress');
  updateProgress('preDepoQuestions', 'preDepoProgress');

  document.querySelectorAll('#preDiscQuestions input[type="checkbox"][data-key], #preDepoQuestions input[type="checkbox"][data-key]').forEach(function(cb) {
    cb.addEventListener('change', function() {
      updateProgress('preDiscQuestions', 'preDiscProgress');
      updateProgress('preDepoQuestions', 'preDepoProgress');
      debounceSave(300);
    });
  });
});
</script>
<script type="module">
import{neon}from'https://esm.sh/@neondatabase/serverless';
const sql=neon('postgresql://neondb_owner:npg_rwK4vVmAyzG5@ep-mute-cloud-aik2rpsg.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require');
const PAGE_ID='expert-deposition',statusEl=document.getElementById('sync-status'),notesEl=document.getElementById('mgmt-notes'),checkboxes=document.querySelectorAll('input[type="checkbox"][data-key]');
function setStatus(t,c){if(statusEl){statusEl.textContent=t;statusEl.style.color=c||'#737373';}}
let saveTimer=null;function debounceSave(ms=500){clearTimeout(saveTimer);saveTimer=setTimeout(saveState,ms);}
async function ensureTable(){await sql`CREATE TABLE IF NOT EXISTS spec_approvals(page_id TEXT PRIMARY KEY,checkboxes JSONB NOT NULL DEFAULT '{}',notes TEXT DEFAULT '',updated_at TIMESTAMPTZ DEFAULT now())`;}
function gatherState(){const s={};checkboxes.forEach(cb=>{const k=cb.dataset.key,d=document.getElementById(cb.id+'-date');s[k]={checked:cb.checked,date:d?d.textContent:''};});return{checkboxes:s,notes:notesEl?notesEl.value:''};}
async function saveState(){try{setStatus('Saving...','#737373');const s=gatherState();await sql`INSERT INTO spec_approvals(page_id,checkboxes,notes,updated_at)VALUES(${PAGE_ID},${JSON.stringify(s.checkboxes)},${s.notes},now())ON CONFLICT(page_id)DO UPDATE SET checkboxes=${JSON.stringify(s.checkboxes)},notes=${s.notes},updated_at=now()`;setStatus('Saved','#2e7d32');}catch(e){console.error(e);setStatus('Save failed','#c62828');}}
async function loadState(){try{await ensureTable();const rows=await sql`SELECT checkboxes,notes FROM spec_approvals WHERE page_id=${PAGE_ID}`;if(rows.length>0){const{checkboxes:cb,notes}=rows[0];if(cb)checkboxes.forEach(c=>{const k=c.dataset.key;if(cb[k]){c.checked=cb[k].checked||false;const d=document.getElementById(c.id+'-date');if(d)d.textContent=cb[k].date||'';}});if(notesEl&&notes)notesEl.value=notes;}setStatus('Synced','#2e7d32');}catch(e){console.error(e);setStatus('Offline','#c62828');}}
checkboxes.forEach(cb=>{cb.addEventListener('change',()=>{const d=document.getElementById(cb.id+'-date');if(d)d.textContent=cb.checked?'Approved: '+new Date().toLocaleString():'';debounceSave(300);});});
if(notesEl)notesEl.addEventListener('input',()=>debounceSave(500));
loadState();
</script>
</body>
</html>
'''

rsquo = '\u2019'
mdash = '\u2014'

dd_q1 = question_item("ed-dd-q1", 1, f"What key facts or admissions are you hoping to lock in from this witness that we can{rsquo}t get otherwise?")
dd_q2 = question_item("ed-dd-q2", 2, f"What risk or downside exists if we don{rsquo}t depose this person before trial or settlement discussions?")
dd_q3 = question_item("ed-dd-q3", 3, f"How does this deposition align with our overall case strategy{mdash}for example, will it impact settlement leverage or trial prep?")
dd_q4 = question_item("ed-dd-q4", 4, f"Have you identified any alternative means of getting the same information{mdash}like documents or interrogatories{mdash}without the deposition?")
dd_q5 = question_item("ed-dd-q5", 5, f"How does the cost{mdash}both time and resources{mdash}of this deposition compare to the value it{rsquo}s expected to deliver for the case outcome?")

pre_phase_questions = f'''
<div class="rounded-lg border-2 border-purple-200 bg-card shadow-sm mb-4" id="preDiscQuestions" data-grade-required="2">
  <button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
    <h3 class="text-sm font-semibold text-foreground flex items-center gap-3">
      <span class="w-7 h-7 rounded-full bg-[#8b5cf6] text-white text-xs font-bold inline-flex items-center justify-center shrink-0">&#9733;</span>
      Questions Before Written Discovery
    </h3>
    <div class="flex items-center gap-2 shrink-0">
      <span class="badge">Attorney</span>
      <span class="badge grade-badge">Required (Grade 2+)</span>
      <span class="text-xs text-muted-foreground" id="preDiscProgress">0 / 5</span>
      <svg data-chevron class="w-5 h-5 text-muted-foreground transition-transform duration-200 rotate-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
    </div>
  </button>
  <div data-card-body class="px-6 py-5 border-t border-border hidden">
    <div class="space-y-2">
      {question_item("ed-wd-q1", 1, "What specific element of liability or damages are you trying to prove or disprove with this discovery set?")}
      {question_item("ed-wd-q2", 2, "What defense theory are you anticipating, and how does this discovery box them in?")}
      {question_item("ed-wd-q3", 3, "If the opposing party responds evasively or incompletely, what is your follow-up plan?")}
      {question_item("ed-wd-q4", 4, "How will these discovery responses shape your deposition outline or trial strategy?")}
      {question_item("ed-wd-q5", 5, "What settlement leverage will this discovery create if answered favorably?")}
    </div>
  </div>
</div>

<div class="rounded-lg border-2 border-purple-200 bg-card shadow-sm mb-4" id="preDepoQuestions" data-grade-required="2">
  <button onclick="toggleCard(this)" class="w-full flex items-center justify-between px-5 py-4 hover:bg-accent/50 transition-colors text-left">
    <h3 class="text-sm font-semibold text-foreground flex items-center gap-3">
      <span class="w-7 h-7 rounded-full bg-[#8b5cf6] text-white text-xs font-bold inline-flex items-center justify-center shrink-0">&#9733;</span>
      Questions Before Deposition Decisions
    </h3>
    <div class="flex items-center gap-2 shrink-0">
      <span class="badge">Attorney</span>
      <span class="badge grade-badge">Required (Grade 2+)</span>
      <span class="text-xs text-muted-foreground" id="preDepoProgress">0 / 5</span>
      <svg data-chevron class="w-5 h-5 text-muted-foreground transition-transform duration-200 rotate-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/></svg>
    </div>
  </button>
  <div data-card-body class="px-6 py-5 border-t border-border hidden">
    <div class="space-y-2">
      {dd_q1}
      {dd_q2}
      {dd_q3}
      {dd_q4}
      {dd_q5}
    </div>
  </div>
</div>
'''

# Assemble final output
output = head + pre_phase_questions + full_content + approval + footer

# Write to file
with open('/Users/daustmac/Documents/case-opening-flow/expert-deposition.html', 'w') as f:
    f.write(output)

print(f"Written {len(output)} characters to expert-deposition.html")
print(f"Line count: {output.count(chr(10))}")
