var zlib = require('zlib');

var tar = require('tar-stream')
var $ = require('jquery');
var CodeMirror = require('codemirror');
require('codemirror/addon/edit/matchbrackets');
require('codemirror/mode/clike/clike');

$(function () {
  var body = $('textarea')[0];

  var myCodeMirror = CodeMirror.fromTextArea(body, {
    lineNumbers: true,
    mode:  "clike",
    theme: 'monokai',
  });

  $('#submit').on('click', function () {
  	
  })
})
