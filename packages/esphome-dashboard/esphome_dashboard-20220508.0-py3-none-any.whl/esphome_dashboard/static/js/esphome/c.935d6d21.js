import{r as o,_ as e,c as n,j as t,n as i,s,$ as c}from"./index-54a243cf.js";import"./c.6fb756f5.js";import{c as a,C as l,t as r,b as d}from"./c.cde604b8.js";class h{constructor(){this.chunks=""}transform(o,e){this.chunks+=o;const n=this.chunks.split("\r\n");this.chunks=n.pop(),n.forEach((o=>e.enqueue(o+"\r\n")))}flush(o){o.enqueue(this.chunks)}}class u extends HTMLElement{constructor(){super(...arguments),this.allowInput=!0}logs(){var o;return(null===(o=this._console)||void 0===o?void 0:o.logs())||""}connectedCallback(){if(this._console)return;if(this.attachShadow({mode:"open"}).innerHTML=`\n      <style>\n        :host, input {\n          background-color: #1c1c1c;\n          color: #ddd;\n          font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier,\n            monospace;\n          line-height: 1.45;\n          display: flex;\n          flex-direction: column;\n        }\n        form {\n          display: flex;\n          align-items: center;\n          padding: 0 8px 0 16px;\n        }\n        input {\n          flex: 1;\n          padding: 4px;\n          margin: 0 8px;\n          border: 0;\n          outline: none;\n        }\n        ${a}\n      </style>\n      <div class="log"></div>\n      ${this.allowInput?"<form>\n                >\n                <input autofocus>\n              </form>\n            ":""}\n    `,this._console=new l(this.shadowRoot.querySelector("div")),this.allowInput){const o=this.shadowRoot.querySelector("input");this.addEventListener("click",(()=>{var e;""===(null===(e=getSelection())||void 0===e?void 0:e.toString())&&o.focus()})),o.addEventListener("keydown",(o=>{"Enter"===o.key&&(o.preventDefault(),o.stopPropagation(),this._sendCommand())}))}const o=new AbortController,e=this._connect(o.signal);this._cancelConnection=()=>(o.abort(),e)}async _connect(o){this.logger.debug("Starting console read loop");try{await this.port.readable.pipeThrough(new TextDecoderStream,{signal:o}).pipeThrough(new TransformStream(new h)).pipeTo(new WritableStream({write:o=>{this._console.addLine(o.replace("\r",""))}})),o.aborted||(this._console.addLine(""),this._console.addLine(""),this._console.addLine("Terminal disconnected"))}catch(o){this._console.addLine(""),this._console.addLine(""),this._console.addLine(`Terminal disconnected: ${o}`)}finally{await(e=100,new Promise((o=>setTimeout(o,e)))),this.logger.debug("Finished console read loop")}var e}async _sendCommand(){const o=this.shadowRoot.querySelector("input"),e=o.value,n=new TextEncoder,t=this.port.writable.getWriter();await t.write(n.encode(e+"\r\n")),this._console.addLine(`> ${e}\r\n`),o.value="",o.focus();try{t.releaseLock()}catch(o){console.error("Ignoring release lock error",o)}}async disconnect(){this._cancelConnection&&(await this._cancelConnection(),this._cancelConnection=void 0)}async reset(){this.logger.debug("Triggering reset."),await this.port.setSignals({dataTerminalReady:!1,requestToSend:!0}),await this.port.setSignals({dataTerminalReady:!1,requestToSend:!1}),await new Promise((o=>setTimeout(o,1e3)))}}customElements.define("ewt-console",u);let p=class extends s{render(){return c`
      <mwc-dialog
        open
        .heading=${this.configuration?`Logs ${this.configuration}`:"Logs"}
        scrimClickAction
        @closed=${this._handleClose}
      >
        <ewt-console
          .port=${this.port}
          .logger=${console}
          .allowInput=${!1}
        ></ewt-console>
        <mwc-button
          slot="secondaryAction"
          label="Download Logs"
          @click=${this._downloadLogs}
        ></mwc-button>
        ${this.configuration?c`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Edit"
                @click=${this._openEdit}
              ></mwc-button>
            `:""}
        <mwc-button
          slot="secondaryAction"
          label="Reset Device"
          @click=${this._resetDevice}
        ></mwc-button>
        <mwc-button
          slot="primaryAction"
          dialogAction="close"
          label="Close"
        ></mwc-button>
      </mwc-dialog>
    `}async _openEdit(){(await import("./index-54a243cf.js").then((function(o){return o.U}))).openEditDialog(this.configuration)}async _handleClose(){await this._console.disconnect(),this.closePortOnClose&&await this.port.close(),this.parentNode.removeChild(this)}async _resetDevice(){await this._console.reset()}_downloadLogs(){r(this._console.logs(),(this.configuration?`${d(this.configuration)}_logs`:"logs")+".txt")}};p.styles=o`
    mwc-dialog {
      --mdc-dialog-max-width: 90vw;
    }
    ewt-console {
      width: calc(80vw - 48px);
      height: calc(90vh - 128px);
    }
  `,e([n()],p.prototype,"configuration",void 0),e([n()],p.prototype,"port",void 0),e([n()],p.prototype,"closePortOnClose",void 0),e([t("ewt-console")],p.prototype,"_console",void 0),p=e([i("esphome-logs-webserial-dialog")],p);
