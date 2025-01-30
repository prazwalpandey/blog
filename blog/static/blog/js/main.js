/*
	Future Imperfect by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function($) {

	var	$window = $(window),
		$body = $('body'),
		$menu = $('#menu'),
		$sidebar = $('#sidebar'),
		$main = $('#main');

	// Breakpoints.
		breakpoints({
			xlarge:   [ '1281px',  '1680px' ],
			large:    [ '981px',   '1280px' ],
			medium:   [ '737px',   '980px'  ],
			small:    [ '481px',   '736px'  ],
			xsmall:   [ null,      '480px'  ]
		});

	// Play initial animations on page load.
		$window.on('load', function() {
			window.setTimeout(function() {
				$body.removeClass('is-preload');
			}, 100);
		});

	// Menu.
		$menu
			.appendTo($body)
			.panel({
				delay: 500,
				hideOnClick: true,
				hideOnSwipe: true,
				resetScroll: true,
				resetForms: true,
				side: 'right',
				target: $body,
				visibleClass: 'is-menu-visible'
			});

	// Search (header).
	var $search = $('#search-form'),
        $search_input = $search.find('#search-input'),
        $search_icon = $('.fa-search');

    // When the search icon is clicked
    $search_icon.on('click', function (event) {
        event.preventDefault(); // Prevent default link behavior

        if ($search.is(':visible')) {
            if ($search_input.val().trim()) {
                $search.submit(); // Submit form if there is text
            } else {
                $search.hide(); // Hide form if empty
            }
        } else {
            $search.show();
            $search_input.focus();
        }
    });

	$(document).on('click', function (event) {
        if (!$search.is(event.target) && !$search_icon.is(event.target) && $search.has(event.target).length === 0) {
            $search.hide();
        }
    });

    // Submit form when Enter is pressed
    $search_input.on('keypress', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            $search.submit();
        }
    });
})(jQuery);