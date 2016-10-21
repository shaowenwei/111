    
$(function(){
  $('button').click(function(){
    var user = $('#new_username_input').val();
    var pass = $('#new_password1_input').val();
    $.ajax({
      url: '/hd1qzdkp/p3/api/v1/user',
      data: $('form').serialize(),
      type: 'POST',
      success: function(data,status){
        obj=[];
        data1=JSON.parse(data);
        response=data1.ret_data.error;
        response_text='';
        if (response){
          response_text = response.join("<br>");
        }
        document.getElementById("errors").innerHTML = response_text;
        if (!response){
          $(location).attr('href', 'login');
        }
      },
      error: function(error){
        console.log(error);
      }
    });
  });
});
