// Filter toggle
document.querySelectorAll('.filter-toggle-btn').forEach(function(btn) {
  btn.addEventListener('click', function() {
    var panel = btn.closest('.filter-wrapper').querySelector('.filter-panel');
    if (!panel) return;
    var isOpen = panel.classList.contains('open');
    panel.classList.toggle('open', !isOpen);
    btn.classList.toggle('active', !isOpen);
  });
});

// Animal gallery thumbs
var mainImg = document.getElementById('gallery-main-img');
var thumbs = document.querySelectorAll('.animal-gallery__thumb');
if (mainImg && thumbs.length) {
  thumbs.forEach(function(thumb) {
    thumb.addEventListener('click', function() {
      var src = thumb.querySelector('img') ? thumb.querySelector('img').src : '';
      if (src) mainImg.src = src;
      thumbs.forEach(function(t) { t.classList.remove('active'); });
      thumb.classList.add('active');
    });
  });
  // строкуif (thumbs[0]) thumbs[0].classList.add('active'); — удалили,
  // главное фото показывается отдельно и не совпадает с первой миниатюрой
}

// Favourite heart (AJAX)
function getCsrfToken() {
  var el = document.querySelector('[name=csrfmiddlewaretoken]');
  if (el) return el.value;
  var match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : '';
}
document.querySelectorAll('.animal-card__fav').forEach(function(btn) {
  btn.addEventListener('click', function(e) {
    e.preventDefault();
    var animalId = btn.dataset.animalId;
    fetch('/animals/' + animalId + '/toggle-favorite/', {
      method: 'POST',
      headers: { 'X-CSRFToken': getCsrfToken(), 'Content-Type': 'application/json' },
      credentials: 'same-origin',
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
      if (data.status === 'ok') {
        btn.classList.toggle('active', data.is_favorite);
        var icon = btn.querySelector('.heart-icon');
        if (icon) icon.textContent = data.is_favorite ? '❤️' : '🤍';
      }
    })
    .catch(function() {});
  });
});

// Application type selector
var typeBtns = document.querySelectorAll('.type-selector__btn');
var titleInput = document.getElementById('id_title');
if (typeBtns.length && titleInput) {
  typeBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      typeBtns.forEach(function(b) { b.classList.remove('active'); });
      btn.classList.add('active');
      titleInput.value = btn.dataset.value;
    });
  });
}

// Auto-dismiss messages
document.querySelectorAll('.message').forEach(function(msg) {
  setTimeout(function() {
    msg.style.transition = 'opacity 0.4s';
    msg.style.opacity = '0';
    setTimeout(function() { msg.remove(); }, 400);
  }, 4000);
});
