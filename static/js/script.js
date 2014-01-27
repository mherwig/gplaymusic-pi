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
  
  function ajax(toggle){
    $.ajax("/ajax/"+toggle+"/",{ type: "GET" }).always(function (response) {
      results = JSON.parse(response['responseText']);
      if(toggle != "stop"){
        $("#"+toggle+"-button").toggleClass("active");
      }
    });
    return false;
  }

  $('#random-button').click(function(e){
      e.preventDefault();
      ajax("random");
  });
  $('#stop-button').click(function(e){
      e.preventDefault();
      $('#nowplaying').collapse('hide');
      $('#pause-button').addClass('disabled');
      ajax("stop");
  });
  $('#repeat-button').click(function(e){
      e.preventDefault();
      ajax("repeat");
  });
  $('#pause-button').click(function(e){
	  e.preventDefault();
	  $('#nowplaying').collapse('toggle');
      ajax("pause");
  });

});
