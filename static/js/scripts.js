$(function(){
	$('#btnUpdate').click(function(){
        console.log("hello")
		
		$.ajax({
			url: '/editbook',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
                $('#editalert').show()
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});

