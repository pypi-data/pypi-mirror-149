import{h as e,i as o,M as t,_ as i,j as r,f as a,c as n,o as d,z as s,q as c,A as l,R as p,$ as u,k as m,p as h,v as _,r as b,n as v,C as f,B as g,s as y,D as w,E as k,F as S,a as E}from"./index-54a243cf.js";import"./c.6fb756f5.js";import{F as P,c as x,s as C}from"./c.d840e936.js";import{c as T,o as I}from"./c.b540756b.js";import{s as $,a as O,C as B,d as R,b as D,e as A}from"./c.4b8b3eaf.js";import{a as L,b as M,c as H,d as W}from"./c.660c326f.js";import{g as F,f as N}from"./c.1966b1d8.js";import{S as z,a as U,c as G,s as V}from"./c.4b69909b.js";const j=Symbol("selection controller");class K{constructor(){this.selected=null,this.ordered=null,this.set=new Set}}class q{constructor(e){this.sets={},this.focusedSet=null,this.mouseIsDown=!1,this.updating=!1,e.addEventListener("keydown",(e=>{this.keyDownHandler(e)})),e.addEventListener("mousedown",(()=>{this.mousedownHandler()})),e.addEventListener("mouseup",(()=>{this.mouseupHandler()}))}static getController(e){const o=!("global"in e)||"global"in e&&e.global?document:e.getRootNode();let t=o[j];return void 0===t&&(t=new q(o),o[j]=t),t}keyDownHandler(e){const o=e.target;"checked"in o&&this.has(o)&&("ArrowRight"==e.key||"ArrowDown"==e.key?this.selectNext(o):"ArrowLeft"!=e.key&&"ArrowUp"!=e.key||this.selectPrevious(o))}mousedownHandler(){this.mouseIsDown=!0}mouseupHandler(){this.mouseIsDown=!1}has(e){return this.getSet(e.name).set.has(e)}selectPrevious(e){const o=this.getOrdered(e),t=o.indexOf(e),i=o[t-1]||o[o.length-1];return this.select(i),i}selectNext(e){const o=this.getOrdered(e),t=o.indexOf(e),i=o[t+1]||o[0];return this.select(i),i}select(e){e.click()}focus(e){if(this.mouseIsDown)return;const o=this.getSet(e.name),t=this.focusedSet;this.focusedSet=o,t!=o&&o.selected&&o.selected!=e&&o.selected.focus()}isAnySelected(e){const o=this.getSet(e.name);for(const e of o.set)if(e.checked)return!0;return!1}getOrdered(e){const o=this.getSet(e.name);return o.ordered||(o.ordered=Array.from(o.set),o.ordered.sort(((e,o)=>e.compareDocumentPosition(o)==Node.DOCUMENT_POSITION_PRECEDING?1:0))),o.ordered}getSet(e){return this.sets[e]||(this.sets[e]=new K),this.sets[e]}register(e){const o=e.name||e.getAttribute("name")||"",t=this.getSet(o);t.set.add(e),t.ordered=null}unregister(e){const o=this.getSet(e.name);o.set.delete(e),o.ordered=null,o.selected==e&&(o.selected=null)}update(e){if(this.updating)return;this.updating=!0;const o=this.getSet(e.name);if(e.checked){for(const t of o.set)t!=e&&(t.checked=!1);o.selected=e}if(this.isAnySelected(e))for(const e of o.set){if(void 0===e.formElementTabIndex)break;e.formElementTabIndex=e.checked?0:-1}this.updating=!1}}var X={NATIVE_CONTROL_SELECTOR:".mdc-radio__native-control"},Y={DISABLED:"mdc-radio--disabled",ROOT:"mdc-radio"},Z=function(t){function i(e){return t.call(this,o(o({},i.defaultAdapter),e))||this}return e(i,t),Object.defineProperty(i,"cssClasses",{get:function(){return Y},enumerable:!1,configurable:!0}),Object.defineProperty(i,"strings",{get:function(){return X},enumerable:!1,configurable:!0}),Object.defineProperty(i,"defaultAdapter",{get:function(){return{addClass:function(){},removeClass:function(){},setNativeControlDisabled:function(){}}},enumerable:!1,configurable:!0}),i.prototype.setDisabled=function(e){var o=i.cssClasses.DISABLED;this.adapter.setNativeControlDisabled(e),e?this.adapter.addClass(o):this.adapter.removeClass(o)},i}(t);class Q extends P{constructor(){super(...arguments),this._checked=!1,this.useStateLayerCustomProperties=!1,this.global=!1,this.disabled=!1,this.value="on",this.name="",this.reducedTouchTarget=!1,this.mdcFoundationClass=Z,this.formElementTabIndex=0,this.focused=!1,this.shouldRenderRipple=!1,this.rippleElement=null,this.rippleHandlers=new p((()=>(this.shouldRenderRipple=!0,this.ripple.then((e=>{this.rippleElement=e})),this.ripple)))}get checked(){return this._checked}set checked(e){var o,t;const i=this._checked;e!==i&&(this._checked=e,this.formElement&&(this.formElement.checked=e),null===(o=this._selectionController)||void 0===o||o.update(this),!1===e&&(null===(t=this.formElement)||void 0===t||t.blur()),this.requestUpdate("checked",i),this.dispatchEvent(new Event("checked",{bubbles:!0,composed:!0})))}_handleUpdatedValue(e){this.formElement.value=e}renderRipple(){return this.shouldRenderRipple?u`<mwc-ripple unbounded accent
        .internalUseStateLayerCustomProperties="${this.useStateLayerCustomProperties}"
        .disabled="${this.disabled}"></mwc-ripple>`:""}get isRippleActive(){var e;return(null===(e=this.rippleElement)||void 0===e?void 0:e.isActive)||!1}connectedCallback(){super.connectedCallback(),this._selectionController=q.getController(this),this._selectionController.register(this),this._selectionController.update(this)}disconnectedCallback(){this._selectionController.unregister(this),this._selectionController=void 0}focus(){this.formElement.focus()}createAdapter(){return Object.assign(Object.assign({},m(this.mdcRoot)),{setNativeControlDisabled:e=>{this.formElement.disabled=e}})}handleFocus(){this.focused=!0,this.handleRippleFocus()}handleClick(){this.formElement.focus()}handleBlur(){this.focused=!1,this.formElement.blur(),this.rippleHandlers.endFocus()}setFormData(e){this.name&&this.checked&&e.append(this.name,this.value)}render(){const e={"mdc-radio--touch":!this.reducedTouchTarget,"mdc-ripple-upgraded--background-focused":this.focused,"mdc-radio--disabled":this.disabled};return u`
      <div class="mdc-radio ${h(e)}">
        <input
          tabindex="${this.formElementTabIndex}"
          class="mdc-radio__native-control"
          type="radio"
          name="${this.name}"
          aria-label="${_(this.ariaLabel)}"
          aria-labelledby="${_(this.ariaLabelledBy)}"
          .checked="${this.checked}"
          .value="${this.value}"
          ?disabled="${this.disabled}"
          @change="${this.changeHandler}"
          @focus="${this.handleFocus}"
          @click="${this.handleClick}"
          @blur="${this.handleBlur}"
          @mousedown="${this.handleRippleMouseDown}"
          @mouseenter="${this.handleRippleMouseEnter}"
          @mouseleave="${this.handleRippleMouseLeave}"
          @touchstart="${this.handleRippleTouchStart}"
          @touchend="${this.handleRippleDeactivate}"
          @touchcancel="${this.handleRippleDeactivate}">
        <div class="mdc-radio__background">
          <div class="mdc-radio__outer-circle"></div>
          <div class="mdc-radio__inner-circle"></div>
        </div>
        ${this.renderRipple()}
      </div>`}handleRippleMouseDown(e){const o=()=>{window.removeEventListener("mouseup",o),this.handleRippleDeactivate()};window.addEventListener("mouseup",o),this.rippleHandlers.startPress(e)}handleRippleTouchStart(e){this.rippleHandlers.startPress(e)}handleRippleDeactivate(){this.rippleHandlers.endPress()}handleRippleMouseEnter(){this.rippleHandlers.startHover()}handleRippleMouseLeave(){this.rippleHandlers.endHover()}handleRippleFocus(){this.rippleHandlers.startFocus()}changeHandler(){this.checked=this.formElement.checked}}i([r(".mdc-radio")],Q.prototype,"mdcRoot",void 0),i([r("input")],Q.prototype,"formElement",void 0),i([a()],Q.prototype,"useStateLayerCustomProperties",void 0),i([n({type:Boolean})],Q.prototype,"global",void 0),i([n({type:Boolean,reflect:!0})],Q.prototype,"checked",null),i([n({type:Boolean}),d((function(e){this.mdcFoundation.setDisabled(e)}))],Q.prototype,"disabled",void 0),i([n({type:String}),d((function(e){this._handleUpdatedValue(e)}))],Q.prototype,"value",void 0),i([n({type:String})],Q.prototype,"name",void 0),i([n({type:Boolean})],Q.prototype,"reducedTouchTarget",void 0),i([n({type:Number})],Q.prototype,"formElementTabIndex",void 0),i([a()],Q.prototype,"focused",void 0),i([a()],Q.prototype,"shouldRenderRipple",void 0),i([s("mwc-ripple")],Q.prototype,"ripple",void 0),i([c,n({attribute:"aria-label"})],Q.prototype,"ariaLabel",void 0),i([c,n({attribute:"aria-labelledby"})],Q.prototype,"ariaLabelledBy",void 0),i([l({passive:!0})],Q.prototype,"handleRippleTouchStart",null);const J=b`.mdc-touch-target-wrapper{display:inline}.mdc-radio{padding:calc((40px - 20px) / 2)}.mdc-radio .mdc-radio__native-control:enabled:not(:checked)+.mdc-radio__background .mdc-radio__outer-circle{border-color:rgba(0, 0, 0, 0.54)}.mdc-radio .mdc-radio__native-control:enabled:checked+.mdc-radio__background .mdc-radio__outer-circle{border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-radio .mdc-radio__native-control:enabled+.mdc-radio__background .mdc-radio__inner-circle{border-color:#018786;border-color:var(--mdc-theme-secondary, #018786)}.mdc-radio [aria-disabled=true] .mdc-radio__native-control:not(:checked)+.mdc-radio__background .mdc-radio__outer-circle,.mdc-radio .mdc-radio__native-control:disabled:not(:checked)+.mdc-radio__background .mdc-radio__outer-circle{border-color:rgba(0, 0, 0, 0.38)}.mdc-radio [aria-disabled=true] .mdc-radio__native-control:checked+.mdc-radio__background .mdc-radio__outer-circle,.mdc-radio .mdc-radio__native-control:disabled:checked+.mdc-radio__background .mdc-radio__outer-circle{border-color:rgba(0, 0, 0, 0.38)}.mdc-radio [aria-disabled=true] .mdc-radio__native-control+.mdc-radio__background .mdc-radio__inner-circle,.mdc-radio .mdc-radio__native-control:disabled+.mdc-radio__background .mdc-radio__inner-circle{border-color:rgba(0, 0, 0, 0.38)}.mdc-radio .mdc-radio__background::before{background-color:#018786;background-color:var(--mdc-theme-secondary, #018786)}.mdc-radio .mdc-radio__background::before{top:calc(-1 * (40px - 20px) / 2);left:calc(-1 * (40px - 20px) / 2);width:40px;height:40px}.mdc-radio .mdc-radio__native-control{top:calc((40px - 40px) / 2);right:calc((40px - 40px) / 2);left:calc((40px - 40px) / 2);width:40px;height:40px}@media screen and (forced-colors: active),(-ms-high-contrast: active){.mdc-radio [aria-disabled=true] .mdc-radio__native-control:not(:checked)+.mdc-radio__background .mdc-radio__outer-circle,.mdc-radio .mdc-radio__native-control:disabled:not(:checked)+.mdc-radio__background .mdc-radio__outer-circle{border-color:GrayText}.mdc-radio [aria-disabled=true] .mdc-radio__native-control:checked+.mdc-radio__background .mdc-radio__outer-circle,.mdc-radio .mdc-radio__native-control:disabled:checked+.mdc-radio__background .mdc-radio__outer-circle{border-color:GrayText}.mdc-radio [aria-disabled=true] .mdc-radio__native-control+.mdc-radio__background .mdc-radio__inner-circle,.mdc-radio .mdc-radio__native-control:disabled+.mdc-radio__background .mdc-radio__inner-circle{border-color:GrayText}}.mdc-radio{display:inline-block;position:relative;flex:0 0 auto;box-sizing:content-box;width:20px;height:20px;cursor:pointer;will-change:opacity,transform,border-color,color}.mdc-radio__background{display:inline-block;position:relative;box-sizing:border-box;width:20px;height:20px}.mdc-radio__background::before{position:absolute;transform:scale(0, 0);border-radius:50%;opacity:0;pointer-events:none;content:"";transition:opacity 120ms 0ms cubic-bezier(0.4, 0, 0.6, 1),transform 120ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-radio__outer-circle{position:absolute;top:0;left:0;box-sizing:border-box;width:100%;height:100%;border-width:2px;border-style:solid;border-radius:50%;transition:border-color 120ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-radio__inner-circle{position:absolute;top:0;left:0;box-sizing:border-box;width:100%;height:100%;transform:scale(0, 0);border-width:10px;border-style:solid;border-radius:50%;transition:transform 120ms 0ms cubic-bezier(0.4, 0, 0.6, 1),border-color 120ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-radio__native-control{position:absolute;margin:0;padding:0;opacity:0;cursor:inherit;z-index:1}.mdc-radio--touch{margin-top:4px;margin-bottom:4px;margin-right:4px;margin-left:4px}.mdc-radio--touch .mdc-radio__native-control{top:calc((40px - 48px) / 2);right:calc((40px - 48px) / 2);left:calc((40px - 48px) / 2);width:48px;height:48px}.mdc-radio__native-control:checked+.mdc-radio__background,.mdc-radio__native-control:disabled+.mdc-radio__background{transition:opacity 120ms 0ms cubic-bezier(0, 0, 0.2, 1),transform 120ms 0ms cubic-bezier(0, 0, 0.2, 1)}.mdc-radio__native-control:checked+.mdc-radio__background .mdc-radio__outer-circle,.mdc-radio__native-control:disabled+.mdc-radio__background .mdc-radio__outer-circle{transition:border-color 120ms 0ms cubic-bezier(0, 0, 0.2, 1)}.mdc-radio__native-control:checked+.mdc-radio__background .mdc-radio__inner-circle,.mdc-radio__native-control:disabled+.mdc-radio__background .mdc-radio__inner-circle{transition:transform 120ms 0ms cubic-bezier(0, 0, 0.2, 1),border-color 120ms 0ms cubic-bezier(0, 0, 0.2, 1)}.mdc-radio--disabled{cursor:default;pointer-events:none}.mdc-radio__native-control:checked+.mdc-radio__background .mdc-radio__inner-circle{transform:scale(0.5);transition:transform 120ms 0ms cubic-bezier(0, 0, 0.2, 1),border-color 120ms 0ms cubic-bezier(0, 0, 0.2, 1)}.mdc-radio__native-control:disabled+.mdc-radio__background,[aria-disabled=true] .mdc-radio__native-control+.mdc-radio__background{cursor:default}.mdc-radio__native-control:focus+.mdc-radio__background::before{transform:scale(1);opacity:.12;transition:opacity 120ms 0ms cubic-bezier(0, 0, 0.2, 1),transform 120ms 0ms cubic-bezier(0, 0, 0.2, 1)}:host{display:inline-block;outline:none}.mdc-radio{vertical-align:bottom}.mdc-radio .mdc-radio__native-control:enabled:not(:checked)+.mdc-radio__background .mdc-radio__outer-circle{border-color:var(--mdc-radio-unchecked-color, rgba(0, 0, 0, 0.54))}.mdc-radio [aria-disabled=true] .mdc-radio__native-control:not(:checked)+.mdc-radio__background .mdc-radio__outer-circle,.mdc-radio .mdc-radio__native-control:disabled:not(:checked)+.mdc-radio__background .mdc-radio__outer-circle{border-color:var(--mdc-radio-disabled-color, rgba(0, 0, 0, 0.38))}.mdc-radio [aria-disabled=true] .mdc-radio__native-control:checked+.mdc-radio__background .mdc-radio__outer-circle,.mdc-radio .mdc-radio__native-control:disabled:checked+.mdc-radio__background .mdc-radio__outer-circle{border-color:var(--mdc-radio-disabled-color, rgba(0, 0, 0, 0.38))}.mdc-radio [aria-disabled=true] .mdc-radio__native-control+.mdc-radio__background .mdc-radio__inner-circle,.mdc-radio .mdc-radio__native-control:disabled+.mdc-radio__background .mdc-radio__inner-circle{border-color:var(--mdc-radio-disabled-color, rgba(0, 0, 0, 0.38))}`;let ee=class extends Q{};ee.styles=[J],ee=i([v("mwc-radio")],ee);var oe={ROOT:"mdc-form-field"},te={LABEL_SELECTOR:".mdc-form-field > label"},ie=function(t){function i(e){var r=t.call(this,o(o({},i.defaultAdapter),e))||this;return r.click=function(){r.handleClick()},r}return e(i,t),Object.defineProperty(i,"cssClasses",{get:function(){return oe},enumerable:!1,configurable:!0}),Object.defineProperty(i,"strings",{get:function(){return te},enumerable:!1,configurable:!0}),Object.defineProperty(i,"defaultAdapter",{get:function(){return{activateInputRipple:function(){},deactivateInputRipple:function(){},deregisterInteractionHandler:function(){},registerInteractionHandler:function(){}}},enumerable:!1,configurable:!0}),i.prototype.init=function(){this.adapter.registerInteractionHandler("click",this.click)},i.prototype.destroy=function(){this.adapter.deregisterInteractionHandler("click",this.click)},i.prototype.handleClick=function(){var e=this;this.adapter.activateInputRipple(),requestAnimationFrame((function(){e.adapter.deactivateInputRipple()}))},i}(t);class re extends g{constructor(){super(...arguments),this.alignEnd=!1,this.spaceBetween=!1,this.nowrap=!1,this.label="",this.mdcFoundationClass=ie}createAdapter(){return{registerInteractionHandler:(e,o)=>{this.labelEl.addEventListener(e,o)},deregisterInteractionHandler:(e,o)=>{this.labelEl.removeEventListener(e,o)},activateInputRipple:async()=>{const e=this.input;if(e instanceof P){const o=await e.ripple;o&&o.startPress()}},deactivateInputRipple:async()=>{const e=this.input;if(e instanceof P){const o=await e.ripple;o&&o.endPress()}}}}get input(){var e,o;return null!==(o=null===(e=this.slottedInputs)||void 0===e?void 0:e[0])&&void 0!==o?o:null}render(){const e={"mdc-form-field--align-end":this.alignEnd,"mdc-form-field--space-between":this.spaceBetween,"mdc-form-field--nowrap":this.nowrap};return u`
      <div class="mdc-form-field ${h(e)}">
        <slot></slot>
        <label class="mdc-label"
               @click="${this._labelClick}">${this.label}</label>
      </div>`}click(){this._labelClick()}_labelClick(){const e=this.input;e&&(e.focus(),e.click())}}i([n({type:Boolean})],re.prototype,"alignEnd",void 0),i([n({type:Boolean})],re.prototype,"spaceBetween",void 0),i([n({type:Boolean})],re.prototype,"nowrap",void 0),i([n({type:String}),d((async function(e){var o;null===(o=this.input)||void 0===o||o.setAttribute("aria-label",e)}))],re.prototype,"label",void 0),i([r(".mdc-form-field")],re.prototype,"mdcRoot",void 0),i([f("",!0,"*")],re.prototype,"slottedInputs",void 0),i([r("label")],re.prototype,"labelEl",void 0);const ae=b`.mdc-form-field{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87));display:inline-flex;align-items:center;vertical-align:middle}.mdc-form-field>label{margin-left:0;margin-right:auto;padding-left:4px;padding-right:0;order:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{margin-left:auto;margin-right:0}[dir=rtl] .mdc-form-field>label,.mdc-form-field>label[dir=rtl]{padding-left:0;padding-right:4px}.mdc-form-field--nowrap>label{text-overflow:ellipsis;overflow:hidden;white-space:nowrap}.mdc-form-field--align-end>label{margin-left:auto;margin-right:0;padding-left:0;padding-right:4px;order:-1}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{margin-left:0;margin-right:auto}[dir=rtl] .mdc-form-field--align-end>label,.mdc-form-field--align-end>label[dir=rtl]{padding-left:4px;padding-right:0}.mdc-form-field--space-between{justify-content:space-between}.mdc-form-field--space-between>label{margin:0}[dir=rtl] .mdc-form-field--space-between>label,.mdc-form-field--space-between>label[dir=rtl]{margin:0}:host{display:inline-flex}.mdc-form-field{width:100%}::slotted(*){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}::slotted(mwc-switch){margin-right:10px}[dir=rtl] ::slotted(mwc-switch),::slotted(mwc-switch[dir=rtl]){margin-left:10px}`;let ne=class extends re{};ne.styles=[ae],ne=i([v("mwc-formfield")],ne);const de=u`
  <optgroup label="ESP8266">
    <option value="esp01_1m">Generic ESP8266 (for example Sonoff)</option>
    <option value="nodemcuv2">NodeMCU</option>
    <option value="d1_mini">Wemos D1 and Wemos D1 mini</option>
    <option value="d1_mini_lite">Wemos D1 mini Lite</option>
    <option value="d1_mini_pro">Wemos D1 mini Pro</option>
    <option value="huzzah">Adafruit HUZZAH ESP8266</option>
    <option value="oak">DigiStump Oak</option>
    <option value="thing">Sparkfun ESP8266 Thing</option>
    <option value="thingdev">Sparkfun ESP8266 Thing - Dev Board</option>
  </optgroup>
  <optgroup label="ESP32">
    <option value="esp-wrover-kit">Generic ESP32 (WROVER Module)</option>
    <option value="nodemcu-32s">NodeMCU-32S</option>
    <option value="lolin_d32">Wemos Lolin D32</option>
    <option value="lolin_d32_pro">Wemos Lolin D32 Pro</option>
    <option value="featheresp32">Adafruit ESP32 Feather</option>
    <option value="m5stack-core-esp32">M5Stack Core ESP32</option>
  </optgroup>
  <optgroup label="Other ESP8266s">
    <option value="gen4iod">4D Systems gen4 IoD Range</option>
    <option value="wifi_slot">Amperka WiFi Slot</option>
    <option value="espduino">Doit ESPDuino</option>
    <option value="espectro">DycodeX ESPectro Core</option>
    <option value="espino">ESPino</option>
    <option value="esp_wroom_02">Espressif ESP-WROOM-02 module</option>
    <option value="esp12e">Espressif ESP-12E module</option>
    <option value="esp01">Espressif ESP-01 512k module</option>
    <option value="esp07">Espressif ESP-07 module</option>
    <option value="esp8285">Generic ESP8285 module</option>
    <option value="espresso_lite_v1">ESPert ESPresso Lite 1.0</option>
    <option value="espresso_lite_v2">ESPert ESPresso Lite 2.0</option>
    <option value="phoenix_v1">ESPert Phoenix 1.0</option>
    <option value="wifinfo">WiFInfo</option>
    <option value="espmxdevkit">ESP-Mx DevKit</option>
    <option value="heltec_wifi_kit_8">Heltec WiFi kit 8</option>
    <option value="nodemcu">NodeMCU 0.9</option>
    <option value="modwifi">Olimex MOD-WIFI</option>
    <option value="wio_link">SeedStudio Wio Link</option>
    <option value="wio_node">SeedStudio Wio Node</option>
    <option value="sonoff_basic">Sonoff Basic</option>
    <option value="sonoff_s20">Sonoff S20</option>
    <option value="sonoff_sv">Sonoff SV</option>
    <option value="sonoff_th">Sonoff TH</option>
    <option value="sparkfunBlynk">Sparkfun Blynk Board</option>
    <option value="esp210">SweetPea ESP-210</option>
    <option value="espinotee">ThaiEasyElec ESPino</option>
    <option value="d1">Wemos D1 Revision 1</option>
    <option value="wifiduino">WiFiDuino</option>
    <option value="xinabox_cw01">XinaBox CW01</option>
  </optgroup>
  <optgroup label="Other ESP32s">
    <option value="lolin32">Wemos Lolin 32</option>
    <option value="m5stack-fire">M5Stack FIRE</option>
    <option value="wemosbat">Wemos WiFi &amp; Bluetooth Battery</option>
    <option value="node32s">Node32s</option>
    <option value="alksesp32">ALKS ESP32</option>
    <option value="az-delivery-devkit-v4">
      AZ-Delivery ESP-32 Dev Kit C V4
    </option>
    <option value="bpi-bit">BPI-Bit</option>
    <option value="briki_abc_esp32">Briki ABC</option>
    <option value="briki_mbc-wb_esp32">Briki MBC-WB</option>
    <option value="d-duino-32">D-duino-32</option>
    <option value="esp32-devkitlipo">OLIMEX ESP32-DevKit-LiPo</option>
    <option value="esp32-evb">OLIMEX ESP32-EVB</option>
    <option value="esp32-gateway">OLIMEX ESP32-GATEWAY</option>
    <option value="esp32-poe-iso">OLIMEX ESP32-PoE-ISO</option>
    <option value="esp32-poe">OLIMEX ESP32-PoE</option>
    <option value="esp32-pro">OLIMEX ESP32-PRO</option>
    <option value="esp320">Electronic SweetPeas ESP320</option>
    <option value="esp32cam">AI Thinker ESP32-CAM</option>
    <option value="esp32dev">Espressif ESP32 Dev Module</option>
    <option value="esp32doit-devkit-v1">DOIT ESP32 DEVKIT V1</option>
    <option value="esp32doit-espduino">DOIT ESPduino32</option>
    <option value="esp32thing">SparkFun ESP32 Thing</option>
    <option value="esp32thing_plus">SparkFun ESP32 Thing Plus</option>
    <option value="esp32vn-iot-uno">ESP32vn IoT Uno</option>
    <option value="espea32">April Brother ESPea32</option>
    <option value="espectro32">ESPectro32</option>
    <option value="espino32">ESPino32</option>
    <option value="etboard">ETBoard</option>
    <option value="firebeetle32">FireBeetle-ESP32</option>
    <option value="fm-devkit">ESP32 FM DevKit</option>
    <option value="frogboard">Frog Board ESP32</option>
    <option value="healthypi4">ProtoCentral HealthyPi 4</option>
    <option value="heltec_wifi_kit_32">Heltec WiFi Kit 32</option>
    <option value="heltec_wifi_kit_32_v2">Heltec WiFi Kit 32 V2</option>
    <option value="heltec_wifi_lora_32">Heltec WiFi LoRa 32</option>
    <option value="heltec_wifi_lora_32_V2">Heltec WiFi LoRa 32 (V2)</option>
    <option value="heltec_wireless_stick">Heltec Wireless Stick</option>
    <option value="heltec_wireless_stick_lite">
      Heltec Wireless Stick Lite
    </option>
    <option value="honeylemon">HONEYLemon</option>
    <option value="hornbill32dev">Hornbill ESP32 Dev</option>
    <option value="hornbill32minima">Hornbill ESP32 Minima</option>
    <option value="imbrios-logsens-v1p1">Imbrios LogSens V1P1</option>
    <option value="inex_openkb">INEX OpenKB</option>
    <option value="intorobot">IntoRobot Fig</option>
    <option value="iotaap_magnolia">IoTaaP Magnolia</option>
    <option value="iotbusio">oddWires IoT-Bus Io</option>
    <option value="iotbusproteus">oddWires IoT-Bus Proteus</option>
    <option value="kits-edu">KITS ESP32 EDU</option>
    <option value="labplus_mpython">Labplus mPython</option>
    <option value="lopy">Pycom LoPy</option>
    <option value="lopy4">Pycom LoPy4</option>
    <option value="m5stack-atom">M5Stack-ATOM</option>
    <option value="m5stack-grey">M5Stack GREY ESP32</option>
    <option value="m5stack-core2">M5Stack Core2</option>
    <option value="m5stack-coreink">M5Stack-Core Ink</option>
    <option value="m5stack-timer-cam">M5Stack Timer CAM</option>
    <option value="m5stick-c">M5Stick-C</option>
    <option value="magicbit">MagicBit</option>
    <option value="mgbot-iotik32a">MGBOT IOTIK 32A</option>
    <option value="mgbot-iotik32b">MGBOT IOTIK 32B</option>
    <option value="mhetesp32devkit">MH ET LIVE ESP32DevKIT</option>
    <option value="mhetesp32minikit">MH ET LIVE ESP32MiniKit</option>
    <option value="microduino-core-esp32">Microduino Core ESP32</option>
    <option value="nano32">MakerAsia Nano32</option>
    <option value="nina_w10">u-blox NINA-W10 series</option>
    <option value="nscreen-32">YeaCreate NSCREEN-12</option>
    <option value="odroid_esp32">ODROID-GO</option>
    <option value="onehorse32dev">Onehorse ESP32 Dev Module</option>
    <option value="oroca_edubot">OROCA EduBot</option>
    <option value="pico32">ESP32 Pico Kit</option>
    <option value="piranha_esp32">Fishino Piranha ESP-32</option>
    <option value="pocket_32">Dongsen Tech Pocket 32</option>
    <option value="pycom_gpy">Pycom GPy</option>
    <option value="qchip">Qchip</option>
    <option value="quantum">Noduino Quantum</option>
    <option value="s_odi_ultra">S.ODI Ultra v1</option>
    <option value="sensesiot_weizen">LOGISENSES Senses Weizen</option>
    <option value="sg-o_airMon">SG-O AirMon</option>
    <option value="sparkfun_lora_gateway_1-channel">
      SparkFun LoRa Gateway 1-Channel
    </option>
    <option value="tinypico">TinyPICO</option>
    <option value="ttgo-lora32-v1">TTGO LoRa32-OLED V1</option>
    <option value="ttgo-lora32-v2">TTGO LoRa32-OLED V2</option>
    <option value="ttgo-lora32-v21">TTGO LoRa32-OLED v2.1.6</option>
    <option value="ttgo-t-beam">TTGO T-Beam</option>
    <option value="ttgo-t-watch">TTGO T-Watch</option>
    <option value="ttgo-t1">TTGO T1</option>
    <option value="turta_iot_node">Turta IoT Node</option>
    <option value="vintlabs-devkit-v1">VintLabs ESP32 Devkit</option>
    <option value="wemos_d1_mini32">WeMos D1 MINI ESP32</option>
    <option value="wesp32">Silicognition wESP32</option>
    <option value="widora-air">Widora AIR</option>
    <option value="wifiduino32">Blinker WiFiduino32</option>
    <option value="xinabox_cw02">XinaBox CW02</option>
  </optgroup>
`;let se=class extends y{constructor(){super(...arguments),this._busy=!1,this._board="ESP32",this._hasWifiSecrets=void 0,this._customBoard="",this._data={ssid:`!secret ${z}`,psk:`!secret ${U}`},this._state=$?"basic_config":"ask_esphome_web",this._installed=!1,this._cleanNameInput=e=>{this._error=void 0;const o=e.target;o.value=x(o.value)},this._cleanNameBlur=e=>{const o=e.target;o.value=C(o.value)},this._cleanSSIDBlur=e=>{const o=e.target;o.value=o.value.trim()}}render(){let e,o,t=!1;return"ask_esphome_web"===this._state?[e,o,t]=this._renderAskESPHomeWeb():"basic_config"===this._state?[e,o,t]=this._renderBasicConfig():"pick_board"===this._state?(e="Select your device type",o=this._renderPickBoard()):"connect_webserial"===this._state?(e="Installation",o=this._renderConnectSerial()):"connecting_webserial"===this._state?(o=this._renderProgress("Connecting"),t=!0):"prepare_flash"===this._state?(o=this._renderProgress("Preparing installation"),t=!0):"flashing"===this._state?(o=void 0===this._writeProgress?this._renderProgress("Erasing"):this._renderProgress(u`
                Installing<br /><br />
                This will take
                ${"ESP8266"===this._board?"a minute":"2 minutes"}.<br />
                Keep this page visible to prevent slow down
              `,this._writeProgress>3?this._writeProgress:void 0),t=!0):"wait_come_online"===this._state?(o=this._renderProgress("Finding device on network"),t=!0):"done"===this._state&&(o=this._renderDone()),u`
      <mwc-dialog
        open
        heading=${e}
        scrimClickAction
        @closed=${this._handleClose}
        .hideActions=${t}
        >${o}</mwc-dialog
      >
    `}_renderProgress(e,o){return u`
      <div class="center">
        <div>
          <mwc-circular-progress
            active
            ?indeterminate=${void 0===o}
            .progress=${void 0!==o?o/100:void 0}
            density="8"
          ></mwc-circular-progress>
          ${void 0!==o?u`<div class="progress-pct">${o}%</div>`:""}
        </div>
        ${e}
      </div>
    `}_renderMessage(e,o,t){return u`
      <div class="center">
        <div class="icon">${e}</div>
        ${o}
      </div>
      ${t?u`
            <mwc-button
              slot="primaryAction"
              dialogAction="ok"
              label="Close"
            ></mwc-button>
          `:""}
    `}_renderAskESPHomeWeb(){return["New device",u`
      <div>
        A device needs to be connected to a computer using a USB cable to be
        added to ESPHome. Once added, ESPHome will interact with the device
        wirelessly.
      </div>
      <div>
        ${O?"Your browser does not support WebSerial.":"You are not browsing the dashboard over a secure connection (HTTPS)."}
        This prevents ESPHome from being able to install this on devices
        connected to this computer.
      </div>
      <div>
        You will still be able to install ESPHome by connecting the device to
        the computer that runs the ESPHome dashboard.
      </div>
      <div>
        Alternatively, you can use ESPHome Web to prepare a device for being
        used with ESPHome using this computer.
      </div>

      <mwc-button
        slot="primaryAction"
        label="Continue"
        @click=${()=>{this._state="basic_config"}}
      ></mwc-button>

      <a
        slot="secondaryAction"
        href=${"https://web.esphome.io/?dashboard_wizard"}
        target="_blank"
        rel="noopener"
      >
        <mwc-button
          no-attention
          dialogAction="close"
          label="Open ESPHome Web"
        ></mwc-button>
      </a>
    `,!1]}_renderBasicConfig(){if(void 0===this._hasWifiSecrets)return[void 0,this._renderProgress("Initializing"),!0];return[$?"New device":"Create configuration",u`
      ${this._error?u`<div class="error">${this._error}</div>`:""}

      <mwc-textfield
        label="Name"
        name="name"
        required
        pattern="^[a-z0-9-]+$"
        helper="Lowercase letters (a-z), numbers (0-9) or dash (-)"
        @input=${this._cleanNameInput}
        @blur=${this._cleanNameBlur}
      ></mwc-textfield>

      ${this._hasWifiSecrets?u`
            <div>
              This device will be configured to connect to the Wi-Fi network
              stored in your secrets.
            </div>
          `:u`
            <div>
              Enter the credentials of the Wi-Fi network that you want your
              device to connect to.
            </div>
            <div>
              This information will be stored in your secrets and used for this
              and future devices. You can edit the information later by editing
              your secrets at the top of the page.
            </div>

            <mwc-textfield
              label="Network name"
              name="ssid"
              required
              @blur=${this._cleanSSIDBlur}
            ></mwc-textfield>

            <mwc-textfield
              label="Password"
              name="password"
              type="password"
              helper="Leave blank if no password"
            ></mwc-textfield>
          `}

      <mwc-button
        slot="primaryAction"
        label="Next"
        @click=${this._handleBasicConfigSubmit}
      ></mwc-button>

      <mwc-button
        no-attention
        slot="secondaryAction"
        dialogAction="close"
        label="Cancel"
      ></mwc-button>
    `,!1]}_renderPickBoard(){return u`
      ${this._error?u`<div class="error">${this._error}</div>`:""}

      <div>
        Select the type of device that this configuration will be installed on.
      </div>
      <mwc-formfield label="ESP32" checked>
        <mwc-radio
          name="board"
          value="ESP32"
          @click=${this._handlePickBoardRadio}
          ?checked=${"ESP32"===this._board}
        ></mwc-radio>
      </mwc-formfield>

      <mwc-formfield label="ESP32-S2">
        <mwc-radio
          name="board"
          value="ESP32S2"
          @click=${this._handlePickBoardRadio}
          ?checked=${"ESP32S2"===this._board}
        ></mwc-radio>
      </mwc-formfield>

      <mwc-formfield label="ESP32-C3">
        <mwc-radio
          name="board"
          value="ESP32C3"
          @click=${this._handlePickBoardRadio}
          ?checked=${"ESP32C3"===this._board}
        ></mwc-radio>
      </mwc-formfield>

      <mwc-formfield label="ESP8266">
        <mwc-radio
          name="board"
          value="ESP8266"
          @click=${this._handlePickBoardRadio}
          ?checked=${"ESP8266"===this._board}
        ></mwc-radio>
      </mwc-formfield>

      <mwc-formfield label="Pick specific board">
        <mwc-radio
          name="board"
          value="CUSTOM"
          @click=${this._handlePickBoardRadio}
          ?checked=${"CUSTOM"===this._board}
        ></mwc-radio>
      </mwc-formfield>
      ${"CUSTOM"!==this._board?"":u`
            <div class="formfield-extra">
              <select @change=${this._handlePickBoardCustom}>
                ${de}
              </select>
            </div>
          `}
      <div>
        Pick a custom board if the default targets don't work or if you want to
        use the pin numbers printed on the device in your configuration.
      </div>

      <mwc-button
        slot="primaryAction"
        label="Next"
        @click=${this._handlePickBoardSubmit}
      ></mwc-button>
      <mwc-button
        no-attention
        slot="secondaryAction"
        dialogAction="close"
        label="Cancel"
      ></mwc-button>
    `}_renderConnectSerial(){return u`
      ${this._error?u`<div class="error">${this._error}</div>`:""}

      <div>
        ESPHome will now create your configuration and install it on your
        device.
      </div>

      <div>
        Connect your ESP board with a USB cable to your computer and click on
        connect. You need to do this once. Later updates install wirelessly.
        <a
          href="https://esphome.io/guides/getting_started_hassio.html#webserial"
          target="_blank"
          >Learn more</a
        >
      </div>

      <div>Skip this step to install it on your device later.</div>

      <mwc-button
        slot="primaryAction"
        label="Connect"
        .disabled=${this._busy}
        @click=${this._handleConnectSerialSubmit}
      ></mwc-button>
      <mwc-button
        no-attention
        slot="secondaryAction"
        label="Skip this step"
        .disabled=${this._busy}
        @click=${this._handleConnectSerialSkip}
      ></mwc-button>
    `}_renderDone(){return this._error?this._renderMessage("👀",this._error,!0):u`
      ${this._renderMessage("🎉","Configuration created!",this._installed)}
      ${this._installed?"":u`
            <div>
              You can now install the configuration to your device. The first
              time this requires a cable.
            </div>
            <div>
              Once the device is installed and connected to your network, you
              will be able to manage it wirelessly.
            </div>
            <mwc-button
              slot="primaryAction"
              dialogAction="ok"
              label="Install"
              @click=${()=>w(`${this._data.name}.yaml`)}
            ></mwc-button>
            <mwc-button
              no-attention
              slot="secondaryAction"
              dialogAction="close"
              label="Skip"
            ></mwc-button>
          `}
    `}firstUpdated(e){super.firstUpdated(e),G().then((e=>{this._hasWifiSecrets=e}))}updated(e){if(super.updated(e),e.has("_state")||e.has("_hasWifiSecrets")){const e=this.shadowRoot.querySelector("mwc-textfield, mwc-radio, mwc-button");e&&e.updateComplete.then((()=>e.focus()))}e.has("_board")&&"CUSTOM"===this._board&&(this._customBoard=this.shadowRoot.querySelector("select").value)}async _handleBasicConfigSubmit(){const e=this._inputName,o=e.reportValidity(),t=!!this._hasWifiSecrets||this._inputSSID.reportValidity();if(!o||!t)return void(o?this._inputSSID.focus():e.focus());const i=e.value;try{return await L(`${i}.yaml`),void(this._error="Name already in use")}catch(e){}this._data.name=i,this._hasWifiSecrets||(this._wifi={ssid:this._inputSSID.value,password:this._inputPassword.value}),setTimeout((()=>{this._state=$&&O?"connect_webserial":"pick_board"}),0)}_handlePickBoardRadio(e){this._board=e.target.value}_handlePickBoardCustom(e){this._customBoard=e.target.value}async _handlePickBoardSubmit(){"ESP32"===this._board?(this._data.platform="ESP32",this._data.board="esp32dev"):"ESP8266"===this._board?(this._data.platform="ESP8266",this._data.board="esp01_1m"):"ESP32S2"===this._board?(this._data.platform="ESP32S2",this._data.board="esp32-s2-saola-1"):"ESP32C3"===this._board?(this._data.platform="ESP32C3",this._data.board="esp32-c3-devkitm-1"):this._data.board=this._customBoard,this._busy=!0;try{this._wifi&&await V(this._wifi.ssid,this._wifi.password),await M(this._data),k(),this._state="done"}catch(e){this._error=e.message||e}finally{this._busy=!1}}_handleConnectSerialSkip(){this._error=void 0,this._state="pick_board"}async _handleConnectSerialSubmit(){let e;this._busy=!0,this._error=void 0;let o=!1;try{try{e=await T(console)}catch(e){return console.error(e),void("NotFoundError"===e.name?I():this._error=e.message||String(e))}this._state="connecting_webserial";try{await e.initialize()}catch(o){return console.error(o),this._state="connect_webserial",void(e.connected&&(this._error="Failed to initialize. Try resetting your device or holding the BOOT button while selecting your serial port until it starts preparing the installation."))}if(this._state="prepare_flash",e.chipFamily===B)this._board="ESP32",this._data.board="esp32dev";else if(e.chipFamily===R)this._board="ESP8266",this._data.board="esp01_1m";else if(e.chipFamily===D)this._board="ESP32S2",this._data.board="esp32-s2-saola-1",this._data.platform="ESP32S2";else{if(e.chipFamily!==A)return this._state="connect_webserial",void(this._error=`Unable to identify the connected device (${e.chipFamily}).`);this._board="ESP32C3",this._data.board="esp32-c3-devkitm-1",this._data.platform="ESP32C3"}try{await M(this._data)}catch(e){return console.error(e),this._state="connect_webserial",void(this._error="Unable to create the configuration")}o=!0;try{await H(this._configFilename)}catch(e){return console.error(e),this._state="connect_webserial",void(this._error="Unable to compile the configuration")}this._state="flashing";try{const o=await F(this._configFilename);await N(e,o,!0,(e=>{this._writeProgress=e}))}catch(e){return console.error(e),this._state="connect_webserial",void(this._error="Error installing the configuration")}o=!1,this._installed=!0,await e.hardReset(),this._state="wait_come_online";try{await new Promise(((e,o)=>{const t=S((o=>{o[this._configFilename]&&(t(),clearTimeout(i),e(void 0))})),i=setTimeout((()=>{t(),o("Timeout")}),2e4)}))}catch(e){console.error(e),this._error="Configuration created but unable to detect the device on the network"}this._state="done"}finally{this._busy=!1,e&&(e.connected&&(console.log("Disconnecting esp"),await e.disconnect()),console.log("Closing port"),await e.port.close()),o&&await W(this._configFilename)}}get _configFilename(){return`${this._data.name}.yaml`}async _handleClose(){this.parentNode.removeChild(this)}};se.styles=[E,b`
      :host {
        --mdc-dialog-max-width: 390px;
      }
      mwc-textfield[name="name"] + div {
        margin-top: 18px;
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
      .error {
        color: var(--alert-error-color);
        margin-bottom: 16px;
      }
    `],i([a()],se.prototype,"_busy",void 0),i([a()],se.prototype,"_board",void 0),i([a()],se.prototype,"_hasWifiSecrets",void 0),i([a()],se.prototype,"_writeProgress",void 0),i([a()],se.prototype,"_state",void 0),i([a()],se.prototype,"_error",void 0),i([r("mwc-textfield[name=name]")],se.prototype,"_inputName",void 0),i([r("mwc-textfield[name=ssid]")],se.prototype,"_inputSSID",void 0),i([r("mwc-textfield[name=password]")],se.prototype,"_inputPassword",void 0),se=i([v("esphome-wizard-dialog")],se);export{se as ESPHomeWizardDialog};
