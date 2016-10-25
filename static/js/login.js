$(function(){
  $('#login_submit').click(function(){
    var username = $('#login_username_input').val();
    var password = $('#login_password_input').val();
    var data={
      "username":username,
      "password":password

    }
    $.ajax({
      url: '/hd1qzdkp/p3/api/v1/login',
      data: JSON.stringify(data),
      contentType:"application/json; charset=UTF-8",
      type: 'POST',
      success: function(response){
        //res = JSON.parse(response);
        var reg=new RegExp("(^|&)"+'url'+"=([^&]*)(&|$)");
        var r=window.location.search.substr(1).match(reg);
        console.log(r);
        if (r!=null)
          {
            var newurl=unescape(r[2]);
          console.log(newurl);
          console.log('/hd1qzdkp/p3'+newurl);
          $(location).attr('href','/hd1qzdkp/p3'+newurl);
        }
        else{
          $(location).attr('href','albums');
        }
        
      },
      error: function(error){
        res = JSON.parse(error.response);
        $("#errors").text(res['error'].errors[0].message);

      console.log(error);
      }
    });
  });
});
