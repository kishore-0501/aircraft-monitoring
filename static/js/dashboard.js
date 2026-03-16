let charts={};

// GAUGES
const loadGauge = new JustGage({
    id: "loadGauge",
    value: 0,
    min: 0,
    max: 100,
    title: "Load %",
    levelColors:["#00ff00","#f9c802","#ff0000"]
});

const vibrationGauge = new JustGage({
    id: "vibrationGauge",
    value: 0,
    min: 0,
    max: 10,
    title: "Vibration",
    levelColors:["#00ff00","#f9c802","#ff0000"]
});

async function fetchData(){

const res = await fetch("/api/data");
const data = await res.json();

if(data.length===0) return;

let labels=data.map((_,i)=>i+1);

let temp=data.map(d=>d.temperature);
let rpm=data.map(d=>d.rpm);
let fuel=data.map(d=>d.fuel_flow);
let pressure=data.map(d=>d.pressure);
let vibration=data.map(d=>d.vibration);

drawLine("temperatureChart",labels,temp);
drawLine("rpmChart",labels,rpm);

drawBar("fuelChart",labels,fuel);
drawBar("pressureChart",labels,pressure);

let last=data[data.length-1];

loadGauge.refresh(Math.round(last.engine_load));
vibrationGauge.refresh(last.vibration);
    
}

function drawLine(id,labels,data){

let ctx=document.getElementById(id);

if(ctx.chart){
ctx.chart.data.labels=labels;
ctx.chart.data.datasets[0].data=data;
ctx.chart.update();
return;
}

ctx.chart=new Chart(ctx,{
type:"line",
data:{
labels:labels,
datasets:[{
label:id,
data:data,
borderColor:"#007bff",
fill:false
}]
}
});

}

function drawBar(id,labels,data){

let ctx=document.getElementById(id);

if(ctx.chart){
ctx.chart.data.labels=labels;
ctx.chart.data.datasets[0].data=data;
ctx.chart.update();
return;
}

ctx.chart=new Chart(ctx,{
type:"bar",
data:{
labels:labels,
datasets:[{
data:data,
backgroundColor:"#4fa3ff"
}]
},
options:{plugins:{legend:{display:false}}}
});

}

fetchData();
setInterval(fetchData,2000);