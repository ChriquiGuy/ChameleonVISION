
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
		      var popup = document.getElementById("myPopup");
		      popup.classList.toggle("show");
		    }

				window.onload=function(){
					var input = document.getElementById('inputGroupFile01');
					input.addEventListener('change', function() {
						readXlsxFile(input.files[0]).then(function(data) {
							console.log(data);
							var i = 0;
							data.map((row, index) => {
								if (i == 0) { // is the first row, its the headres
									var table = document.getElementById('tbl-data')
									generateTableRows(table, row, i);
								}
								if (i > 0) {
									var table = document.getElementById('tbl-data')
									generateTableRows(table, row);
								}
								++i;
							});
							let ctx = document.getElementById("mychart");
							let myChart = new Chart(ctx, {
								type: 'doughnut',
								data: {
									labels: ['team A: ball in', 'team B: ball in', 'team A: ball out', 'team B: ball out'],
									datasets: [{
										label: 'Game statistics',
										data: [data[1][6], data[1][7], data[1][8], data[1][9]],
										backgroundColor: [
											'rgba(255, 99, 132,0.9)',
											'rgba(54, 162, 235, 0.9)',
											'rgba(255, 206, 86, 0.9)',
											'rgba(75, 192, 192, 0.9)',

										],
										borderColor: [
											'rgba(255, 99, 132, 0.2)',
											'rgba(54, 162, 235, 0.2)',
											'rgba(255, 206, 86, 0.2)',
											'rgba(75, 192, 192, 0.2)',
											// 'rgba(153, 102, 255, 0.2)',
											// 'rgba(255, 159, 64, 0.2)'
										],
										borderWidth: 1
									}]
								},
								options: {
									scales: {
										y: {
											beginAtZero: true
										}
									}
								}
							})
							$('#number1').jQuerySimpleCounter({
								end: data[1][6],
								duration: 3000
							});
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
							let h1_first_team = document.getElementById("h1_first_team");
							h1_first_team.innerHTML = data[1][1];
							h1_first_team.style.display = "block";
							let h1_second_team = document.getElementById("h1_second_team");
							h1_second_team.innerHTML = data[1][2];
							h1_second_team.style.display = "block";
						});
					});

					function generateTableRows(table, data, i) {
						let newRow = table.insertRow(-1);
						//console.log(newRow);
						data.map((row, index) => {
							if (i != 0) {
								let newcell = newRow.insertCell();
								//  console.log(newcell);
								let newText = document.createTextNode(row)
								console.log(newText);
								newcell.appendChild(newText);
							}
							let canvas = document.getElementById("mychart")
							canvas.style.display = "block";
							let stats = document.getElementById("projectFacts")
							stats.style.display = "block";
							let excel_file_table = document.getElementById("tbl-data")
							excel_file_table.style.display = "block";
							let save_data_button = document.getElementById("save_data")
							save_data_button.style.display = "block"
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
				}
