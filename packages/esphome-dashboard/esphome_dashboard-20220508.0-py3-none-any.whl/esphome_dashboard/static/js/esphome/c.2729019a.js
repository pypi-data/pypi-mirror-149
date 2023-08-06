import{_ as e,c as o,n as s,s as i,$ as t}from"./index-54a243cf.js";import"./c.cde604b8.js";import"./c.6fb756f5.js";let a=class extends i{render(){return t`
      <esphome-process-dialog
        .heading=${`Clean MQTT discovery topics for ${this.configuration}`}
        .type=${"clean-mqtt"}
        .spawnParams=${{configuration:this.configuration}}
        @closed=${this._handleClose}
      >
      </esphome-process-dialog>
    `}_handleClose(){this.parentNode.removeChild(this)}};e([o()],a.prototype,"configuration",void 0),a=e([s("esphome-clean-mqtt-dialog")],a);
