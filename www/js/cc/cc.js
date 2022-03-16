// ================================================================
// Animated Counter [START]
// ================================================================
const json_data_url_2 = '../../json/cc/basic_facts.json';

window.onload = getJSON(json_data_url_2, function(err, json_data) {
  if (err !== null) {
    console.log('Something went wrong: ' + err);
  } else {
    console.log('Basic facts:');
    console.log(json_data);
  }

const counters = document.querySelectorAll('.counter');
const speed = 150; // The lower the slower

counters.forEach(counter => {
	const updateCount = () => {
    // TODO: Parse json data correctly - how to access the right data? n_users, n_countries, n_evaluations
    // console.log("TEST 2:");
    // console.log(counter);
		const target = json_data[counter.id];
		const count = +counter.innerText;

    console.log('TEST');
    console.log(json_data);

		// Lower inc to slow and higher to slow
		const inc = target / speed;

		// console.log(inc);
		// console.log(count);

		// Check if target is reached
		if (count < target) {
			// Add inc to count and output in counter
			counter.innerText = Math.round(count + inc);
			// Call function every ms
			setTimeout(updateCount, 1);
		} else {
			counter.innerText = target;
		}
	};

	updateCount();
});


  });



// ================================================================
// Animated Counter [END]
// ================================================================


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
      options : {
        scales: {
          y: {
            title: {
              display: true,
              text: 'Number of users'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Age range in years'
            }
          }
        }     
      },
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
