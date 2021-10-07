//ふわっと見せるためのJS。3-5-3 ページが読み込まれたらすぐに動かしたい&画面をスクロールをしたら動かしたい場合内のソースコード使用

function fadeAnime(){
	// flipLeft
	$('.grid-item').each(function(){
		var elemPos = $(this).offset().top;
		var scroll = $(window).scrollTop();
		var windowHeight = $(window).height();
		if (scroll >= elemPos - windowHeight){
			$(this).addClass('flipLeft');
		}else{
			$(this).removeClass('flipLeft');
		}
	});
}

// 画面をスクロールをしたら動かしたい場合の記述
	$(window).scroll(function (){
	fadeAnime();/* アニメーション用の関数を呼ぶ*/
	});// ここまで画面をスクロールをしたら動かしたい場合の記述

// ページが読み込まれたらすぐに動かしたい場合の記述
	$(window).on('load', function(){
	fadeAnime();/* アニメーション用の関数を呼ぶ*/
	});// ここまでページが読み込まれたらすぐに動かしたい場合の記述
