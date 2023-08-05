const VALID_CHART_TYPES_TO_SUBSAMPLE = ['bar', 'line', 'scatter'];

const isChartDataSubsampled = (seriesObject, xLength) => {
  if (!seriesObject) { return false; }

  if (!VALID_CHART_TYPES_TO_SUBSAMPLE.includes(seriesObject.type)) { return false; }
  // Sample seriesObject
  // data: Array(262)
  // type: "line"
  // x_data: Array(262)

  if (xLength !== seriesObject.data.length) {
    return true;   
  }

  return false;    
}

self.addEventListener('message', function(message) {
  let maxItems = 475;

  switch (message.data) {
    case 'close':
      self.close();
      break;
    default:
      let model = message.data.model;
      let xLength = message.data.xLength;

      const series = model.series && model.series.length > 0 ? model.series[0] : {};
      const isSubsampled = isChartDataSubsampled(series, xLength);

      // if xAxis data is not given
      if (!model.xAxis.data || model.xAxis.data.length === 0) {
        createXAxis(model, xLength, isSubsampled);
        filteredSeriesData(model, isSubsampled);
      }

      postMessage(model);
  }
  function createXAxis(model, xLength, isSubsampled = false) {
    let nFilter;
    const data = model.xAxis.data;

    if (isSubsampled) {
      let dataPoints = [];
      
      if (model.series && model.series.length > 0 && model.series[0]['x_data']) {
        dataPoints = model.series[0]['x_data'];
        delete model.series[0]['x_data'];
      }

      model.xAxis.data = dataPoints;
    } 
    else if(xLength > maxItems*2) {
      nFilter = Math.ceil(xLength / maxItems);
      for (let i = 0; i < xLength; i=i+nFilter) {
        data.push(i);
      }
    }
    else if(xLength > maxItems && xLength <= maxItems*2) {
      nFilter = Math.round(xLength / (xLength - maxItems));
      for (let i = 0; i < xLength; i++) {
        if(i % nFilter) data.push(i);
      }
    }
    else {
      for (let i = 0; i < xLength; i++) {
        data.push(i);
      }
    }
    if(data[0] !== 0) data.unshift(0);
    if(data.length > maxItems) {
      if (data[data.length - 1] !== xLength - 1) data.push(xLength - 1);
    }
  }
  function filteredSeriesData(model, isSubsampled = false) {
    model.series.forEach((chart)=> {
      if (isSubsampled) { return; }

      let newChartData = [];
      model.xAxis.data.forEach((indexPoint)=> {
        newChartData.push(chart.data[indexPoint])
      });

      chart.data = newChartData;
    });
  }
}, false);