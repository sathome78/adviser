"use strict";

// parallax function

function Paralax(parent, element, transition, animationSpeed, offset, adaptive) {
	var adaptiveMod;
	if (!adaptive) {
		adaptiveMod = 992;
	}
	if (adaptive) {
		adaptiveMod = adaptive;
	}
	if (parent !== null && window.innerWidth > adaptiveMod) {
		var sizeCalc = parseInt(getComputedStyle(document.body).fontSize) / 20;
		var elemOffset = parent.clientHeight / (animationSpeed * sizeCalc);

		if (window.pageYOffset + parent.clientHeight > parent.offsetTop) {
			var scrollSize = window.pageYOffset;
			if (offset) {
				element.setAttribute("style", "top:" + elemOffset + ";");
			}
			TweenMax.to(element, transition, { y: scrollSize / (animationSpeed * sizeCalc) });
		}
	}
	if (!(window.innerWidth > adaptiveMod)) {
		element.setAttribute("style", "top:" + "" + "transform:" + "");
		element.css("transform", "");
	}
};

document.addEventListener('scroll', function (e) {
	var ParalaxParent = document.querySelector(".fs-image-container");
	var ParalaxElement = document.querySelector(".fs-image-container img");
	Paralax(ParalaxParent, ParalaxElement, 0.1, 3, false, 1);
	var currentSection;
	if (document.querySelector(".scroll-block") !== null) {
		document.querySelectorAll(".scroll-block").forEach(function (i) {
			if (i.offsetTop - 120 < window.pageYOffset && i.offsetTop + i.clientHeight > window.pageYOffset) {
				currentSection = i.getAttribute("id");

				if (!document.querySelector(".advisor-navigation-item a[href='#" + currentSection + "']").closest(".advisor-navigation-item").classList.contains("active")) {
					document.querySelectorAll(".advisor-navigation-item").forEach(function (nav) {
						nav.classList.remove("active");
					});
					document.querySelector(".advisor-navigation-item a[href='#" + currentSection + "']").closest(".advisor-navigation-item").classList.add("active");
				}
			}
		});
	}
});

// end parallax function


// input label script

var activeInput = function activeInput(el) {
	if (el.val() !== "") {
		el.closest(".wrap-input").find(".wrap-input__label").addClass("active");
	} else {
		el.closest(".wrap-input").find(".wrap-input__label").removeClass("active");
	}
};

$(".wrap-input__input").keyup(function () {
	activeInput($(this));
});

$(".wrap-input__input").focusout(function () {
	activeInput($(this));
});

//end input label script


//open menu script

$(".burger").click(function () {
	$(".mobile-menu").toggleClass("active");
	if ($(".mobile-menu").hasClass("active")) {
		$("body").addClass("modal-open");
	} else {
		$("body").removeClass("modal-open");
	}
});

//end open menu script

//form validation script

$(".reqiered-field").keyup(function (e) {
	console.log($(this).val());
	if ($(this).val() == "") {
		$(this).closest(".input-item").addClass("validation-error");
		$(this).closest(".input-item").find(".error span").html("can't be empty");
		sendForm = false;
	} else if ($(this).attr("name") == "email") {
		if ($(this).val() == "") {
			$(this).closest(".input-item").addClass("validation-error");
			$(this).closest(".input-item").find(".error span").html("can't be empty");
			sendForm = false;
		} else if (!/\S+@\S+\.\S+/.test($(this).val())) {
			console.log(/\S+@\S+\.\S+/.test($(this).val()));
			$(this).closest(".input-item").addClass("validation-error");
			$(this).closest(".input-item").find(".error span").html("invalid email");
			sendForm = false;
		} else {
			$(this).closest(".input-item").removeClass("validation-error");
		}
	} else {
		$(this).closest(".input-item").removeClass("validation-error");
	}
});

$(".reqiered-field").focusout(function (e) {
	console.log($(this).val());
	if ($(this).val() == "") {
		$(this).closest(".input-item").addClass("validation-error");
		$(this).closest(".input-item").find(".error span").html("can't be empty");
		sendForm = false;
	} else if ($(this).attr("name") == "email") {
		if ($(this).val() == "") {
			$(this).closest(".input-item").addClass("validation-error");
			$(this).closest(".input-item").find(".error span").html("can't be empty");
			sendForm = false;
		} else if (!/\S+@\S+\.\S+/.test($(this).val())) {
			console.log(/\S+@\S+\.\S+/.test($(this).val()));
			$(this).closest(".input-item").addClass("validation-error");
			$(this).closest(".input-item").find(".error span").html("invalid email");
			sendForm = false;
		} else {
			$(this).closest(".input-item").removeClass("validation-error");
		}
	} else {
		$(this).closest(".input-item").removeClass("validation-error");
	}
});
//end form validation script


//ajax script
var sendForm;
$("form").on("submit", function (e) {
	e.preventDefault();
	var thisForm = $(this);
	sendForm = true;
	$(this).find(".reqiered-field").each(function () {
		console.log($(this).val());
		if ($(this).val() == "") {
			$(this).closest(".input-item").addClass("validation-error");
			$(this).closest(".input-item").find(".error span").html("can't be empty");
			sendForm = false;
		} else if ($(this).attr("name") == "email") {
			if ($(this).val() == "") {
				$(this).closest(".input-item").addClass("validation-error");
				$(this).closest(".input-item").find(".error span").html("can't be empty");
				sendForm = false;
			} else if (!/\S+@\S+\.\S+/.test($(this).val())) {
				console.log(/\S+@\S+\.\S+/.test($(this).val()));
				$(this).closest(".input-item").addClass("validation-error");
				$(this).closest(".input-item").find(".error span").html("invalid email");
				sendForm = false;
			} else {
				$(this).closest(".input-item").removeClass("validation-error");
			}
		} else {
			$(this).closest(".input-item").removeClass("validation-error");
		}
	});
	if (sendForm) {
		var that = $(this);
		var formData = new FormData(that.get(0));
		$.ajax({
			url: $(this).attr('action'),
			type: 'POST',
			contentType: false,
			processData: false,
			data: formData,

			success: function success(data) {
				$(".thk-modal").addClass("active");
				$("body").addClass("modal-open");
				if (that.hasClass("list-form")) {
					$("body").removeClass("modal-open");
					$(".list-form .success-mess").addClass("active");
				}

				that.find(".form-input").each(function () {
					$(this).val("");
				});
			},
			error: function error(xhr, err, data) {
				$(".err-modal").addClass("active");
				$("body").addClass("modal-open");
				console.log(that);
				if (that.hasClass("list-form")) {
					$("body").removeClass("modal-open");
					$(".list-form .success-mess").addClass("active");
				}
			}
		});
	}
});
//end ajax script

// modal close script
$(".close-trigger").click(function () {
	$(".modal").removeClass("active");
	$(".mobile-menu").removeClass("active");
	$(".sidebar").removeClass("active");
	$("body").removeClass("modal-open");
});

//end modal close script


// head change script

$(".radio-form-list").on('change', function () {
	console.log($(this).attr('data-head'));
	var headTxt = $(this).attr('data-head');
	$('.variable-title').html(headTxt);
});

//end head change script

// anchor scroll script

document.querySelectorAll("a[href*='#']").forEach(function (userItem) {
	userItem.addEventListener('click', function (e) {
		e.preventDefault();
		var anchor = this;
		var blockID = anchor.getAttribute('href');
		var elPos = document.querySelector(blockID).offsetTop;
		window.scroll({ top: elPos - 100, left: 0, behavior: 'smooth' });
	});
});

//end anchor scroll script


$(".open-sedebar-trigger").click(function () {
	$(".sidebar").addClass("active");
});

$(".drop-wr").click(function () {
	if ($(this).hasClass("active")) {
		$(this).removeClass("active");
	} else {
		$(this).addClass("active");
	}
});

$(".dropdown-item").click(function () {
	var selectVal = $(this).find("p").html();
	var inputValue = $(this).find("p").attr("data-value");
	$(".drop-wr .select-txt").html(selectVal);
	$(".drop-wr input").attr("value", inputValue);
});

var VanillaRunOnDomReady = function VanillaRunOnDomReady() {

	var crop_max_width = 400;
	var crop_max_height = 400;
	var jcrop_api;
	var canvas;
	var context;
	var image;

	var prefsize;

	$("#crop-file").change(function () {
		loadImage(this);
	});

	function loadImage(input) {
		if (input.files && input.files[0]) {
			var reader = new FileReader();
			canvas = null;
			reader.onload = function (e) {
				image = new Image();
				image.onload = validateImage;
				image.src = e.target.result;
			};
			reader.readAsDataURL(input.files[0]);
		}
	}

	function dataURLtoBlob(dataURL) {
		var BASE64_MARKER = ';base64,';
		if (dataURL.indexOf(BASE64_MARKER) == -1) {
			var parts = dataURL.split(',');
			var contentType = parts[0].split(':')[1];
			var raw = decodeURIComponent(parts[1]);

			return new Blob([raw], {
				type: contentType
			});
		}
		var parts = dataURL.split(BASE64_MARKER);
		var contentType = parts[0].split(':')[1];
		var raw = window.atob(parts[1]);
		var rawLength = raw.length;
		var uInt8Array = new Uint8Array(rawLength);
		for (var i = 0; i < rawLength; ++i) {
			uInt8Array[i] = raw.charCodeAt(i);
		}

		return new Blob([uInt8Array], {
			type: contentType
		});
	}

	function validateImage() {
		if (canvas != null) {
			image = new Image();
			image.onload = restartJcrop;
			image.src = canvas.toDataURL('image/png');
		} else restartJcrop();
	}

	function restartJcrop() {
		if (jcrop_api != null) {
			jcrop_api.destroy();
		}
		$("#views").empty();
		$("#views").append("<canvas id=\"canvas\">");
		canvas = $("#canvas")[0];
		context = canvas.getContext("2d");
		canvas.width = image.width;
		canvas.height = image.height;
		context.drawImage(image, 0, 0);
		$("#canvas").Jcrop({
			onChange: selectcanvas,
			onRelease: clearcanvas,
			boxWidth: crop_max_width,
			boxHeight: crop_max_height,
			aspectRatio: 1 / 1
		}, function () {
			jcrop_api = this;
		});
		clearcanvas();
	}

	function clearcanvas() {
		prefsize = {
			x: 0,
			y: 0,
			w: canvas.width,
			h: canvas.height
		};
	}

	function selectcanvas(coords) {
		prefsize = {
			x: Math.round(coords.x),
			y: Math.round(coords.y),
			w: Math.round(coords.w),
			h: Math.round(coords.h)
		};
	}

	function applyCrop() {
		canvas.width = prefsize.w;
		canvas.height = prefsize.h;
		context.drawImage(image, prefsize.x, prefsize.y, prefsize.w, prefsize.h, 0, 0, canvas.width, canvas.height);
		validateImage();
	}

	function applyScale(scale) {
		if (scale == 1) return;
		canvas.width = canvas.width * scale;
		canvas.height = canvas.height * scale;
		context.drawImage(image, 0, 0, canvas.width, canvas.height);
		validateImage();
	}

	function applyRotate() {
		canvas.width = image.height;
		canvas.height = image.width;
		context.clearRect(0, 0, canvas.width, canvas.height);
		context.translate(image.height / 2, image.width / 2);
		context.rotate(Math.PI / 2);
		context.drawImage(image, -image.width / 2, -image.height / 2);
		validateImage();
	}

	function applyHflip() {
		context.clearRect(0, 0, canvas.width, canvas.height);
		context.translate(image.width, 0);
		context.scale(-1, 1);
		context.drawImage(image, 0, 0);
		validateImage();
	}

	function applyVflip() {
		context.clearRect(0, 0, canvas.width, canvas.height);
		context.translate(0, image.height);
		context.scale(1, -1);
		context.drawImage(image, 0, 0);
		validateImage();
	}

	$("#views").keyup(function (e) {
		if (e.keyCode == 13) {

			applyCrop();
		}
	});
	$("#scalebutton").click(function (e) {
		var scale = prompt("Scale Factor:", "1");
		applyScale(scale);
	});
	$("#rotatebutton").click(function (e) {
		applyRotate();
	});
	$("#hflipbutton").click(function (e) {
		applyHflip();
	});
	$("#vflipbutton").click(function (e) {
		applyVflip();
	});

	$("#form").submit(function (e) {
		e.preventDefault();
		formData = new FormData($(this)[0]);
		var blob = dataURLtoBlob(canvas.toDataURL('image/png'));
		//---Add file blob to the form data
		formData.append("cropped_image[]", blob);
		$.ajax({
			url: "whatever.php",
			type: "POST",
			data: formData,
			contentType: false,
			cache: false,
			processData: false,
			success: function success(data) {
				alert("Success");
			},
			error: function error(data) {
				alert("Error");
			},
			complete: function complete(data) {}
		});
	});
};

var alreadyrunflag = 0;

if (document.addEventListener) document.addEventListener("DOMContentLoaded", function () {
	alreadyrunflag = 1;
	VanillaRunOnDomReady();
}, false);else if (document.all && !window.opera) {
	document.write('<script type="text/javascript" id="contentloadtag" defer="defer" src="javascript:void(0)"><\/script>');
	var contentloadtag = document.getElementById("contentloadtag");
	contentloadtag.onreadystatechange = function () {
		if (this.readyState == "complete") {
			alreadyrunflag = 1;
			VanillaRunOnDomReady();
		}
	};
}

window.onload = function () {
	setTimeout("if (!alreadyrunflag){VanillaRunOnDomReady}", 0);
};