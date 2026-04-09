'use strict';

const fs = require('fs');
const path = require('path');

// Read all JSON and YAML files in the current directory
const swaggerFiles = fs.readdirSync(__dirname)
  .filter(file => file.endsWith('.json') || file.endsWith('.yaml') || file.endsWith('.yml'))
  .reduce((acc, file) => {
    const content = fs.readFileSync(path.join(__dirname, file), 'utf8');
    acc[file] = content;
    return acc;
  }, {});

module.exports = swaggerFiles; 