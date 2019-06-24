$(document).ready(function(){
  var button = 0;
  sp = $(window).width();
  if (sp < 767){
    $(".bar2").on("click", function(){
      button += 1;
    });
  }
  setInterval(function(){
    if (button % 2 == 0){
      $(".button-hide").css("display", "none");
    } else {
      $(".button-hide").css("display", "block");
    }
  }, 1);
});
