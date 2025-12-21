<!-- docs/index.md -->
# Bar Chart Example

<div id="chart-container" style="width: 600px;height:400px;"></div>

<script>
  // Initialize the ECharts instance upon page load
  document.addEventListener('DOMContentLoaded', (event) => {
    var chartDom = document.getElementById('chart-container');
    var myChart = echarts.init(chartDom);
    var option;

    // Specify the configuration and data for the chart
    option = {
      title: {
        text: 'ECharts Bar Chart'
      },
      tooltip: {},
      legend: {
        data: ['Sales']
      },
      xAxis: {
        data: ['Shirt', 'Cardigan', 'Chiffon Shirt', 'Pants', 'Heels', 'Pumps']
      },
      yAxis: {},
      series: [
        {
          name: 'Sales',
          type: 'bar',
          data: [5, 20, 36, 10, 10, 20]
        }
      ]
    };

    // Render the chart using the configuration
    myChart.setOption(option);
  });
</script>
