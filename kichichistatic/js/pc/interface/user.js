$(".notifications div button").each(function(){
    $(this).hide()
})


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


$(document).ready(function(){

var h = $(window).height()
$('#first_section').css('height', h+'px')
$('#first_section').hover(function(){
        document.documentElement.style.setProperty('--display','initial')
    }, function(){
        document.documentElement.style.setProperty('--display','none')
})

$(".notifications div").hover(
    function (){
        var elemen = $(this).attr('id')
        $("button[id='"+elemen+"']").show()
    },
    function (){
        var elemen = $(this).attr('id')
        $("button[id='"+elemen+"']").hide()
    }
)

$('body').on('submit','#in_no', function(e){
    e.preventDefault();
    var username = document.getElementById('profil_username').innerText
    $.ajax({
        method: "POST",
        async: true,
        url: '/dreamteam/no/',
        data:$(this).serialize(),
        success: function (data){
        var notification_id = data.id
          $('#notification'+notification_id).hide()
          $("#notification_number").text(data.number)
        },
        error: function (json){
            
        },
    })


})

$('.notifications form').submit(function(e){
    e.preventDefault();
    var username = document.getElementById('profil_username').innerText
    $.ajax({
        method: "POST",
        async: true,
        url: '/user/delete/notification/',
        data:$(this).serialize(),
        success: function (data){
        var notification_id = data.id
          $('#notification'+notification_id).hide()
          $("#notification_number").text(data.number)
        },
        error: function (json){
            
        },
    })
})

var start = 2;
var limit = 3;

var maxreached = false;

var zero = 1000000;
$(window).scroll(function(){


    if ($(window).scrollTop() ==  $(document).height() - $(window).height()){

        if (!maxreached){
            loadpublication(start, limit, q);
        }
    }

    if ($(window).scrollTop() > zero){
        $('.navbar').hide();
    } else {
        $('.navbar').show();
    }
     zero = $(window).scrollTop();
});



function loadpublication(s, l, q){

    if (nomore == 'True'){
        return false;
    }

    if (maxreached){
        return false;
    }

    $.ajax({
        method: 'GET',
        url: '/publication/get/?start='+s+'&limit='+l+'&q='+q,
        success: function(publication){

            start = start + 1
            limit = limit + 1

            if (publication.tonot){
                return false;
            }

            var output = ''

            if (publication.ads){
                output += '<div class="ads publication_block mt-4 mb-4">'
                output += '<div class="publication_header">'
                output += '<h2>Πthon 1.0.2</h2>'
                if (lang == 'fr'){
                    output += '<h6>Logiciel en téléchargement gratuit</h6><hr>'
                } else if (lang == 'en'){
                    output += '<h6>Download the sofware for free</h6><hr>'
                }
                if (lang == 'fr'){
                    output += '<a href="http://infteamcd.pythonanywhere.com" target="_blank">Cliquez ici pour télécharger</a>'
                } else if (lang == 'en'){
                    output += '<a href="http://infteamcd.pythonanywhere.com" target="_blank">Clic here to download</a>'
                }
                
                output += '</div>'
                output += '<div class="publication_file">'
                output += '<img src="/static/images/stat.gif" class="form-control mt-2" alt="">'
                output += '</div>'
                output += '</div>'
            }

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
                output += '<input type="hidden" name="id"  value="'+ publication.id +'">'
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
                output += '<input type="text" id="input_comment'+ publication.id +'" class="form-control" name="comment" placeholder="Ecrivez un commentaire..." maxlength="70" required>'
            } else if (lang == 'en'){
                output += '<input type="text" id="input_comment'+ publication.id +'" class="form-control" name="comment" placeholder="Wriet a comment..." maxlength="70" required>'
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



$('#team-message').submit(function(e){
    e.preventDefault();
    $.ajax({
        method:'POST',
        url:'/accounts/message/',
        async:true,
        data:$(this).serialize(),
        success:function(data){
            if (lang == 'fr'){
                $('#team-message').html('<h1 class="jumbotron display-4">Votre message a été envoyé</h1>')
            } else if (lang == 'en'){
                $('#team-message').html('<h1 class="jumbotron display-4">Your message has been sent</h1>')
            }
            
        },
        error:function(data){
           
        },
    })
})








})




