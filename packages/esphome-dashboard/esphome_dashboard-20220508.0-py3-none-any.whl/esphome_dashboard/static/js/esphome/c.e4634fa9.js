import{a as e,r as t,_ as o,c as a,f as r,j as s,n as i,s as n,$ as l}from"./index-54a243cf.js";import{c,s as m}from"./c.d840e936.js";import"./c.6fb756f5.js";import{p as d,o as u}from"./c.ecdd56e2.js";let p=class extends n{constructor(){super(...arguments),this._cleanNameInput=e=>{this._error=void 0;const t=e.target;t.value=c(t.value)},this._cleanNameBlur=e=>{const t=e.target;t.value=m(t.value)}}render(){return l`
      <mwc-dialog
        open
        heading=${`Rename ${this.configuration}`}
        scrimClickAction
        @closed=${this._handleClose}
      >
        ${this._error?l`<div class="error">${this._error}</div>`:""}

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
          no-attention
          slot="secondaryAction"
          dialogAction="close"
          label="Close"
        ></mwc-button>
        <mwc-button
          slot="primaryAction"
          label="Rename"
          @click=${this._handleRename}
        ></mwc-button>
      </mwc-dialog>
    `}firstUpdated(e){super.firstUpdated(e);this._inputName.value=this.suggestedName}async _handleRename(e){d();const t=this._inputName;if(!t.reportValidity())return void t.focus();const o=t.value;o!==this.suggestedName&&u(this.configuration,o),this.shadowRoot.querySelector("mwc-dialog").close()}_handleClose(){this.parentNode.removeChild(this)}};p.styles=[e,t`
      .error {
        color: var(--alert-error-color);
        margin-bottom: 16px;
      }
    `],o([a()],p.prototype,"configuration",void 0),o([r()],p.prototype,"_error",void 0),o([s("mwc-textfield[name=name]")],p.prototype,"_inputName",void 0),p=o([i("esphome-rename-dialog")],p);
