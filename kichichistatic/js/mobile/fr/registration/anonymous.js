$(document).ready(function(){

var start = 1;
var limit = 2;



var maxreached = false;




$('#btn-connect-tab').click(function(){
    location = '#kichichi-nav'
    $('.tab2').css('display', 'none')
    $('.tab1').css('display', 'initial')
})

$('#btn-signup-tab').click(function(){
    $('.tab1').css('display', 'none')
    $('.tab2').css('display', 'initial')
})

var zero = 100;
$(window).scroll(function(){

    if ($(window).scrollTop() > 200 ){
        $('.form-q').addClass('fixed-top')
        $('.form-q').css('background-color', '#d7d4d4')

    } else {
        $('.form-q').css('background-color', 'transparent')
        $('.form-q').removeClass('fixed-top')
    }

//    zero = $(window).scrollTop();


    if ($(window).scrollTop() ==  $(document).height() - $(window).height()){

        if (!maxreached){
            get_publictions(start, limit);
        }


    }





})






function get_publictions(s, l) {

    if (maxreached){
        return false;
    }

    $.ajax({
        method: 'GET',
        url: '/accounts/get-publications/?start='+s+'&limit='+l+'&q=None',
        success: function(publication){

            start = start + 1
            limit = limit + 1
            var output = '<section class="publication-block mt-2 mb-2" >';
            output += '<div class="container mt-4 mb-4" id="publication-'+publication.id+'">'
            output += '<div class="publication-header">'
            output += '<img src="'+ publication.profil +'" class="publication_profil ml-4 mr-4" alt="">'
            output += '<span class="publication-username mr-4">'+publication.publisher+'</span>'
            output += '</div>'
            output += '</div>'
            output += '<div class="publication_title pl-4">'
            output += '<blockquote class="mt-4">'
            output += publication.text
            output += '<br>'
            if (publication.size != 'None'){
                output += '<strong>Taille: '+ publication.size +' Mo</strong>'
            }
            output += '</blockquote><hr></div>'
            output += '<div class="publication-file">'
            if (publication.audio != 'None'){
                output += '<audio src="'+publication.audio+'" class="form-control mt-2" controls preload="metadata"></audio>'
            }  else if (publication.video != 'None'){
                output += '<video src="'+publication.video+'" class="form-control mt-2" controls preload="metadata"></video>'
            } else if (publication.image != 'None'){
                output += '<img src="'+publication.image+'" class="form-control mt-2" alt="">'
            }
            output += '<hr>'
            output += '<div class="publication-appreciation mt-4 container row">'
            output += '<div class="col-12 text-center" id="tokoss">'
            output += '<img src="/static/images/tokoss/tokoss.png" id="tokoss_img{{ publication.id }}" alt="">'
            output += '<span id="tokoss{{ publication.id }}" class="ml-2" >'+publication.likes_number+'  Tokoss  </span>'
            output += '</div>'
            output += '</div></section>'
            if (publication.nomore == true){
                output += '<div class="col-8 offset-2 text-center container"><h6>Plus de nouvelles publications publiques</h6></div>'


            }
            $('.publications').append(output)
        },
        error:function(error){

            console.log(error)
        }
    })
//
//
//var output =   '<section class="publication-block" >';
//    output += '<div class="container mt-4 mb-4" id="publication-'+publication.id+'">'
//    output +=                    '<div class="publication-header">'
//    output +=                        '<img src="'+publication.profil+'" class="publication_profil ml-4 mr-4" alt="">'
//    output +=                        '<span class="publication-username mr-4">'+publication.publisher+'</span>'
//    output +=                    '</div>'
//    output +=                '</div>'
//    output +=                '<div class="publication_title pl-4">'
//    output +=                    '<blockquote class="mt-4">''
//    output +=                        publication.text
//    output +=                        '<br>'
//if (publication.is_file){
//    output += '<strong>Taille:'+ publication.size+' Mo</strong>'
//}
//
//                        '</blockquote>'
//                        '<hr>'
//                    '</div>'
//                    '<div class="publication-file">'
//if (publication.is_video){
//    output += '<video src="'+publication.file+'" class="form-control mt-2" controls preload="metadata"></video>'
//}
//if (publication.is_audio){
//    output += '<audio src="'+publication.file+'" class="form-control mt-2" controls preload="metadata"></audio>'
//}
//if (publication.is_image){
//    output += <img src="{{ publication.file.url }}" class="form-control mt-2" alt="">
//}
//    output +=                '</div><hr>'
//    output +=                '<div class="publication-appreciation mt-4 container row">'
//    output +=                    '<div class="col-4" id="tokoss">'
//    output +=                        '<img src="/kichichistatic/images/tokoss/tokoss.png" id="tokoss_img{{ publication.id }}" alt="">'
//    output +=                        '<span id="tokoss{{ publication.id }}" class="ml-2" >'+publication.tokoss+' Tokoss  </span>'
//    output +=                   '</div>'
//    output +=                    '<div class="col-4" id="share">'
//    output +=                        '<span class="ml-4 mr-2"><img src="kichichistatic/images/tokoss.png" alt=""></span>'
//    output +=                        'Partager'
//    output +=                    '</div>'
//    output +=                    '<div class="col-4 inappropriate" id="publication.id">'
//    output +=                        '<span class="ml-4 mr-2"> <button type="submit"><img src="kichichistatic/images/tokoss/Inappropriate.png" alt=""></button> </span>'
//    output +=                        'Inapproprié'
//    output +=                    '</div>'
//    output +=                '</div>'
//    output +=            '</section>'
//
//
//
//
//
//
//
//
//
//
//




}



















$("#signup-form").submit(function(e){
    e.preventDefault()

    $.ajax({

        method: "POST",
        url: '/accounts/signup/',
        async: true,
        data:$(this).serialize(),
        success: function (data){
            if (data.valid_username){
                document.getElementById("signup_username_label").innerHTML = 'Le nom d\'utilisateur ne peut contenir <br> que les signes "_" et "-"'
            } else if (data.passwords_match){
                document.getElementById("signup_username_label").innerHTML = "Les mots de passes ne correspondent pas"
            } else if (data.username_exist){
                document.getElementById("signup_username_label").innerHTML = "Ce nom d'utilisateur existe déjà"
            } else if (data.valid_contact_email){
                document.getElementById("signup_username_label").innerHTML = "Cette adresse électronique n'est pas valide"
            } else if (data.valid_contact_phone_number){
                document.getElementById("signup_username_label").innerHTML = "le numéro cellulaire doit être <br> de ce format +2438888888888"
            } else if (data.valid_password){
                document.getElementById("signup_username_label").innerHTML = "<ul><li>le mot de passe doit avoir <br> plus de 8 caractères </li><li>le mot de passe ne doit pas contenir <br> que des chiffres.</li></ul>"
            } else if (data.existing_mail_address){
                document.getElementById("signup_username_label").innerHTML = "Un autre utilisateur est inscrit avec cette adresse mail"
            } else if (data.existing_phone_number){
                document.getElementById("signup_username_label").innerHTML = "Un autre utilisateur est inscrit avec ce numéro"
            } else if (data.success) {
                location = '/'
            }
        },
        error: function (json){
            document.getElementById("signup_username_label").innerHTML = "Une erreur est survenue, <br> le formulaire n'a pas été soumis, <br>veuillez réessayer ultérieurement"
        },

    })
})

$("#login-form").submit(function(e){
    e.preventDefault()

    $.ajax({

        method: "POST",
        url: '/accounts/login/',
        async: true,
        data:$(this).serialize(),
        success: function (data){
            if (data.success){
                location = '/'
            } else if (data.error){
                if (!data.erroronpassword){
                    $("#login-username").css('background-color', 'darkkhaki')
                }
                $("#login-password").css('background-color', 'darkkhaki')
            }
        },
        error: function (json){
            $("#login-username").css('background-color', 'darkkhaki')
            $("#login-password").css('background-color', 'darkkhaki')
        },

    })
})

$("#login-username").on('keydown', function(){
    $("#login-username").css('background-color', 'white')
})
$("#login-password").on('keydown', function(){
    $("#login-password").css('background-color', 'white')
})








});






