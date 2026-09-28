const API = "/api";
const $ = (s, r=document) => r.querySelector(s);
const $$ = (s, r=document) => [...r.querySelectorAll(s)];

function niceNumber(v){
  if(typeof v === "number" && Number.isFinite(v)) return Number.isInteger(v) ? String(v) : String(Number(v.toFixed(6)));
  return String(v);
}
function formatResult(v, operation){
  if (Array.isArray(v)) {
    if (v.length === 0) return "No values";
    if (operation === "prime_factors") return v.join(" × ");
    if (operation === "swap_temp" || operation === "swap_no_temp") return `A = ${niceNumber(v[0])}\nB = ${niceNumber(v[1])}`;
    return v.map(niceNumber).join(", ");
  }
  if (v && typeof v === "object") {
    if (Object.prototype.hasOwnProperty.call(v, "sum") && Object.prototype.hasOwnProperty.call(v, "average")) {
      return `Sum: ${niceNumber(v.sum)}\nAverage: ${niceNumber(v.average)}`;
    }
    return Object.entries(v).map(([k,val]) => `${k}: ${niceNumber(val)}`).join("\n");
  }
  return niceNumber(v);
}
function setResult(box, value, error=false, operation=""){
  if(!box) return;
  box.textContent = formatResult(value, operation);
  box.classList.toggle("error", error);
}
function toast(msg, type="info"){
  const t=$( "#toast" ); if(!t) return;
  t.textContent=msg; t.dataset.type=type; t.classList.add("show");
  clearTimeout(window.__toast); window.__toast=setTimeout(()=>t.classList.remove("show"),2200);
}
async function runApi(operation,args,box){
  setResult(box,"Running…",false,operation);
  try{
    const r=await fetch(`${API}/run`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({operation,args})});
    const d=await r.json();
    if(!r.ok || !d.ok) throw new Error(d.error || "The program could not be run.");
    setResult(box,d.result,false,operation); toast("Result ready","success");
  }catch(e){ setResult(box,e.message,true,operation); toast("Start the Python server and try again","error"); }
}

/* Navigation */
const pageNames={dashboard:"Dashboard",calculations:"Calculations",numbers:"Number Operations",factoring:"Factoring",roots:"Square Roots",swapping:"Swapping",advanced:"Advanced",control:"Control Statements",guide:"Topic Guide"};
function openPage(id){
  $$(".page").forEach(p=>p.classList.remove("active"));
  const page=document.getElementById(id); if(page) page.classList.add("active");
  $$("[data-page]").forEach(x=>x.classList.toggle("active",x.dataset.page===id));
  const crumb=$("#crumb"); if(crumb) crumb.textContent=pageNames[id]||id;
  window.scrollTo({top:0,behavior:"smooth"});
}
$$('[data-page]').forEach(b=>b.addEventListener("click",()=>openPage(b.dataset.page)));
$$('[data-go]').forEach(b=>b.addEventListener("click",()=>openPage(b.dataset.go)));

/* Mobile sidebar */
$("#openSidebar")?.addEventListener("click",()=>$("#sidebar")?.classList.add("open"));
$("#closeSidebar")?.addEventListener("click",()=>$("#sidebar")?.classList.remove("open"));

/* Theme */
$("#themeBtn")?.addEventListener("click",()=>{
  document.body.classList.toggle("light");
  localStorage.setItem("theme",document.body.classList.contains("light")?"light":"dark");
});
if(localStorage.getItem("theme")==="light") document.body.classList.add("light");

/* Calculations */
const calc=$("#calculations");
if(calc){
  const s=$("select",calc), i=$("#calcInput",calc), label=$("#calcInputLabel",calc), b=$( ".run-demo",calc), o=$(".result-value",calc);
  const updateCalcInput = () => {
    const isSum = s.value === "sum_average";
    if(label) label.textContent = isSum ? "Numbers" : "Number";
    if(i) {
      i.type = isSum ? "text" : "number";
      i.placeholder = isSum ? "10, 20, 30" : "Enter a number";
    }
  };
  s?.addEventListener("change", updateCalcInput);
  updateCalcInput();
  b?.addEventListener("click",()=>{
    const op=s.value;
    if(op==="sum_average") {
      const raw=i.value.split(",").map(x=>x.trim()).filter(Boolean);
      const numbers=raw.map(Number);
      if(!raw.length || numbers.some(x=>!Number.isFinite(x))) return setResult(o,"Enter numbers like 10, 20, 30.",true);
      runApi(op,{numbers},o);
    } else {
      const n=Number(i.value);
      if(!Number.isFinite(n)) return setResult(o,"Enter a valid number.",true);
      runApi(op,{n},o);
    }
  });
}

/* Number operations */
const nums=$("#numbers");
if(nums){
  const s=$("select",nums), ins=$$("input",nums), b=$( ".run-demo",nums), o=$(".result-value",nums);
  const labels=$$("label",nums);
  const updateNumbers=()=>{
    const base=s.value==="base_conversion";
    if(labels[0]) labels[0].textContent=base ? "Decimal number" : "First number";
    if(labels[1]) labels[1].innerHTML=base ? "Base <small>(2–36)</small>" : "Second number <small>(for GCD)</small>";
    if(ins[1]) ins[1].placeholder=base ? "e.g. 2" : "Optional";
  };
  s?.addEventListener("change",updateNumbers); updateNumbers();
  b?.addEventListener("click",()=>{
    const op=s.value, a=Number(ins[0]?.value), bb=Number(ins[1]?.value);
    if(!Number.isFinite(a)) return setResult(o,"Enter a valid number.",true);
    if((op==="gcd" || op==="base_conversion") && !Number.isFinite(bb)) return setResult(o,op==="gcd"?"Enter the second number.":"Enter a base from 2 to 36.",true);
    const m={reverse:["reverse",{n:a}],count_digits:["count_digits",{n:a}],gcd:["gcd",{a,b:bb}],base_conversion:["base_conversion",{n:a,base:bb}]};
    const item=m[op]; if(item) runApi(item[0],item[1],o);
  });
}

/* Factoring */
const fact=$("#factoring");
if(fact){
  const s=$("select",fact), i=$("input",fact), b=$(".run-demo",fact), o=$(".result-value",fact);
  b?.addEventListener("click",()=>{const n=Number(i.value);runApi(s.value,s.value==="generate_primes"?{limit:n}:{n},o)});
}

/* Square roots */
const roots=$("#roots");
if(roots){
  const s=$("select",roots), i=$("input",roots), b=$(".run-demo",roots), o=$(".result-value",roots);
  b?.addEventListener("click",()=>runApi({newton:"sqrt_newton",long:"sqrt_long",repeated:"sqrt_repeated"}[s.value],{n:Number(i.value)},o));
}

/* Swapping */
const swap=$("#swapping");
if(swap){
  const ins=$$("input",swap), bs=$$(".button-row button",swap), o=$(".result-value",swap);
  bs.forEach((b,index)=>b.addEventListener("click",()=>runApi(index===0?"swap_temp":"swap_no_temp",{a:Number(ins[0].value),b:Number(ins[1].value)},o)));
}

/* Advanced */
const adv=$("#advanced");
if(adv){
  $$(".feature-card",adv).forEach(card=>{
    $(".run-advanced",card)?.addEventListener("click",()=>{
      const v=$$("input",card).map(x=>Number(x.value));
      const box=$(".mini-result",card), op=card.dataset.operation;
      if(op==="large_power") runApi(op,{base:v[0],exponent:v[1]},box);
      else if(op==="pseudo_random") runApi(op,{seed:v[0],low:v[1],high:v[2]},box);
      else runApi(op,{low:v[0],high:v[1]},box);
    });
  });
}

/* Control statements */
const control=$("#control");
if(control){
  const b=$(".run-control",control), s=$(".control-lab select",control), i=$(".control-lab input",control), o=$(".control-result",control);
  b?.addEventListener("click",()=>runApi("control",{mode:s.value,n:Number(i.value)},o));
}

