$(document).ready(function(){
  var count = 0;

  setInterval(function(){
    count += 1;
  }, 5000);
  $(".left").on("click", function(){
    count += -1;
  });
  $(".right").on("click", function(){
    count += 1;
  });

  setInterval(function(){
    if (count % 3 == 0){
      //1番目
      $(".top0").css("display", "block");
      $(".top1").css("display", "none");
      $(".top2").css("display", "none");
      $(".point1").css("background-color", "white");
      $(".point2").css("background-color", "transparent");
      $(".point3").css("background-color", "transparent");
    } else if (count % 3 == 1) {
      //2番目
      $(".top0").css("display", "none");
      $(".top1").css("display", "block");
      $(".top2").css("display", "none");
      $(".point1").css("background-color", "transparent");
      $(".point2").css("background-color", "white");
      $(".point3").css("background-color", "transparent");
    } else {
      //3番目
      $(".top0").css("display", "none");
      $(".top1").css("display", "none");
      $(".top2").css("display", "block");
      $(".point1").css("background-color", "transparent");
      $(".point2").css("background-color", "transparent");
      $(".point3").css("background-color", "white");
    }
  }, 1);
});
