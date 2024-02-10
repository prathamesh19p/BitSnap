$(function() {
  const $urlInput = $('#url_input');
  const $errorMsg = $('#error_msg');
  const $shortenBtn = $('#shorten_btn');
  const $shortenedPlace = $('#shortened_place');
  const $visitedPlace = $('#visited_place');
  const $resultContainer = $('#result_container');
  const $copyBtn = $('#copy_btn');
  const regex = /^(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z0-9\u00a1-\uffff][a-z0-9\u00a1-\uffff_-]{0,62})?[a-z0-9\u00a1-\uffff]\.)+(?:[a-z\u00a1-\uffff]{2,}\.?))(?::\d{2,5})?(?:[/?#]\S*)?$/i;

  function showError(errorMsg) {
    $errorMsg.html(errorMsg).toggleClass('is-invisible', false);
    $urlInput.removeClass('is-primary').addClass('is-danger');
    $shortenBtn.prop('disabled', true).removeClass('is-primary').addClass('is-danger');
  }

  function hideError() {
    $errorMsg.addClass('is-invisible');
    $urlInput.addClass('is-primary').removeClass('is-danger');
    $shortenBtn.prop('disabled', false).addClass('is-primary').removeClass('is-danger');
  }

  function toggleInput(disabled) {
    $shortenBtn.toggleClass('is-loading', disabled);
    $urlInput.prop('disabled', disabled);
  }

  $urlInput.on('input', hideError);

  $('#main_form').submit(function(e) {
    e.preventDefault();

    $resultContainer.addClass('is-invisible');
    hideError();

    let url = $(this).serializeArray()[0].value.trim();
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      url = 'https://' + url;
    }

    if (!regex.test(url)) {
      showError('The URL is invalid');
      return;
    }

    toggleInput(true);
    $.post('/shorten', { url })
      .done(function(data) {
        $shortenedPlace.attr('href', data.hash).text(window.location.href + data.hash);
        $visitedPlace.text(data.visited_times);
        $resultContainer.removeClass('is-invisible');
      })
      .fail(function(xhr) {
        const errorMsg = xhr.responseText || 'Sorry, something went wrong';
        showError(errorMsg);
      })
      .always(function() {
        toggleInput(false);
      });
  });

  $copyBtn.on('click', function() {
    const tempInput = $('<input>').val($shortenedPlace.text()).appendTo('body');
    tempInput.select();
    document.execCommand('copy');
    tempInput.remove();

    $copyBtn.text('Copied!');
    setTimeout(function() {
      $copyBtn.text('Copy');
    }, 1500);
  });
});
