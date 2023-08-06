import{s as t,$ as e,a as r,r as i,_ as s,c as o,f as a,n}from"./index-54a243cf.js";import"./c.6fb756f5.js";import"./c.b540756b.js";import{a as l,c}from"./c.660c326f.js";import{f as d,g as p}from"./c.1966b1d8.js";import{o as h,a as g}from"./c.e2227e58.js";import{X as _}from"./c.4b8b3eaf.js";import"./c.d140f4af.js";import"./c.d2150cf9.js";let m=class extends t{constructor(){super(...arguments),this._state="connecting_webserial"}render(){let t,r=!1;return"connecting_webserial"===this._state?(t=this._renderProgress("Connecting"),r=!0):"prepare_installation"===this._state?(t=this._renderProgress("Preparing installation"),r=!0):"installing"===this._state?(t=void 0===this._writeProgress?this._renderProgress("Erasing"):this._renderProgress(e`
                Installing<br /><br />
                This will take
                ${"ESP8266"===this._platform?"a minute":"2 minutes"}.<br />
                Keep this page visible to prevent slow down
              `,this._writeProgress>3?this._writeProgress:void 0),r=!0):"done"===this._state&&(t=this._error?t=e`
          ${this._renderMessage("👀",this._error,!1)}
          <mwc-button
            slot="secondaryAction"
            dialogAction="ok"
            label="Close"
          ></mwc-button>
          <mwc-button
            slot="primaryAction"
            label="Retry"
            @click=${this._handleRetry}
          ></mwc-button>
        `:this._renderMessage("🎉","Configuration installed!",!0)),e`
      <mwc-dialog
        open
        heading=${undefined}
        scrimClickAction
        @closed=${this._handleClose}
        .hideActions=${r}
      >
        ${t}
      </mwc-dialog>
    `}_renderProgress(t,r){return e`
      <div class="center">
        <div>
          <mwc-circular-progress
            active
            ?indeterminate=${void 0===r}
            .progress=${void 0!==r?r/100:void 0}
            density="8"
          ></mwc-circular-progress>
          ${void 0!==r?e`<div class="progress-pct">${r}%</div>`:""}
        </div>
        ${t}
      </div>
    `}_renderMessage(t,r,i){return e`
      <div class="center">
        <div class="icon">${t}</div>
        ${r}
      </div>
      ${i?e`
            <mwc-button
              slot="primaryAction"
              dialogAction="ok"
              label="Close"
            ></mwc-button>
          `:""}
    `}firstUpdated(t){super.firstUpdated(t),this._handleInstall()}_openCompileDialog(){h(this.params.configuration,!1),this._close()}_handleRetry(){g(this.params,(()=>this._close()))}async _handleInstall(){const t=this.esploader;t.port.addEventListener("disconnect",(async()=>{this._state="done",this._error="Device disconnected",this.params.port||await t.port.close()}));try{try{await t.initialize()}catch(e){return console.error(e),this._state="done",this._error="Failed to initialize.",void(t.connected&&(this._error+=" Try resetting your device or holding the BOOT button while selecting your serial port until it starts preparing the installation."))}this._platform=_[t.chipFamily];const e=this.params.filesCallback||(t=>this._getFilesForConfiguration(this.params.configuration,t));let r=[];try{r=await e(this._platform)}catch(t){return this._state="done",void(this._error=String(t))}if(!r)return;this._state="installing";try{await d(t,r,!0===this.params.erase,(t=>{this._writeProgress=t}))}catch(t){return void("done"!==this._state&&(this._error=`Installation failed: ${t}`,this._state="done"))}await t.hardReset(),this._state="done"}finally{if(t.connected&&(console.log("Disconnecting esp"),await t.disconnect()),!this.params.port){console.log("Closing port");try{await t.port.close()}catch(t){}}}}async _getFilesForConfiguration(t,r){let i;try{i=await l(t)}catch(t){return this._state="done",void(this._error="Error fetching configuration information")}if(r!==i.esp_platform.toUpperCase())return this._state="done",void(this._error=`Configuration does not match the platform of the connected device. Expected an ${i.esp_platform.toUpperCase()} device.`);this._state="prepare_installation";try{await c(t)}catch(t){return this._error=e`
        Failed to prepare configuration<br /><br />
        <button class="link" @click=${this._openCompileDialog}>
          See what went wrong.
        </button>
      `,void(this._state="done")}return"done"!==this._state?await p(t):void 0}_close(){this.shadowRoot.querySelector("mwc-dialog").close()}async _handleClose(){this.params.onClose&&this.params.onClose("done"===this._state&&void 0===this._error),this.parentNode.removeChild(this)}};m.styles=[r,i`
      mwc-list-item {
        margin: 0 -20px;
      }
      svg {
        fill: currentColor;
      }
      .center {
        text-align: center;
      }
      mwc-circular-progress {
        margin-bottom: 16px;
      }
      .progress-pct {
        position: absolute;
        top: 50px;
        left: 0;
        right: 0;
      }
      .icon {
        font-size: 50px;
        line-height: 80px;
        color: black;
      }
      .show-ports {
        margin-top: 16px;
      }
      .error {
        padding: 8px 24px;
        background-color: #fff59d;
        margin: 0 -24px;
      }
    `],s([o()],m.prototype,"params",void 0),s([o()],m.prototype,"esploader",void 0),s([a()],m.prototype,"_writeProgress",void 0),s([a()],m.prototype,"_state",void 0),s([a()],m.prototype,"_error",void 0),m=s([n("esphome-install-web-dialog")],m);export{m as ESPHomeInstallWebDialog};
