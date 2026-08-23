
const fs = require('fs');
if (!fs.existsSync('./package.json')) { console.log('No package.json'); process.exit(0); }
const pkg = require('./package.json');
const all = { ...(pkg.dependencies || {}), ...(pkg.devDependencies || {}) };
const critical = process.argv.slice(2);
critical.forEach(p => {
  const v = all[p];
  if (!v) console.log(`MISSING: ${p}`);
  else console.log(`OK: ${p} (${v})`);
});
