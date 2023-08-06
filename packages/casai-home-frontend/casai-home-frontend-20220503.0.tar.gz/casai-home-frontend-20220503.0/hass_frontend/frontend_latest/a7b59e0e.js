(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6938],{73826:(e,t,r)=>{"use strict";r.d(t,{f:()=>m});var a=r(55358);function i(e,t,r,a){var i=s();if(a)for(var d=0;d<a.length;d++)i=a[d](i);var u=t((function(e){i.initializeInstanceElements(e,h.elements)}),r),h=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},a=0;a<e.length;a++){var i,s=e[a];if("method"===s.kind&&(i=t.find(r)))if(c(s.descriptor)||c(i.descriptor)){if(n(s)||n(i))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");i.descriptor=s.descriptor}else{if(n(s)){if(n(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");i.decorators=s.decorators}l(s,i)}else t.push(s)}return t}(u.d.map(o)),e);return i.initializeClassElements(u.F,h.elements),i.runClassFinishers(u.F,h.finishers)}function s(){s=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(a){t.forEach((function(t){var i=t.placement;if(t.kind===a&&("static"===i||"prototype"===i)){var s="static"===i?e:r;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var a=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===a?void 0:a.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],a=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!n(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),a.push.apply(a,t.finishers)}),this),!t)return{elements:r,finishers:a};var s=this.decorateConstructor(r,t);return a.push.apply(a,s.finishers),s.finishers=a,s},addElementPlacement:function(e,t,r){var a=t[e.placement];if(!r&&-1!==a.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");a.push(e.key)},decorateElement:function(e,t){for(var r=[],a=[],i=e.decorators,s=i.length-1;s>=0;s--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var l=this.fromElementDescriptor(e),n=this.toElementFinisherExtras((0,i[s])(l)||l);e=n.element,this.addElementPlacement(e,t),n.finisher&&a.push(n.finisher);var c=n.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:a,extras:r}},decorateConstructor:function(e,t){for(var r=[],a=t.length-1;a>=0;a--){var i=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[a])(i)||i);if(void 0!==s.finisher&&r.push(s.finisher),void 0!==s.elements){e=s.elements;for(var o=0;o<e.length-1;o++)for(var l=o+1;l<e.length;l++)if(e[o].key===e[l].key&&e[o].placement===e[l].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=u(e.key),a=String(e.placement);if("static"!==a&&"prototype"!==a&&"own"!==a)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+a+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:r,placement:a,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:d(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=d(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var a=(0,t[r])(e);if(void 0!==a){if("function"!=typeof a)throw new TypeError("Finishers must return a constructor.");e=a}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function o(e){var t,r=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var a={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(a.decorators=e.decorators),"field"===e.kind&&(a.initializer=e.value),a}function l(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function n(e){return e.decorators&&e.decorators.length}function c(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function d(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var a=r.call(e,t||"default");if("object"!=typeof a)return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,a=new Array(t);r<t;r++)a[r]=e[r];return a}function p(e,t,r){return(p="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var a=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=f(e)););return e}(e,t);if(a){var i=Object.getOwnPropertyDescriptor(a,t);return i.get?i.get.call(r):i.value}})(e,t,r||e)}function f(e){return(f=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}const m=e=>i(null,(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,a.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",key:"__unsubs",value:void 0},{kind:"method",key:"connectedCallback",value:function(){p(f(r.prototype),"connectedCallback",this).call(this),this.__checkSubscribed()}},{kind:"method",key:"disconnectedCallback",value:function(){if(p(f(r.prototype),"disconnectedCallback",this).call(this),this.__unsubs){for(;this.__unsubs.length;){const e=this.__unsubs.pop();e instanceof Promise?e.then((e=>e())):e()}this.__unsubs=void 0}}},{kind:"method",key:"updated",value:function(e){p(f(r.prototype),"updated",this).call(this,e),e.has("hass")&&this.__checkSubscribed()}},{kind:"method",key:"hassSubscribe",value:function(){return[]}},{kind:"method",key:"__checkSubscribed",value:function(){void 0===this.__unsubs&&this.isConnected&&void 0!==this.hass&&(this.__unsubs=this.hassSubscribe())}}]}}),e)},16938:(e,t,r)=>{"use strict";r.r(t),r.d(t,{HuiEnergySourcesTableCard:()=>k});var a=r(23512),i=r(50424),s=r(55358),o=r(92483),l=r(15838),n=r(89525),c=r(91741),d=r(45524),u=(r(17595),r(22098),r(55424)),h=r(58763),p=r(73826);function f(){f=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(a){t.forEach((function(t){var i=t.placement;if(t.kind===a&&("static"===i||"prototype"===i)){var s="static"===i?e:r;this.defineClassElement(s,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var a=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===a?void 0:a.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],a=[],i={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,i)}),this),e.forEach((function(e){if(!_(e))return r.push(e);var t=this.decorateElement(e,i);r.push(t.element),r.push.apply(r,t.extras),a.push.apply(a,t.finishers)}),this),!t)return{elements:r,finishers:a};var s=this.decorateConstructor(r,t);return a.push.apply(a,s.finishers),s.finishers=a,s},addElementPlacement:function(e,t,r){var a=t[e.placement];if(!r&&-1!==a.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");a.push(e.key)},decorateElement:function(e,t){for(var r=[],a=[],i=e.decorators,s=i.length-1;s>=0;s--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var l=this.fromElementDescriptor(e),n=this.toElementFinisherExtras((0,i[s])(l)||l);e=n.element,this.addElementPlacement(e,t),n.finisher&&a.push(n.finisher);var c=n.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:a,extras:r}},decorateConstructor:function(e,t){for(var r=[],a=t.length-1;a>=0;a--){var i=this.fromClassDescriptor(e),s=this.toClassDescriptor((0,t[a])(i)||i);if(void 0!==s.finisher&&r.push(s.finisher),void 0!==s.elements){e=s.elements;for(var o=0;o<e.length-1;o++)for(var l=o+1;l<e.length;l++)if(e[o].key===e[l].key&&e[o].placement===e[l].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return w(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?w(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=g(e.key),a=String(e.placement);if("static"!==a&&"prototype"!==a&&"own"!==a)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+a+'"');var i=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var s={kind:t,key:r,placement:a,descriptor:Object.assign({},i)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(i,"get","The property descriptor of a field descriptor"),this.disallowProperty(i,"set","The property descriptor of a field descriptor"),this.disallowProperty(i,"value","The property descriptor of a field descriptor"),s.initializer=e.initializer),s},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:v(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=v(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var a=(0,t[r])(e);if(void 0!==a){if("function"!=typeof a)throw new TypeError("Finishers must return a constructor.");e=a}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function m(e){var t,r=g(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var a={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(a.decorators=e.decorators),"field"===e.kind&&(a.initializer=e.value),a}function y(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function _(e){return e.decorators&&e.decorators.length}function b(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function v(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function g(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var a=r.call(e,t||"default");if("object"!=typeof a)return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function w(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,a=new Array(t);r<t;r++)a[r]=e[r];return a}let k=function(e,t,r,a){var i=f();if(a)for(var s=0;s<a.length;s++)i=a[s](i);var o=t((function(e){i.initializeInstanceElements(e,l.elements)}),r),l=i.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===s.key&&e.placement===s.placement},a=0;a<e.length;a++){var i,s=e[a];if("method"===s.kind&&(i=t.find(r)))if(b(s.descriptor)||b(i.descriptor)){if(_(s)||_(i))throw new ReferenceError("Duplicated methods ("+s.key+") can't be decorated.");i.descriptor=s.descriptor}else{if(_(s)){if(_(i))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+s.key+").");i.decorators=s.decorators}y(s,i)}else t.push(s)}return t}(o.d.map(m)),e);return i.initializeClassElements(o.F,l.elements),i.runClassFinishers(o.F,l.finishers)}([(0,s.Mo)("hui-energy-sources-table-card")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,s.SB)()],key:"_data",value:void 0},{kind:"method",key:"hassSubscribe",value:function(){var e;return[(0,u.UB)(this.hass,{key:null===(e=this._config)||void 0===e?void 0:e.collection_key}).subscribe((e=>{this._data=e}))]}},{kind:"method",key:"getCardSize",value:function(){return 3}},{kind:"method",key:"setConfig",value:function(e){this._config=e}},{kind:"method",key:"render",value:function(){var e,t,r,a,s,p,f;if(!this.hass||!this._config)return i.dy``;if(!this._data)return i.dy`Loading...`;let m=0,y=0,_=0,b=0,v=0,g=0;const w=(0,u.Jj)(this._data.prefs),k=getComputedStyle(this),E=k.getPropertyValue("--energy-solar-color").trim(),C=k.getPropertyValue("--energy-battery-out-color").trim(),P=k.getPropertyValue("--energy-battery-in-color").trim(),$=k.getPropertyValue("--energy-grid-return-color").trim(),S=k.getPropertyValue("--energy-grid-consumption-color").trim(),D=k.getPropertyValue("--energy-gas-color").trim(),A=(null===(e=w.grid)||void 0===e?void 0:e[0].flow_from.some((e=>e.stat_cost||e.entity_energy_price||e.number_energy_price)))||(null===(t=w.grid)||void 0===t?void 0:t[0].flow_to.some((e=>e.stat_compensation||e.entity_energy_price||e.number_energy_price)))||(null===(r=w.gas)||void 0===r?void 0:r.some((e=>e.stat_cost||e.entity_energy_price||e.number_energy_price)));return i.dy` <ha-card>
      ${this._config.title?i.dy`<h1 class="card-header">${this._config.title}</h1>`:""}
      <div class="mdc-data-table">
        <div class="mdc-data-table__table-container">
          <table class="mdc-data-table__table" aria-label="Energy sources">
            <thead>
              <tr class="mdc-data-table__header-row">
                <th class="mdc-data-table__header-cell"></th>
                <th
                  class="mdc-data-table__header-cell"
                  role="columnheader"
                  scope="col"
                >
                  Source
                </th>
                <th
                  class="mdc-data-table__header-cell mdc-data-table__header-cell--numeric"
                  role="columnheader"
                  scope="col"
                >
                  Energy
                </th>
                ${A?i.dy` <th
                      class="mdc-data-table__header-cell mdc-data-table__header-cell--numeric"
                      role="columnheader"
                      scope="col"
                    >
                      Cost
                    </th>`:""}
              </tr>
            </thead>
            <tbody class="mdc-data-table__content">
              ${null===(a=w.solar)||void 0===a?void 0:a.map(((e,t)=>{const r=this.hass.states[e.stat_energy_from],a=(0,h.Kj)(this._data.stats[e.stat_energy_from])||0;_+=a;const s=t>0?(0,l.CO)((0,l.p3)((0,n.W)((0,l.Rw)((0,l.wK)(E)),t))):E;return i.dy`<tr class="mdc-data-table__row">
                  <td class="mdc-data-table__cell cell-bullet">
                    <div
                      class="bullet"
                      style=${(0,o.V)({borderColor:s,backgroundColor:s+"7F"})}
                    ></div>
                  </td>
                  <th class="mdc-data-table__cell" scope="row">
                    ${r?(0,c.C)(r):e.stat_energy_from}
                  </th>
                  <td
                    class="mdc-data-table__cell mdc-data-table__cell--numeric"
                  >
                    ${(0,d.u)(a,this.hass.locale)} kWh
                  </td>
                  ${A?i.dy`<td class="mdc-data-table__cell"></td>`:""}
                </tr>`}))}
              ${w.solar?i.dy`<tr class="mdc-data-table__row total">
                    <td class="mdc-data-table__cell"></td>
                    <th class="mdc-data-table__cell" scope="row">
                      Solar total
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${(0,d.u)(_,this.hass.locale)} kWh
                    </td>
                    ${A?i.dy`<td class="mdc-data-table__cell"></td>`:""}
                  </tr>`:""}
              ${null===(s=w.battery)||void 0===s?void 0:s.map(((e,t)=>{const r=this.hass.states[e.stat_energy_from],a=this.hass.states[e.stat_energy_to],s=(0,h.Kj)(this._data.stats[e.stat_energy_from])||0,u=(0,h.Kj)(this._data.stats[e.stat_energy_to])||0;b+=s-u;const p=t>0?(0,l.CO)((0,l.p3)((0,n.W)((0,l.Rw)((0,l.wK)(C)),t))):C,f=t>0?(0,l.CO)((0,l.p3)((0,n.W)((0,l.Rw)((0,l.wK)(P)),t))):P;return i.dy`<tr class="mdc-data-table__row">
                    <td class="mdc-data-table__cell cell-bullet">
                      <div
                        class="bullet"
                        style=${(0,o.V)({borderColor:p,backgroundColor:p+"7F"})}
                      ></div>
                    </td>
                    <th class="mdc-data-table__cell" scope="row">
                      ${r?(0,c.C)(r):e.stat_energy_from}
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${(0,d.u)(s,this.hass.locale)} kWh
                    </td>
                    ${A?i.dy`<td class="mdc-data-table__cell"></td>`:""}
                  </tr>
                  <tr class="mdc-data-table__row">
                    <td class="mdc-data-table__cell cell-bullet">
                      <div
                        class="bullet"
                        style=${(0,o.V)({borderColor:f,backgroundColor:f+"7F"})}
                      ></div>
                    </td>
                    <th class="mdc-data-table__cell" scope="row">
                      ${a?(0,c.C)(a):e.stat_energy_from}
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${(0,d.u)(-1*u,this.hass.locale)} kWh
                    </td>
                    ${A?i.dy`<td class="mdc-data-table__cell"></td>`:""}
                  </tr>`}))}
              ${w.battery?i.dy`<tr class="mdc-data-table__row total">
                    <td class="mdc-data-table__cell"></td>
                    <th class="mdc-data-table__cell" scope="row">
                      Battery total
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${(0,d.u)(b,this.hass.locale)} kWh
                    </td>
                    ${A?i.dy`<td class="mdc-data-table__cell"></td>`:""}
                  </tr>`:""}
              ${null===(p=w.grid)||void 0===p?void 0:p.map((e=>i.dy`${e.flow_from.map(((e,t)=>{const r=this.hass.states[e.stat_energy_from],a=(0,h.Kj)(this._data.stats[e.stat_energy_from])||0;m+=a;const s=e.stat_cost||this._data.info.cost_sensors[e.stat_energy_from],u=s?(0,h.Kj)(this._data.stats[s])||0:null;null!==u&&(y+=u);const p=t>0?(0,l.CO)((0,l.p3)((0,n.W)((0,l.Rw)((0,l.wK)(S)),t))):S;return i.dy`<tr class="mdc-data-table__row">
                    <td class="mdc-data-table__cell cell-bullet">
                      <div
                        class="bullet"
                        style=${(0,o.V)({borderColor:p,backgroundColor:p+"7F"})}
                      ></div>
                    </td>
                    <th class="mdc-data-table__cell" scope="row">
                      ${r?(0,c.C)(r):e.stat_energy_from}
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${(0,d.u)(a,this.hass.locale)} kWh
                    </td>
                    ${A?i.dy` <td
                          class="mdc-data-table__cell mdc-data-table__cell--numeric"
                        >
                          ${null!==u?(0,d.u)(u,this.hass.locale,{style:"currency",currency:this.hass.config.currency}):""}
                        </td>`:""}
                  </tr>`}))}
                ${e.flow_to.map(((e,t)=>{const r=this.hass.states[e.stat_energy_to],a=-1*((0,h.Kj)(this._data.stats[e.stat_energy_to])||0);m+=a;const s=e.stat_compensation||this._data.info.cost_sensors[e.stat_energy_to],u=s?-1*((0,h.Kj)(this._data.stats[s])||0):null;null!==u&&(y+=u);const p=t>0?(0,l.CO)((0,l.p3)((0,n.W)((0,l.Rw)((0,l.wK)($)),t))):$;return i.dy`<tr class="mdc-data-table__row">
                    <td class="mdc-data-table__cell cell-bullet">
                      <div
                        class="bullet"
                        style=${(0,o.V)({borderColor:p,backgroundColor:p+"7F"})}
                      ></div>
                    </td>
                    <th class="mdc-data-table__cell" scope="row">
                      ${r?(0,c.C)(r):e.stat_energy_to}
                    </th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${(0,d.u)(a,this.hass.locale)} kWh
                    </td>
                    ${A?i.dy` <td
                          class="mdc-data-table__cell mdc-data-table__cell--numeric"
                        >
                          ${null!==u?(0,d.u)(u,this.hass.locale,{style:"currency",currency:this.hass.config.currency}):""}
                        </td>`:""}
                  </tr>`}))}`))}
              ${w.grid?i.dy` <tr class="mdc-data-table__row total">
                    <td class="mdc-data-table__cell"></td>
                    <th class="mdc-data-table__cell" scope="row">Grid total</th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${(0,d.u)(m,this.hass.locale)} kWh
                    </td>
                    ${A?i.dy`<td
                          class="mdc-data-table__cell mdc-data-table__cell--numeric"
                        >
                          ${(0,d.u)(y,this.hass.locale,{style:"currency",currency:this.hass.config.currency})}
                        </td>`:""}
                  </tr>`:""}
              ${null===(f=w.gas)||void 0===f?void 0:f.map(((e,t)=>{const r=this.hass.states[e.stat_energy_from],a=(0,h.Kj)(this._data.stats[e.stat_energy_from])||0;v+=a;const s=e.stat_cost||this._data.info.cost_sensors[e.stat_energy_from],u=s?(0,h.Kj)(this._data.stats[s])||0:null;null!==u&&(g+=u);const p=t>0?(0,l.CO)((0,l.p3)((0,n.W)((0,l.Rw)((0,l.wK)(D)),t))):D;return i.dy`<tr class="mdc-data-table__row">
                  <td class="mdc-data-table__cell cell-bullet">
                    <div
                      class="bullet"
                      style=${(0,o.V)({borderColor:p,backgroundColor:p+"7F"})}
                    ></div>
                  </td>
                  <th class="mdc-data-table__cell" scope="row">
                    ${r?(0,c.C)(r):e.stat_energy_from}
                  </th>
                  <td
                    class="mdc-data-table__cell mdc-data-table__cell--numeric"
                  >
                    ${(0,d.u)(a,this.hass.locale)} m³
                  </td>
                  ${A?i.dy`<td
                        class="mdc-data-table__cell mdc-data-table__cell--numeric"
                      >
                        ${null!==u?(0,d.u)(u,this.hass.locale,{style:"currency",currency:this.hass.config.currency}):""}
                      </td>`:""}
                </tr>`}))}
              ${w.gas?i.dy`<tr class="mdc-data-table__row total">
                    <td class="mdc-data-table__cell"></td>
                    <th class="mdc-data-table__cell" scope="row">Gas total</th>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${(0,d.u)(v,this.hass.locale)} m³
                    </td>
                    ${A?i.dy`<td
                          class="mdc-data-table__cell mdc-data-table__cell--numeric"
                        >
                          ${(0,d.u)(g,this.hass.locale,{style:"currency",currency:this.hass.config.currency})}
                        </td>`:""}
                  </tr>`:""}
              ${g&&y?i.dy`<tr class="mdc-data-table__row total">
                    <td class="mdc-data-table__cell"></td>
                    <th class="mdc-data-table__cell" scope="row">
                      Total costs
                    </th>
                    <td class="mdc-data-table__cell"></td>
                    <td
                      class="mdc-data-table__cell mdc-data-table__cell--numeric"
                    >
                      ${(0,d.u)(g+y,this.hass.locale,{style:"currency",currency:this.hass.config.currency})}
                    </td>
                  </tr>`:""}
            </tbody>
          </table>
        </div>
      </div>
    </ha-card>`}},{kind:"get",static:!0,key:"styles",value:function(){return i.iv`
      ${(0,i.$m)(a)}
      .mdc-data-table {
        width: 100%;
        border: 0;
      }
      .mdc-data-table__header-cell,
      .mdc-data-table__cell {
        color: var(--primary-text-color);
        border-bottom-color: var(--divider-color);
      }
      .mdc-data-table__row:not(.mdc-data-table__row--selected):hover {
        background-color: rgba(var(--rgb-primary-text-color), 0.04);
      }
      .total {
        --mdc-typography-body2-font-weight: 500;
      }
      .total .mdc-data-table__cell {
        border-top: 1px solid var(--divider-color);
      }
      ha-card {
        height: 100%;
      }
      .card-header {
        padding-bottom: 0;
      }
      .content {
        padding: 16px;
      }
      .has-header {
        padding-top: 0;
      }
      .cell-bullet {
        width: 32px;
        padding-right: 0;
      }
      .bullet {
        border-width: 1px;
        border-style: solid;
        border-radius: 4px;
        height: 16px;
        width: 32px;
      }
    `}}]}}),(0,p.f)(i.oi))}}]);
//# sourceMappingURL=a7b59e0e.js.map