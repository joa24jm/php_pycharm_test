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

/**
 * Get the string or JSON-object content of a file from its path. Parameter asObject determines whether to return an
 * object or not.
 *
 * @param path
 * @param asObject
 * @returns {Promise<any>}
 */
function getFileContent(path, asObject = false) {
  return fetch(path)
    .then(content => asObject ? content.json() : content.text())
    .catch(error => console.error(error));
}

/**
 * Tries to give the value representation back its original data type.
 *
 * @param value
 * @returns {string|number|null}
 */
function applyCorrectDataType(value) {

  if (value === null || value === 'null') {
    return null;
  }

  const numberValue = Number(value);
  if (!isNaN(numberValue)) {
    return numberValue;
  }

  return `${value.replaceAll('"', '')}`;
}


/**
 * A helper function
 *
 * @param inputString
 * @param lineDelimiter
 * @param elementDelimiter
 */
function csvToObject(inputString, {lineDelimiter = '\n', elementDelimiter = ','} = {}) {

  // Get the header row from the topmost CSV-file line of content.
  const firstLineEndIndex = inputString.indexOf(lineDelimiter);
  // Regex according to: https://stackoverflow.com/questions/21105360/regex-find-comma-not-inside-quotes
  const elementDelimiterRegex = new RegExp(`(?!\\B"[^"]*)${elementDelimiter}(?![^"]*"\\B)`);
  const headerElements = inputString
    .slice(0, firstLineEndIndex)
    .split(elementDelimiterRegex)
    .map((elementString) => applyCorrectDataType(elementString));

  // After removing the header from CSV-file content, split up the remaining string into an array (=rows) of arrays (=elements)
  const rowElements = inputString
    .slice(firstLineEndIndex + 1)
    .split(lineDelimiter)
    .map((rowStrings) => {
      return rowStrings.split(elementDelimiter)
        .map((elementString) => applyCorrectDataType(elementString));
    });

  const objectToReturn = {};
  objectToReturn['header'] = headerElements;
  objectToReturn['data'] = rowElements;

  return objectToReturn;
}

/**
 * Retrieve a hex color from d3 Chromatic Scale: Category 10
 * from: https://github.com/d3/d3-scale-chromatic#schemeCategory10
 * Maps a value within a range to the corresponding color.
 *
 * @param value
 * @param minValue
 * @param maxValue
 * @param defaultColor
 * @returns {string}
 */
function getChromaticScaleColor(value = 0, {minValue = 0, maxValue = 100, defaultColor = '#000'} = {}) {
  const colorScale = ['1f77b4', 'ff7f0e', '2ca02c', 'd62728', '9467bd', '8c564b', 'e377c2', '7f7f7f', 'bcbd22', '17becf'];
  if (maxValue <= minValue || value < minValue || value > maxValue) {
    console.error(`Check your min- (${minValue}), max- (${maxValue}) and target (${value}) values!`);
    return defaultColor;
  }

  // Map value to color scale with respect to min- and max-values.
  const distance = Math.abs(minValue - maxValue);
  const colorIndex = Math.floor((value - minValue) / distance * colorScale.length);
  return colorScale[colorIndex];
}
