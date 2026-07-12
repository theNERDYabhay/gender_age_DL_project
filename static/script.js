const video=document.getElementById('video');
if(video){navigator.mediaDevices.getUserMedia({video:true}).then(s=>video.srcObject=s);}
const btn=document.getElementById('scanBtn');
if(btn){btn.onclick=()=>alert('Connect to /predict endpoint.');}