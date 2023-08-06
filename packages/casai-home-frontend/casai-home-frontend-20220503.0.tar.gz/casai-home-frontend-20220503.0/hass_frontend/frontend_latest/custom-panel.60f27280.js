/*! For license information please see custom-panel.60f27280.js.LICENSE.txt */
(()=>{var e,t,r={25945:(e,t,r)=>{"use strict";r.d(t,{fl:()=>g,iv:()=>s});const o=window.ShadowRoot&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,i=Symbol(),a=new Map;class n{constructor(e,t){if(this._$cssResult$=!0,t!==i)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e}get styleSheet(){let e=a.get(this.cssText);return o&&void 0===e&&(a.set(this.cssText,e=new CSSStyleSheet),e.replaceSync(this.cssText)),e}toString(){return this.cssText}}const l=e=>new n("string"==typeof e?e:e+"",i),s=(e,...t)=>{const r=1===e.length?e[0]:t.reduce(((t,r,o)=>t+(e=>{if(!0===e._$cssResult$)return e.cssText;if("number"==typeof e)return e;throw Error("Value passed to 'css' function must be a 'css' function result: "+e+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(r)+e[o+1]),e[0]);return new n(r,i)},c=(e,t)=>{o?e.adoptedStyleSheets=t.map((e=>e instanceof CSSStyleSheet?e:e.styleSheet)):t.forEach((t=>{const r=document.createElement("style");r.textContent=t.cssText,e.appendChild(r)}))},d=o?e=>e:e=>e instanceof CSSStyleSheet?(e=>{let t="";for(const r of e.cssRules)t+=r.cssText;return l(t)})(e):e;var h,p,u,v;const m={toAttribute(e,t){switch(t){case Boolean:e=e?"":null;break;case Object:case Array:e=null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){let r=e;switch(t){case Boolean:r=null!==e;break;case Number:r=null===e?null:Number(e);break;case Object:case Array:try{r=JSON.parse(e)}catch(e){r=null}}return r}},f=(e,t)=>t!==e&&(t==t||e==e),b={attribute:!0,type:String,converter:m,reflect:!1,hasChanged:f};class g extends HTMLElement{constructor(){super(),this._$Et=new Map,this.isUpdatePending=!1,this.hasUpdated=!1,this._$Ei=null,this.o()}static addInitializer(e){var t;null!==(t=this.l)&&void 0!==t||(this.l=[]),this.l.push(e)}static get observedAttributes(){this.finalize();const e=[];return this.elementProperties.forEach(((t,r)=>{const o=this._$Eh(r,t);void 0!==o&&(this._$Eu.set(o,r),e.push(o))})),e}static createProperty(e,t=b){if(t.state&&(t.attribute=!1),this.finalize(),this.elementProperties.set(e,t),!t.noAccessor&&!this.prototype.hasOwnProperty(e)){const r="symbol"==typeof e?Symbol():"__"+e,o=this.getPropertyDescriptor(e,r,t);void 0!==o&&Object.defineProperty(this.prototype,e,o)}}static getPropertyDescriptor(e,t,r){return{get(){return this[t]},set(o){const i=this[e];this[t]=o,this.requestUpdate(e,i,r)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)||b}static finalize(){if(this.hasOwnProperty("finalized"))return!1;this.finalized=!0;const e=Object.getPrototypeOf(this);if(e.finalize(),this.elementProperties=new Map(e.elementProperties),this._$Eu=new Map,this.hasOwnProperty("properties")){const e=this.properties,t=[...Object.getOwnPropertyNames(e),...Object.getOwnPropertySymbols(e)];for(const r of t)this.createProperty(r,e[r])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(e){const t=[];if(Array.isArray(e)){const r=new Set(e.flat(1/0).reverse());for(const e of r)t.unshift(d(e))}else void 0!==e&&t.push(d(e));return t}static _$Eh(e,t){const r=t.attribute;return!1===r?void 0:"string"==typeof r?r:"string"==typeof e?e.toLowerCase():void 0}o(){var e;this._$Ev=new Promise((e=>this.enableUpdating=e)),this._$AL=new Map,this._$Ep(),this.requestUpdate(),null===(e=this.constructor.l)||void 0===e||e.forEach((e=>e(this)))}addController(e){var t,r;(null!==(t=this._$Em)&&void 0!==t?t:this._$Em=[]).push(e),void 0!==this.renderRoot&&this.isConnected&&(null===(r=e.hostConnected)||void 0===r||r.call(e))}removeController(e){var t;null===(t=this._$Em)||void 0===t||t.splice(this._$Em.indexOf(e)>>>0,1)}_$Ep(){this.constructor.elementProperties.forEach(((e,t)=>{this.hasOwnProperty(t)&&(this._$Et.set(t,this[t]),delete this[t])}))}createRenderRoot(){var e;const t=null!==(e=this.shadowRoot)&&void 0!==e?e:this.attachShadow(this.constructor.shadowRootOptions);return c(t,this.constructor.elementStyles),t}connectedCallback(){var e;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null===(e=this._$Em)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostConnected)||void 0===t?void 0:t.call(e)}))}enableUpdating(e){}disconnectedCallback(){var e;null===(e=this._$Em)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostDisconnected)||void 0===t?void 0:t.call(e)}))}attributeChangedCallback(e,t,r){this._$AK(e,r)}_$Eg(e,t,r=b){var o,i;const a=this.constructor._$Eh(e,r);if(void 0!==a&&!0===r.reflect){const n=(null!==(i=null===(o=r.converter)||void 0===o?void 0:o.toAttribute)&&void 0!==i?i:m.toAttribute)(t,r.type);this._$Ei=e,null==n?this.removeAttribute(a):this.setAttribute(a,n),this._$Ei=null}}_$AK(e,t){var r,o,i;const a=this.constructor,n=a._$Eu.get(e);if(void 0!==n&&this._$Ei!==n){const e=a.getPropertyOptions(n),l=e.converter,s=null!==(i=null!==(o=null===(r=l)||void 0===r?void 0:r.fromAttribute)&&void 0!==o?o:"function"==typeof l?l:null)&&void 0!==i?i:m.fromAttribute;this._$Ei=n,this[n]=s(t,e.type),this._$Ei=null}}requestUpdate(e,t,r){let o=!0;void 0!==e&&(((r=r||this.constructor.getPropertyOptions(e)).hasChanged||f)(this[e],t)?(this._$AL.has(e)||this._$AL.set(e,t),!0===r.reflect&&this._$Ei!==e&&(void 0===this._$ES&&(this._$ES=new Map),this._$ES.set(e,r))):o=!1),!this.isUpdatePending&&o&&(this._$Ev=this._$EC())}async _$EC(){this.isUpdatePending=!0;try{await this._$Ev}catch(e){Promise.reject(e)}const e=this.performUpdate();return null!=e&&await e,!this.isUpdatePending}performUpdate(){var e;if(!this.isUpdatePending)return;this.hasUpdated,this._$Et&&(this._$Et.forEach(((e,t)=>this[t]=e)),this._$Et=void 0);let t=!1;const r=this._$AL;try{t=this.shouldUpdate(r),t?(this.willUpdate(r),null===(e=this._$Em)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostUpdate)||void 0===t?void 0:t.call(e)})),this.update(r)):this._$E_()}catch(e){throw t=!1,this._$E_(),e}t&&this._$AE(r)}willUpdate(e){}_$AE(e){var t;null===(t=this._$Em)||void 0===t||t.forEach((e=>{var t;return null===(t=e.hostUpdated)||void 0===t?void 0:t.call(e)})),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}_$E_(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$Ev}shouldUpdate(e){return!0}update(e){void 0!==this._$ES&&(this._$ES.forEach(((e,t)=>this._$Eg(t,this[t],e))),this._$ES=void 0),this._$E_()}updated(e){}firstUpdated(e){}}g.finalized=!0,g.elementProperties=new Map,g.elementStyles=[],g.shadowRootOptions={mode:"open"},null===(p=(h=globalThis).reactiveElementPlatformSupport)||void 0===p||p.call(h,{ReactiveElement:g}),(null!==(u=(v=globalThis).reactiveElementVersions)&&void 0!==u?u:v.reactiveElementVersions=[]).push("1.0.0-rc.3")},29561:(e,t,r)=>{"use strict";r.d(t,{iv:()=>c.iv,dy:()=>d.dy,YP:()=>d.YP,oi:()=>h});var o,i,a,n,l,s,c=r(25945),d=r(99602);class h extends c.fl{constructor(){super(...arguments),this.renderOptions={host:this},this._$Dt=void 0}createRenderRoot(){var e,t;const r=super.createRenderRoot();return null!==(e=(t=this.renderOptions).renderBefore)&&void 0!==e||(t.renderBefore=r.firstChild),r}update(e){const t=this.render();super.update(e),this._$Dt=(0,d.sY)(t,this.renderRoot,this.renderOptions)}connectedCallback(){var e;super.connectedCallback(),null===(e=this._$Dt)||void 0===e||e.setConnected(!0)}disconnectedCallback(){var e;super.disconnectedCallback(),null===(e=this._$Dt)||void 0===e||e.setConnected(!1)}render(){return d.Jb}}h.finalized=!0,h._$litElement$=!0,null===(i=(o=globalThis).litElementHydrateSupport)||void 0===i||i.call(o,{LitElement:h}),null===(n=(a=globalThis).litElementPlatformSupport)||void 0===n||n.call(a,{LitElement:h});(null!==(l=(s=globalThis).litElementVersions)&&void 0!==l?l:s.litElementVersions=[]).push("3.0.0-rc.3")},99602:(e,t,r)=>{"use strict";var o,i,a,n;r.d(t,{dy:()=>E,Jb:()=>S,sY:()=>T,YP:()=>k});const l=globalThis.trustedTypes,s=l?l.createPolicy("lit-html",{createHTML:e=>e}):void 0,c=`lit$${(Math.random()+"").slice(9)}$`,d="?"+c,h=`<${d}>`,p=document,u=(e="")=>p.createComment(e),v=e=>null===e||"object"!=typeof e&&"function"!=typeof e,m=Array.isArray,f=e=>{var t;return m(e)||"function"==typeof(null===(t=e)||void 0===t?void 0:t[Symbol.iterator])},b=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,g=/-->/g,y=/>/g,_=/>|[ 	\n\r](?:([^\s"'>=/]+)([ 	\n\r]*=[ 	\n\r]*(?:[^ 	\n\r"'`<>=]|("|')|))|$)/g,$=/'/g,w=/"/g,x=/^(?:script|style|textarea)$/i,A=e=>(t,...r)=>({_$litType$:e,strings:t,values:r}),E=A(1),k=A(2),S=Symbol.for("lit-noChange"),C=Symbol.for("lit-nothing"),P=new WeakMap,T=(e,t,r)=>{var o,i;const a=null!==(o=null==r?void 0:r.renderBefore)&&void 0!==o?o:t;let n=a._$litPart$;if(void 0===n){const e=null!==(i=null==r?void 0:r.renderBefore)&&void 0!==i?i:null;a._$litPart$=n=new M(t.insertBefore(u(),e),e,void 0,null!=r?r:{})}return n._$AI(e),n},U=p.createTreeWalker(p,129,null,!1),O=(e,t)=>{const r=e.length-1,o=[];let i,a=2===t?"<svg>":"",n=b;for(let t=0;t<r;t++){const r=e[t];let l,s,d=-1,p=0;for(;p<r.length&&(n.lastIndex=p,s=n.exec(r),null!==s);)p=n.lastIndex,n===b?"!--"===s[1]?n=g:void 0!==s[1]?n=y:void 0!==s[2]?(x.test(s[2])&&(i=RegExp("</"+s[2],"g")),n=_):void 0!==s[3]&&(n=_):n===_?">"===s[0]?(n=null!=i?i:b,d=-1):void 0===s[1]?d=-2:(d=n.lastIndex-s[2].length,l=s[1],n=void 0===s[3]?_:'"'===s[3]?w:$):n===w||n===$?n=_:n===g||n===y?n=b:(n=_,i=void 0);const u=n===_&&e[t+1].startsWith("/>")?" ":"";a+=n===b?r+h:d>=0?(o.push(l),r.slice(0,d)+"$lit$"+r.slice(d)+c+u):r+c+(-2===d?(o.push(void 0),t):u)}const l=a+(e[r]||"<?>")+(2===t?"</svg>":"");return[void 0!==s?s.createHTML(l):l,o]};class H{constructor({strings:e,_$litType$:t},r){let o;this.parts=[];let i=0,a=0;const n=e.length-1,s=this.parts,[h,p]=O(e,t);if(this.el=H.createElement(h,r),U.currentNode=this.el.content,2===t){const e=this.el.content,t=e.firstChild;t.remove(),e.append(...t.childNodes)}for(;null!==(o=U.nextNode())&&s.length<n;){if(1===o.nodeType){if(o.hasAttributes()){const e=[];for(const t of o.getAttributeNames())if(t.endsWith("$lit$")||t.startsWith(c)){const r=p[a++];if(e.push(t),void 0!==r){const e=o.getAttribute(r.toLowerCase()+"$lit$").split(c),t=/([.?@])?(.*)/.exec(r);s.push({type:1,index:i,name:t[2],strings:e,ctor:"."===t[1]?R:"?"===t[1]?L:"@"===t[1]?z:j})}else s.push({type:6,index:i})}for(const t of e)o.removeAttribute(t)}if(x.test(o.tagName)){const e=o.textContent.split(c),t=e.length-1;if(t>0){o.textContent=l?l.emptyScript:"";for(let r=0;r<t;r++)o.append(e[r],u()),U.nextNode(),s.push({type:2,index:++i});o.append(e[t],u())}}}else if(8===o.nodeType)if(o.data===d)s.push({type:2,index:i});else{let e=-1;for(;-1!==(e=o.data.indexOf(c,e+1));)s.push({type:7,index:i}),e+=c.length-1}i++}}static createElement(e,t){const r=p.createElement("template");return r.innerHTML=e,r}}function N(e,t,r=e,o){var i,a,n,l;if(t===S)return t;let s=void 0!==o?null===(i=r._$Cl)||void 0===i?void 0:i[o]:r._$Cu;const c=v(t)?void 0:t._$litDirective$;return(null==s?void 0:s.constructor)!==c&&(null===(a=null==s?void 0:s._$AO)||void 0===a||a.call(s,!1),void 0===c?s=void 0:(s=new c(e),s._$AT(e,r,o)),void 0!==o?(null!==(n=(l=r)._$Cl)&&void 0!==n?n:l._$Cl=[])[o]=s:r._$Cu=s),void 0!==s&&(t=N(e,s._$AS(e,t.values),s,o)),t}class B{constructor(e,t){this.v=[],this._$AN=void 0,this._$AD=e,this._$AM=t}get _$AU(){return this._$AM._$AU}p(e){var t;const{el:{content:r},parts:o}=this._$AD,i=(null!==(t=null==e?void 0:e.creationScope)&&void 0!==t?t:p).importNode(r,!0);U.currentNode=i;let a=U.nextNode(),n=0,l=0,s=o[0];for(;void 0!==s;){if(n===s.index){let t;2===s.type?t=new M(a,a.nextSibling,this,e):1===s.type?t=new s.ctor(a,s.name,s.strings,this,e):6===s.type&&(t=new D(a,this,e)),this.v.push(t),s=o[++l]}n!==(null==s?void 0:s.index)&&(a=U.nextNode(),n++)}return i}m(e){let t=0;for(const r of this.v)void 0!==r&&(void 0!==r.strings?(r._$AI(e,r,t),t+=r.strings.length-2):r._$AI(e[t])),t++}}class M{constructor(e,t,r,o){this.type=2,this._$C_=!0,this._$AN=void 0,this._$AA=e,this._$AB=t,this._$AM=r,this.options=o}get _$AU(){var e,t;return null!==(t=null===(e=this._$AM)||void 0===e?void 0:e._$AU)&&void 0!==t?t:this._$C_}get parentNode(){return this._$AA.parentNode}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(e,t=this){e=N(this,e,t),v(e)?e===C||null==e||""===e?(this._$AH!==C&&this._$AR(),this._$AH=C):e!==this._$AH&&e!==S&&this.$(e):void 0!==e._$litType$?this.T(e):void 0!==e.nodeType?this.A(e):f(e)?this.M(e):this.$(e)}C(e,t=this._$AB){return this._$AA.parentNode.insertBefore(e,t)}A(e){this._$AH!==e&&(this._$AR(),this._$AH=this.C(e))}$(e){const t=this._$AA.nextSibling;null!==t&&3===t.nodeType&&(null===this._$AB?null===t.nextSibling:t===this._$AB.previousSibling)?t.data=e:this.A(p.createTextNode(e)),this._$AH=e}T(e){var t;const{values:r,_$litType$:o}=e,i="number"==typeof o?this._$AC(e):(void 0===o.el&&(o.el=H.createElement(o.h,this.options)),o);if((null===(t=this._$AH)||void 0===t?void 0:t._$AD)===i)this._$AH.m(r);else{const e=new B(i,this),t=e.p(this.options);e.m(r),this.A(t),this._$AH=e}}_$AC(e){let t=P.get(e.strings);return void 0===t&&P.set(e.strings,t=new H(e)),t}M(e){m(this._$AH)||(this._$AH=[],this._$AR());const t=this._$AH;let r,o=0;for(const i of e)o===t.length?t.push(r=new M(this.C(u()),this.C(u()),this,this.options)):r=t[o],r._$AI(i),o++;o<t.length&&(this._$AR(r&&r._$AB.nextSibling,o),t.length=o)}_$AR(e=this._$AA.nextSibling,t){var r;for(null===(r=this._$AP)||void 0===r||r.call(this,!1,!0,t);e&&e!==this._$AB;){const t=e.nextSibling;e.remove(),e=t}}setConnected(e){var t;void 0===this._$AM&&(this._$C_=e,null===(t=this._$AP)||void 0===t||t.call(this,e))}}class j{constructor(e,t,r,o,i){this.type=1,this._$AH=C,this._$AN=void 0,this.element=e,this.name=t,this._$AM=o,this.options=i,r.length>2||""!==r[0]||""!==r[1]?(this._$AH=Array(r.length-1).fill(C),this.strings=r):this._$AH=C}get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}_$AI(e,t=this,r,o){const i=this.strings;let a=!1;if(void 0===i)e=N(this,e,t,0),a=!v(e)||e!==this._$AH&&e!==S,a&&(this._$AH=e);else{const o=e;let n,l;for(e=i[0],n=0;n<i.length-1;n++)l=N(this,o[r+n],t,n),l===S&&(l=this._$AH[n]),a||(a=!v(l)||l!==this._$AH[n]),l===C?e=C:e!==C&&(e+=(null!=l?l:"")+i[n+1]),this._$AH[n]=l}a&&!o&&this.P(e)}P(e){e===C?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=e?e:"")}}class R extends j{constructor(){super(...arguments),this.type=3}P(e){this.element[this.name]=e===C?void 0:e}}class L extends j{constructor(){super(...arguments),this.type=4}P(e){e&&e!==C?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name)}}class z extends j{constructor(){super(...arguments),this.type=5}_$AI(e,t=this){var r;if((e=null!==(r=N(this,e,t,0))&&void 0!==r?r:C)===S)return;const o=this._$AH,i=e===C&&o!==C||e.capture!==o.capture||e.once!==o.once||e.passive!==o.passive,a=e!==C&&(o===C||i);i&&this.element.removeEventListener(this.name,this,o),a&&this.element.addEventListener(this.name,this,e),this._$AH=e}handleEvent(e){var t,r;"function"==typeof this._$AH?this._$AH.call(null!==(r=null===(t=this.options)||void 0===t?void 0:t.host)&&void 0!==r?r:this.element,e):this._$AH.handleEvent(e)}}class D{constructor(e,t,r){this.element=e,this.type=6,this._$AN=void 0,this._$AM=t,this.options=r}get _$AU(){return this._$AM._$AU}_$AI(e){N(this,e)}}null===(i=(o=globalThis).litHtmlPlatformSupport)||void 0===i||i.call(o,H,M),(null!==(a=(n=globalThis).litHtmlVersions)&&void 0!==a?a:n.litHtmlVersions=[]).push("2.0.0-rc.4")},50424:(e,t,r)=>{"use strict";r.d(t,{oi:()=>o.oi,iv:()=>o.iv,dy:()=>o.dy,YP:()=>o.YP});r(25945),r(99602);var o=r(29561)},47181:(e,t,r)=>{"use strict";r.d(t,{B:()=>o});const o=(e,t,r,o)=>{o=o||{},r=null==r?{}:r;const i=new Event(t,{bubbles:void 0===o.bubbles||o.bubbles,cancelable:Boolean(o.cancelable),composed:void 0===o.composed||o.composed});return i.detail=r,e.dispatchEvent(i),i}},37846:()=>{if(/^((?!chrome|android).)*version\/14\.0\s.*safari/i.test(navigator.userAgent)){const e=window.Element.prototype.attachShadow;window.Element.prototype.attachShadow=function(t){return t&&t.delegatesFocus&&delete t.delegatesFocus,e.apply(this,[t])}}},11654:(e,t,r)=>{"use strict";r.d(t,{_l:()=>i,q0:()=>a,Qx:()=>l,e$:()=>s});var o=r(50424);const i={"primary-background-color":"#111111","card-background-color":"#1c1c1c","secondary-background-color":"#202020","primary-text-color":"#e1e1e1","secondary-text-color":"#9b9b9b","disabled-text-color":"#6f6f6f","app-header-text-color":"#e1e1e1","app-header-background-color":"#101e24","switch-unchecked-button-color":"#999999","switch-unchecked-track-color":"#9b9b9b","divider-color":"rgba(225, 225, 225, .12)","mdc-ripple-color":"#AAAAAA","codemirror-keyword":"#C792EA","codemirror-operator":"#89DDFF","codemirror-variable":"#f07178","codemirror-variable-2":"#EEFFFF","codemirror-variable-3":"#DECB6B","codemirror-builtin":"#FFCB6B","codemirror-atom":"#F78C6C","codemirror-number":"#FF5370","codemirror-def":"#82AAFF","codemirror-string":"#C3E88D","codemirror-string-2":"#f07178","codemirror-comment":"#545454","codemirror-tag":"#FF5370","codemirror-meta":"#FFCB6B","codemirror-attribute":"#C792EA","codemirror-property":"#C792EA","codemirror-qualifier":"#DECB6B","codemirror-type":"#DECB6B","energy-grid-return-color":"#b39bdb"},a={"state-icon-error-color":"var(--error-state-color, var(--error-color))","state-unavailable-color":"var(--state-icon-unavailable-color, var(--disabled-text-color))","sidebar-text-color":"var(--primary-text-color)","sidebar-background-color":"var(--card-background-color)","sidebar-selected-text-color":"var(--primary-color)","sidebar-selected-icon-color":"var(--primary-color)","sidebar-icon-color":"rgba(var(--rgb-primary-text-color), 0.6)","switch-checked-color":"var(--primary-color)","switch-checked-button-color":"var(--switch-checked-color, var(--primary-background-color))","switch-checked-track-color":"var(--switch-checked-color, #000000)","switch-unchecked-button-color":"var(--switch-unchecked-color, var(--primary-background-color))","switch-unchecked-track-color":"var(--switch-unchecked-color, #000000)","slider-color":"var(--primary-color)","slider-secondary-color":"var(--light-primary-color)","slider-track-color":"var(--scrollbar-thumb-color)","label-badge-background-color":"var(--card-background-color)","label-badge-text-color":"rgba(var(--rgb-primary-text-color), 0.8)","paper-listbox-background-color":"var(--card-background-color)","paper-item-icon-color":"var(--state-icon-color)","paper-item-icon-active-color":"var(--state-icon-active-color)","table-row-background-color":"var(--primary-background-color)","table-row-alternative-background-color":"var(--secondary-background-color)","paper-slider-knob-color":"var(--slider-color)","paper-slider-knob-start-color":"var(--slider-color)","paper-slider-pin-color":"var(--slider-color)","paper-slider-pin-start-color":"var(--slider-color)","paper-slider-active-color":"var(--slider-color)","paper-slider-secondary-color":"var(--slider-secondary-color)","paper-slider-container-color":"var(--slider-track-color)","data-table-background-color":"var(--card-background-color)","markdown-code-background-color":"var(--primary-background-color)","mdc-theme-primary":"var(--primary-color)","mdc-theme-secondary":"var(--accent-color)","mdc-theme-background":"var(--primary-background-color)","mdc-theme-surface":"var(--card-background-color)","mdc-theme-on-primary":"var(--text-primary-color)","mdc-theme-on-secondary":"var(--text-primary-color)","mdc-theme-on-surface":"var(--primary-text-color)","mdc-theme-text-disabled-on-light":"var(--disabled-text-color)","mdc-theme-text-primary-on-background":"var(--primary-text-color)","mdc-theme-text-secondary-on-background":"var(--secondary-text-color)","mdc-theme-text-icon-on-background":"var(--secondary-text-color)","app-header-text-color":"var(--text-primary-color)","app-header-background-color":"var(--primary-color)","mdc-checkbox-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-checkbox-disabled-color":"var(--disabled-text-color)","mdc-radio-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-radio-disabled-color":"var(--disabled-text-color)","mdc-tab-text-label-color-default":"var(--primary-text-color)","mdc-button-disabled-ink-color":"var(--disabled-text-color)","mdc-button-outline-color":"var(--divider-color)","mdc-dialog-scroll-divider-color":"var(--divider-color)","chip-background-color":"rgba(var(--rgb-primary-text-color), 0.15)","material-body-text-color":"var(--primary-text-color)","material-background-color":"var(--card-background-color)","material-secondary-background-color":"var(--secondary-background-color)","material-secondary-text-color":"var(--secondary-text-color)"},n=o.iv`
  button.link {
    background: none;
    color: inherit;
    border: none;
    padding: 0;
    font: inherit;
    text-align: left;
    text-decoration: underline;
    cursor: pointer;
  }
`,l=o.iv`
  :host {
    font-family: var(--paper-font-body1_-_font-family);
    -webkit-font-smoothing: var(--paper-font-body1_-_-webkit-font-smoothing);
    font-size: var(--paper-font-body1_-_font-size);
    font-weight: var(--paper-font-body1_-_font-weight);
    line-height: var(--paper-font-body1_-_line-height);
  }

  app-header-layout,
  ha-app-layout {
    background-color: var(--primary-background-color);
  }

  app-header,
  app-toolbar {
    background-color: var(--app-header-background-color);
    font-weight: 400;
    color: var(--app-header-text-color, white);
  }

  app-toolbar {
    height: var(--header-height);
  }

  app-header div[sticky] {
    height: 48px;
  }

  app-toolbar [main-title] {
    margin-left: 20px;
  }

  h1 {
    font-family: var(--paper-font-headline_-_font-family);
    -webkit-font-smoothing: var(--paper-font-headline_-_-webkit-font-smoothing);
    white-space: var(--paper-font-headline_-_white-space);
    overflow: var(--paper-font-headline_-_overflow);
    text-overflow: var(--paper-font-headline_-_text-overflow);
    font-size: var(--paper-font-headline_-_font-size);
    font-weight: var(--paper-font-headline_-_font-weight);
    line-height: var(--paper-font-headline_-_line-height);
  }

  h2 {
    font-family: var(--paper-font-title_-_font-family);
    -webkit-font-smoothing: var(--paper-font-title_-_-webkit-font-smoothing);
    white-space: var(--paper-font-title_-_white-space);
    overflow: var(--paper-font-title_-_overflow);
    text-overflow: var(--paper-font-title_-_text-overflow);
    font-size: var(--paper-font-title_-_font-size);
    font-weight: var(--paper-font-title_-_font-weight);
    line-height: var(--paper-font-title_-_line-height);
  }

  h3 {
    font-family: var(--paper-font-subhead_-_font-family);
    -webkit-font-smoothing: var(--paper-font-subhead_-_-webkit-font-smoothing);
    white-space: var(--paper-font-subhead_-_white-space);
    overflow: var(--paper-font-subhead_-_overflow);
    text-overflow: var(--paper-font-subhead_-_text-overflow);
    font-size: var(--paper-font-subhead_-_font-size);
    font-weight: var(--paper-font-subhead_-_font-weight);
    line-height: var(--paper-font-subhead_-_line-height);
  }

  a {
    color: var(--primary-color);
  }

  .secondary {
    color: var(--secondary-text-color);
  }

  .error {
    color: var(--error-color);
  }

  .warning {
    color: var(--error-color);
  }

  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }

  ${n}

  .card-actions a {
    text-decoration: none;
  }

  .card-actions .warning {
    --mdc-theme-primary: var(--error-color);
  }

  .layout.horizontal,
  .layout.vertical {
    display: flex;
  }
  .layout.inline {
    display: inline-flex;
  }
  .layout.horizontal {
    flex-direction: row;
  }
  .layout.vertical {
    flex-direction: column;
  }
  .layout.wrap {
    flex-wrap: wrap;
  }
  .layout.no-wrap {
    flex-wrap: nowrap;
  }
  .layout.center,
  .layout.center-center {
    align-items: center;
  }
  .layout.bottom {
    align-items: flex-end;
  }
  .layout.center-justified,
  .layout.center-center {
    justify-content: center;
  }
  .flex {
    flex: 1;
    flex-basis: 0.000000001px;
  }
  .flex-auto {
    flex: 1 1 auto;
  }
  .flex-none {
    flex: none;
  }
  .layout.justified {
    justify-content: space-between;
  }
`,s=(o.iv`
  /* prevent clipping of positioned elements */
  paper-dialog-scrollable {
    --paper-dialog-scrollable: {
      -webkit-overflow-scrolling: auto;
    }
  }

  /* force smooth scrolling for iOS 10 */
  paper-dialog-scrollable.can-scroll {
    --paper-dialog-scrollable: {
      -webkit-overflow-scrolling: touch;
    }
  }

  .paper-dialog-buttons {
    align-items: flex-end;
    padding: 8px;
    padding-bottom: max(env(safe-area-inset-bottom), 8px);
  }

  @media all and (min-width: 450px) and (min-height: 500px) {
    ha-paper-dialog {
      min-width: 400px;
    }
  }

  @media all and (max-width: 450px), all and (max-height: 500px) {
    paper-dialog,
    ha-paper-dialog {
      margin: 0;
      width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      min-width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      max-width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      max-height: calc(100% - var(--header-height));

      position: fixed !important;
      bottom: 0px;
      left: env(safe-area-inset-left);
      right: env(safe-area-inset-right);
      overflow: scroll;
      border-bottom-left-radius: 0px;
      border-bottom-right-radius: 0px;
    }
  }

  /* mwc-dialog (ha-dialog) styles */
  ha-dialog {
    --mdc-dialog-min-width: 400px;
    --mdc-dialog-max-width: 600px;
    --mdc-dialog-heading-ink-color: var(--primary-text-color);
    --mdc-dialog-content-ink-color: var(--primary-text-color);
    --justify-action-buttons: space-between;
  }

  ha-dialog .form {
    padding-bottom: 24px;
    color: var(--primary-text-color);
  }

  a {
    color: var(--primary-color);
  }

  /* make dialog fullscreen on small screens */
  @media all and (max-width: 450px), all and (max-height: 500px) {
    ha-dialog {
      --mdc-dialog-min-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-max-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-min-height: 100%;
      --mdc-dialog-max-height: 100%;
      --mdc-shape-medium: 0px;
      --vertial-align-dialog: flex-end;
    }
  }
  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }
  .error {
    color: var(--error-color);
  }
`,o.iv`
  .ha-scrollbar::-webkit-scrollbar {
    width: 0.4rem;
    height: 0.4rem;
  }

  .ha-scrollbar::-webkit-scrollbar-thumb {
    -webkit-border-radius: 4px;
    border-radius: 4px;
    background: var(--scrollbar-thumb-color);
  }

  .ha-scrollbar {
    overflow-y: auto;
    scrollbar-color: var(--scrollbar-thumb-color) transparent;
    scrollbar-width: thin;
  }
`,o.iv`
  body {
    background-color: var(--primary-background-color);
    color: var(--primary-text-color);
    height: calc(100vh - 32px);
    width: 100vw;
  }
`)}},o={};function i(e){var t=o[e];if(void 0!==t)return t.exports;var a=o[e]={exports:{}};return r[e](a,a.exports,i),a.exports}i.m=r,i.d=(e,t)=>{for(var r in t)i.o(t,r)&&!i.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},i.f={},i.e=e=>Promise.all(Object.keys(i.f).reduce(((t,r)=>(i.f[r](e,t),t)),[])),i.u=e=>({2678:"e76fca52",3835:"46b3d562",5453:"4078f8b2",6134:"a8f1b87a",8811:"838c68c3"}[e]+".js"),i.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),e={},t="home-assistant-frontend:",i.l=(r,o,a,n)=>{if(e[r])e[r].push(o);else{var l,s;if(void 0!==a)for(var c=document.getElementsByTagName("script"),d=0;d<c.length;d++){var h=c[d];if(h.getAttribute("src")==r||h.getAttribute("data-webpack")==t+a){l=h;break}}l||(s=!0,(l=document.createElement("script")).charset="utf-8",l.timeout=120,i.nc&&l.setAttribute("nonce",i.nc),l.setAttribute("data-webpack",t+a),l.src=r),e[r]=[o];var p=(t,o)=>{l.onerror=l.onload=null,clearTimeout(u);var i=e[r];if(delete e[r],l.parentNode&&l.parentNode.removeChild(l),i&&i.forEach((e=>e(o))),t)return t(o)},u=setTimeout(p.bind(null,void 0,{type:"timeout",target:l}),12e4);l.onerror=p.bind(null,l.onerror),l.onload=p.bind(null,l.onload),s&&document.head.appendChild(l)}},i.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},i.p="/frontend_latest/",(()=>{var e={8017:0};i.f.j=(t,r)=>{var o=i.o(e,t)?e[t]:void 0;if(0!==o)if(o)r.push(o[2]);else{var a=new Promise(((r,i)=>o=e[t]=[r,i]));r.push(o[2]=a);var n=i.p+i.u(t),l=new Error;i.l(n,(r=>{if(i.o(e,t)&&(0!==(o=e[t])&&(e[t]=void 0),o)){var a=r&&("load"===r.type?"missing":r.type),n=r&&r.target&&r.target.src;l.message="Loading chunk "+t+" failed.\n("+a+": "+n+")",l.name="ChunkLoadError",l.type=a,l.request=n,o[1](l)}}),"chunk-"+t,t)}};var t=(t,r)=>{var o,a,[n,l,s]=r,c=0;for(o in l)i.o(l,o)&&(i.m[o]=l[o]);if(s)s(i);for(t&&t(r);c<n.length;c++)a=n[c],i.o(e,a)&&e[a]&&e[a][0](),e[n[c]]=0},r=self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))})(),(()=>{"use strict";i(37846);var e=i(47181);const t=(e,t,r)=>new Promise(((o,i)=>{const a=document.createElement(e);let n="src",l="body";switch(a.onload=()=>o(t),a.onerror=()=>i(t),e){case"script":a.async=!0,r&&(a.type=r);break;case"link":a.type="text/css",a.rel="stylesheet",n="href",l="head"}a[n]=t,document[l].appendChild(a)})),r=e=>t("script",e),o="customElements"in window&&"content"in document.createElement("template"),a="ha-main-window",n=window.name===a?window:parent.name===a?parent:top;var l=i(11654);const s={},c=e=>{const o=(e=>e.html_url?{type:"html",url:e.html_url}:e.module_url&&e.js_url||e.module_url?{type:"module",url:e.module_url}:{type:"js",url:e.js_url})(e);return"js"===o.type?(o.url in s||(s[o.url]=r(o.url)),s[o.url]):"module"===o.type?(i=o.url,t("script",i,"module")):Promise.reject("No valid url found in panel config.");var i};let d,h;function p(e){h&&((e,t)=>{"setProperties"in e?e.setProperties(t):Object.keys(t).forEach((r=>{e[r]=t[r]}))})(h,e)}function u(t,a){const s=document.createElement("style");s.innerHTML="body { margin:0; } \n  @media (prefers-color-scheme: dark) {\n    body {\n      background-color: #111111;\n      color: #e1e1e1;\n    }\n  }",document.head.appendChild(s);const u=t.config._panel_custom;let v=Promise.resolve();o||(v=v.then((()=>r("/static/polyfills/webcomponents-bundle.js")))),v.then((()=>c(u))).then((()=>d||Promise.resolve())).then((()=>{h=(e=>{const t="html_url"in e?`ha-panel-${e.name}`:e.name;return document.createElement(t)})(u);h.addEventListener("hass-toggle-menu",(t=>{window.parent.customPanel&&(0,e.B)(window.parent.customPanel,t.type,t.detail)})),window.addEventListener("location-changed",(e=>{window.parent.customPanel&&window.parent.customPanel.navigate(window.location.pathname,e.detail)})),p({panel:t,...a}),document.body.appendChild(h)}),(e=>{let r;console.error(e,t),"hassio"===t.url_path?(Promise.all([i.e(5453),i.e(3835),i.e(6134),i.e(2678)]).then(i.bind(i,82678)),r=document.createElement("supervisor-error-screen")):(Promise.all([i.e(5453),i.e(6134),i.e(8811)]).then(i.bind(i,48811)),r=document.createElement("hass-error-screen"),r.error=`Unable to load the panel source: ${e}.`);const o=document.createElement("style");o.innerHTML=l.e$.cssText,document.body.appendChild(o),r.hass=a.hass,document.body.appendChild(r)})),document.body.addEventListener("click",(t=>{const r=(e=>{if(e.defaultPrevented||0!==e.button||e.metaKey||e.ctrlKey||e.shiftKey)return;const t=e.composedPath().filter((e=>"A"===e.tagName))[0];if(!t||t.target||t.hasAttribute("download")||"external"===t.getAttribute("rel"))return;let r=t.href;if(!r||-1!==r.indexOf("mailto:"))return;const o=window.location,i=o.origin||o.protocol+"//"+o.host;return 0===r.indexOf(i)&&(r=r.substr(i.length),"#"!==r)?(e.preventDefault(),r):void 0})(t);r&&((t,r)=>{const o=(null==r?void 0:r.replace)||!1;var i;o?n.history.replaceState(null!==(i=n.history.state)&&void 0!==i&&i.root?{root:!0}:null,"",t):n.history.pushState(null,"",t),(0,e.B)(n,"location-changed",{replace:o})})(r)}))}window.loadES5Adapter=()=>(d||(d=r("/static/polyfills/custom-elements-es5-adapter.js").catch()),d),document.addEventListener("DOMContentLoaded",(()=>window.parent.customPanel.registerIframe(u,p)),{once:!0})})()})();
//# sourceMappingURL=custom-panel.60f27280.js.map