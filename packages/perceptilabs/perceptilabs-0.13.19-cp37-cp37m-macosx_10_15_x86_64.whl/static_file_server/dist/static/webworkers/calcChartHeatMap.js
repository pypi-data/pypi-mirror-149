self.addEventListener('message', function(message) {
  let maxItems = 20;

  switch (message.data) {
    case 'close':
      self.close();
      break;
    default:
      let model = message.data;
      var nFilter;
      let arrValue = model.series[0].data.map((num)=> num[2]);
      let arrX = model.series[0].data.map((num)=> num[0]);
      let arrY = model.series[0].data.map((num)=> num[1]);
      let sizeX = Math.max(...arrX);
      let sizeY = Math.max(...arrY);

      // if(sizeX > maxItems*2 || sizeY > maxItems*2) {
      //   //nFilter = Math.ceil(xLength / maxItems);
      //   //todo нужно переделать модель на   [[],[],[]],
      //   //                                  [[],[],[]],
      //   //                                  [[],[],[]]
      //   //и удалять колонки и ряды
      //   //
      // }
      // else if((sizeX > maxItems && sizeX <= maxItems*2) || (sizeY > maxItems && sizeY <= maxItems*2)) {
      //
      // }
      // else {
      //
      // }
      if(!model.xAxis.data.length) {
        createAxis(model.xAxis.data, sizeX) ;
        createAxis(model.yAxis.data, sizeY) ;
      }
      model.visualMap.min = Math.min(...arrValue);
      model.visualMap.max = Math.max(...arrValue);
      postMessage(model);

    function createAxis(data, length) {
      for (let i = 0; i <= length; i++) {
        data.push(i);
      }
    }
  }
}, false);
