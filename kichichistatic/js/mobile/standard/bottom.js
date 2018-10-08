$(document).ready(function(){

var label1 = $('#label1');
var label2 = $('#label2');
var label3 = $('#label3');
var label4 = $('#label4');



$('body').on('click', '.fixed-bottom label', function(){
    $('.active').removeClass('active')
    $(this).toggleClass('active')

    var num = $(this).attr("id")
    divdisplaying(num)
})

function divdisplaying(args){
    $('#home-section').css('display','none')
    $('#notif-section').css('display','none')
    $('#chat-section').css('display','none')
    $('#profil-section').css('display','none')
    $('#label3').css('background-color', 'unset')
    // $('.chat-header').removeClass('fixed-top')
    $('.navbar').show()
    if (args == 'label1'){
        $('#home-section').css('display','initial')
        $('#home-section').scrollTop($('#home-section')[0].scrollHeight);
    }
    if (args == "label2"){
        $('#notif-section').css('display','initial')
    }if (args == "label3"){
        $('#chat-section').css('display','initial')
        $('#label3').css('background-color', 'gainsboro')
        // $('.chat-header').addClass('fixed-top')
        $('body').scrollTop($('body')[0].scrollHeight);
        $('.navbar').hide()
    }if (args == 'label4'){
        $('#profil-section').css('display','initial')
    }
}


$('#label1').click(function(){
    
})


$('#label2').click(function(){
    
})

$('#label3').click(function(){
    
})

$('#label4').click(function(){
    
})





































})