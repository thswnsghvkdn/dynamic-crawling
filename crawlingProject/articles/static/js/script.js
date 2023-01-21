$(document).ready(function(){
    $('#create').on('click', function(){
        $.ajax({
            url: 'create/',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(){
                alert("크롤링 완료");
            }
        });
    });
});
  