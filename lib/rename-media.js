var fs = require('fs');
var path = require('path');
var removeDiacritics = require('diacritics').remove;

var root = '../Ultimate_Geography';
var jsonFile = path.join(root, 'Ultimate_Geography.json');
var mediaFolder = path.join(root, 'media');

// Read JSON file
var raw = fs.readFileSync(jsonFile, 'utf-8');
var notes = require(jsonFile).notes;
var newNames = [];

// Rename flags
// raw = notes.reduce(processMedia.bind(null, 'flag'), raw);

// Rename maps
raw = notes.reduce(processMedia.bind(null, 'map'), raw);

function processMedia(type, raw, note) {
  var country = note.fields[0];
  var img = note.fields[type === 'flag' ? 5 : 7];
  if (!img) return raw;
  
  // Find old name and create new name
  var oldName = img.substring(img.indexOf('"') + 1, img.lastIndexOf('"'));
  var newName = 'ug-' + type + '-' + cleanFileName(country) + oldName.substring(oldName.lastIndexOf('.'));

  if (!fs.existsSync(path.join(mediaFolder, oldName))) {
    console.log(path.join(mediaFolder, oldName), 'not found');
    return raw;
  }

  // Rename image file
  fs.renameSync(path.join(mediaFolder, oldName), path.join(mediaFolder, newName));

  // Replace filename in JSON
  return replaceAll(raw, oldName, newName);
}

// Write changes
fs.writeFile(jsonFile, raw, function (err) {
  if (err) return console.log(err);
  console.log('writing to ' + jsonFile);
});

function cleanFileName(fileName) {
  return removeDiacritics(fileName.toLowerCase()).replace(/ \(.+\)/, '').replace(/ /g, '_');
}

function replaceAll(target, search, replacement) {
  var regex = new RegExp(escapeRegExp(search), 'gm');
  return target.replace(regex, replacement);
}

function escapeRegExp(s) {
  return s.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&');
}
