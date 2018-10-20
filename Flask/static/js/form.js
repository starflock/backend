$(document).ready(function() {
	alert('here');
	$('form').on('submit', function(event) {
		alert('submitted');
		$.ajax({
			data : {
				name : $('#name1').val(),
				email : $('#email1').val()
			}
			type : 'POST',
			url : '/register'
		})
		.done(function(data) {
		// if(data.error) {
		// 	alert('Errors');
		// } else {
		// 	alert('No Errors');
		// }
		});
		event.preventDefault();
	});

});