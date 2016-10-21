
function completion(username,password1){
	alert("success");
	$.post(
		"/api/v1/user",
		{ username: $('#username').val()
		password1: $('#password1').val() },
		function(data,status){
			alert('success');
		}
	);
}


/*$("#form1").submit(function(event) {
	event.preventDefault();
	var $form = $( this ), url = $form.attr( 'action' );
	var posting = $.post(
		url, 
		{ username: $('#username').val() 
		  password1: $('#password1').val()
	    }, 
		function( data,status ) {
			alert('success');
		}
	);
	}
);*/