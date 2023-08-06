/*! For license information please see 71d59c51.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[55768],{61092:(t,i,e)=>{e.d(i,{K:()=>l});var s=e(87480),a=(e(91156),e(14114)),o=e(98734),r=e(37500),n=e(33310),h=e(8636);class l extends r.oi{constructor(){super(...arguments),this.value="",this.group=null,this.tabindex=-1,this.disabled=!1,this.twoline=!1,this.activated=!1,this.graphic=null,this.multipleGraphics=!1,this.hasMeta=!1,this.noninteractive=!1,this.selected=!1,this.shouldRenderRipple=!1,this._managingList=null,this.boundOnClick=this.onClick.bind(this),this._firstChanged=!0,this._skipPropRequest=!1,this.rippleHandlers=new o.A((()=>(this.shouldRenderRipple=!0,this.ripple))),this.listeners=[{target:this,eventNames:["click"],cb:()=>{this.onClick()}},{target:this,eventNames:["mouseenter"],cb:this.rippleHandlers.startHover},{target:this,eventNames:["mouseleave"],cb:this.rippleHandlers.endHover},{target:this,eventNames:["focus"],cb:this.rippleHandlers.startFocus},{target:this,eventNames:["blur"],cb:this.rippleHandlers.endFocus},{target:this,eventNames:["mousedown","touchstart"],cb:t=>{const i=t.type;this.onDown("mousedown"===i?"mouseup":"touchend",t)}}]}get text(){const t=this.textContent;return t?t.trim():""}render(){const t=this.renderText(),i=this.graphic?this.renderGraphic():r.dy``,e=this.hasMeta?this.renderMeta():r.dy``;return r.dy`
      ${this.renderRipple()}
      ${i}
      ${t}
      ${e}`}renderRipple(){return this.shouldRenderRipple?r.dy`
      <mwc-ripple
        .activated=${this.activated}>
      </mwc-ripple>`:this.activated?r.dy`<div class="fake-activated-ripple"></div>`:""}renderGraphic(){const t={multi:this.multipleGraphics};return r.dy`
      <span class="mdc-deprecated-list-item__graphic material-icons ${(0,h.$)(t)}">
        <slot name="graphic"></slot>
      </span>`}renderMeta(){return r.dy`
      <span class="mdc-deprecated-list-item__meta material-icons">
        <slot name="meta"></slot>
      </span>`}renderText(){const t=this.twoline?this.renderTwoline():this.renderSingleLine();return r.dy`
      <span class="mdc-deprecated-list-item__text">
        ${t}
      </span>`}renderSingleLine(){return r.dy`<slot></slot>`}renderTwoline(){return r.dy`
      <span class="mdc-deprecated-list-item__primary-text">
        <slot></slot>
      </span>
      <span class="mdc-deprecated-list-item__secondary-text">
        <slot name="secondary"></slot>
      </span>
    `}onClick(){this.fireRequestSelected(!this.selected,"interaction")}onDown(t,i){const e=()=>{window.removeEventListener(t,e),this.rippleHandlers.endPress()};window.addEventListener(t,e),this.rippleHandlers.startPress(i)}fireRequestSelected(t,i){if(this.noninteractive)return;const e=new CustomEvent("request-selected",{bubbles:!0,composed:!0,detail:{source:i,selected:t}});this.dispatchEvent(e)}connectedCallback(){super.connectedCallback(),this.noninteractive||this.setAttribute("mwc-list-item","");for(const t of this.listeners)for(const i of t.eventNames)t.target.addEventListener(i,t.cb,{passive:!0})}disconnectedCallback(){super.disconnectedCallback();for(const t of this.listeners)for(const i of t.eventNames)t.target.removeEventListener(i,t.cb);this._managingList&&(this._managingList.debouncedLayout?this._managingList.debouncedLayout(!0):this._managingList.layout(!0))}firstUpdated(){const t=new Event("list-item-rendered",{bubbles:!0,composed:!0});this.dispatchEvent(t)}}(0,s.__decorate)([(0,n.IO)("slot")],l.prototype,"slotElement",void 0),(0,s.__decorate)([(0,n.GC)("mwc-ripple")],l.prototype,"ripple",void 0),(0,s.__decorate)([(0,n.Cb)({type:String})],l.prototype,"value",void 0),(0,s.__decorate)([(0,n.Cb)({type:String,reflect:!0})],l.prototype,"group",void 0),(0,s.__decorate)([(0,n.Cb)({type:Number,reflect:!0})],l.prototype,"tabindex",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0}),(0,a.P)((function(t){t?this.setAttribute("aria-disabled","true"):this.setAttribute("aria-disabled","false")}))],l.prototype,"disabled",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0})],l.prototype,"twoline",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0})],l.prototype,"activated",void 0),(0,s.__decorate)([(0,n.Cb)({type:String,reflect:!0})],l.prototype,"graphic",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean})],l.prototype,"multipleGraphics",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean})],l.prototype,"hasMeta",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0}),(0,a.P)((function(t){t?(this.removeAttribute("aria-checked"),this.removeAttribute("mwc-list-item"),this.selected=!1,this.activated=!1,this.tabIndex=-1):this.setAttribute("mwc-list-item","")}))],l.prototype,"noninteractive",void 0),(0,s.__decorate)([(0,n.Cb)({type:Boolean,reflect:!0}),(0,a.P)((function(t){const i=this.getAttribute("role"),e="gridcell"===i||"option"===i||"row"===i||"tab"===i;e&&t?this.setAttribute("aria-selected","true"):e&&this.setAttribute("aria-selected","false"),this._firstChanged?this._firstChanged=!1:this._skipPropRequest||this.fireRequestSelected(t,"property")}))],l.prototype,"selected",void 0),(0,s.__decorate)([(0,n.SB)()],l.prototype,"shouldRenderRipple",void 0),(0,s.__decorate)([(0,n.SB)()],l.prototype,"_managingList",void 0)},96762:(t,i,e)=>{e.d(i,{W:()=>s});const s=e(37500).iv`:host{cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent;height:48px;display:flex;position:relative;align-items:center;justify-content:flex-start;overflow:hidden;padding:0;padding-left:var(--mdc-list-side-padding, 16px);padding-right:var(--mdc-list-side-padding, 16px);outline:none;height:48px;color:rgba(0,0,0,.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host:focus{outline:none}:host([activated]){color:#6200ee;color:var(--mdc-theme-primary, #6200ee);--mdc-ripple-color: var( --mdc-theme-primary, #6200ee )}:host([activated]) .mdc-deprecated-list-item__graphic{color:#6200ee;color:var(--mdc-theme-primary, #6200ee)}:host([activated]) .fake-activated-ripple::before{position:absolute;display:block;top:0;bottom:0;left:0;right:0;width:100%;height:100%;pointer-events:none;z-index:1;content:"";opacity:0.12;opacity:var(--mdc-ripple-activated-opacity, 0.12);background-color:#6200ee;background-color:var(--mdc-ripple-color, var(--mdc-theme-primary, #6200ee))}.mdc-deprecated-list-item__graphic{flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;display:inline-flex}.mdc-deprecated-list-item__graphic ::slotted(*){flex-shrink:0;align-items:center;justify-content:center;fill:currentColor;width:100%;height:100%;text-align:center}.mdc-deprecated-list-item__meta{width:var(--mdc-list-item-meta-size, 24px);height:var(--mdc-list-item-meta-size, 24px);margin-left:auto;margin-right:0;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-hint-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-item__meta.multi{width:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:var(--mdc-list-item-meta-size, 24px);line-height:var(--mdc-list-item-meta-size, 24px)}.mdc-deprecated-list-item__meta ::slotted(.material-icons),.mdc-deprecated-list-item__meta ::slotted(mwc-icon){line-height:var(--mdc-list-item-meta-size, 24px) !important}.mdc-deprecated-list-item__meta ::slotted(:not(.material-icons):not(mwc-icon)){-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-caption-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.75rem;font-size:var(--mdc-typography-caption-font-size, 0.75rem);line-height:1.25rem;line-height:var(--mdc-typography-caption-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-caption-font-weight, 400);letter-spacing:0.0333333333em;letter-spacing:var(--mdc-typography-caption-letter-spacing, 0.0333333333em);text-decoration:inherit;text-decoration:var(--mdc-typography-caption-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-caption-text-transform, inherit)}[dir=rtl] .mdc-deprecated-list-item__meta,.mdc-deprecated-list-item__meta[dir=rtl]{margin-left:0;margin-right:auto}.mdc-deprecated-list-item__meta ::slotted(*){width:100%;height:100%}.mdc-deprecated-list-item__text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden}.mdc-deprecated-list-item__text ::slotted([for]),.mdc-deprecated-list-item__text[for]{pointer-events:none}.mdc-deprecated-list-item__primary-text{text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;margin-bottom:-20px;display:block}.mdc-deprecated-list-item__primary-text::before{display:inline-block;width:0;height:32px;content:"";vertical-align:0}.mdc-deprecated-list-item__primary-text::after{display:inline-block;width:0;height:20px;content:"";vertical-align:-20px}.mdc-deprecated-list-item__secondary-text{-moz-osx-font-smoothing:grayscale;-webkit-font-smoothing:antialiased;font-family:Roboto, sans-serif;font-family:var(--mdc-typography-body2-font-family, var(--mdc-typography-font-family, Roboto, sans-serif));font-size:0.875rem;font-size:var(--mdc-typography-body2-font-size, 0.875rem);line-height:1.25rem;line-height:var(--mdc-typography-body2-line-height, 1.25rem);font-weight:400;font-weight:var(--mdc-typography-body2-font-weight, 400);letter-spacing:0.0178571429em;letter-spacing:var(--mdc-typography-body2-letter-spacing, 0.0178571429em);text-decoration:inherit;text-decoration:var(--mdc-typography-body2-text-decoration, inherit);text-transform:inherit;text-transform:var(--mdc-typography-body2-text-transform, inherit);text-overflow:ellipsis;white-space:nowrap;overflow:hidden;display:block;margin-top:0;line-height:normal;display:block}.mdc-deprecated-list-item__secondary-text::before{display:inline-block;width:0;height:20px;content:"";vertical-align:0}.mdc-deprecated-list--dense .mdc-deprecated-list-item__secondary-text{font-size:inherit}* ::slotted(a),a{color:inherit;text-decoration:none}:host([twoline]){height:72px}:host([twoline]) .mdc-deprecated-list-item__text{align-self:flex-start}:host([disabled]),:host([noninteractive]){cursor:default;pointer-events:none}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*){opacity:.38}:host([disabled]) .mdc-deprecated-list-item__text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__primary-text ::slotted(*),:host([disabled]) .mdc-deprecated-list-item__secondary-text ::slotted(*){color:#000;color:var(--mdc-theme-on-surface, #000)}.mdc-deprecated-list-item__secondary-text ::slotted(*){color:rgba(0, 0, 0, 0.54);color:var(--mdc-theme-text-secondary-on-background, rgba(0, 0, 0, 0.54))}.mdc-deprecated-list-item__graphic ::slotted(*){background-color:transparent;color:rgba(0, 0, 0, 0.38);color:var(--mdc-theme-text-icon-on-background, rgba(0, 0, 0, 0.38))}.mdc-deprecated-list-group__subheader ::slotted(*){color:rgba(0, 0, 0, 0.87);color:var(--mdc-theme-text-primary-on-background, rgba(0, 0, 0, 0.87))}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 40px);height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 40px);line-height:var(--mdc-list-item-graphic-size, 40px)}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 40px) !important}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic ::slotted(*){border-radius:50%}:host([graphic=avatar]) .mdc-deprecated-list-item__graphic,:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic,:host([graphic=control]) .mdc-deprecated-list-item__graphic{margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 16px)}[dir=rtl] :host([graphic=avatar]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=medium]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=large]) .mdc-deprecated-list-item__graphic,[dir=rtl] :host([graphic=control]) .mdc-deprecated-list-item__graphic,:host([graphic=avatar]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=medium]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=large]) .mdc-deprecated-list-item__graphic[dir=rtl],:host([graphic=control]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 16px);margin-right:0}:host([graphic=icon]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 24px);height:var(--mdc-list-item-graphic-size, 24px);margin-left:0;margin-right:var(--mdc-list-item-graphic-margin, 32px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 24px);line-height:var(--mdc-list-item-graphic-size, 24px)}:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=icon]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 24px) !important}[dir=rtl] :host([graphic=icon]) .mdc-deprecated-list-item__graphic,:host([graphic=icon]) .mdc-deprecated-list-item__graphic[dir=rtl]{margin-left:var(--mdc-list-item-graphic-margin, 32px);margin-right:0}:host([graphic=avatar]:not([twoLine])),:host([graphic=icon]:not([twoLine])){height:56px}:host([graphic=medium]:not([twoLine])),:host([graphic=large]:not([twoLine])){height:72px}:host([graphic=medium]) .mdc-deprecated-list-item__graphic,:host([graphic=large]) .mdc-deprecated-list-item__graphic{width:var(--mdc-list-item-graphic-size, 56px);height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic.multi,:host([graphic=large]) .mdc-deprecated-list-item__graphic.multi{width:auto}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(*),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(*){width:var(--mdc-list-item-graphic-size, 56px);line-height:var(--mdc-list-item-graphic-size, 56px)}:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=medium]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(.material-icons),:host([graphic=large]) .mdc-deprecated-list-item__graphic ::slotted(mwc-icon){line-height:var(--mdc-list-item-graphic-size, 56px) !important}:host([graphic=large]){padding-left:0px}`},89833:(t,i,e)=>{e.d(i,{O:()=>c});var s=e(87480),a=e(86251),o=e(37500),r=e(33310),n=e(8636),h=e(51346),l=e(71260);const d={fromAttribute:t=>null!==t&&(""===t||t),toAttribute:t=>"boolean"==typeof t?t?"":null:t};class c extends a.P{constructor(){super(...arguments),this.rows=2,this.cols=20,this.charCounter=!1}render(){const t=this.charCounter&&-1!==this.maxLength,i=t&&"internal"===this.charCounter,e=t&&!i,s=!!this.helper||!!this.validationMessage||e,a={"mdc-text-field--disabled":this.disabled,"mdc-text-field--no-label":!this.label,"mdc-text-field--filled":!this.outlined,"mdc-text-field--outlined":this.outlined,"mdc-text-field--end-aligned":this.endAligned,"mdc-text-field--with-internal-counter":i};return o.dy`
      <label class="mdc-text-field mdc-text-field--textarea ${(0,n.$)(a)}">
        ${this.renderRipple()}
        ${this.outlined?this.renderOutline():this.renderLabel()}
        ${this.renderInput()}
        ${this.renderCharCounter(i)}
        ${this.renderLineRipple()}
      </label>
      ${this.renderHelperText(s,e)}
    `}renderInput(){const t=this.label?"label":void 0,i=-1===this.minLength?void 0:this.minLength,e=-1===this.maxLength?void 0:this.maxLength,s=this.autocapitalize?this.autocapitalize:void 0;return o.dy`
      <textarea
          aria-labelledby=${(0,h.o)(t)}
          class="mdc-text-field__input"
          .value="${(0,l.a)(this.value)}"
          rows="${this.rows}"
          cols="${this.cols}"
          ?disabled="${this.disabled}"
          placeholder="${this.placeholder}"
          ?required="${this.required}"
          ?readonly="${this.readOnly}"
          minlength="${(0,h.o)(i)}"
          maxlength="${(0,h.o)(e)}"
          name="${(0,h.o)(""===this.name?void 0:this.name)}"
          inputmode="${(0,h.o)(this.inputMode)}"
          autocapitalize="${(0,h.o)(s)}"
          @input="${this.handleInputChange}"
          @blur="${this.onInputBlur}">
      </textarea>`}}(0,s.__decorate)([(0,r.IO)("textarea")],c.prototype,"formElement",void 0),(0,s.__decorate)([(0,r.Cb)({type:Number})],c.prototype,"rows",void 0),(0,s.__decorate)([(0,r.Cb)({type:Number})],c.prototype,"cols",void 0),(0,s.__decorate)([(0,r.Cb)({converter:d})],c.prototype,"charCounter",void 0)},96791:(t,i,e)=>{e.d(i,{W:()=>s});const s=e(37500).iv`.mdc-text-field{height:100%}.mdc-text-field__input{resize:none}`},54444:(t,i,e)=>{e(48175);var s=e(9672),a=e(87156),o=e(50856);(0,s.k)({_template:o.d`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=(0,a.vz)(this).parentNode,i=(0,a.vz)(this).getOwnerRoot();return this.for?(0,a.vz)(i).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?i.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===(0,a.vz)(this).textContent.trim()){for(var t=!0,i=(0,a.vz)(this).getEffectiveChildNodes(),e=0;e<i.length;e++)if(""!==i[e].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var i,e,s=this.offsetParent.getBoundingClientRect(),a=this._target.getBoundingClientRect(),o=this.getBoundingClientRect(),r=(a.width-o.width)/2,n=(a.height-o.height)/2,h=a.left-s.left,l=a.top-s.top;switch(this.position){case"top":i=h+r,e=l-o.height-t;break;case"bottom":i=h+r,e=l+a.height+t;break;case"left":i=h-o.width-t,e=l+n;break;case"right":i=h+a.width+t,e=l+n}this.fitToVisibleBounds?(s.left+i+o.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,i)+"px",this.style.right="auto"),s.top+e+o.height>window.innerHeight?(this.style.bottom=s.height-l+t+"px",this.style.top="auto"):(this.style.top=Math.max(-s.top,e)+"px",this.style.bottom="auto")):(this.style.left=i+"px",this.style.top=e+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var i=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":i+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":i+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},31157:(t,i,e)=>{e.d(i,{e:()=>r});var s=e(73418);function a(t){return"horizontal"===t?"row":"column"}class o extends s.IE{constructor(){super(...arguments),this._itemSize={},this._gaps={},this._padding={}}get _defaultConfig(){return Object.assign({},super._defaultConfig,{itemSize:{width:"300px",height:"300px"},gap:"8px",padding:"match-gap"})}get _gap(){return this._gaps.row}get _idealSize(){return this._itemSize[(0,s.qF)(this.direction)]}get _idealSize1(){return this._itemSize[(0,s.qF)(this.direction)]}get _idealSize2(){return this._itemSize[(0,s.gu)(this.direction)]}get _gap1(){return this._gaps[(t=this.direction,"horizontal"===t?"column":"row")];var t}get _gap2(){return this._gaps[a(this.direction)]}get _padding1(){const t=this._padding,[i,e]="horizontal"===this.direction?["left","right"]:["top","bottom"];return[t[i],t[e]]}get _padding2(){const t=this._padding,[i,e]="horizontal"===this.direction?["top","bottom"]:["left","right"];return[t[i],t[e]]}set itemSize(t){const i=this._itemSize,e=parseInt(t.width),s=parseInt(t.height);e!==i.width&&(i.width=e,this._triggerReflow()),s!==i.height&&(i.height=s,this._triggerReflow())}_setGap(t){const i=t.split(" ").map((t=>function(t){return"auto"===t?1/0:parseInt(t)}(t))),e=this._gaps;i[0]!==e.row&&(e.row=i[0],this._triggerReflow()),void 0===i[1]?i[0]!==e.column&&(e.column=i[0],this._triggerReflow()):i[1]!==e.column&&(e.column=i[1],this._triggerReflow())}set padding(t){const i=this._padding,e=t.split(" ").map((t=>function(t){return"match-gap"===t?1/0:parseInt(t)}(t)));1===e.length?i.top=i.right=i.bottom=i.left=e[0]:2===e.length?(i.top=i.bottom=e[0],i.right=i.left=e[1]):3===e.length?(i.top=e[0],i.right=i.left=e[1],i.bottom=e[2]):4===e.length&&["top","right","bottom","left"].forEach(((t,s)=>i[t]=e[s]))}}const r=t=>Object.assign({type:n},t);class n extends o{constructor(){super(...arguments),this._metrics=null,this.flex=null,this.justify=null}get _defaultConfig(){return Object.assign({},super._defaultConfig,{flex:!1,justify:"start"})}set gap(t){this._setGap(t)}_updateLayout(){const t=this.justify,[i,e]=this._padding1,[o,r]=this._padding2;["_gap1","_gap2"].forEach((i=>{const e=this[i];if(e===1/0&&!["space-between","space-around","space-evenly"].includes(t))throw new Error("grid layout: gap can only be set to 'auto' when justify is set to 'space-between', 'space-around' or 'space-evenly'");if(e===1/0&&"_gap2"===i)throw new Error(`grid layout: ${a(this.direction)}-gap cannot be set to 'auto' when direction is set to ${this.direction}`)}));const n={rolumns:-1,itemSize1:-1,itemSize2:-1,gap1:this._gap1===1/0?-1:this._gap1,gap2:this._gap2,padding1:{start:i===1/0?this._gap1:i,end:e===1/0?this._gap1:e},padding2:{start:o===1/0?this._gap2:o,end:r===1/0?this._gap2:r},positions:[]};let h=this._viewDim2;this.flex||["start","center","end"].includes(t)?(h-=n.padding2.start,h-=n.padding2.end):"space-between"===t?h+=n.gap2:"space-evenly"===t&&(h-=n.gap2);const l=h/(this._idealSize2+n.gap2);if(this.flex){switch(n.rolumns=Math.round(l),n.itemSize2=Math.round((h-n.gap2*(n.rolumns-1))/n.rolumns),!0===this.flex?"area":this.flex.preserve){case"aspect-ratio":n.itemSize1=Math.round(this._idealSize1/this._idealSize2*n.itemSize2);break;case(0,s.qF)(this.direction):n.itemSize1=Math.round(this._idealSize1);break;default:n.itemSize1=Math.round(this._idealSize1*this._idealSize2/n.itemSize2)}}else n.itemSize1=this._idealSize1,n.itemSize2=this._idealSize2,n.rolumns=Math.floor(l);let d,c;if(this.flex||["start","center","end"].includes(t)){const i=n.rolumns*n.itemSize2+(n.rolumns-1)*n.gap2;d=this.flex||"start"===t?n.padding2.start:"end"===t?this._viewDim2-n.padding2.end-i:Math.round(this._viewDim2/2-i/2),c=n.gap2}else{const s=h-n.rolumns*n.itemSize2;"space-between"===t?(c=Math.round(s/(n.rolumns-1)),d=0):"space-around"===t?(c=Math.round(s/n.rolumns),d=Math.round(c/2)):(c=Math.round(s/(n.rolumns+1)),d=c),this._gap1===1/0&&(n.gap1=c,i===1/0&&(n.padding1.start=d),e===1/0&&(n.padding1.end=d))}for(let t=0;t<n.rolumns;t++)n.positions.push(d),d+=n.itemSize2+c;this._metrics=n}get _delta(){return this._metrics.itemSize1+this._metrics.gap1}_getItemSize(t){return{[this._sizeDim]:this._metrics.itemSize1,[this._secondarySizeDim]:this._metrics.itemSize2}}_getActiveItems(){const{padding1:t}=this._metrics,i=Math.max(0,this._scrollPosition-this._overhang),e=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang),s=Math.max(0,Math.floor((i-t.start)/this._delta)),a=Math.max(0,Math.ceil((e-t.start)/this._delta));this._first=s*this._metrics.rolumns,this._last=Math.min(a*this._metrics.rolumns-1,this._totalItems-1),this._physicalMin=t.start+this._delta*s,this._physicalMax=t.start+this._delta*a}_getItemPosition(t){const{rolumns:i,padding1:e,positions:a,itemSize1:o,itemSize2:r}=this._metrics;return{[this._positionDim]:e.start+Math.floor(t/i)*this._delta,[this._secondaryPositionDim]:a[t%i],[(0,s.qF)(this.direction)]:o,[(0,s.gu)(this.direction)]:r}}_updateScrollSize(){this._scrollSize=Math.max(1,Math.ceil(this._totalItems/this._metrics.rolumns)*this._delta+this._gap)}}},73418:(t,i,e)=>{let s,a;async function o(){return a||async function(){s=window.EventTarget;try{new s}catch(t){s=(await e.e(98251).then(e.t.bind(e,98251,19))).default.EventTarget}return a=s}()}function r(t){return"horizontal"===t?"width":"height"}function n(t){return"horizontal"===t?"height":"width"}e.d(i,{IE:()=>h,qF:()=>r,gu:()=>n});class h{constructor(t){this._latestCoords={left:0,top:0},this._direction=null,this._viewportSize={width:0,height:0},this._pendingReflow=!1,this._pendingLayoutUpdate=!1,this._scrollToIndex=-1,this._scrollToAnchor=0,this._firstVisible=0,this._lastVisible=0,this._eventTargetPromise=o().then((t=>{this._eventTarget=new t})),this._physicalMin=0,this._physicalMax=0,this._first=-1,this._last=-1,this._sizeDim="height",this._secondarySizeDim="width",this._positionDim="top",this._secondaryPositionDim="left",this._scrollPosition=0,this._scrollError=0,this._totalItems=0,this._scrollSize=1,this._overhang=1e3,this._eventTarget=null,Promise.resolve().then((()=>this.config=t||this._defaultConfig))}get _defaultConfig(){return{direction:"vertical"}}set config(t){Object.assign(this,Object.assign({},this._defaultConfig,t))}get config(){return{direction:this.direction}}get totalItems(){return this._totalItems}set totalItems(t){const i=Number(t);i!==this._totalItems&&(this._totalItems=i,this._scheduleReflow())}get direction(){return this._direction}set direction(t){(t="horizontal"===t?t:"vertical")!==this._direction&&(this._direction=t,this._sizeDim="horizontal"===t?"width":"height",this._secondarySizeDim="horizontal"===t?"height":"width",this._positionDim="horizontal"===t?"left":"top",this._secondaryPositionDim="horizontal"===t?"top":"left",this._triggerReflow())}get viewportSize(){return this._viewportSize}set viewportSize(t){const{_viewDim1:i,_viewDim2:e}=this;Object.assign(this._viewportSize,t),e!==this._viewDim2?this._scheduleLayoutUpdate():i!==this._viewDim1&&this._checkThresholds()}get viewportScroll(){return this._latestCoords}set viewportScroll(t){Object.assign(this._latestCoords,t);const i=this._scrollPosition;this._scrollPosition=this._latestCoords[this._positionDim],i!==this._scrollPosition&&(this._scrollPositionChanged(i,this._scrollPosition),this._updateVisibleIndices({emit:!0})),this._checkThresholds()}reflowIfNeeded(t=!1){(t||this._pendingReflow)&&(this._pendingReflow=!1,this._reflow())}scrollToIndex(t,i="start"){if(Number.isFinite(t)){switch(t=Math.min(this.totalItems,Math.max(0,t)),this._scrollToIndex=t,"nearest"===i&&(i=t>this._first+this._num/2?"end":"start"),i){case"start":this._scrollToAnchor=0;break;case"center":this._scrollToAnchor=.5;break;case"end":this._scrollToAnchor=1;break;default:throw new TypeError("position must be one of: start, center, end, nearest")}this._scheduleReflow()}}async dispatchEvent(t){await this._eventTargetPromise,this._eventTarget.dispatchEvent(t)}async addEventListener(t,i,e){await this._eventTargetPromise,this._eventTarget.addEventListener(t,i,e)}async removeEventListener(t,i,e){await this._eventTargetPromise,this._eventTarget.removeEventListener(t,i,e)}_updateLayout(){}get _viewDim1(){return this._viewportSize[this._sizeDim]}get _viewDim2(){return this._viewportSize[this._secondarySizeDim]}_scheduleReflow(){this._pendingReflow=!0}_scheduleLayoutUpdate(){this._pendingLayoutUpdate=!0,this._scheduleReflow()}_triggerReflow(){this._scheduleLayoutUpdate(),Promise.resolve().then((()=>this.reflowIfNeeded()))}_reflow(){this._pendingLayoutUpdate&&(this._updateLayout(),this._pendingLayoutUpdate=!1),this._updateScrollSize(),this._getActiveItems(),this._scrollIfNeeded(),this._updateVisibleIndices(),this._emitScrollSize(),this._emitRange(),this._emitChildPositions(),this._emitScrollError()}_scrollIfNeeded(){if(-1===this._scrollToIndex)return;const t=this._scrollToIndex,i=this._scrollToAnchor,e=this._getItemPosition(t)[this._positionDim],s=this._getItemSize(t)[this._sizeDim],a=this._scrollPosition+this._viewDim1*i,o=e+s*i,r=Math.floor(Math.min(this._scrollSize-this._viewDim1,Math.max(0,this._scrollPosition-a+o)));this._scrollError+=this._scrollPosition-r,this._scrollPosition=r}_emitRange(t){const i=Object.assign({first:this._first,last:this._last,num:this._num,stable:!0,firstVisible:this._firstVisible,lastVisible:this._lastVisible},t);this.dispatchEvent(new CustomEvent("rangechange",{detail:i}))}_emitScrollSize(){const t={[this._sizeDim]:this._scrollSize};this.dispatchEvent(new CustomEvent("scrollsizechange",{detail:t}))}_emitScrollError(){if(this._scrollError){const t={[this._positionDim]:this._scrollError,[this._secondaryPositionDim]:0};this.dispatchEvent(new CustomEvent("scrollerrorchange",{detail:t})),this._scrollError=0}}_emitChildPositions(){const t={};for(let i=this._first;i<=this._last;i++)t[i]=this._getItemPosition(i);this.dispatchEvent(new CustomEvent("itempositionchange",{detail:t}))}get _num(){return-1===this._first||-1===this._last?0:this._last-this._first+1}_checkThresholds(){if(0===this._viewDim1&&this._num>0)this._scheduleReflow();else{const t=Math.max(0,this._scrollPosition-this._overhang),i=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang);(this._physicalMin>t||this._physicalMax<i)&&this._scheduleReflow()}}_updateVisibleIndices(t){if(-1===this._first||-1===this._last)return;let i=this._first;for(;i<this._last&&Math.round(this._getItemPosition(i)[this._positionDim]+this._getItemSize(i)[this._sizeDim])<=Math.round(this._scrollPosition);)i++;let e=this._last;for(;e>this._first&&Math.round(this._getItemPosition(e)[this._positionDim])>=Math.round(this._scrollPosition+this._viewDim1);)e--;i===this._firstVisible&&e===this._lastVisible||(this._firstVisible=i,this._lastVisible=e,t&&t.emit&&this._emitRange())}_scrollPositionChanged(t,i){const e=this._scrollSize-this._viewDim1;(t<e||i<e)&&(this._scrollToIndex=-1)}}}}]);
//# sourceMappingURL=71d59c51.js.map