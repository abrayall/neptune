$(function(e){
  'use strict'
	
	/* leads */
    var ctx = $('#leads');
	ctx.height(230);
	var myChart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"],
			type: 'line',
			datasets: [{
				label: "Leads",
				data: [253, 256, 395, 204, 251, 458, 364, 145, 156, 250, 253, 278],
				backgroundColor: 'rgba(45,102,247,0.8)',
				borderColor: 'rgba(45,102,247,0.9)',
				borderWidth: 0,
				pointStyle: 'circle',
				pointRadius: 0,
				pointBorderColor: 'transparent',
				pointBackgroundColor: 'rgba(45,102,247,0.8)',
			}]
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			tooltips: {
				mode: 'index',
				titleFontSize: 12,
				titleFontColor: 'rgba(0,0,0,0.9)',
				bodyFontColor: 'rgba(0,0,0,0.9)',
				backgroundColor: '#fff',
				bodyFontFamily: 'Montserrat',
				cornerRadius: 0,
				intersect: false,
			},
			legend: {
				display: false,
				labels: {
					usePointStyle: true,
					fontFamily: 'Montserrat',
				},
			},
			scales: {
				xAxes: [{
					ticks: {
						fontColor: "#8e9cad",
					},
					display: true,
					gridLines: {
						color: 'rgba(67, 87, 133, .09)'
					},
					scaleLabel: {
						display: false,
						labelString: '',
						fontColor: 'rgba(67, 87, 133, .09)'
					}
				}],
				yAxes: [{
					ticks: {
						fontColor: "#8e9cad",
					},
					display: true,
					gridLines: {
						display: false,
						drawBorder: true
					},
				}]
			},
			title: {
				display: false,
				text: 'Normal Legend'
			}
		}
	});
	/*leads end */
	
	/* sparkline_bar21 */
	$(".sparkline_bar21").sparkline([2, 4, 3, 4, 5, 4,5,3,4,5,2,4,5,4], {
		type: 'bar',
		height: 40,
		width:250,
		barWidth: 5,
		barSpacing: 7,
		colorMap: {
			'9': '#a1a1a1'
		},
		barColor: '#2d66f7'
	});
	/* sparkline_bar21 end */
	
	/* sparkline_bar22 */
	$(".sparkline_bar22").sparkline([2, 4, 3, 4, 5, 4,5,3,4,5,2,4,5,4], {
		type: 'bar',
		height: 40,
		width:250,
		barWidth: 5,
		barSpacing: 7,
		colorMap: {
			'9': '#a1a1a1'
		},
		barColor: '#f72d66'
	});
	/* sparkline_bar22 end */
	
	/*-----echart1-----*/

	var chartdata = [
		{
		  name: 'Marketing Spend $',
		  type: 'bar',
		  data: [10, 15, 9, 18, 10, 15, 18]
		},
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
			  data: [ 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'sun'],
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
		color:[ '#2dcbf7']
	};
	barChart.setOption(option);
	
});

