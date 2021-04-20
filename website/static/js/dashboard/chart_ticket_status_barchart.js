// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Bar Chart Example
var ctx = document.getElementById("ticket_status_barchart");
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ["hello", "world", "goals"],
    datasets: [{
      data: [100, 25, 15],
      backgroundColor: ['#4e73df', '#1cc88a', '#36b9cc'],
      hoverBackgroundColor: ['#2e59d9', '#17a673', '#2c9faf'],
      hoverBorderColor: "rgba(234, 236, 244, 1)",
    }],
  },
    legend: {
      display: false
    },
    cutoutPercentage: 80,
  },
});
