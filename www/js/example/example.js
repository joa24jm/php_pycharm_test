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
      document.getElementById('myExampleChart'),
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

// ================================================================
// Living Room Corner Chart [START]
// ================================================================

new Chart(document.getElementById("livingRoomCornerChart"), {
  type: 'pie',
  data: {
    labels: ["Right Wall", "Floor", "Left Wall"],
    datasets: [{
      label: "",
      backgroundColor: ["#BBBBBB", "#3B2929","#878787"],
      data: [35, 35, 30]
    }]
  },
  options: {
    title: {
      display: true,
      text: 'A graphical visualisation of a living room corner as pie chart.'
    }
  }
});

// ================================================================
// Living Room Corner Chart [END]
// ================================================================