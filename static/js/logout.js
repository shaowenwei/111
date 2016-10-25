$(function(){
  $('#nav_logout').click(function(){
    $.ajax({
      url: '/hd1qzdkp/p3/api/v1/logout',
      type: 'POST',
      data: {},
      success: function(response){
      console.log(response);
     $(location).attr('href','');
      
      },
      error: function(error){
      console.log(error);
      }
    });
  });
});
