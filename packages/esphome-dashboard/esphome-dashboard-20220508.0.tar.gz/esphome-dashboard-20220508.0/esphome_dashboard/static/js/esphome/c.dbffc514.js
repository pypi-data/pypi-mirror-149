import{a as t,r as o,_ as e,c as s,f as i,n as r,s as n,$ as a}from"./index-54a243cf.js";import"./c.6fb756f5.js";import"./c.cde604b8.js";import{g as c}from"./c.d140f4af.js";import{m as l,s as p,a as m}from"./c.4b8b3eaf.js";const h=(t,o)=>{import("./c.855cf2af.js");const e=document.createElement("esphome-logs-dialog");e.configuration=t,e.target=o,document.body.append(e)},d=(t,o,e)=>{import("./c.935d6d21.js");const s=document.createElement("esphome-logs-webserial-dialog");s.configuration=e,s.port=t,s.closePortOnClose=o,document.body.append(s)};let w=class extends n{constructor(){super(...arguments),this._show="options"}render(){let t,o;return"options"===this._show?(t="How to get the logs for your device?",o=a`
        <mwc-list-item
          twoline
          hasMeta
          dialogAction="close"
          .port=${"OTA"}
          @click=${this._pickPort}
        >
          <span>Wirelessly</span>
          <span slot="secondary">Requires the device to be online</span>
          ${l}
        </mwc-list-item>

        <mwc-list-item
          twoline
          hasMeta
          .port=${"WEBSERIAL"}
          @click=${this._pickWebSerial}
        >
          <span>Plug into this computer</span>
          <span slot="secondary">
            For devices connected via USB to this computer
          </span>
          ${l}
        </mwc-list-item>

        <mwc-list-item twoline hasMeta @click=${this._showServerPorts}>
          <span>Plug into computer running ESPHome Dashboard</span>
          <span slot="secondary">
            For devices connected via USB to the server
          </span>
          ${l}
        </mwc-list-item>
        <mwc-button
          no-attention
          slot="primaryAction"
          dialogAction="close"
          label="Cancel"
        ></mwc-button>
      `):"web_instructions"===this._show?(t="View logs in the browser",o=a`
        <div>
          ESPHome can view the logs of your device via the browser if certain
          requirements are met:
        </div>
        <ul>
          <li>ESPHome is visited over HTTPS</li>
          <li>Your browser supports WebSerial</li>
        </ul>
        <div>
          Not all requirements are currently met. The easiest solution is to
          view the logs with ESPHome Web. ESPHome Web works 100% in your browser
          and no data will be shared with the ESPHome project.
        </div>

        <a
          slot="primaryAction"
          href=${"https://web.esphome.io/?dashboard_logs"}
          target="_blank"
          rel="noopener"
        >
          <mwc-button
            dialogAction="close"
            label="OPEN ESPHOME WEB"
          ></mwc-button>
        </a>
        <mwc-button
          no-attention
          slot="secondaryAction"
          label="Back"
          @click=${()=>{this._show="options"}}
        ></mwc-button>
      `):(t="Pick server port",o=a`${void 0===this._ports?a`
              <mwc-list-item>
                <span>Loading ports…</span>
              </mwc-list-item>
            `:0===this._ports.length?a`
              <mwc-list-item>
                <span>No serial ports found.</span>
              </mwc-list-item>
            `:this._ports.map((t=>a`
                <mwc-list-item
                  twoline
                  hasMeta
                  dialogAction="close"
                  .port=${t.port}
                  @click=${this._pickPort}
                >
                  <span>${t.desc}</span>
                  <span slot="secondary">${t.port}</span>
                  ${l}
                </mwc-list-item>
              `))}

        <mwc-button
          no-attention
          slot="primaryAction"
          label="Back"
          @click=${()=>{this._show="options"}}
        ></mwc-button>`),a`
      <mwc-dialog
        open
        heading=${t}
        scrimClickAction
        @closed=${this._handleClose}
      >
        ${o}
      </mwc-dialog>
    `}firstUpdated(t){super.firstUpdated(t),c().then((t=>{0!==t.length||p?this._ports=t:(this._handleClose(),h(this.configuration,"OTA"))}))}_showServerPorts(){this._show="server_ports"}_pickPort(t){h(this.configuration,t.currentTarget.port)}async _pickWebSerial(t){if(p&&m)try{const t=await navigator.serial.requestPort();await t.open({baudRate:115200}),this.shadowRoot.querySelector("mwc-dialog").close(),d(t,!0,this.configuration)}catch(t){console.error(t)}else this._show="web_instructions"}_handleClose(){this.parentNode.removeChild(this)}};w.styles=[t,o`
      mwc-list-item {
        margin: 0 -20px;
      }
    `],e([s()],w.prototype,"configuration",void 0),e([i()],w.prototype,"_ports",void 0),e([i()],w.prototype,"_show",void 0),w=e([r("esphome-logs-target-dialog")],w);var u=Object.freeze({__proto__:null});export{u as l,h as o};
