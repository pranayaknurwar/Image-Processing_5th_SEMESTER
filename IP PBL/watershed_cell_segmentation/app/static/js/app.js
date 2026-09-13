const $=s=>document.querySelector(s);
const imgItems=[["original","Original"],["noisy","Noisy"],["filtered","Filtered"],["threshold","Threshold"],["morphology","Morphology"],["distance","Distance Transform"],["markers","Markers"],["segmented","Watershed Output"]];
const form=$("#processForm");
if(form){
 const input=form.querySelector('input[type=file]'), preview=$("#preview");
 input.addEventListener("change",()=>{const f=input.files[0];if(f){preview.src=URL.createObjectURL(f);$("#empty").style.display="none"}});
 form.addEventListener("submit",async e=>{
  e.preventDefault(); $("#status").textContent="Processing…";
  const r=await fetch("/api/process",{method:"POST",body:new FormData(form)}); const d=await r.json();
  if(!r.ok){$("#status").textContent=d.error||"Processing failed";return}
  $("#status").textContent="Done"; $("#results").classList.remove("hidden");
  $("#imageGrid").innerHTML=imgItems.map(([k,t])=>`<div class="image-card"><img src="${d[k]}"><h4>${t}</h4></div>`).join("");
  const vals=[["Cells detected",d.cell_count],["MSE",d.mse],["PSNR (dB)",d.psnr??"N/A"],["SSIM",d.ssim]];
  $("#metricCards").innerHTML=vals.map(x=>`<div class="metric"><span>${x[0]}</span><b>${x[1]}</b></div>`).join("");
  $("#metricNote").textContent=d.segmentation_note;
 });
}
const kf=$("#kernelForm");
if(kf){
 let chart;
 kf.addEventListener("submit",async e=>{
  e.preventDefault();$("#kernelStatus").textContent="Running 4 kernel experiments…";
  const r=await fetch("/api/kernel-experiment",{method:"POST",body:new FormData(kf)});const d=await r.json();
  if(!r.ok){$("#kernelStatus").textContent=d.error;return}
  $("#kernelStatus").textContent="Experiment complete. Values are calculated from the uploaded image.";
  $("#kernelBody").innerHTML=d.results.map(x=>`<tr><td>${x.kernel}</td><td>${x.psnr??"N/A"}</td><td>${x.mse}</td><td>${x.ssim}</td><td>${x.cells}</td></tr>`).join("");
  const ctx=$("#kernelChart"); if(chart)chart.destroy();
  chart=new Chart(ctx,{type:"line",data:{labels:d.results.map(x=>x.kernel),datasets:[{label:"PSNR (dB)",data:d.results.map(x=>x.psnr)}]},options:{responsive:true,maintainAspectRatio:false,scales:{y:{title:{display:true,text:"PSNR (dB)"}},x:{title:{display:true,text:"Kernel Size"}}}}});
 });
}
