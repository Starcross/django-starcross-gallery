/** Justify image grid based on thumbnail class

    These global vars should be present

    hdpi_factor e.g. 2
    image_margin e.g 6.0

*/



function justify_images() {
/** Fix the width each image in a container to fully justify each row */

    var container = document.getElementById('image_container')
    // Get exact width of container
    var container_width = container.getBoundingClientRect()['width'];

    // Find the images in the thumbnail container
    var images = document.querySelectorAll('.image');
    if (images == []) {
        return;
    }
    // Assume all images have the same height from the ImageSpecField resize
    var target_height = images[0].naturalHeight / hdpi_factor;

    // Keep an array of images for the current row and it's width
    var row_width = 0;
    var row_images = [];
    for (var i=0; i < images.length; i++) {
        // Add the current image and it's width
        row_images.push(images[i]);
        row_width += (images[i].naturalWidth / hdpi_factor);
        // Look ahead to see how wide the next image is
        var next_half_width = 0;
        if (i < images.length - 1) {
            next_half_width = images[i+1].naturalWidth / hdpi_factor / 2 ;
        }
        // See if the we have exceed the size of the row, including half the next image
        // This keeps us closer to the target height
        if ((row_width + next_half_width) >= container_width) {
            // Account for the total width of all margins on this row
            var margin_total = image_margin * (row_images.length - 1);
            // Find the factor required to shrink or enlarge the images in this row
            var resize_factor = (container_width - margin_total) / row_width;
            resize_row(row_images, resize_factor);
            // Reset values for new row
            row_width = 0;
            row_images = [];
        } else {
            // Add the margin to the running row width
            row_width += image_margin;
        }

    }

}

function resize_row(images, factor) {
/** Set each item in the image array according to the given factor */

    for (var i=0; i < images.length; i++) {

        var width = ((images[i].naturalWidth / hdpi_factor) * factor);
        images[i].style.width = width + "px";
        var height = ((images[i].naturalHeight / hdpi_factor) * factor);
        images[i].style.height = height + "px";
        // Add a margin if this is not the last image
        if (i < (images.length - 1)) {
            images[i].style.marginRight = image_margin + 'px';
        } else {
            images[i].style.marginRight = '0';
        }
    }
}

window.addEventListener('load',justify_images);
window.addEventListener('resize',justify_images);