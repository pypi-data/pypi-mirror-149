/*! For license information please see ac11fc07.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6074,5214],{63207:(e,t,i)=>{"use strict";i(65660),i(15112);var r=i(9672),n=i(87156),s=i(50856),o=i(94604);(0,r.k)({_template:s.d`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center-center;
        position: relative;

        vertical-align: middle;

        fill: var(--iron-icon-fill-color, currentcolor);
        stroke: var(--iron-icon-stroke-color, none);

        width: var(--iron-icon-width, 24px);
        height: var(--iron-icon-height, 24px);
        @apply --iron-icon;
      }

      :host([hidden]) {
        display: none;
      }
    </style>
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:o.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(e){var t=(e||"").split(":");this._iconName=t.pop(),this._iconsetName=t.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(e){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,n.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,n.vz)(this.root).appendChild(this._img))}})},15112:(e,t,i)=>{"use strict";i.d(t,{P:()=>n});i(94604);var r=i(9672);class n{constructor(e){n[" "](e),this.type=e&&e.type||"default",this.key=e&&e.key,e&&"value"in e&&(this.value=e.value)}get value(){var e=this.type,t=this.key;if(e&&t)return n.types[e]&&n.types[e][t]}set value(e){var t=this.type,i=this.key;t&&i&&(t=n.types[t]=n.types[t]||{},null==e?delete t[i]:t[i]=e)}get list(){if(this.type){var e=n.types[this.type];return e?Object.keys(e).map((function(e){return s[this.type][e]}),this):[]}}byKey(e){return this.key=e,this.value}}n[" "]=function(){},n.types={};var s=n.types;(0,r.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(e,t,i){var r=new n({type:e,key:t});return void 0!==i&&i!==r.value?r.value=i:this.value!==r.value&&(this.value=r.value),r},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(e){e&&(this.value=this)},byKey:function(e){return new n({type:this.type,key:e}).value}})},98626:(e,t,i)=>{"use strict";function r(e){return new Promise(((t,i)=>{e.oncomplete=e.onsuccess=()=>t(e.result),e.onabort=e.onerror=()=>i(e.error)}))}function n(e,t){const i=indexedDB.open(e);i.onupgradeneeded=()=>i.result.createObjectStore(t);const n=r(i);return(e,i)=>n.then((r=>i(r.transaction(t,e).objectStore(t))))}let s;function o(){return s||(s=n("keyval-store","keyval")),s}function a(e,t=o()){return t("readonly",(t=>r(t.get(e))))}function c(e,t,i=o()){return i("readwrite",(i=>(i.put(t,e),r(i.transaction))))}function l(e=o()){return e("readwrite",(e=>(e.clear(),r(e.transaction))))}i.d(t,{ZH:()=>l,MT:()=>n,U2:()=>a,RV:()=>r,t8:()=>c})},76666:(e,t,i)=>{"use strict";i.d(t,{$:()=>r.$});var r=i(81471)},82816:(e,t,i)=>{"use strict";i.d(t,{o:()=>r.o});var r=i(49629)},96305:(e,t,i)=>{"use strict";i.d(t,{v:()=>r});const r=(e,t)=>e&&Object.keys(e.services).filter((i=>t in e.services[i]))},77980:(e,t,i)=>{"use strict";i.r(t),i.d(t,{HaConfigServerControl:()=>g});i(53918),i(53268),i(12730),i(30879);var r=i(50424),n=i(55358),s=i(96305),o=(i(54909),i(22098),i(41886)),a=i(5986),c=(i(1359),i(11654)),l=(i(88165),i(29311));function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var s="static"===n?e:i;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!p(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var s=this.decorateConstructor(i,t);return r.push.apply(r,s.finishers),s.finishers=r,s},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,s=n.length-1;s>=0;s--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var a=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,n[s])(a)||a);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==s.finisher&&i.push(s.finisher),void 0!==s.elements){e=s.elements;for(var o=0;o<e.length-1;o++)for(var a=o+1;a<e.length;a++)if(e[o].key===e[a].key&&e[o].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return y(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?y(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=m(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:v(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=v(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function h(e){var t,i=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function u(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function v(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function y(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}let g=function(e,t,i,r){var n=d();if(r)for(var s=0;s<r.length;s++)n=r[s](n);var o=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},r=0;r<e.length;r++){var n,s=e[r];if("method"===s.kind&&(n=t.find(i)))if(f(s.descriptor)||f(n.descriptor)){if(p(s)||p(n))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");n.descriptor=s.descriptor}else{if(p(s)){if(p(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");n.decorators=s.decorators}u(s,n)}else t.push(s)}return t}(o.d.map(h)),e);return n.initializeClassElements(o.F,a.elements),n.runClassFinishers(o.F,a.finishers)}([(0,n.Mo)("ha-config-server-control")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"isWide",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"showAdvanced",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_validating",value:()=>!1},{kind:"field",decorators:[(0,n.SB)()],key:"_reloadableDomains",value:()=>[]},{kind:"field",key:"_validateLog",value:()=>""},{kind:"field",key:"_isValid",value:()=>null},{kind:"method",key:"updated",value:function(e){const t=e.get("hass");!e.has("hass")||t&&t.config.components===this.hass.config.components||(this._reloadableDomains=(0,s.v)(this.hass,"reload").sort())}},{kind:"method",key:"render",value:function(){return r.dy`
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        back-path="/config"
        .tabs=${l.configSections.general}
        .showAdvanced=${this.showAdvanced}
      >
        <ha-config-section .isWide=${this.isWide}>
          <span slot="header"
            >${this.hass.localize("ui.panel.config.server_control.caption")}</span
          >
          <span slot="introduction"
            >${this.hass.localize("ui.panel.config.server_control.description")}</span
          >

          ${this.showAdvanced?r.dy` <ha-card
                header=${this.hass.localize("ui.panel.config.server_control.section.validation.heading")}
              >
                <div class="card-content">
                  ${this.hass.localize("ui.panel.config.server_control.section.validation.introduction")}
                  ${this._validateLog?r.dy`
                        <div class="config-invalid">
                          <span class="text">
                            ${this.hass.localize("ui.panel.config.server_control.section.validation.invalid")}
                          </span>
                          <mwc-button raised @click=${this._validateConfig}>
                            ${this.hass.localize("ui.panel.config.server_control.section.validation.check_config")}
                          </mwc-button>
                        </div>
                        <div id="configLog" class="validate-log">
                          ${this._validateLog}
                        </div>
                      `:r.dy`
                        <div
                          class="validate-container layout vertical center-center"
                        >
                          ${this._validating?r.dy`
                                <ha-circular-progress
                                  active
                                ></ha-circular-progress>
                              `:r.dy`
                                ${this._isValid?r.dy` <div
                                      class="validate-result"
                                      id="result"
                                    >
                                      ${this.hass.localize("ui.panel.config.server_control.section.validation.valid")}
                                    </div>`:""}
                                <mwc-button
                                  raised
                                  @click=${this._validateConfig}
                                >
                                  ${this.hass.localize("ui.panel.config.server_control.section.validation.check_config")}
                                </mwc-button>
                              `}
                        </div>
                      `}
                </div>
              </ha-card>`:""}

          <ha-card
            header=${this.hass.localize("ui.panel.config.server_control.section.server_management.heading")}
          >
            <div class="card-content">
              ${this.hass.localize("ui.panel.config.server_control.section.server_management.introduction")}
            </div>
            <div class="card-actions warning">
              <ha-call-service-button
                class="warning"
                .hass=${this.hass}
                domain="homeassistant"
                service="restart"
                .confirmation=${this.hass.localize("ui.panel.config.server_control.section.server_management.confirm_restart")}
                >${this.hass.localize("ui.panel.config.server_control.section.server_management.restart")}
              </ha-call-service-button>
              <ha-call-service-button
                class="warning"
                .hass=${this.hass}
                domain="homeassistant"
                service="stop"
                confirmation=${this.hass.localize("ui.panel.config.server_control.section.server_management.confirm_stop")}
                >${this.hass.localize("ui.panel.config.server_control.section.server_management.stop")}
              </ha-call-service-button>
            </div>
          </ha-card>

          ${this.showAdvanced?r.dy`
                <ha-card
                  header=${this.hass.localize("ui.panel.config.server_control.section.reloading.heading")}
                >
                  <div class="card-content">
                    ${this.hass.localize("ui.panel.config.server_control.section.reloading.introduction")}
                  </div>
                  <div class="card-actions">
                    <ha-call-service-button
                      .hass=${this.hass}
                      domain="homeassistant"
                      service="reload_core_config"
                      >${this.hass.localize("ui.panel.config.server_control.section.reloading.core")}
                    </ha-call-service-button>
                  </div>
                  ${this._reloadableDomains.map((e=>r.dy`<div class="card-actions">
                        <ha-call-service-button
                          .hass=${this.hass}
                          .domain=${e}
                          service="reload"
                          >${this.hass.localize(`ui.panel.config.server_control.section.reloading.${e}`)||this.hass.localize("ui.panel.config.server_control.section.reloading.reload","domain",(0,a.Lh)(this.hass.localize,e))}
                        </ha-call-service-button>
                      </div>`))}
                </ha-card>
              `:""}
        </ha-config-section>
      </hass-tabs-subpage>
    `}},{kind:"method",key:"_validateConfig",value:async function(){this._validating=!0,this._validateLog="",this._isValid=null;const e=await(0,o.Ij)(this.hass);this._validating=!1,this._isValid="valid"===e.result,e.errors&&(this._validateLog=e.errors)}},{kind:"get",static:!0,key:"styles",value:function(){return[c.Qx,r.iv`
        .validate-container {
          height: 140px;
        }

        .validate-result {
          color: var(--success-color);
          font-weight: 500;
          margin-bottom: 1em;
        }

        .config-invalid {
          margin: 1em 0;
        }

        .config-invalid .text {
          color: var(--error-color);
          font-weight: 500;
        }

        .config-invalid mwc-button {
          float: right;
        }

        .validate-log {
          white-space: pre-line;
          direction: ltr;
        }

        ha-config-section {
          padding-bottom: 24px;
        }
      `]}}]}}),r.oi)}}]);
//# sourceMappingURL=ac11fc07.js.map