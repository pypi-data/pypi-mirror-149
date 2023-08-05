"use strict";(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[545],{5545:function(e,t,o){o.d(t,{Z:function(){return ce}});var n=o(3366),r=o(7462),a=o(7294),l=o(6010),i=o(7579),s=o(8925),c=o(3633),p=o(7960);function u(e){return"undefined"!==typeof e.normalize?e.normalize("NFD").replace(/[\u0300-\u036f]/g,""):e}function d(e,t){for(let o=0;o<e.length;o+=1)if(t(e[o]))return o;return-1}const g=function(e={}){const{ignoreAccents:t=!0,ignoreCase:o=!0,limit:n,matchFrom:r="any",stringify:a,trim:l=!1}=e;return(e,{inputValue:i,getOptionLabel:s})=>{let c=l?i.trim():i;o&&(c=c.toLowerCase()),t&&(c=u(c));const p=e.filter((e=>{let n=(a||s)(e);return o&&(n=n.toLowerCase()),t&&(n=u(n)),"start"===r?0===n.indexOf(c):n.indexOf(c)>-1}));return"number"===typeof n?p.slice(0,n):p}}();function m(e){const{autoComplete:t=!1,autoHighlight:o=!1,autoSelect:n=!1,blurOnSelect:l=!1,disabled:u,clearOnBlur:m=!e.freeSolo,clearOnEscape:f=!1,componentName:b="useAutocomplete",defaultValue:h=(e.multiple?[]:null),disableClearable:v=!1,disableCloseOnSelect:x=!1,disabledItemsFocusable:y=!1,disableListWrap:Z=!1,filterOptions:C=g,filterSelectedOptions:$=!1,freeSolo:S=!1,getOptionDisabled:I,getOptionLabel:k=(e=>{var t;return null!=(t=e.label)?t:e}),isOptionEqualToValue:O=((e,t)=>e===t),groupBy:P,handleHomeEndKeys:w=!e.freeSolo,id:R,includeInputInList:L=!1,inputValue:T,multiple:A=!1,onChange:z,onClose:M,onHighlightChange:N,onInputChange:D,onOpen:F,open:E,openOnFocus:V=!1,options:j,readOnly:W=!1,selectOnFocus:H=!e.freeSolo,value:q}=e,K=(0,i.Z)(R);let B=k;B=e=>{const t=k(e);return"string"!==typeof t?String(t):t};const G=a.useRef(!1),U=a.useRef(!0),_=a.useRef(null),J=a.useRef(null),[Q,X]=a.useState(null),[Y,ee]=a.useState(-1),te=o?0:-1,oe=a.useRef(te),[ne,re]=(0,s.Z)({controlled:q,default:h,name:b}),[ae,le]=(0,s.Z)({controlled:T,default:"",name:b,state:"inputValue"}),[ie,se]=a.useState(!1),ce=a.useCallback(((e,t)=>{if(!(A?ne.length<t.length:null!==t)&&!m)return;let o;if(A)o="";else if(null==t)o="";else{const e=B(t);o="string"===typeof e?e:""}ae!==o&&(le(o),D&&D(e,o,"reset"))}),[B,ae,A,D,le,m,ne]),pe=a.useRef();a.useEffect((()=>{const e=ne!==pe.current;pe.current=ne,ie&&!e||S&&!e||ce(null,ne)}),[ne,ce,ie,pe,S]);const[ue,de]=(0,s.Z)({controlled:E,default:!1,name:b,state:"open"}),[ge,me]=a.useState(!0),fe=!A&&null!=ne&&ae===B(ne),be=ue&&!W,he=be?C(j.filter((e=>!$||!(A?ne:[ne]).some((t=>null!==t&&O(e,t))))),{inputValue:fe&&ge?"":ae,getOptionLabel:B}):[],ve=ue&&he.length>0&&!W;const xe=(0,c.Z)((e=>{-1===e?_.current.focus():Q.querySelector(`[data-tag-index="${e}"]`).focus()}));a.useEffect((()=>{A&&Y>ne.length-1&&(ee(-1),xe(-1))}),[ne,A,Y,xe]);const ye=(0,c.Z)((({event:e,index:t,reason:o="auto"})=>{if(oe.current=t,-1===t?_.current.removeAttribute("aria-activedescendant"):_.current.setAttribute("aria-activedescendant",`${K}-option-${t}`),N&&N(e,-1===t?null:he[t],o),!J.current)return;const n=J.current.querySelector('[role="option"].Mui-focused');n&&(n.classList.remove("Mui-focused"),n.classList.remove("Mui-focusVisible"));const r=J.current.parentElement.querySelector('[role="listbox"]');if(!r)return;if(-1===t)return void(r.scrollTop=0);const a=J.current.querySelector(`[data-option-index="${t}"]`);if(a&&(a.classList.add("Mui-focused"),"keyboard"===o&&a.classList.add("Mui-focusVisible"),r.scrollHeight>r.clientHeight&&"mouse"!==o)){const e=a,t=r.clientHeight+r.scrollTop,o=e.offsetTop+e.offsetHeight;o>t?r.scrollTop=o-r.clientHeight:e.offsetTop-e.offsetHeight*(P?1.3:0)<r.scrollTop&&(r.scrollTop=e.offsetTop-e.offsetHeight*(P?1.3:0))}})),Ze=(0,c.Z)((({event:e,diff:o,direction:n="next",reason:r="auto"})=>{if(!be)return;const a=function(e,t){if(!J.current||-1===e)return-1;let o=e;for(;;){if("next"===t&&o===he.length||"previous"===t&&-1===o)return-1;const e=J.current.querySelector(`[data-option-index="${o}"]`),n=!y&&(!e||e.disabled||"true"===e.getAttribute("aria-disabled"));if(!(e&&!e.hasAttribute("tabindex")||n))return o;o+="next"===t?1:-1}}((()=>{const e=he.length-1;if("reset"===o)return te;if("start"===o)return 0;if("end"===o)return e;const t=oe.current+o;return t<0?-1===t&&L?-1:Z&&-1!==oe.current||Math.abs(o)>1?0:e:t>e?t===e+1&&L?-1:Z||Math.abs(o)>1?e:0:t})(),n);if(ye({index:a,reason:r,event:e}),t&&"reset"!==o)if(-1===a)_.current.value=ae;else{const e=B(he[a]);_.current.value=e;0===e.toLowerCase().indexOf(ae.toLowerCase())&&ae.length>0&&_.current.setSelectionRange(ae.length,e.length)}})),Ce=a.useCallback((()=>{if(!be)return;const e=A?ne[0]:ne;if(0!==he.length&&null!=e){if(J.current)if(null==e)oe.current>=he.length-1?ye({index:he.length-1}):ye({index:oe.current});else{const t=he[oe.current];if(A&&t&&-1!==d(ne,(e=>O(t,e))))return;const o=d(he,(t=>O(t,e)));-1===o?Ze({diff:"reset"}):ye({index:o})}}else Ze({diff:"reset"})}),[he.length,!A&&ne,$,Ze,ye,be,ae,A]),$e=(0,c.Z)((e=>{(0,p.Z)(J,e),e&&Ce()}));a.useEffect((()=>{Ce()}),[Ce]);const Se=e=>{ue||(de(!0),me(!0),F&&F(e))},Ie=(e,t)=>{ue&&(de(!1),M&&M(e,t))},ke=(e,t,o,n)=>{if(Array.isArray(ne)){if(ne.length===t.length&&ne.every(((e,o)=>e===t[o])))return}else if(ne===t)return;z&&z(e,t,o,n),re(t)},Oe=a.useRef(!1),Pe=(e,t,o="selectOption",n="options")=>{let r=o,a=t;if(A){a=Array.isArray(ne)?ne.slice():[];const e=d(a,(e=>O(t,e)));-1===e?a.push(t):"freeSolo"!==n&&(a.splice(e,1),r="removeOption")}ce(e,a),ke(e,a,r,{option:t}),x||e.ctrlKey||e.metaKey||Ie(e,r),(!0===l||"touch"===l&&Oe.current||"mouse"===l&&!Oe.current)&&_.current.blur()};const we=(e,t)=>{if(!A)return;Ie(e,"toggleInput");let o=Y;-1===Y?""===ae&&"previous"===t&&(o=ne.length-1):(o+="next"===t?1:-1,o<0&&(o=0),o===ne.length&&(o=-1)),o=function(e,t){if(-1===e)return-1;let o=e;for(;;){if("next"===t&&o===ne.length||"previous"===t&&-1===o)return-1;const e=Q.querySelector(`[data-tag-index="${o}"]`);if(e&&e.hasAttribute("tabindex")&&!e.disabled&&"true"!==e.getAttribute("aria-disabled"))return o;o+="next"===t?1:-1}}(o,t),ee(o),xe(o)},Re=e=>{G.current=!0,le(""),D&&D(e,"","clear"),ke(e,A?[]:null,"clear")},Le=e=>o=>{if(e.onKeyDown&&e.onKeyDown(o),!o.defaultMuiPrevented&&(-1!==Y&&-1===["ArrowLeft","ArrowRight"].indexOf(o.key)&&(ee(-1),xe(-1)),229!==o.which))switch(o.key){case"Home":be&&w&&(o.preventDefault(),Ze({diff:"start",direction:"next",reason:"keyboard",event:o}));break;case"End":be&&w&&(o.preventDefault(),Ze({diff:"end",direction:"previous",reason:"keyboard",event:o}));break;case"PageUp":o.preventDefault(),Ze({diff:-5,direction:"previous",reason:"keyboard",event:o}),Se(o);break;case"PageDown":o.preventDefault(),Ze({diff:5,direction:"next",reason:"keyboard",event:o}),Se(o);break;case"ArrowDown":o.preventDefault(),Ze({diff:1,direction:"next",reason:"keyboard",event:o}),Se(o);break;case"ArrowUp":o.preventDefault(),Ze({diff:-1,direction:"previous",reason:"keyboard",event:o}),Se(o);break;case"ArrowLeft":we(o,"previous");break;case"ArrowRight":we(o,"next");break;case"Enter":if(-1!==oe.current&&be){const e=he[oe.current],n=!!I&&I(e);if(o.preventDefault(),n)return;Pe(o,e,"selectOption"),t&&_.current.setSelectionRange(_.current.value.length,_.current.value.length)}else S&&""!==ae&&!1===fe&&(A&&o.preventDefault(),Pe(o,ae,"createOption","freeSolo"));break;case"Escape":be?(o.preventDefault(),o.stopPropagation(),Ie(o,"escape")):f&&(""!==ae||A&&ne.length>0)&&(o.preventDefault(),o.stopPropagation(),Re(o));break;case"Backspace":if(A&&!W&&""===ae&&ne.length>0){const e=-1===Y?ne.length-1:Y,t=ne.slice();t.splice(e,1),ke(o,t,"removeOption",{option:ne[e]})}}},Te=e=>{se(!0),V&&!G.current&&Se(e)},Ae=e=>{null!==J.current&&J.current.parentElement.contains(document.activeElement)?_.current.focus():(se(!1),U.current=!0,G.current=!1,n&&-1!==oe.current&&be?Pe(e,he[oe.current],"blur"):n&&S&&""!==ae?Pe(e,ae,"blur","freeSolo"):m&&ce(e,ne),Ie(e,"blur"))},ze=e=>{const t=e.target.value;ae!==t&&(le(t),me(!1),D&&D(e,t,"input")),""===t?v||A||ke(e,null,"clear"):Se(e)},Me=e=>{ye({event:e,index:Number(e.currentTarget.getAttribute("data-option-index")),reason:"mouse"})},Ne=()=>{Oe.current=!0},De=e=>{const t=Number(e.currentTarget.getAttribute("data-option-index"));Pe(e,he[t],"selectOption"),Oe.current=!1},Fe=e=>t=>{const o=ne.slice();o.splice(e,1),ke(t,o,"removeOption",{option:ne[e]})},Ee=e=>{ue?Ie(e,"toggleInput"):Se(e)},Ve=e=>{e.target.getAttribute("id")!==K&&e.preventDefault()},je=()=>{_.current.focus(),H&&U.current&&_.current.selectionEnd-_.current.selectionStart===0&&_.current.select(),U.current=!1},We=e=>{""!==ae&&ue||Ee(e)};let He=S&&ae.length>0;He=He||(A?ne.length>0:null!==ne);let qe=he;if(P){new Map;qe=he.reduce(((e,t,o)=>{const n=P(t);return e.length>0&&e[e.length-1].group===n?e[e.length-1].options.push(t):e.push({key:o,index:o,group:n,options:[t]}),e}),[])}return u&&ie&&Ae(),{getRootProps:(e={})=>(0,r.Z)({"aria-owns":ve?`${K}-listbox`:null},e,{onKeyDown:Le(e),onMouseDown:Ve,onClick:je}),getInputLabelProps:()=>({id:`${K}-label`,htmlFor:K}),getInputProps:()=>({id:K,value:ae,onBlur:Ae,onFocus:Te,onChange:ze,onMouseDown:We,"aria-activedescendant":be?"":null,"aria-autocomplete":t?"both":"list","aria-controls":ve?`${K}-listbox`:void 0,"aria-expanded":ve,autoComplete:"off",ref:_,autoCapitalize:"none",spellCheck:"false",role:"combobox"}),getClearProps:()=>({tabIndex:-1,onClick:Re}),getPopupIndicatorProps:()=>({tabIndex:-1,onClick:Ee}),getTagProps:({index:e})=>(0,r.Z)({key:e,"data-tag-index":e,tabIndex:-1},!W&&{onDelete:Fe(e)}),getListboxProps:()=>({role:"listbox",id:`${K}-listbox`,"aria-labelledby":`${K}-label`,ref:$e,onMouseDown:e=>{e.preventDefault()}}),getOptionProps:({index:e,option:t})=>{const o=(A?ne:[ne]).some((e=>null!=e&&O(t,e))),n=!!I&&I(t);return{key:B(t),tabIndex:-1,role:"option",id:`${K}-option-${e}`,onMouseOver:Me,onClick:De,onTouchStart:Ne,"data-option-index":e,"aria-disabled":n,"aria-selected":o}},id:K,inputValue:ae,value:ne,dirty:He,popupOpen:be,focused:ie||-1!==Y,anchorEl:Q,setAnchorEl:X,focusedTag:Y,groupedOptions:qe}}var f=o(7192),b=o(1796),h=o(1849),v=o(1496),x=o(3616),y=o(8216),Z=o(8979),C=o(6087);function $(e){return(0,Z.Z)("MuiListSubheader",e)}(0,C.Z)("MuiListSubheader",["root","colorPrimary","colorInherit","gutters","inset","sticky"]);var S=o(5893);const I=["className","color","component","disableGutters","disableSticky","inset"],k=(0,v.ZP)("li",{name:"MuiListSubheader",slot:"Root",overridesResolver:(e,t)=>{const{ownerState:o}=e;return[t.root,"default"!==o.color&&t[`color${(0,y.Z)(o.color)}`],!o.disableGutters&&t.gutters,o.inset&&t.inset,!o.disableSticky&&t.sticky]}})((({theme:e,ownerState:t})=>(0,r.Z)({boxSizing:"border-box",lineHeight:"48px",listStyle:"none",color:e.palette.text.secondary,fontFamily:e.typography.fontFamily,fontWeight:e.typography.fontWeightMedium,fontSize:e.typography.pxToRem(14)},"primary"===t.color&&{color:e.palette.primary.main},"inherit"===t.color&&{color:"inherit"},!t.disableGutters&&{paddingLeft:16,paddingRight:16},t.inset&&{paddingLeft:72},!t.disableSticky&&{position:"sticky",top:0,zIndex:1,backgroundColor:e.palette.background.paper})));var O=a.forwardRef((function(e,t){const o=(0,x.Z)({props:e,name:"MuiListSubheader"}),{className:a,color:i="default",component:s="li",disableGutters:c=!1,disableSticky:p=!1,inset:u=!1}=o,d=(0,n.Z)(o,I),g=(0,r.Z)({},o,{color:i,component:s,disableGutters:c,disableSticky:p,inset:u}),m=(e=>{const{classes:t,color:o,disableGutters:n,inset:r,disableSticky:a}=e,l={root:["root","default"!==o&&`color${(0,y.Z)(o)}`,!n&&"gutters",r&&"inset",!a&&"sticky"]};return(0,f.Z)(l,$,t)})(g);return(0,S.jsx)(k,(0,r.Z)({as:s,className:(0,l.Z)(m.root,a),ref:t,ownerState:g},d))})),P=o(5113),w=o(3946),R=o(8169),L=(0,R.Z)((0,S.jsx)("path",{d:"M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z"}),"Cancel"),T=o(1705),A=o(7739);function z(e){return(0,Z.Z)("MuiChip",e)}var M=(0,C.Z)("MuiChip",["root","sizeSmall","sizeMedium","colorPrimary","colorSecondary","disabled","clickable","clickableColorPrimary","clickableColorSecondary","deletable","deletableColorPrimary","deletableColorSecondary","outlined","filled","outlinedPrimary","outlinedSecondary","avatar","avatarSmall","avatarMedium","avatarColorPrimary","avatarColorSecondary","icon","iconSmall","iconMedium","iconColorPrimary","iconColorSecondary","label","labelSmall","labelMedium","deleteIcon","deleteIconSmall","deleteIconMedium","deleteIconColorPrimary","deleteIconColorSecondary","deleteIconOutlinedColorPrimary","deleteIconOutlinedColorSecondary","focusVisible"]);const N=["avatar","className","clickable","color","component","deleteIcon","disabled","icon","label","onClick","onDelete","onKeyDown","onKeyUp","size","variant"],D=(0,v.ZP)("div",{name:"MuiChip",slot:"Root",overridesResolver:(e,t)=>{const{ownerState:o}=e,{color:n,clickable:r,onDelete:a,size:l,variant:i}=o;return[{[`& .${M.avatar}`]:t.avatar},{[`& .${M.avatar}`]:t[`avatar${(0,y.Z)(l)}`]},{[`& .${M.avatar}`]:t[`avatarColor${(0,y.Z)(n)}`]},{[`& .${M.icon}`]:t.icon},{[`& .${M.icon}`]:t[`icon${(0,y.Z)(l)}`]},{[`& .${M.icon}`]:t[`iconColor${(0,y.Z)(n)}`]},{[`& .${M.deleteIcon}`]:t.deleteIcon},{[`& .${M.deleteIcon}`]:t[`deleteIcon${(0,y.Z)(l)}`]},{[`& .${M.deleteIcon}`]:t[`deleteIconColor${(0,y.Z)(n)}`]},{[`& .${M.deleteIcon}`]:t[`deleteIconOutlinedColor${(0,y.Z)(n)}`]},t.root,t[`size${(0,y.Z)(l)}`],t[`color${(0,y.Z)(n)}`],r&&t.clickable,r&&"default"!==n&&t[`clickableColor${(0,y.Z)(n)})`],a&&t.deletable,a&&"default"!==n&&t[`deletableColor${(0,y.Z)(n)}`],t[i],"outlined"===i&&t[`outlined${(0,y.Z)(n)}`]]}})((({theme:e,ownerState:t})=>{const o=(0,b.Fq)(e.palette.text.primary,.26);return(0,r.Z)({maxWidth:"100%",fontFamily:e.typography.fontFamily,fontSize:e.typography.pxToRem(13),display:"inline-flex",alignItems:"center",justifyContent:"center",height:32,color:e.palette.text.primary,backgroundColor:e.palette.action.selected,borderRadius:16,whiteSpace:"nowrap",transition:e.transitions.create(["background-color","box-shadow"]),cursor:"default",outline:0,textDecoration:"none",border:0,padding:0,verticalAlign:"middle",boxSizing:"border-box",[`&.${M.disabled}`]:{opacity:e.palette.action.disabledOpacity,pointerEvents:"none"},[`& .${M.avatar}`]:{marginLeft:5,marginRight:-6,width:24,height:24,color:"light"===e.palette.mode?e.palette.grey[700]:e.palette.grey[300],fontSize:e.typography.pxToRem(12)},[`& .${M.avatarColorPrimary}`]:{color:e.palette.primary.contrastText,backgroundColor:e.palette.primary.dark},[`& .${M.avatarColorSecondary}`]:{color:e.palette.secondary.contrastText,backgroundColor:e.palette.secondary.dark},[`& .${M.avatarSmall}`]:{marginLeft:4,marginRight:-4,width:18,height:18,fontSize:e.typography.pxToRem(10)},[`& .${M.icon}`]:(0,r.Z)({color:"light"===e.palette.mode?e.palette.grey[700]:e.palette.grey[300],marginLeft:5,marginRight:-6},"small"===t.size&&{fontSize:18,marginLeft:4,marginRight:-4},"default"!==t.color&&{color:"inherit"}),[`& .${M.deleteIcon}`]:(0,r.Z)({WebkitTapHighlightColor:"transparent",color:o,fontSize:22,cursor:"pointer",margin:"0 5px 0 -6px","&:hover":{color:(0,b.Fq)(o,.4)}},"small"===t.size&&{fontSize:16,marginRight:4,marginLeft:-4},"default"!==t.color&&{color:(0,b.Fq)(e.palette[t.color].contrastText,.7),"&:hover, &:active":{color:e.palette[t.color].contrastText}})},"small"===t.size&&{height:24},"default"!==t.color&&{backgroundColor:e.palette[t.color].main,color:e.palette[t.color].contrastText},t.onDelete&&{[`&.${M.focusVisible}`]:{backgroundColor:(0,b.Fq)(e.palette.action.selected,e.palette.action.selectedOpacity+e.palette.action.focusOpacity)}},t.onDelete&&"default"!==t.color&&{[`&.${M.focusVisible}`]:{backgroundColor:e.palette[t.color].dark}})}),(({theme:e,ownerState:t})=>(0,r.Z)({},t.clickable&&{userSelect:"none",WebkitTapHighlightColor:"transparent",cursor:"pointer","&:hover":{backgroundColor:(0,b.Fq)(e.palette.action.selected,e.palette.action.selectedOpacity+e.palette.action.hoverOpacity)},[`&.${M.focusVisible}`]:{backgroundColor:(0,b.Fq)(e.palette.action.selected,e.palette.action.selectedOpacity+e.palette.action.focusOpacity)},"&:active":{boxShadow:e.shadows[1]}},t.clickable&&"default"!==t.color&&{[`&:hover, &.${M.focusVisible}`]:{backgroundColor:e.palette[t.color].dark}})),(({theme:e,ownerState:t})=>(0,r.Z)({},"outlined"===t.variant&&{backgroundColor:"transparent",border:`1px solid ${"light"===e.palette.mode?e.palette.grey[400]:e.palette.grey[700]}`,[`&.${M.clickable}:hover`]:{backgroundColor:e.palette.action.hover},[`&.${M.focusVisible}`]:{backgroundColor:e.palette.action.focus},[`& .${M.avatar}`]:{marginLeft:4},[`& .${M.avatarSmall}`]:{marginLeft:2},[`& .${M.icon}`]:{marginLeft:4},[`& .${M.iconSmall}`]:{marginLeft:2},[`& .${M.deleteIcon}`]:{marginRight:5},[`& .${M.deleteIconSmall}`]:{marginRight:3}},"outlined"===t.variant&&"default"!==t.color&&{color:e.palette[t.color].main,border:`1px solid ${(0,b.Fq)(e.palette[t.color].main,.7)}`,[`&.${M.clickable}:hover`]:{backgroundColor:(0,b.Fq)(e.palette[t.color].main,e.palette.action.hoverOpacity)},[`&.${M.focusVisible}`]:{backgroundColor:(0,b.Fq)(e.palette[t.color].main,e.palette.action.focusOpacity)},[`& .${M.deleteIcon}`]:{color:(0,b.Fq)(e.palette[t.color].main,.7),"&:hover, &:active":{color:e.palette[t.color].main}}}))),F=(0,v.ZP)("span",{name:"MuiChip",slot:"Label",overridesResolver:(e,t)=>{const{ownerState:o}=e,{size:n}=o;return[t.label,t[`label${(0,y.Z)(n)}`]]}})((({ownerState:e})=>(0,r.Z)({overflow:"hidden",textOverflow:"ellipsis",paddingLeft:12,paddingRight:12,whiteSpace:"nowrap"},"small"===e.size&&{paddingLeft:8,paddingRight:8})));function E(e){return"Backspace"===e.key||"Delete"===e.key}var V=a.forwardRef((function(e,t){const o=(0,x.Z)({props:e,name:"MuiChip"}),{avatar:i,className:s,clickable:c,color:p="default",component:u,deleteIcon:d,disabled:g=!1,icon:m,label:b,onClick:h,onDelete:v,onKeyDown:Z,onKeyUp:C,size:$="medium",variant:I="filled"}=o,k=(0,n.Z)(o,N),O=a.useRef(null),P=(0,T.Z)(O,t),w=e=>{e.stopPropagation(),v&&v(e)},R=!(!1===c||!h)||c,M="small"===$,V=R||v?A.Z:u||"div",j=(0,r.Z)({},o,{component:V,disabled:g,size:$,color:p,onDelete:!!v,clickable:R,variant:I}),W=(e=>{const{classes:t,disabled:o,size:n,color:r,onDelete:a,clickable:l,variant:i}=e,s={root:["root",i,o&&"disabled",`size${(0,y.Z)(n)}`,`color${(0,y.Z)(r)}`,l&&"clickable",l&&`clickableColor${(0,y.Z)(r)}`,a&&"deletable",a&&`deletableColor${(0,y.Z)(r)}`,`${i}${(0,y.Z)(r)}`],label:["label",`label${(0,y.Z)(n)}`],avatar:["avatar",`avatar${(0,y.Z)(n)}`,`avatarColor${(0,y.Z)(r)}`],icon:["icon",`icon${(0,y.Z)(n)}`,`iconColor${(0,y.Z)(r)}`],deleteIcon:["deleteIcon",`deleteIcon${(0,y.Z)(n)}`,`deleteIconColor${(0,y.Z)(r)}`,`deleteIconOutlinedColor${(0,y.Z)(r)}`]};return(0,f.Z)(s,z,t)})(j),H=V===A.Z?(0,r.Z)({component:u||"div",focusVisibleClassName:W.focusVisible},v&&{disableRipple:!0}):{};let q=null;if(v){const e=(0,l.Z)("default"!==p&&("outlined"===I?W[`deleteIconOutlinedColor${(0,y.Z)(p)}`]:W[`deleteIconColor${(0,y.Z)(p)}`]),M&&W.deleteIconSmall);q=d&&a.isValidElement(d)?a.cloneElement(d,{className:(0,l.Z)(d.props.className,W.deleteIcon,e),onClick:w}):(0,S.jsx)(L,{className:(0,l.Z)(W.deleteIcon,e),onClick:w})}let K=null;i&&a.isValidElement(i)&&(K=a.cloneElement(i,{className:(0,l.Z)(W.avatar,i.props.className)}));let B=null;return m&&a.isValidElement(m)&&(B=a.cloneElement(m,{className:(0,l.Z)(W.icon,m.props.className)})),(0,S.jsxs)(D,(0,r.Z)({as:V,className:(0,l.Z)(W.root,s),disabled:!(!R||!g)||void 0,onClick:h,onKeyDown:e=>{e.currentTarget===e.target&&E(e)&&e.preventDefault(),Z&&Z(e)},onKeyUp:e=>{e.currentTarget===e.target&&(v&&E(e)?v(e):"Escape"===e.key&&O.current&&O.current.blur()),C&&C(e)},ref:P,ownerState:j},H,k,{children:[K||B,(0,S.jsx)(F,{className:(0,l.Z)(W.label),ownerState:j,children:b}),q]}))})),j=o(7021),W=o(5827),H=o(4656),q=o(4707),K=(0,R.Z)((0,S.jsx)("path",{d:"M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"}),"Close"),B=o(224);function G(e){return(0,Z.Z)("MuiAutocomplete",e)}var U,_,J=(0,C.Z)("MuiAutocomplete",["root","fullWidth","focused","focusVisible","tag","tagSizeSmall","tagSizeMedium","hasPopupIcon","hasClearIcon","inputRoot","input","inputFocused","endAdornment","clearIndicator","popupIndicator","popupIndicatorOpen","popper","popperDisablePortal","paper","listbox","loading","noOptions","option","groupLabel","groupUl"]);const Q=["autoComplete","autoHighlight","autoSelect","blurOnSelect","ChipProps","className","clearIcon","clearOnBlur","clearOnEscape","clearText","closeText","componentsProps","defaultValue","disableClearable","disableCloseOnSelect","disabled","disabledItemsFocusable","disableListWrap","disablePortal","filterOptions","filterSelectedOptions","forcePopupIcon","freeSolo","fullWidth","getLimitTagsText","getOptionDisabled","getOptionLabel","isOptionEqualToValue","groupBy","handleHomeEndKeys","id","includeInputInList","inputValue","limitTags","ListboxComponent","ListboxProps","loading","loadingText","multiple","noOptionsText","onChange","onClose","onHighlightChange","onInputChange","onOpen","open","openOnFocus","openText","options","PaperComponent","PopperComponent","popupIcon","readOnly","renderGroup","renderInput","renderOption","renderTags","selectOnFocus","size","value"],X=(0,v.ZP)("div",{name:"MuiAutocomplete",slot:"Root",overridesResolver:(e,t)=>{const{ownerState:o}=e,{fullWidth:n,hasClearIcon:r,hasPopupIcon:a,inputFocused:l,size:i}=o;return[{[`& .${J.tag}`]:t.tag},{[`& .${J.tag}`]:t[`tagSize${(0,y.Z)(i)}`]},{[`& .${J.inputRoot}`]:t.inputRoot},{[`& .${J.input}`]:t.input},{[`& .${J.input}`]:l&&t.inputFocused},t.root,n&&t.fullWidth,a&&t.hasPopupIcon,r&&t.hasClearIcon]}})((({ownerState:e})=>(0,r.Z)({[`&.${J.focused} .${J.clearIndicator}`]:{visibility:"visible"},"@media (pointer: fine)":{[`&:hover .${J.clearIndicator}`]:{visibility:"visible"}}},e.fullWidth&&{width:"100%"},{[`& .${J.tag}`]:(0,r.Z)({margin:3,maxWidth:"calc(100% - 6px)"},"small"===e.size&&{margin:2,maxWidth:"calc(100% - 4px)"}),[`& .${J.inputRoot}`]:{flexWrap:"wrap",[`.${J.hasPopupIcon}&, .${J.hasClearIcon}&`]:{paddingRight:30},[`.${J.hasPopupIcon}.${J.hasClearIcon}&`]:{paddingRight:56},[`& .${J.input}`]:{width:0,minWidth:30}},[`& .${j.Z.root}`]:{paddingBottom:1,"& .MuiInput-input":{padding:"4px 4px 4px 0px"}},[`& .${j.Z.root}.${W.Z.sizeSmall}`]:{[`& .${j.Z.input}`]:{padding:"2px 4px 3px 0"}},[`& .${H.Z.root}`]:{padding:9,[`.${J.hasPopupIcon}&, .${J.hasClearIcon}&`]:{paddingRight:39},[`.${J.hasPopupIcon}.${J.hasClearIcon}&`]:{paddingRight:65},[`& .${J.input}`]:{padding:"7.5px 4px 7.5px 6px"},[`& .${J.endAdornment}`]:{right:9}},[`& .${H.Z.root}.${W.Z.sizeSmall}`]:{padding:6,[`& .${J.input}`]:{padding:"2.5px 4px 2.5px 6px"}},[`& .${q.Z.root}`]:{paddingTop:19,paddingLeft:8,[`.${J.hasPopupIcon}&, .${J.hasClearIcon}&`]:{paddingRight:39},[`.${J.hasPopupIcon}.${J.hasClearIcon}&`]:{paddingRight:65},[`& .${q.Z.input}`]:{padding:"7px 4px"},[`& .${J.endAdornment}`]:{right:9}},[`& .${q.Z.root}.${W.Z.sizeSmall}`]:{paddingBottom:1,[`& .${q.Z.input}`]:{padding:"2.5px 4px"}},[`& .${W.Z.hiddenLabel}`]:{paddingTop:8},[`& .${J.input}`]:(0,r.Z)({flexGrow:1,textOverflow:"ellipsis",opacity:0},e.inputFocused&&{opacity:1})}))),Y=(0,v.ZP)("div",{name:"MuiAutocomplete",slot:"EndAdornment",overridesResolver:(e,t)=>t.endAdornment})({position:"absolute",right:0,top:"calc(50% - 14px)"}),ee=(0,v.ZP)(w.Z,{name:"MuiAutocomplete",slot:"ClearIndicator",overridesResolver:(e,t)=>t.clearIndicator})({marginRight:-2,padding:4,visibility:"hidden"}),te=(0,v.ZP)(w.Z,{name:"MuiAutocomplete",slot:"PopupIndicator",overridesResolver:({ownerState:e},t)=>(0,r.Z)({},t.popupIndicator,e.popupOpen&&t.popupIndicatorOpen)})((({ownerState:e})=>(0,r.Z)({padding:2,marginRight:-2},e.popupOpen&&{transform:"rotate(180deg)"}))),oe=(0,v.ZP)(h.Z,{name:"MuiAutocomplete",slot:"Popper",overridesResolver:(e,t)=>{const{ownerState:o}=e;return[{[`& .${J.option}`]:t.option},t.popper,o.disablePortal&&t.popperDisablePortal]}})((({theme:e,ownerState:t})=>(0,r.Z)({zIndex:e.zIndex.modal},t.disablePortal&&{position:"absolute"}))),ne=(0,v.ZP)(P.Z,{name:"MuiAutocomplete",slot:"Paper",overridesResolver:(e,t)=>t.paper})((({theme:e})=>(0,r.Z)({},e.typography.body1,{overflow:"auto"}))),re=(0,v.ZP)("div",{name:"MuiAutocomplete",slot:"Loading",overridesResolver:(e,t)=>t.loading})((({theme:e})=>({color:e.palette.text.secondary,padding:"14px 16px"}))),ae=(0,v.ZP)("div",{name:"MuiAutocomplete",slot:"NoOptions",overridesResolver:(e,t)=>t.noOptions})((({theme:e})=>({color:e.palette.text.secondary,padding:"14px 16px"}))),le=(0,v.ZP)("div",{name:"MuiAutocomplete",slot:"Listbox",overridesResolver:(e,t)=>t.listbox})((({theme:e})=>({listStyle:"none",margin:0,padding:"8px 0",maxHeight:"40vh",overflow:"auto",[`& .${J.option}`]:{minHeight:48,display:"flex",overflow:"hidden",justifyContent:"flex-start",alignItems:"center",cursor:"pointer",paddingTop:6,boxSizing:"border-box",outline:"0",WebkitTapHighlightColor:"transparent",paddingBottom:6,paddingLeft:16,paddingRight:16,[e.breakpoints.up("sm")]:{minHeight:"auto"},[`&.${J.focused}`]:{backgroundColor:e.palette.action.hover,"@media (hover: none)":{backgroundColor:"transparent"}},'&[aria-disabled="true"]':{opacity:e.palette.action.disabledOpacity,pointerEvents:"none"},[`&.${J.focusVisible}`]:{backgroundColor:e.palette.action.focus},'&[aria-selected="true"]':{backgroundColor:(0,b.Fq)(e.palette.primary.main,e.palette.action.selectedOpacity),[`&.${J.focused}`]:{backgroundColor:(0,b.Fq)(e.palette.primary.main,e.palette.action.selectedOpacity+e.palette.action.hoverOpacity),"@media (hover: none)":{backgroundColor:e.palette.action.selected}},[`&.${J.focusVisible}`]:{backgroundColor:(0,b.Fq)(e.palette.primary.main,e.palette.action.selectedOpacity+e.palette.action.focusOpacity)}}}}))),ie=(0,v.ZP)(O,{name:"MuiAutocomplete",slot:"GroupLabel",overridesResolver:(e,t)=>t.groupLabel})((({theme:e})=>({backgroundColor:e.palette.background.paper,top:-8}))),se=(0,v.ZP)("ul",{name:"MuiAutocomplete",slot:"GroupUl",overridesResolver:(e,t)=>t.groupUl})({padding:0,[`& .${J.option}`]:{paddingLeft:24}});var ce=a.forwardRef((function(e,t){var o,i;const s=(0,x.Z)({props:e,name:"MuiAutocomplete"}),{autoComplete:c=!1,autoHighlight:p=!1,autoSelect:u=!1,blurOnSelect:d=!1,ChipProps:g,className:b,clearIcon:v=U||(U=(0,S.jsx)(K,{fontSize:"small"})),clearOnBlur:Z=!s.freeSolo,clearOnEscape:C=!1,clearText:$="Clear",closeText:I="Close",componentsProps:k={},defaultValue:O=(s.multiple?[]:null),disableClearable:w=!1,disableCloseOnSelect:R=!1,disabled:L=!1,disabledItemsFocusable:T=!1,disableListWrap:A=!1,disablePortal:z=!1,filterSelectedOptions:M=!1,forcePopupIcon:N="auto",freeSolo:D=!1,fullWidth:F=!1,getLimitTagsText:E=(e=>`+${e}`),getOptionLabel:j=(e=>{var t;return null!=(t=e.label)?t:e}),groupBy:W,handleHomeEndKeys:H=!s.freeSolo,includeInputInList:q=!1,limitTags:J=-1,ListboxComponent:ce="ul",ListboxProps:pe,loading:ue=!1,loadingText:de="Loading\u2026",multiple:ge=!1,noOptionsText:me="No options",openOnFocus:fe=!1,openText:be="Open",PaperComponent:he=P.Z,PopperComponent:ve=h.Z,popupIcon:xe=_||(_=(0,S.jsx)(B.Z,{})),readOnly:ye=!1,renderGroup:Ze,renderInput:Ce,renderOption:$e,renderTags:Se,selectOnFocus:Ie=!s.freeSolo,size:ke="medium"}=s,Oe=(0,n.Z)(s,Q),{getRootProps:Pe,getInputProps:we,getInputLabelProps:Re,getPopupIndicatorProps:Le,getClearProps:Te,getTagProps:Ae,getListboxProps:ze,getOptionProps:Me,value:Ne,dirty:De,id:Fe,popupOpen:Ee,focused:Ve,focusedTag:je,anchorEl:We,setAnchorEl:He,inputValue:qe,groupedOptions:Ke}=m((0,r.Z)({},s,{componentName:"Autocomplete"})),Be=!w&&!L&&De&&!ye,Ge=(!D||!0===N)&&!1!==N,Ue=(0,r.Z)({},s,{disablePortal:z,focused:Ve,fullWidth:F,hasClearIcon:Be,hasPopupIcon:Ge,inputFocused:-1===je,popupOpen:Ee,size:ke}),_e=(e=>{const{classes:t,disablePortal:o,focused:n,fullWidth:r,hasClearIcon:a,hasPopupIcon:l,inputFocused:i,popupOpen:s,size:c}=e,p={root:["root",n&&"focused",r&&"fullWidth",a&&"hasClearIcon",l&&"hasPopupIcon"],inputRoot:["inputRoot"],input:["input",i&&"inputFocused"],tag:["tag",`tagSize${(0,y.Z)(c)}`],endAdornment:["endAdornment"],clearIndicator:["clearIndicator"],popupIndicator:["popupIndicator",s&&"popupIndicatorOpen"],popper:["popper",o&&"popperDisablePortal"],paper:["paper"],listbox:["listbox"],loading:["loading"],noOptions:["noOptions"],option:["option"],groupLabel:["groupLabel"],groupUl:["groupUl"]};return(0,f.Z)(p,G,t)})(Ue);let Je;if(ge&&Ne.length>0){const e=e=>(0,r.Z)({className:(0,l.Z)(_e.tag),disabled:L},Ae(e));Je=Se?Se(Ne,e):Ne.map(((t,o)=>(0,S.jsx)(V,(0,r.Z)({label:j(t),size:ke},e({index:o}),g))))}if(J>-1&&Array.isArray(Je)){const e=Je.length-J;!Ve&&e>0&&(Je=Je.splice(0,J),Je.push((0,S.jsx)("span",{className:_e.tag,children:E(e)},Je.length)))}const Qe=Ze||(e=>(0,S.jsxs)("li",{children:[(0,S.jsx)(ie,{className:_e.groupLabel,ownerState:Ue,component:"div",children:e.group}),(0,S.jsx)(se,{className:_e.groupUl,ownerState:Ue,children:e.children})]},e.key)),Xe=$e||((e,t)=>(0,S.jsx)("li",(0,r.Z)({},e,{children:j(t)}))),Ye=(e,t)=>{const o=Me({option:e,index:t});return Xe((0,r.Z)({},o,{className:_e.option}),e,{selected:o["aria-selected"],inputValue:qe})};return(0,S.jsxs)(a.Fragment,{children:[(0,S.jsx)(X,(0,r.Z)({ref:t,className:(0,l.Z)(_e.root,b),ownerState:Ue},Pe(Oe),{children:Ce({id:Fe,disabled:L,fullWidth:!0,size:"small"===ke?"small":void 0,InputLabelProps:Re(),InputProps:{ref:He,className:_e.inputRoot,startAdornment:Je,endAdornment:(0,S.jsxs)(Y,{className:_e.endAdornment,ownerState:Ue,children:[Be?(0,S.jsx)(ee,(0,r.Z)({},Te(),{"aria-label":$,title:$,ownerState:Ue},k.clearIndicator,{className:(0,l.Z)(_e.clearIndicator,null==(o=k.clearIndicator)?void 0:o.className),children:v})):null,Ge?(0,S.jsx)(te,(0,r.Z)({},Le(),{disabled:L,"aria-label":Ee?I:be,title:Ee?I:be,className:(0,l.Z)(_e.popupIndicator),ownerState:Ue,children:xe})):null]})},inputProps:(0,r.Z)({className:(0,l.Z)(_e.input),disabled:L,readOnly:ye},we())})})),Ee&&We?(0,S.jsx)(oe,{as:ve,className:(0,l.Z)(_e.popper),disablePortal:z,style:{width:We?We.clientWidth:null},ownerState:Ue,role:"presentation",anchorEl:We,open:!0,children:(0,S.jsxs)(ne,(0,r.Z)({ownerState:Ue,as:he},k.paper,{className:(0,l.Z)(_e.paper,null==(i=k.paper)?void 0:i.className),children:[ue&&0===Ke.length?(0,S.jsx)(re,{className:_e.loading,ownerState:Ue,children:de}):null,0!==Ke.length||D||ue?null:(0,S.jsx)(ae,{className:_e.noOptions,ownerState:Ue,role:"presentation",onMouseDown:e=>{e.preventDefault()},children:me}),Ke.length>0?(0,S.jsx)(le,(0,r.Z)({as:ce,className:_e.listbox,ownerState:Ue},ze(),pe,{children:Ke.map(((e,t)=>W?Qe({key:e.key,group:e.group,children:e.options.map(((t,o)=>Ye(t,e.index+o)))}):Ye(e,t)))})):null]}))}):null]})}))}}]);