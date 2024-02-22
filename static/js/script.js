/**
 * Scrolls to the top of the screen, and hides the "Back to Top" button
 */
function scrollScreen() {
    $('#to-top').removeClass('visible');
    if (window.scrollY) {
        $('#to-top').addClass('visible');
    }

    // Giving the hero image a slight perspective effect
    let heroImagePosition = Math.floor(window.scrollY / 4);
    $('#hero-image').css('background-position-y', `${heroImagePosition}px`);
}

/**
 * Adjusts elements whose properties depend on the screen width
 */
function resizeWindow() {
    let width = $(document).width();

    // Creates sufficient spacing between the brand logo and main page body to avoid overlap
    let logoHeight = $('#logo-brand').height();
    let navHeight = $('#navbar').height();
    let headingGap = Math.ceil((logoHeight / 2) - (navHeight / 2));
    if (width < 768) {
        headingGap -= navHeight;
        console.log('smol');
    }
    $('#content-header').css('min-height', '');
    if (headingGap > 0) {
        $('#content-header').css('min-height', `${headingGap}px`);
    }
}

$(document).ready(() => {
    // Makes the "Back to Top" button only visible when the user has scrolled past the start of the page
    $(window).on('scroll', scrollScreen).resize(resizeWindow);

    // Returns to the top of the screen when the "Back to Top" button is clicked
    $('#to-top').click(function() {
        window.scrollTo(0, 0);
    });

    scrollScreen();
    resizeWindow();
});