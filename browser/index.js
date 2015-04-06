require('stream');

var zlib = require('browserify-zlib');
var crypto = require('crypto-browserify');

var request = require('request');
var Dicer = require('dicer');
var inspect = require('util').inspect;
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

  var RE_BOUNDARY = /^multipart\/.+?(?:; boundary=(?:(?:"(.+)")|(?:([^\s]+))))$/i;
  var NAME_BOUNDARY = /^form-data.*?(?:; name=(?:(?:"(.+)")|(?:([^\s]+))))$/i;

  function submit (target, next) {
    // Create tar packer
    var pack = tar.pack()
   
    // add a file called main.c with the codemirror content
    pack.entry({ name: 'main.c' }, myCodeMirror.getValue());
    pack.finalize()

    var gzip = zlib.createGzip();
    
    var req = request
    .post(location.protocol + '//' + location.hostname + ':' + location.port + '/api/' + target)

    pack
    .pipe(gzip)
    .pipe(req)
    .on('response', function (res, body) {
      var m;
      if (res.headers['content-type']
          && (m = RE_BOUNDARY.exec(res.headers['content-type']))) {
        
        var d = new Dicer({
          boundary: m[1] || m[2]
        });

        var name = '', result = '', info = '';
        d.on('part', function(p) {
          console.log('New part!');
          p.on('header', function(header) {
            for (var h in header) {
              var m;
              if (h == 'content-disposition' &&
                (m = NAME_BOUNDARY.exec(header[h].join('\n')))) {
                name = m[1] || m[2];
              }
            }
          });
          p.on('data', function (data) {
            if (name == 'result') {
              result += data;
            }
            if (name == 'info') {
              info += data.toString();
            }
            // console.log('Part data: ' + inspect(data.toString()));
          });
          p.on('end', function() {
            // console.log('End of part\n');
          });
        });
        d.on('finish', function() {
          // console.log('End of parts');
          next(result, info);
        });
        d.on('error', function () {
          // ignore output??
        })

        req.pipe(d);
      }
    })
  }

  $('#submit-test').on('click', function () {
    submit('test', function (result, info) {
      $('#output-info').text(info.toString().replace(/\s+$/, ''));
      $('#output-result').text(result.toString().replace(/\s+$/, ''));
    })
  })

  $('#submit-build').on('click', function () {
    submit('build', function (result, info) {
      $('#output-info').text(info.toString().replace(/\s+$/, ''));
      $('#output-result').text('Build successful. Click download binary above.');

      var data = new Buffer(result, 'base64');
      console.log('md5', crypto.createHash('md5').update(data).digest('hex'));
      console.log('length', data.length);

      var elem = $('#binary-test').css('display', 'inline')[0];
      elem.href = 'data:application/octet-stream;base64,' + result;
      elem.target = '_blank';
      elem.download = 'output';
    })
  })
})
