## Paper 2 Static Coding App — Send-Out Guide

Two single-file HTML coding apps, one per coder pair, for the human-validation phase of "Sanding Off the Edges." Hosted via GitHub Pages so coders open a URL in any browser. Each save POSTs the row to a Google Apps Script web app that writes it into a shared Google Sheet, one tab per coder. Browser localStorage stays as a backup so a flaky network or a closed tab never costs anyone work.

---

### Current deployment (recorded 2026-04-28)

| Resource | URL |
|----------|-----|
| Pair 1 coder link | <https://www.morganwack.com/paper2-coding/pair1.html> |
| Pair 2 coder link | <https://www.morganwack.com/paper2-coding/pair2.html> |
| Submissions Sheet (you only) | <https://docs.google.com/spreadsheets/d/1h8H01eEAsIG6aYNZagruDPs0NqhU4fJxfEHlxrbqflg/edit> |
| Apps Script project | <https://script.google.com/u/0/home/projects/1xZDda-3RELueYdU-YaYDJ0ObLBboaoZIoF6FK92A-bqS6WJ-p7SWyR0W/edit> |
| Apps Script web app endpoint (do not share) | `https://script.google.com/macros/s/AKfycbyjua4ZBIVRtIrQUZAZvgDvhaAbZmhEVKkeO0TjNcdSYdS45fMyVfTB-Em4azbciGUuhQ/exec` |
| GitHub repo | <https://github.com/morwack/paper2-coding> |

The end-to-end save round-trip was verified live on 2026-04-28 (Pair 1, signed in as `coder1`, item 1 saved as DISMISS / N/A / N/A). The custom domain `www.morganwack.com` is in front of GitHub Pages because it is configured at the user account level. Coders should use the morganwack.com URL, not the morwack.github.io variant, since GitHub redirects the latter to the former.

---

### Files in this folder

| File | What it is |
|------|-----------|
| `pair1.html` | 200 comments for Pair 1 (50 per community: NNN, Superstonk, flatearth, conspiracy). Self-contained. ~155 KB. |
| `pair2.html` | 200 comments for Pair 2 (the disjoint other half). ~150 KB. |
| `apps_script.gs` | Google Apps Script to paste into the Sheet that should receive submissions. |
| `build_static_app.py` | Regenerates the two HTML files from the source coding sheets. Reads `SHEETS_ENDPOINT` from the top of the file. |
| `README.md` | This file. |

The codebook PDF lives in the validation folder of the no-canon paper. Send it as an attachment alongside the URL.

---

## End-to-end setup (do these once)

### Step 1. Create the Google Sheet that will receive submissions

1. Go to <https://sheets.new>. Name the sheet something like `Paper 2 Coding Submissions`.
2. Leave the default `Sheet1` tab in place. The Apps Script auto-creates `coder1`, `coder2`, `coder3`, `coder4` tabs on first hit, so no manual tab setup is required.
3. **Extensions → Apps Script.** A new tab opens with a `Code.gs` editor.
4. Delete whatever boilerplate is in `Code.gs`. Open `apps_script.gs` from this folder, copy its entire contents, and paste into `Code.gs`. Click the floppy disk icon to save.
5. **Deploy → New deployment.** Click the gear icon, choose **Web app**.
   - Description, anything you like.
   - **Execute as**, *Me (your account)*.
   - **Who has access**, *Anyone*. (Required so the coders' browsers can POST without signing in. The script still runs as you, so only your Sheet is touched.)
   - Click **Deploy**. Authorize when prompted (Google warns about an "unverified" script, click *Advanced → Go to ... (unsafe)* and Allow). This is normal for personal Apps Scripts.
6. Copy the **Web app URL** that appears. It looks like `https://script.google.com/macros/s/AKfyc.../exec`.
7. Smoke-test in any browser by visiting the URL directly. You should see `{"ok":true,"ping":"paper2-coding endpoint alive"}`.

### Step 2. Wire the URL into the HTML and rebuild

1. Open `build_static_app.py`. Find `SHEETS_ENDPOINT = ''` near the top. Replace the empty string with the URL from step 1.7.
2. Rebuild:
   ```bash
   cd ~/Desktop/Paper2_Static_App
   python3 build_static_app.py
   ```
   Output should report `sheet endpoint: yes` for both pairs.
3. Push the rebuilt HTML to GitHub Pages (Step 3 below) and smoke-test on the live URL. There is no need to open `pair1.html` locally. The app is only useful through the hosted URL because that is the same origin coders will use, and any localStorage state on `file://` is irrelevant to them.

### Step 3. Push to GitHub and enable GitHub Pages

The `gh` CLI is not installed on this machine, so the repo creation step happens in the browser.

1. Open <https://github.com/new>.
   - Repository name, `paper2-coding`.
   - Visibility, **Public** (required for free GitHub Pages on a personal account).
   - Do **not** initialize with a README or `.gitignore`. Leave it empty.
   - Click **Create repository**.
2. In Terminal:
   ```bash
   cd ~/Desktop/Paper2_Static_App
   git add .
   git commit -m "Paper 2 coding pages with Sheet sync"
   git remote add origin git@github.com:morwack/paper2-coding.git
   git push -u origin main
   ```
   (If your SSH key is registered under a different GitHub username, swap `morwack`.)
3. On GitHub, open the repo's **Settings → Pages**. Source, *Deploy from a branch*. Branch, `main`, folder `/ (root)`. Save.
4. Wait roughly 30 seconds. Coder URLs are then:
   - Pair 1, <https://www.morganwack.com/paper2-coding/pair1.html>
   - Pair 2, <https://www.morganwack.com/paper2-coding/pair2.html>

That is the link you send to coders.

---

## Pre-flight check before sending

Open the live Pair 1 URL (<https://www.morganwack.com/paper2-coding/pair1.html>) in a clean browser window.

1. Sign in as `test`. The page transitions to the coding view, but `test` is not in the allowed list, so the sheet sync will report an error in the status line. That is expected.
2. Sign out, sign in again as `coder1`.
3. Code 2 items, click **Save and next** each time. The status line should show `Saved and synced` in green within about one second.
4. Switch to the Google Sheet. You should see two rows on the `coder1` tab.
5. Edit one of the items in the app and hit Save again. The same row in the sheet should update in place (no duplicate row).
6. Click the orange **View original Reddit thread** button on at least one item to confirm the permalink opens correctly.
7. Click **Reset (clears codes)** to wipe the test session, then delete the `coder1` tab from the Sheet so it is empty for real coders.

Repeat the same check on the Pair 2 URL with `coder3`.

---

## Email templates

Replace the bracketed placeholders. Each coder must sign in with the exact name listed below. That name picks the destination tab in the sheet and becomes the filename of the backup CSV.

### Email to Pair 1

To, `[coder1 email]`, `[coder2 email]`
Subject, Paper 2 conspiracy-comment coding, instructions
Attachments, `CODER_INSTRUCTIONS.pdf`

> Hi `[Name1]` and `[Name2]`,
>
> Thanks for agreeing to code for the validation phase of my Paper 2 ("Sanding Off the Edges"). You are **Pair 1**. Together you'll independently code 200 Reddit comments using a 4-category scheme. Total time per coder is roughly 4 hours, ideally split across two or three sessions over the next week.
>
> **What I need from each of you**
>
> 1. **Read `CODER_INSTRUCTIONS.pdf` carefully** (~30 min). It walks through Step 0 (does the thread carry a checkable claim?) and the Q1 → Q2 → Q3 decision tree, with paradigmatic examples for each category.
> 2. **Open the coding page in any browser** (Chrome, Safari, Firefox, Edge are all fine).
>     - **`[Name1]`**, your link is <https://www.morganwack.com/paper2-coding/pair1.html> and you sign in as `coder1`.
>     - **`[Name2]`**, your link is <https://www.morganwack.com/paper2-coding/pair1.html> and you sign in as `coder2`.
>     Use the same browser and the same machine for the whole task. Your progress saves automatically (no account needed). It's safe to close the tab and come back later.
> 3. **Use the orange "View original Reddit thread" button** whenever the title and parent comment are not enough context. Many Superstonk and r/conspiracy threads are image posts, so the link will show you the screenshot, selftext, and surrounding replies the comment was reacting to. (For r/NoNewNormal items, the subreddit was banned by Reddit, so the link will show a "banned" page. For NNN you can usually code from text alone, or try the Wayback Machine link the page suggests.)
> 4. **Calibration round (do this together).** Schedule a one-hour call with each other before going independent. On the call, each of you codes the first 20 comments (items 1 to 20) on your own, then compare your codes side by side and discuss any disagreements. The goal is to align on the boundary cases (DISMISS vs OFF, CHALLENGE vs BUILD, and Step 0 thread-has-claim) before doing the rest alone.
> 5. **Independent round.** Once calibration is done, code items 21 to 200 on your own. **Do not look at your co-coder's codes** during this part. Click "Save and next" after each item.
> 6. **No need to email anything back.** Each save automatically posts to a shared Google Sheet on my end. The status line next to the Save button confirms each row reached the sheet. If you ever see a red `Saved locally, sheet sync failed` message, click the blue **Sync unsynced to sheet** button in the sidebar to push everything that hasn't made it through.
>
> **Practical reminders**
> - The interface saves automatically as you click Save and next. You can stop and resume any time.
> - **Use one consistent browser on one machine** through the whole task. If you switch browsers or machines, you'll lose any items that were saved locally but never reached the sheet. Items already on the sheet are safe.
> - Don't clear browser cookies or site data while you're working. The sidebar counter shows how many items have actually reached the sheet.
> - If anything in the codebook feels ambiguous, jot a note in the Notes box for that item and keep going. We can discuss flagged items afterward.
>
> Reach out with any questions. Thanks again!
>
> Morgan

### Email to Pair 2

Same as above, but,
- The link is <https://www.morganwack.com/paper2-coding/pair2.html>
- Replace "Pair 1" with "Pair 2"
- The two coders sign in as `coder3` and `coder4`

---

## What you receive at the end

One Google Sheet with four tabs (`coder1`, `coder2`, `coder3`, `coder4`). Each row has columns `item_id, community, coder, pair, timestamp, thread_has_claim, type, challenge_direction, coherence_shift, notes`.

To pull each tab to a CSV for the agreement script, use **File → Download → Comma-separated values (.csv)** in the Sheet, once per tab. Save the four files as `coder1_pair1_codes.csv`, `coder2_pair1_codes.csv`, `coder3_pair2_codes.csv`, `coder4_pair2_codes.csv` to match what `compute_agreement.py` expects.

Then run reliability:

```bash
cd ~/Desktop/Paper2_No_Canon
# Inter-coder kappa within each pair
python3 replication/compute_agreement.py coder1_pair1_codes.csv coder2_pair1_codes.csv
python3 replication/compute_agreement.py coder3_pair2_codes.csv coder4_pair2_codes.csv

# LLM-human kappa, each coder against the LLM answer key
# answer_key.csv is in replication/output/human_validation/
```

**Reliability targets**
- Primary, LLM-human κ > 0.60 for `type`, > 0.70 for `challenge_direction` (averaged across the 4 coders)
- Secondary, inter-coder κ > 0.60 within each pair

If both targets clear, the paper's reliability section is in good shape.

---

## How the sheet sync works (technical notes)

- **Each save** triggers a `fetch` POST from the coder's browser to the Apps Script `/exec` URL. Body is a small JSON payload with the coder name, item id, community, the four DV values, the notes field, and an ISO timestamp.
- **Content-Type is `text/plain`** so the request is treated as a CORS "simple request" and the browser does not fire a preflight (Apps Script web apps cannot answer the OPTIONS preflight cleanly).
- **Apps Script upserts** by `(coder, item_id)`. If a coder revisits an item and changes their answer, the same row updates in place. New items append.
- **`LockService`** serializes concurrent writes so two coders submitting at the exact same instant cannot collide.
- **Per-coder localStorage** still holds every saved code as a backup. The `synced` map records which item ids have been confirmed by the sheet. The sidebar counter and the **Sync unsynced to sheet** button operate on the difference between coded and synced.

If the Apps Script URL ever changes (for example, you redeploy with a new version), update `SHEETS_ENDPOINT` at the top of `build_static_app.py`, rerun the script, then `git add . && git commit -m "..." && git push`. GitHub Pages serves the new build within a minute.

---

## Things to communicate to coders explicitly

- **One browser, one machine.** localStorage is per-browser, per-device. Switching mid-task means anything not yet synced to the sheet is lost.
- **Don't clear browser data while working.** Items not yet on the sheet would be lost. The sidebar counter tells them how many of their coded items are on the sheet.
- **Hostile tone alone does not equal DISMISS.** Many CHALLENGE comments are blunt. The classification is about whether the comment engages with the claim's content, not about politeness.
- **Use the Notes box for flagged items.** Don't agonize on edge cases. Pick the closest category, leave a note, move on. Discussion happens at the end.

---

## Regenerating the HTML files

If the source coding sheets change (unlikely at this point), or you redeploy the Apps Script and get a new endpoint URL, rebuild,

```bash
cd ~/Desktop/Paper2_Static_App
python3 build_static_app.py
git add pair1.html pair2.html build_static_app.py
git commit -m "Rebuild coding apps"
git push
```

It reads from `~/Desktop/Paper2_Coding_App_Pair1/data/items.json` and `~/Desktop/Paper2_Coding_App_Pair2/data/items.json`, applies the embedded HTML/CSS/JS template, and overwrites `pair1.html` and `pair2.html`.

---

## Reminder fires May 4, 2026

A scheduled trigger (`trig_012Pt4Dua3oCFPVzwb7VRbKv`) fires May 4 at 09:00 Europe/Zurich reminding you to send the materials. Manage at <https://claude.ai/code/scheduled>.

---

## State summary (for picking up later)

- **Static apps**, this folder (`~/Desktop/Paper2_Static_App/`), git repo to be pushed to `github.com/<your-handle>/paper2-coding`
- **Coder PDF**, `~/Desktop/Paper2_No_Canon/replication/output/human_validation/CODER_INSTRUCTIONS.pdf` (or wherever the no-canon paper's validation folder ends up)
- **Active paper**, no-canon only, `~/Desktop/Paper2_No_Canon/`, Overleaf <https://www.overleaf.com/project/69db88d9609c48577132578b>
- **Codebook**, revised decision tree (Q1 content, Q2 add vs push back, Q3 actionable handle), LLM-LLM κ = 0.644 on the 400-comment pilot
- **Validation design**, paired-split, 4 coders × 200 comments each, 50 per community per pair
- **Agreement script**, `~/Desktop/Paper2_No_Canon/replication/compute_agreement.py` (or the equivalent in the no-canon replication folder)
- **Reminder**, May 4, 2026 at 09:00 Europe/Zurich
