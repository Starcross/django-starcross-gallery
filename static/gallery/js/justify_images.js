/** Justify image grid based on thumbnail class

    These global vars should be present

    hdpi_factor e.g. 2
    image_margin e.g 6.0

*/



function justify_images(event) {
/** Fix the width each image in a container to fully justify each row */

    var container = document.getElementById('image_container');
    // Get exact width of container - 1 to allow for rounding error
    var container_width = container.getBoundingClientRect()['width'] - 1 ;

    // Find the images in the thumbnail container
    var images = document.querySelectorAll('.image');
    if (images == []) {
        return;
    }
    // Assume all images have the same height from the ImageSpecField resize
    // var target_height = images[0].naturalHeight / hdpi_factor;

    // Build an array of images for the current row and it's width
    var row_width = 0;
    var row_images = [];
    for (var i=0; i < images.length; i++) {
        // Add the current image and it's width
        row_images.push(images[i]);
        row_width += (images[i].naturalWidth / hdpi_factor);
        // Look ahead to see how wide the next image is
        var next_half_width = 0;
        var resize_factor = 1;  // Initialize for orphans too...
        if (i < images.length - 1) {
            next_half_width = images[i+1].naturalWidth / hdpi_factor / 2 ;
        }
        // See if the we have exceed the size of the row, including half the next image
        // This keeps us closer to the target height
        if ((row_width + next_half_width) >= container_width) {
            // Account for the total width of all margins on this row
            var margin_total = image_margin * (row_images.length - 1);
            // Find the factor required to shrink or enlarge the images in this row
            resize_factor = (container_width - margin_total) / (row_width - margin_total);
            resize_row(row_images, resize_factor);
            // Reset values for new row
            row_width = 0;
            row_images = [];
        } else {
            // Add the margin to the running row width
            row_width += image_margin;
        }
        // If there are any orphans on an incomplete last row, resize these
        if (row_width && i === images.length - 1) {
            resize_row(row_images, resize_factor);
        }

    }

}

function resize_row(images, factor) {
/** Set each item in the image array according to the given factor */

    for (var i=0; i < images.length; i++) {

        var overlay = images[i].nextElementSibling;
        var width = ((images[i].naturalWidth / hdpi_factor) * factor);
        // html spec says these must be integers without a unit...
        images[i].width = Math.floor(width);
        var height = ((images[i].naturalHeight / hdpi_factor) * factor);
        images[i].height = Math.floor(height);
        // Add a margin to image and overlay if this is not the last image
        if (i < (images.length - 1)) {
            images[i].classList.add('image_spacer');
            overlay.classList.add('image_spacer');

        } else {
            images[i].classList.remove('image_spacer');
            overlay.classList.remove('image_spacer');
        }
    }
}

window.addEventListener('resize',justify_images);
