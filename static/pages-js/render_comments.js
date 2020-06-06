var autoExpand = function (field) {

  // Reset field height
  field.style.height = 'inherit';

  // Get the computed styles for the element
  var computed = window.getComputedStyle(field);

  // Calculate the height
  var height = parseInt(computed.getPropertyValue('border-top-width'), 10)
    + parseInt(computed.getPropertyValue('padding-top'), 10)
    + field.scrollHeight
    + parseInt(computed.getPropertyValue('padding-bottom'), 10)
    + parseInt(computed.getPropertyValue('border-bottom-width'), 10);

  field.style.height = height + 'px';

};

document.addEventListener('input', function (event) {
  if (event.target.tagName.toLowerCase() !== 'textarea') return;
  autoExpand(event.target);
}, false);

function post_comment() {
  comment_field = document.getElementById('comments');
  comments = comment_field.value;
  $.ajax({
    url: '/ajax/submit_comment/',
    dataType: 'json',
    data: {
      user_id: user_id,
      post_id: post_id,
      comment: comments,
    },
    success: function (data) {
      comment_field.value = "";
      comment_validation();

      $('#comments-display-area').load(document.URL + ' #comments-display-area');
    }
  });
}

function comment_validation() {
  var comment_value = document.getElementById("comments").value;
  if (comment_value.length < 1) {
    document.getElementById("comment-btn").disabled = true;
  }
  else {
    document.getElementById("comment-btn").disabled = false;;
  }
}


function show_trackers() {
  var tracker_div = document.getElementById('trackers');
  if (tracker_div.style.display == 'block') {
    tracker_div.style = "display:none";
    var show_tracker_btn = document.getElementById('show-tracker-btn');
    show_tracker_btn.innerHTML = "Show Trackers";
  } else {
    tracker_div.style = "display:block";
    var show_tracker_btn = document.getElementById('show-tracker-btn');
    show_tracker_btn.innerHTML = "Hide Trackers";
  }
}

