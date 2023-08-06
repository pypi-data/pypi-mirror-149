import{a as t,r as e,_ as i,c as o,f as s,j as a,n as r,s as d,$ as n,S as l,P as c}from"./index-54a243cf.js";import"./c.6fb756f5.js";import{c as h,s as u}from"./c.d840e936.js";import{c as p,s as m}from"./c.4b69909b.js";import{o as v}from"./c.ecdd56e2.js";import{o as _}from"./c.d2150cf9.js";let f=class extends d{constructor(){super(...arguments),this._state="ask",this._busy=!1,this._cleanNameInput=t=>{this._error=void 0;const e=t.target;e.value=h(e.value)},this._cleanNameBlur=t=>{const e=t.target;e.value=u(e.value)},this._cleanSSIDBlur=t=>{const e=t.target;e.value=e.value.trim()}}render(){let t,e;return"ask"===this._state?(t="Adopt device",e=n`
        <div>
          Adopting ${this.device.name} will create an ESPHome configuration for
          this device. This allows you to install updates and customize the
          original firmware.
        </div>

        ${this._error?n`<div class="error">${this._error}</div>`:""}
        ${!1!==this._hasWifiSecrets?n`
              <div>
                This device will be configured to connect to the Wi-Fi network
                stored in your secrets.
              </div>
            `:n`
              <div>
                Enter the credentials of the Wi-Fi network that you want your
                device to connect to.
              </div>
              <div>
                This information will be stored in your secrets and used for
                this and future devices. You can edit the information later by
                editing your secrets at the top of the page.
              </div>

              <mwc-textfield
                label="Network name"
                name="ssid"
                required
                @blur=${this._cleanSSIDBlur}
                .disabled=${this._busy}
              ></mwc-textfield>

              <mwc-textfield
                label="Password"
                name="password"
                type="password"
                helper="Leave blank if no password"
                .disabled=${this._busy}
              ></mwc-textfield>
            `}

        <mwc-button
          slot="primaryAction"
          .label=${this._busy?"Adopting…":"Adopt"}
          @click=${this._handleAdopt}
          .disabled=${void 0===this._hasWifiSecrets}
        ></mwc-button>
        ${this._busy?"":n`
              <mwc-button
                no-attention
                slot="secondaryAction"
                label="Cancel"
                dialogAction="cancel"
              ></mwc-button>
            `}
      `):"adopted"===this._state?(t="Configuration created",e=n`
        <div>
          To finish adoption of ${this.device.name}, the new configuration needs
          to be installed on the device.
        </div>

        ${this._error?n`<div class="error">${this._error}</div>`:""}

        <mwc-textfield
          label="New Name"
          name="name"
          required
          dialogInitialFocus
          spellcheck="false"
          pattern="^[a-z0-9-]+$"
          helper="Lowercase letters (a-z), numbers (0-9) or dash (-)"
          @input=${this._cleanNameInput}
          @blur=${this._cleanNameBlur}
        ></mwc-textfield>

        <mwc-button
          slot="primaryAction"
          label="Install"
          @click=${this._handleInstall}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          no-attention
          label="skip"
          @click=${()=>{this._state="skipped"}}
        ></mwc-button>
      `):"skipped"===this._state&&(t="Installation skipped",e=n`
        <div>
          You will be able to rename the device and install the configuration at
          a later point from the three-dot menu on the device card.
        </div>
        <mwc-button
          slot="primaryAction"
          dialogAction="close"
          label="Close"
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          no-attention
          label="back"
          @click=${()=>{this._state="adopted"}}
        ></mwc-button>
      `),n`
      <mwc-dialog .heading=${t} @closed=${this._handleClose} open>
        ${e}
      </mwc-dialog>
    `}firstUpdated(t){super.firstUpdated(t),p().then((t=>{this._hasWifiSecrets=t}))}updated(t){if(super.updated(t),t.has("_state")&&"adopted"===this._state){const t=this.shadowRoot.querySelector("mwc-textfield");t.value=this.device.name,t.updateComplete.then((()=>t.focus()))}}_handleClose(){this.parentNode.removeChild(this)}async _handleAdopt(){if(this._error=void 0,!1===this._hasWifiSecrets){if(!this._inputSSID.reportValidity())return void this._inputSSID.focus();this._busy=!0;try{await m(this._inputSSID.value,this._inputPassword.value)}catch(t){return this._busy=!1,void(this._error="Failed to store Wi-Fi credentials")}}this._busy=!0;try{await l(this.device),c(this,"adopted"),this._state="adopted"}catch(t){this._busy=!1,this._error="Failed to import device"}}async _handleInstall(){const t=this._inputName;if(!t.reportValidity())return void t.focus();const e=t.value;e===this.device.name?_(`${this.device.name}.yaml`,"OTA"):v(`${this.device.name}.yaml`,e),this.shadowRoot.querySelector("mwc-dialog").close()}};f.styles=[t,e`
      :host {
        --mdc-dialog-max-width: 390px;
      }
      .error {
        color: var(--alert-error-color);
        margin-bottom: 16px;
      }
    `],i([o()],f.prototype,"device",void 0),i([s()],f.prototype,"_hasWifiSecrets",void 0),i([s()],f.prototype,"_state",void 0),i([s()],f.prototype,"_busy",void 0),i([s()],f.prototype,"_error",void 0),i([a("mwc-textfield[name=ssid]")],f.prototype,"_inputSSID",void 0),i([a("mwc-textfield[name=password]")],f.prototype,"_inputPassword",void 0),i([a("mwc-textfield[name=name]")],f.prototype,"_inputName",void 0),f=i([r("esphome-adopt-dialog")],f);
