	var data_global = 0;
	var donut_chart = 0;
	var create_db_form_flag = 0;
	let flag_of_percentage = 0;
	$.fn.jQuerySimpleCounter = function( options ) {
	    var settings = $.extend({
	        start:  0,
	        end:    100,
	        easing: 'swing',
	        duration: 400,
	        complete: ''
	    }, options );

	    var thisElement = $(this);

	    $({count: settings.start}).animate({count: settings.end}, {
			duration: settings.duration,
			easing: settings.easing,
			step: function() {
				var mathCount = Math.ceil(this.count);
				thisElement.text(mathCount);
			},
			complete: settings.complete
		});
	};


$('#number1').jQuerySimpleCounter({end: 12,duration: 3000});
$('#number2').jQuerySimpleCounter({end: 55,duration: 3000});
$('#number3').jQuerySimpleCounter({end: 359,duration: 2000});
$('#number4').jQuerySimpleCounter({end: 246,duration: 2500});



  	/* AUTHOR LINK */
     $('.about-me-img').hover(function(){
            $('.authorWindowWrapper').stop().fadeIn('fast').find('p').addClass('trans');
        }, function(){
            $('.authorWindowWrapper').stop().fadeOut('fast').find('p').removeClass('trans');
        });

			function myFunction() {

					var br = document.createElement("br");
					var input = document.getElementById('inputGroupFile01');
					readXlsxFile(input.files[0]).then(function(data) {

					 if(create_db_form_flag == 0){
					 var form = document.createElement("form");
					 form.setAttribute("method", "post");
					 form.setAttribute("action", "php/save.php");
					 // form.setAttribute("class", "was-validated");
					 form.setAttribute("id", "db_form");
					 form.setAttribute("onsubmit", " return submit_form()");

					 // form.addEventListener('change', form_validation);
					 // form.addEventListener('onsubmit', form_validation);



					 // Create an label for game name
					 var label_game_name = document.createElement("label");
					 label_game_name.style.fontSize = "x-large";
					 var text_for_game_name_label = document.createTextNode("Game name:");
					 label_game_name.appendChild(text_for_game_name_label);

					 // Create an input for game name
					 var game_name = document.createElement("input");
					 game_name.setAttribute("type", "text");
					 game_name.setAttribute("name", "GameName");
					 game_name.setAttribute("class", "form-control");
					 game_name.setAttribute("id", "game_name");
					 // game_name.setAttribute("onchange" , "form_validate(this.value)");
					 game_name.value= data[1][0];

					 // Create an label for teamA name
					 var label_teamA_name = document.createElement("label");
					 label_teamA_name.style.fontSize = "x-large";
					 var text_for_teamA_name_label = document.createTextNode("Team A:");
					 label_teamA_name.appendChild(text_for_teamA_name_label);

					 // Create an input for teamA name
						var team_A = document.createElement("input");
						team_A.setAttribute("type", "text");
						team_A.setAttribute("name", "TeamA");
						team_A.setAttribute("id", "team_a");
						team_A.setAttribute("class", "form-control");
						team_A.value= data[1][1];


					 // Create an label for teamB name
 					 var label_teamB_name = document.createElement("label");
 					 label_teamB_name.style.fontSize = "x-large";
 					 var text_for_teamB_name_label = document.createTextNode("Team B:");
 					 label_teamB_name.appendChild(text_for_teamB_name_label);


						// Create an input for teamB name
						var team_B = document.createElement("input");
						team_B.setAttribute("type", "text");
						team_B.setAttribute("name", "TeamB");
						team_B.setAttribute("id", "team_b");
						team_B.setAttribute("class", "form-control");
						team_B.value= data[1][2];


						// Game location

						// Create an label for game location
  					 var label_game_location = document.createElement("label");
  					 label_game_location.style.fontSize = "x-large";
  					 var text_for_game_location_label = document.createTextNode("Game Location:");
  					 label_game_location.appendChild(text_for_game_location_label);

						 // Create an input for game location
						 var where_gamed_play = document.createElement("input");
						 where_gamed_play.required;
						 where_gamed_play.setAttribute("type", "text");
						 where_gamed_play.setAttribute("name", "where_gamed_play");
						 where_gamed_play.setAttribute("class", "form-control");
						 where_gamed_play.setAttribute("id", "where_gamed_play");
						 where_gamed_play.value= data[1][3];

						 // Create an label for game Date
							var label_game_date = document.createElement("label");
							label_game_date.style.fontSize = "x-large";
							var text_for_game_date_label = document.createTextNode("Game date: (format: yyyy-mm-dd)");
							label_game_date.appendChild(text_for_game_date_label);


							// Create an input for game Date
							var date_of_game = document.createElement("input");
							date_of_game.setAttribute("type", "text");
							date_of_game.setAttribute("name", "date_of_game");
							date_of_game.setAttribute("class", "form-control");
							date_of_game.setAttribute("id", "date_of_game");
							date_of_game.value= data[1][4];


							// Create an label for game weather
							 var label_game_weather = document.createElement("label");
							 label_game_weather.style.fontSize = "x-large";
							 var text_for_game_weather_label = document.createTextNode("Weather:");
							 label_game_weather.appendChild(text_for_game_weather_label);

							// Create an input element for Weather
							var weather = document.createElement("input");
							weather.setAttribute("type", "text");
							weather.setAttribute("name", "Weather");
							weather.setAttribute("class", "form-control");
							weather.setAttribute("id", "weather");
							weather.value= data[1][5];

							// Create an label for teamA ball in
							 var label_ball_in_acc_team_a = document.createElement("label");
							 label_ball_in_acc_team_a.style.fontSize = "x-large";
							 var text_for_label_ball_in_acc_team_a = document.createTextNode("Team A ball in (%):");
							 label_ball_in_acc_team_a.appendChild(text_for_label_ball_in_acc_team_a);

							 // Create an input for teamA ball in
							var ball_in_acc_team_a = document.createElement("input");
							ball_in_acc_team_a.setAttribute("type", "text");
							ball_in_acc_team_a.setAttribute("name", "ball_in_acc_team_a");
							ball_in_acc_team_a.setAttribute("class", "form-control");
							ball_in_acc_team_a.addEventListener('change', ball_in_a_input_change);
							ball_in_acc_team_a.setAttribute("id", "ball_in_acc_team_a");
							ball_in_acc_team_a.value= data[1][6];

							// Create an label for teamB ball in
							 var label_ball_in_acc_team_b = document.createElement("label");
							 label_ball_in_acc_team_b.style.fontSize = "x-large";
							 var text_for_label_ball_in_acc_team_b = document.createTextNode("Team B ball in (%):");
							 label_ball_in_acc_team_b.appendChild(text_for_label_ball_in_acc_team_b);

							// Create an input element for retype-password
							var ball_in_acc_team_b = document.createElement("input");
							ball_in_acc_team_b.setAttribute("type", "text");
							ball_in_acc_team_b.setAttribute("name", "ball_in_acc_team_b");
							ball_in_acc_team_b.addEventListener('change', ball_in_b_input_change);
							ball_in_acc_team_b.setAttribute("class", "form-control");
							ball_in_acc_team_b.setAttribute("id", "ball_in_acc_team_b");
							ball_in_acc_team_b.value= data[1][7];

							// Create an label for teamA ball in
							 var label_ball_out_acc_team_a = document.createElement("label");
							 label_ball_out_acc_team_a.style.fontSize = "x-large";
							 var text_for_label_ball_out_acc_team_a = document.createTextNode("Team A ball out (%):");
							 label_ball_out_acc_team_a.appendChild(text_for_label_ball_out_acc_team_a);

							var ball_out_acc_team_a = document.createElement("input");
							ball_out_acc_team_a.setAttribute("type", "text");
							ball_out_acc_team_a.setAttribute("name", "ball_out_acc_team_a");
							ball_out_acc_team_a.setAttribute("class", "form-control");
							ball_out_acc_team_a.setAttribute("id", "ball_out_acc_team_a");
							ball_out_acc_team_a.addEventListener('change', ball_out_a_input_change);
							ball_out_acc_team_a.value= data[1][8];


							// Create an label for teamB ball in
							 var label_ball_out_acc_team_b = document.createElement("label");
							 label_ball_out_acc_team_b.style.fontSize = "x-large";
							 var text_for_label_ball_out_acc_team_b = document.createTextNode("Team B ball out (%):");
							 label_ball_out_acc_team_b.appendChild(text_for_label_ball_out_acc_team_b);
							var ball_out_acc_team_b = document.createElement("input");
							ball_out_acc_team_b.setAttribute("type", "text");
							ball_out_acc_team_b.setAttribute("name", "ball_out_acc_team_b");
							ball_out_acc_team_b.setAttribute("class", "form-control");
							ball_out_acc_team_b.setAttribute("id", "ball_out_acc_team_b");
							ball_out_acc_team_b.addEventListener('change', ball_out_b_input_change);
							ball_out_acc_team_b.value= data[1][9];

							// Create an label for game weather
							 var system_accuracy_percentage_label = document.createElement("label");
							 system_accuracy_percentage_label.style.fontSize = "x-large";
							 var system_accuracy_percentage_text = document.createTextNode("system accurecy (%):");
							 system_accuracy_percentage_label.appendChild(system_accuracy_percentage_text);

							// Create an input element for Weather
							var system_accuracy_percentage_input = document.createElement("input");
							system_accuracy_percentage_input.readOnly = true;
							system_accuracy_percentage_input.setAttribute("type", "text");
							system_accuracy_percentage_input.setAttribute("name", "system_accuracy");
							system_accuracy_percentage_input.setAttribute("class", "form-control");
							system_accuracy_percentage_input.setAttribute("id", "system_accuracy_percentage_input");
							system_accuracy_percentage_input.value= data[1][10];


								 // create a submit button
							 var s = document.createElement("input");
							 s.setAttribute("type", "submit");
							 s.setAttribute("value", "Submit");
							 s.setAttribute("class", "btn btn-primary");
							 s.setAttribute("id", "submit_btn");
							 // s.addEventListener('click', return submit_form);


							 // Append the full game name label to the form
							 form.appendChild(label_game_name);
							 form.appendChild(br.cloneNode());


							 // Append the full game name input to the form
							 form.appendChild(game_name);
							 form.appendChild(br.cloneNode());


							 // Append the teamA label name to the form
							 form.appendChild(label_teamA_name);
							 form.appendChild(br.cloneNode());

							 // Append the teamA input name to the form
							 form.appendChild(team_A);
							 form.appendChild(br.cloneNode());


							// Append the teamB label name to the form
							form.appendChild(label_teamB_name);
							form.appendChild(br.cloneNode());

							// Append the teamB input name to the form
							 form.appendChild(team_B);
							 form.appendChild(br.cloneNode());

							 // Append the game location label to the form
							 form.appendChild(label_game_location);
 							 form.appendChild(br.cloneNode());

							 // Append the game location input to the form
							 form.appendChild(where_gamed_play);
							 form.appendChild(br.cloneNode());


							 // Append the game date label to the form
							 form.appendChild(label_game_date);
 							 form.appendChild(br.cloneNode());

							 // Append the game date input to the form
							 form.appendChild(date_of_game);
							 form.appendChild(br.cloneNode());

							 // Append the game weather label to the form
							 form.appendChild(label_game_weather);
 							 form.appendChild(br.cloneNode());

							 // Append the game weather label to the form
							 form.appendChild(weather);
							 form.appendChild(br.cloneNode());

							// Append the team A  ball in label to the form
							form.appendChild(label_ball_in_acc_team_a);
							form.appendChild(br.cloneNode());


							 // Append the team A ball in input to the form
							 form.appendChild(ball_in_acc_team_a);
							 form.appendChild(br.cloneNode());


							 // Append the team B  ball in label to the form
							 form.appendChild(label_ball_in_acc_team_b);
							 form.appendChild(br.cloneNode());

							 // Append the team B  ball in input to the form
							 form.appendChild(ball_in_acc_team_b);
							 form.appendChild(br.cloneNode());


							 // Append the team A ball out label to the form
							 form.appendChild(label_ball_out_acc_team_a);
							 form.appendChild(br.cloneNode());


							  // Append the team A ball out label to the form
							 form.appendChild(ball_out_acc_team_a);
							 form.appendChild(br.cloneNode());

							 // Append the team B ball out label to the form
							form.appendChild(label_ball_out_acc_team_b);
							form.appendChild(br.cloneNode());

							// Append the team B ball out input to the form
							form.appendChild(ball_out_acc_team_b);
							form.appendChild(br.cloneNode());

							// Append the team B ball out label to the form
						  form.appendChild(system_accuracy_percentage_label);
						  form.appendChild(br.cloneNode());

						  // Append the team B ball out input to the form
						  form.appendChild(system_accuracy_percentage_input);
						  form.appendChild(br.cloneNode());

							 // Append the submit button to the form
							form.appendChild(s);
							document.getElementById("model_body").appendChild(form);
							create_db_form_flag++;
						}
					});
					// form_validate();
				}

				function show_pop_up(){
					var popup = document.getElementById("myPopup");
		      popup.classList.toggle("show");

					if(popup.classList.contains("show")) // Check if the popup is shown
     			setTimeout(() => popup.classList.remove("show"), 2500) // If yes hide it after 10000 milliseconds
				}

				window.onload=function(){
					var circle_chart = document.getElementById("circle_chart");
					circle_chart.style.display = "none";
					var input = document.getElementById('inputGroupFile01');
					input.addEventListener('change', function() {
						readXlsxFile(input.files[0]).then(function(data) {
							data_global = data;
							var i = 0;
							choose = 'doughnut';
							data.map((row, index) => {
								if (i == 0) { // is the first row, its the headres
									var table = document.getElementById('tbl-data')
									generateTableRows(table, row, i ,choose);
								}
								if (i > 0) {
									var table = document.getElementById('tbl-data');
									generateTableRows(table, row, i, choose);
								}
								++i;
							});
							displayChart(data, choose, 'my_donut_chart');
							$('#number1').jQuerySimpleCounter({
								end: data[1][6],
								duration: 3000
							});
							// var number1 = document.getElementById('number1');
							// number1.innerHTML = number1.value + "%";
							$('#number2').jQuerySimpleCounter({
								end: data[1][8],
								duration: 3000
							});
							$('#number3').jQuerySimpleCounter({
								end: data[1][7],
								duration: 2000
							});
							$('#number4').jQuerySimpleCounter({
								end: data[1][9],
								duration: 2500
							});
							let team_a_ball_in = document.getElementById("team_a_ball_in");
							team_a_ball_in.innerHTML = data[1][1] + " ball in (%)";

							let team_b_ball_in = document.getElementById("team_b_ball_in");
							team_b_ball_in.innerHTML = data[1][2] + " ball in (%)";

							let team_a_ball_out = document.getElementById("team_a_ball_out");
							team_a_ball_out.innerHTML = data[1][1] + " ball out (%)";

							let team_b_ball_out = document.getElementById("team_b_ball_out");
							team_b_ball_out.innerHTML = data[1][2] + " ball out (%)";
							// ctx.fillText(data[1][7].value + "%", 100,100, 200);
							let h1_first_team = document.getElementById("h1_first_team");
							h1_first_team.innerHTML = data[1][1];
							h1_first_team.style.display = "block";
							let h1_second_team = document.getElementById("h1_second_team");
							h1_second_team.innerHTML = data[1][2];
							h1_second_team.style.display = "block";
						});
					});



					function generateTableRows(table, data, i, choose) {
						let id = 1;
						let newRow = table.insertRow(-1);
						data.map((row, index) => {
							if (i != 0) {
								let newcell = newRow.insertCell();
								let newText = document.createTextNode(row)
								// console.log(newText);
								newcell.setAttribute("id", id);
								newcell.appendChild(newText);
								id++;
							}
							// console.log(data);
							let canvas = document.getElementById("my_bar_chart");
							if(choose == 'doughnut'){
							 canvas = document.getElementById("my_donut_chart");
							}
							canvas.style.display = "block";
							let stats = document.getElementById("projectFacts");
							stats.style.display = "block";
							let save_data_button = document.getElementById("save_data");
							save_data_button.style.display = "block";

							let list = document.getElementById("list");
							list.style.display = "block";

							let input_csv = document.getElementById("input_csv");
							input_csv.style.display = "none";

							var circle_chart = document.getElementById("circle_chart");
							circle_chart.style.display = "block";
							if(flag_of_percentage == 0){
								update_percentage();
								flag_of_percentage = 1;
							}
						});
					}

					function generateTableHead(table, data) {
						let thead = table.createTHead();
						let row = thead.insertRow();
						for (let key of data) {
							let th = document.createElement('thead');
							// th.classList.add("table-dark");
							let text = document.createTextNode(key);
							th.appendChild(text);
							row.appendChild(th);
						}
					}
					function ifChooseChange(lsat_choose, current_choose){
						if(lsat_choose != current_choose){
							return true;
						} else{
							return false;
						}
					}
				}

				function submit_form(){
			    let formValid = form_validation()
			    return formValid;
				}

				function form_validation(){
						let if_form_valid = true;
					  if_form_valid = valdiate_input_string(document.getElementById("game_name"),"Game Name ");
						if(if_form_valid == false) return false;
						if_form_valid = valdiate_input_string(document.getElementById("team_a"),"Team A ");
						if(if_form_valid == false) return false;
						if_form_valid =valdiate_input_string(document.getElementById("team_b"),"Team B ");
						if(if_form_valid == false) return false;
						if_form_valid =valdiate_input_string(document.getElementById("where_gamed_play"),"Game Location ");
						if(if_form_valid == false) return false;
						if_form_valid =valdiate_input_string(document.getElementById("date_of_game"),"Game date");
						if(if_form_valid == false)  return false;
						if_form_valid =valdiate_input_string(document.getElementById("weather"),"Weather");
						if(if_form_valid == false)  return false;
 				  	if_form_valid =valdiate_input_number(document.getElementById("ball_in_acc_team_a"),"Team A ball in ");
						if(if_form_valid == false) return false;
						if_form_valid =valdiate_input_number(document.getElementById("ball_in_acc_team_b"),"Team B ball in ");
						if(if_form_valid == false) return false;
						if_form_valid =valdiate_input_number(document.getElementById("ball_out_acc_team_a"),"Team A ball out ");
						if(if_form_valid == false) return false;
						if_form_valid = valdiate_input_number(document.getElementById("ball_out_acc_team_b"),"Team B ball out ");
						if(if_form_valid == false){
							return false;
						}
						else{
							return true;
						}
				}

				function valdiate_input_string(element,msg){
					value = element.value;
					if(value == ""){
						alert(msg + " must be filled out");
						element.setAttribute("class", "form-control is-invalid");
						return false;
					}
					if(!isNaN(value) && !isNaN(parseFloat(value)) && !isNaN(parseInt(value))){
						alert(msg +" must be word, can't be a number");
						element.setAttribute("class", "form-control is-invalid");
						return false;
					}
					element.setAttribute("class", "form-control is-valid");
					return true;
				}

				function valdiate_input_number(element,msg){
					value = element.value;
					if(value == ""){
						alert(msg + " must be filled out");
						element.setAttribute("class", "form-control is-invalid");

						return false;
					}
					if(isNaN(value) && isNaN(parseFloat(value)) && isNaN(parseInt(value))){
						alert(msg +" must be Number!");
						element.setAttribute("class", "form-control is-invalid");
						return false;
					}
					if(value >= 0 && value <= 100){
					element.setAttribute("class", "form-control is-valid");
					return true;
				} else {
					alert(msg +" must be between 0 to 100!");
					element.setAttribute("class", "form-control is-invalid");
					return false;
				}
			}
				function stop_submit(){
					$('form').submit(function(e) {
						e.preventDefault();
					});
					return false;
				}

				function start_submit(){
					return true;
				}

				function ball_in_a_input_change(e){
					if(e.target.value >= 0 && e.target.value <= 100){
						var teamA_ball_out_obj = document.getElementById("ball_out_acc_team_a");
						var a = 100-e.target.value;
						teamA_ball_out_obj.value = a;
					} else{
						alert("Value of Ball in Team A must be between 0 to 100");
						// submit_form();
					}
				}

				function ball_in_b_input_change(e){
					if(e.target.value >= 0 && e.target.value <= 100){
					var teamB_ball_out_obj = document.getElementById("ball_out_acc_team_b");
					var b = 100-e.target.value;
					teamB_ball_out_obj.value = b;
				  } else {
					alert("Value of Ball in Team B must be between 0 to 100");
			  	}
		  	}
				function ball_out_a_input_change(e){
					if(e.target.value >= 0 && e.target.value <= 100){
					var teamA_ball_out_obj = document.getElementById("ball_in_acc_team_a");
					var a = 100-e.target.value;
					teamA_ball_out_obj.value = a;
				}else {
					alert("Value of Ball Out Team A must be between 0 to 100");
				}
			}
				function ball_out_b_input_change(e){
					if(e.target.value >= 0 && e.target.value <= 100){
					var teamB_ball_out_obj = document.getElementById("ball_in_acc_team_b");
					var b = 100-e.target.value;
					teamB_ball_out_obj.value = b;
				 }else{
					 alert("Value of Ball Out Team B must be between 0 to 100");
				}
			}

				function update_percentage(){
					console.log(data_global);
					let system_accuracy_percentage = document.getElementById("system_accuracy_percentage");
					system_accuracy_percentage.innerHTML = "";
					var y = document.createTextNode(data_global[1][10].toString() +'%');
					system_accuracy_percentage.appendChild(y);
					let fill = document.getElementById("circle-chart_fill");
					fill.setAttribute("stroke-dasharray" , data_global[1][10].toString() + ', 100');
				}

				function displayChart(data,choose,id){
					let ctx = document.getElementById(id);
					if(choose == "doughnut"){
						var bar_chart = document.getElementById('my_bar_chart');
						bar_chart.style.display = "none";
						var rader_chart = document.getElementById('my_radar_chart');
						rader_chart.style.display = "none";
						ctx.style.display = "block";
						dataArray = [data[1][6], data[1][7], data[1][8], data[1][9]];
					} else{
						if(choose == "bar"){
						var donut_chart = document.getElementById('my_donut_chart');
						donut_chart.style.display = "none";
						var rader_chart = document.getElementById('my_radar_chart');
						rader_chart.style.display = "none";
						ctx.style.display = "block";
						dataArray = [data[1][6], data[1][7], data[1][8], data[1][9] , 0];
					} else {
						var donut_chart = document.getElementById('my_donut_chart');
						donut_chart.style.display = "none";
						var bar_chart = document.getElementById('my_bar_chart');
						bar_chart.style.display = "none";
						ctx.style.display = "block";
					}
					}
					// ctx.style.display = 'none';

					let myChart = new Chart(ctx, {
						title: {
							verticalAlign: "center"
						},
						type: choose,
						data: {
							labels: [data[1][1] +': '+'ball in', data[1][2] +': '+'ball in', data[1][1] +': '+'ball out',data[1][2] +': '+'ball out'],
							datasets: [{
								label: 'Game statistics',
								data: dataArray,
								backgroundColor: [
									'rgba(255, 99, 132,0.9)',
									'rgba(54, 162, 235, 0.9)',
									'rgba(255, 206, 86, 0.9)',
									'rgba(75, 192, 192, 0.9)',
								],
								borderColor: [
									'rgba(255, 99, 132, 1)',
									'rgba(54, 162, 235, 1)',
									'rgba(255, 206, 86, 1)',
									'rgba(75, 192, 192, 1)',
									// 'rgba(153, 102, 255, 0.2)',
									// 'rgba(255, 159, 64, 0.2)'
								],
								borderWidth: 5,
							}]
						},
						options: {
							cutoutPercentage: 60,
							scales: {
								y: {
									beginAtZero: true
								},
								pointLabels: {
      					fontSize: 16
								},
							},
							tooltips: {
							  callbacks: {
							    label: function(tooltipItem, data) {
							      return data['labels'][tooltipItem['index']] + ': ' + data['datasets'][0]['data'][tooltipItem['index']] + '%';
							    }
							  }
							},
							legend: {
								labels: {
									fontSize: 20
								}
							},
						}
					})
			}

				function getChoosenValue(){
					var choose = "";
					var id = "";
					var choose_value = document.getElementById("list");
					if(choose_value.value == "donut_chart"){
						choose = 'doughnut';
						id = "my_donut_chart";
					} else {
						if(choose_value.value == "bar_chart"){
						choose = 'bar';
						id = "my_bar_chart";
					} else{
						choose = 'radar';
						id = "my_radar_chart";
					}
				}
					if(choose !='choose'){
					displayChart(data_global,choose,id);
					}
				}
