
const video=document.getElementById("video");
const canvas=document.getElementById("canvas");
const scanBtn=document.getElementById("scanBtn");
const loading=document.getElementById("loading");

async function startCamera(){
    try{
        const stream=await navigator.mediaDevices.getUserMedia({video:true});
        video.srcObject=stream;
    }catch(err){
        alert("Camera access denied: "+err.message);
    }
}

startCamera();

scanBtn.addEventListener("click", async ()=>{
    loading.style.display="block";

    canvas.width=video.videoWidth;
    canvas.height=video.videoHeight;

    const ctx=canvas.getContext("2d");
    ctx.drawImage(video,0,0);

    const blob=await new Promise(resolve=>canvas.toBlob(resolve,"image/jpeg",0.95));

    const formData=new FormData();
    formData.append("image",blob,"capture.jpg");

    try{
        const response=await fetch("/predict",{
            method:"POST",
            body:formData
        });

        const data=await response.json();

        if(data.error){
            alert(data.error);
        }else{
            document.getElementById("gender").textContent=data.gender;
            document.getElementById("age").textContent=data.age;
            document.getElementById("compliment").textContent=data.compliment;
        }
    }catch(e){
        alert("Request failed: "+e.message);
    }

    loading.style.display="none";
});
