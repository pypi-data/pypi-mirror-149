var masterSocket = null;
var mopidyDevices = []
var mopidy_client = []
var mopidy_connecting = false;

function check_mopidy(resolve) {
  if (!mopidy_connecting && mopidy.playback != undefined && mopidy.tracklist != undefined) {
    resolve()
  }
  else
   setTimeout(function () { check_mopidy(resolve) }, 1000)
}

function mopidy_connected() {
  const promise = new Promise(function (resolve) { check_mopidy(resolve) });
  return promise;
}

function setMopidyEvents(mopidy_cl) {
  mopidy_cl.on("websocket:error", () => {
    mopidy_connecting = true;
  });
  mopidy_cl.on("state:online", () => {
    console.log('mopidy online '+mopidy_client._webSocket.url)
    mopidy_connecting = false;
    playlists = {}
    if (currentPlaylist.length > 0)
      library.showTracklist(currentPlaylist)
  });
  mopidy_cl.on("websocket:close", () => {
    mopidy_connecting = true;
  });

}

function switchDevice(device, sendMessage) {
      mopidyDevice = mopidyDevices[device]
      if (currentWebsocketUrl != mopidyDevice.ws) {
        currentWebsocketUrl = mopidyDevice.ws
        mopidy_connecting = true;
        console.log("waiting reconnect")

        mopidy_client.playback.getState().then( function(state) {
            if (state == "playing" && sendMessage) {
              masterSocket.send(JSON.stringify({message:"activate",name:device}))
            }
            var connectOptions = {callingConvention: 'by-position-or-by-name'}
            connectOptions['webSocketUrl'] = mopidyDevice.ws
            currentWebsocketUrl = mopidyDevice.ws
            console.log(mopidy_connecting)
            mopidy_client = new Mopidy(connectOptions)
            mopidy = mopidy_client
            // initialize events
            setMopidyEvents(mopidy_client)
            initSocketevents()
            if ( syncedProgressTimer != null) 
              syncedProgressTimer.stop()
            syncedProgressTimer = new SyncedProgressTimer(8, mopidy)
            resetSong()
            library.getPlaylists()
            switchContent('current')
        });
      }
}

function updateDevices(devices) {
   mopidyDevices = devices;
   $('#deviceselect').customSelect('empty')
   var anyActive = false;
   for (var device in devices) {
    if (devices[device].active) anyActive = true;
   }
   var n = 0;
   for (var device in devices) {
    var option = $('<option></option>').attr("value", devices[device].name).text(devices[device].name);
    if (devices[device].active || (n == 0 && !anyActive)) {
      option.attr("selected",true)
      switchDevice(device,false)
    }
    $('#deviceselect').customSelect('append',option)
    n++;
   }

   $('#deviceselect').on('change', function(e) {
     console.log(e.target.value);
      var device = e.target.value;
      switchDevice(device,true)
   });


}


function initMasterApi() {
  var loc = window.location;
  if (masterSocket != null) {
    if (masterSocket.readyState == WebSocket.OPEN) {
      return;
    }
    masterSocket.onopen = function (event) {};
  }
  mopidy_client =  mopidy;
  setMopidyEvents(mopidy_client)

  masterSocket = new WebSocket('ws://'+loc.host+'/master/socketapi/ws');
  masterSocket.onmessage = function (event) {
    console.log(event.data)
    msg = JSON.parse(event.data)
    if ( msg.msg == 'devices' ) {
      updateDevices(msg.devices)
    }
  }
  masterSocket.onerror = function (event) {
    $('#devicesist').hide()
  }
  masterSocket.onopen = function (event) {
    masterSocket.send(JSON.stringify({message:'subscribe'}));
    masterSocket.send(JSON.stringify({message:'list'}));
  }
}


