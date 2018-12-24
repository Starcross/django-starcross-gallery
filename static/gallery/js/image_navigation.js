/** Provide navigation keys to change the current image */

var left = 37; var right = 39;

document.addEventListener("keydown", function(event) {
    switch(event.which) {
        case left:
            if (previous_image_url) {
                window.location.href = previous_image_url;
            }
        break;
        case right:
            if (next_image_url) {
                window.location.href = next_image_url;
            }
        break;
        default: return;
    }
   event.preventDefault();
});