/**
Provide drag and drop support on image display pages
*/

document.addEventListener('drop', function(event) {
    var data_input  = document.getElementById('image_upload_form').elements['data'];
    data_input.files = event.dataTransfer.files;
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
