(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6169],{6169:(e,t,r)=>{"use strict";r.r(t);var s=r(50424),i=r(50467),o=r(99476);const n={1:5,2:3,3:2};class a extends o.p{static async getConfigElement(){return await Promise.all([r.e(5009),r.e(8161),r.e(2955),r.e(8985),r.e(1657),r.e(6561),r.e(4268),r.e(2613),r.e(9799),r.e(6294),r.e(3098),r.e(8595),r.e(9841),r.e(6087),r.e(2001),r.e(6002),r.e(5025),r.e(2990),r.e(1480),r.e(7482),r.e(4535),r.e(8331),r.e(6826),r.e(6902),r.e(3902),r.e(259),r.e(5126),r.e(2979),r.e(7504),r.e(2382)]).then(r.bind(r,22382)),document.createElement("hui-grid-card-editor")}async getCardSize(){if(!this._cards||!this._config)return 0;if(this.square){const e=n[this.columns]||1;return(this._cards.length<this.columns?e:this._cards.length/this.columns*e)+(this._config.title?1:0)}const e=[];for(const t of this._cards)e.push((0,i.N)(t));const t=await Promise.all(e);let r=this._config.title?1:0;for(let e=0;e<t.length;e+=this.columns)r+=Math.max(...t.slice(e,e+this.columns));return r}get columns(){var e;return(null===(e=this._config)||void 0===e?void 0:e.columns)||3}get square(){var e;return!1!==(null===(e=this._config)||void 0===e?void 0:e.square)}setConfig(e){super.setConfig(e),this.style.setProperty("--grid-card-column-count",String(this.columns)),this.toggleAttribute("square",this.square)}static get styles(){return[super.sharedStyles,s.iv`
        #root {
          display: grid;
          grid-template-columns: repeat(
            var(--grid-card-column-count, ${3}),
            minmax(0, 1fr)
          );
          grid-gap: var(--grid-card-gap, 8px);
        }
        :host([square]) #root {
          grid-auto-rows: 1fr;
        }
        :host([square]) #root::before {
          content: "";
          width: 0;
          padding-bottom: 100%;
          grid-row: 1 / 1;
          grid-column: 1 / 1;
        }

        :host([square]) #root > *:not([hidden]) {
          grid-row: 1 / 1;
          grid-column: 1 / 1;
        }
        :host([square]) #root > *:not([hidden]) ~ *:not([hidden]) {
          /*
	       * Remove grid-row and grid-column from every element that comes after
	       * the first not-hidden element
	       */
          grid-row: unset;
          grid-column: unset;
        }
      `]}}customElements.define("hui-grid-card",a)}}]);
//# sourceMappingURL=de7bb92a.js.map