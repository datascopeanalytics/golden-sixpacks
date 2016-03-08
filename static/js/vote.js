// Only enable the vote button if a radio button is checked
$(function(){
    $("input[type='radio']").change(function(){

	$("input[type='submit']").prop("disabled", false);
    });
});
