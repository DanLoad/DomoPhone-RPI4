$(document).ready(function(){
  var mql1 = window.matchMedia('all and (max-width: 575px)');
	var mql2 = window.matchMedia('all and (min-width: 576px)');

  if (mql1.matches) {
		$("#link_id").show();
		$("#list_name").hide();
	} else if (mql2.matches) {
		$("#list_name").show();
		$("#link_id").hide();
	}

  window.onresize = function(event) {
    var mql1 = window.matchMedia('all and (max-width: 575px)');
  	var mql2 = window.matchMedia('all and (min-width: 576px)');

    if (mql1.matches) {
      $("#link_id").show();
      $("#list_name").hide();
    } else if (mql2.matches) {
      $("#list_name").show();
      $("#link_id").hide();
      $("#nav_user").css({"position": "relative"});
      $("#nav_user").css({"background": ""});
    }
  };


  $('#link_id').click(function(){
    var wrapper = $('#navigation');
    var nsc = $(document).scrollTop();
    var bp1 = wrapper.offset().top;
 	  var display = $("#list_name").css("display");

 	  if (display == 'none') {

     	$("#list_name").show();
     	$("#nav_user").css({"position": "fixed"});
      $("#nav_user").css({"width": "100%"});
      $("#nav_user").css({"z-index": "999"});
     	$("#nav_user").css({"top": "0"});
     	$("#nav_user").css({"background": "rgba(0,105,105,1)"});

   	} else {

   		$("#list_name").hide();
   		if (nsc<bp1) {
   		$("#nav_user").css({"background": ""});
   		}
   	if (nsc<bp1) {
   		$("#nav_user").css({"position": "relative"});
   			}
   	}
  });


  $(window).scroll(function(){
    var mql1 = window.matchMedia('all and (max-width: 575px)');
  	var mql2 = window.matchMedia('all and (min-width: 576px)');
    var navbar =  $('#nav_user');

		if(mql1.matches) {
      var wrapper = $('#navigation');
			var nsc = $(document).scrollTop();
			var bp1 = wrapper.offset().top;
			var bp2 = bp1 + wrapper.outerHeight()-$(window).height();
			var show = $("#list_name").css("display");

			if (nsc>bp1) {
				navbar.css('position','fixed');
				$("#nav_user").css({"background": "rgba(0,105,105,1)"});
			}
			else {
				if(show == 'none') {
					navbar.css('position','relative');
					$("#nav_user").css({"background": ""});
				}
			}
			if (nsc>bp2) {

			}
			else {
				navbar.css('top', '0');
			}
		}
	});
});
