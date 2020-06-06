$(document).ready(function () {
    $("#like-list-btn").click(function () {
        var list_of_likes = document.getElementById("likes-list");
        var list_of_dislikes = document.getElementById("dislikes-list");
        list_of_likes.innerHTML = "";
        list_of_dislikes.innerHTML = "";
        $.ajax({
            url: '/ajax/get_like_list/',
            dataType: 'json',
            data: {
              user_id: user_id,
             post_id : post_id,
            },
             
            success: function (data) {
                document.getElementById("liked-by").style = "display:block;";
                document.getElementById("disliked-by").style = "display:block;";
                for (var i in data.dislike_list) {
                    var node = document.createElement("LI");
                    node.style = "font-size:13px;";
                    var name = document.createTextNode(data.dislike_list[i]);
                    node.appendChild(name);
                    list_of_dislikes.appendChild(node);
                }
                for (var i = 0; i < data.like_list.length; i++) {
                    var node = document.createElement("LI");
                    node.style = "font-size:13px;";
                    var name = document.createTextNode(data.like_list[i]);
                    node.appendChild(name);
                    list_of_likes.appendChild(node);
                }
            }
        });
    });
});