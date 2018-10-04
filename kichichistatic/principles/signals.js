setInterval(function(){
    $.ajax({
        method: "GET",
        async: true,
        url: '/accounts/online/',
        success: function (data){
           if (data.online){
               if (langue == 'fr'){
                    $('.onliner').text('En ligne...')
               } else if (langue == 'en'){
                    $('.onliner').text('Online...')
               }
                
           } else {
               if (langue == 'fr'){
                    $('.onliner').text('Hors ligne...')
               } else if (langue == 'en'){
                    $('.onliner').text('Offline...')
               }
                
           }
        },
        error: function (json){
            console.log(json)
        },
    })
}, 10000)

