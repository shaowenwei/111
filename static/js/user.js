    
$(function(){
  $('#new_submit').click(function(){
    var message=[];
    var username = $('#new_username_input').val();
    var password1 = $('#new_password1_input').val();
    var password2 = $('#new_password2_input').val();
    var firstname = $('#new_firstname_input').val();
    var lastname = $('#new_lastname_input').val();
    var email = $('#new_email_input').val(); 
    
   if (username=="" || password1=="" || password2=="" || firstname=="" || lastname=="" || email=="")
    {
      message.push("You did not provide the necessary fields");
    }
    else
    {
      if (firstname!="" && firstname.length>20)
      {
        message.push("Firstname must be no longer than 20 characters");
      }
      if (lastname.length>20)
      {
        message.push("Lastname must be no longer than 20 characters");
      }
      if (password1.length<8)
      {
        message.push("Passwords must be at least 8 characters long");
      }
      if (!(password1.search(/^[a-zA-Z]+$/) && password1.search(/^[0-9]+$/)))
      {
        message.push("Passwords must contain at least one letter and one number");
      }
      if (!password1.match(/^[a-zA-Z_0-9]+$/))
      {
        message.push("Passwords may only contain letters, digits, and underscores");
      }
      if (email.length>40)
      {
        message.push("Email must be no longer than 40 characters");
      }
      var pattern = /^([0-9A-Za-z\-_\.]+)@([0-9a-z]+\.[a-z]{2,3}(\.[a-z]{2})?)$/g;   
      flag = pattern.test(email);
      if (!flag)
      {
        message.push("Email address must be valid");
      }
    }
    error_message='';
    error_message = message.join("<br>");
    document.getElementById("errors").innerHTML=error_message;
    var data = {
      "username": username,
      "firstname": firstname,
      "lastname": lastname,
      "password1": password1,
      "password2": password2,
      "email": email 
    }
    if(message.length==0)
    {
      $.ajax({
        url: '/hd1qzdkp/p3/api/v1/user',
        data: JSON.stringify(data),
        contentType:"application/json; charset=UTF-8",
        type: 'POST',
        success: function(data){
            $(location).attr('href', 'login');
        },
        error: function(error,status){
          response=error.responseJSON.error.errors;
          var list=[];
          for(var x in response)
          {
            list.push(response[x].message);
          }
          response_text='';
          response_text = list.join("<br>");
          document.getElementById("errors").innerHTML = response_text;
        }
      });
    }
  });
});
