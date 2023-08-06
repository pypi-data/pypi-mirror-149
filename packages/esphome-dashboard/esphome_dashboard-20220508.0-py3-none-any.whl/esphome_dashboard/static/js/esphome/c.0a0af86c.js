import{r as t,_ as o,c as e,f as s,n as i,s as n,$ as a,Q as r}from"./index-54a243cf.js";import"./c.cde604b8.js";import{o as l}from"./c.d2150cf9.js";import"./c.6fb756f5.js";let c=class extends n{render(){return a`
      <esphome-process-dialog
        .heading=${`Install ${this.configuration}`}
        .type=${"upload"}
        .spawnParams=${{configuration:this.configuration,port:this.target}}
        @closed=${this._handleClose}
        @process-done=${this._handleProcessDone}
      >
        ${"OTA"===this.target?"":a`
              <a
                href="https://esphome.io/guides/faq.html#i-can-t-get-flashing-over-usb-to-work"
                slot="secondaryAction"
                target="_blank"
                >❓</a
              >
            `}
        <mwc-button
          slot="secondaryAction"
          dialogAction="close"
          label="Edit"
          @click=${this._openEdit}
        ></mwc-button>
        ${void 0===this._result||0===this._result?"":a`
              <mwc-button
                slot="secondaryAction"
                dialogAction="close"
                label="Retry"
                @click=${this._handleRetry}
              ></mwc-button>
            `}
      </esphome-process-dialog>
    `}_openEdit(){r(this.configuration)}_handleProcessDone(t){this._result=t.detail}_handleRetry(){l(this.configuration,this.target)}_handleClose(){this.parentNode.removeChild(this)}};c.styles=t`
    a[slot="secondaryAction"] {
      text-decoration: none;
      line-height: 32px;
    }
  `,o([e()],c.prototype,"configuration",void 0),o([e()],c.prototype,"target",void 0),o([s()],c.prototype,"_result",void 0),c=o([i("esphome-install-server-dialog")],c);
