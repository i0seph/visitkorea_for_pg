/*
 * Copyright(c) 2019. KTDS Opensource Business Team. All rights reserved.
 * Author: Ioseph
 * 이 저작물은 크리에이티브 커먼즈 저작자표시-비영리 4.0 국제 라이선스에 따라 이용할 수 있습니다.
 */

function click_navi(){
	var locaval = "";
	var cateval = "";
	var check_subloca = 0;
	$("#sublocanavi input:checkbox").each(function() {
		check_subloca += 1;
	       if($(this).is(":checked")){
		       if(locaval != "") locaval += ",";
		       locaval += $(this).val(); 
	       }
	});
	if(check_subloca == 0) locaval = "undefind";
	$("#catenavi input:checkbox").each(function() {
	       if($(this).is(":checked")){
		       if(cateval != "") cateval += ",";
		       cateval += $(this).val(); 
	       }
	});
	locaval = (locaval == "") ? "all" : locaval;
	cateval = (cateval == "") ? "all" : cateval;

	$.ajax({
		url:'/ajax/list/' + locaval + "/" + cateval,
		success:function(data){
			if(locaval == "all" && cateval == "all"){
				$("#map").show();
				$("#festalist").show();
				$("#placelist").empty();
				display_festalist();
			}
			else {
				$("#map").hide();
				$("#placelist").empty();
				$("#festalist").hide();
				$.each(data, function(num, row){
					if(! row.imgurl) imgurl = "http://api.visitkorea.or.kr/static/images/common/noImage.gif";
					else imgurl = row.imgurl;
					$("#placelist").append("<li onclick='self.location.href=\"/place/" + row.place_id + "\"'>" + row.place_name + "<br />" + "<img src=" + imgurl + " height='128' />"+ "</li>");
				});
			}
		}
	});
}

function display_location(){
	$.ajax({
		url:'/ajax/location/',
		success:function(data){
			$.each(data, function(num, row){
				$("#locanavi").append("<li><input type='radio' name='toploca' value='" + row.addrid + "' />" + row.addrname + "</li>");
			});
			$("#locanavi").append("<li><input type='radio' name='toploca' value='undefind' />미지정</li>");

			$("#locanavi input:radio").change(function(obj){ display_subnavi(this.value); });

		}
	});
}


function display_subnavi(toploca){
	if(toploca != "undefind"){
	$.ajax({
		url:'/ajax/location/' + toploca,
		success:function(data){
			$("#sublocanavi").empty();
			$.each(data, function(num, row){
				$("#sublocanavi").append("<li><input type='checkbox' name='subloca' value='" + row.addrid + "' />" + row.addrname + "</li>");
			});

			$("#sublocanavi input:checkbox").change(function(obj){ click_navi() });

		}

	});
	}
	else {
			$("#sublocanavi").empty();
			click_navi();
	}
}

function display_category(){
	$.ajax({
		url:'/ajax/category/',
		success:function(data){
			$.each(data, function(num, row){
				$("#catenavi").append("<li><input type='checkbox' value='" + row.tourid + "' />" + row.tourname + "</li>");
			});
			$("#catenavi input:checkbox").change(function(obj){ click_navi(); });

		}
	});
}

function display_randomlist(){
	$.ajax({
		url:'/ajax/random10/',
		success:function(data){
			$("#placelist").empty();
			$.each(data, function(num, row){
/*
				if(! row.imgurl) imgurl = "http://api.visitkorea.or.kr/static/images/common/noImage.gif";
				else imgurl = row.imgurl;
				$("#placelist").append("<li onclick='self.location.href=\"/place/" + row.place_id + "\"'>" + row.place_name + "<br />" + "<img src=" + imgurl + " height='128' />"+ "</li>");
*/

var markerPosition  = new daum.maps.LatLng(row.lat, row.long);
var infowindow = new kakao.maps.InfoWindow({
    map: map,
    position : markerPosition, 
    content : "<div onclick='self.location.href=\"/place/" + row.place_id + "\"' style='cursor: pointer'>" + row.place_name + "</div>",
    removable : false
});
			});

		}
	});
}

function display_festalist(){
	$.ajax({
		url:'/ajax/gettodayfesta/',
		success:function(data){
			$("#festalist").show();
			$("#festalist ul").empty();
			$.each(data, function(num, row){
				$("#festalist ul").append("<li onclick='self.location.href=\"/place/" + row.place_id + "\"'>" + row.place_name + "</li>");
			});

		}
	});
}

function startpage(){
	display_location();
	display_category();
	display_randomlist();
	display_festalist();
	$("#input_search").keypress(function(e) {
		if (e.keyCode == 13){
			$.ajax({
				url:'/ajax/namesearch/' + $("#input_search").val(),
				success:function(data){
					$("#map").hide();
					$("#festalist").hide();
					$("#placelist").empty();
					$.each(data, function(num, row){
						if(! row.imgurl) imgurl = "http://api.visitkorea.or.kr/static/images/common/noImage.gif";
						else imgurl = row.imgurl;
						$("#placelist").append("<li onclick='self.location.href=\"/place/" + row.place_id + "\"'>" + row.place_name + "<br />" + "<img src=" + imgurl + " height='128' />"+ "</li>");


					});
				}
			});
		}    
	});
}

function startplace(place_id, x, y){
	$.ajax({
		url:'/ajax/getnames/' +  $("#placelocation").text() + '/' + $("#placecategory").text(),
		success:function(data){
			$("#placelocation").text(data.locaname);
			$("#placecategory").text(data.catename);
		}
	});
	$.ajax({
		url:'/ajax/getattrib/' +  place_id,
		success:function(data){
			$.each(data, function(num, row){
				$("#placedl").append("<dt>" + row.attname + "</dt>");
				$("#placedl").append("<dd>" + row.v + "</dd>");
			});
		}

	});


	$.ajax({
		url:'/ajax/getimages/' +  place_id,
		success:function(data){
			$.each(data, function(num, row){
				$("#place_images").append("<div><img src='" + row.imgurl + "' height='400' /></div>");
			});

			$('#place_images').bbslider({
				controls:   true,
				transition: 'slide',
				duration:   500,
			});
		}
	});

	$.ajax({
		url:'/ajax/near/' + place_id + '/' +  x + '/' + y,
		success:function(data){
			$.each(data, function(num, row){
				if(! row.imgurl) imgurl = "http://api.visitkorea.or.kr/static/images/common/noImage.gif";
				else imgurl = row.imgurl;
				$("#nearlist").append("<div onclick='self.location.href=\"/place/" + row.place_id + "\"'>[" + row.tourname + '] ' + row.place_name + "(" + row.distance + "km)<br />" + "<img src=" + imgurl + " height='128' />"+ "</div>");

			});
		}
	});
}
