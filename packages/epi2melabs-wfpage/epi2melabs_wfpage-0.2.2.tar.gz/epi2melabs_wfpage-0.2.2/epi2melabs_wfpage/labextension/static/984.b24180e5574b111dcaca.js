"use strict";(self.webpackChunk_epi2melabs_epi2melabs_wfpage=self.webpackChunk_epi2melabs_epi2melabs_wfpage||[]).push([[984],{5984:(e,t,o)=>{o.r(t),o.d(t,{default:()=>ce});var a=o(1189),n=o(1557),r=o(5467),l=o(7970);const i=new(o(8940).LabIcon)({name:"ui-components:labs",svgstr:'\n  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="42" height="51" viewBox="0 0 42 51">\n    <defs>\n        <filter id="Rectangle_1" x="0" y="0" width="42" height="27" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur"/>\n        <feComposite in="SourceGraphic"/>\n        </filter>\n        <filter id="Rectangle_2" x="0" y="24" width="42" height="27" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur-2"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur-2"/>\n        <feComposite in="SourceGraphic"/>\n        </filter>\n        <filter id="Rectangle_3" x="0" y="12" width="28" height="27" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur-3"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur-3"/>\n        <feComposite in="SourceGraphic"/>\n        </filter>\n    </defs>\n    <g id="Component_2_1" data-name="Component 2 – 1" transform="translate(9 6)">\n        <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_1)">\n        <rect id="Rectangle_1-2" data-name="Rectangle 1" width="24" height="9" rx="1" transform="translate(9 6)" fill="#08bbb2"/>\n        </g>\n        <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_2)">\n        <rect id="Rectangle_2-2" data-name="Rectangle 2" width="24" height="9" rx="1" transform="translate(9 30)" fill="#0179a4"/>\n        </g>\n        <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_3)">\n        <rect id="Rectangle_3-2" data-name="Rectangle 3" width="10" height="9" rx="1" transform="translate(9 18)" fill="#fccb10"/>\n        </g>\n    </g>\n  </svg>\n'});var s=o(6271),d=o.n(s),c=o(2950),m=o.n(c);const p=m()((({className:e,title:t,body:o,active:a,tabs:n})=>d().createElement("div",{className:`header-title ${e}`},d().createElement("div",{className:"header-title-contents"},d().createElement("h1",null,t),o,d().createElement("ul",{className:"header-title-tabs"},n.map(((e,t)=>d().createElement("li",{className:`header-title-workflows-link ${t===a?"active":""} ${e.className||""}`},d().createElement("button",{onClick:()=>e.onClick()},e.body)))))))))`
  && {
    max-width: 100%;
    padding: 50px 25px;
    margin: 0 0 50px 0;
    display: flex;
    align-items: center;
    flex-direction: column;
    justify-content: flex-start;
    border-bottom: 1px solid rgba(0, 0, 0, 0.125);
  }

  .header-title-contents {
    width: 100%;
    max-width: 1024px;
    text-align: left;
  }

  .header-title-contents h1 {
    padding: 0 0 25px 0;
  }

  .header-title-contents p {
    max-width: 800px;
  }

  .header-title-tabs {
    padding: 35px 0 5px 0;
    display: flex;
  }

  .header-title-tabs button {
    margin-right: 15px;
    padding: 12px 24px;
    border-radius: 4px;
    border: none;
    display: block;
    font-weight: 500;
    font-size: 13px;
    line-height: 1em;
    transition: 0.2s ease-in-out all;
    background-color: #eee;
    cursor: pointer;
  }

  .header-title-tabs .active button {
    color: white;
    background-color: #00485b;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
  }
`;var b=o(5159);const u="ENCOUNTERED_ERROR",g="COMPLETED_SUCCESSFULLY",f="TERMINATED",h=[g,f,u],w={UNKNOWN:{name:"UNKNOWN",className:"grey"},LAUNCHED:{name:"LAUNCHED",className:"blue"},[u]:{name:"ENCOUNTERED_ERROR",className:"orange"},[g]:{name:"COMPLETED_SUCCESSFULLY",className:"green"},[f]:{name:"TERMINATED",className:"black"}},x=m()((({status:e,className:t})=>d().createElement("div",{className:`status-indicator ${t}`},d().createElement("div",{className:w[e].className}))))`
  > div {
    width: 16px;
    height: 16px;
    padding: 0;
    border-radius: 100%;
    line-height: 18px;
    text-align: center;
    font-size: 10px;
    color: white;
  }

  .blue {
    cursor: pointer;
    background-color: #005c75;
    box-shadow: 0 0 0 rgba(204, 169, 44, 0.4);
    animation: pulse-blue 2s infinite;
  }

  @keyframes pulse-blue {
    0% {
      -moz-box-shadow: 0 0 0 0 rgba(44, 119, 204, 0.4);
      box-shadow: 0 0 0 0 rgba(44, 119, 204, 0.4);
    }
    70% {
      -moz-box-shadow: 0 0 0 10px rgba(44, 119, 204, 0);
      box-shadow: 0 0 0 10px rgba(44, 119, 204, 0);
    }
    100% {
      -moz-box-shadow: 0 0 0 0 rgba(44, 119, 204, 0);
      box-shadow: 0 0 0 0 rgba(44, 119, 204, 0);
    }
  }

  .orange {
    cursor: pointer;
    background-color: #e34040;
    box-shadow: 0 0 0 rgba(23, 187, 117, 0.4);
    animation: pulse-orange 2s infinite;
  }

  @keyframes pulse-orange {
    0% {
      -moz-box-shadow: 0 0 0 0 rgba(255, 140, 0, 0.4);
      box-shadow: 0 0 0 0 rgba(255, 140, 0, 0.4);
    }
    70% {
      -moz-box-shadow: 0 0 0 10px rgba(255, 140, 0, 0);
      box-shadow: 0 0 0 10px rgba(255, 140, 0, 0);
    }
    100% {
      -moz-box-shadow: 0 0 0 0 rgba(255, 140, 0, 0);
      box-shadow: 0 0 0 0 rgba(255, 140, 0, 0);
    }
  }

  .green {
    cursor: pointer;
    background-color: #17bb75;
    box-shadow: 0 0 0 rgba(23, 187, 117, 0.4);
    animation: pulse-green 2s infinite;
  }

  @keyframes pulse-green {
    0% {
      -moz-box-shadow: 0 0 0 0 rgba(23, 187, 117, 0.4);
      box-shadow: 0 0 0 0 rgba(23, 187, 117, 0.4);
    }
    70% {
      -moz-box-shadow: 0 0 0 10px rgba(23, 187, 117, 0);
      box-shadow: 0 0 0 10px rgba(23, 187, 117, 0);
    }
    100% {
      -moz-box-shadow: 0 0 0 0 rgba(23, 187, 117, 0);
      box-shadow: 0 0 0 0 rgba(23, 187, 117, 0);
    }
  }

  .grey {
    background-color: #707070;
  }

  .black {
    background-color: black;
  }
`,k=m()((({className:e})=>d().createElement("span",{className:e},d().createElement("div",{className:"lds-ellipsis"},d().createElement("div",null),d().createElement("div",null),d().createElement("div",null),d().createElement("div",null)))))`
  display: flex;
  align-items: center;

  .lds-ellipsis {
    display: inline-block;
    position: relative;
    width: 80px;
    height: 20px;
  }
  .lds-ellipsis div {
    position: absolute;
    top: 5px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.1);
    animation-timing-function: cubic-bezier(0, 1, 1, 0);
  }
  .lds-ellipsis div:nth-child(1) {
    left: 8px;
    animation: lds-ellipsis1 0.6s infinite;
  }
  .lds-ellipsis div:nth-child(2) {
    left: 8px;
    animation: lds-ellipsis2 0.6s infinite;
  }
  .lds-ellipsis div:nth-child(3) {
    left: 32px;
    animation: lds-ellipsis2 0.6s infinite;
  }
  .lds-ellipsis div:nth-child(4) {
    left: 56px;
    animation: lds-ellipsis3 0.6s infinite;
  }
  @keyframes lds-ellipsis1 {
    0% {
      transform: scale(0);
    }
    100% {
      transform: scale(1);
    }
  }
  @keyframes lds-ellipsis3 {
    0% {
      transform: scale(1);
    }
    100% {
      transform: scale(0);
    }
  }
  @keyframes lds-ellipsis2 {
    0% {
      transform: translate(0, 0);
    }
    100% {
      transform: translate(24px, 0);
    }
  }
`;var y=o(4190),E=o(9155);async function v(e="",t={}){const o=E.ServerConnection.makeSettings(),a=y.URLExt.join(o.baseUrl,"epi2melabs-wfpage",e);let n;try{n=await E.ServerConnection.makeRequest(a,t,o)}catch(e){throw new E.ServerConnection.NetworkError(e)}let r=await n.text();if(r.length>0)try{r=JSON.parse(r)}catch(e){console.log("Not a JSON response body.",n)}if(!n.ok)throw new E.ServerConnection.ResponseError(n,r.message||r);return r}const N=m()((({className:e,title:t,logfile:o,instanceData:a,instanceStatus:n})=>{const[r,l]=(0,s.useState)(null),i=async(e,t)=>{if(e){const o=encodeURIComponent(`${e.path}/${t}`),{contents:a}=await v(`file/${o}?contents=true`);null!==a&&l(a)}};return(0,s.useEffect)((()=>{if(i(a,o),!h.includes(n)){const e=setInterval((()=>i(a,o)),7500);return()=>{i(a,o),clearInterval(e)}}}),[n,o]),d().createElement("div",{className:`instance-logs ${e}`},d().createElement("div",{className:"instance-logs-header"},d().createElement("h3",null,t)),d().createElement("div",{className:"instance-logs-items"},r&&r.length?d().createElement("ul",null,r.map((e=>d().createElement("li",null,d().createElement("p",null,e))))):d().createElement("div",null,d().createElement(k,null))))}))`
  && {
    border-radius: 4px;
    padding: 25px;
    margin: 0 0 50px 0;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    background-color: white;
  }

  .instance-logs-header {
    padding-bottom: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .instance-logs-items {
    max-height: 500px;
    overflow-y: scroll;
    padding: 15px;
    background-color: #f4f4f4;
    border-radius: 4px;
  }

  .instance-logs-items p {
    font-family: monospace;
  }
`;var C=o(9931),S=o(4900);const O=m()((({className:e,instanceData:t,instanceStatus:o,app:a,docTrack:n})=>{const[r,l]=(0,s.useState)([]),i=async e=>{const{curr_dir:t,base_dir:o}=await v("cwd");return`${o.replace(t,"").replace(/^\//,"")}/instances/${e.path.replace(/\\/g,"/").split("/").reverse()[0]}`},c=async e=>{if(e){const t=`${await i(e)}/output`;try{const e=await(await n.services.contents.get(t)).content.filter((e=>"directory"!==e.type));l(e)}catch(e){console.log("Instance outputs not available yet")}}};(0,s.useEffect)((()=>{if(c(t),!h.includes(o)){const e=setInterval((()=>{c(t)}),1e4);return()=>{c(t),clearInterval(e)}}}),[o]);const m=e=>{const t=n.open(e);t&&(t.trusted=!0)},p=(e=>{let t=null;return r.length&&r.forEach((o=>{o.name===`${e.workflow}-report.html`&&(t=o)})),t})(t);return d().createElement("div",{className:`instance-outputs ${e}`},d().createElement("div",{className:"instance-outputs-header"},d().createElement("h3",null,"Output files"),d().createElement("div",null,d().createElement("button",{onClick:()=>t?(async e=>{const t=await i(e);a.commands.execute("filebrowser:go-to-path",{path:t})})(t):""},"Open folder"),p?d().createElement("button",{onClick:()=>m(p.path)},"Open report"):"")),d().createElement("div",{className:"instance-outputs-items"},r.length?d().createElement("ul",null,r.map((e=>d().createElement("li",null,d().createElement("button",{onClick:()=>m(e.path)},d().createElement("h4",null,e.name),d().createElement(C.FontAwesomeIcon,{icon:S.faArrowUpRightFromSquare})))))):h.includes(o)?d().createElement("h4",null,"Workflow has terminated but no outputs are available."):d().createElement("div",null,d().createElement(k,null))))}))`
  && {
    border-radius: 4px;
    padding: 25px;
    margin: 0 0 50px 0;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    background-color: white;
  }

  .instance-outputs-header {
    padding-bottom: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .instance-outputs-header button {
    margin-left: 15px;
    padding: 10px 24px;
    border-radius: 4px;
    border: none;
    font-weight: 500;
    font-size: 13px;
    line-height: 1em;
    transition: 0.2s ease-in-out all;
    background-color: #eee;
    cursor: pointer;
  }

  .instance-outputs-items li button {
    width: 100%;
    padding: 15px 0;
    display: flex;
    border-radius: 0;
    justify-content: space-between;
    align-items: center;
    outline: none;
    background-color: transparent;
    border: none;
    border-top: 1px solid #f2f2f2;
    cursor: pointer;
  }

  .instance-outputs-items li button svg {
    color: #eee;
  }

  .instance-outputs-items li:hover button svg {
    color: #ccc;
  }
`,z=m()((({className:e,instanceData:t})=>{const o=(0,b.useNavigate)(),a=(0,b.useParams)(),[n,r]=(0,s.useState)(null);(0,s.useEffect)((()=>{l(t)}),[]);const l=async e=>{if(e){const t=encodeURIComponent(`${e.path}/params.json`),{contents:o}=await v(`file/${t}?contents=true`);null!==o&&r(o)}};return d().createElement("div",{className:`instance-params ${e}`},d().createElement("div",{className:"instance-params-header"},d().createElement("h3",null,"Instance params"),d().createElement("div",{className:"instance-section-header-controls"},d().createElement("button",{onClick:()=>{t&&o(`/workflows/${t.workflow}/${t.id}`)}},"Rerun workflow"))),d().createElement("div",{className:"instance-params-details"},d().createElement("ul",null,d().createElement("li",null,d().createElement("div",null,d().createElement("p",{className:"preheader"},"Created at"),d().createElement("h4",null,t.updated_at))),d().createElement("li",null,d().createElement("div",null,d().createElement("p",{className:"preheader"},"Unique ID"),d().createElement("h4",null,a.id))))),d().createElement("div",{className:"instance-params-items"},n&&n.length?d().createElement("ul",null,n.map((e=>d().createElement("li",null,d().createElement("p",null,e))))):d().createElement("div",null,d().createElement(k,null))))}))`
  && {
    border-radius: 4px;
    padding: 25px;
    margin: 0 0 50px 0;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    background-color: white;
  }

  .instance-params-header {
    padding-bottom: 25px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .instance-params-header button {
    margin-left: 15px;
    padding: 10px 24px;
    border-radius: 4px;
    border: none;
    font-weight: 500;
    font-size: 13px;
    line-height: 1em;
    transition: 0.2s ease-in-out all;
    background-color: #eee;
    cursor: pointer;
  }

  .instance-params-details ul li {
    padding: 15px 0 0 0;
    margin: 0 0 15px 0;
    text-align: left;
    border-top: 1px solid #f2f2f2;
  }

  .instance-params-details ul li p {
    padding: 0 0 5px 0;
    color: #ccc;
  }

  .instance-params-items {
    max-height: 500px;
    overflow-y: scroll;
    padding: 15px;
    background-color: #f4f4f4;
    border-radius: 4px;
  }

  .instance-params-items p {
    font-family: monospace;
  }
`,j=m()((({className:e,docTrack:t,app:o})=>{const a=(0,b.useNavigate)(),n=(0,b.useParams)(),[r,l]=(0,s.useState)(0),[i,c]=(0,s.useState)(""),[m,u]=(0,s.useState)(null),g=async()=>{const e=await v(`instances/${n.id}`);return u(e),c(e.status),e};if((0,s.useEffect)((()=>{(async()=>{await g()})();const e=setInterval((()=>g()),5e3);return()=>{clearInterval(e)}}),[]),!m)return d().createElement("div",{className:`instance ${e}`},d().createElement("div",{className:"loading-screen"},d().createElement("p",null,"Instance data is loading... (If this screen persists, check connection to jupyterlab server and/or labslauncher)"),d().createElement(k,null)));const f=["LAUNCHED"].includes(i),h=[{body:"Workflow outputs",onClick:()=>l(0),element:d().createElement("div",{className:"tab-contents"},d().createElement(O,{instanceData:m,instanceStatus:i,app:o,docTrack:t}),d().createElement(N,{title:"Workflow logs",logfile:"nextflow.stdout",instanceData:m,instanceStatus:i}))},{body:"Instance details",onClick:()=>l(1),element:d().createElement("div",{className:"tab-contents"},d().createElement(z,{instanceData:m}),d().createElement(N,{title:"Instance logs",logfile:"invoke.stdout",instanceData:m,instanceStatus:i}))},{body:f?"Stop instance":"Delete instance",className:"instance-delete",onClick:()=>(async e=>{const t=await v(`instances/${n.id}`,{method:"DELETE",headers:{"Content-Type":"application/json"},body:JSON.stringify({delete:e})});e&&t.deleted&&a("/workflows")})(!f)}];return d().createElement("div",{className:`instance ${e}`},d().createElement("div",{className:"instance-container"},d().createElement(p,{title:m.name,body:d().createElement("div",{className:"instance-details"},d().createElement("div",{className:"instance-status"},d().createElement(x,{status:i||"UNKNOWN"}),d().createElement("p",null,i)),d().createElement("p",null,m.workflow),d().createElement("p",null,"Last Updated: ",m.updated_at)),active:r,tabs:h}),h[r].element))}))`
  background-color: #f6f6f6;

  .loading-screen {
    display: flex;
    justify-content: center;
    min-height: calc(100vh - 100px);
    align-items: center;
    flex-direction: column;
  }

  .loading-screen p {
    text-align: center;
    max-width: 600px;
    padding-bottom: 15px;
  }

  .instance-container {
    box-sizing: border-box;
    padding: 0 0 50px 0 !important;
  }

  @keyframes fadeInUp {
    from {
      transform: translate3d(0, 40px, 0);
    }

    to {
      transform: translate3d(0, 0, 0);
      opacity: 1;
    }
  }

  .tab-contents {
    box-sizing: border-box;
    width: 100%;
    max-width: calc(1024px + 30px);
    padding: 0 15px;
    margin: 0 auto 25px auto;
    opacity: 0;
    animation-name: fadeInUp;
    animation-duration: 1s;
    animation-fill-mode: both;
  }

  .instance-details {
    display: flex;
    align-items: center;
  }

  .instance-details p {
    padding-left: 15px;
    text-transform: uppercase;
    font-size: 11px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    color: rgba(0, 0, 0, 0.5);
  }

  .instance-status {
    display: flex;
    align-items: center;
  }

  .instance-status p {
    color: black;
    padding-left: 15px;
  }

  .instance-delete {
    margin-left: auto;
  }

  .instance-delete button {
    background-color: #e34040;
    color: white;
    cursor: pointer;
    margin-right: 0;
  }
`;var I=o(7118),R=o.n(I),$=o(2372),_=o(864);const U=m()((({id:e,label:t,format:o,description:a,defaultValue:n,error:r,onChange:l,className:i})=>{const[c,m]=(0,s.useState)(n);return d().createElement("div",{className:`BooleanInput ${i} ${c?"checked":"unchecked"}`},d().createElement("h4",null,t),d().createElement("p",null,a),d().createElement("label",{htmlFor:e},d().createElement("input",{id:e,className:"boolInput",type:"checkbox",defaultChecked:n,onChange:t=>{m(!!t.target.checked),l(e,o,!!t.target.checked)}}),d().createElement("span",null,d().createElement(C.FontAwesomeIcon,{icon:c?S.faCheck:S.faTimes}))),r.length?d().createElement("div",{className:"error"},r.map((e=>d().createElement("p",null,"Error: ",e)))):"")}))`
  h4 {
    padding: 0 0 5px 0;
  }

  p {
    padding: 0 0 10px 0;
  }

  label {
    position: relative;
    display: inline-block;
  }

  label span {
    box-sizing: border-box;
    min-width: 75px;
    margin: 0;
    padding: 15px 25px;
    display: block;

    text-align: center;
    font-size: 16px;
    font-family: monospace;
    letter-spacing: 0.05em;
    line-height: 1em;

    color: #212529;
    background-color: #f8f9fa;
    border: 1px solid rgba(0, 0, 0, 0.125);
    border-radius: 4px;
    outline: none;

    cursor: pointer;
    transition: 0.2s ease-in-out all;
    -moz-appearance: textfield;
  }

  input {
    position: absolute;
    top: 0;
    left: 0;
    opacity: 0;
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }

  label span:hover {
    border-color: #005c75;
    box-shadow: 0 0 0 0.25rem rgb(13 110 253 / 25%);
  }

  input:checked + span {
    background-color: #005c75;
    color: white;
  }
`,L=m()((({id:e,label:t,format:o,description:a,defaultValue:n,choices:r,error:l,onChange:i,className:s})=>d().createElement("div",{className:`SelectInput ${s}`},d().createElement("h4",null,t),d().createElement("p",null,a),d().createElement("label",{htmlFor:e},d().createElement("select",{id:e,onChange:t=>i(e,o,t.target.value)},n?"":d().createElement("option",{className:"placeholder",selected:!0,disabled:!0,hidden:!0,value:"Select an option"},"Select an option"),r.map((e=>d().createElement("option",{key:e.label,selected:!(e.value!==n),value:e.value},e.label))))),l.length?d().createElement("div",{className:"error"},l.map((e=>d().createElement("p",null,"Error: ",e)))):"")))`
  h4 {
    padding: 0 0 5px 0;
  }

  p {
    padding: 0 0 10px 0;
  }

  label {
    display: flex;
  }

  select {
    margin: 0;
    min-width: 50%;
    padding: 15px 25px;

    font-size: 14px;
    line-height: 1em;

    color: #212529;
    background-color: #f8f9fa;
    border: 1px solid rgba(0, 0, 0, 0.125);
    border-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  select:hover {
    border-color: #005c75;
    box-shadow: 0 0 0 0.25rem rgb(13 110 253 / 25%);
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`,T=m()((({id:e,label:t,format:o,description:a,defaultValue:n,minLength:r,maxLength:l,pattern:i,error:s,onChange:c,className:m})=>d().createElement("div",{className:`TextInput ${m}`},d().createElement("h4",null,t),d().createElement("p",null,a),d().createElement("label",{htmlFor:e},d().createElement("input",{id:e,type:"text",placeholder:"Enter a value",defaultValue:n,pattern:i,minLength:r,maxLength:l,onChange:t=>c(e,o,t.target.value)})),s.length?d().createElement("div",{className:"error"},s.map((e=>d().createElement("p",null,"Error: ",e)))):"")))`
  h4 {
    padding: 0 0 5px 0;
  }

  p {
    padding: 0 0 10px 0;
  }

  label {
    display: flex;
  }

  input {
    box-sizing: border-box;
    width: 100%;
    margin: 0;
    padding: 15px 25px;

    font-size: 14px;
    line-height: 1em;

    color: #212529;
    background-color: #f8f9fa;
    border: 1px solid rgba(0, 0, 0, 0.125);
    border-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  input:hover {
    border-color: #005c75;
    box-shadow: 0 0 0 0.25rem rgb(13 110 253 / 25%);
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`,F=e=>{let t;switch(e){case"file-path":t="file";break;case"directory-path":t="directory";break;default:t="path"}return t},D=m()((({id:e,label:t,format:o,description:a,defaultValue:n,pattern:r,error:l,onChange:i,className:c})=>{const[m,p]=(0,s.useState)(""),[b,u]=(0,s.useState)(null),[g,f]=(0,s.useState)("/"),[h,w]=(0,s.useState)([]),[x,k]=(0,s.useState)(!1),y=(0,s.useRef)(null),E=F(o);let N=[];l.length&&(N=[...l]),b&&(N=[b,...N]),(0,s.useEffect)((()=>{(async()=>{const e=await(async e=>{const t=encodeURIComponent(e);return(await v(`directory/${t}?contents=true`,{method:"GET"})).contents})(g);e&&w(e.filter((e=>!("directory"===E&&!e.isdir))).sort(((e,t)=>e.name.localeCompare(t.name))))})()}),[g]);return d().createElement("div",{id:e,className:`FileInput ${c}`},d().createElement("h4",null,t),d().createElement("p",null,a),d().createElement("div",{className:"file-input-container"},d().createElement("label",{htmlFor:e},d().createElement("input",{id:e,ref:y,type:"text",placeholder:"Enter a value",defaultValue:n,pattern:r,onChange:t=>{(async(t,o)=>{if([/http:\/\//,/https:\/\//,/^$/,/s3:\/\//].some((e=>e.test(t))))return u(null),void i(e,o,t);const a=encodeURIComponent(t),n=await v(`${o}/${a}`,{method:"GET"});if(!n.exists)return u(n.error),void i(e,o,"");u(null),i(e,o,t)})(t.target.value,F(o))}})),d().createElement("button",{className:"file-browser-toggle",onClick:()=>k(!x)},"Browse")),x?d().createElement("div",{className:"file-browser"},d().createElement("div",{className:"file-browser-contents"},d().createElement("div",{className:"file-browser-path file-browser-close"},d().createElement("button",{onClick:()=>k(!1)},d().createElement(C.FontAwesomeIcon,{icon:S.faTimes}),m.length?"Close":"Select")),d().createElement("ul",null,"/"!==g?d().createElement("li",{className:"file-browser-path file-browser-back"},d().createElement("button",{onClick:()=>f((e=>{const t=e.split("/").slice(0,-1).join("/");return""===t?"/":t})(g))},d().createElement(C.FontAwesomeIcon,{icon:S.faLevelUpAlt}),"Go Up")):"",h.map((e=>d().createElement("li",{className:"file-browser-path "+(m===e.path?"selected":"")},d().createElement("button",{onClick:()=>((e,t,o)=>{if(e===m)return;if(!t&&"directory"===E)return;if(t&&"file"===E)return;p(e);const a=o.current;if(a){((e,t)=>{var o,a;const n=null===(o=Object.getOwnPropertyDescriptor(e,"value"))||void 0===o?void 0:o.set,r=Object.getPrototypeOf(e),l=null===(a=Object.getOwnPropertyDescriptor(r,"value"))||void 0===a?void 0:a.set;n&&n!==l?null==l||l.call(e,t):null==n||n.call(e,t)})(a,e);const t=new Event("input",{bubbles:!0});a.dispatchEvent(t)}})(e.path,e.isdir,y),onDoubleClick:()=>{return t=e.path,void(e.isdir&&f(t));var t}},d().createElement(C.FontAwesomeIcon,{icon:e.isdir?S.faFolder:S.faFile}),e.name))))))):"",N.length?d().createElement("div",{className:"error"},N.map((e=>d().createElement("p",null,"Error: ",e)))):"")}))`
  h4 {
    padding: 0 0 5px 0;
  }

  p {
    padding: 0 0 10px 0;
  }

  .file-input-container {
    display: flex;
    color: #212529;
    border-radius: 4px;
    border: 1px solid rgba(0, 0, 0, 0.125);
    background-color: #f8f9fa;
  }

  .file-input-container:hover {
    border-color: #005c75;
    box-shadow: 0 0 0 0.25rem rgb(13 110 253 / 25%);
  }

  label {
    width: 100%;
    display: flex;
  }

  input {
    display: block;
    width: 100%;
    box-sizing: border-box;
  }

  input,
  .file-browser-toggle {
    margin: 0;
    padding: 15px 25px;

    font-size: 14px;
    line-height: 1em;

    color: #212529;
    border: 0;
    background-color: transparent;
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  .file-browser-toggle {
    line-height: 1.2em;
    border-radius: 0;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    background-color: rgba(0, 0, 0, 0.125);
    color: #333;
    cursor: pointer;
  }

  .file-browser-toggle:hover {
    background-color: #005c75;
    color: white;
  }

  .file-browser {
    position: fixed;
    z-index: 10000;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    top: 0px;
    left: 0px;
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.35);
    /* max-height: 300px; */
    /* margin: 10px 0 0 0; */
    /* border-radius: 4px; */
    /* background-color: #f3f3f3; */
    /* overflow-y: auto; */
  }

  .file-browser-contents {
    width: 900px;
    /* max-height: 500px; */
    border-radius: 4px;
    overflow-y: auto;
    /* background-color: #f3f3f3; */
    background-color: rgba(255, 255, 255, 0.6);
  }

  .file-browser-contents > ul {
    max-height: 500px;
    overflow-y: auto;
  }

  .file-browser-path button {
    box-sizing: border-box;
    width: 100%;
    padding: 15px 25px;
    display: flex;
    align-items: center;
    text-align: left;
    font-size: 12px;
    font-family: monospace;
    letter-spacing: 0.05em;
    outline: none;
    border: none;
    border-radius: 0;
    border-bottom: 1px solid #f4f4f4;
    cursor: pointer;
  }

  .file-browser-path:nth-child(even) button {
    background-color: #f2f2f2;
  }

  .file-browser-path:last-child button {
    border-bottom: none;
  }

  .file-browser-path button:hover {
    color: #005c75;
  }

  .file-browser-path.selected button {
    background-color: #005c75;
    color: white;
  }

  .file-browser-path.selected button:hover {
    color: white;
  }

  .file-browser-back {
    font-style: italic;
    background-color: rgba(0, 0, 0, 0.1);
  }

  .file-browser-close {
    background-color: transparent;
  }

  .file-browser-path.file-browser-close button {
    display: flex;
    justify-content: end;
    border-radius: 0;
    border-bottom: 2px solid #ccc;
    color: #333;
  }

  .file-browser-path.file-browser-close:hover button {
    background-color: #f2f2f2;
    color: #333;
  }

  .file-browser-path button svg {
    padding: 0 10px 0 0;
    color: lightgray;
    font-size: 1.5em;
  }

  .file-browser-path button:hover svg {
    color: #005c75;
  }

  .file-browser-path.selected button:hover svg {
    color: lightgray;
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`,A=m()((({id:e,label:t,format:o,description:a,defaultValue:n,min:r,max:l,error:i,onChange:s,className:c})=>d().createElement("div",{className:`NumInput ${c}`},d().createElement("h4",null,t),d().createElement("p",null,a),d().createElement("label",{htmlFor:e},d().createElement("input",{id:e,type:"number",defaultValue:n,min:r,max:l,onChange:t=>s(e,o,Number(t.target.value))})),i.length?d().createElement("div",{className:"error"},i.map((e=>d().createElement("p",null,"Error: ",e)))):"")))`
  h4 {
    padding: 0 0 5px 0;
  }

  p {
    padding: 0 0 10px 0;
  }

  label {
    display: flex;
  }

  input {
    margin: 0;
    padding: 15px 25px;

    font-size: 14px;
    line-height: 1em;

    color: #212529;
    background-color: #f8f9fa;
    border: 1px solid rgba(0, 0, 0, 0.125);
    border-radius: 4px;
    outline: none;

    transition: 0.2s ease-in-out all;
  }

  .error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }

  input:hover {
    border-color: #005c75;
    box-shadow: 0 0 0 0.25rem rgb(13 110 253 / 25%);
  }

  input::-webkit-inner-spin-button {
    -webkit-appearance: none;
  }
`,M=(e,t)=>({id:e,label:e,format:t.format||"",description:t.description||t.help_text,defaultValue:t.default}),P=m()((({id:e,schema:t,error:o,onChange:a,className:n})=>d().createElement("div",{className:`parameter ${n}`},((e,t,o,a)=>(e=>"boolean"===e.type)(t)?d().createElement(U,Object.assign({},((e,t)=>({id:e,label:e,format:t.format||"",description:t.description||t.help_text,defaultValue:t.default}))(e,t),{error:o,onChange:a})):(e=>!!e.enum)(t)?d().createElement(L,Object.assign({},((e,t)=>({id:e,label:e,format:t.format||"",description:t.description||t.help_text,defaultValue:t.default,choices:t.enum.map((e=>({value:e,label:e})))}))(e,t),{error:o,onChange:a})):(e=>!("string"!==e.type||!["file-path","directory-path","path"].includes(e.format)))(t)?d().createElement(D,Object.assign({},M(e,t),{error:o,onChange:a})):(e=>"string"===e.type&&!e.enum)(t)?d().createElement(T,Object.assign({},M(e,t),{error:o,onChange:a})):(e=>!!["integer","number"].includes(e.type))(t)?d().createElement(A,Object.assign({},((e,t)=>({id:e,label:e,format:t.format||"",description:t.description||t.help_text,defaultValue:t.default,min:t.minimum,max:t.maximum}))(e,t),{error:o,onChange:a})):d().createElement(T,Object.assign({},M(e,t),{error:o,onChange:a})))(e,t,o,a))))`
  padding: 25px 15px;
`,W=m()((({title:e,fa_icon:t,properties:o,errors:a,initOpen:n,onChange:r,className:l})=>{const[i,c]=(0,s.useState)(n),m=0===Object.keys(a).length;$.library.add(S.fas,_.fab);const p=null==t?void 0:t.split(" ")[1],b=null==t?void 0:t.split(" ")[0],u=(null==p?void 0:p.startsWith("fa-"))?p.split("fa-")[1]:p;return d().createElement("div",{className:`parameter-section ${l}`},d().createElement("div",{className:"parameter-section-container "+(m?"valid":"")},d().createElement("button",{className:"parameter-section-toggle",onClick:()=>c(!i)},d().createElement("h3",null,"string"==typeof t?d().createElement(C.FontAwesomeIcon,{icon:[b,u]}):"",e),d().createElement("div",{className:"parameter-section-toggle-controls"},d().createElement(C.FontAwesomeIcon,{icon:i?S.faCaretUp:S.faCaretDown}),m?d().createElement("div",{className:"parameter-section-toggle-errors valid"},d().createElement(C.FontAwesomeIcon,{icon:S.faCheckCircle})):d().createElement("div",{className:"parameter-section-toggle-errors invalid"},d().createElement(C.FontAwesomeIcon,{icon:S.faTimesCircle})))),d().createElement("ul",{className:"parameter-section-items "+(i?"open":"closed")},Object.entries(o).sort((([,e],[,t])=>e.order-t.order)).map((([e,t])=>d().createElement("li",null,d().createElement(P,{id:e,schema:t,error:a[e]||[],onChange:r})))))))}))`
  && {
    margin: 25px 0;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    background-color: white;
    border-radius: 4px;
  }

  .parameter-section-toggle {
    box-sizing: border-box;
    width: 100%;
    display: flex;
    padding: 25px;
    justify-content: space-between;
    align-items: center;
    border: none;
    outline: none;
    background-color: transparent;
    cursor: pointer;
  }

  .parameter-section-toggle:hover {
    background-color: #f3f3f3;
  }

  .parameter-section-toggle h3 svg {
    margin-right: 15px;
  }

  .parameter-section-toggle-controls {
    display: flex;
  }

  .parameter-section-toggle-controls svg {
    width: 18px;
    height: 18px;
  }

  .parameter-section-toggle-errors {
    display: flex;
    align-items: center;
  }

  .parameter-section-toggle-errors svg {
    margin-left: 5px;
  }

  .parameter-section-toggle-errors.valid svg {
    color: #1d9655;
  }

  .parameter-section-toggle-errors.invalid svg {
    // color: #e34040;
    color: #e11515;
  }

  .parameter-section-toggle-errors.invalid p {
    font-weight: bold;
    color: #e34040;
  }

  .parameter-section-items {
    display: block;
    transition: 0.2s ease-in-out all;
  }

  .parameter-section-items.closed {
    display: none;
  }

  .parameter-section-items.open {
    display: block;
    background-color: #fff;
  }

  .parameter-section-items > li {
    padding: 25px 0;
    width: calc(100% - 50px);
    margin: 0 auto;
    box-sizing: border-box;
    background-color: #fff;
    border-top: 1px solid #f2f2f2;
    color: #212529;
  }
`,B=m()((({className:e,parameterSections:t,parameterErrors:o,parametersValid:a,onChangeParameter:n,instanceName:r,instanceNameError:l,instanceCreateError:i,onChangeInstanceName:s,onClickLaunch:c})=>d().createElement("div",{className:`launch-panel ${e}`},d().createElement("div",{className:"instance-name "+(r?"":"invalid")},d().createElement("input",{id:"worflow-name-input",type:"text",placeholder:"Name your experiment...",onChange:e=>s(e.target.value),maxLength:50}),d().createElement("div",{className:"instance-name-input-errors "+(l||!r?"invalid":"")},l||!r?d().createElement(C.FontAwesomeIcon,{icon:S.faTimesCircle}):d().createElement(C.FontAwesomeIcon,{icon:S.faCheckCircle}))),d().createElement("div",{className:"parameter-sections"},d().createElement("ul",null,t.map(((e,t)=>{return d().createElement("li",null,d().createElement(W,{title:e.title,description:e.description,fa_icon:e.fa_icon,initOpen:!t,properties:e.properties,errors:(a=e.properties,r=o,Object.keys(a).reduce(((e,t)=>Object.prototype.hasOwnProperty.call(r,t)?Object.assign(Object.assign({},e),{[t]:r[t]}):e),{})),onChange:n}));var a,r})))),d().createElement("div",{className:"launch-control "+(a&&r?"active":"inactive")},d().createElement("button",{onClick:()=>c()},"Launch Workflow"),i?d().createElement("div",{className:"error"},d().createElement("p",null,"Error: ",i)):""))))`
  //
  // Instance naming
  //
  .instance-name {
    position: relative;
  }

  .instance-name input {
    box-sizing: border-box;
    width: 100%;
    margin: 0;
    padding: 25px;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    background-color: white;
    border: none;
    border-radius: 4px;
    outline: none;
    transition: 0.2s ease-in-out all;
  }

  .instance-name.invalid input {
    color: #e34040;
  }

  .instance-name-input-errors {
    position: absolute;
    top: 25px;
    right: 25px;
  }

  .instance-name-input-errors svg {
    width: 18px;
    height: 18px;
    color: #1d9655;
  }

  .instance-name-input-errors.invalid svg {
    color: #e34040;
  }

  //
  // Launch control
  //
  .launch-control {
    margin: 15px 0 0 0;
  }

  .launch-control button {
    box-sizing: border-box;
    width: 100%;
    padding: 25px 25px;
    border: 0;
    text-transform: uppercase;
    font-size: 11px;
    border-radius: 4px;
    font-weight: bold;
    line-height: 1em;
    letter-spacing: 0.05em;
    transition: 0.2s ease-in-out all;
    outline: none;
    cursor: pointer;
  }

  .launch-control.active button {
    border: 1px solid #1d9655;
    background-color: #1d9655;
    color: white;
  }
  .launch-control.active button:hover {
    cursor: pointer;
    background-color: white;
    color: #1d9655;
  }
  .launch-control.error p {
    padding: 15px 0 0 0;
    color: #e34040;
  }
`;var G=o(7629),V=o.n(G);const q=m()((({className:e,body:t,icon:o})=>d().createElement("div",{className:e},d().createElement("div",{className:"empty"},d().createElement(C.FontAwesomeIcon,{icon:o}),d().createElement("h4",null,t)))))`
  && {
    margin: 0 auto;
    box-sizing: border-box;
  }

  .empty {
    width: 100%;
    height: 250px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
    background-color: #ffffff;
  }

  .empty svg {
    padding-bottom: 15px;
    color: lightgray;
  }
`,H=m()((({className:e,docs:t})=>(console.log(t),d().createElement("div",{className:`docs-panel ${e}`},t&&0!==Object.keys(t).length?d().createElement("div",{className:"docs-panel-contents markdown-body"},Object.values(t).map((e=>d().createElement(V(),{children:e})))):d().createElement(q,{body:"No documentation available",icon:S.faFolderOpen})))))`
  .docs-panel-contents {
    border-radius: 4px;
    padding: 25px;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    background-color: white;
  }

  .markdown-body {
    -ms-text-size-adjust: 100%;
    -webkit-text-size-adjust: 100%;
    margin: 0;
    color: #24292f;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial,
      sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji';
    font-size: 16px;
    line-height: 1.5;
    word-wrap: break-word;
  }

  .markdown-body h1:hover .anchor .octicon-link:before,
  .markdown-body h2:hover .anchor .octicon-link:before,
  .markdown-body h3:hover .anchor .octicon-link:before,
  .markdown-body h4:hover .anchor .octicon-link:before,
  .markdown-body h5:hover .anchor .octicon-link:before,
  .markdown-body h6:hover .anchor .octicon-link:before {
    width: 16px;
    height: 16px;
    content: ' ';
    display: inline-block;
    background-color: currentColor;
    -webkit-mask-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' version='1.1' aria-hidden='true'><path fill-rule='evenodd' d='M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z'></path></svg>");
    mask-image: url("data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' version='1.1' aria-hidden='true'><path fill-rule='evenodd' d='M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z'></path></svg>");
  }

  .markdown-body details,
  .markdown-body figcaption,
  .markdown-body figure {
    display: block;
  }

  .markdown-body summary {
    display: list-item;
  }

  .markdown-body [hidden] {
    display: none !important;
  }

  .markdown-body a {
    background-color: transparent;
    color: #0969da;
    text-decoration: none;
  }

  .markdown-body a:active,
  .markdown-body a:hover {
    outline-width: 0;
  }

  .markdown-body abbr[title] {
    border-bottom: none;
    text-decoration: underline dotted;
  }

  .markdown-body b,
  .markdown-body strong {
    font-weight: 600;
  }

  .markdown-body dfn {
    font-style: italic;
  }

  .markdown-body h1 {
    margin: 0.67em 0;
    font-weight: 600;
    padding-bottom: 0.3em;
    font-size: 2em;
    border-bottom: 1px solid hsla(210, 18%, 87%, 1);
  }

  .markdown-body mark {
    background-color: #fff8c5;
    color: #24292f;
  }

  .markdown-body small {
    font-size: 90%;
  }

  .markdown-body sub,
  .markdown-body sup {
    font-size: 75%;
    line-height: 0;
    position: relative;
    vertical-align: baseline;
  }

  .markdown-body sub {
    bottom: -0.25em;
  }

  .markdown-body sup {
    top: -0.5em;
  }

  .markdown-body img {
    border-style: none;
    max-width: 100%;
    box-sizing: content-box;
    background-color: #ffffff;
  }

  .markdown-body code,
  .markdown-body kbd,
  .markdown-body pre,
  .markdown-body samp {
    font-family: monospace, monospace;
    font-size: 1em;
  }

  .markdown-body figure {
    margin: 1em 40px;
  }

  .markdown-body hr {
    box-sizing: content-box;
    overflow: hidden;
    background: transparent;
    border-bottom: 1px solid hsla(210, 18%, 87%, 1);
    height: 0.25em;
    padding: 0;
    margin: 24px 0;
    background-color: #d0d7de;
    border: 0;
  }

  .markdown-body input {
    font: inherit;
    margin: 0;
    overflow: visible;
    font-family: inherit;
    font-size: inherit;
    line-height: inherit;
  }

  .markdown-body [type='button'],
  .markdown-body [type='reset'],
  .markdown-body [type='submit'] {
    -webkit-appearance: button;
  }

  .markdown-body [type='button']::-moz-focus-inner,
  .markdown-body [type='reset']::-moz-focus-inner,
  .markdown-body [type='submit']::-moz-focus-inner {
    border-style: none;
    padding: 0;
  }

  .markdown-body [type='button']:-moz-focusring,
  .markdown-body [type='reset']:-moz-focusring,
  .markdown-body [type='submit']:-moz-focusring {
    outline: 1px dotted ButtonText;
  }

  .markdown-body [type='checkbox'],
  .markdown-body [type='radio'] {
    box-sizing: border-box;
    padding: 0;
  }

  .markdown-body [type='number']::-webkit-inner-spin-button,
  .markdown-body [type='number']::-webkit-outer-spin-button {
    height: auto;
  }

  .markdown-body [type='search'] {
    -webkit-appearance: textfield;
    outline-offset: -2px;
  }

  .markdown-body [type='search']::-webkit-search-cancel-button,
  .markdown-body [type='search']::-webkit-search-decoration {
    -webkit-appearance: none;
  }

  .markdown-body ::-webkit-input-placeholder {
    color: inherit;
    opacity: 0.54;
  }

  .markdown-body ::-webkit-file-upload-button {
    -webkit-appearance: button;
    font: inherit;
  }

  .markdown-body a:hover {
    text-decoration: underline;
  }

  .markdown-body hr::before {
    display: table;
    content: '';
  }

  .markdown-body hr::after {
    display: table;
    clear: both;
    content: '';
  }

  .markdown-body table {
    border-spacing: 0;
    border-collapse: collapse;
    display: block;
    width: max-content;
    max-width: 100%;
    overflow: auto;
  }

  .markdown-body td,
  .markdown-body th {
    padding: 0;
  }

  .markdown-body details summary {
    cursor: pointer;
  }

  .markdown-body details:not([open]) > *:not(summary) {
    display: none !important;
  }

  .markdown-body kbd {
    display: inline-block;
    padding: 3px 5px;
    font: 11px ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas,
      Liberation Mono, monospace;
    line-height: 10px;
    color: #24292f;
    vertical-align: middle;
    background-color: #f6f8fa;
    border: solid 1px rgba(175, 184, 193, 0.2);
    border-bottom-color: rgba(175, 184, 193, 0.2);
    border-radius: 6px;
    box-shadow: inset 0 -1px 0 rgba(175, 184, 193, 0.2);
  }

  .markdown-body h1,
  .markdown-body h2,
  .markdown-body h3,
  .markdown-body h4,
  .markdown-body h5,
  .markdown-body h6 {
    margin-top: 24px;
    margin-bottom: 16px;
    font-weight: 600;
    line-height: 1.25;
  }

  .markdown-body h2 {
    font-weight: 600;
    padding-bottom: 0.3em;
    font-size: 1.5em;
    border-bottom: 1px solid hsla(210, 18%, 87%, 1);
  }

  .markdown-body h3 {
    font-weight: 600;
    font-size: 1.25em;
  }

  .markdown-body h4 {
    font-weight: 600;
    font-size: 1em;
  }

  .markdown-body h5 {
    font-weight: 600;
    font-size: 0.875em;
  }

  .markdown-body h6 {
    font-weight: 600;
    font-size: 0.85em;
    color: #57606a;
  }

  .markdown-body p {
    margin-top: 0;
    margin-bottom: 10px;
  }

  .markdown-body blockquote {
    margin: 0;
    padding: 0 1em;
    color: #57606a;
    border-left: 0.25em solid #d0d7de;
  }

  .markdown-body ul,
  .markdown-body ol {
    margin-top: 0;
    margin-bottom: 0;
    padding-left: 2em;
  }

  .markdown-body ol ol,
  .markdown-body ul ol {
    list-style-type: lower-roman;
  }

  .markdown-body ul ul ol,
  .markdown-body ul ol ol,
  .markdown-body ol ul ol,
  .markdown-body ol ol ol {
    list-style-type: lower-alpha;
  }

  .markdown-body dd {
    margin-left: 0;
  }

  .markdown-body tt,
  .markdown-body code {
    font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas,
      Liberation Mono, monospace;
    font-size: 12px;
  }

  .markdown-body pre {
    margin-top: 0;
    margin-bottom: 0;
    font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, Consolas,
      Liberation Mono, monospace;
    font-size: 12px;
    word-wrap: normal;
  }

  .markdown-body .octicon {
    display: inline-block;
    overflow: visible !important;
    vertical-align: text-bottom;
    fill: currentColor;
  }

  .markdown-body ::placeholder {
    color: #6e7781;
    opacity: 1;
  }

  .markdown-body input::-webkit-outer-spin-button,
  .markdown-body input::-webkit-inner-spin-button {
    margin: 0;
    -webkit-appearance: none;
    appearance: none;
  }

  .markdown-body .pl-c {
    color: #6e7781;
  }

  .markdown-body .pl-c1,
  .markdown-body .pl-s .pl-v {
    color: #0550ae;
  }

  .markdown-body .pl-e,
  .markdown-body .pl-en {
    color: #8250df;
  }

  .markdown-body .pl-smi,
  .markdown-body .pl-s .pl-s1 {
    color: #24292f;
  }

  .markdown-body .pl-ent {
    color: #116329;
  }

  .markdown-body .pl-k {
    color: #cf222e;
  }

  .markdown-body .pl-s,
  .markdown-body .pl-pds,
  .markdown-body .pl-s .pl-pse .pl-s1,
  .markdown-body .pl-sr,
  .markdown-body .pl-sr .pl-cce,
  .markdown-body .pl-sr .pl-sre,
  .markdown-body .pl-sr .pl-sra {
    color: #0a3069;
  }

  .markdown-body .pl-v,
  .markdown-body .pl-smw {
    color: #953800;
  }

  .markdown-body .pl-bu {
    color: #82071e;
  }

  .markdown-body .pl-ii {
    color: #f6f8fa;
    background-color: #82071e;
  }

  .markdown-body .pl-c2 {
    color: #f6f8fa;
    background-color: #cf222e;
  }

  .markdown-body .pl-sr .pl-cce {
    font-weight: bold;
    color: #116329;
  }

  .markdown-body .pl-ml {
    color: #3b2300;
  }

  .markdown-body .pl-mh,
  .markdown-body .pl-mh .pl-en,
  .markdown-body .pl-ms {
    font-weight: bold;
    color: #0550ae;
  }

  .markdown-body .pl-mi {
    font-style: italic;
    color: #24292f;
  }

  .markdown-body .pl-mb {
    font-weight: bold;
    color: #24292f;
  }

  .markdown-body .pl-md {
    color: #82071e;
    background-color: #ffebe9;
  }

  .markdown-body .pl-mi1 {
    color: #116329;
    background-color: #dafbe1;
  }

  .markdown-body .pl-mc {
    color: #953800;
    background-color: #ffd8b5;
  }

  .markdown-body .pl-mi2 {
    color: #eaeef2;
    background-color: #0550ae;
  }

  .markdown-body .pl-mdr {
    font-weight: bold;
    color: #8250df;
  }

  .markdown-body .pl-ba {
    color: #57606a;
  }

  .markdown-body .pl-sg {
    color: #8c959f;
  }

  .markdown-body .pl-corl {
    text-decoration: underline;
    color: #0a3069;
  }

  .markdown-body [data-catalyst] {
    display: block;
  }

  .markdown-body g-emoji {
    font-family: 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';
    font-size: 1em;
    font-style: normal !important;
    font-weight: 400;
    line-height: 1;
    vertical-align: -0.075em;
  }

  .markdown-body g-emoji img {
    width: 1em;
    height: 1em;
  }

  .markdown-body::before {
    display: table;
    content: '';
  }

  .markdown-body::after {
    display: table;
    clear: both;
    content: '';
  }

  .markdown-body > *:first-child {
    margin-top: 0 !important;
  }

  .markdown-body > *:last-child {
    margin-bottom: 0 !important;
  }

  .markdown-body a:not([href]) {
    color: inherit;
    text-decoration: none;
  }

  .markdown-body .absent {
    color: #cf222e;
  }

  .markdown-body .anchor {
    float: left;
    padding-right: 4px;
    margin-left: -20px;
    line-height: 1;
  }

  .markdown-body .anchor:focus {
    outline: none;
  }

  .markdown-body p,
  .markdown-body blockquote,
  .markdown-body ul,
  .markdown-body ol,
  .markdown-body dl,
  .markdown-body table,
  .markdown-body pre,
  .markdown-body details {
    margin-top: 0;
    margin-bottom: 16px;
  }

  .markdown-body blockquote > :first-child {
    margin-top: 0;
  }

  .markdown-body blockquote > :last-child {
    margin-bottom: 0;
  }

  .markdown-body sup > a::before {
    content: '[';
  }

  .markdown-body sup > a::after {
    content: ']';
  }

  .markdown-body h1 .octicon-link,
  .markdown-body h2 .octicon-link,
  .markdown-body h3 .octicon-link,
  .markdown-body h4 .octicon-link,
  .markdown-body h5 .octicon-link,
  .markdown-body h6 .octicon-link {
    color: #24292f;
    vertical-align: middle;
    visibility: hidden;
  }

  .markdown-body h1:hover .anchor,
  .markdown-body h2:hover .anchor,
  .markdown-body h3:hover .anchor,
  .markdown-body h4:hover .anchor,
  .markdown-body h5:hover .anchor,
  .markdown-body h6:hover .anchor {
    text-decoration: none;
  }

  .markdown-body h1:hover .anchor .octicon-link,
  .markdown-body h2:hover .anchor .octicon-link,
  .markdown-body h3:hover .anchor .octicon-link,
  .markdown-body h4:hover .anchor .octicon-link,
  .markdown-body h5:hover .anchor .octicon-link,
  .markdown-body h6:hover .anchor .octicon-link {
    visibility: visible;
  }

  .markdown-body h1 tt,
  .markdown-body h1 code,
  .markdown-body h2 tt,
  .markdown-body h2 code,
  .markdown-body h3 tt,
  .markdown-body h3 code,
  .markdown-body h4 tt,
  .markdown-body h4 code,
  .markdown-body h5 tt,
  .markdown-body h5 code,
  .markdown-body h6 tt,
  .markdown-body h6 code {
    padding: 0 0.2em;
    font-size: inherit;
  }

  .markdown-body ul.no-list,
  .markdown-body ol.no-list {
    padding: 0;
    list-style-type: none;
  }

  .markdown-body ol[type='1'] {
    list-style-type: decimal;
  }

  .markdown-body ol[type='a'] {
    list-style-type: lower-alpha;
  }

  .markdown-body ol[type='i'] {
    list-style-type: lower-roman;
  }

  .markdown-body div > ol:not([type]) {
    list-style-type: decimal;
  }

  .markdown-body ul ul,
  .markdown-body ul ol,
  .markdown-body ol ol,
  .markdown-body ol ul {
    margin-top: 0;
    margin-bottom: 0;
  }

  .markdown-body li > p {
    margin-top: 16px;
  }

  .markdown-body li + li {
    margin-top: 0.25em;
  }

  .markdown-body dl {
    padding: 0;
  }

  .markdown-body dl dt {
    padding: 0;
    margin-top: 16px;
    font-size: 1em;
    font-style: italic;
    font-weight: 600;
  }

  .markdown-body dl dd {
    padding: 0 16px;
    margin-bottom: 16px;
  }

  .markdown-body table th {
    font-weight: 600;
  }

  .markdown-body table th,
  .markdown-body table td {
    padding: 6px 13px;
    border: 1px solid #d0d7de;
  }

  .markdown-body table tr {
    background-color: #ffffff;
    border-top: 1px solid hsla(210, 18%, 87%, 1);
  }

  .markdown-body table tr:nth-child(2n) {
    background-color: #f6f8fa;
  }

  .markdown-body table img {
    background-color: transparent;
  }

  .markdown-body img[align='right'] {
    padding-left: 20px;
  }

  .markdown-body img[align='left'] {
    padding-right: 20px;
  }

  .markdown-body .emoji {
    max-width: none;
    vertical-align: text-top;
    background-color: transparent;
  }

  .markdown-body span.frame {
    display: block;
    overflow: hidden;
  }

  .markdown-body span.frame > span {
    display: block;
    float: left;
    width: auto;
    padding: 7px;
    margin: 13px 0 0;
    overflow: hidden;
    border: 1px solid #d0d7de;
  }

  .markdown-body span.frame span img {
    display: block;
    float: left;
  }

  .markdown-body span.frame span span {
    display: block;
    padding: 5px 0 0;
    clear: both;
    color: #24292f;
  }

  .markdown-body span.align-center {
    display: block;
    overflow: hidden;
    clear: both;
  }

  .markdown-body span.align-center > span {
    display: block;
    margin: 13px auto 0;
    overflow: hidden;
    text-align: center;
  }

  .markdown-body span.align-center span img {
    margin: 0 auto;
    text-align: center;
  }

  .markdown-body span.align-right {
    display: block;
    overflow: hidden;
    clear: both;
  }

  .markdown-body span.align-right > span {
    display: block;
    margin: 13px 0 0;
    overflow: hidden;
    text-align: right;
  }

  .markdown-body span.align-right span img {
    margin: 0;
    text-align: right;
  }

  .markdown-body span.float-left {
    display: block;
    float: left;
    margin-right: 13px;
    overflow: hidden;
  }

  .markdown-body span.float-left span {
    margin: 13px 0 0;
  }

  .markdown-body span.float-right {
    display: block;
    float: right;
    margin-left: 13px;
    overflow: hidden;
  }

  .markdown-body span.float-right > span {
    display: block;
    margin: 13px auto 0;
    overflow: hidden;
    text-align: right;
  }

  .markdown-body code,
  .markdown-body tt {
    padding: 0.2em 0.4em;
    margin: 0;
    font-size: 85%;
    background-color: rgba(175, 184, 193, 0.2);
    border-radius: 6px;
  }

  .markdown-body code br,
  .markdown-body tt br {
    display: none;
  }

  .markdown-body del code {
    text-decoration: inherit;
  }

  .markdown-body pre code {
    font-size: 100%;
  }

  .markdown-body pre > code {
    padding: 0;
    margin: 0;
    word-break: normal;
    white-space: pre;
    background: transparent;
    border: 0;
  }

  .markdown-body .highlight {
    margin-bottom: 16px;
  }

  .markdown-body .highlight pre {
    margin-bottom: 0;
    word-break: normal;
  }

  .markdown-body .highlight pre,
  .markdown-body pre {
    padding: 16px;
    overflow: auto;
    font-size: 85%;
    line-height: 1.45;
    background-color: #f6f8fa;
    border-radius: 6px;
  }

  .markdown-body pre code,
  .markdown-body pre tt {
    display: inline;
    max-width: auto;
    padding: 0;
    margin: 0;
    overflow: visible;
    line-height: inherit;
    word-wrap: normal;
    background-color: transparent;
    border: 0;
  }

  .markdown-body .csv-data td,
  .markdown-body .csv-data th {
    padding: 5px;
    overflow: hidden;
    font-size: 12px;
    line-height: 1;
    text-align: left;
    white-space: nowrap;
  }

  .markdown-body .csv-data .blob-num {
    padding: 10px 8px 9px;
    text-align: right;
    background: #ffffff;
    border: 0;
  }

  .markdown-body .csv-data tr {
    border-top: 0;
  }

  .markdown-body .csv-data th {
    font-weight: 600;
    background: #f6f8fa;
    border-top: 0;
  }

  .markdown-body .footnotes {
    font-size: 12px;
    color: #57606a;
    border-top: 1px solid #d0d7de;
  }

  .markdown-body .footnotes ol {
    padding-left: 16px;
  }

  .markdown-body .footnotes li {
    position: relative;
  }

  .markdown-body .footnotes li:target::before {
    position: absolute;
    top: -8px;
    right: -8px;
    bottom: -8px;
    left: -24px;
    pointer-events: none;
    content: '';
    border: 2px solid #0969da;
    border-radius: 6px;
  }

  .markdown-body .footnotes li:target {
    color: #24292f;
  }

  .markdown-body .footnotes .data-footnote-backref g-emoji {
    font-family: monospace;
  }

  .markdown-body .task-list-item {
    list-style-type: none;
  }

  .markdown-body .task-list-item label {
    font-weight: 400;
  }

  .markdown-body .task-list-item.enabled label {
    cursor: pointer;
  }

  .markdown-body .task-list-item + .task-list-item {
    margin-top: 3px;
  }

  .markdown-body .task-list-item .handle {
    display: none;
  }

  .markdown-body .task-list-item-checkbox {
    margin: 0 0.2em 0.25em -1.6em;
    vertical-align: middle;
  }

  .markdown-body .contains-task-list:dir(rtl) .task-list-item-checkbox {
    margin: 0 -1.6em 0.25em 0.2em;
  }

  .markdown-body ::-webkit-calendar-picker-indicator {
    filter: invert(50%);
  }
`;const Y=m()((({className:e})=>{const t=(0,b.useParams)(),o=(0,b.useNavigate)(),[a,n]=(0,s.useState)(),[r,l]=(0,s.useState)({}),[i,c]=(0,s.useState)(!1),[m,u]=(0,s.useState)({}),[g,f]=(0,s.useState)([]),[h,w]=(0,s.useState)(null),[x,k]=(0,s.useState)(null),[y,E]=(0,s.useState)(null),[N,C]=(0,s.useState)("animated"),[S,O]=(0,s.useState)(0);(0,s.useEffect)((()=>{(async()=>{const e=await(async()=>await v(`workflows/${t.name}`))();n(e);const o=await(async e=>{if(e){const{path:t}=await v(`instances/${e}`),o=encodeURIComponent(`${t}/params.json`),{exists:a,contents:n}=await v(`file/${o}?contents=true`);return a?JSON.parse(n.join("")):null}})(t.instance_id);l(o||e.defaults);const a=Object.values(e.schema.definitions).map((e=>{return Object.assign(Object.assign({},e),{properties:(t=e.properties,Object.entries(t).filter((([e,t])=>!t.hidden&&"out_dir"!==e)).reduce(((e,t)=>Object.assign({[t[0]]:t[1]},e)),{}))});var t})).filter((e=>0!==Object.keys(e.properties).length));if(o){const e=((e,t)=>e.map((e=>Object.assign(Object.assign({},e),{properties:Object.entries(e.properties).reduce(((e,o)=>Object.assign({[o[0]]:Object.assign(Object.assign({},o[1]),{default:t[o[0]]||o[1].default})},e)),{})}))))(a,o);f(e)}else f(a)})()}),[]),(0,s.useEffect)((()=>{if(a){const{valid:e,errors:t}=function(e,t){const o=new(R())({allErrors:!0,strictSchema:!1,verbose:!0}).compile(t);return{valid:o(e),errors:o.errors}}(r,a.schema);u(e?{}:(e=>{const t={};return e.forEach((e=>{Object.values(e.params).forEach((o=>{t[o]=[...t[o]||[],e.message||""]}))})),t})(t)),c(e)}}),[r]);const z=new RegExp("^[-0-9A-Za-z_ ]+$"),j=[{body:"Launch workflow",onClick:()=>O(0),element:d().createElement("div",{className:`tab-contents ${N}`,onAnimationEnd:()=>C("")},d().createElement(B,{parameterSections:g,parameterErrors:m,parametersValid:i,onChangeParameter:(e,t,o)=>{if(""!==o)l(Object.assign(Object.assign({},r),{[e]:o}));else{const t=r,o=e,a=(t[o],function(e,t){var o={};for(var a in e)Object.prototype.hasOwnProperty.call(e,a)&&t.indexOf(a)<0&&(o[a]=e[a]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols){var n=0;for(a=Object.getOwnPropertySymbols(e);n<a.length;n++)t.indexOf(a[n])<0&&Object.prototype.propertyIsEnumerable.call(e,a[n])&&(o[a[n]]=e[a[n]])}return o}(t,["symbol"==typeof o?o:o+""]));l(a)}},instanceName:y,instanceNameError:h,instanceCreateError:x,onChangeInstanceName:e=>""===e?(E(null),void w("An instance name cannot be empty")):z.test(e)?(E(e),void w(null)):(E(null),void w("An instance name can only contain dashes, underscores, spaces, letters and numbers")),onClickLaunch:async()=>{if(!i||!y)return;const{created:e,instance:a,error:n}=await v("instances",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(Object.assign({workflow:t.name,params:r},y?{name:y}:{}))});n&&k(n),e&&o(`/instances/${a.id}`)}}))},{body:"Documentation",onClick:()=>O(1),element:d().createElement("div",{className:"tab-contents animated"},d().createElement(H,{docs:null==a?void 0:a.docs}))}];return a?d().createElement("div",{className:`workflow ${e}`},d().createElement("div",{className:"workflow-container"},d().createElement(p,{title:a.name,body:d().createElement("p",{className:"large"},a.desc),active:S,tabs:j}),j[S].element)):d().createElement(d().Fragment,null)}))`
  background-color: #f6f6f6;

  .workflow-container {
    box-sizing: border-box;
    padding: 0 0 50px 0 !important;
  }

  @keyframes fadeInUp {
    from {
      transform: translate3d(0, 40px, 0);
    }

    to {
      transform: translate3d(0, 0, 0);
      opacity: 1;
    }
  }

  .tab-contents {
    width: 100%;
    padding: 0 15px;
    box-sizing: border-box;
    max-width: calc(1024px + 30px);
    margin: 0 auto 25px auto;
  }

  .animated {
    opacity: 0;
    animation-name: fadeInUp;
    animation-duration: 1s;
    animation-fill-mode: both;
  }
`;var J=o(5131),K=o.n(J);const Z=m()((({path:e,onClick:t,docTrack:o,buttonText:a,className:n})=>{const[r,l]=(0,s.useState)([]),i=async e=>{l(await c(e,o))};(0,s.useEffect)((()=>{i(e);const t=t=>{i(e)},a=o.services.contents.fileChanged;return a.connect(t),()=>{a.disconnect(t)}}),[e]);const c=async(e,t)=>(await(async(e,t)=>(await Promise.all((await t.services.contents.get(e)).content.map((e=>"directory"===e.type?null:e)))).filter((e=>!!e)))(e,t)).filter((e=>e.path.endsWith(".ipynb"))).map((e=>({name:e.name,path:e.path,last_modified:e.last_modified})));return 0===r.length?d().createElement("div",{className:`notebooks-list ${n}`},d().createElement(q,{body:"There are no notebooks to display",icon:S.faBookOpen})):d().createElement("div",{className:`notebooks-list ${n}`},d().createElement("ul",null,r.map((e=>{return d().createElement("li",null,d().createElement("div",{className:"notebook"},d().createElement("button",{className:"notebook-button",onClick:()=>t(e.path,o)},d().createElement("div",{className:"notebook-header"},d().createElement(C.FontAwesomeIcon,{icon:S.faBook})),d().createElement("div",{className:"notebook-details"},d().createElement("div",{className:"notebook-name"},d().createElement("p",{className:"preheader"},"Notebook name"),d().createElement("h3",{className:"large"},(e=>e.split("/").reverse()[0].split("_").join(" ").split(".ipynb").join(""))(e.path))),d().createElement("div",{className:"notebook-modified"},d().createElement("p",{className:"preheader"},"Last modified"),d().createElement("h4",null,(a=e.last_modified,K()(a).format("MMMM Do YYYY, h:mm:ss a"))))))));var a}))))}))`
  && {
    max-width: calc(1024px + 30px);
    padding: 0 15px 15px 15px;
    margin: 0 auto;
    box-sizing: border-box;
  }

  > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-template-rows: minmax(min-content, max-content);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    list-style: none;
  }

  .notebook {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }

  .notebook-button {
    outline: none;
    border: none;
    background-color: transparent;
    cursor: pointer;
  }

  .notebook-header {
    box-sizing: border-box;
    width: 100%;
    padding: 25px 25px 0;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    border-radius: 4px;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
  }

  .notebook-header svg {
    padding: 15px 16px;
    border-radius: 50px;
    background-color: transparent;
    border: 2px solid #e65100;
    color: #e65100;
  }

  .notebook-details {
    padding: 25px 25px 25px 25px;
    text-align: left;
  }

  .notebook-details p {
    padding: 0 0 5px 0;
    color: #ccc;
  }

  .notebook-name {
    padding: 0 0 10px 0;
    margin: 0 0 15px 0;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-bottom: 1px solid #f2f2f2;
  }
`,Q=m()((({className:e,docTrack:t,templateDir:o,workDir:a})=>{const[n,r]=(0,s.useState)(0),l=[{body:"Notebooks",onClick:()=>r(0),element:d().createElement("div",{className:"tab-contents"},d().createElement(Z,{path:o,onClick:async(e,t)=>{await t.copy(e,a).then((o=>{t.open(e)}))},docTrack:t,buttonText:"Open notebook"}))},{body:"Notebook history",onClick:()=>r(1),element:d().createElement("div",{className:"tab-contents"},d().createElement(Z,{path:a,onClick:(e,t)=>{t.open(e)},docTrack:t,buttonText:"Open notebook"}))}];return d().createElement("div",{className:`index-panel ${e}`},d().createElement(p,{title:"EPI2ME Labs Notebooks",body:d().createElement("p",{className:"large"},"EPI2ME Labs maintains a growing collection of notebooks on a range of topics from basic quality control to genome assembly. These are free free and open to use by anyone."),active:n,tabs:l}),l[n].element)}))`
  && {
    background-color: #f6f6f6;
    padding-bottom: 50px;
  }

  @keyframes fadeInUp {
    from {
      transform: translate3d(0, 40px, 0);
    }

    to {
      transform: translate3d(0, 0, 0);
      opacity: 1;
    }
  }

  .tab-contents {
    opacity: 0;
    animation-name: fadeInUp;
    animation-duration: 1s;
    animation-fill-mode: both;
  }
`,X=m()((({className:e})=>{const[t,o]=(0,s.useState)([]);return(0,s.useEffect)((()=>{(async()=>{const e=await v("workflows");o(Object.values(e))})()}),[]),0===t.length?d().createElement("div",{className:`workflows-list ${e}`},d().createElement(q,{body:"No workflows installed",icon:S.faFolderOpen})):d().createElement("div",{className:`workflows-list ${e}`},d().createElement("ul",null,t.map((e=>d().createElement("li",null,d().createElement("div",{className:"workflow"},d().createElement(b.Link,{className:"workflow-link",to:`/workflows/${e.name}`},d().createElement("div",{className:"workflow-header"},d().createElement(C.FontAwesomeIcon,{icon:S.faDna})),d().createElement("div",{className:"workflow-details"},d().createElement("div",{className:"workflow-name"},d().createElement("p",{className:"preheader"},"Workflow name"),d().createElement("h3",{className:"large"},e.name)),d().createElement("div",{className:"workflow-version"},d().createElement("p",{className:"preheader"},"Workflow version"),d().createElement("h4",null,e.defaults.wfversion))))))))))}))`
  && {
    max-width: calc(1024px + 30px);
    padding: 0 15px 15px 15px;
    margin: 0 auto;
    box-sizing: border-box;
  }

  > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    grid-template-rows: minmax(min-content, max-content);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    list-style: none;
  }

  .workflow {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }

  .workflow-header {
    box-sizing: border-box;
    width: 100%;
    padding: 25px 25px 0;
    display: flex;
    align-items: center;
    justify-content: flex-start;
    border-radius: 4px;
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
  }

  .workflow-header svg {
    padding: 15px 16px;
    border-radius: 50px;
    background-color: transparent;
    border: 2px solid #00485b;
    color: #00485b;
  }

  .workflow-details {
    padding: 25px 25px 25px 25px;
    text-align: left;
  }

  .workflow-details p {
    padding: 0 0 5px 0;
    color: #ccc;
  }

  .workflow-name {
    padding: 0 0 10px 0;
    margin: 0 0 15px 0;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-bottom: 1px solid #f2f2f2;
  }
`,ee=m()((({className:e,onlyTracked:t})=>{const[o,a]=(0,s.useState)([]),[n,r]=(0,s.useState)([]);(0,s.useEffect)((()=>{(async()=>{const e=await v("instances"),t=Object.values(e),o=t.filter((e=>["UNKNOWN","LAUNCHED"].includes(e.status)));a(t),r(o)})()}),[]),(0,s.useEffect)((()=>{const e=setInterval((()=>(async()=>{const e=await Promise.all(n.map((async e=>await v(`instances/${e.id}`,{method:"GET",headers:{"Content-Type":"application/json"}}))));r(e)})()),5e3);return()=>{clearInterval(e)}}),[n]);const l=(t?n:o).sort(((e,t)=>e.created_at<t.created_at?1:e.created_at>t.created_at?-1:0));return 0===l.length?d().createElement("div",{className:`instance-list ${e}`},d().createElement(q,{body:"There is no workflow history to display",icon:S.faHistory})):d().createElement("div",{className:`instance-list ${e}`},d().createElement("ul",null,l.map((e=>d().createElement("li",null,d().createElement("div",{className:"instance"},d().createElement(b.Link,{className:"instance-link",to:`/instances/${e.id}`},d().createElement("div",{className:"instance-details"},d().createElement("div",{className:"instance-name"},d().createElement("p",{className:"preheader"},"ID: ",e.id),d().createElement("h3",{className:"large"},e.name)),d().createElement("div",{className:"instance-created"},d().createElement("p",{className:"preheader"},"Created date"),d().createElement("h4",null,(e=>{const t=e.split("-");return`${t.slice(0,-2).join("/")} at ${t.slice(-2).join(":")}`})(e.created_at))),d().createElement("div",{className:"instance-status-indicator"},d().createElement("div",{className:"instance-status"},d().createElement(x,{status:e.status}),d().createElement("p",{className:"preheader"},e.status)))))))))))}))`
  && {
    width: calc(1024px + 30px);
    padding: 0 15px 15px 15px;
    margin: 0 auto;
    box-sizing: border-box;
  }

  > ul {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
    grid-template-rows: minmax(min-content, max-content);
    grid-column-gap: 20px;
    grid-row-gap: 20px;
    list-style: none;
  }

  .instance {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: white;
    box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
    border-radius: 4px;
    transition: box-shadow 0.25s ease, transform 0.25s ease;
  }

  .instance-details {
    padding: 25px 25px 25px 25px;
  }

  .instance-details p {
    padding: 0 0 5px 0;
    color: #ccc;
  }

  .instance-name,
  .instance-created {
    padding: 0 0 10px 0;
    margin: 0 0 15px 0;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    border-bottom: 1px solid #f2f2f2;
  }

  .instance-status {
    display: flex;
    align-items: center;
  }

  .instance-status p {
    padding: 0 0 0 15px;
  }
`,te=ee,oe=m()((({className:e})=>{const[t,o]=(0,s.useState)(0),a=[{body:"Select workflow",onClick:()=>o(0),element:d().createElement("div",{className:"tab-contents"},d().createElement(X,null))},{body:"Workflow history",onClick:()=>o(1),element:d().createElement("div",{className:"tab-contents"},d().createElement(te,null))}];return d().createElement("div",{className:`index-panel ${e}`},d().createElement(p,{title:"EPI2ME Labs Workflows",body:d().createElement("p",{className:"large"},"EPI2ME Labs is developing nextflow workflows covering a variety everyday bioinformatics needs. These workflows are free and open to to be used by anyone."),active:t,tabs:a}),a[t].element)}))`
  && {
    background-color: #f6f6f6;
    padding-bottom: 50px;
  }

  @keyframes fadeInUp {
    from {
      transform: translate3d(0, 40px, 0);
    }

    to {
      transform: translate3d(0, 0, 0);
      opacity: 1;
    }
  }

  .tab-contents {
    opacity: 0;
    animation-name: fadeInUp;
    animation-duration: 1s;
    animation-fill-mode: both;
  }
`,ae=()=>{const e=new Blob(['\n  <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="148" height="198" viewBox="0 0 148 198">\n    <defs>\n      <filter id="Rectangle_1" x="0" y="0" width="148" height="68" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur"/>\n        <feComposite in="SourceGraphic"/>\n      </filter>\n      <filter id="Rectangle_2" x="0" y="130" width="148" height="68" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur-2"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur-2"/>\n        <feComposite in="SourceGraphic"/>\n      </filter>\n      <filter id="Rectangle_3" x="0" y="65" width="73" height="68" filterUnits="userSpaceOnUse">\n        <feOffset dy="3" input="SourceAlpha"/>\n        <feGaussianBlur stdDeviation="3" result="blur-3"/>\n        <feFlood flood-opacity="0.098"/>\n        <feComposite operator="in" in2="blur-3"/>\n        <feComposite in="SourceGraphic"/>\n      </filter>\n    </defs>\n    <g id="Component_1_2" data-name="Component 1 – 2" transform="translate(9 6)">\n      <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_1)">\n        <rect id="Rectangle_1-2" data-name="Rectangle 1" width="130" height="50" rx="5" transform="translate(9 6)" fill="#08bbb2"/>\n      </g>\n      <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_2)">\n        <rect id="Rectangle_2-2" data-name="Rectangle 2" width="130" height="50" rx="5" transform="translate(9 136)" fill="#0179a4"/>\n      </g>\n      <g transform="matrix(1, 0, 0, 1, -9, -6)" filter="url(#Rectangle_3)">\n        <rect id="Rectangle_3-2" data-name="Rectangle 3" width="55" height="50" rx="5" transform="translate(9 71)" fill="#fccb10"/>\n      </g>\n    </g>\n  </svg>\n'],{type:"image/svg+xml"}),t=URL.createObjectURL(e);return d().createElement("div",{className:"labsLogo"},d().createElement("img",{src:t,alt:"The EPI2ME Labs logo"}))},ne=m()((({className:e})=>d().createElement("header",{className:`header ${e}`},d().createElement("div",{className:"header-contents"},d().createElement(b.Link,{className:"header-logo",to:"/"},d().createElement(ae,null)),d().createElement("div",{className:"header-links"},d().createElement("ul",null,d().createElement("li",{className:"text-link"},d().createElement(b.Link,{to:"/workflows"},"Workflows")),d().createElement("li",{className:"text-link"},d().createElement(b.Link,{to:"/notebooks"},"Notebooks")),d().createElement("li",null,d().createElement(b.Link,{to:"/"},d().createElement(C.FontAwesomeIcon,{icon:S.faHouse})))))))))`
  padding: 15px 25px;
  position: sticky;
  top: 0;
  left: 0;
  right: 0;
  background-color: #00485b;
  color: white;
  box-shadow: 0 6px 15px rgb(36 37 38 / 8%);
  z-index: 2000;

  .header-contents {
    max-width: 1024px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
  }

  .header-links {
    display: flex;
  }

  .header-links ul {
    display: flex;
    align-items: center;
  }

  .header-links a {
    margin: 0 0 0 20px;
    outline: none;
    background: none;
    border: none;
    vertical-align: middle;
    cursor: pointer;
  }

  .header-links .text-link a {
    color: white;
    font-size: 13px;
    font-weight: 500;
  }

  .header-links a svg {
    font-size: 1.2em;
    color: rgba(255, 255, 255, 0.35);
  }

  .header-links a:hover svg {
    color: rgba(255, 255, 255, 0.85);
  }

  .labsLogo {
    display: flex;
  }

  .labsLogo img {
    width: 25px;
  }

  a {
    font-weight: bold;
  }
`,re=m()((({className:e})=>d().createElement("footer",{className:`footer ${e}`},d().createElement("p",null,"@2008 - ",K()().year()," Oxford Nanopore Technologies. All rights reserved"))))`
  width: 100%;
  padding: 25px;
  text-align: center;
  box-sizing: border-box;
`,le=m().div``;class ie extends r.ReactWidget{constructor(e,t,o){super(),this.app=e,this.docTrack=t,this.settings=o,this.addClass("jp-ReactWidget"),this.addClass("epi2melabs-wfpage-widget")}render(){return d().createElement(b.MemoryRouter,null,d().createElement(le,null,d().createElement("main",{style:{position:"relative"}},d().createElement(ne,null),d().createElement("div",null,d().createElement(b.Routes,null,d().createElement(b.Route,{path:"/workflows/:name"},d().createElement(b.Route,{path:":instance_id",element:d().createElement(Y,null)}),d().createElement(b.Route,{path:"",element:d().createElement(Y,null)})),d().createElement(b.Route,{path:"/workflows",element:d().createElement(oe,null)}),d().createElement(b.Route,{path:"/instances/:id",element:d().createElement(j,{docTrack:this.docTrack,app:this.app})}),d().createElement(b.Route,{path:"/notebooks",element:d().createElement(Q,{docTrack:this.docTrack,templateDir:this.settings.get("template_dir").composite,workDir:this.settings.get("working_dir").composite})}),d().createElement(b.Route,{path:"/",element:d().createElement(oe,null)}))),d().createElement(re,null))))}}const se="@epi2melabs/epi2melabs-wfpage:plugin",de="create-epi2me-labs-launcher",ce={id:se,autoStart:!0,requires:[l.ILauncher,a.ISettingRegistry,n.IDocumentManager],activate:(e,t,o,a)=>{const{commands:n,shell:l}=e,s=(t,o,a)=>{const n=new ie(e,o,a),l=new r.MainAreaWidget({content:n});l.title.label="EPI2ME Labs",t.add(l,"main")};Promise.all([e.restored,o.load(se)]).then((([,o])=>{n.addCommand(de,{caption:"Create an EPI2ME Labs launcher",label:"EPI2ME Labs",icon:i,execute:()=>s(l,a,o)}),s(l,a,o),t&&t.add({command:de,category:"EPI2ME Labs"}),e.commands.execute("filebrowser:hide-main")}))}}}}]);