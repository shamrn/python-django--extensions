
// When a call comes in, the connection is made from the numbers in the "incomingPhonNum" variable
// When requesting a callback, first the call goes to the specialist, then the connection to the customer
// At input we receive a string with the number "7999999999999:79999999999:79999999999" .
// The last number is the customer number, the rest of the managers (those who will receive the first call)
// Also, if the first manager did not take the call, the call goes to the next manager
// Also implemented is the mail sending the result.


var call1, call2, callIncoming, data, client, managers, manager;
var callerid = ''  // purchased number from voximplant
var incomingPhonNum = ''; // number for incoming call

var email = {
    "host": "",
    "login": "",
    "password": "",
    "email_from": "",
    "email_to": [""]
};

VoxEngine.addEventListener(AppEvents.Started, handleScenarioStart);
VoxEngine.addEventListener(AppEvents.HttpRequest, handleHttpRequest);
VoxEngine.addEventListener(AppEvents.CallAlerting, handleIncoming);


function handleIncoming(e) {
  // Function for incoming call, when there is an incoming call,
  // connect the caller to the number in the "incoming_phon_num" variable

    callIncoming = e.call;
    callIncoming.startEarlyMedia();
    callIncoming.say("Добрый день, Пожалуйста, подождите соединения с филиалом компании <>", Language.RU_RUSSIAN_FEMALE);

    callIncoming.addEventListener(CallEvents.PlaybackFinished, function (e) {
        callConnect = VoxEngine.callPSTN(incomingPhonNum, callerid);

        callConnect.addEventListener(CallEvents.Connected, function (e) {
            Net.sendMail(email.host, email.email_from, email.email_to,
                "VoxImplant <>: Клиент успешно дозвонился в филиал компании, клиент: " + callIncoming.callerid(),
                "Сообщение отправлено автоматически!",
                function () {
                }, {login: email.login, password: email.password});
            // connect two calls with each other - media
            VoxEngine.sendMediaBetween(callIncoming, callConnect);
            // and signalling
            VoxEngine.easyProcess(callIncoming, callConnect);
        });

        callConnect.addEventListener(CallEvents.Failed, function (e) {
            callIncoming.say("К сожалению соединение не может быть установлено", Language.RU_RUSSIAN_FEMALE);
            callIncoming.addEventListener(CallEvents.PlaybackFinished, function (e) {
                VoxEngine.terminate();
            });
            Net.sendMail(email.host, email.email_from, email.email_to,
                "VoxImplant PoolDirector: Входящий звонок, не удалось дозвониться, клиент: " + callIncoming.callerid(),
                "Сообщение отправлено автоматически!",
                function () {
                }, {login: email.login, password: email.password});
        });
        callConnect.addEventListener(CallEvents.Disconnected, function (e) {
            VoxEngine.terminate();
        });
    })
}

function handleHttpRequest(e) {
  // Handle HTTP request sent using media_session_access_url
  VoxEngine.terminate();
}

// managers processing
// -------------------
function handleScenarioStart(e) {
  // Data can be passed to scenario using customData
  // script_custom_data param in StartScenarios HTTP request will be available to scenario as customData
  // in this scenario we will pass number1:number2 string via script_custom_data
  data = VoxEngine.customData().split(":");
  if (data.length < 2) return;
  client = data[data.length-1];
  managers = data.slice(0, data.length-1);

  Net.sendMail(email.host, email.email_from, email.email_to,
               "VoxImplant <>: новый запрос, клиент: " + client + " менеджеры: " + managers,
               "Сообщение отправлено автоматически!",
               function () {}, {login: email.login, password: email.password});

  manager = managers[0];

  // start scenario - calling number 1
  call1 = VoxEngine.callPSTN(manager, callerid);
  // assign event handlers
  call1.addEventListener(CallEvents.Connected, handleCall1Connected);
  call1.addEventListener(CallEvents.Failed, handleCall1Failed);
  call1.addEventListener(CallEvents.Disconnected, function(e) { VoxEngine.terminate(); });
}

function handleCall1Failed(e) {
  // if manager is last of managers - failure, else try next one
  if (managers.indexOf(manager) == managers.length-1) {
    // we can send it to outer world using HTTP request
    Net.sendMail(email.host, email.email_from, email.email_to,
                 "VoxImplant <>: не удалось дозвониться к менеджеру, клиент: " + client + " менеджеры: " + managers,
                 "Сообщение отправлено автоматически!",
                 function () {}, {login: email.login, password: email.password});
  } else {
    // repeat part of handleScenarioStart code
    manager = managers[managers.indexOf(manager)+1];
    // start scenario - calling number 1
    call1 = VoxEngine.callPSTN(manager, callerid);
    // assign event handlers
    call1.addEventListener(CallEvents.Connected, handleCall1Connected);
    call1.addEventListener(CallEvents.Failed, handleCall1Failed);
    call1.addEventListener(CallEvents.Disconnected, function(e) { VoxEngine.terminate(); });
  }

  // failure reason available here
  // var code = e.code, reason = e.reason;
  // Net.httpRequest("http://somewebservice", function(e1) {
  //   // HTTP request info - e1.code, e1.text, e1.data, e1.headers
  //   // terminate session
  //   VoxEngine.terminate();
  // });
}

// client processing
// -----------------
function handleCall1Connected(e) {
  Net.sendMail(email.host, email.email_from, email.email_to,
               "VoxImplant <>: успешно дозвонились к менеджеру, клиент: "+ client +" менеджеры: "+ managers,
               "Сообщение отправлено автоматически!",
               function () {}, {login: email.login, password: email.password});

  // first call connected successfully, play message
  call1.say("Добрый день, это звонок из приложения <>" +
            " Пожалуйста, подождите соединения с клиентом", Language.RU_RUSSIAN_FEMALE);
  call1.addEventListener(CallEvents.PlaybackFinished, function(e1) {
    // after message played - calling client number
    call2 = VoxEngine.callPSTN(client, callerid);
    // assign event handlers
    call2.addEventListener(CallEvents.Connected, handleCall2Connected);
    call2.addEventListener(CallEvents.Failed, function(e) {
        call1.say("К сожалению соединение не может быть установлено", Language.RU_RUSSIAN_FEMALE);
        call1.addEventListener(CallEvents.PlaybackFinished, function(e3) { VoxEngine.terminate(); });
        Net.sendMail(email.host, email.email_from, email.email_to,
                 "VoxImplant <>: не удалось дозвониться к клиенту, клиент: "+ client +" менеджеры: "+ managers,
                 "Сообщение отправлено автоматически!",
                 function () {}, {login: email.login, password: email.password});
      });
    call2.addEventListener(CallEvents.Disconnected, function(e) { VoxEngine.terminate(); });
  });
}

function handleCall2Connected(e) {
  Net.sendMail(email.host, email.email_from, email.email_to,
               "VoxImplant <>: успешно дозвонились к клиенту, клиент: "+ client +" менеджеры: "+ managers,
               "Сообщение отправлено автоматически!",
               function () {}, {login: email.login, password: email.password});

  // connect two calls with each other - media
  VoxEngine.sendMediaBetween(call1, call2);
  // and signalling
  VoxEngine.easyProcess(call1, call2);
}
