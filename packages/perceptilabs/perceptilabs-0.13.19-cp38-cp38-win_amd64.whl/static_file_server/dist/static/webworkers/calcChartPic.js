self.addEventListener('message', function(message) {
  switch (message.data) {
    case 'close':
      self.close();
      break;
    default:
      const canvasImg = message.data.canvasImg;
      const dataImg = message.data.dataImg;
      if(typeof dataImg.data === 'string') {
        dataImg.data = JSON.parse(dataImg.data);
      }
      dataImg.data.forEach((el, index) => canvasImg.data[index] = el);

      postMessage(canvasImg);
  }
}, false);
