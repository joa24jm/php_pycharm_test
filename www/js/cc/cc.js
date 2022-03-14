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

    // ================================================
    // START
    // ================================================
    // Hi Johannes, ab hier bitte deinen Code schreiben.
    // ================================================
    // Notes:
    // - get the data from the `json_data` object
    //
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

    const _ = new Chart(
      document.getElementById('coronaCheckChart'),
      config
    );
    // ================================================
    // END
    // ================================================
  }
});
