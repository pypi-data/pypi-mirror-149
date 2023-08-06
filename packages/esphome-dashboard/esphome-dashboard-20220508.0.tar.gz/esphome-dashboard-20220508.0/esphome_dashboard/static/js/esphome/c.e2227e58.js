import{e as t,d as e,t as o,b as i,a as s,r as a,_ as r,c as n,f as l,n as c,s as d,$ as p}from"./index-54a243cf.js";import{g as h}from"./c.d140f4af.js";import"./c.6fb756f5.js";import{E as m,c as u,o as w}from"./c.b540756b.js";import{m as _,s as g,a as v}from"./c.4b8b3eaf.js";import{o as b}from"./c.d2150cf9.js";import{c as f,g as $}from"./c.660c326f.js";class y{constructor(t){this.U=t}disconnect(){this.U=void 0}reconnect(t){this.U=t}deref(){return this.U}}class k{constructor(){this.Y=void 0,this.q=void 0}get(){return this.Y}pause(){var t;null!==(t=this.Y)&&void 0!==t||(this.Y=new Promise((t=>this.q=t)))}resume(){var t;null===(t=this.q)||void 0===t||t.call(this),this.Y=this.q=void 0}}const C=t=>!o(t)&&"function"==typeof t.then;const S=t(class extends e{constructor(){super(...arguments),this._$Cwt=1073741823,this._$Cyt=[],this._$CG=new y(this),this._$CK=new k}render(...t){var e;return null!==(e=t.find((t=>!C(t))))&&void 0!==e?e:i}update(t,e){const o=this._$Cyt;let s=o.length;this._$Cyt=e;const a=this._$CG,r=this._$CK;this.isConnected||this.disconnected();for(let t=0;t<e.length&&!(t>this._$Cwt);t++){const i=e[t];if(!C(i))return this._$Cwt=t,i;t<s&&i===o[t]||(this._$Cwt=1073741823,s=0,Promise.resolve(i).then((async t=>{for(;r.get();)await r.get();const e=a.deref();if(void 0!==e){const o=e._$Cyt.indexOf(i);o>-1&&o<e._$Cwt&&(e._$Cwt=o,e.setValue(t))}})))}return i}disconnected(){this._$CG.disconnect(),this._$CK.pause()}reconnected(){this._$CG.reconnect(this),this._$CK.resume()}}),P=(t,e)=>{import("./c.4342ef59.js");const o=document.createElement("esphome-compile-dialog");o.configuration=t,o.downloadFactoryFirmware=e,document.body.append(o)},x=async(t,e)=>{let o;if(import("./c.4c3ccd57.js"),t.port)o=new m(t.port,console);else try{o=await u(console)}catch(o){return void("NotFoundError"===o.name?w((()=>x(t,e))):alert(`Unable to connect: ${o.message}`))}e&&e();const i=document.createElement("esphome-install-web-dialog");i.params=t,i.esploader=o,document.body.append(i)};let A=class extends d{constructor(){super(...arguments),this._state="pick_option"}render(){let t,e;return"pick_option"===this._state?(t="How do you want to install this on your device?",e=p`
        <mwc-list-item
          twoline
          hasMeta
          .port=${"OTA"}
          @click=${this._handleLegacyOption}
        >
          <span>Wirelessly</span>
          <span slot="secondary">Requires the device to be online</span>
          ${_}
        </mwc-list-item>

        ${this._error?p`<div class="error">${this._error}</div>`:""}

        <mwc-list-item twoline hasMeta @click=${this._handleBrowserInstall}>
          <span>Plug into this computer</span>
          <span slot="secondary">
            For devices connected via USB to this computer
          </span>
          ${_}
        </mwc-list-item>

        <mwc-list-item twoline hasMeta @click=${this._showServerPorts}>
          <span>Plug into the computer running ESPHome Dashboard</span>
          <span slot="secondary">
            For devices connected via USB to the server
          </span>
          ${_}
        </mwc-list-item>

        <mwc-list-item
          twoline
          hasMeta
          @click=${()=>{this._state="pick_download_type"}}
        >
          <span>Manual download</span>
          <span slot="secondary">
            Install it yourself using ESPHome Web or other tools
          </span>
          ${_}
        </mwc-list-item>

        <mwc-button
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      `):"pick_server_port"===this._state?(t="Pick Server Port",e=void 0===this._ports?this._renderProgress("Loading serial devices"):0===this._ports.length?this._renderMessage("👀","No serial devices found.",!0):p`
              ${this._ports.map((t=>p`
                  <mwc-list-item
                    twoline
                    hasMeta
                    .port=${t.port}
                    @click=${this._handleLegacyOption}
                  >
                    <span>${t.desc}</span>
                    <span slot="secondary">${t.port}</span>
                    ${_}
                  </mwc-list-item>
                `))}

              <mwc-button
                no-attention
                slot="primaryAction"
                label="Back"
                @click=${()=>{this._state="pick_option"}}
              ></mwc-button>
            `):"pick_download_type"===this._state?(t="What version do you want to download?",e=p`
        <mwc-list-item
          twoline
          hasMeta
          dialogAction="close"
          @click=${this._handleWebDownload}
        >
          <span>Modern format</span>
          <span slot="secondary">
            For use with ESPHome Web and other tools.
          </span>
          ${_}
        </mwc-list-item>

        <mwc-list-item
          twoline
          hasMeta
          dialogAction="close"
          @click=${this._handleManualDownload}
        >
          <span>Legacy format</span>
          <span slot="secondary">For use with ESPHome Flasher.</span>
          ${_}
        </mwc-list-item>

        <a
          href="https://web.esphome.io"
          target="_blank"
          rel="noopener noreferrer"
          class="bottom-left"
          >Open ESPHome Web</a
        >
        <mwc-button
          no-attention
          slot="primaryAction"
          label="Back"
          @click=${()=>{this._state="pick_option"}}
        ></mwc-button>
      `):"web_instructions"===this._state&&(t="Install ESPHome via the browser",e=p`
        <div>
          ESPHome can install ${this.configuration} on your device via the
          browser if certain requirements are met:
        </div>
        <ul>
          <li>ESPHome is visited over HTTPS</li>
          <li>Your browser supports WebSerial</li>
        </ul>
        <div>
          Not all requirements are currently met. The easiest solution is to
          download your project and do the installation with ESPHome Web.
          ESPHome Web works 100% in your browser and no data will be shared with
          the ESPHome project.
        </div>
        <ol>
          <li>
            ${S(this._compileConfiguration,p`<a download disabled href="#">Download project</a>
                preparing&nbsp;download…
                <mwc-circular-progress
                  density="-8"
                  indeterminate
                ></mwc-circular-progress>`)}
          </li>
          <li>
            <a href=${"https://web.esphome.io/?dashboard_install"} target="_blank" rel="noopener"
              >Open ESPHome Web</a
            >
          </li>
        </ol>

        <mwc-button
          no-attention
          slot="secondaryAction"
          label="Back"
          @click=${()=>{this._state="pick_option"}}
        ></mwc-button>
        <mwc-button
          no-attention
          slot="primaryAction"
          dialogAction="close"
          label="Close"
        ></mwc-button>
      `),p`
      <mwc-dialog
        open
        heading=${t}
        scrimClickAction
        @closed=${this._handleClose}
        .hideActions=${!1}
      >
        ${e}
      </mwc-dialog>
    `}_renderProgress(t,e){return p`
      <div class="center">
        <div>
          <mwc-circular-progress
            active
            ?indeterminate=${void 0===e}
            .progress=${void 0!==e?e/100:void 0}
            density="8"
          ></mwc-circular-progress>
          ${void 0!==e?p`<div class="progress-pct">${e}%</div>`:""}
        </div>
        ${t}
      </div>
    `}_renderMessage(t,e,o){return p`
      <div class="center">
        <div class="icon">${t}</div>
        ${e}
      </div>
      ${o&&p`
        <mwc-button
          slot="primaryAction"
          dialogAction="ok"
          label="Close"
        ></mwc-button>
      `}
    `}firstUpdated(t){super.firstUpdated(t),this._updateSerialPorts()}async _updateSerialPorts(){this._ports=await h()}willUpdate(t){super.willUpdate(t),t.has("_state")&&"web_instructions"===this._state&&!this._compileConfiguration&&(this._abortCompilation=new AbortController,this._compileConfiguration=f(this.configuration).then((()=>p`
            <a download href="${$(this.configuration,!0)}"
              >Download project</a
            >
          `),(()=>p`
            <a download disabled href="#">Download project</a>
            <span class="prepare-error">preparation failed:</span>
            <button
              class="link"
              dialogAction="close"
              @click=${this._handleWebDownload}
            >
              see what went wrong
            </button>
          `)).finally((()=>{this._abortCompilation=void 0})))}updated(t){if(super.updated(t),t.has("_state"))if("pick_server_port"===this._state){const t=async()=>{await this._updateSerialPorts(),this._updateSerialInterval=window.setTimeout((async()=>{await t()}),5e3)};t()}else"pick_server_port"===t.get("_state")&&(clearTimeout(this._updateSerialInterval),this._updateSerialInterval=void 0)}_storeDialogWidth(){this.style.setProperty("--mdc-dialog-min-width",`${this.shadowRoot.querySelector("mwc-list-item").clientWidth+4}px`)}_showServerPorts(){this._storeDialogWidth(),this._state="pick_server_port"}_handleManualDownload(){P(this.configuration,!1)}_handleWebDownload(){P(this.configuration,!0)}_handleLegacyOption(t){b(this.configuration,t.currentTarget.port),this._close()}_handleBrowserInstall(){if(!g||!v)return this._storeDialogWidth(),void(this._state="web_instructions");x({configuration:this.configuration},(()=>this._close()))}_close(){this.shadowRoot.querySelector("mwc-dialog").close()}async _handleClose(){var t;null===(t=this._abortCompilation)||void 0===t||t.abort(),this._updateSerialInterval&&(clearTimeout(this._updateSerialInterval),this._updateSerialInterval=void 0),this.parentNode.removeChild(this)}};A.styles=[s,a`
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
      li mwc-circular-progress {
        margin: 0;
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
      .prepare-error {
        color: var(--alert-error-color);
      }
      li a {
        display: inline-block;
        margin-right: 8px;
      }
      a[disabled] {
        pointer-events: none;
        color: #999;
      }
      ol {
        margin-bottom: 0;
      }
      a.bottom-left {
        z-index: 1;
        position: absolute;
        line-height: 36px;
        bottom: 9px;
      }
    `],r([n()],A.prototype,"configuration",void 0),r([l()],A.prototype,"_ports",void 0),r([l()],A.prototype,"_state",void 0),r([l()],A.prototype,"_error",void 0),A=r([c("esphome-install-choose-dialog")],A);var E=Object.freeze({__proto__:null});export{x as a,E as i,P as o};
