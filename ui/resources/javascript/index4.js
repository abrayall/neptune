$(function(e){
  'use strict'
  
	/*-----echart-----*/
	var chartdata3 = [
		{
		  name: 'Outpatients',
		  type: 'bar',
		  stack: 'Stack',
		  data: [14, 18, 20, 14, 29, 21, 25, 14, 24, 14, 18, 20, 14,17,14, 29, 21]
		},
		{
		  name: 'Inpatients',
		  type: 'bar',
		  stack: 'Stack',
		  data: [12, 14, 15, 50, 24, 24, 10, 20 ,30, 30, 24, 24, 10, 20 ,30,12, 14, 15]
		}
	];

	var option5 = {
		grid: {
		  top: '6',
		  right: '0',
		  bottom: '17',
		  left: '25',
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
		xAxis: {
		  data: ['2003','2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'],
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
		series: chartdata3,
		color:[ '#2d66f7', '#cedbfd']
	};
	var chart5 = document.getElementById('echart5');
	var barChart5 = echarts.init(chart5);
	barChart5.setOption(option5);
	/*-----echart-----*/
	
	/*-----canvasDoughnut-----*/
	if ($('.canvasDoughnut').length){

		var chart_doughnut_settings = {
			type: 'doughnut',
			tooltipFillColor: "rgba(51, 51, 51, 0.55)",
			data: {
				labels: [
					"Excellent",
					"Very Good",
					"Good",
					"Average",
					"Poor",
					"Bad"
				],
				datasets: [{
					data: [68, 55, 45, 34, 27, 15],
					backgroundColor: [
						"#2d66f7",
						"#2dcbf7",
						"#f7be2d",
						"#2df7be",
						"#f7592d",
						"#f72d66 "

					],
					hoverBackgroundColor: [
						"#2d66f7",
						"#2dcbf7",
						"#f7be2d",
						"#2df7be",
						"#f7592d",
						"#f72d66 "

					]
				}]
			},
			options: {
				legend: false,
				responsive: false
			}
		}

		$('.canvasDoughnut').each(function(){

			var chart_element = $(this);
			var chart_doughnut = new Chart( chart_element, chart_doughnut_settings);

		});
	}
	/*-----canvasDoughnut-----*/
	
	/*----AreaChart2----*/
	var ctx = document.getElementById( "AreaChart2" );
	var myChart = new Chart( ctx, {
		type: 'line',
		data: {
			labels: ['Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'],
			type: 'line',
			datasets: [ {
				data: [83, 73, 91, 85, 76, 90, 100],
				label: 'Male Bounce Rate',
				backgroundColor: 'rgb(45, 102, 247,0.1)',
				borderColor: 'rgba(45, 102, 247,0.6)',
				borderWidth: '3',
				pointBorderColor: 'transparent',
				pointBackgroundColor: 'transparent',
			}
			]
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
				titleFontColor: '#7886a0',
				bodyFontColor: '#7886a0',
				backgroundColor: '#fff',
				titleFontFamily: 'Montserrat',
				bodyFontFamily: 'Montserrat',
				cornerRadius: 3,
				intersect: false,
			},
			scales: {
				xAxes: [ {
					gridLines: {
						color: 'transparent',
						zeroLineColor: 'transparent'
					},
					ticks: {
						fontSize: 2,
						fontColor: 'transparent'
					}
				} ],
				yAxes: [ {
					display:false,
					ticks: {
						display: false,
					}
				} ]
			},
			title: {
				display: false,
			},
			elements: {
				line: {
					borderWidth: 1
				},
				point: {
					radius: 4,
					hitRadius: 10,
					hoverRadius: 4
				}
			}
		}
	} );
	/*----End AreaChart2----*/
  
	/*-----echart6-----*/
	var chartdata4 = [
		{
		  name: 'Surgical Stays',
		  type: 'bar',
		  stack: 'Stack',
		  data: [14, 18, 20, 14]
		},
		{
		  name: 'Maternal and Neonatal Stays',
		  type: 'bar',
		  stack: 'Stack',
		  data: [12, 14, 15, 50]
		},
		{
		  name: 'Medical Stays',
		  type: 'bar',
		  stack: 'Stack',
		  data: [24, 10, 20 ,30]
		}
	];

	var option6 = {
		grid: {
		  top: '6',
		  right: '10',
		  bottom: '17',
		  left: '92',
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
		xAxis: {
		  type: 'value',
		  display: false,
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
		yAxis: {
		  type: 'category',
		   data: ['Medicare', 'Medicaid', 'Private Insurance', 'Uninsured'],
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
		series: chartdata4,
		color:[ '#2d66f7', '#6b94fa', '#cedbfd']
	};
	var chart6 = document.getElementById('echart6');
	var barChart6 = echarts.init(chart6);
	barChart6.setOption(option6);
});