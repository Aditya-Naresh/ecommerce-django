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
// --------------------------------------------------------------------------

  // Product Variation
  $(".choose-size").hide();


  $(".choose-color").on('click', function(){
    $(".choose-color").removeClass('focused')
    $(this).addClass('focused')
    var _color = $(this).attr('data-color')
    $(".choose-size").removeClass('active')
    $(".choose-size").hide()

    $(".color-"+ _color).show()
    $(".color-"+ _color).first().addClass('active')
    var _price = $(".color-"+_color).first().attr('data-price')
    $(".product-price").text(_price)


  })


  var _color = $(".choose-color").first().attr('data-color')
  var _price = $(".choose-size").first().attr('data-price')
  $(".color-"+_color).show()
  $(".choose-color").first().addClass('focused')
  $(".color-"+ _color).first().addClass('active')
  $(".product-price").text(_price)

  

  $(".choose-size").on('click', function(){
    $(".choose-size").removeClass('active')
    $(this).addClass('active')
    var _price=$(this).attr('data-price')
    $(".product-price").text(_price)
  })

}) // Document Ready end
   
