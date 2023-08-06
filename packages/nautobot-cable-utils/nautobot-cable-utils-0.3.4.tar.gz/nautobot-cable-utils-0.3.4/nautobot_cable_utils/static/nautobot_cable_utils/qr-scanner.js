const html5QrCode = new Html5Qrcode("qr-reader");
const qrCodeSuccessCallback = (decodedText, decodedResult) => {
            document.getElementsByName("template")[0].value = decodedText;
            html5QrCode.stop();
            document.getElementById("toggle-flash").style.visibility = "hidden";
};
const config = { fps: 10, qrbox: { width: 250, height: 250 } };
var btorch = false;

$( document ).ready(function() {
  // set focus on char field (fix until autofocus function is implemented by source project)
  document.getElementsByName("template")[0].focus()
});

function toggleQrcodeReader() {
    if(html5QrCode.getState() === Html5QrcodeScannerState.SCANNING ||
     html5QrCode.getState() === Html5QrcodeScannerState.PAUSED
    )
    {
        html5QrCode.stop();
        document.getElementById("toggle-flash").style.visibility = "hidden";
    }
    else{
        html5QrCode.start({ facingMode: "environment" }, config, qrCodeSuccessCallback);
        // show up light toggle only after qr scanner has been started
        document.getElementById("toggle-flash").style.visibility = "visible";
    }
}

function toggleTorch() 
{    
  if(html5QrCode.getState() === Html5QrcodeScannerState.SCANNING ||
     html5QrCode.getState() === Html5QrcodeScannerState.PAUSED
    )
  {
    html5QrCode.applyVideoConstraints(
       {
         advanced: [{torch: !btorch}]
       });
  }
  btorch = !btorch;
}