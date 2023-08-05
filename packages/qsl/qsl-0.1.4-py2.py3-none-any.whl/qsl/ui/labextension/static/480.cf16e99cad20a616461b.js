"use strict";(self.webpackChunkqslwidgets=self.webpackChunkqslwidgets||[]).push([[480],{4458:function(e,t,a){var l=this&&this.__importDefault||function(e){return e&&e.__esModule?e:{default:e}};Object.defineProperty(t,"__esModule",{value:!0}),t.defaultWidgetState=t.CommonWidget=void 0;const i=l(a(6271)),s=a(8564),n=a(559);t.defaultWidgetState={states:[],urls:[],type:"image",transitioning:!1,config:{image:[],regions:[]},labels:{image:{},polygons:[],masks:[],boxes:[]},action:"",preload:[],maxCanvasSize:512,maxViewHeight:512,buttons:{next:!0,prev:!0,save:!0,config:!0,delete:!0,ignore:!0,unignore:!0},base:{serverRoot:"",url:""},progress:-1,mode:"light"},t.CommonWidget=({extract:e})=>{var t,a;const l=e("config"),r=e("states"),o=e("transitioning"),u=e("urls"),d=e("type"),c=e("labels"),b=e("action"),m=e("progress"),p=e("mode"),g=e("buttons"),v=e("preload"),f=e("maxCanvasSize"),_=e("maxViewHeight"),h={config:{image:(null===(t=l.value)||void 0===t?void 0:t.image)||[],regions:(null===(a=l.value)||void 0===a?void 0:a.regions)||[]},preload:v.value,options:{progress:m.value,maxCanvasSize:f.value,showNavigation:!0},callbacks:{onSave:g.value.save?e=>{c.set(e),b.set("save")}:void 0,onSaveConfig:g.value.config?l.set:void 0,onNext:g.value.next?()=>b.set("next"):void 0,onPrev:g.value.prev?()=>b.set("prev"):void 0,onDelete:g.value.delete?()=>b.set("delete"):void 0,onIgnore:g.value.ignore?()=>b.set("ignore"):void 0,onUnignore:g.value.unignore?()=>b.set("unignore"):void 0}};return i.default.createElement(s.ThemeProvider,{theme:s.createTheme({palette:{mode:p.value||"light"}})},i.default.createElement(s.ScopedCssBaseline,null,i.default.createElement(s.Box,{style:{padding:16}},i.default.createElement(n.Labeler,null,0===r.value.length?null:1==r.value.length?"image"===d.value?i.default.createElement(n.ImageLabeler,Object.assign({},h,{maxViewHeight:_.value,labels:c.value||{},target:u.value[0],metadata:o.value?{}:r.value[0].metadata})):i.default.createElement(n.VideoLabeler,Object.assign({},h,{maxViewHeight:_.value,labels:Array.isArray(c.value)?c.value:[],target:u.value[0],metadata:o.value?{}:r.value[0].metadata})):i.default.createElement(n.BatchImageLabeler,Object.assign({},h,{labels:c.value||{},target:u.value,states:o.value?[]:r.value,setStates:e=>r.set(e)}))))))}},2639:function(e,t,a){var l=this&&this.__importDefault||function(e){return e&&e.__esModule?e:{default:e}};Object.defineProperty(t,"__esModule",{value:!0}),t.MediaLabelerView=t.MediaLabelerModel=void 0;const i=l(a(6271)),s=l(a(4456)),n=a(5294),r=a(2565),o=a(7295),u=a(4458),d=a(8657),c=({model:e})=>{const t=o.useModelStateExtractor(e),a=t("base");return i.default.useEffect((()=>{a.set({serverRoot:n.PageConfig.getOption("serverRoot"),url:n.PageConfig.getBaseUrl()})})),i.default.createElement(u.CommonWidget,{extract:t})};class b extends r.DOMWidgetModel{defaults(){return Object.assign(Object.assign(Object.assign({},super.defaults()),{_model_name:b.model_name,_model_module:b.model_module,_model_module_version:b.model_module_version,_view_name:b.view_name,_view_module:b.view_module,_view_module_version:b.view_module_version}),u.defaultWidgetState)}}t.MediaLabelerModel=b,b.serializers=Object.assign({},r.DOMWidgetModel.serializers),b.model_name="MediaLabelerModel",b.model_module=d.MODULE_NAME,b.model_module_version=d.MODULE_VERSION,b.view_name="MediaLabelerView",b.view_module=d.MODULE_NAME,b.view_module_version=d.MODULE_VERSION;class m extends r.DOMWidgetView{render(){this.el.classList.add("qsl-image-labeler-widget");const e=i.default.createElement(c,{model:this.model});s.default.render(e,this.el)}}t.MediaLabelerView=m},7295:function(e,t,a){var l=this&&this.__importDefault||function(e){return e&&e.__esModule?e:{default:e}};Object.defineProperty(t,"__esModule",{value:!0}),t.useModelEvent=t.useModelState=t.useModelStateExtractor=void 0;const i=l(a(6271)),s=(e,t)=>{const[a,l]=i.default.useState(null==t?void 0:t.get(e));return n(t,`change:${e}`,(t=>{l(t.get(e))}),[e]),{value:a,set:function(a,l){null==t||t.set(e,a,l),null==t||t.save_changes()}}};t.useModelState=s,t.useModelStateExtractor=e=>t=>s(t,e);const n=(e,t,a,l)=>{i.default.useEffect((()=>{const l=t=>e&&a(e,t);return null==e||e.on(t,l),()=>{null==e||e.unbind(t,l)}}),(l||[]).concat([e]))};t.useModelEvent=n},4480:(e,t,a)=>{Object.defineProperty(t,"__esModule",{value:!0});const l=a(2565),i=a(8657),s=a(2639),n={id:"qsl:plugin",requires:[l.IJupyterWidgetRegistry],activate:function(e,t){t.registerWidget({name:i.MODULE_NAME,version:i.MODULE_VERSION,exports:{MediaLabelerModel:s.MediaLabelerModel,MediaLabelerView:s.MediaLabelerView}})},autoStart:!0};t.default=n},8657:(e,t,a)=>{Object.defineProperty(t,"__esModule",{value:!0}),t.MODULE_NAME=t.MODULE_VERSION=void 0;const l=a(4147);t.MODULE_VERSION=l.version,t.MODULE_NAME=l.name},4147:e=>{e.exports=JSON.parse('{"name":"qslwidgets","version":"0.0.19","description":"Widgets for the QSL image labeling package.","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/faustomorales/qsl","bugs":{"url":"https://github.com/faustomorales/qsl/issues"},"license":"MIT","author":{"name":"Fausto Morales","email":"fausto@robinbay.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/faustomorales/qsl"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf qsl/labextension","clean:nbextension":"rimraf qsl/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","format":"prettier --write src","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@emotion/react":"^11.8.1","@emotion/styled":"^11.8.1","@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","@mui/icons-material":"^5.6.1","@mui/material":"^5.6.1","react":"^17.0.2","react-dom":"^17.0.2","react-highlight":"^0.14.0","react-image-labeler":"0.0.1-alpha.55"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@babel/preset-react":"^7.14.5","@babel/preset-typescript":"^7.14.5","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/react":"^17.0.11","@types/react-dom":"^17.0.8","@types/react-highlight":"^0.12.5","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","babel-loader":"^8.2.2","css-loader":"^6.7.1","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","html-webpack-plugin":"^5.5.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.0.0","webpack-cli":"^4.0.0"},"babel":{"presets":["@babel/preset-env","@babel/preset-react","@babel/preset-typescript"]},"jupyterlab":{"extension":"lib/plugin","outputDir":"../qsl/ui/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}')}}]);