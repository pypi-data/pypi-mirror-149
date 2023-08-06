import{_ as e,c as t,n as o,s as i,$ as n,P as a}from"./index-54a243cf.js";import"./c.6fb756f5.js";import{d as l}from"./c.660c326f.js";let c=class extends i{render(){return n`
      <mwc-dialog
        .heading=${`Delete ${this.name}`}
        @closed=${this._handleClose}
        open
      >
        <div>Are you sure you want to delete ${this.name}?</div>
        <mwc-button
          slot="primaryAction"
          label="Delete"
          dialogAction="close"
          @click=${this._handleDelete}
        ></mwc-button>
        <mwc-button
          slot="secondaryAction"
          no-attention
          label="Cancel"
          dialogAction="cancel"
        ></mwc-button>
      </mwc-dialog>
    `}_handleClose(){this.parentNode.removeChild(this)}async _handleDelete(){await l(this.configuration),a(this,"deleted")}};e([t()],c.prototype,"name",void 0),e([t()],c.prototype,"configuration",void 0),c=e([o("esphome-delete-device-dialog")],c);
