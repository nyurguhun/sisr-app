var dropZone = document.getElementById('dropZone');

//Show the copy icon when dragging over.  
dropZone.addEventListener('dragover', function(e) {
    e.stopPropagation();
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
});

// Get file data on drop
dropZone.addEventListener('drop', function(e) {
    e.stopPropagation();
    e.preventDefault();
    var files = e.dataTransfer.files; // Array of all files

    for (var i=0, file; file=files[i]; i++) {
        if (file.type.match(/image.*/)) {
            var reader = new FileReader();

            reader.onload = function(e2) {
                // finished reading file data.
                var newimg = document.createElement('img');
                newimg.src= e2.target.result;
                var oldimg = document.getElementById('img');
                oldimg.replaceWith(newimg);
                newimg.setAttribute("id", "img");
                //dropZone.appendChild(img);
                //document.body.appendChild(img);
                //var img = document.getElementById('img');
                //img.src= e2.target.result;
            }

            reader.readAsDataURL(file); // start reading the file data.
        } else {
            alert("Sorry! We support jpg format only!");
        }
    }
});


function handleFileSelect(evt) {
    var files = evt.target.files; // FileList object

    // Loop through the FileList and render image files as thumbnails.
    for (var i = 0, f; f = files[i]; i++) {

      // Only process image files.
      if (!f.type.match('image.*')) {
        continue;
      }

      var reader = new FileReader();

      // Closure to capture the file information.
      reader.onload = (function(theFile) {
        return function(e) {
          // Render thumbnail.
          var newimg = document.createElement('img');
                newimg.src= e.target.result;
                var oldimg = document.getElementById('img');
                oldimg.replaceWith(newimg);
                newimg.setAttribute("id", "img");


          /*var span = document.createElement('span');
          span.innerHTML = ['<img class="thumb" src="', e.target.result,
                            '" title="', escape(theFile.name), '"/>'].join('');
          document.getElementById('list').insertBefore(span, null); */
        };
      })(f);

      // Read in the image file as a data URL.
      reader.readAsDataURL(f);
    }
  }

  document.getElementById('files').addEventListener('change', handleFileSelect, false);
