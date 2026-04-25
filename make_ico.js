const fs = require('fs');
const path = require('path');

const pngPath = path.join(__dirname, 'logo_256.png');
const icoPath = path.join(__dirname, 'logo.ico');

if (!fs.existsSync(pngPath)) {
    console.error('Error: logo.png not found!');
    process.exit(1);
}

const pngData = fs.readFileSync(pngPath);
const pngSize = pngData.length;

// ICO Header (6 bytes)
const header = Buffer.alloc(6);
header.writeUInt16LE(0, 0); // Reserved
header.writeUInt16LE(1, 2); // Type (1 = ICO)
header.writeUInt16LE(1, 4); // Number of images (1)

// ICO Directory Entry (16 bytes)
const directory = Buffer.alloc(16);
directory.writeUInt8(0, 0);   // Width (0 = 256px)
directory.writeUInt8(0, 1);   // Height (0 = 256px)
directory.writeUInt8(0, 2);   // Color palette (0 = no palette)
directory.writeUInt8(0, 3);   // Reserved
directory.writeUInt16LE(1, 4); // Color planes (1)
directory.writeUInt16LE(32, 6); // Bits per pixel (32)
directory.writeUInt32LE(pngSize, 8); // Size of the image data
directory.writeUInt32LE(22, 12);     // Offset of the image data (Header + Directory = 6 + 16 = 22)

const icoData = Buffer.concat([header, directory, pngData]);

fs.writeFileSync(icoPath, icoData);
console.log('Success! logo.ico has been created successfully.');
