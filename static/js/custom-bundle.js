"use strict";

// parallax function
// $(window).on("load",function(){
// 	var loc = window.location.search.substr(1);
// 	if(loc == "type=listing"){
// 		$("#id_request_type_0").prop('checked', true);
// 		$("#id_request_type_1").prop('checked', false);
// 		var headTxt = $("#id_request_type_0").attr('data-head');
// 		$('.variable-title').html(headTxt);
// 	}
// 	else{
// 		$("#id_request_type_1").prop('checked', true);
// 		$("#id_request_type_0").prop('checked', false);
// 		var headTxt = $("#id_request_type_1").attr('data-head');
// 		$('.variable-title').html(headTxt);
// 	}


// })


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

	if (!$(this).hasClass("drop-input")) {
		if ($(this).val() == "") {
			// $(this).closest(".input-item").removeClass("active");
			$(this).closest(".input-item").addClass("validation-error");
			$(this).closest(".input-item").find(".error span").html("can't be empty");
			sendForm = false;
		} else if ($(this).attr("name") == "email") {
			if ($(this).val() == "") {
				$(this).closest(".input-item").addClass("validation-error");
				$(this).closest(".input-item").find(".error span").html("can't be empty");
				sendForm = false;
			} else if (!/\S+@\S+\.\S+/.test($(this).val())) {
				$(this).closest(".input-item").addClass("validation-error");
				$(this).closest(".input-item").find(".error span").html("invalid email");
				sendForm = false;
			} else {
				$(this).closest(".input-item").removeClass("validation-error");
			}
		} else {
			$(this).closest(".input-item").removeClass("validation-error");
		}
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
		$(".list-form button[type ='submit']").attr('disabled', true);
		var that = $(this);
		var formData = new FormData(that.get(0));
		$.ajax({
			url: $(this).attr('action'),
			type: 'POST',
			contentType: false,
			processData: false,
			data: formData,

			success: function success(data) {
				$(".list-form button[type ='submit']").attr('disabled', false);
				if (that.hasClass("nomodal")) {
					$("body").removeClass("modal-open");
					$(".list-form .success-mess").addClass("active");
				} else {
					$(".thk-modal").addClass("active");
					$("body").addClass("modal-open");
				}

				that.find(".form-input").each(function () {
					if (!$(this).hasClass("noclear")) {
						$(this).val("");
					}
				});
			},
			error: function error(xhr, err, data) {
				$(".list-form button[type ='submit']").attr('disabled', false);
				if (that.hasClass("nomodal")) {
					$("body").removeClass("modal-open");
					$(".list-form .success-mess").addClass("active");
				} else {
					$(".err-modal").addClass("active");
					$("body").addClass("modal-open");
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
		if (blockID !== "#") {
			var elPos = document.querySelector(blockID).offsetTop;
			window.scroll({ top: elPos - 100, left: 0, behavior: 'smooth' });
		}
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

	$(".drop-wr input").closest(".drop-wr").find(".wrap-input__label").addClass("active");
	var selectVal = $(this).find("p").html();
	var inputValue = $(this).find("p").attr("data-value");
	$(".drop-wr .select-txt").html(selectVal);

	$(".drop-wr input").attr("value", inputValue);
	if ($(".drop-wr input").val() != "") {
		$(".drop-wr input").closest(".input-item").removeClass("validation-error");
	}
});

$(".lang-variant").click(function () {
	var lang = $(this).html();
	$(".cur-lang").html(lang);
});

$(".menu-mob__drop-wrap").click(function () {
	$(this).toggleClass("active");
});

// var VanillaRunOnDomReady = function() {

// 	var crop_max_width = 400;
// 	var crop_max_height = 400;
// 	var jcrop_api;
// 	var canvas;
// 	var context;
// 	var image;

// 	var prefsize;

// 	$("#crop-file").change(function() {
// 		loadImage(this);
// 	});

// 	function loadImage(input) {
// 		if (input.files && input.files[0]) {
// 			var reader = new FileReader();
// 			canvas = null;
// 			reader.onload = function(e) {
// 				image = new Image();
// 				image.onload = validateImage;
// 				image.src = e.target.result;
// 			}
// 			reader.readAsDataURL(input.files[0]);
// 		}
// 	}

// 	function dataURLtoBlob(dataURL) {
// 		var BASE64_MARKER = ';base64,';
// 		if (dataURL.indexOf(BASE64_MARKER) == -1) {
// 			var parts = dataURL.split(',');
// 			var contentType = parts[0].split(':')[1];
// 			var raw = decodeURIComponent(parts[1]);

// 			return new Blob([raw], {
// 				type: contentType
// 			});
// 		}
// 		var parts = dataURL.split(BASE64_MARKER);
// 		var contentType = parts[0].split(':')[1];
// 		var raw = window.atob(parts[1]);
// 		var rawLength = raw.length;
// 		var uInt8Array = new Uint8Array(rawLength);
// 		for (var i = 0; i < rawLength; ++i) {
// 			uInt8Array[i] = raw.charCodeAt(i);
// 		}

// 		return new Blob([uInt8Array], {
// 			type: contentType
// 		});
// 	}

// 	function validateImage() {
// 		if (canvas != null) {
// 			image = new Image();
// 			image.onload = restartJcrop;
// 			image.src = canvas.toDataURL('image/png');
// 		} else restartJcrop();
// 	}

// 	function restartJcrop() {
// 		if (jcrop_api != null) {
// 			jcrop_api.destroy();
// 		}
// 		$("#views").empty();
// 		$("#views").append("<canvas id=\"canvas\">");
// 		canvas = $("#canvas")[0];
// 		context = canvas.getContext("2d");
// 		canvas.width = image.width;
// 		canvas.height = image.height;
// 		context.drawImage(image, 0, 0);
// 		$("#canvas").Jcrop({
// 			onChange: selectcanvas,
// 			onRelease: clearcanvas,
// 			boxWidth: crop_max_width,
// 			boxHeight: crop_max_height,
// 			aspectRatio: 1 / 1
// 		}, function() {
// 			jcrop_api = this;
// 		});
// 		clearcanvas();
// 	}

// 	function clearcanvas() {
// 		prefsize = {
// 			x: 0,
// 			y: 0,
// 			w: canvas.width,
// 			h: canvas.height,
// 		};
// 	}

// 	function selectcanvas(coords) {
// 		prefsize = {
// 			x: Math.round(coords.x),
// 			y: Math.round(coords.y),
// 			w: Math.round(coords.w),
// 			h: Math.round(coords.h)
// 		};
// 	}

// 	function applyCrop() {
// 		canvas.width = prefsize.w;
// 		canvas.height = prefsize.h;
// 		context.drawImage(image, prefsize.x, prefsize.y, prefsize.w, prefsize.h, 0, 0, canvas.width, canvas.height);
// 		validateImage();
// 	}

// 	function applyScale(scale) {
// 		if (scale == 1) return;
// 		canvas.width = canvas.width * scale;
// 		canvas.height = canvas.height * scale;
// 		context.drawImage(image, 0, 0, canvas.width, canvas.height);
// 		validateImage();
// 	}

// 	function applyRotate() {
// 		canvas.width = image.height;
// 		canvas.height = image.width;
// 		context.clearRect(0, 0, canvas.width, canvas.height);
// 		context.translate(image.height / 2, image.width / 2);
// 		context.rotate(Math.PI / 2);
// 		context.drawImage(image, -image.width / 2, -image.height / 2);
// 		validateImage();
// 	}

// 	function applyHflip() {
// 		context.clearRect(0, 0, canvas.width, canvas.height);
// 		context.translate(image.width, 0);
// 		context.scale(-1, 1);
// 		context.drawImage(image, 0, 0);
// 		validateImage();
// 	}

// 	function applyVflip() {
// 		context.clearRect(0, 0, canvas.width, canvas.height);
// 		context.translate(0, image.height);
// 		context.scale(1, -1);
// 		context.drawImage(image, 0, 0);
// 		validateImage();
// 	}

// 	$("#views").keyup(function(e) {
// 		if(e.keyCode == 13){

// 			applyCrop();
// 		}
// 	});
// 	$("#scalebutton").click(function(e) {
// 		var scale = prompt("Scale Factor:", "1");
// 		applyScale(scale);
// 	});
// 	$("#rotatebutton").click(function(e) {
// 		applyRotate();
// 	});
// 	$("#hflipbutton").click(function(e) {
// 		applyHflip();
// 	});
// 	$("#vflipbutton").click(function(e) {
// 		applyVflip();
// 	});

// 	$("#form").submit(function(e) {
// 		e.preventDefault();
// 		formData = new FormData($(this)[0]);
// 		var blob = dataURLtoBlob(canvas.toDataURL('image/png'));
//   //---Add file blob to the form data
//   formData.append("cropped_image[]", blob);
//   $.ajax({
//   	url: "whatever.php",
//   	type: "POST",
//   	data: formData,
//   	contentType: false,
//   	cache: false,
//   	processData: false,
//   	success: function(data) {
//   		alert("Success");
//   	},
//   	error: function(data) {
//   		alert("Error");
//   	},
//   	complete: function(data) {}
//   });
// });


// }

// var alreadyrunflag = 0;

// if (document.addEventListener)
// 	document.addEventListener("DOMContentLoaded", function(){
// 		alreadyrunflag=1; 
// 		VanillaRunOnDomReady();
// 	}, false);
// else if (document.all && !window.opera) {
// 	document.write('<script type="text/javascript" id="contentloadtag" defer="defer" src="javascript:void(0)"><\/script>');
// 	var contentloadtag = document.getElementById("contentloadtag")
// 	contentloadtag.onreadystatechange=function(){
// 		if (this.readyState=="complete"){
// 			alreadyrunflag=1;
// 			VanillaRunOnDomReady();
// 		}
// 	}
// }

// window.onload = function(){
// 	setTimeout("if (!alreadyrunflag){VanillaRunOnDomReady}", 0);
// }


document.addEventListener("DOMContentLoaded", function () {
	openChat = function openChat() {
		if (document.getElementById("launcher") !== null) {
			var chatEl = document.getElementById("launcher");
			var iframeDoc = chatEl.contentWindow.document.body.getElementsByTagName("button")[0];
			iframeDoc.click();
		}
	};
});

var openChat;
var $zopim = '';

$(".vip").click(function (e) {
	if (document.documentElement.clientWidth > 992) {
		e.preventDefault();
		openChat();
	}
});

var zCh = function zCh() {
	if ($zopim == '') {
		setTimeout(function () {

			zCh();
		}, 200);
	} else {
		$zopim(function () {
			zE('webWidget', 'setLocale', 'en');
			$zopim.livechat.addTags('EXRATES');
		});
	}
};
if (document.documentElement.clientWidth > 992) {
	zCh();
}

$(document).ready(function () {
	// downloadPost();
	filterHeadFunc();
});

$('body').on('click', ".clearFilter", function (e) {
	e.preventDefault();
	var urlNoParam = window.location.href.split('?')[0];
	window.history.pushState('', '', urlNoParam);
	filterHeadFunc();
	downloadPost();
});

$(window).on('scroll', function (e) {
	var scrollSize = $(".analitics-item-wr").innerHeight() - 100 - $(window).innerHeight();
	if ($(document).scrollTop() > scrollSize) {
		if (scrollFlag) {
			scrollFlag = false;
			downloadPost();
		}
	}
});

window.addEventListener("popstate", function (e) {
	filterHeadFunc();
	var pageNumber = 1;
	downloadPost();
}, false);

var filterHeadFunc = function filterHeadFunc() {
	strGET = window.location.search.replace('?', '');
	if (strGET != "" && $("#template").length) {
		var filterParam = strGET.replace('=', '');
		$("#template .head-filter h5").html(filterParam);
		$("#template .tags-block span").html(filterParam);
		$("#template .tags-block a").attr("href", '/analytics/' + strGET);
		var filterHead = $("#template .filter-block").clone();
		$(".analitics-inner").prepend(filterHead);
	} else {
		$(".analitics-inner .filter-block").remove();
	}
};

$(".share-link a").click(function (e) {
	e.preventDefault();
	var shareUrl = $(this).closest(".analitics-item").find(".hidden-link").attr("href");
	if ($(this).closest(".share-link").hasClass("tg")) {
		window.open('https://telegram.me/share/url?url=' + shareUrl);
	}
	if ($(this).closest(".share-link").hasClass("fb")) {
		window.open('https://facebook.com/sharer/sharer.php?u=' + shareUrl);
	}
	if ($(this).closest(".share-link").hasClass("tw")) {
		window.open('https://facebook.com/sharer/sharer.php?u=' + shareUrl);
	}
});

var strGET;
var postPreview;
var pageNumber = 2;
var scrollFlag = true;
console.log(strGET);
var apiUrl;
var downloadPost = function downloadPost() {
	strGET = window.location.search.replace('?', '');
	if (strGET != "") {
		apiUrl = "/api/articles/?page=" + pageNumber + "&" + strGET;
	} else {
		apiUrl = "/api/articles/?page=" + pageNumber;
	}
	$.ajax({
		// url: "/api/articles/?page=" + pageNumber,
		url: apiUrl,
		type: 'GET',
		success: function success(data) {
			postPreview = "";
			console.log(data);
			console.log(data.results);
			postPreview = data.results;
			for (var i = 0; i < postPreview.length; i++) {
				$("#template .title h5").html(postPreview[i].title);
				$("#template .pic-container img").attr("src", postPreview[i].preview_image);
				$("#template .category p").html("");
				$("#template .category a").attr("href", postPreview[i].currency_pair_link);
				$("#template .category a").html(postPreview[i].currency_pair);
				$("#template .description p").html(postPreview[i].short_description);
				$("#template .date p").html(postPreview[i].published_at);
				$("#template .view p").html(postPreview[i].views);
				$("#template .hidden-link").attr("href", postPreview[i].link);
				var item = $("#template .analitics-item").clone();
				$(".analitics-item-wr").append(item);
			}
			pageNumber++;

			if (data.next != null) {
				scrollFlag = true;
			}
		},
		error: function error(xhr, err, data) {}
	});
};
"use strict";