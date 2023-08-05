/*! For license information please see ea33416f.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[52350,93152],{89833:(t,i,e)=>{e.d(i,{O:()=>c});var n=e(87480),o=e(86251),a=e(37500),s=e(33310),r=e(8636),l=e(51346),h=e(71260);const d={fromAttribute:t=>null!==t&&(""===t||t),toAttribute:t=>"boolean"==typeof t?t?"":null:t};class c extends o.P{constructor(){super(...arguments),this.rows=2,this.cols=20,this.charCounter=!1}render(){const t=this.charCounter&&-1!==this.maxLength,i=t&&"internal"===this.charCounter,e=t&&!i,n=!!this.helper||!!this.validationMessage||e,o={"mdc-text-field--disabled":this.disabled,"mdc-text-field--no-label":!this.label,"mdc-text-field--filled":!this.outlined,"mdc-text-field--outlined":this.outlined,"mdc-text-field--end-aligned":this.endAligned,"mdc-text-field--with-internal-counter":i};return a.dy`
      <label class="mdc-text-field mdc-text-field--textarea ${(0,r.$)(o)}">
        ${this.renderRipple()}
        ${this.outlined?this.renderOutline():this.renderLabel()}
        ${this.renderInput()}
        ${this.renderCharCounter(i)}
        ${this.renderLineRipple()}
      </label>
      ${this.renderHelperText(n,e)}
    `}renderInput(){const t=this.label?"label":void 0,i=-1===this.minLength?void 0:this.minLength,e=-1===this.maxLength?void 0:this.maxLength,n=this.autocapitalize?this.autocapitalize:void 0;return a.dy`
      <textarea
          aria-labelledby=${(0,l.o)(t)}
          class="mdc-text-field__input"
          .value="${(0,h.a)(this.value)}"
          rows="${this.rows}"
          cols="${this.cols}"
          ?disabled="${this.disabled}"
          placeholder="${this.placeholder}"
          ?required="${this.required}"
          ?readonly="${this.readOnly}"
          minlength="${(0,l.o)(i)}"
          maxlength="${(0,l.o)(e)}"
          name="${(0,l.o)(""===this.name?void 0:this.name)}"
          inputmode="${(0,l.o)(this.inputMode)}"
          autocapitalize="${(0,l.o)(n)}"
          @input="${this.handleInputChange}"
          @blur="${this.onInputBlur}">
      </textarea>`}}(0,n.__decorate)([(0,s.IO)("textarea")],c.prototype,"formElement",void 0),(0,n.__decorate)([(0,s.Cb)({type:Number})],c.prototype,"rows",void 0),(0,n.__decorate)([(0,s.Cb)({type:Number})],c.prototype,"cols",void 0),(0,n.__decorate)([(0,s.Cb)({converter:d})],c.prototype,"charCounter",void 0)},96791:(t,i,e)=>{e.d(i,{W:()=>n});const n=e(37500).iv`.mdc-text-field{height:100%}.mdc-text-field__input{resize:none}`},63207:(t,i,e)=>{e(65660),e(15112);var n=e(9672),o=e(87156),a=e(50856),s=e(48175);(0,n.k)({_template:a.d`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center-center;
        position: relative;

        vertical-align: middle;

        fill: var(--iron-icon-fill-color, currentcolor);
        stroke: var(--iron-icon-stroke-color, none);

        width: var(--iron-icon-width, 24px);
        height: var(--iron-icon-height, 24px);
        @apply --iron-icon;
      }

      :host([hidden]) {
        display: none;
      }
    </style>
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:s.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(t){var i=(t||"").split(":");this._iconName=i.pop(),this._iconsetName=i.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(t){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,o.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,o.vz)(this.root).appendChild(this._img))}})},89194:(t,i,e)=>{e(48175),e(65660),e(70019);var n=e(9672),o=e(50856);(0,n.k)({_template:o.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},54444:(t,i,e)=>{e(48175);var n=e(9672),o=e(87156),a=e(50856);(0,n.k)({_template:a.d`
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
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=(0,o.vz)(this).parentNode,i=(0,o.vz)(this).getOwnerRoot();return this.for?(0,o.vz)(i).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?i.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===(0,o.vz)(this).textContent.trim()){for(var t=!0,i=(0,o.vz)(this).getEffectiveChildNodes(),e=0;e<i.length;e++)if(""!==i[e].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var i,e,n=this.offsetParent.getBoundingClientRect(),o=this._target.getBoundingClientRect(),a=this.getBoundingClientRect(),s=(o.width-a.width)/2,r=(o.height-a.height)/2,l=o.left-n.left,h=o.top-n.top;switch(this.position){case"top":i=l+s,e=h-a.height-t;break;case"bottom":i=l+s,e=h+o.height+t;break;case"left":i=l-a.width-t,e=h+r;break;case"right":i=l+o.width+t,e=h+r}this.fitToVisibleBounds?(n.left+i+a.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,i)+"px",this.style.right="auto"),n.top+e+a.height>window.innerHeight?(this.style.bottom=n.height-h+t+"px",this.style.top="auto"):(this.style.top=Math.max(-n.top,e)+"px",this.style.bottom="auto")):(this.style.left=i+"px",this.style.top=e+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var i=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":i+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":i+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},21560:(t,i,e)=>{e.d(i,{ZH:()=>d,MT:()=>a,U2:()=>l,RV:()=>o,t8:()=>h});const n=function(){if(!(!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent))||!indexedDB.databases)return Promise.resolve();let t;return new Promise((i=>{const e=()=>indexedDB.databases().finally(i);t=setInterval(e,100),e()})).finally((()=>clearInterval(t)))};function o(t){return new Promise(((i,e)=>{t.oncomplete=t.onsuccess=()=>i(t.result),t.onabort=t.onerror=()=>e(t.error)}))}function a(t,i){const e=n().then((()=>{const e=indexedDB.open(t);return e.onupgradeneeded=()=>e.result.createObjectStore(i),o(e)}));return(t,n)=>e.then((e=>n(e.transaction(i,t).objectStore(i))))}let s;function r(){return s||(s=a("keyval-store","keyval")),s}function l(t,i=r()){return i("readonly",(i=>o(i.get(t))))}function h(t,i,e=r()){return e("readwrite",(e=>(e.put(i,t),o(e.transaction))))}function d(t=r()){return t("readwrite",(t=>(t.clear(),o(t.transaction))))}},97330:(t,i,e)=>{e.d(i,{_:()=>o,B:()=>a});var n=e(43715);const o=(t,i,e,o)=>{if(t[i])return t[i];let a,s=0,r=(0,n.M)();const l=()=>{if(!e)throw new Error("Collection does not support refresh");return e(t).then((t=>r.setState(t,!0)))},h=()=>l().catch((i=>{if(t.connected)throw i}));return t[i]={get state(){return r.state},refresh:l,subscribe(i){s++,1===s&&(o&&(a=o(t,r)),e&&(t.addEventListener("ready",h),h()));const n=r.subscribe(i);return void 0!==r.state&&setTimeout((()=>i(r.state)),0),()=>{n(),s--,s||(a&&a.then((t=>{t()})),t.removeEventListener("ready",l))}}},t[i]},a=(t,i,e,n,a)=>o(n,t,i,e).subscribe(a)},43715:(t,i,e)=>{e.d(i,{M:()=>n});const n=t=>{let i=[];function e(e,n){t=n?e:Object.assign(Object.assign({},t),e);let o=i;for(let i=0;i<o.length;i++)o[i](t)}return{get state(){return t},action(i){function n(t){e(t,!1)}return function(){let e=[t];for(let t=0;t<arguments.length;t++)e.push(arguments[t]);let o=i.apply(this,e);if(null!=o)return o instanceof Promise?o.then(n):n(o)}},setState:e,subscribe:t=>(i.push(t),()=>{!function(t){let e=[];for(let n=0;n<i.length;n++)i[n]===t?t=null:e.push(i[n]);i=e}(t)})}}},19596:(t,i,e)=>{e.d(i,{s:()=>c});var n=e(81563),o=e(38941);const a=(t,i)=>{var e,n;const o=t._$AN;if(void 0===o)return!1;for(const t of o)null===(n=(e=t)._$AO)||void 0===n||n.call(e,i,!1),a(t,i);return!0},s=t=>{let i,e;do{if(void 0===(i=t._$AM))break;e=i._$AN,e.delete(t),t=i}while(0===(null==e?void 0:e.size))},r=t=>{for(let i;i=t._$AM;t=i){let e=i._$AN;if(void 0===e)i._$AN=e=new Set;else if(e.has(t))break;e.add(t),d(i)}};function l(t){void 0!==this._$AN?(s(this),this._$AM=t,r(this)):this._$AM=t}function h(t,i=!1,e=0){const n=this._$AH,o=this._$AN;if(void 0!==o&&0!==o.size)if(i)if(Array.isArray(n))for(let t=e;t<n.length;t++)a(n[t],!1),s(n[t]);else null!=n&&(a(n,!1),s(n));else a(this,t)}const d=t=>{var i,e,n,a;t.type==o.pX.CHILD&&(null!==(i=(n=t)._$AP)&&void 0!==i||(n._$AP=h),null!==(e=(a=t)._$AQ)&&void 0!==e||(a._$AQ=l))};class c extends o.Xe{constructor(){super(...arguments),this._$AN=void 0}_$AT(t,i,e){super._$AT(t,i,e),r(this),this.isConnected=t._$AU}_$AO(t,i=!0){var e,n;t!==this.isConnected&&(this.isConnected=t,t?null===(e=this.reconnected)||void 0===e||e.call(this):null===(n=this.disconnected)||void 0===n||n.call(this)),i&&(a(this,t),s(this))}setValue(t){if((0,n.OR)(this._$Ct))this._$Ct._$AI(t,this);else{const i=[...this._$Ct._$AH];i[this._$Ci]=t,this._$Ct._$AI(i,this,0)}}disconnected(){}reconnected(){}}},1460:(t,i,e)=>{e.d(i,{l:()=>s});var n=e(15304),o=e(38941);const a={},s=(0,o.XM)(class extends o.Xe{constructor(){super(...arguments),this.nt=a}render(t,i){return i()}update(t,[i,e]){if(Array.isArray(i)){if(Array.isArray(this.nt)&&this.nt.length===i.length&&i.every(((t,i)=>t===this.nt[i])))return n.Jb}else if(this.nt===i)return n.Jb;return this.nt=Array.isArray(i)?Array.from(i):i,this.render(i,e)}})},22142:(t,i,e)=>{e.d(i,{C:()=>c});var n=e(15304),o=e(38941),a=e(81563),s=e(19596);class r{constructor(t){this.U=t}disconnect(){this.U=void 0}reconnect(t){this.U=t}deref(){return this.U}}class l{constructor(){this.Y=void 0,this.q=void 0}get(){return this.Y}pause(){var t;null!==(t=this.Y)&&void 0!==t||(this.Y=new Promise((t=>this.q=t)))}resume(){var t;null===(t=this.q)||void 0===t||t.call(this),this.Y=this.q=void 0}}const h=t=>!(0,a.pt)(t)&&"function"==typeof t.then;class d extends s.s{constructor(){super(...arguments),this._$Cft=1073741823,this._$Cwt=[],this._$CG=new r(this),this._$CK=new l}render(...t){var i;return null!==(i=t.find((t=>!h(t))))&&void 0!==i?i:n.Jb}update(t,i){const e=this._$Cwt;let o=e.length;this._$Cwt=i;const a=this._$CG,s=this._$CK;this.isConnected||this.disconnected();for(let t=0;t<i.length&&!(t>this._$Cft);t++){const n=i[t];if(!h(n))return this._$Cft=t,n;t<o&&n===e[t]||(this._$Cft=1073741823,o=0,Promise.resolve(n).then((async t=>{for(;s.get();)await s.get();const i=a.deref();if(void 0!==i){const e=i._$Cwt.indexOf(n);e>-1&&e<i._$Cft&&(i._$Cft=e,i.setValue(t))}})))}return n.Jb}disconnected(){this._$CG.disconnect(),this._$CK.pause()}reconnected(){this._$CG.reconnect(this),this._$CK.resume()}}const c=(0,o.XM)(d)}}]);
//# sourceMappingURL=ea33416f.js.map