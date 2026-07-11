// Unit tests for the pure helpers exported by html/app.js.
//
//     node tools/test_app.js
//
// The DOM wiring in app.js is skipped under Node (no `document`); only the
// pure functions are exercised here.

'use strict';
const assert = require('assert');
const { escapeHtml, markHTML, isoDaysAgo, inRange } = require('../html/app.js');

let passed = 0;
function ok(name, cond) { assert.ok(cond, name); passed++; }
function eq(name, a, b) { assert.strictEqual(a, b, name + ' (got ' + JSON.stringify(a) + ')'); passed++; }

// escapeHtml
eq('escapes the three markup chars', escapeHtml('<a> & <b>'), '&lt;a&gt; &amp; &lt;b&gt;');

// markHTML
eq('no needle -> escaped only', markHTML('a<b', ''), 'a&lt;b');
eq('wraps matches case-insensitively',
   markHTML('Dee and DEE', 'dee'), '<mark>Dee</mark> and <mark>DEE</mark>');
eq('escapes text around a mark',
   markHTML('x <Dee>', 'dee'), 'x &lt;<mark>Dee</mark>&gt;');
eq('no match -> escaped, unmarked', markHTML('chess', 'zzz'), 'chess');

// inRange
ok('open bounds admit any date', inRange('2020-01-01', '', '') === true);
ok('below min excluded', inRange('2017-12-31', '2018-01-01', '2022-12-31') === false);
ok('within range included', inRange('2019-06-01', '2018-01-01', '2022-12-31') === true);
ok('above max excluded', inRange('2023-01-01', '2018-01-01', '2022-12-31') === false);
ok('lower bound only', inRange('2021-05-05', '2020-01-01', '') === true);
ok('empty date matches only when fully open', inRange('', '2018-01-01', '') === false);
ok('empty date matches when open', inRange('', '', '') === true);

// isoDaysAgo (UTC, deterministic)
const now = new Date('2026-07-11T12:00:00Z');
eq('31 days ago', isoDaysAgo(31, now), '2026-06-10');
eq('365 days ago', isoDaysAgo(365, now), '2025-07-11');

console.log('app.js: ' + passed + ' assertions passed');
