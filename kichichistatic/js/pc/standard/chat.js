$('.chatbox').hide()

$(document).ready(function(){



$('#resize-chat').click(function(){
    $('.chatbox').toggleClass('hide')
    if ($('.chatbox').hasClass('hide')){
        $('.chatbox').hide()
        $(this).text('+')
    } else {
        $('.chatbox').show()
        $(this).text('-')
        $('#chat-unread').remove()
    }
    $('#chatlogs').scrollTop($('#chatlogs')[0].scrollHeight);
})




$('.chat-form form').submit(function(e){
    e.preventDefault()

    var myprofil = $('#profiler').attr('name');
    var message = $('#chat-write').val()
    var chat = ''
    chat += '<div class="chat self mb-4">'
    chat += '<div class="user-photo"><img src="'+ myprofil +'" alt=""></div>'
    chat += '<p class="chat-message">'+message+'</p>'
    chat += '</div>'

    $('.chatlogs').append(chat)

    $('#chatlogs').scrollTop($('#chatlogs')[0].scrollHeight);

     $.ajax({
        method:'POST',
        async: true,
        url: '/dreamteam/chat/',
        data:$(this).serialize(),
        success: function (data){
            if (data.success){
                $('#chat-write').val('')
            }

        },
        error: function (json){
           
        },
    })

})


setInterval(function(){
    $.ajax({
        method:'GET',
        async: true,
        url: '/dreamteam/checkchat/',
        success: function (data){
            if (data.success){
                            
                var chat = ''
                chat += '<div class="chat friend mb-4">'
                chat += '<div class="user-photo"><img src="'+ data.url +'" alt=""></div>'
                chat += '<p class="chat-message">'+data.message+'</p>'
                chat += '</div>'

                $('.chatlogs').append(chat)

                $('#chatlogs').scrollTop($('#chatlogs')[0].scrollHeight);

                if ($('.chatbox').hasClass('hide')){
                    if (lang == 'fr'){
                        $('<span id="chat-unread" class="ml-2">Nouveau message</span>').insertBefore('.onliner')
                    } else if (lang == 'en'){
                        $('<span id="chat-unread" class="ml-2">New message</span>').insertBefore('.onliner')
                    }
                    
                }
            }

        },
        error: function (json){
            
        },
    })

}, 1000)














})
