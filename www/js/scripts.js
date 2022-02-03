var getJSON = function(url, callback) {
  console.log('Loading JSON ...');
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.responseType = 'json';
  xhr.onload = function() {
    var status = xhr.status;
    if (status === 200) {
      console.log('... success! Status ' + status);
      callback(null, xhr.response);
    } else {
      console.log('... error! Status ' + status);
      callback(status, xhr.response);
    }
  };
  xhr.send();
};
