"""
Build a self-contained static HTML coding app per pair.
One HTML file = one URL. No server required. Coders' codes saved to
localStorage AND (optionally) POSTed to a Google Apps Script web app
that writes one row per (coder, item_id) into a Google Sheet.

Usage: python3 build_static_app.py
"""
import json
from pathlib import Path

OUT_DIR = Path('/Users/mwack/Desktop/Paper2_Static_App')
OUT_DIR.mkdir(exist_ok=True)

# Google Apps Script web app URL. Leave as '' to disable sheet sync (codes
# only land in localStorage and the downloaded CSV). To enable: deploy
# `apps_script.gs` as a web app (Execute as: Me, Anyone with the link),
# paste the resulting /exec URL here, and re-run this script.
SHEETS_ENDPOINT = 'https://script.google.com/macros/s/AKfycbyjua4ZBIVRtIrQUZAZvgDvhaAbZmhEVKkeO0TjNcdSYdS45fMyVfTB-Em4azbciGUuhQ/exec'

# Pair sources
PAIRS = {
    'pair1': '/Users/mwack/Desktop/Paper2_Coding_App_Pair1',
    'pair2': '/Users/mwack/Desktop/Paper2_Coding_App_Pair2',
}

HTML_TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{project_name}</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{ font-family: -apple-system, system-ui, "Helvetica Neue", Helvetica, Arial, sans-serif;
         margin: 0; background: #f6f7f8; color: #222; line-height: 1.5; }}
  .wrap {{ display: grid; grid-template-columns: 280px 1fr; min-height: 100vh; }}
  .side {{ background: #fff; border-right: 1px solid #ddd; padding: 18px; }}
  .main {{ padding: 24px 32px; max-width: 980px; }}
  h1 {{ font-size: 1.15em; margin: 0 0 6px; }}
  h2 {{ font-size: 1em; margin: 18px 0 6px; color: #333; }}
  h3 {{ font-size: 0.95em; margin: 16px 0 4px; }}
  .pill {{ display: inline-block; background: #eef; padding: 2px 9px; border-radius: 10px;
          font-size: 0.78em; margin-right: 6px; color: #335; }}
  .box {{ background: #fff; border: 1px solid #ddd; border-radius: 6px; padding: 14px 18px;
         font-size: 0.95em; max-height: 50vh; overflow-y: auto; white-space: pre-wrap; word-wrap: break-word; }}
  .yellow {{ background: #fffbe6; }}
  .blue {{ background: #e6f4ff; }}
  .grey {{ background: #f6f6f6; color: #555; font-size: 0.88em; }}
  label.radio {{ display: inline-block; margin: 4px 14px 4px 0; cursor: pointer; }}
  label.radio input {{ margin-right: 4px; }}
  .help {{ color: #666; font-size: 0.85em; margin: 2px 0 6px; }}
  textarea {{ width: 100%; font-family: inherit; font-size: 0.92em; padding: 8px;
             border: 1px solid #ccc; border-radius: 4px; min-height: 50px; }}
  button {{ font-family: inherit; font-size: 0.92em; padding: 8px 16px; border-radius: 4px;
           border: 1px solid #999; background: #fff; cursor: pointer; }}
  button.primary {{ background: #2563eb; color: #fff; border-color: #2563eb; font-weight: 600; }}
  button.primary:hover {{ background: #1d4ed8; }}
  button.danger {{ color: #c00; border-color: #c00; }}
  .nav {{ margin: 18px 0; display: flex; gap: 8px; align-items: center; }}
  .nav button {{ flex: 1; }}
  .progress-bar {{ height: 8px; background: #e5e5e5; border-radius: 4px; overflow: hidden; }}
  .progress-bar > div {{ background: #2563eb; height: 100%; transition: width 0.2s; }}
  #login {{ background: #fffbe6; padding: 30px; border-radius: 6px; max-width: 460px; margin: 80px auto;
            text-align: center; border: 1px solid #f0d97a; }}
  #login input {{ font-size: 1em; padding: 8px; width: 80%; margin: 12px 0; }}
  .codes {{ background: #fafafa; border: 1px solid #ddd; border-radius: 6px; padding: 12px; margin-top: 12px; }}
  hr {{ border: none; border-top: 1px solid #e5e5e5; margin: 16px 0; }}
  .small {{ font-size: 0.82em; color: #777; }}
  details {{ margin-top: 14px; }}
  summary {{ cursor: pointer; font-size: 0.88em; color: #333; }}
  details > div {{ margin-top: 8px; }}
  #sync-status {{ display: inline-block; margin-left: 12px; font-size: 0.85em; }}
  .sync-ok {{ color: #080; }}
  .sync-pending {{ color: #a60; }}
  .sync-error {{ color: #c00; }}
</style>
</head>
<body>

<div id="login">
  <h1>{project_name}</h1>
  <p>Sign in with your assigned coder name.</p>
  <input id="coder-name" placeholder="e.g. coder1" autocomplete="off">
  <br>
  <button class="primary" onclick="login()">Start coding</button>
  <p class="small" style="margin-top: 24px;">
    Your progress is saved automatically in this browser and (if a sheet
    endpoint is configured) posted to a shared Google Sheet on every save.
    Use the same browser for the whole task. Codes do not sync across
    browsers or devices through localStorage, but anything that reaches
    the sheet is safe regardless of which browser you used.
  </p>
</div>

<div id="app" style="display: none;">
<div class="wrap">
  <div class="side">
    <h1>{project_name}</h1>
    <div class="small">Coder: <b id="who"></b> &middot; <a href="#" onclick="logout(); return false;">switch</a></div>
    <hr>

    <h2>Progress</h2>
    <div class="small"><span id="progress-text"></span></div>
    <div class="progress-bar"><div id="progress-bar-inner" style="width: 0%;"></div></div>
    <div class="small" id="sync-counter" style="margin-top: 6px;"></div>

    <hr>
    <h2>Navigate</h2>
    <div class="nav">
      <button onclick="prev()">&larr; Prev</button>
      <button onclick="next()">Next &rarr;</button>
    </div>
    <input id="jump" type="number" min="1" max="{n_items}" placeholder="Jump to #" style="width: 70%; padding: 4px;">
    <button onclick="jump()">Go</button>

    <hr>
    <button onclick="syncAll()" id="sync-all-btn" class="primary" style="width: 100%;">Sync unsynced to sheet</button>
    <button onclick="downloadCsv()" style="width: 100%; margin-top: 6px;">Download my codes (CSV)</button>
    <button onclick="if(confirm('Clear ALL your codes? This cannot be undone.')) clearCodes();" class="danger" style="width: 100%; margin-top: 6px;">Reset (clears codes)</button>

    <hr>
    <details>
      <summary>Codebook reminder</summary>
      <div class="small">
        <b>Q1.</b> Does the comment address the claim's content (evidence, logic, mechanism, actor, or framing)?<br>
        <i>No &rarr; OFF.</i><br>
        <i>Yes &rarr; Q2.</i>
        <br><br>
        <b>Q2.</b> Net-add or net-push-back?<br>
        <i>Add &rarr; BUILD.</i><br>
        <i>Push back &rarr; Q3.</i>
        <br><br>
        <b>Q3.</b> Does the pushback give the community something specific to work with?<br>
        <i>Yes &rarr; CHALLENGE.</i><br>
        <i>No &rarr; DISMISS.</i>
        <br><br>
        Full instructions in the PDF you were sent.
      </div>
    </details>
  </div>

  <div class="main">
    <div id="meta" style="margin-bottom: 12px;"></div>

    <h2>Thread title</h2>
    <div class="box grey" id="title"></div>

    <h2>Parent / context (what this comment is replying to)</h2>
    <div class="box yellow" id="parent"></div>

    <h2>Comment to code</h2>
    <div class="box" id="body"></div>

    <h2>Apply the decision tree (Q1 &rarr; Q2 &rarr; Q3)</h2>

    <div id="dvs"></div>

    <h3>Notes (optional)</h3>
    <textarea id="notes" placeholder="Flag anything confusing or worth discussing"></textarea>

    <div style="margin-top: 18px;">
      <button class="primary" onclick="saveAndNext()">Save and next</button>
      <button onclick="saveOnly()">Save (stay)</button>
      <span id="sync-status"></span>
    </div>

    <div class="small" style="margin-top: 14px;">
      Saves go to your browser's local storage and (if configured) to the shared Google Sheet.
      The sidebar counter tracks how many of your coded items have reached the sheet.
    </div>
  </div>
</div>
</div>

<script>
const ITEMS = {items_json};
const CODEBOOK = {codebook_json};
const PROJECT = {project_quoted};
const PAIR = {pair_quoted};
const SHEETS_ENDPOINT = {endpoint_quoted};

const LS_KEY = (k) => `paper2_${{PAIR}}_${{k}}`;

let coder = null;
let idx = 0;

function login() {{
  const name = document.getElementById('coder-name').value.trim().replace(/[^A-Za-z0-9_-]/g, '_');
  if (!name) {{ alert('Please type your name'); return; }}
  coder = name;
  localStorage.setItem(LS_KEY('coder'), name);
  idx = parseInt(localStorage.getItem(LS_KEY(`idx_${{name}}`)) || '0', 10);
  document.getElementById('login').style.display = 'none';
  document.getElementById('app').style.display = 'block';
  document.getElementById('who').textContent = coder;
  render();
}}

function logout() {{
  if (!confirm('Sign out? Your codes are still saved in this browser.')) return;
  coder = null;
  document.getElementById('login').style.display = 'block';
  document.getElementById('app').style.display = 'none';
}}

function loadCodes() {{
  return JSON.parse(localStorage.getItem(LS_KEY(`codes_${{coder}}`)) || '{{}}');
}}

function saveCodesObj(obj) {{
  localStorage.setItem(LS_KEY(`codes_${{coder}}`), JSON.stringify(obj));
}}

function loadSynced() {{
  return JSON.parse(localStorage.getItem(LS_KEY(`synced_${{coder}}`)) || '{{}}');
}}

function markSynced(item_id) {{
  const s = loadSynced();
  s[item_id] = new Date().toISOString();
  localStorage.setItem(LS_KEY(`synced_${{coder}}`), JSON.stringify(s));
  updateSyncCounter();
}}

function clearCodes() {{
  if (!coder) return;
  localStorage.removeItem(LS_KEY(`codes_${{coder}}`));
  localStorage.removeItem(LS_KEY(`idx_${{coder}}`));
  localStorage.removeItem(LS_KEY(`synced_${{coder}}`));
  idx = 0;
  render();
}}

function setSyncStatus(state, msg) {{
  const el = document.getElementById('sync-status');
  if (!el) return;
  el.className = '';
  if (state === 'pending') {{ el.textContent = 'Syncing to sheet...'; el.classList.add('sync-pending'); }}
  else if (state === 'ok') {{ el.textContent = 'Saved and synced'; el.classList.add('sync-ok'); }}
  else if (state === 'error') {{ el.textContent = 'Saved locally, sheet sync failed (will retry on Sync button)'; el.classList.add('sync-error'); }}
  else if (state === 'local') {{ el.textContent = 'Saved locally (no sheet endpoint configured)'; }}
  else {{ el.textContent = msg || ''; }}
}}

function updateSyncCounter() {{
  const el = document.getElementById('sync-counter');
  if (!el) return;
  const total = ITEMS.length;
  const codedCount = Object.keys(loadCodes()).length;
  if (!SHEETS_ENDPOINT) {{
    el.textContent = `${{codedCount}} / ${{total}} coded (local only)`;
    return;
  }}
  const syncedCount = Object.keys(loadSynced()).length;
  el.textContent = `${{syncedCount}} / ${{codedCount}} coded items reached the sheet`;
}}

function syncOne(item_id, codes) {{
  if (!SHEETS_ENDPOINT) {{ setSyncStatus('local'); return Promise.resolve(false); }}
  setSyncStatus('pending');
  const item = ITEMS.find(x => x.item_id === item_id);
  const payload = {{
    item_id: item_id,
    community: item ? (item.system || '') : '',
    coder: coder,
    pair: PAIR,
    timestamp: codes.timestamp || new Date().toISOString(),
    type: codes.type || '',
    challenge_direction: codes.challenge_direction || '',
    coherence_shift: codes.coherence_shift || '',
    notes: codes.notes || ''
  }};
  return fetch(SHEETS_ENDPOINT, {{
    method: 'POST',
    headers: {{ 'Content-Type': 'text/plain;charset=utf-8' }},
    body: JSON.stringify(payload)
  }})
  .then(r => r.json())
  .then(j => {{
    if (j && j.ok) {{ markSynced(item_id); setSyncStatus('ok'); return true; }}
    setSyncStatus('error', j && j.error);
    return false;
  }})
  .catch(err => {{ setSyncStatus('error', err.message); return false; }});
}}

async function syncAll() {{
  if (!SHEETS_ENDPOINT) {{ alert('No sheet endpoint configured for this build.'); return; }}
  const all = loadCodes();
  const synced = loadSynced();
  const pending = Object.keys(all).filter(id => !synced[id]);
  if (pending.length === 0) {{ alert('All coded items have already reached the sheet.'); return; }}
  if (!confirm(`Push ${{pending.length}} unsynced item(s) to the sheet now?`)) return;
  const btn = document.getElementById('sync-all-btn');
  btn.disabled = true;
  let ok = 0, fail = 0;
  for (const id of pending) {{
    const success = await syncOne(id, all[id]);
    if (success) ok++; else fail++;
  }}
  btn.disabled = false;
  alert(`Sync done. ${{ok}} reached the sheet, ${{fail}} failed (still saved locally — try again later).`);
}}

function render() {{
  const item = ITEMS[idx];
  const all = loadCodes();
  const prior = all[item.item_id] || {{}};

  document.getElementById('meta').innerHTML =
    `<span class="pill">Item ${{idx + 1}} of ${{ITEMS.length}}</span>`
    + `<span class="pill">ID: ${{item.item_id}}</span>`
    + `<span class="pill">Community: ${{item.system}}</span>`
    + `<span class="pill">${{item.framing || ''}}</span>`;

  document.getElementById('title').textContent = item.claim_text || '(no thread title)';
  document.getElementById('parent').textContent = item.query || '(top-level comment)';
  document.getElementById('body').textContent = item.response_text || '';
  document.getElementById('notes').value = prior.notes || '';

  const dvWrap = document.getElementById('dvs');
  dvWrap.innerHTML = '';
  CODEBOOK.dvs.forEach(dv => {{
    const d = document.createElement('div');
    d.style.marginTop = '14px';
    const label = document.createElement('div');
    label.innerHTML = `<b>${{dv.label}}</b>`;
    d.appendChild(label);
    if (dv.help) {{
      const help = document.createElement('div');
      help.className = 'help';
      help.textContent = dv.help;
      d.appendChild(help);
    }}
    dv.options.forEach(opt => {{
      const id = `${{dv.name}}_${{opt.value}}`;
      const lbl = document.createElement('label');
      lbl.className = 'radio';
      const radio = document.createElement('input');
      radio.type = 'radio';
      radio.name = dv.name;
      radio.value = opt.value;
      radio.id = id;
      if (prior[dv.name] === opt.value) radio.checked = true;
      lbl.appendChild(radio);
      lbl.appendChild(document.createTextNode(' ' + opt.label));
      d.appendChild(lbl);
    }});
    dvWrap.appendChild(d);
  }});

  const total = ITEMS.length;
  const done = Object.keys(all).length;
  document.getElementById('progress-text').textContent = `${{done}} / ${{total}} items coded (${{Math.round(100 * done / total)}}%)`;
  document.getElementById('progress-bar-inner').style.width = (100 * done / total) + '%';
  updateSyncCounter();

  document.getElementById('jump').value = idx + 1;
  localStorage.setItem(LS_KEY(`idx_${{coder}}`), idx);
  setSyncStatus('clear');
  window.scrollTo(0, 0);
}}

function collect() {{
  const item = ITEMS[idx];
  const out = {{}};
  CODEBOOK.dvs.forEach(dv => {{
    const sel = document.querySelector(`input[name="${{dv.name}}"]:checked`);
    out[dv.name] = sel ? sel.value : '';
  }});
  out.notes = document.getElementById('notes').value;
  out.timestamp = new Date().toISOString();
  return {{ item_id: item.item_id, codes: out }};
}}

function saveCurrent() {{
  const {{ item_id, codes }} = collect();
  const all = loadCodes();
  all[item_id] = codes;
  saveCodesObj(all);
  const synced = loadSynced();
  delete synced[item_id];
  localStorage.setItem(LS_KEY(`synced_${{coder}}`), JSON.stringify(synced));
  syncOne(item_id, codes);
}}

function saveAndNext() {{
  saveCurrent();
  if (idx < ITEMS.length - 1) idx++;
  render();
}}

function saveOnly() {{
  saveCurrent();
}}

function prev() {{ if (idx > 0) {{ idx--; render(); }} }}
function next() {{ if (idx < ITEMS.length - 1) {{ idx++; render(); }} }}
function jump() {{
  const v = parseInt(document.getElementById('jump').value, 10);
  if (!isNaN(v) && v >= 1 && v <= ITEMS.length) {{ idx = v - 1; render(); }}
}}

function downloadCsv() {{
  const all = loadCodes();
  const dvNames = CODEBOOK.dvs.map(d => d.name);
  const fields = ['item_id', 'community', 'coder', 'timestamp', ...dvNames, 'notes'];
  const lines = [fields.join(',')];
  ITEMS.forEach(item => {{
    const c = all[item.item_id] || {{}};
    const row = [
      item.item_id,
      item.system || '',
      coder,
      c.timestamp || '',
      ...dvNames.map(n => c[n] || ''),
      (c.notes || '').replace(/"/g, '""')
    ];
    lines.push(row.map(v => {{
      const s = String(v == null ? '' : v);
      return /[",\\n]/.test(s) ? `"${{s}}"` : s;
    }}).join(','));
  }});
  const blob = new Blob([lines.join('\\n')], {{ type: 'text/csv' }});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `${{coder}}_${{PAIR}}_codes.csv`;
  document.body.appendChild(a);
  a.click();
  setTimeout(() => {{ URL.revokeObjectURL(a.href); a.remove(); }}, 100);
}}

window.addEventListener('load', () => {{
  const saved = localStorage.getItem(LS_KEY('coder'));
  if (saved) {{
    document.getElementById('coder-name').value = saved;
  }}
}});
</script>
</body>
</html>
'''


for pair_id, pair_dir in PAIRS.items():
    items = json.load(open(f'{pair_dir}/data/items.json'))
    codebook = json.load(open(f'{pair_dir}/data/codebook.json'))
    project_name = codebook.get('project_name', f'Coding App {pair_id}')

    html = HTML_TEMPLATE.format(
        project_name=project_name,
        n_items=len(items),
        items_json=json.dumps(items),
        codebook_json=json.dumps(codebook),
        project_quoted=json.dumps(project_name),
        pair_quoted=json.dumps(pair_id),
        endpoint_quoted=json.dumps(SHEETS_ENDPOINT),
    )
    out_path = OUT_DIR / f'{pair_id}.html'
    out_path.write_text(html)
    print(f'Wrote {out_path} ({out_path.stat().st_size // 1024} KB, {len(items)} items, sheet endpoint: {"yes" if SHEETS_ENDPOINT else "no"})')
