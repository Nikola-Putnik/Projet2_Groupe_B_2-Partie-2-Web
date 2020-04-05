$(document).foundation()


// LIKE BUTTON - url : https://foundation.zurb.com/building-blocks/blocks/button-like.html
$(function() {
  $('.button-like')
    .bind('click', function(event) {
      $(".button-like").toggleClass("liked");
    })
});
