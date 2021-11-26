$( document ).ready(function() {

WS_ADDR = "ws://"+window.location.hostname;
WS_PORT = 20022;
socket_opened = false;

function ws_onopen(){
      console.log("Соединение установлено."+WS_ADDR+":"+WS_PORT);
      console.log("send",WS_DATA);
      socket.send(JSON.stringify(WS_DATA));
      socket_opened = true;
}

function ws_onclose(event){
      if (event.wasClean) {
        console.log('Соединение закрыто чисто');
      } else {
        console.log('Обрыв соединения'); // например, "убит" процесс сервера
        //warning("Ошибка соединения");
        socket = null;
      }
      console.log('Код: ' + event.code + ' причина: ' + event.reason);
      socket_opened = false;
}

/*function ws_onmessage(event){
      console.log("Получены данные:" + event.data);
}*/
    function ws_onmessage(event) {
        var data = event.data;
        //foot_message(data);
        WS_MESSAGE = JSON.parse(data); 
        console.log(WS_MESSAGE);
        console.log("Получены данные ",WS_MESSAGE);
        if (WS_MESSAGE["weight"].length>=2){
            var w = WS_MESSAGE.weight[1];
            put_weight(w);
        }
    }

function ws_onerror(error){
      console.log("Ошибка " + error.message);
}

});
