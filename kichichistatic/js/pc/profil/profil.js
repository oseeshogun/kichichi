$(document).ready(function(){


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');



$('#file_profil').change(function(e){
    var file = $(this)[0].files;
    var input = document.getElementById('file_profil')
    var filename = e.target.value.split("\\").pop();
    $('.upload_span_profil').text(filename);
    var ext = filename.substring(filename.lastIndexOf('.')+1).toLowerCase();


    $('.upload_span_profil').text(filename);

    if (ext == 'jpg'){
        $("#btn_profil").css('display', 'initial')
    } else if (ext == 'jpeg'){
        $("#btn_profil").css('display', 'initial')
    } else if (ext == 'png'){
        $("#btn_profil").css('display', 'initial')
    } else {
        input.value = ""
        if (lang == 'fr'){
            $('.upload_span_profil').text('Le profil doit être une image');
        } else if (lang == 'en'){
            $('.upload_span_profil').text('The profile must be a picture');
        }
       
    }


})







$("#file").change(function(e){
    var file = $(this)[0].files;
    var input = document.getElementById('file')
    var filename = e.target.value.split("\\").pop();
    $('.upload_span').text(filename);
    var ext = filename.substring(filename.lastIndexOf('.')+1).toLowerCase();


    $('.text-red').text('')
    if (ext == 'mp4'){
        if (file[0].size/1050030 >  10){
            if (lang == 'fr'){
                $('.text-red').text('La taille limite pour les fichiers mp4 est de 10 Mb')
            } else if (lang == 'en'){
                $('.text-red').text('The maximum size for mp4 is 10 Mb')
            }
            
            input.value = "";
        }
    } else if (ext == '3gp') {
        if (file[0].size/1050030 >  10){
            if (lang == 'fr'){
                $('.text-red').text('La taille limite pour les fichiers 3gp est de 10 Mb')
            } else if (lang == 'en'){
                $('.text-red').text('The maximum size for 3gp is 10 Mb')
            }
            
            input.value = "";
        }
    } else if ( ext == 'mp3' ){
        if (file[0].size/1050030 >  5){
            if (lang == 'fr'){
                $('.text-red').text('La taille limite pour les fichiers mp3 est de 5 Mb')
            } else if (lang == 'en'){
                $('.text-red').text('The maximum size for mp3 is 5 Mb')
            }
            
            input.value = "";
        }
    }   else if (ext == 'aac') {
        if (file[0].size/1050030 >  5){
            if (lang == 'fr'){
                $('.text-red').text('La taille limite pour les fichiers aac est de 5 Mb')
            } else if (lang == 'en'){
                $('.text-red').text('The maximum size for aac is 5 Mb')
            }
            
            input.value = "";
        }
    }   else if (ext == 'jpg'){
        if (file[0].size/1050030 >  1){
            if (lang == 'fr'){
                $('.text-red').text('La taille limite pour les images est de 1 Mb')
            } else if (lang == 'en'){
                $('.text-red').text('The maximum size for pictures is 1 Mb')
            }
            
            input.value = "";
        }
    } else if (ext == 'jpeg'){
        if (file[0].size/1050030 >  1){
            if (lang == 'fr'){
                $('.text-red').text('La taille limite pour les images est de 1 Mb')
            } else if (lang == 'en'){
                $('.text-red').text('The maximum size for pictures is 1 Mb')
            }
            
            input.value = "";
        }
    } else if (ext == 'png'){
        if (file[0].size/1050030 >  1){
            if (lang == 'fr'){

            } else if (lang == 'en'){
                
            }
            $('.text-red').text('La taille limite pour les images est de 1 Mb')
            input.value = "";
        }
    } else if (ext == 'gif'){
        if (file[0].size/1050030 >  2){
            if (lang == 'fr'){
                $('.text-red').text('La taille limite pour les gif est de 2 Mb')
            } else if (lang == 'en'){
                $('.text-red').text('The maximum size for gifs is 2 Mb')
            }
            
            input.value = "";
        }
    } else {
        if (lang == 'fr'){
            $('.text-red').text('Ce type de fichier ne peut être posté')
        } else if (lang == 'en'){
            $('.text-red').text('This type of file is not supported!')    
        }
        
        input.value = "";
    }


});







var start = 2;
var limit = 3;

var maxreached = false;

var zero = 1000000;
$(window).scroll(function(){


    if ($(window).scrollTop() ==  $(document).height() - $(window).height()){

        if (!maxreached){
            loadpublication(start, limit, username);
        }
    }

    if ($(window).scrollTop() > zero){
        $('.navbar').hide();
    } else {
        $('.navbar').show();
    }

     zero = $(window).scrollTop();
});



function loadpublication(s, l, u){

    if (nopublication){
        return false;
    }

    if (maxreached){
        return false;
    }

    $.ajax({
        method: 'GET',
        url: '/profile/getpublication/?start='+s+'&limit='+l+'&username='+u,
        success: function(publication){

            start = start + 1
            limit = limit + 1



            var output = ''
            output += '<link rel="stylesheet" href="/static/css/bases/pc/publication.css">'
            output += '<div class="container publication_block mb-4 new_publication" id="publication_container'+publication.id+'">'
            output += '<div class="publication_header">'
            output += '<img src="'+ publication.profil +'" class="publication_profil ml-4 mr-4" alt="">'
            output += '<span class="publication_username mr-4">'+ publication.publisher +'</span>'
            output += '</div>'
            output += '<div class="publication_title">'
            output += '<blockquote class="mt-4">'
            output += publication.text
            output += '<br>'
            if (publication.is_file){
                if (lang == 'fr'){
                    output += '<strong>Taille: '+ publication.size +' Mo</strong>'
                }   else if (lang == 'en'){
                    output += '<strong>Size: '+ publication.size +' Mo</strong>'
                }
            }
            output += '</blockquote>'
            output += '<hr>'
            output += '</div>'
            output += '<div class="publication_file">'
            if (publication.audio){
                output += '<audio src="'+ publication.audio +'" class="form-control mt-2" controls preload="metadata"></audio>'
            } else if (publication.video){
                output += '<video src="'+ publication.video +'" class="form-control mt-2" controls preload="metadata"></video>'
            } else if (publication.image){
                output += '<img src="'+ publication.image +'" class="form-control mt-2" alt="">'
            }
            output += '</div>'
            output += '<hr>'
            output += '<div class="publication_appreciation mt-4 row">'
            output += '<div class="col-4" id="tokoss">'
            output += '<form action="/publication/tokoss/" class="" id="'+ publication.id +'" toks="'+ publication.likes_number +'" method="POST">'
            output += '<input type="hidden" name="csrfmiddlewaretoken" value="'+ csrftoken +'" />'
            output += '<input type="hidden" name="publication_id"  value="'+ publication.id +'">'
            output += '<button type="submit" class="ml-4 mr-2">'
            if (publication.liker){
                output += '<img src="/static/images/tokoss/tokoss.png" id="tokoss_img'+ publication.id +'" alt="">'
            } else {
                output += '<img src="/static/images/tokoss/not_tokoss.png" id="tokoss_img'+ publication.id +'" alt="">'
            }
            output += '</button>'
            output += '<span id="tokoss'+ publication.id +'" >'+ publication.likes_number +'  Tokoss  </span>'
            output += '</form>'
            output += '</div>'
            if (publication.is_him){
                output += '<div class="col-6" id="delete'+ publication.id +'" class="delete_publication">'
                output += '<form action="/publication/delete/" id="delete-form" method="post">'
                output += '<input type="hidden" name="csrfmiddlewaretoken" value="'+ csrftoken +'" />'
                output += '<button type="submit"><img src="/static/images/no.png" alt=""><span class="ml-4 mr-2">'
                if (lang == 'fr'){
                    output += 'Supprimer'
                } else if (lang == 'en'){
                    output += 'Delete'
                }
                output += '</span></button>'
                output += '</form></div>'
            } else {
                output += '<div class="col-6 inappropriate" id="inappropriate'+ publication.id +'">'
                output += '<form action="'+ publication.id +'" method="POST">'
                output += '<input type="hidden" name="csrfmiddlewaretoken" value="'+ csrftoken +'" />'
                output += '<input type="hidden" name="id"  value="'+ publication.id +'">'
                output += '<span class="ml-4 mr-2"> <button type="submit"><img src="/static/images/tokoss/Inappropriate.png" alt=""></button> </span>'
                if (lang == 'fr'){
                    output += 'Inapproprié'
                } else if (lang == 'en'){
                    output += 'Inappropriate'
                }
                output += '</form></div>'
            }
            output += '</div>'


            output += '<div class="mt-4 title_notifications comment_header">'
            output += '<span id="comment_count'+ publication.id +'" class="lire'+ publication.id +'" > '+ publication.comments_count
            if (lang == 'fr'){
                output += ' Commentaires'
            } else if (lang == 'en'){
                output += ' Comments'
            }
            output += '</span>'
            output += '<div id="comments'+ publication.id +'" class="comments mt-2 mb-2">'
            if (publication.comment_by != false){
                output += '<h6 id="comment_by'+ publication.id +'" ><strong>'+ publication.comment_by +'</strong></h6>'
                output += '<div class="mt-2 commentaire ml-4" id="comment_comment'+ publication.id +'" >'
                output += publication.comment
                output += '<hr>'

            }
            output += '</div>'
            output += '<img src="" class="mr-4 comment_img" id="comment_img'+ publication.id +'" alt=""> <span id="comment_by'+ publication.id +'" ></span>'
            output += '<div class="ml-4" id="comment_comment'+ publication.id +'" >'
            output += '</div>'
            output += '</div>'
            output += '<div class="commentaire">'
            output += '<form action="" id="comment'+ publication.id +'"  class="mt-2" method="post">'
            output += '<input type="hidden" name="csrfmiddlewaretoken" value="'+ csrftoken +'" />'
            output += '<input type="hidden" name="publication_id"  value="'+ publication.id +'">'
            output += '<input type="hidden" name="type" class="'+ publication.id +'"  value="follow">'
            if (lang == 'fr'){
                output += '<input type="text" id="input_comment{{ publication.id }}" class="form-control" name="comment" placeholder="Ecrivez un commentaire..." maxlength="70" required>'
            } else if (lang == 'en'){
                output += '<input type="text" id="input_comment{{ publication.id }}" class="form-control" name="comment" placeholder="Wriet a comment..." maxlength="70" required>'
            }
            output += '</form>'
            output += '</div>'
            output += '</div>'
            output += '</div>'


            if (publication.nomore){
                 if (lang == 'fr'){
                    output += ' <h6 class="text-center mt-4" style="color:gray">Plus de publications</h6>'
                } else if (lang == 'en'){
                    output += ' <h6 class="text-center mt-4" style="color:gray">No more publications</h6>'
                }

                maxreached = true
            }

            $('#publications').append(output)

            $('.new_publication  form').each(function(){
                $(this).prepend("")
            })
        },
        error:function(error){

        }
    })
}




$("#edit_profil").click(function(){
    $('#profil_form').css('display', 'initial')
    $(this).hide()
})
$('#edit_cancel').click(function(e){
    e.preventDefault();
    $('#profil_form').css('display', 'none');
    $("#edit_profil").show();
})









$('body').on('submit', '#dreamteam_demande', function(e){
    e.preventDefault()
    id = $(this).attr('action')
        $.ajax({
        method:'POST',
        async: true,
        url: '/dreamteam/demande/',
        data:$(this).serialize(),
        success: function (data){
            if (data.add){
                if (lang == 'fr'){
                    $('#dreamtean_btn'+id).text('Annuler la demande')
                } else if (lang == 'en'){
                    $('#dreamtean_btn'+id).text('Cancel request')
                }
                
            }
            if (data.remove){
                if (lang == 'fr'){
                    $('#dreamtean_btn'+id).text('Ajouter à la dream team')
                } else if (lang == 'en'){
                    $('#dreamtean_btn'+id).text('Add to dream team')
                }
                
            }

        },
        error: function (json){
            
        },
    })

})




































































})