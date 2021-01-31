$(function(e){
  'use strict'

	/* Apexchart*/
	var options = {
		chart: {
			height: 241,
			type: 'area',
			stacked: true,
			events: {
			  selection: function(chart, e) {
				console.log(new Date(e.xaxis.min) )
			  }
			},
		},
		colors: ['#2d66f7', '#6b94fa', '#cedbfd'],
		dataLabels: {
		  enabled: false
		},
		stroke: {
			curve: 'smooth'
		},
		series: [{
                name: 'sales',
                data: [10, 15, 9, 18, 10, 15, 10, 15, 9, 18, 10, 15]
            },{
                name: 'profit',
                data: [8, 5, 17, 10, 10, 12,8, 5, 18, 10, 10, 12]
            }, {
                name: 'Sales Revenue',
                data: [10, 14, 10, 15, 9, 20, 10, 14, 10, 15, 9, 17]
		}],
		fill: {
			gradient: {
			  enabled: true,
			  opacityFrom: 0.6,
			  opacityTo: 0.8,
			}
		},
			legend: {
			position: 'bottom',
			horizontalAlign: 'center'
		},
    }
    var chart = new ApexCharts(
      document.querySelector("#chart"),
      options
    );
    chart.render();
    function generateDayWiseTimeSeries(baseval, count, yrange) {
		var i = 0;
		var series = [];
		while (i < count) {
			var x = baseval;
			var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

			series.push([x, y]);
			baseval += 86400000;
			i++;
		}
		return series;
    }


    /*sparkline*/
    var randomizeArray = function (arg) {
		var array = arg.slice();
		var currentIndex = array.length,
		temporaryValue, randomIndex;
		while (0 !== currentIndex) {
			randomIndex = Math.floor(Math.random() * currentIndex);
			currentIndex -= 1;

			temporaryValue = array[currentIndex];
			array[currentIndex] = array[randomIndex];
			array[randomIndex] = temporaryValue;
		}
		return array;
    }
    var sparklineData = [47, 45, 54, 38, 56, 24, 65, 31, 37, 39, 62, 51, 35, 41, 35, 27, 93, 53, 61, 27, 54, 43, 19, 46];
	$.get('http://localhost:5000/api/rest/metrics/query?metric=' + $('#spark1').attr('title') + '&start=-1m', function(data) {
        window.spark1 = new ApexCharts(document.querySelector("#spark1"), {
          chart: {
            type: 'area',
            height: 40,
            sparkline: {
              enabled: true
            },
          },
          stroke: {
            curve: 'straight'
          },
          fill: {
            opacity: 0.3,
            gradient: {
              enabled: false
            }
          },
          series: [{
            name: 'Total Sales',
            data: $.map(JSON.parse(data), function(measurement) {
                return measurement.value
            })
          }],
          yaxis: {
            min: 0
          },
          colors: ['#cedbfd'],

        });

        window.spark1.render();

        var socket = new WebSocket('ws://localhost:5000/api/socket/metrics/query?metric=' + $('#spark1').attr('title'))
        socket.onmessage = function(message) {
            console.log([JSON.parse(message.data)])
            window.spark1.appendData([{'data': [JSON.parse(message.data).value]}])
        }
    })

	//Spark2
	var spark2 = {
      chart: {
        type: 'area',
        height: 40,
        sparkline: {
          enabled: true
        },
      },
      stroke: {
        curve: 'straight'
      },
      fill: {
        opacity: 0.3,
        gradient: {
          enabled: false
        }
      },
      series: [{
		name: 'Total Profits',
        data: randomizeArray(sparklineData)
      }],
      yaxis: {
        min: 0
      },
      colors: ['#fdcedb'],

    }
	var spark2 = new ApexCharts(document.querySelector("#spark2"), spark2);
    spark2.render();
	//Spark3
	var spark3 = {
      chart: {
        type: 'area',
        height: 40,
        sparkline: {
          enabled: true
        },
      },
      stroke: {
        curve: 'straight'
      },
      fill: {
        opacity: 0.3,
        gradient: {
          enabled: false
        }
      },
      series: [{
		name: 'Total Orders',
        data: randomizeArray(sparklineData)
      }],
      yaxis: {
        min: 0
      },
      colors: ['#fce8b5'],

    }
	var spark3 = new ApexCharts(document.querySelector("#spark3"), spark3);
    spark3.render();
	//Spark4
	var spark4 = {
      chart: {
        type: 'area',
        height: 40,
        sparkline: {
          enabled: true
        },
      },
      stroke: {
        curve: 'straight'
      },
      fill: {
        opacity: 0.3,
        gradient: {
          enabled: false
        }
      },
      series: [{
		name: 'Total Sales Revenue',
        data: randomizeArray(sparklineData)
      }],
      yaxis: {
        min: 0
      },
      colors: ['#b5fce8'],

    }
	var spark4 = new ApexCharts(document.querySelector("#spark4"), spark4);
    spark4.render();

 });
