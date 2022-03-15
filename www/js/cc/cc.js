// ================================================================
// Basic Chart.js example [START]
// ================================================================
const json_data_url = '../../json/cc/age_distribution.json';

window.onload = getJSON(json_data_url, function(err, json_data) {
  if (err !== null) {
    console.log('Something went wrong: ' + err);
  } else {
    console.log('JSON Data:');
    console.log(json_data);

    // ================================================
    // START
    // ================================================

    const data = {
      labels: Object.keys(json_data),
      datasets: [{
        label: 'Age Distribution',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgb(54, 162, 235)',
        data: Object.values(json_data),
      }]
    };

    const config = {
      type: 'bar',
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
