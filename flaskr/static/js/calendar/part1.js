
	(function(){

		'use strict';

		var dayNamesShort = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'];
		var monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
		var icon = '<svg viewBox="0 0 512 512"><polygon points="268.395,256 134.559,121.521 206.422,50 411.441,256 206.422,462 134.559,390.477 "/></svg>';

		var root = document.getElementById('picker1');
		var dateInput = document.getElementById('date1');
		var altInput = document.getElementById('alt1');
		var doc = document.documentElement;

		function format ( dt ) {
			// attention code de porc:
			var ZeMonth = dt.getMonth() + 1;
			if (ZeMonth < 10) { ZeMonth = '0' + ZeMonth; }
			var ZeDay = dt.getDate();
			if (ZeDay < 10) { ZeDay = '0' + ZeDay; }
			return Picker.prototype.pad(dt.getFullYear() + '-' + ZeMonth + '-' + ZeDay);
			// return Picker.prototype.pad(dt.getDate()) + ' ' + monthNames[dt.getMonth()].slice(0,3) + ' ' + dt.getFullYear();
		}

		function show ( ) {
			root.removeAttribute('hidden');
		}

		function hide ( ) {
			root.setAttribute('hidden', '');
			doc.removeEventListener('click', hide);
		}

		function onSelectHandler ( ) {

			var value = this.get();

			if ( value.start ) {
				dateInput.value = value.start.Ymd();
				altInput.value = format(value.start);
				hide();
			}
		}

		var picker = new Picker(root, {
			min: new Date(dateInput.min),
			max: new Date(dateInput.max),
			icon: icon,
			twoCalendars: false,
			dayNamesShort: dayNamesShort,
			monthNames: monthNames,
			onSelect: onSelectHandler
		});

		root.parentElement.addEventListener('click', function ( e ) { e.stopPropagation(); });

		dateInput.addEventListener('change', function ( ) {

			if ( dateInput.value ) {
				picker.select(new Date(dateInput.value));
			} else {
				picker.clear();
			}
		});

		altInput.addEventListener('focus', function ( ) {
			altInput.blur();
			show();
			doc.addEventListener('click', hide, false);
		});

	}());
