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
            alert("Please, choose img");
        }
    }
});
