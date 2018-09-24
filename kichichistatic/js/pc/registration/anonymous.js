$(document).ready(function(){

var start = 1;
var limit = 2;


var maxreached = false;

$(window).scroll(function(){
    if ($(window).scrollTop() ==  $(document).height() - $(window).height()){
        if (!maxreached){
                get_publictions(start, limit,q);
            }
        }
});



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
                    $("#username").css('background-color', 'darkkhaki')
                }
                $("#password").css('background-color', 'darkkhaki')
            }
        },
        error: function (json){
            $("#username").css('background-color', 'darkkhaki')
            $("#password").css('background-color', 'darkkhaki')
        },

    })
})

$("#username").on('keydown', function(){
    $("#username").css('background-color', 'white')
})
$("#password").on('keydown', function(){
    $("#password").css('background-color', 'white')
})





$("#signup-form").submit(function(e){
    e.preventDefault()

    $.ajax({

        method: "POST",
        url: '/accounts/signup/',
        async: true,
        data:$(this).serialize(),
        success: function (data){
            if (data.valid_username){
                if (lang == 'fr'){
                    document.getElementById("signup_username_label").innerHTML = 'Le nom d\'utilisateur ne peut contenir <br> que les signes "_" et "-"'
                } else if (lang == 'en'){
                    document.getElementById("signup_username_label").innerHTML = 'The username must only contain <br> the signs "_" et "-"'
                }
            } else if (data.passwords_match){
                if (lang == 'fr'){
                    document.getElementById("signup_username_label").innerHTML = "Les mots de passes ne correspondent pas"
                }   else if (lang == 'en') {
                    document.getElementById("signup_username_label").innerHTML = "The passwords don't match"
                }
            } else if (data.username_exist){
                if (lang == 'fr'){
                    document.getElementById("signup_username_label").innerHTML = "Ce nom d'utilisateur existe déjà"
                } else if (lang == 'en') {
                    document.getElementById("signup_username_label").innerHTML = "This username is in use"
                }
            } else if (data.valid_contact_email){
                if (lang == 'fr'){
                    document.getElementById("signup_username_label").innerHTML = "Cette adresse électronique n'est pas valide"
                } else if (lang == 'en') {
                    document.getElementById("signup_username_label").innerHTML = "This email address is not valid"
                }
            } else if (data.valid_contact_phone_number){
                if (lang == 'fr'){
                    document.getElementById("signup_username_label").innerHTML = "le numéro cellulaire doit être <br> de ce format +2438888888888"
                } else if (lang == 'en') {
                    document.getElementById("signup_username_label").innerHTML = "The phone number must be <br> in this format +2438888888888"
                }
            } else if (data.valid_password){
                if (lang == 'fr'){
                    document.getElementById("signup_username_label").innerHTML = "<ul><li>le mot de passe doit avoir <br> plus de 8 caractères </li><li>le mot de passe ne doit pas contenir <br> que des chiffres.</li></ul>"
                } else if (lang == 'en') {
                    document.getElementById("signup_username_label").innerHTML = "<ul><li>The password must have <br> more than 8 caracters </li><li>The password must not contain <br> only digits.</li></ul>"
                }
            } else if (data.existing_mail_address){
                if (lang == 'fr'){
                    document.getElementById("signup_username_label").innerHTML = "Un autre utilisateur est inscrit avec cette adresse mail"
                } else if (lang == 'en') {
                    document.getElementById("signup_username_label").innerHTML = "An other user has this email address"
                }
            } else if (data.existing_phone_number){
                if (lang == 'fr'){
                    document.getElementById("signup_username_label").innerHTML = "Un autre utilisateur est inscrit avec ce numéro"
                } else if (lang == 'en') {
                    document.getElementById("signup_username_label").innerHTML = "An other user has this phone number"
                }
            } else if (data.success) {
                location = '/'
            }
        },
        error: function (json){
            if (lang == 'fr'){
                document.getElementById("signup_username_label").innerHTML = "Une erreur est survenue, <br> le formulaire n'a pas été soumis, <br>veuillez réessayer ultérieurement"
            } else if (lang == 'en'){
                document.getElementById("signup_username_label").innerHTML = "An error occured, <br> the form was not summitted, <br> please, try again later"
            }
        },

    })
})




function get_publictions(s, l, q) {

    if (maxreached){
        return false;
    }

    $.ajax({
        method: 'GET',
        url: '/accounts/get-publications/?start='+s+'&limit='+l+'&q='+q,
        success: function(publication){

            start = start + 1
            limit = limit + 1
            var output = '<section class="publication-block" >';
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
                if (lang == 'fr'){
                    output += '<strong>Taille: '+ publication.size +' Mo</strong>'
                } else if (lang == 'en'){
                    output += '<strong>Size: '+ publication.size +' Mo</strong>'
                }
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
            output += '<div class="col-4" id="tokoss">'
            output += '<img src="/static/images/tokoss/tokoss.png" id="tokoss_img{{ publication.id }}" alt="">'
            output += '<span id="tokoss{{ publication.id }}" class="ml-2" >'+publication.likes_number+'  Tokoss  </span>'
            output += '</div>'
            output += '</div></section>'
            if (publication.nomore == true){
                if (lang == 'fr'){
                    if (q_exist){
                        output += '<div class="col-8 offset-2 text-center container"><h6>Plus de nouvelles publications publiques pour cette recherche</h6></div>'
                    } else {
                        output += '<div class="col-8 offset-2 text-center container"><h6>Plus de nouvelles publications publiques</h6></div>'
                    }
                } else if (lang == 'en'){
                    if (q_exist){
                        output += '<div class="col-8 offset-2 text-center container"><h6>No more public publications for this recherche</h6></div>'
                    } else {
                        output += '<div class="col-8 offset-2 text-center container"><h6>No more public publications</h6></div>'
                    }
                }
            }
            $('.publications').append(output)
        },
        error:function(error){
            console.log(error)
        }
    })
}

})