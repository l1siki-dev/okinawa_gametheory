// docs/javascripts/charts.js
document$.subscribe(function() {
  const canvas = document.getElementById('myChart');
  if (canvas) {
    new Chart(canvas, {
      type: 'line',
      data: { /* your data */ },
      options: { /* your options */ }
    });
  }
});
