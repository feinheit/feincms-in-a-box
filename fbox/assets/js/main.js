let $ = require('jquery');
let smoothScroll = require('smoothScroll');
// let _ = require('lodash');

require('imports?jQuery=jquery!foundation-sites/js/foundation/foundation');
require('imports?jQuery=jquery!foundation-sites/js/foundation/foundation.topbar');


$(function() {
  $(document).foundation({
    topbar: {
      // Set this to false and it will pull the top level link name as the back text
      custom_back_text: false,
      // will copy parent links into dropdowns for mobile navigation
      mobile_show_parent_link: false,
      sticky_on: 'large',
    },
  });

  $('.back-to-top').click(() => smoothScroll(0, 0));
});
