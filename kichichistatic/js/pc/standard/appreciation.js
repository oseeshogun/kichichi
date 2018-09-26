$(document).ready(function(){




$("#tokoss form").submit(function(e){
    e.preventDefault()
    var id = $(this).attr('id')
    var tokoss = $(this).attr('toks')

    $.ajax({

        method: "POST",
        async: true,
        url: '/publication/tokoss/',
        data:$(this).serialize(),
        success: function (data){
            if (data.success){
                var likes = data.likes
                $('#tokoss'+id).text(likes + ' Tokoss')

                var image = document.getElementById('#tokoss_img'+id)
                if (data.unlike){
                    $('#tokoss_img'+id).attr('src', '/static/images/tokoss/not_tokoss.png')
                } else {
                    $('#tokoss_img'+id).attr('src', '/static/images/tokoss/tokoss.png')
                }

            }
        },
        error: function (json){
            console.log(json)
        },


    })
});




//inapropriate function
$('.inappropriate form').submit(function(e){
    e.preventDefault();

    var publication_id = $(this).attr('action')
    $.ajax({
        method: "POST",
        async: true,
        url: '/publication/inappropriate/',
        data:$(this).serialize(),
        success: function (data){
          $('#publication_container'+publication_id).hide()
        },
        error: function (json){
            console.log(json)
        },
    })
})


$('.delete_publication form').submit(function(e){
    e.preventDefault();

    var publication_id = $(this).attr('action')
    $.ajax({
        method: "POST",
        async: true,
        url: '/publication/delete/',
        data:$(this).serialize(),
        success: function (data){
          $('#publication_container'+publication_id).hide()
        },
        error: function (json){
            console.log(json)
        },
    })
})















})