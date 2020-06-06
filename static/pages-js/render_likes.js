$(document).ready(function () {
    $("#likeBtn").click(function () {
      $.ajax({
        url: '/ajax/validate_like/',
        dataType: 'json',
        data: {
          user_id: user_id ,
      post_id : post_id,
        },

    success: function (data) {
      $("#showLikes").text(data.updated_like)
      $("#showUnLikes").text(data.updated_unlikes)

      if (data.is_liked) {
        document.getElementById("thumb_up").style = "color:#0076F3 ;";
        document.getElementById("thumb_down").style = "color:white;";
      }
      else {
        document.getElementById("thumb_up").style = "color:white;";

      }
    }
      });
    });
});