
$(document).ready(function(){

    $("#file").change(function(e){
        var file = $(this)[0].files;
        var input = document.getElementById('file')
        var filename = e.target.value.split("\\").pop();
        $('.upload_span').text(filename);
        var ext = filename.substring(filename.lastIndexOf('.')+1).toLowerCase();


        $('.text-red').text('')
        if (ext == 'mp4'){
            if (file[0].size/1050030 >  5){
                $('.text-red').text('The maximum size for mp4 is 5 Mb')
                input.value = "";
            }
        } else if (ext == '3gp') {
            if (file[0].size/1050030 >  3){
                $('.text-red').text('The maximum size for 3gp is 3 Mb')
                input.value = "";
            }
        } else if ( ext == 'mp3' ){
            if (file[0].size/1050030 >  3){
                $('.text-red').text('The maximum size for mp3 is 3 Mb')
                input.value = "";
            }
        }   else if (ext == 'aac') {
            if (file[0].size/1050030 >  3){
                $('.text-red').text('The maximum size for aac is 3 Mb')
                input.value = "";
            }
        }   else if (ext == 'jpg'){
            if (file[0].size/1050030 >  1){
                $('.text-red').text('The maximum size for pictures is 1 Mb')
                input.value = "";
            }
        } else if (ext == 'jpeg'){
            if (file[0].size/1050030 >  1){
                $('.text-red').text('The maximum size for pictures is 1 Mb')
                input.value = "";
            }
        } else if (ext == 'png'){
            if (file[0].size/1050030 >  1){
                $('.text-red').text('The maximum size for pictures is 1 Mb')
                input.value = "";
            }
        } else if (ext == 'gif'){
            if (file[0].size/1050030 >  1){
                $('.text-red').text('The maximum size for gifs is 1 Mb')
                input.value = "";
            }
        } else {
            $('.text-red').text('This type of file is not supported')
            input.value = "";
        }


    });

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
            $('.upload_span_profil').text('The profile must be a picture');
        }


    })


    $("#edit_profil").click(function(){
        $('#profil_form').css('display', 'initial')
        $(this).hide()
    })
    $('#edit_cancel').click(function(e){
        e.preventDefault();
        $('#profil_form').css('display', 'none');
        $("#edit_profil").show();
    })
    $('.classement button').click(function(){
        var user = $(this).attr('user')
        if($(this).attr('k') == 'dreamteam'){

            $('#'+user).attr('class', 'dreamteam')
        }else if($(this).attr('k') == 'family'){
            $('#'+user).attr('class', 'family')
        } else if($(this).attr('k') == 'friends'){
            $('#'+user).attr('class', 'friends')
        }
    })

    $('.classement form').submit(function(e){
        e.preventDefault();
        var user = e.target.id
        var username = document.getElementById('profil_username').innerText
        var token = $('input [name=csrfmiddlewaretoken]').val()

        if ($(this).hasClass('dreamteam')){
            $.ajax({
            method: "POST",
            async: true,
            url: '/user/'+username+'/dreamteam/',
            data:$(this).serialize(),
            success: function (data){
            $('#dreamteam_'+user).text("Demande envoyée")
            },
            error: function (json){
                console.log(json)
            },
        })
        } else if ($(this).hasClass('family')){
            $.ajax({
            method: "POST",
            async: true,
            url: '/user/'+username+'/family/',
            data:$(this).serialize(),
            success: function (data){
                $('#family_'+user).text("Rétirer de la famille")
            },
            error: function (json){
                console.log(json)
            },
        })
        } else if ($(this).hasClass('friends')){
            $.ajax({
            method: "POST",
            async: true,
            url: '/user/'+username+'/friends/',
            data:$(this).serialize(),
            success: function (data){
                $('#friends_'+user).text("Rétirer des amis")
            },
            error: function (json){
                console.log(json)
            },
        })
        }

    })




})

