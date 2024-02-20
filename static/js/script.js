function scrollScreen() {
    $('#to-top').removeClass('visible');
    if (window.scrollY) {
        $('#to-top').addClass('visible');
    }

    // Giving the hero image a slight perspective effect
    let heroImagePosition = Math.floor(window.scrollY / 4);
    $('#hero-image').css('background-position-y', `${heroImagePosition}px`);
}

$(document).ready(() => {
    // Makes the "Back to Top" button only visible when the user has scrolled past the start of the page
    $(window).on('scroll', scrollScreen);

    // Returns to the top of the screen when the "Back to Top" button is clicked
    $('#to-top').click(function() {
        window.scrollTo(0, 0);
    });

    scrollScreen();
});