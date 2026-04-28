// Paper 2 coding sheet endpoint
// =============================
// Standalone Apps Script project (script.new). Opens the target Sheet by ID,
// so it does not need to be a container-bound script. Deploy:
//   Deploy > New deployment > Web app
//   Execute as:  Me (your account)
//   Who has access:  Anyone
// Copy the resulting "Web app URL" and paste it into build_static_app.py
// (SHEETS_ENDPOINT) and rebuild the HTML files.
//
// One row per (coder, item_id) pair. Re-coding overwrites the row.
// Each coder gets their own tab (coder1 .. coder4), auto-created on first hit.

const SHEET_ID = '1h8H01eEAsIG6aYNZagruDPs0NqhU4fJxfEHlxrbqflg';

const HEADERS = [
  'item_id',
  'community',
  'coder',
  'pair',
  'timestamp',
  'thread_has_claim',
  'type',
  'challenge_direction',
  'coherence_shift',
  'notes'
];

const ALLOWED_CODERS = ['coder1', 'coder2', 'coder3', 'coder4'];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const body = JSON.parse(e.postData.contents);
    const coder = String(body.coder || '').trim();
    if (ALLOWED_CODERS.indexOf(coder) === -1) {
      return jsonOut({ ok: false, error: 'invalid coder ' + coder });
    }

    const ss = SpreadsheetApp.openById(SHEET_ID);
    let sheet = ss.getSheetByName(coder);
    if (!sheet) {
      sheet = ss.insertSheet(coder);
      sheet.appendRow(HEADERS);
      sheet.setFrozenRows(1);
    }

    if (sheet.getLastRow() === 0) {
      sheet.appendRow(HEADERS);
      sheet.setFrozenRows(1);
    }

    const itemId = String(body.item_id || '').trim();
    if (!itemId) return jsonOut({ ok: false, error: 'missing item_id' });

    const row = HEADERS.map(function (h) {
      const v = body[h];
      return v == null ? '' : v;
    });

    const lastRow = sheet.getLastRow();
    if (lastRow > 1) {
      const idColValues = sheet.getRange(2, 1, lastRow - 1, 1).getValues();
      for (let i = 0; i < idColValues.length; i++) {
        if (String(idColValues[i][0]) === itemId) {
          sheet.getRange(i + 2, 1, 1, HEADERS.length).setValues([row]);
          return jsonOut({ ok: true, action: 'update', row: i + 2 });
        }
      }
    }
    sheet.appendRow(row);
    return jsonOut({ ok: true, action: 'append', row: sheet.getLastRow() });
  } catch (err) {
    return jsonOut({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

function doGet(e) {
  return jsonOut({ ok: true, ping: 'paper2-coding endpoint alive' });
}

function jsonOut(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
