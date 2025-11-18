// Load images on demand as user scrolls down the page

const pagination_size = 40;
let scroll_cursor = 0;

function init_infinite_scroll() {
    scroll_cursor = load_images_from_cursor(scroll_cursor);
}

function check_infinite_scroll(event) {
    // Based on https://benjaminhorn.io/code/how-to-implement-infinite-scroll/
    // Handle a scrollable element nested within fixed elements by referring to event.target
    let target =  (event.target instanceof HTMLDocument) ?
        event.target.scrollingElement : event.target;
    // Fetch variables
    let scrollTop = target.scrollTop;
    let windowHeight = target.clientHeight;
    let bodyHeight = target.scrollHeight - windowHeight;
    let scrollPercentage = (scrollTop / bodyHeight);

    // if the scroll is more than 90% from the top, load more content.
    if (scrollPercentage > 0.7) {
        scroll_cursor = load_images_from_cursor(scroll_cursor);
    }

}

function load_images_from_cursor(cursor) {
    // Find the images in the thumbnail container
    const images = document.querySelectorAll('.image');
    const thumbnails = document.querySelectorAll('.thumbnail');

    let i = cursor; // start from last position
    
    // Change the source of the next page of images if any left
    for (; i < images.length && i < cursor + pagination_size; i++) {
        // Re-justify after this image has loaded
        images[i].addEventListener('load', justify_images);
        // and change its display property to show it
        thumbnails[i].style.display = 'block';
        // Initiate the load
        const src = images[i].getAttribute('data-src');
        images[i].setAttribute('src', src);
    }
    if (i >= images.length && cursor < images.length) {
        // All images have been set to load, no further need
        window.removeEventListener('scroll',check_infinite_scroll);
    }
    return i;
}

window.addEventListener('load',init_infinite_scroll);
window.addEventListener('scroll',check_infinite_scroll, {'capture':true});
