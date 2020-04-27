//Funkcnost ak uz je stranka bezpecne nacitana
$(document).ready(function() {
	namespace = '/test';
	var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);


	//checking function
	function isOneChecked() {
	var forward = document.getElementById("forward").checked;
	var backward = document.getElementById("backward").checked;
	var distance = document.getElementById("distance").value;

	if(distance == ""){
		return false
	}

	if(forward && !backward){
		return true;
	}

	if(backward && !forward){
		return true;
	}

  return false;
}
	///////////////////

	//pause function so user cant interact
	function Pause() {
		document.getElementById("button_a").disabled = true;
		document.getElementById("button_b").disabled = true;
		document.getElementById("button_c").disabled = true;
		document.getElementById("button_position").disabled = true;
		document.getElementById("button_distance").disabled = true;
  	return;
	}
//////////////////

//unpause function so user can interact
	function Unpause() {
		document.getElementById("button_a").disabled = false;
		document.getElementById("button_b").disabled = false;
		document.getElementById("button_c").disabled = false;
		document.getElementById("button_position").disabled = false;
		document.getElementById("button_distance").disabled = false;
  	return;
	}
	/////////////////

	//function to get form distance data
	function GetDistanceDirection(){
		if(document.getElementById('forward').checked){
			console.log(document.getElementById('forward').checked);
			console.log("Forward");
			return "F";
		}
		if(document.getElementById('backward').checked){
			console.log(document.getElementById('backward').checked);
			console.log("Backward");
			return "B";
		}
	}

	function GetDistanceData(){
		console.log(document.getElementById("distance").value)
		return document.getElementById("distance").value;
	}
	///////////////////////////

	//function to get robot position data
	function GetPositionData(){
		var robot_settings = [];
		robot_settings.push(document.getElementById("height").value);
		robot_settings.push(document.getElementById("stretch").value);
		robot_settings.push(document.getElementById("rotate").value);
		//console.log(robot_settings[0]);
		return robot_settings
	}
	/////////////////////////////////////

	//check robot position data
	function CheckPositionData(position_data){
		var i;
		for (i = 0; i < position_data.length; i++) {
  		if(position_data[i].length < 1){
				console.log("Check BAD");
				return false;
				}
			}
		console.log("Check ok");
		return true;
	}
	///////////////////////////

	//unpausing, calling from python
	socket.on('unpause', function() {
		Unpause();
		console.log("unpausing");
	});
///////////////////////////////////

//buttons click function experiment A
	$('#button_a').click(function(event) {
		console.log("Button A");
		socket.emit('a_place', {value: $(this).val()});
		Pause();
		console.log("pausing");
		return false;
	});

	//button experiment B
	$('#button_b').click(function(event) {
		console.log("Button B");
		socket.emit('b_place', {value: $(this).val()});
		Pause();
		console.log("pausing");
		return false;
	});

	//button experiment C
	$('#button_c').click(function(event) {
		console.log("Button C");
		socket.emit('c_place', {value: $(this).val()});
		Pause();
		console.log("pausing");
		return false;
	});

	//button distance for Arduino
	$('#button_distance').click(function(event) {
		console.log("Button Distance");

		if(isOneChecked()){
			socket.emit('distance', GetDistanceDirection(),GetDistanceData());
			console.log("pause")
			Pause();
			console.log("pausing");
			return false;
		}
		else{
			alert("Error you didnt choose direction or distance!");
		}
	});

	//button position for uArm SwiftPro
	$('#button_position').click(function(event) {
		console.log("Button Pozition");
		var position_data = GetPositionData();

		if(CheckPositionData(position_data)){
			socket.emit('position', position_data);
			Pause();
			console.log("pausing");
		return false;
		}
		else{
			alert("Error you didnt enter correct robot position!")
		}
	});
///////////////////////////

});
