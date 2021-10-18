var application = document.querySelector('.detail-application');

application.addEventListener('click', function() {
    var result = window.confirm('応募してもいいですか？');

    if( result ) {
        console.log('応募しました。');
    }
})

var kick = document.querySelector('.detail-kick');
kick.addEventListener('click', function() {
    var result = window.confirm('応募を取り消しますか？');

    if( result ) {
        console.log('応募を取り消しました。');
    }
})