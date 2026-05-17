#!/usr/bin/env node
const { execSync } = require('child_process');
const fs = require('fs');

const DEFAULT_DATES = [
  '2026-05-13T12:00:00',
  '2026-05-07T12:00:00',
  '2026-03-31T12:00:00',
  '2026-03-22T12:00:00',
  '2026-03-24T12:00:00',
  '2026-03-19T12:00:00',
  '2026-03-09T12:00:00',
];

function commitForDate(dateIso, readmePath = 'README.md') {
  const display = dateIso.split('T')[0];
  const line = `Remembering ${display} — I miss this day.` + '\n';
  fs.appendFileSync(readmePath, line, { encoding: 'utf8' });

  const env = Object.assign({}, process.env, {
    GIT_AUTHOR_DATE: dateIso,
    GIT_COMMITTER_DATE: dateIso,
  });

  execSync(`git add ${readmePath}`, { env, stdio: 'inherit' });
  execSync(`git commit -m "Add memory line for ${display}"`, { env, stdio: 'inherit' });
}

function main() {
  const args = process.argv.slice(2);
  const dates = args.length ? args : DEFAULT_DATES;
  for (const d of dates) {
    console.log(`Creating commit dated ${d} -> appending to README.md`);
    commitForDate(d);
  }
}

main();
