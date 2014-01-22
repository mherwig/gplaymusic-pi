$(document).ready(function() {

  $('#search-box').keyup(function() {
    $('.thumbnail').each(function(){
        if($(this).attr('name').toLowerCase().indexOf($('#search-box').val().toLowerCase()) == -1){
            $(this).hide();
        }else{
            $(this).show();
        }
    });
  });

  function ajax(toggle){
    $.ajax("/ajax/"+toggle+"/",{ type: "GET" }).always(function (response) {
      results = JSON.parse(response['responseText']);
      if(toggle != "stop"){
        $("#"+toggle+"-button").toggleClass('btn-highlight');
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
      ajax("stop");
  });
  $('#repeat-button').click(function(e){
      e.preventDefault();
      ajax("repeat");
  });

});
