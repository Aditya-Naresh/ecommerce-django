$(document).ready(function () {

  $('.p_img').ezPlus()
    $('.p_img').addClass('hidden')
    $('.p_img').first().removeClass('hidden').addClass('focused')
    $(".thumbnail").on('click', function(e){
    e.preventDefault()
    var _img = $(this).data('image')
    $(".p_img").addClass('hidden')
    $("#image-" + _img).removeClass('hidden').addClass('focused')
})


      $(".form-control").on('change', function(e){
        e.preventDefault()
        var _colorId = 
        console.log(_colorId);
      })
     
    })
   
