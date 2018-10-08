$(document).ready(function(){




    $('body').on('submit', '#tokoss form', function(e){
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
                
            },
    
    
        })
    })
    
    
    
    //inapropriate function
    $('body').on('submit', '.inappropriate form', function(e){
        e.preventDefault();
    
        var publication_id = $(this).attr('action')
        $.ajax({
            method: "POST",
            async: true,
            url: '/publication/inappropriate/',
            data:$(this).serialize(),
            success: function (data){
              $('#publication_container'+publication_id).remove()
            },
            error: function (json){
                
            },
        })
    });
    
    
    $('body').on('submit', '.delete_publication form', function(e){
        e.preventDefault();
    
        var publication_id = $(this).attr('action')
        $.ajax({
            method: "POST",
            async: true,
            url: '/publication/delete/',
            data:$(this).serialize(),
            success: function (data){
              $('#publication_container'+publication_id).remove()
            },
            error: function (json){
               
            },
        })
    })
    
    
    
    
    
    $('body').on('submit', '.commentaire form', function(e){
        e.preventDefault()
    
        $.ajax({
    
            method: "POST",
            async: true,
            url: '/publication/addcomment/',
            data:$(this).serialize(),
            success: function (data){
                if (data.success){
                    var comment_number = data.comment_number
                    var id = data.id
                    var image_url = data.image
                    var comment = data.comment
                    $('#comment_count'+id).text(comment_number + ' commentaires')
                    $('#comment_by'+id).text(data.username)
                    $('#comment_comment'+id).html(comment + '<hr>')
    
                    $('#comment_img'+id).attr('src', image_url)
                    input = document.getElementById('input_comment'+id)
                    input.value = ''
    
    
                }
            },
            error: function (json){
               
            },
    
    
        })
    });
    
    
    
    
    
    
    $('body').on('click', '.comment_header span', function (){
    
        var publication_lire_id = $(this).attr('class')
        $.ajax({
    
            method: "GET",
            async: true,
            url: '/publication/getcomments/',
            data:{
                'publication': publication_lire_id
            },
            success: function (data){
                var id = data.id
                var div = document.getElementById('comments'+id)
                var num = data.comment_number
                div.innerHTML = '<span id="comment_by'+id+'" ><strong></strong></span><div class="mt-2 ml-4" id="comment_comment'+id+'" ><hr></div>'
                for (var i = 1; i <= num; i++){
                    div.innerHTML += '<h6 id="comment_by{{ publication.id }}" ><strong> '+ data['username'+i]+'</strong></h6><div class="mt-2 ml-4" id="comment_comment{{ publication.id }}" >'+ data['comment'+i]+'</div> <hr>'
                }
    
            },
            error: function (json){
                
            },
    
    
        })
    })
    
    
    
    
    })