// cookie
$.ajaxSetup({
	beforeSend: function (xhr, settings) {
	function getCookie(name) {
		var cookieValue = null;
		if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
			cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
			break;
			}
		}
		}
		return cookieValue;
	}
	if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
		xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	}
	}
});

// like
$(document).on("click", ".post-liked", function () {
	var id = $(this).data('id');
	$.ajax({
	type: "post",
	url: "/like/",
	data: {
		id: id,
		csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
	},
	success: function (data) {
		$("#post-like-" + id).removeClass("post-liked a_liked liked").addClass("post-like");
		var like_count = data["like_count"]
		$("#like-count-" + id).html(like_count);
	}
	});
});
$(document).on("click", ".post-like", function () {
	var id = $(this).data('id');
	$.ajax({
	type: "post",
	url: "/like/",
	data: {
		id: id,
		csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
	},
	success: function (data) {
		$("#post-like-" + id).removeClass("post-like").addClass("post-liked liked");
		var like_count = data["like_count"]
		$("#like-count-" + id).html(like_count);
	}
	});
});

// follow
$(document).on("click", ".user-follow", function () {
	var id = $(this).data('id');
	$.ajax({
	  type: "post",
	  url: "/accounts/follow/",
	  data: {
		id: id,
		csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
	  },
	  success: function (data) {
		$("#user-follow-" + id).removeClass("user-follow").addClass("user-disfollow");
		var targetSrc = $("#user-follow-" + id+' img').attr('src'); // 画像URLを取得
		// var replaceURL = targetSrc.replace('watch_gray.png','watch_white.png');
		if(targetSrc){
			var replaceURL = targetSrc.replace('watch_white.png', 'watch_gray.png');
			$("#user-follow-" + id + ' img').attr({src:replaceURL});
		} else{
			$("#user-follow-" + id).html("フォロー")
		}
		var follow_count = data["follow_count"]
		$("#follow-count-" + id).html(follow_count);
		alert(data["message"])
	  }
	});
});
$(document).on("click", ".user-disfollow", function () {
	var id = $(this).data('id');
	$.ajax({
	  type: "post",
	  url: "/accounts/follow/",
	  data: {
		id: id,
		csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
	  },
	  success: function (data) {
		$("#user-follow-" + id).removeClass("user-disfollow").addClass("user-follow");
		var targetSrc = $("#user-follow-" + id + ' img').attr('src'); // 画像URLを取得
		// var replaceURL = targetSrc.replace('watch_white.png', 'watch_gray.png');
		if(targetSrc){
			var replaceURL = targetSrc.replace('watch_gray.png','watch_white.png');
			$("#user-follow-" + id + ' img').attr({src:replaceURL});
		} else{
			$("#user-follow-" + id).html("フォロー解除")
		}
		var follow_count = data["follow_count"]
		$("#follow-count-" + id).html(follow_count);
		alert(data["message"])
	  }
	});
});

// apply
$(document).on("click", ".post-apply", function () {
	var id = $(this).data('id');
	$.ajax({
	type: "post",
	url: "/apply/",
	data: {
		id: id,
		csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
	},
	success: function (data) {
		if (confirm("本当に応募してもよいですか？") === false){
			return
		}
		$("#post-apply-" + id).removeClass("post-apply").addClass("post-disapply");
		$("#post-apply-" + id).removeClass("detail-application").addClass("detail-kick");
		$("#post-apply-" + id).html("取り下げ")
		var apply_count = data["apply_count"]
		$("#apply-count-" + id).html(apply_count);
		// alert(data["message"])
	}
	});
});
$(document).on("click", ".post-disapply", function () {
	var id = $(this).data('id');
	$.ajax({
	type: "post",
	url: "/apply/",
	data: {
		id: id,
		csrfmiddlewaretoken: $("#csrfmiddlewaretoken").val()
	},
	success: function (data) {
		if (confirm("本当に取り下げてよいですか？") === false){
			return
		}
		$("#post-apply-" + id).removeClass("post-disapply").addClass("post-apply");
		$("#post-apply-" + id).removeClass("detail-kick").addClass("detail-application");
		$("#post-apply-" + id).html("応募")
		var apply_count = data["apply_count"]
		$("#apply-count-" + id).html(apply_count);
		// alert(data["message"])
	}
	});
});
