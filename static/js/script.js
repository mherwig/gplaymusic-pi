$(document).ready(function() {

	$('#search-box').keyup(function() {
		$('.thumbnail').each(function(){
			if($(this).attr('name').toLowerCase().indexOf($('#search-box').val().toLowerCase()) == -1){
				$(this).parents('.col-xs-12.col-md-3').hide();
			}else{
				$(this).parents('.col-xs-12.col-md-3').show();
			}
		});
	});
  
	$('#nowplaying').collapse({
		toggle: false
	})
	
	function play(item, item_id) {
		$.ajax("/play/" + item + "/" + item_id).done(function(current) {
			update_controls(current.status);
			update_nowplaying(current);
		});
	}
	
	function update_nowplaying(track) {
		$('#nowplaying-text').html(track.artist + " - " + track.name);
	}

	function controls(method){
		$.ajax("/controls/" + method + "/").always(function() {
			if(method != "stop"){
				$("#" + method + "-button").toggleClass("active");
			}
		}).done(function(status) {
			update_controls(status);
		});
	}
	
	function update_controls(status) {
		if(status.random == "1") {
			$("#random-button").addClass('active');
		} else {
			$("#random-button").removeClass('active');
		}

		if(status.repeat == "1") {
			$("#repeat-button").addClass('active');
		} else {
			$("#repeat-button").removeClass('active');
		}
		
		if (status.state == "play") {
			$("#pause-button").removeClass('disabled');
			$("#pause-button").removeClass('active');
			$('#nowplaying').collapse('show');
		} else if(status.state == "pause") {
			$("#pause-button").addClass('active');
			$('#nowplaying').collapse('hide');
		} else if(status.state == "stop") {
			$("#pause-button").removeClass('active');
			$("#pause-button").addClass('disabled');
			$('#nowplaying').collapse('hide');
		}
	}
	
	$('a.play-artist').click(function(e){
		e.preventDefault();
		
		play("artist", $(this).attr('name'));
	});

	$('a.play-album').click(function(e){
		e.preventDefault();
		
		play("album", $(this).attr('name'));
	});
	
	$('a.play-track').click(function(e){
		e.preventDefault();
		
		play("track", $(this).attr('name'));
	});
	
	$('a.play-playlist').click(function(e){
		e.preventDefault();
		
		play("playlist", $(this).attr('name'));
	});

	$('#random-button').click(function(e){
		e.preventDefault();
		
		controls("random");
	});
	$('#stop-button').click(function(e){
		e.preventDefault();
		
		controls("stop");
	});
	$('#repeat-button').click(function(e){
		e.preventDefault();
		
		controls("repeat");
	});
	$('#pause-button').click(function(e){
		e.preventDefault();
		
		controls("pause");
	});

});
