import { KokoroTTS } from "https://cdn.jsdelivr.net/npm/kokoro-js@1.2.1/dist/kokoro.web.js";
let tts=null;
self.onmessage=async(event)=>{
 const d=event.data||{};
 try{
  if(d.type==="load"){
   if(tts){self.postMessage({type:"ready"});return;}
   tts=await KokoroTTS.from_pretrained("onnx-community/Kokoro-82M-v1.0-ONNX",{
    dtype:"q8",device:"wasm",
    progress_callback:p=>self.postMessage({type:"progress",status:p?.status||"download",progress:p?.progress||0})
   });
   self.postMessage({type:"ready"});
  }else if(d.type==="generate"){
   if(!tts)throw new Error("Mesin suara belum siap. Muat ulang halaman.");
   const out=await tts.generate(d.text,{voice:d.voice,speed:d.speed});
   const audio=out.audio;
   self.postMessage({type:"audio",audio,sampling_rate:out.sampling_rate},[audio.buffer]);
  }
 }catch(error){self.postMessage({type:"error",message:error?.message||String(error)});}
};