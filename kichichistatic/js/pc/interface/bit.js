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
            console.log(json)
        },
    })
})

var start = 2;
var limit = 3;

var maxreached = false;


$(window).scroll(function(){
    if ($(window).scrollTop() ==  $(document).height() - $(window).height()){

        if (!maxreached){
            loadpublication(start, limit);
        }
    }

});



function loadpublication(start, limit){

    if (maxreached){
        return false;
    }

    $.ajax({
        method: 'GET',
        url: '/publication/get/?start='+start+'&limit='+limit,
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
            output += '<span id="tokoss'+ publication.id +'">'+ publication.likes_number +'  Tokoss  </span>'
            output += '</form>'
            output += '</div>'
            output += ''
            output += ''
            output += ''
            output += ''
            output += ''
            output += ''




            if (publication.nomore){

                maxreached = true
            }

            $('#publications').append(output)

            $('.new_publication  form').each(function(){
                $(this).prepend("")
            })
        },
        error:function(error){

            console.log(error)
        }
    })






}












})

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
            console.log(json)
        },


    })
})
