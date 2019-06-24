$(document).ready(function(){
  hsize = $(window).height();
  menuheight = $(".bar-container").height();
  $(".dark").css("height", hsize - menuheight + "px");
  $(".main1").css("height", hsize - menuheight + "px");
  $(".main-container").css("padding-top", + "px");
});

$(window).resize(function(){
  hsize = $(window).height();
  menuheight = $(".bar-container").height();
  $(".dark").css("height", hsize - menuheight + "px");
  $(".main1").css("height", hsize - menuheight + "px");
  $(".main-container").css("padding-top", + "px");
});
