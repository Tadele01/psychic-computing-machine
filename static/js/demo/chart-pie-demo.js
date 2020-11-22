// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Pie Chart Example
var ctx = document.getElementById("myPieChart");
const url = "http://127.0.0.1:5000/sentiment_analysis/realDonaldTrump";
var json_from_api;
var myPieChart;
fetch(url)
  .then(response => response.json())
  .then(json_from_api => console.log(json_from_api))
  .then(
  	 myPieChart = new Chart(ctx, {
	  type: 'doughnut',
	  data: {
		labels: json_from_api.labels,
		datasets: [{
		  data: json_from_api.values_,
		  backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
		  hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
		  hoverBorderColor: "rgba(234, 236, 244, 1)",
		}],
	  },
	  options: {
		maintainAspectRatio: false,
		tooltips: {
		  backgroundColor: "rgb(255,255,255)",
		  bodyFontColor: "#858796",
		  borderColor: '#dddfeb',
		  borderWidth: 1,
		  xPadding: 15,
		  yPadding: 15,
		  displayColors: false,
		  caretPadding: 10,
		},
		legend: {
		  display: false
		},
		cutoutPercentage: 80,
	  },
	})
  
  );


