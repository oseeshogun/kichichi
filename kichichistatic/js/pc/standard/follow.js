$(document).ready(function(){


$('body').on('submit', '#following_p form', function(e){
    e.preventDefault();
    var id = $(this).attr('action')

    $.ajax({
        method:'POST',
        async: true,
        url: '/user/follow/',
        data:$(this).serialize(),
        success: function (data){

            $('#prop_btn'+id).html(data.text)
            document.getElementsByClassName('type'+id).value = data.success

        },
        error: function (json){
           
        },
    })
})



})