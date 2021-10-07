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
		$("#post-like-" + id).removeClass("post-liked text-secondary").addClass("post-like text-dark");
		$("#post-like-" + id).html("いいね")
		var like_count = data["like_count"]
		$("#like-count-" + id).html(like_count);
		alert(data["message"])
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
		$("#post-like-" + id).removeClass("post-like text-dark").addClass("post-liked text-secondary");
		$("#post-like-" + id).html("いいねしました")
		var like_count = data["like_count"]
		$("#like-count-" + id).html(like_count);
		alert(data["message"])
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
		$("#user-follow-" + id).html("フォロー")
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
		$("#user-follow-" + id).html("フォロー解除")
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
		$("#post-apply-" + id).removeClass("post-apply").addClass("post-disapply");
		$("#post-apply-" + id).html("応募")
		var apply_count = data["apply_count"]
		$("#apply-count-" + id).html(apply_count);
		alert(data["message"])
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
		$("#post-apply-" + id).removeClass("post-disapply").addClass("post-apply");
		$("#post-apply-" + id).html("取り下げ")
		var apply_count = data["apply_count"]
		$("#apply-count-" + id).html(apply_count);
		alert(data["message"])
	}
	});
});
