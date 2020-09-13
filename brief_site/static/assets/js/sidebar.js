$(function() {
    initMenuEvent();

    function initMenuEvent() {
      $('#menu-toggle').on('click', function (e) {
        e.preventDefault();
        if ($('#sidebar-wrapper').hasClass('sidebar-not-active')) {
          $('#sidebar-wrapper').removeClass('sidebar-not-active');
          $('#main-area').removeClass('sidebar-not-active');
          $('#main-icon').removeClass('glyphicon-menu-right');
          $('#main-icon').addClass('glyphicon-menu-left');
        } else {
          $('#sidebar-wrapper').addClass('sidebar-not-active');
          $('#main-area').addClass('sidebar-not-active');
          $('#main-icon').removeClass('glyphicon-menu-left');
          $('#main-icon').addClass('glyphicon-menu-right');
        }
      });

      $('.menu-wrapper').find('.fold-item').on('click', function (e) {
        e.preventDefault();
        let target = $(e.target);
        if (!target.hasClass('glyphicon-triangle-bottom')) {
          target = target.find('.glyphicon-triangle-bottom');
        }
        if (target.length <= 0) {
          return;
        }

        let foldItem = target.parents('.fold-item'),
          nextArea = foldItem.next(),
          foldItemId = foldItem.attr('id');
        if (nextArea.hasClass('collapsing')) {
          return;
        }
        if (nextArea.hasClass('in') && target.hasClass('rotate')) {
          $('#sidebar-wrapper #' + foldItemId).find('span.glyphicon-triangle-bottom').removeClass('rotate');
          $('#menubar-wrapper #' + foldItemId).find('span.glyphicon-triangle-bottom').removeClass('rotate');
          return;
        }
        if (!nextArea.hasClass('in') && !target.hasClass('rotate')) {
          $('#sidebar-wrapper #' + foldItemId).find('span.glyphicon-triangle-bottom').addClass('rotate');
          $('#menubar-wrapper #' + foldItemId).find('span.glyphicon-triangle-bottom').addClass('rotate');
        }
      });
    }

   let initMenu = (function(activeMenuClassName, elementId, foldItemId) {
        if (typeof (elementId) === 'string' || typeof (foldItemId) === 'string') {
          $('.menu-wrapper #' + elementId).collapse('toggle');
          $('#sidebar-wrapper #' + foldItemId).find('span.glyphicon-triangle-bottom').addClass('rotate');
          $('#menubar-wrapper #' + foldItemId).find('span.glyphicon-triangle-bottom').addClass('rotate');
        }
        $('#sidebar-wrapper .' + activeMenuClassName).addClass('active');
        $('#menubar-wrapper .' + activeMenuClassName).addClass('active');
    });

    window.initMenu = initMenu;
});
