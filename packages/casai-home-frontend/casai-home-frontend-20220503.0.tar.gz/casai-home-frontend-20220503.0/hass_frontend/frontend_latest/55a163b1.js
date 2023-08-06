/*! For license information please see 55a163b1.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[453],{39841:(t,e,r)=>{"use strict";r(94604),r(65660);var n=r(9672),i=r(87156),a=r(50856),o=r(44181);(0,n.k)({_template:a.d`
    <style>
      :host {
        display: block;
        /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
        position: relative;
        z-index: 0;
      }

      #wrapper ::slotted([slot=header]) {
        @apply --layout-fixed-top;
        z-index: 1;
      }

      #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) {
        height: 100%;
      }

      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {
        position: absolute;
      }

      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) #wrapper #contentContainer {
        @apply --layout-fit;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
      }

      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
        position: relative;
      }

      :host([fullbleed]) {
        @apply --layout-vertical;
        @apply --layout-fit;
      }

      :host([fullbleed]) #wrapper,
      :host([fullbleed]) #wrapper #contentContainer {
        @apply --layout-vertical;
        @apply --layout-flex;
      }

      #contentContainer {
        /* Create a stacking context here so that all children appear below the header. */
        position: relative;
        z-index: 0;
      }

      @media print {
        :host([has-scrolling-region]) #wrapper #contentContainer {
          overflow-y: visible;
        }
      }

    </style>

    <div id="wrapper" class="initializing">
      <slot id="headerSlot" name="header"></slot>

      <div id="contentContainer">
        <slot></slot>
      </div>
    </div>
`,is:"app-header-layout",behaviors:[o.Y],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return(0,i.vz)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var t=this.header;if(this.isAttached&&t){this.$.wrapper.classList.remove("initializing"),t.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var e=t.offsetHeight;this.hasScrollingRegion?(t.style.left="",t.style.right=""):requestAnimationFrame(function(){var e=this.getBoundingClientRect(),r=document.documentElement.clientWidth-e.right;t.style.left=e.left+"px",t.style.right=r+"px"}.bind(this));var r=this.$.contentContainer.style;t.fixed&&!t.condenses&&this.hasScrollingRegion?(r.marginTop=e+"px",r.paddingTop=""):(r.paddingTop=e+"px",r.marginTop="")}}})},23682:(t,e,r)=>{"use strict";function n(t,e){if(e.length<t)throw new TypeError(t+" argument"+(t>1?"s":"")+" required, but only "+e.length+" present")}r.d(e,{Z:()=>n})},90394:(t,e,r)=>{"use strict";function n(t){if(null===t||!0===t||!1===t)return NaN;var e=Number(t);return isNaN(e)?e:e<0?Math.ceil(e):Math.floor(e)}r.d(e,{Z:()=>n})},79021:(t,e,r)=>{"use strict";r.d(e,{Z:()=>o});var n=r(90394),i=r(34327),a=r(23682);function o(t,e){(0,a.Z)(2,arguments);var r=(0,i.Z)(t),o=(0,n.Z)(e);return isNaN(o)?new Date(NaN):o?(r.setDate(r.getDate()+o),r):r}},32182:(t,e,r)=>{"use strict";r.d(e,{Z:()=>o});var n=r(90394),i=r(34327),a=r(23682);function o(t,e){(0,a.Z)(2,arguments);var r=(0,i.Z)(t),o=(0,n.Z)(e);if(isNaN(o))return new Date(NaN);if(!o)return r;var s=r.getDate(),l=new Date(r.getTime());l.setMonth(r.getMonth()+o+1,0);var u=l.getDate();return s>=u?l:(r.setFullYear(l.getFullYear(),l.getMonth(),s),r)}},70390:(t,e,r)=>{"use strict";r.d(e,{Z:()=>i});var n=r(93752);function i(){return(0,n.Z)(Date.now())}},61334:(t,e,r)=>{"use strict";function n(){var t=new Date,e=t.getFullYear(),r=t.getMonth(),n=t.getDate(),i=new Date(0);return i.setFullYear(e,r,n-1),i.setHours(23,59,59,999),i}r.d(e,{Z:()=>n})},82045:(t,e,r)=>{"use strict";r.d(e,{Z:()=>a});var n=r(34327),i=r(23682);function a(t,e){(0,i.Z)(2,arguments);var r=(0,n.Z)(t).getTime(),a=(0,n.Z)(e.start).getTime(),o=(0,n.Z)(e.end).getTime();if(!(a<=o))throw new RangeError("Invalid interval");return r>=a&&r<=o}},59429:(t,e,r)=>{"use strict";r.d(e,{Z:()=>a});var n=r(34327),i=r(23682);function a(t){(0,i.Z)(1,arguments);var e=(0,n.Z)(t);return e.setHours(0,0,0,0),e}},13250:(t,e,r)=>{"use strict";r.d(e,{Z:()=>a});var n=r(34327),i=r(23682);function a(t){(0,i.Z)(1,arguments);var e=(0,n.Z)(t);return e.setDate(1),e.setHours(0,0,0,0),e}},27088:(t,e,r)=>{"use strict";r.d(e,{Z:()=>i});var n=r(59429);function i(){return(0,n.Z)(Date.now())}},83008:(t,e,r)=>{"use strict";function n(){var t=new Date,e=t.getFullYear(),r=t.getMonth(),n=t.getDate(),i=new Date(0);return i.setFullYear(e,r,n-1),i.setHours(0,0,0,0),i}r.d(e,{Z:()=>n})},34327:(t,e,r)=>{"use strict";r.d(e,{Z:()=>i});var n=r(23682);function i(t){(0,n.Z)(1,arguments);var e=Object.prototype.toString.call(t);return t instanceof Date||"object"==typeof t&&"[object Date]"===e?new Date(t.getTime()):"number"==typeof t||"[object Number]"===e?new Date(t):("string"!=typeof t&&"[object String]"!==e||"undefined"==typeof console||(console.warn("Starting with v2.0.0-beta.1 date-fns doesn't accept strings as date arguments. Please use `parseISO` to parse strings. See: https://git.io/fjule"),console.warn((new Error).stack)),new Date(NaN))}}}]);
//# sourceMappingURL=55a163b1.js.map