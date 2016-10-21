$(function(){
  $('#login_submit').click(function(){
    var username = $('#login_username_input').val();
    var password = $('#login_password_input').val();
    $.ajax({
      url: '/hd1qzdkp/p3/api/v1/login',
      data: $('form').serialize(),
      type: 'POST',
      success: function(response){
        res = JSON.parse(response);
      
      if(res['error'].username)
      {
        $(location).attr('href','albums');
      }
      /*else
      {$("#errors").text(res['error'].errors[0].message);}*/
      
      },
      error: function(error){
      res=JSON.parse(error.response);
        $("#errors").text(res['error'].errors[0].message);
        console.log(error);
      }
    });
  });
});
