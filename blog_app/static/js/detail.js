$("#like").hide();

function Comment(csrf){
  let desc = $("#description").val();
  let post = $("#post_id").val();
  let reply = $("#comment_id").val();
  let commentData = {"post":post,"description":desc, "csrfmiddlewaretoken":csrf}
  if (reply){
    commentData["comment"] = reply
  }

  if (reply){
        $.ajax({
      url : "/blog/add-reply/",
      method : "POST",
      data : commentData,
      success : function(resp){
        data = resp["reply"]
        
          $(document.getElementById(`${data["comment"]}`)).append(`
          
	  	<div class="comment-area-box media mt-5">
					<img alt="" src="/static/images/comment.jpeg" class="mt-2 img-fluid float-left mr-3" width="80">
			<div class="media-body ml-4">
				
				<h4 class="mb-0 ">${data["user"]}</h4>
				<span class="date-comm font-sm text-capitalize text-color"><i class="ti-time mr-2"></i>${data["created_at"]}</span>

				<div class="comment-content mt-3">${data["description"]}</p>
				</div>
	
			</div>
		</div>
		
		
		
          `)
        }
    });
    
  } else{
    $.ajax({
      url : "/blog/add-comment/",
      method : "POST",
      data : commentData,
      success : function(resp){
        console.log(resp)
        data = resp["com"]
        
        $("#more_comment").append(`
		<div class="comment-area-box media mt-5">
			<img alt="" src="/static/images/man.png" width="80" class="mt-2 img-fluid float-left mr-3">

			<div class="media-body ml-4">
				
				<h4 class="mb-0 ">${data["user"]}</h4>
				<span class="date-comm font-sm text-capitalize text-color"><i class="ti-time mr-2"></i>${data["created_at"]}</span>

				<div class="comment-content mt-3">${data["description"]}</p>
				</div>
				<div class="comment-meta mt-4 mt-lg-0 mt-md-0">
					<a onclick="commentForm('comment_submit','${data['comment_id']}');" class="text-underline">Reply</a>
				</div>
			</div>
		</div>
		
			<div class="container ml-2" id="reply${data["comment_id"]}">
		
		`)
        
        
      }
    });
  }
}

