// get bar chart canvas
var mychart = document.getElementById("chart").getContext("2d");

  steps = 10
  max = 17000

// draw bar chart
new Chart(mychart).Bar(barData, {
  scaleOverride: true,
  scaleSteps: steps,
  scaleStepWidth: Math.ceil(max / steps),
  scaleStartValue: 0,
  scaleShowVerticalLines: true,
  scaleShowGridLines : true,
  barShowStroke : true,
  scaleShowLabels: true
  }
);