( function ( $ ) {
	"use strict";
    
	/*-----echart1-----*/
	var chartdata = [
		{
		  name: 'Available Balance $',
		  type: 'bar',
		  data: [10, 15, 9, 18, 10, 15, 10, 15, 9, 18, 10, 15]
		},
		
		{
		  name: 'Pending Balance $',
		  type: 'bar',
		  data: [10, 14, 10, 15, 9, 20, 10, 14, 10, 15, 9, 17]
		}
	];

	var chart = document.getElementById('echart1');
	var barChart = echarts.init(chart);

	var option = {
		grid: {
		  top: '6',
		  right: '0',
		  bottom: '17',
		  left: '25',
		},
		xAxis: {
		  data: [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug',  'Sep', 'Oct', 'Nov', 'Dec'],
		  axisLine: {
			lineStyle: {
			  color: 'rgba(67, 87, 133, .09)'
			}
		  },
		  axisLabel: {
			fontSize: 10,
			color: '#8e9cad'
		  }
		},
		tooltip: {
			show: true,
			showContent: true,
			alwaysShowContent: true,
			triggerOn: 'mousemove',
			trigger: 'axis',
			axisPointer:
			{
				label: {
					show: false,
				}
			}

		},
		yAxis: {
		  splitLine: {
			lineStyle: {
			  color: 'rgba(67, 87, 133, .09)'
			}
		  },
		  axisLine: {
			lineStyle: {
			  color: 'rgba(67, 87, 133, .09)'
			}
		  },
		  axisLabel: {
			fontSize: 10,
			color: '#8e9cad'
		  }
		},
		series: chartdata,
		color:[ '#2d66f7','#f7be2d ']
	};
	barChart.setOption(option);
	
	/* Chartjs (#quick-ratio) */
	var ctx = document.getElementById('quick-ratio').getContext('2d');
	var myChart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
			type: 'line',
			datasets: [{
				label: "Quick ratio",
				data: [5, 105, 26, 145, 65, 172, 182, 98, 215, 245, 62, 255],
				backgroundColor: "rgba(45,102,247,0.1)",
				borderColor: "rgba(45,102,247,0.5)",
				borderWidth: 4,
				pointStyle: 'circle',
				pointRadius: 0,
				pointBorderColor: 'transparent',
				pointBackgroundColor: '#2d66f7',
			}]
		},
		options: {
			maintainAspectRatio: false,
			legend: {
				display: false
			},
			responsive: true,
			tooltips: {
                mode: 'index',
                titleFontSize: 12,
                titleFontColor: '#031938',
                bodyFontColor: '#031938',
                backgroundColor: '#fff',
                titleFontFamily: 'Montserrat',
                bodyFontFamily: 'Montserrat',
                cornerRadius: 3,
                intersect: false,
            },
			scales: {
				xAxes: [{
					display: false,
					gridLines: {
						color: 'rgba(0,0,0,0.061)'
					},
					scaleLabel: {
						display: false,
						labelString: '',
						fontColor: 'rgba(0,0,0,0.61)'
					}
				}],
				yAxes: [{
					display: false,
					gridLines: {
						display: false,
						drawBorder: true
					},
					scaleLabel: {
						display: false,
						labelString: 'Customer retention in %',
						fontColor: 'rgba(0,0,0,0.61)'
					}
				}]
			},
			title: {
				display: false,
				text: 'Normal Legend'
			}
		}
	});
	/* Chartjs (#quick-ratio) closed*/
	
	/* Chartjs (#current-ratio) */
	var ctx = document.getElementById('current-ratio');
	var myChart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
			type: 'line',
			datasets: [{
				label: "Current ratio",
				data: [5, 105, 26, 145, 65, 172, 182, 98, 215, 245, 62, 255],
				backgroundColor: "rgba(247,45,102,0.1)",
				borderColor: "rgba(247,45,102,0.5)",
				borderWidth: 4,
				pointStyle: 'circle',
				pointRadius: 0,
				pointBorderColor: 'transparent',
				pointBackgroundColor: '#f54274',
			}]
		},
		options: {
			maintainAspectRatio: false,
			legend: {
				display: false
			},
			responsive: true,
			tooltips: {
                mode: 'index',
                titleFontSize: 12,
                titleFontColor: '#031938',
                bodyFontColor: '#031938',
                backgroundColor: '#fff',
                titleFontFamily: 'Montserrat',
                bodyFontFamily: 'Montserrat',
                cornerRadius: 3,
                intersect: false,
            },
			scales: {
				xAxes: [{
					display: false,
					gridLines: {
						color: 'rgba(0,0,0,0.061)'
					},
					scaleLabel: {
						display: false,
						labelString: '',
						fontColor: 'rgba(0,0,0,0.61)'
					}
				}],
				yAxes: [{
					display: false,
					gridLines: {
						display: false,
						drawBorder: true
					},
					scaleLabel: {
						display: false,
						labelString: 'Customer retention in %',
						fontColor: 'rgba(0,0,0,0.61)'
					}
				}]
			},
			title: {
				display: false,
				text: 'Normal Legend'
			}
		}
	});
	/* Chartjs (#current-ratio) closed*/
	
	/* sparkline_area */
	$(".sparkline_area").sparkline([5, 6, 7, 9, 9, 5, 3, 2, 2, 4, 6, 7], {
		type: 'line',
		lineColor: '#f7be2d',
		fillColor: '#f7be2d',
		spotColor: '#f72d66',
		minSpotColor: '#f72d66',
		maxSpotColor: '#f72d66',
		highlightSpotColor: '#f7be2d',
		highlightLineColor: '#f7be2d',
		spotRadius: 2.5,
		width: 85
	});
	
	/* sparkline_bar31 */
	$(".sparkline_bar31").sparkline([2, 4, 3, 4, 5, 4,5,3,4,5,2,4,5,4], {
		type: 'bar',
		height: 80,
		width:250,
		barWidth: 5,
		barSpacing: 7,
		colorMap: {
			'9': '#a1a1a1'
		},
		barColor: '#2d66f7'
	});
	/* sparkline_bar31 end */
	
	/* sparkline_bar32 */
	$(".sparkline_bar32").sparkline([2, 4, 3, 4, 5, 4,5,3,4,5,2,4,5,4], {
		type: 'bar',
		height: 80,
		width:250,
		barWidth: 5,
		barSpacing: 7,
		colorMap: {
			'9': '#a1a1a1'
		},
		barColor: '#f72d66'
	});
	/* sparkline_bar32 end */
	
	/*---- morrisBar8----*/
	new Morris.Donut({
		  element: 'morrisBar8',
		  data: [
			{value: 50, label: 'Net'},
			{value: 25, label: 'Cash In'},
			{value: 15, label: 'Cash Out'}
		  ],
		  colors: [
		'#2d66f7', '#f72d66', '#f7be2d'

	  ],
		  formatter: function (x) { return x + "%"}
		}).on('click', function(i, row){
		  console.log(i, row);
	});
	
})( jQuery );

