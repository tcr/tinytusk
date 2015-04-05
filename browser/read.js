var inspect = require('util').inspect;

var Dicer = require('dicer');

var d = new Dicer({ boundary: 'lol' });

d.on('part', function(p) {
  console.log('New part!');
  p.on('header', function(header) {
    for (var h in header) {
      console.log('Part header: k: ' + inspect(h)
                  + ', v: ' + inspect(header[h]));
    }
  });
  p.on('data', function(data) {
    console.log('Part data: ' + inspect(data.toString()));
  });
  p.on('end', function() {
    console.log('End of part\n');
  });
});
d.on('finish', function() {
  console.log('End of parts');
});
process.stdin.pipe(d);
