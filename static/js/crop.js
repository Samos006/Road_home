/* static/js/crop.js
   Требует Cropper.js подключённого на странице через CDN.
   Экспортирует глобально: openCropModal(file, aspectRatio, onDone)
*/
(function () {

  /* Создаём модалку один раз при загрузке */
  var overlay = document.createElement('div');
  overlay.id  = 'crop-overlay';
  overlay.style.cssText = [
    'display:none',
    'position:fixed',
    'inset:0',
    'background:rgba(0,0,0,.78)',
    'z-index:9999',
    'align-items:center',
    'justify-content:center',
    'padding:20px',
  ].join(';');

  overlay.innerHTML =
    '<div style="background:#fff;border-radius:16px;padding:24px;max-width:680px;' +
               'width:100%;display:flex;flex-direction:column;gap:16px;max-height:90vh;">' +

      '<div style="display:flex;justify-content:space-between;align-items:center;">' +
        '<span style="font-weight:800;font-size:18px;color:#2e3532;">Обрезать фотографию</span>' +
        '<button id="crop-x" type="button" style="background:none;border:none;' +
                'font-size:24px;cursor:pointer;color:#7a6e66;line-height:1;">✕</button>' +
      '</div>' +

      '<div style="overflow:hidden;border-radius:10px;background:#2e3532;max-height:52vh;">' +
        '<img id="crop-img" src="" alt="" style="display:block;max-width:100%;max-height:52vh;" />' +
      '</div>' +

      '<p style="font-size:13px;color:#7a6e66;text-align:center;margin:0;">' +
        'Перетащите область · прокрутите колёсиком для масштабирования' +
      '</p>' +

      '<div style="display:flex;gap:12px;justify-content:flex-end;">' +
        '<button id="crop-cancel" type="button" style="padding:9px 22px;border-radius:50px;' +
                'border:2px solid #e0d4c8;background:#fff;font-size:14px;' +
                'font-weight:700;cursor:pointer;">Отмена</button>' +
        '<button id="crop-ok" type="button" style="padding:9px 28px;border-radius:50px;' +
                'border:none;background:#8b2635;color:#fff;font-size:14px;' +
                'font-weight:700;cursor:pointer;">✓ Готово</button>' +
      '</div>' +

    '</div>';

  document.addEventListener('DOMContentLoaded', function () {
    document.body.appendChild(overlay);
  });

  var currentCropper = null;

  /* CSS для круговой обрезки — вставляется один раз */
  var _circleStyle = document.createElement('style');
  _circleStyle.textContent =
    '.crop-circle .cropper-view-box,' +
    '.crop-circle .cropper-face { border-radius: 50%; }' +
    '.crop-circle .cropper-view-box { box-shadow: 0 0 0 1px #fff, 0 0 0 9999px rgba(0,0,0,.5); outline:0; }';
  document.head.appendChild(_circleStyle);

  /* Основная функция */
  window.openCropModal = function (file, aspectRatio, onDone) {
    var img = document.getElementById('crop-img');
    overlay.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    /* Круговой режим только для аватара (1:1) */
    var isCircle = (aspectRatio === 1);
    var cropWrap = img.parentElement;
    if (cropWrap) cropWrap.classList.toggle('crop-circle', isCircle);

    var reader = new FileReader();
    reader.onload = function (e) {
      img.src = e.target.result;
      if (currentCropper) { currentCropper.destroy(); currentCropper = null; }
      currentCropper = new Cropper(img, {
        aspectRatio      : aspectRatio,
        viewMode         : 1,
        dragMode         : 'move',
        autoCropArea     : 0.95,
        restore          : false,
        guides           : !isCircle,   // сетка только для прямоугольника
        center           : true,
        highlight        : false,
        cropBoxMovable   : true,
        cropBoxResizable : true,
        toggleDragModeOnDblclick: false,
      });
    };
    reader.readAsDataURL(file);

    document.getElementById('crop-ok').onclick = function () {
      if (!currentCropper) return;
      currentCropper.getCroppedCanvas({
        maxWidth: 1400, maxHeight: 1400,
        imageSmoothingEnabled: true, imageSmoothingQuality: 'high',
      }).toBlob(function (blob) {
        closeModal();
        onDone(blob);
      }, 'image/jpeg', 0.88);
    };

    document.getElementById('crop-cancel').onclick = closeModal;
    document.getElementById('crop-x').onclick       = closeModal;
  };

  function closeModal() {
    overlay.style.display = 'none';
    document.body.style.overflow = '';
    if (currentCropper) { currentCropper.destroy(); currentCropper = null; }
  }


  /* ══ Инициализации ══ */

  document.addEventListener('DOMContentLoaded', function () {

    /* ── Аватар ── */
    var avatarTrigger = document.getElementById('avatar-input');
    var avatarPreview = document.getElementById('avatar-preview');
    var avatarReal    = document.getElementById('avatar-real-input');

    if (avatarTrigger && avatarReal) {
      avatarTrigger.addEventListener('change', function () {
        var file = this.files[0];
        if (!file) return;
        openCropModal(file, 1, function (blob) {
          if (avatarPreview) {
            avatarPreview.src = URL.createObjectURL(blob);
            avatarPreview.style.display = 'block';
          }
          var f = new File([blob], file.name, { type: 'image/jpeg' });
          var dt = new DataTransfer();
          dt.items.add(f);
          avatarReal.files = dt.files;
        });
      });
    }

    /* ── Фото животных (очередь) ── */
    var animalTrigger  = document.getElementById('animal-photos-trigger');
    var animalReal     = document.getElementById('animal-photos-real');
    var animalPreviews = document.getElementById('animal-photos-previews');
    var animalCounter  = document.getElementById('animal-photos-count');

    if (animalTrigger && animalReal) {
      var queue = [], croppedFiles = [];

      animalTrigger.addEventListener('change', function () {
        queue = Array.from(this.files);
        croppedFiles = [];
        if (animalPreviews) animalPreviews.innerHTML = '';
        cropNext();
      });

      function cropNext() {
        if (queue.length === 0) {
          var dt = new DataTransfer();
          croppedFiles.forEach(function (f) { dt.items.add(f); });
          animalReal.files = dt.files;
          if (animalCounter) {
            animalCounter.textContent = croppedFiles.length + ' фото выбрано';
          }
          return;
        }
        var file = queue.shift();
        openCropModal(file, 4 / 3, function (blob) {
          var f = new File([blob], file.name, { type: 'image/jpeg' });
          croppedFiles.push(f);

          if (animalPreviews) {
            var wrap  = document.createElement('div');
            wrap.style.cssText = 'position:relative;display:inline-block;margin:4px;';
            var img   = document.createElement('img');
            img.src   = URL.createObjectURL(blob);
            img.style.cssText = 'width:96px;height:72px;object-fit:cover;border-radius:8px;' +
                                'border:2px solid #e0d4c8;display:block;';
            var badge = document.createElement('span');
            badge.textContent  = croppedFiles.length;
            badge.style.cssText = 'position:absolute;top:4px;left:4px;background:#8b2635;' +
              'color:#fff;font-size:10px;font-weight:700;border-radius:50%;' +
              'width:18px;height:18px;display:flex;align-items:center;justify-content:center;';
            wrap.appendChild(img);
            wrap.appendChild(badge);
            animalPreviews.appendChild(wrap);
          }
          cropNext();
        });
      }
    }

  });

})();
