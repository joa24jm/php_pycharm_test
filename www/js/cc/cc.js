// ================================================================
// Basic Chart.js example [START]
// ================================================================
const json_data_url = '../../json/example/example.json';

const labels = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
];

window.onload = getJSON(json_data_url, function(err, json_data) {
  if (err !== null) {
    console.log('Something went wrong: ' + err);
  } else {
    console.log('JSON Data:');
    console.log(json_data);

    // Configuring the Chart.js plot ...
    const data = {
      labels: labels,
      datasets: [{
        label: 'My First dataset',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: json_data['values'],
      }]
    };

    const config = {
      type: 'line',
      data: data,
      options: {}
    };

    const myChart = new Chart(
      document.getElementById('coronaCheckChart'),
      config
    );
  }
});

// $.getJSON('../json/example/example.json', function(json_data) {
//   // const json_data = [0, 10, 5, 2, 20, 30, 45]; // last value determines the y-axis scale maximum

//   const data = {
//     labels: labels,
//     datasets: [{
//       label: 'My First dataset',
//       backgroundColor: 'rgb(255, 99, 132)',
//       borderColor: 'rgb(255, 99, 132)',
//       data: json_data,
//     }]
//   };

//   const config = {
//     type: 'line',
//     data: data,
//     options: {}
//   };

//   const myChart = new Chart(
//     document.getElementById('myChart'),
//     config
//   );
// });
// ================================================================
// Basic Chart.js example [END]
// ================================================================