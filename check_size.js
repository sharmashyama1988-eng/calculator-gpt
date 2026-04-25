const fs = require('fs');

const pngPath = 'logo.png';
const data = fs.readFileSync(pngPath);

// PNG Width/Height starts at byte 16 (4 bytes each, Big Endian)
const width = data.readUInt32BE(16);
const height = data.readUInt32BE(20);

console.log(`Dimensions: ${width}x${height}`);
