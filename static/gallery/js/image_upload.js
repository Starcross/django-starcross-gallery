/**
Provide drag and drop support on image display pages
*/

document.addEventListener('drop', function(event) {
    var drop_container = document.getElementById('image_container');
    var image_form = document.getElementById('image_upload_form');
    var data_input  = image_form.elements['data'];

    drop_container.classList.remove('highlight');

    data_input.files = event.dataTransfer.files;
    image_form.submit();

    event.preventDefault();
});

document.addEventListener('dragover', function(event) {
    event.preventDefault();
});

document.addEventListener('dragenter', function(event) {
    var drop_container = document.getElementById('image_container');
    drop_container.classList.add('highlight');
    event.preventDefault();
});

document.addEventListener('dragexit', function() {
    var drop_container = document.getElementById('image_container');
    drop_container.classList.remove('highlight');
});
