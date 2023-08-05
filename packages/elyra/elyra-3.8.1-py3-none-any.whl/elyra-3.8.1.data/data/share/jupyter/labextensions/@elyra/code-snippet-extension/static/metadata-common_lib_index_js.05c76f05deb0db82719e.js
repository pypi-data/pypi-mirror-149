"use strict";
(self["webpackChunk_elyra_code_snippet_extension"] = self["webpackChunk_elyra_code_snippet_extension"] || []).push([["metadata-common_lib_index_js"],{

/***/ "../../node_modules/css-loader/dist/cjs.js!../metadata-common/style/index.css":
/*!************************************************************************************!*\
  !*** ../../node_modules/css-loader/dist/cjs.js!../metadata-common/style/index.css ***!
  \************************************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "../../node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../../node_modules/css-loader/dist/runtime/api.js */ "../../node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "/*\n * Copyright 2018-2022 Elyra Authors\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n * http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\n/* MetadataWidget CSS */\n.elyra-metadata {\n  color: var(--jp-ui-font-color1);\n  background: var(--jp-layout-color1);\n}\n\n.elyra-metadata a,\n.elyra-metadataEditor a {\n  color: var(--jp-content-link-color);\n}\n\n.elyra-metadataHeader {\n  font-weight: bold;\n  padding: 8px 10px;\n  display: flex;\n  justify-content: space-between;\n}\n\n.elyra-metadataHeader p {\n  font-weight: bold;\n}\n\n.elyra-metadataHeader-popper {\n  z-index: 100;\n}\n\n.elyra-metadataHeader-button:hover {\n  background-color: var(--jp-layout-color2);\n  cursor: pointer;\n}\n\n.elyra-metadataHeader-button.MuiButtonGroup-groupedTextHorizontal:not(:last-child) {\n  border-right: none;\n}\n\n.elyra-metadataHeader [fill] {\n  fill: var(--jp-ui-font-color1);\n}\n\n.elyra-metadataHeader + div:first-of-type {\n  overflow-y: auto;\n  height: calc(100vh - 95px);\n}\n\n.elyra-metadata-item {\n  border-bottom: var(--jp-border-width) solid var(--jp-border-color2);\n  display: flex;\n  flex-direction: column;\n  margin: 0;\n  padding: 0;\n}\n\n.elyra-metadata-item .elyra-expandableContainer-details-visible {\n  background-color: var(--jp-cell-editor-background);\n  resize: vertical;\n}\n\n.elyra-metadata-item .CodeMirror.cm-s-jupyter {\n  background-color: inherit;\n  border: none;\n  font-family: var(--jp-code-font-family);\n  font-size: var(--jp-code-font-size);\n  line-height: var(--jp-code-line-height);\n}\n\n.elyra-metadata-item .cm-s-jupyter li .cm-string {\n  word-break: normal;\n}\n\n/* MetadataEditor css */\n.elyra-metadataEditor .jp-InputGroup {\n  width: 100%;\n}\n\n.elyra-metadataEditor-formInput.elyra-metadataEditor-secure label {\n  margin-right: 70px;\n}\n\n.elyra-metadataEditor {\n  color: var(--jp-ui-font-color1);\n}\n\n.elyra-form-DropDown-item {\n  width: 100%;\n  display: flex;\n  flex-direction: column;\n  justify-content: left;\n  margin: 0;\n  border-radius: 0;\n}\n\n.elyra-metadataEditor {\n  padding: 20px;\n  display: flex;\n  flex-wrap: wrap;\n  height: 100%;\n  align-content: flex-start;\n  align-items: flex-start;\n  justify-content: flex-start;\n}\n\n.elyra-metadataEditor .elyra-metadataEditor-arrayInput li {\n  padding-left: 0;\n  padding-bottom: 0;\n}\n\n.elyra-metadataEditor\n  .elyra-metadataEditor-arrayInput\n  li:not(.elyra-metadataEditor-arrayItemEditor)\n  .elyra-elyra-metadataHeaderMuiInputBase-formControl {\n  background-color: var(--jp-border-color3);\n}\n\n.elyra-metadataEditor\n  .elyra-metadataEditor-arrayInput\n  .elyra-metadataEditor-editButtons\n  button {\n  padding: 3px;\n}\n\n.elyra-metadataEditor\n  .elyra-metadataEditor-arrayInput\n  .elyra-metadataEditor-addItemButton {\n  background-color: var(--jp-border-color1);\n}\n\n.elyra-metadataEditor .elyra-metadataEditor-arrayItemEditor {\n  display: flex;\n  padding: 6px 0 3px 0;\n}\n\n.elyra-metadataEditor h3 {\n  flex-basis: 100%;\n  margin-bottom: 15px;\n  color: var(--jp-ui-font-color1);\n}\n\n.elyra-metadataEditor .elyra-form-code.jp-CodeMirrorEditor {\n  background-color: var(--jp-cell-editor-background);\n  border: var(--jp-border-width) solid var(--jp-input-border-color);\n  overflow-y: auto;\n  resize: vertical;\n  min-height: 150px;\n  height: 150px;\n  padding-bottom: 10px;\n  cursor: initial;\n  margin-top: 5px;\n}\n\n.elyra-metadataEditor .CodeMirror.cm-s-jupyter {\n  background-color: inherit;\n  height: 100%;\n}\n\n.elyra-metadataEditor .elyra-metadataEditor-code {\n  height: auto;\n  flex-basis: 100%;\n  display: flex;\n  flex-direction: column;\n}\n\n.elyra-metadataEditor-formInput {\n  margin: 10px;\n  flex-basis: 45%;\n}\n\n.elyra-metadata-editor {\n  overflow-y: auto;\n}\n\n.elyra-metadataEditor .elyra-metadataEditor-saveButton {\n  flex-basis: 100%;\n  display: flex;\n}\n\n/* Code Snippet Filter CSS */\n.elyra-searchbar {\n  margin: 0px 8px;\n}\n\n.elyra-filterTools {\n  border-bottom: var(--jp-border-width) solid var(--jp-border-color1);\n}\n\nmark.elyra-search-bolding {\n  background-color: transparent;\n  font-weight: bold;\n  color: var(--jp-ui-font-color0);\n}\n\n.elyra-filter {\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  margin: 10px 10px 0 10px;\n}\n\n.elyra-filter .elyra-filter-btn {\n  align-self: flex-end;\n  padding: 0px;\n  margin-bottom: 5px;\n  border-radius: 5px;\n  border: none;\n  background: none;\n  cursor: pointer;\n}\n\n.elyra-filter .elyra-filter-btn:hover {\n  background-color: var(--jp-layout-color2);\n}\n\n.elyra-filter-btn svg {\n  display: block;\n  width: 30px;\n  height: 22px;\n}\n\n.elyra-filter-arrow-up.idle,\n.elyra-filter-option.idle {\n  display: none;\n}\n\n.elyra-filter-arrow-up {\n  position: absolute;\n  margin-top: 16px;\n  margin-right: 38px;\n  align-self: flex-end;\n  background-color: var(--jp-layout-color0);\n}\n\n.elyra-filter-option {\n  border: var(--jp-border-width) solid var(--jp-border-color1);\n  height: 140px;\n  width: 100%;\n  margin-bottom: 10px;\n  padding-top: 5px;\n  padding-bottom: 5px;\n  overflow: auto;\n}\n\n.elyra-filter-tags {\n  margin: 8px 8px;\n}\n\n.elyra-filter-tag {\n  margin-left: 3px;\n  margin-right: 3px;\n}\n\nbutton.elyra-filter-tag {\n  height: 24px;\n  padding: 0 12px;\n  cursor: pointer;\n  color: var(--jp-ui-font-color2);\n  font-size: var(--jp-ui-font-size1);\n}\n\nbutton.elyra-filter-tag .elyra-filter-tag-label {\n  overflow: hidden;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n}\n\nbutton.elyra-filter-tag span,\nbutton.elyra-filter-tag svg {\n  pointer-events: none;\n}\n\n.elyra-filter-empty {\n  font-size: var(--jp-ui-font-size1);\n}\n\n.elyra-tools {\n  border-bottom: var(--jp-border-width) solid var(--jp-border-color1);\n}\n\n.elyra-editor-tagList {\n  list-style: none;\n  margin-left: -3px;\n  margin-top: 4px;\n}\n\n.elyra-editor-tag {\n  margin-left: 3px;\n  margin-right: 3px;\n  padding: 0 12px;\n  height: 24px;\n}\n\nbutton.elyra-editor-tag {\n  cursor: pointer;\n  color: var(--jp-ui-font-color2);\n  font-size: var(--jp-ui-font-size1);\n}\n\nbutton.elyra-editor-tag.applied-tag {\n  color: var(--jp-ui-font-color1);\n}\n\nbutton.elyra-editor-tag.unapplied-tag {\n  color: var(--jp-ui-font-color2);\n  white-space: nowrap;\n}\n\n.elyra-editor-tag.tag.unapplied-tag input {\n  border: none;\n}\n\n/* Code Snippet Tags in InputDialog */\n.elyra-inputTagList {\n  list-style: none;\n}\n\n.elyra-inputTag {\n  margin-left: 8px;\n  margin-right: 8px;\n}\n\nbutton.elyra-inputTag {\n  cursor: pointer;\n  background: none;\n  border: none;\n  color: var(--jp-ui-font-color2);\n  padding: 0;\n  font-size: var(--jp-ui-font-size1);\n}\n\ninput.elyra-inputTag {\n  font-size: var(--jp-ui-font-size1);\n  background: none;\n  border: none;\n  color: var(--jp-ui-font-color2);\n  font-size: var(--jp-ui-font-size1);\n  width: 80px;\n  height: 15px;\n}\n\n.elyra-tags {\n  margin-top: 8px;\n}\n\n.elyra-no-metadata-msg {\n  padding-left: 8px;\n}\n", "",{"version":3,"sources":["webpack://./../metadata-common/style/index.css"],"names":[],"mappings":"AAAA;;;;;;;;;;;;;;EAcE;;AAEF,uBAAuB;AACvB;EACE,+BAA+B;EAC/B,mCAAmC;AACrC;;AAEA;;EAEE,mCAAmC;AACrC;;AAEA;EACE,iBAAiB;EACjB,iBAAiB;EACjB,aAAa;EACb,8BAA8B;AAChC;;AAEA;EACE,iBAAiB;AACnB;;AAEA;EACE,YAAY;AACd;;AAEA;EACE,yCAAyC;EACzC,eAAe;AACjB;;AAEA;EACE,kBAAkB;AACpB;;AAEA;EACE,8BAA8B;AAChC;;AAEA;EACE,gBAAgB;EAChB,0BAA0B;AAC5B;;AAEA;EACE,mEAAmE;EACnE,aAAa;EACb,sBAAsB;EACtB,SAAS;EACT,UAAU;AACZ;;AAEA;EACE,kDAAkD;EAClD,gBAAgB;AAClB;;AAEA;EACE,yBAAyB;EACzB,YAAY;EACZ,uCAAuC;EACvC,mCAAmC;EACnC,uCAAuC;AACzC;;AAEA;EACE,kBAAkB;AACpB;;AAEA,uBAAuB;AACvB;EACE,WAAW;AACb;;AAEA;EACE,kBAAkB;AACpB;;AAEA;EACE,+BAA+B;AACjC;;AAEA;EACE,WAAW;EACX,aAAa;EACb,sBAAsB;EACtB,qBAAqB;EACrB,SAAS;EACT,gBAAgB;AAClB;;AAEA;EACE,aAAa;EACb,aAAa;EACb,eAAe;EACf,YAAY;EACZ,yBAAyB;EACzB,uBAAuB;EACvB,2BAA2B;AAC7B;;AAEA;EACE,eAAe;EACf,iBAAiB;AACnB;;AAEA;;;;EAIE,yCAAyC;AAC3C;;AAEA;;;;EAIE,YAAY;AACd;;AAEA;;;EAGE,yCAAyC;AAC3C;;AAEA;EACE,aAAa;EACb,oBAAoB;AACtB;;AAEA;EACE,gBAAgB;EAChB,mBAAmB;EACnB,+BAA+B;AACjC;;AAEA;EACE,kDAAkD;EAClD,iEAAiE;EACjE,gBAAgB;EAChB,gBAAgB;EAChB,iBAAiB;EACjB,aAAa;EACb,oBAAoB;EACpB,eAAe;EACf,eAAe;AACjB;;AAEA;EACE,yBAAyB;EACzB,YAAY;AACd;;AAEA;EACE,YAAY;EACZ,gBAAgB;EAChB,aAAa;EACb,sBAAsB;AACxB;;AAEA;EACE,YAAY;EACZ,eAAe;AACjB;;AAEA;EACE,gBAAgB;AAClB;;AAEA;EACE,gBAAgB;EAChB,aAAa;AACf;;AAEA,4BAA4B;AAC5B;EACE,eAAe;AACjB;;AAEA;EACE,mEAAmE;AACrE;;AAEA;EACE,6BAA6B;EAC7B,iBAAiB;EACjB,+BAA+B;AACjC;;AAEA;EACE,aAAa;EACb,sBAAsB;EACtB,mBAAmB;EACnB,wBAAwB;AAC1B;;AAEA;EACE,oBAAoB;EACpB,YAAY;EACZ,kBAAkB;EAClB,kBAAkB;EAClB,YAAY;EACZ,gBAAgB;EAChB,eAAe;AACjB;;AAEA;EACE,yCAAyC;AAC3C;;AAEA;EACE,cAAc;EACd,WAAW;EACX,YAAY;AACd;;AAEA;;EAEE,aAAa;AACf;;AAEA;EACE,kBAAkB;EAClB,gBAAgB;EAChB,kBAAkB;EAClB,oBAAoB;EACpB,yCAAyC;AAC3C;;AAEA;EACE,4DAA4D;EAC5D,aAAa;EACb,WAAW;EACX,mBAAmB;EACnB,gBAAgB;EAChB,mBAAmB;EACnB,cAAc;AAChB;;AAEA;EACE,eAAe;AACjB;;AAEA;EACE,gBAAgB;EAChB,iBAAiB;AACnB;;AAEA;EACE,YAAY;EACZ,eAAe;EACf,eAAe;EACf,+BAA+B;EAC/B,kCAAkC;AACpC;;AAEA;EACE,gBAAgB;EAChB,uBAAuB;EACvB,mBAAmB;AACrB;;AAEA;;EAEE,oBAAoB;AACtB;;AAEA;EACE,kCAAkC;AACpC;;AAEA;EACE,mEAAmE;AACrE;;AAEA;EACE,gBAAgB;EAChB,iBAAiB;EACjB,eAAe;AACjB;;AAEA;EACE,gBAAgB;EAChB,iBAAiB;EACjB,eAAe;EACf,YAAY;AACd;;AAEA;EACE,eAAe;EACf,+BAA+B;EAC/B,kCAAkC;AACpC;;AAEA;EACE,+BAA+B;AACjC;;AAEA;EACE,+BAA+B;EAC/B,mBAAmB;AACrB;;AAEA;EACE,YAAY;AACd;;AAEA,qCAAqC;AACrC;EACE,gBAAgB;AAClB;;AAEA;EACE,gBAAgB;EAChB,iBAAiB;AACnB;;AAEA;EACE,eAAe;EACf,gBAAgB;EAChB,YAAY;EACZ,+BAA+B;EAC/B,UAAU;EACV,kCAAkC;AACpC;;AAEA;EACE,kCAAkC;EAClC,gBAAgB;EAChB,YAAY;EACZ,+BAA+B;EAC/B,kCAAkC;EAClC,WAAW;EACX,YAAY;AACd;;AAEA;EACE,eAAe;AACjB;;AAEA;EACE,iBAAiB;AACnB","sourcesContent":["/*\n * Copyright 2018-2022 Elyra Authors\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n * http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an \"AS IS\" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */\n\n/* MetadataWidget CSS */\n.elyra-metadata {\n  color: var(--jp-ui-font-color1);\n  background: var(--jp-layout-color1);\n}\n\n.elyra-metadata a,\n.elyra-metadataEditor a {\n  color: var(--jp-content-link-color);\n}\n\n.elyra-metadataHeader {\n  font-weight: bold;\n  padding: 8px 10px;\n  display: flex;\n  justify-content: space-between;\n}\n\n.elyra-metadataHeader p {\n  font-weight: bold;\n}\n\n.elyra-metadataHeader-popper {\n  z-index: 100;\n}\n\n.elyra-metadataHeader-button:hover {\n  background-color: var(--jp-layout-color2);\n  cursor: pointer;\n}\n\n.elyra-metadataHeader-button.MuiButtonGroup-groupedTextHorizontal:not(:last-child) {\n  border-right: none;\n}\n\n.elyra-metadataHeader [fill] {\n  fill: var(--jp-ui-font-color1);\n}\n\n.elyra-metadataHeader + div:first-of-type {\n  overflow-y: auto;\n  height: calc(100vh - 95px);\n}\n\n.elyra-metadata-item {\n  border-bottom: var(--jp-border-width) solid var(--jp-border-color2);\n  display: flex;\n  flex-direction: column;\n  margin: 0;\n  padding: 0;\n}\n\n.elyra-metadata-item .elyra-expandableContainer-details-visible {\n  background-color: var(--jp-cell-editor-background);\n  resize: vertical;\n}\n\n.elyra-metadata-item .CodeMirror.cm-s-jupyter {\n  background-color: inherit;\n  border: none;\n  font-family: var(--jp-code-font-family);\n  font-size: var(--jp-code-font-size);\n  line-height: var(--jp-code-line-height);\n}\n\n.elyra-metadata-item .cm-s-jupyter li .cm-string {\n  word-break: normal;\n}\n\n/* MetadataEditor css */\n.elyra-metadataEditor .jp-InputGroup {\n  width: 100%;\n}\n\n.elyra-metadataEditor-formInput.elyra-metadataEditor-secure label {\n  margin-right: 70px;\n}\n\n.elyra-metadataEditor {\n  color: var(--jp-ui-font-color1);\n}\n\n.elyra-form-DropDown-item {\n  width: 100%;\n  display: flex;\n  flex-direction: column;\n  justify-content: left;\n  margin: 0;\n  border-radius: 0;\n}\n\n.elyra-metadataEditor {\n  padding: 20px;\n  display: flex;\n  flex-wrap: wrap;\n  height: 100%;\n  align-content: flex-start;\n  align-items: flex-start;\n  justify-content: flex-start;\n}\n\n.elyra-metadataEditor .elyra-metadataEditor-arrayInput li {\n  padding-left: 0;\n  padding-bottom: 0;\n}\n\n.elyra-metadataEditor\n  .elyra-metadataEditor-arrayInput\n  li:not(.elyra-metadataEditor-arrayItemEditor)\n  .elyra-elyra-metadataHeaderMuiInputBase-formControl {\n  background-color: var(--jp-border-color3);\n}\n\n.elyra-metadataEditor\n  .elyra-metadataEditor-arrayInput\n  .elyra-metadataEditor-editButtons\n  button {\n  padding: 3px;\n}\n\n.elyra-metadataEditor\n  .elyra-metadataEditor-arrayInput\n  .elyra-metadataEditor-addItemButton {\n  background-color: var(--jp-border-color1);\n}\n\n.elyra-metadataEditor .elyra-metadataEditor-arrayItemEditor {\n  display: flex;\n  padding: 6px 0 3px 0;\n}\n\n.elyra-metadataEditor h3 {\n  flex-basis: 100%;\n  margin-bottom: 15px;\n  color: var(--jp-ui-font-color1);\n}\n\n.elyra-metadataEditor .elyra-form-code.jp-CodeMirrorEditor {\n  background-color: var(--jp-cell-editor-background);\n  border: var(--jp-border-width) solid var(--jp-input-border-color);\n  overflow-y: auto;\n  resize: vertical;\n  min-height: 150px;\n  height: 150px;\n  padding-bottom: 10px;\n  cursor: initial;\n  margin-top: 5px;\n}\n\n.elyra-metadataEditor .CodeMirror.cm-s-jupyter {\n  background-color: inherit;\n  height: 100%;\n}\n\n.elyra-metadataEditor .elyra-metadataEditor-code {\n  height: auto;\n  flex-basis: 100%;\n  display: flex;\n  flex-direction: column;\n}\n\n.elyra-metadataEditor-formInput {\n  margin: 10px;\n  flex-basis: 45%;\n}\n\n.elyra-metadata-editor {\n  overflow-y: auto;\n}\n\n.elyra-metadataEditor .elyra-metadataEditor-saveButton {\n  flex-basis: 100%;\n  display: flex;\n}\n\n/* Code Snippet Filter CSS */\n.elyra-searchbar {\n  margin: 0px 8px;\n}\n\n.elyra-filterTools {\n  border-bottom: var(--jp-border-width) solid var(--jp-border-color1);\n}\n\nmark.elyra-search-bolding {\n  background-color: transparent;\n  font-weight: bold;\n  color: var(--jp-ui-font-color0);\n}\n\n.elyra-filter {\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  margin: 10px 10px 0 10px;\n}\n\n.elyra-filter .elyra-filter-btn {\n  align-self: flex-end;\n  padding: 0px;\n  margin-bottom: 5px;\n  border-radius: 5px;\n  border: none;\n  background: none;\n  cursor: pointer;\n}\n\n.elyra-filter .elyra-filter-btn:hover {\n  background-color: var(--jp-layout-color2);\n}\n\n.elyra-filter-btn svg {\n  display: block;\n  width: 30px;\n  height: 22px;\n}\n\n.elyra-filter-arrow-up.idle,\n.elyra-filter-option.idle {\n  display: none;\n}\n\n.elyra-filter-arrow-up {\n  position: absolute;\n  margin-top: 16px;\n  margin-right: 38px;\n  align-self: flex-end;\n  background-color: var(--jp-layout-color0);\n}\n\n.elyra-filter-option {\n  border: var(--jp-border-width) solid var(--jp-border-color1);\n  height: 140px;\n  width: 100%;\n  margin-bottom: 10px;\n  padding-top: 5px;\n  padding-bottom: 5px;\n  overflow: auto;\n}\n\n.elyra-filter-tags {\n  margin: 8px 8px;\n}\n\n.elyra-filter-tag {\n  margin-left: 3px;\n  margin-right: 3px;\n}\n\nbutton.elyra-filter-tag {\n  height: 24px;\n  padding: 0 12px;\n  cursor: pointer;\n  color: var(--jp-ui-font-color2);\n  font-size: var(--jp-ui-font-size1);\n}\n\nbutton.elyra-filter-tag .elyra-filter-tag-label {\n  overflow: hidden;\n  text-overflow: ellipsis;\n  white-space: nowrap;\n}\n\nbutton.elyra-filter-tag span,\nbutton.elyra-filter-tag svg {\n  pointer-events: none;\n}\n\n.elyra-filter-empty {\n  font-size: var(--jp-ui-font-size1);\n}\n\n.elyra-tools {\n  border-bottom: var(--jp-border-width) solid var(--jp-border-color1);\n}\n\n.elyra-editor-tagList {\n  list-style: none;\n  margin-left: -3px;\n  margin-top: 4px;\n}\n\n.elyra-editor-tag {\n  margin-left: 3px;\n  margin-right: 3px;\n  padding: 0 12px;\n  height: 24px;\n}\n\nbutton.elyra-editor-tag {\n  cursor: pointer;\n  color: var(--jp-ui-font-color2);\n  font-size: var(--jp-ui-font-size1);\n}\n\nbutton.elyra-editor-tag.applied-tag {\n  color: var(--jp-ui-font-color1);\n}\n\nbutton.elyra-editor-tag.unapplied-tag {\n  color: var(--jp-ui-font-color2);\n  white-space: nowrap;\n}\n\n.elyra-editor-tag.tag.unapplied-tag input {\n  border: none;\n}\n\n/* Code Snippet Tags in InputDialog */\n.elyra-inputTagList {\n  list-style: none;\n}\n\n.elyra-inputTag {\n  margin-left: 8px;\n  margin-right: 8px;\n}\n\nbutton.elyra-inputTag {\n  cursor: pointer;\n  background: none;\n  border: none;\n  color: var(--jp-ui-font-color2);\n  padding: 0;\n  font-size: var(--jp-ui-font-size1);\n}\n\ninput.elyra-inputTag {\n  font-size: var(--jp-ui-font-size1);\n  background: none;\n  border: none;\n  color: var(--jp-ui-font-color2);\n  font-size: var(--jp-ui-font-size1);\n  width: 80px;\n  height: 15px;\n}\n\n.elyra-tags {\n  margin-top: 8px;\n}\n\n.elyra-no-metadata-msg {\n  padding-left: 8px;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "../metadata-common/style/index.css":
/*!******************************************!*\
  !*** ../metadata-common/style/index.css ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _code_snippet_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../../code-snippet/node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _code_snippet_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_code_snippet_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../../../node_modules/css-loader/dist/cjs.js!./index.css */ "../../node_modules/css-loader/dist/cjs.js!../metadata-common/style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _code_snippet_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ }),

/***/ "../metadata-common/lib/FilterTools.js":
/*!*********************************************!*\
  !*** ../metadata-common/lib/FilterTools.js ***!
  \*********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.FilterTools = void 0;
/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
const ui_components_1 = __webpack_require__(/*! @elyra/ui-components */ "webpack/sharing/consume/default/@elyra/ui-components/@elyra/ui-components");
const ui_components_2 = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const FILTER_OPTION = 'elyra-filter-option';
const FILTER_TAGS = 'elyra-filter-tags';
const FILTER_TAG = 'elyra-filter-tag';
const FILTER_TAG_LABEL = 'elyra-filter-tag-label';
const FILTER_CHECK = 'elyra-filter-check';
const FILTER_TOOLS = 'elyra-filterTools';
const FILTER_SEARCHBAR = 'elyra-searchbar';
const FILTER_SEARCHWRAPPER = 'elyra-searchwrapper';
const FILTER_CLASS = 'elyra-filter';
const FILTER_BUTTON = 'elyra-filter-btn';
const FILTER_EMPTY = 'elyra-filter-empty';
class FilterTools extends react_1.default.Component {
    constructor(props) {
        super(props);
        this.handleSearch = (event) => {
            this.setState({ searchValue: event.target.value }, this.filterMetadata);
        };
        this.state = { selectedTags: [], searchValue: '' };
        this.createFilterBox = this.createFilterBox.bind(this);
        this.renderFilterOption = this.renderFilterOption.bind(this);
        this.renderTags = this.renderTags.bind(this);
        this.renderAppliedTag = this.renderAppliedTag.bind(this);
        this.renderUnappliedTag = this.renderUnappliedTag.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.filterMetadata = this.filterMetadata.bind(this);
    }
    componentDidMount() {
        this.setState({
            selectedTags: [],
            searchValue: ''
        });
    }
    componentDidUpdate(prevProps) {
        if (prevProps !== this.props) {
            this.setState(state => ({
                selectedTags: state.selectedTags
                    .filter(tag => this.props.tags.includes(tag))
                    .sort()
            }));
        }
    }
    createFilterBox() {
        const filterOption = document.querySelector(`#${this.props.schemaspace} .${FILTER_OPTION}`);
        filterOption === null || filterOption === void 0 ? void 0 : filterOption.classList.toggle('idle');
        this.filterMetadata();
    }
    renderTags() {
        if (!this.props.tags.length) {
            return (react_1.default.createElement("div", { className: FILTER_TAGS },
                react_1.default.createElement("p", { className: FILTER_EMPTY }, "No tags defined")));
        }
        return (react_1.default.createElement("div", { className: FILTER_TAGS }, this.props.tags.sort().map((tag, index) => {
            if (this.state.selectedTags.includes(tag)) {
                return this.renderAppliedTag(tag, index.toString());
            }
            else {
                return this.renderUnappliedTag(tag, index.toString());
            }
        })));
    }
    renderAppliedTag(tag, index) {
        return (react_1.default.createElement("button", { className: `${FILTER_TAG} tag applied-tag`, id: 'filter' + '-' + tag + '-' + index, key: 'filter' + '-' + tag + '-' + index, title: tag, onClick: this.handleClick },
            react_1.default.createElement("span", { className: FILTER_TAG_LABEL }, tag),
            react_1.default.createElement(ui_components_2.checkIcon.react, { className: FILTER_CHECK, tag: "span", elementPosition: "center", height: "18px", width: "18px", marginLeft: "5px", marginRight: "-3px" })));
    }
    renderUnappliedTag(tag, index) {
        return (react_1.default.createElement("button", { className: `${FILTER_TAG} tag unapplied-tag`, id: 'filter' + '-' + tag + '-' + index, key: 'filter' + '-' + tag + '-' + index, title: tag, onClick: this.handleClick },
            react_1.default.createElement("span", { className: FILTER_TAG_LABEL }, tag)));
    }
    handleClick(event) {
        var _a;
        const target = event.target;
        const clickedTag = (_a = target.textContent) !== null && _a !== void 0 ? _a : '';
        this.setState(state => ({
            selectedTags: this.updateTagsCss(target, state.selectedTags, clickedTag)
        }), this.filterMetadata);
    }
    updateTagsCss(target, currentTags, clickedTag) {
        if (target.classList.contains('unapplied-tag')) {
            target.classList.replace('unapplied-tag', 'applied-tag');
            currentTags.splice(-1, 0, clickedTag);
        }
        else if (target.classList.contains('applied-tag')) {
            target.classList.replace('applied-tag', 'unapplied-tag');
            const idx = currentTags.indexOf(clickedTag);
            currentTags.splice(idx, 1);
        }
        return currentTags.sort();
    }
    filterMetadata() {
        var _a;
        const isTagFilterOpen = (_a = document
            .querySelector(`#${this.props.schemaspace} .${FILTER_OPTION}`)) === null || _a === void 0 ? void 0 : _a.classList.contains('idle');
        this.props.onFilter(this.state.searchValue, isTagFilterOpen ? [] : this.state.selectedTags);
    }
    renderFilterOption() {
        return react_1.default.createElement("div", { className: `${FILTER_OPTION} idle` }, this.renderTags());
    }
    render() {
        return (react_1.default.createElement("div", { className: FILTER_TOOLS },
            react_1.default.createElement("div", { className: FILTER_SEARCHBAR },
                react_1.default.createElement(ui_components_2.InputGroup, { className: FILTER_SEARCHWRAPPER, type: "text", placeholder: "Search...", onChange: this.handleSearch, rightIcon: "ui-components:search", value: this.state.searchValue })),
            this.props.omitTags ? (react_1.default.createElement("div", { style: { height: '4px' } })) : (react_1.default.createElement("div", { className: FILTER_CLASS, id: this.props.schemaspace },
                react_1.default.createElement("button", { title: "Filter by tag", className: FILTER_BUTTON, onClick: this.createFilterBox },
                    react_1.default.createElement(ui_components_1.tagIcon.react, null)),
                this.renderFilterOption()))));
    }
}
exports.FilterTools = FilterTools;
//# sourceMappingURL=FilterTools.js.map

/***/ }),

/***/ "../metadata-common/lib/MetadataCommonService.js":
/*!*******************************************************!*\
  !*** ../metadata-common/lib/MetadataCommonService.js ***!
  \*******************************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MetadataCommonService = void 0;
const services_1 = __webpack_require__(/*! @elyra/services */ "webpack/sharing/consume/default/@elyra/services/@elyra/services");
class MetadataCommonService {
    /**
     * Duplicates an existing metadata instance, using
     * '<original-display-name>-Copy<unique-number>' as new display name.
     *
     * @param schemaSpace: schemaspace in which metadataInstance is defined
     * @param metadataInstance: metadata instance to be duplicated
     * @param existingInstances: list of existing metadata instances in schemaspace
     *
     * @returns A promise
     */
    static duplicateMetadataInstance(schemaSpace, metadataInstance, existingInstances) {
        // iterate through the list of currently defined
        // instance names and find the next available one
        // using '<source-instance-name>-Copy<N>'
        let base_name = metadataInstance.display_name;
        const match = metadataInstance.display_name.match(/-Copy\d+$/);
        if (match !== null) {
            base_name = base_name.replace(/-Copy\d+$/, '');
        }
        let count = 1;
        while (existingInstances.find(element => element.display_name === `${base_name}-Copy${count}`) !== undefined) {
            count += 1;
        }
        // Create a duplicate metadata instance using the derived name
        const duplicated_metadata = JSON.parse(JSON.stringify(metadataInstance));
        duplicated_metadata.display_name = `${base_name}-Copy${count}`;
        delete duplicated_metadata.name;
        return services_1.MetadataService.postMetadata(schemaSpace, JSON.stringify(duplicated_metadata));
    }
}
exports.MetadataCommonService = MetadataCommonService;
//# sourceMappingURL=MetadataCommonService.js.map

/***/ }),

/***/ "../metadata-common/lib/MetadataEditor.js":
/*!************************************************!*\
  !*** ../metadata-common/lib/MetadataEditor.js ***!
  \************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MetadataEditor = void 0;
const services_1 = __webpack_require__(/*! @elyra/services */ "webpack/sharing/consume/default/@elyra/services/@elyra/services");
const ui_components_1 = __webpack_require__(/*! @elyra/ui-components */ "webpack/sharing/consume/default/@elyra/ui-components/@elyra/ui-components");
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const codeeditor_1 = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
const algorithm_1 = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
const core_1 = __webpack_require__(/*! @material-ui/core */ "../../node_modules/@material-ui/core/esm/index.js");
const React = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const MetadataEditorTags_1 = __webpack_require__(/*! ./MetadataEditorTags */ "../metadata-common/lib/MetadataEditorTags.js");
const ELYRA_METADATA_EDITOR_CLASS = 'elyra-metadataEditor';
const DIRTY_CLASS = 'jp-mod-dirty';
const CodeBlock = ({ editorServices, defaultValue, language, onChange, defaultError, label, required }) => {
    const [error, setError] = React.useState(defaultError);
    const codeBlockRef = React.useRef(null);
    const editorRef = React.useRef();
    // `editorServices` should never change so make it a ref.
    const servicesRef = React.useRef(editorServices);
    // This is necessary to rerender with error when clicking the save button.
    React.useEffect(() => {
        setError(defaultError);
    }, [defaultError]);
    React.useEffect(() => {
        var _a;
        const handleChange = (args) => {
            setError(required && args.text === '');
            onChange === null || onChange === void 0 ? void 0 : onChange(args.text.split('\n'));
        };
        if (codeBlockRef.current !== null) {
            editorRef.current = servicesRef.current.factoryService.newInlineEditor({
                host: codeBlockRef.current,
                model: new codeeditor_1.CodeEditor.Model({
                    value: defaultValue,
                    mimeType: servicesRef.current.mimeTypeService.getMimeTypeByLanguage({
                        name: language,
                        codemirror_mode: language
                    })
                })
            });
            (_a = editorRef.current) === null || _a === void 0 ? void 0 : _a.model.value.changed.connect(handleChange);
        }
        return () => {
            var _a;
            (_a = editorRef.current) === null || _a === void 0 ? void 0 : _a.model.value.changed.disconnect(handleChange);
        };
        // NOTE: The parent component is unstable so props change frequently causing
        // new editors to be created unnecessarily. This effect on mount should only
        // run on mount. Keep in mind this could have side effects, for example if
        // the `onChange` callback actually does change.
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);
    React.useEffect(() => {
        if (editorRef.current !== undefined) {
            editorRef.current.model.mimeType = servicesRef.current.mimeTypeService.getMimeTypeByLanguage({
                name: language,
                codemirror_mode: language
            });
        }
    }, [language]);
    return (React.createElement("div", null,
        React.createElement(core_1.InputLabel, { error: error, required: required }, label),
        React.createElement("div", { ref: codeBlockRef, className: "elyra-form-code" }),
        error === true && (React.createElement(core_1.FormHelperText, { error: true }, "This field is required."))));
};
const SaveButton = core_1.styled(core_1.Button)({
    borderColor: 'var(--jp-border-color0)',
    color: 'var(--jp-ui-font-color1)',
    '&:hover': {
        borderColor: ' var(--jp-ui-font-color1)'
    }
});
/**
 * Metadata editor widget
 */
class MetadataEditor extends apputils_1.ReactWidget {
    constructor(props) {
        super();
        this.schema = {};
        this.schemaPropertiesByCategory = {};
        this.allMetadata = [];
        this.metadata = {};
        this.handleDropdownChange = (schemaField, value) => {
            this.handleDirtyState(true);
            this.metadata[schemaField] = value;
            if (schemaField === 'language') {
                this.language = value;
            }
            this.update();
        };
        this.editorServices = props.editorServices;
        this.status = props.status;
        this.clearDirty = null;
        this.schemaspace = props.schemaspace;
        this.schemaName = props.schema;
        this.allTags = [];
        this.onSave = props.onSave;
        this.name = props.name;
        this.code = props.code;
        this.themeManager = props.themeManager;
        this.widgetClass = `elyra-metadataEditor-${this.name ? this.name : 'new'}`;
        this.addClass(this.widgetClass);
        this.handleTextInputChange = this.handleTextInputChange.bind(this);
        this.handleArrayInputChange = this.handleArrayInputChange.bind(this);
        this.handleBooleanInputChange = this.handleBooleanInputChange.bind(this);
        this.handleChangeOnTag = this.handleChangeOnTag.bind(this);
        this.handleDropdownChange = this.handleDropdownChange.bind(this);
        this.renderField = this.renderField.bind(this);
        this.invalidForm = false;
        this.showSecure = {};
        this.initializeMetadata();
    }
    initializeMetadata() {
        var _a, _b;
        return __awaiter(this, void 0, void 0, function* () {
            try {
                const schemas = yield services_1.MetadataService.getSchema(this.schemaspace);
                for (const schema of schemas) {
                    if (this.schemaName === schema.name) {
                        this.schema = schema.properties.metadata.properties;
                        this.referenceURL = (_a = schema.uihints) === null || _a === void 0 ? void 0 : _a.reference_url;
                        this.schemaDisplayName = schema.title;
                        this.requiredFields = schema.properties.metadata.required;
                        if (!this.name) {
                            this.title.label = `New ${this.schemaDisplayName}`;
                        }
                        // Find categories of all schema properties
                        this.schemaPropertiesByCategory = { _noCategory: [] };
                        for (const schemaProperty in this.schema) {
                            const category = this.schema[schemaProperty].uihints &&
                                this.schema[schemaProperty].uihints.category;
                            if (!category) {
                                this.schemaPropertiesByCategory['_noCategory'].push(schemaProperty);
                            }
                            else if (this.schemaPropertiesByCategory[category]) {
                                this.schemaPropertiesByCategory[category].push(schemaProperty);
                            }
                            else {
                                this.schemaPropertiesByCategory[category] = [schemaProperty];
                            }
                        }
                        break;
                    }
                }
            }
            catch (error) {
                ui_components_1.RequestErrors.serverError(error);
            }
            try {
                this.allMetadata = yield services_1.MetadataService.getMetadata(this.schemaspace);
            }
            catch (error) {
                ui_components_1.RequestErrors.serverError(error);
            }
            if (this.name) {
                for (const metadata of this.allMetadata) {
                    if (metadata.metadata.tags) {
                        for (const tag of metadata.metadata.tags) {
                            if (!this.allTags.includes(tag)) {
                                this.allTags.push(tag);
                            }
                        }
                    }
                    else {
                        metadata.metadata.tags = [];
                    }
                    if (this.name === metadata.name) {
                        this.metadata = metadata['metadata'];
                        this.displayName = metadata['display_name'];
                        this.title.label = (_b = this.displayName) !== null && _b !== void 0 ? _b : '';
                    }
                }
            }
            else {
                this.displayName = '';
            }
            this.update();
        });
    }
    isValueEmpty(schemaValue) {
        return (schemaValue === undefined ||
            schemaValue === null ||
            schemaValue === '' ||
            (Array.isArray(schemaValue) && schemaValue.length === 0) ||
            (Array.isArray(schemaValue) &&
                schemaValue.length === 1 &&
                schemaValue[0] === '') ||
            schemaValue === '(No selection)');
    }
    /**
     * Checks that all required fields have a value before submitting the form.
     * Returns false if the form is valid. Sets any invalid fields' intent to danger
     * so that the form will highlight the input(s) causing issues in red.
     */
    hasInvalidFields() {
        var _a;
        this.invalidForm = false;
        if (this.displayName === null || this.displayName === '') {
            this.invalidForm = true;
        }
        for (const schemaField in this.schema) {
            const value = this.metadata[schemaField] || this.schema[schemaField].default;
            if (((_a = this.requiredFields) === null || _a === void 0 ? void 0 : _a.includes(schemaField)) &&
                this.isValueEmpty(value)) {
                this.invalidForm = true;
                this.schema[schemaField].uihints.error = true;
            }
            else {
                this.schema[schemaField].uihints.error = false;
            }
        }
        return this.invalidForm;
    }
    onCloseRequest(msg) {
        if (this.dirty) {
            apputils_1.showDialog({
                title: 'Close without saving?',
                body: (React.createElement("p", null,
                    ' ',
                    `"${this.displayName}" has unsaved changes, close without saving?`,
                    ' ')),
                buttons: [apputils_1.Dialog.cancelButton(), apputils_1.Dialog.okButton()]
            }).then((response) => {
                if (response.button.accept) {
                    this.dispose();
                    super.onCloseRequest(msg);
                }
            });
        }
        else {
            this.dispose();
            super.onCloseRequest(msg);
        }
    }
    saveMetadata() {
        const newMetadata = {
            schema_name: this.schemaName,
            display_name: this.displayName,
            metadata: this.metadata
        };
        if (this.hasInvalidFields()) {
            this.update();
            return;
        }
        if (!this.name) {
            services_1.MetadataService.postMetadata(this.schemaspace, JSON.stringify(newMetadata))
                .then((response) => {
                this.handleDirtyState(false);
                this.onSave();
                this.close();
            })
                .catch(error => ui_components_1.RequestErrors.serverError(error));
        }
        else {
            services_1.MetadataService.putMetadata(this.schemaspace, this.name, JSON.stringify(newMetadata))
                .then((response) => {
                this.handleDirtyState(false);
                this.onSave();
                this.close();
            })
                .catch(error => ui_components_1.RequestErrors.serverError(error));
        }
    }
    handleTextInputChange(schemaField, value) {
        var _a;
        this.handleDirtyState(true);
        // Special case because all metadata has a display name
        if (schemaField === 'display_name') {
            this.displayName = value;
        }
        else if (!value && !((_a = this.requiredFields) === null || _a === void 0 ? void 0 : _a.includes(schemaField))) {
            delete this.metadata[schemaField];
        }
        else {
            this.metadata[schemaField] = value;
        }
    }
    handleArrayInputChange(schemaField, values) {
        this.handleDirtyState(true);
        this.metadata[schemaField] = values;
    }
    handleBooleanInputChange(schemaField, value) {
        this.handleDirtyState(true);
        this.metadata[schemaField] = value;
    }
    handleDirtyState(dirty) {
        this.dirty = dirty;
        if (this.dirty && !this.clearDirty) {
            this.clearDirty = this.status.setDirty();
        }
        else if (!this.dirty && this.clearDirty) {
            this.clearDirty.dispose();
            this.clearDirty = null;
        }
        if (this.dirty && !this.title.className.includes(DIRTY_CLASS)) {
            this.title.className += DIRTY_CLASS;
        }
        else if (!this.dirty) {
            this.title.className = this.title.className.replace(DIRTY_CLASS, '');
        }
    }
    getDefaultChoices(fieldName) {
        let defaultChoices = this.schema[fieldName].enum;
        if (!defaultChoices) {
            defaultChoices =
                Object.assign([], this.schema[fieldName].uihints.default_choices) || [];
            for (const otherMetadata of this.allMetadata) {
                if (
                // Don't include the current metadata
                otherMetadata !== this.metadata &&
                    // Don't add if otherMetadata hasn't defined field
                    otherMetadata.metadata[fieldName] &&
                    !algorithm_1.find(defaultChoices, (choice) => {
                        return (choice.toLowerCase() ===
                            otherMetadata.metadata[fieldName].toLowerCase());
                    })) {
                    defaultChoices.push(otherMetadata.metadata[fieldName]);
                }
            }
        }
        return defaultChoices;
    }
    setFormFocus() {
        var _a;
        const isFocused = (_a = document
            .querySelector(`.${this.widgetClass}`)) === null || _a === void 0 ? void 0 : _a.contains(document.activeElement);
        if (!isFocused) {
            const input = document.querySelector(`.${this.widgetClass} .elyra-metadataEditor-form-display_name input`);
            if (input) {
                input.focus();
                input.setSelectionRange(input.value.length, input.value.length);
            }
        }
    }
    onAfterShow(msg) {
        this.setFormFocus();
    }
    onUpdateRequest(msg) {
        super.onUpdateRequest(msg);
        this.setFormFocus();
    }
    renderField(fieldName) {
        var _a, _b, _c, _d;
        let uihints = this.schema[fieldName].uihints;
        const required = this.requiredFields && this.requiredFields.includes(fieldName);
        const defaultValue = this.schema[fieldName].default || '';
        if (uihints === undefined) {
            uihints = {};
            this.schema[fieldName].uihints = uihints;
        }
        if (uihints.hidden) {
            return React.createElement("div", null);
        }
        if (uihints.field_type === 'textinput' ||
            uihints.field_type === undefined) {
            return (React.createElement(ui_components_1.TextInput, { label: this.schema[fieldName].title, description: this.schema[fieldName].description, key: `${fieldName}TextInput`, fieldName: fieldName, defaultValue: this.metadata[fieldName] || defaultValue, required: required, secure: uihints.secure, defaultError: uihints.error, placeholder: uihints.placeholder, onChange: (value) => {
                    this.handleTextInputChange(fieldName, value);
                } }));
        }
        else if (uihints.field_type === 'dropdown') {
            return (React.createElement(ui_components_1.DropDown, { label: this.schema[fieldName].title, key: `${fieldName}DropDown`, description: this.schema[fieldName].description, required: required, defaultError: uihints.error, placeholder: uihints.placeholder, defaultValue: this.schema[fieldName].default, readonly: this.schema[fieldName].enum !== undefined, initialValue: this.metadata[fieldName], options: this.getDefaultChoices(fieldName), onChange: (value) => {
                    this.handleDropdownChange(fieldName, value);
                } }));
        }
        else if (uihints.field_type === 'code') {
            let initialCodeValue = '';
            if (this.name) {
                initialCodeValue = this.metadata.code.join('\n');
            }
            else if (this.code) {
                this.metadata.code = this.code;
                initialCodeValue = this.code.join('\n');
            }
            return (React.createElement("div", { className: 'elyra-metadataEditor-formInput elyra-metadataEditor-code', key: `${fieldName}CodeEditor` }, this.editorServices !== null && (React.createElement(CodeBlock, { editorServices: this.editorServices, language: (_a = this.language) !== null && _a !== void 0 ? _a : this.metadata.language, defaultValue: initialCodeValue, onChange: (value) => {
                    this.metadata.code = value;
                    this.handleDirtyState(true);
                    return;
                }, defaultError: uihints.error, required: required !== null && required !== void 0 ? required : false, label: this.schema[fieldName].title }))));
        }
        else if (uihints.field_type === 'tags') {
            return (React.createElement("div", { className: "elyra-metadataEditor-formInput", key: `${fieldName}TagList` },
                React.createElement(core_1.InputLabel, null, " Tags "),
                React.createElement(MetadataEditorTags_1.MetadataEditorTags, { selectedTags: this.metadata.tags, tags: this.allTags, handleChange: this.handleChangeOnTag })));
        }
        else if (uihints.field_type === 'array') {
            return (React.createElement(ui_components_1.ArrayInput, { label: this.schema[fieldName].title, description: this.schema[fieldName].description, key: `${fieldName}TextInput`, fieldName: fieldName, defaultValues: (_c = (_b = this.metadata[fieldName]) !== null && _b !== void 0 ? _b : this.schema[fieldName].default) !== null && _c !== void 0 ? _c : [], required: required, defaultError: uihints.error, placeholder: uihints.placeholder, onChange: (values) => {
                    this.handleArrayInputChange(fieldName, values);
                } }));
        }
        else if (uihints.field_type === 'boolean') {
            return (React.createElement(ui_components_1.BooleanInput, { label: this.schema[fieldName].title, key: `${fieldName}BooleanInput`, defaultValue: (_d = this.metadata[fieldName]) !== null && _d !== void 0 ? _d : this.schema[fieldName].default, onChange: (value) => {
                    this.handleBooleanInputChange(fieldName, value);
                } }));
        }
        else {
            return null;
        }
    }
    handleChangeOnTag(selectedTags, allTags) {
        this.handleDirtyState(true);
        this.metadata.tags = selectedTags;
        this.allTags = allTags;
    }
    render() {
        var _a;
        const inputElements = [];
        for (const category in this.schemaPropertiesByCategory) {
            if (category !== '_noCategory') {
                inputElements.push(React.createElement("h4", { style: { flexBasis: '100%', padding: '10px' }, key: `${category}Category` }, category));
            }
            for (const schemaProperty of this.schemaPropertiesByCategory[category]) {
                inputElements.push(this.renderField(schemaProperty));
            }
        }
        let headerText = `Edit "${this.displayName}"`;
        if (!this.name) {
            headerText = `Add new ${this.schemaDisplayName} ${(_a = this.titleContext) !== null && _a !== void 0 ? _a : ''}`;
        }
        const error = this.displayName === '' && this.invalidForm;
        const onKeyPress = (event) => {
            const targetElement = event.nativeEvent.target;
            if (event.key === 'Enter' && (targetElement === null || targetElement === void 0 ? void 0 : targetElement.tagName) !== 'TEXTAREA') {
                this.saveMetadata();
            }
        };
        return (React.createElement(ui_components_1.ThemeProvider, { themeManager: this.themeManager },
            React.createElement("div", { onKeyPress: onKeyPress, className: ELYRA_METADATA_EDITOR_CLASS },
                React.createElement("h3", null,
                    " ",
                    headerText,
                    " "),
                React.createElement("p", { style: { width: '100%', marginBottom: '10px' } },
                    "All fields marked with an asterisk are required.\u00A0",
                    this.referenceURL ? (React.createElement(core_1.Link, { href: this.referenceURL, target: "_blank", rel: "noreferrer noopener" }, "[Learn more ...]")) : null),
                this.displayName !== undefined ? (React.createElement(ui_components_1.TextInput, { label: "Name", key: "displayNameTextInput", fieldName: "display_name", defaultValue: this.displayName, required: true, secure: false, defaultError: error, onChange: (value) => {
                        this.handleTextInputChange('display_name', value);
                    } })) : null,
                inputElements,
                React.createElement("div", { className: 'elyra-metadataEditor-formInput elyra-metadataEditor-saveButton', key: 'SaveButton' },
                    React.createElement(SaveButton, { variant: "outlined", color: "primary", onClick: () => {
                            this.saveMetadata();
                        } }, "Save & Close")))));
    }
}
exports.MetadataEditor = MetadataEditor;
//# sourceMappingURL=MetadataEditor.js.map

/***/ }),

/***/ "../metadata-common/lib/MetadataEditorTags.js":
/*!****************************************************!*\
  !*** ../metadata-common/lib/MetadataEditorTags.js ***!
  \****************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MetadataEditorTags = void 0;
/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const ui_components_1 = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
/**
 * CSS STYLING
 */
const METADATA_EDITOR_TAG = 'elyra-editor-tag';
const METADATA_EDITOR_TAG_PLUS_ICON = 'elyra-editor-tag-plusIcon';
const METADATA_EDITOR_TAG_LIST = 'elyra-editor-tagList';
const METADATA_EDITOR_INPUT_TAG = 'elyra-inputTag';
class MetadataEditorTags extends react_1.default.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedTags: [],
            tags: [],
            addingNewTag: false
        };
        this.renderTags = this.renderTags.bind(this);
        this.handleClick = this.handleClick.bind(this);
    }
    componentDidMount() {
        this.setState({
            selectedTags: this.props.selectedTags ? this.props.selectedTags : [],
            tags: this.props.tags ? this.props.tags.sort() : [],
            addingNewTag: false
        });
    }
    componentDidUpdate(prevProps) {
        if (prevProps !== this.props) {
            this.setState({
                selectedTags: this.props.selectedTags ? this.props.selectedTags : [],
                tags: this.props.tags ? this.props.tags : []
            });
        }
    }
    handleClick(event) {
        const target = event.target;
        const clickedTag = target.innerText;
        this.setState(state => ({
            selectedTags: this.updateTagsCss(target, state.selectedTags ? state.selectedTags : [], clickedTag)
        }), this.handleOnChange);
    }
    handleOnChange() {
        this.props.handleChange(this.state.selectedTags, this.state.tags);
    }
    updateTagsCss(target, tags, clickedTag) {
        const currentTags = tags.slice();
        if (target.classList.contains('unapplied-tag')) {
            target.classList.replace('unapplied-tag', 'applied-tag');
            currentTags.splice(-1, 0, clickedTag);
        }
        else if (target.classList.contains('applied-tag')) {
            target.classList.replace('applied-tag', 'unapplied-tag');
            const idx = currentTags.indexOf(clickedTag);
            currentTags.splice(idx, 1);
        }
        return currentTags;
    }
    addTagOnClick(event) {
        this.setState({ addingNewTag: true });
        const inputElement = event.target;
        if (inputElement.value === 'Add Tag') {
            inputElement.value = '';
            inputElement.style.width = '62px';
            inputElement.style.minWidth = '62px';
        }
    }
    addTagOnKeyDown(event) {
        return __awaiter(this, void 0, void 0, function* () {
            const inputElement = event.target;
            if (inputElement.value !== '' && event.keyCode === 13) {
                if (this.state.tags.includes(inputElement.value)) {
                    event.preventDefault();
                    yield apputils_1.showDialog({
                        title: 'A tag with this label already exists.',
                        buttons: [apputils_1.Dialog.okButton()]
                    });
                    return;
                }
                const newTag = inputElement.value;
                // update state all tag and selected tag
                this.setState(state => ({
                    selectedTags: [...state.selectedTags, newTag],
                    tags: [...state.tags, newTag],
                    addingNewTag: false
                }), this.handleOnChange);
            }
        });
    }
    addTagOnBlur(event) {
        const inputElement = event.target;
        inputElement.value = 'Add Tag';
        inputElement.style.width = '50px';
        inputElement.style.minWidth = '50px';
        inputElement.blur();
        this.setState({ addingNewTag: false });
    }
    renderTags() {
        const hasTags = this.state.tags;
        const inputBox = this.state.addingNewTag === true ? (react_1.default.createElement("ul", { className: `${METADATA_EDITOR_TAG} tag unapplied-tag`, key: 'editor-new-tag' },
            react_1.default.createElement("input", { className: `${METADATA_EDITOR_INPUT_TAG}`, onClick: (event) => this.addTagOnClick(event), onKeyDown: (event) => __awaiter(this, void 0, void 0, function* () {
                    yield this.addTagOnKeyDown(event);
                }), onBlur: (event) => this.addTagOnBlur(event), autoFocus: true }))) : (react_1.default.createElement("button", { onClick: () => this.setState({ addingNewTag: true }), className: `${METADATA_EDITOR_TAG} tag unapplied-tag` },
            "Add Tag",
            react_1.default.createElement(ui_components_1.addIcon.react, { tag: "span", className: METADATA_EDITOR_TAG_PLUS_ICON, elementPosition: "center", height: "16px", width: "16px", marginLeft: "2px" })));
        return (react_1.default.createElement("li", { className: METADATA_EDITOR_TAG_LIST },
            hasTags
                ? this.state.tags.map((tag, index) => (() => {
                    if (!this.state.selectedTags) {
                        return (react_1.default.createElement("button", { onClick: this.handleClick, className: `${METADATA_EDITOR_TAG} tag unapplied-tag`, id: 'editor' + '-' + tag + '-' + index, key: 'editor' + '-' + tag + '-' + index }, tag));
                    }
                    if (this.state.selectedTags.includes(tag)) {
                        return (react_1.default.createElement("button", { onClick: this.handleClick, className: `${METADATA_EDITOR_TAG} tag applied-tag`, id: 'editor' + '-' + tag + '-' + index, key: 'editor' + '-' + tag + '-' + index },
                            tag,
                            react_1.default.createElement(ui_components_1.checkIcon.react, { tag: "span", elementPosition: "center", height: "18px", width: "18px", marginLeft: "5px", marginRight: "-3px" })));
                    }
                    else {
                        return (react_1.default.createElement("button", { onClick: this.handleClick, className: `${METADATA_EDITOR_TAG} tag unapplied-tag`, id: 'editor' + '-' + tag + '-' + index, key: 'editor' + '-' + tag + '-' + index }, tag));
                    }
                })())
                : null,
            inputBox));
    }
    render() {
        return react_1.default.createElement("div", null, this.renderTags());
    }
}
exports.MetadataEditorTags = MetadataEditorTags;
//# sourceMappingURL=MetadataEditorTags.js.map

/***/ }),

/***/ "../metadata-common/lib/MetadataHeaderButtons.js":
/*!*******************************************************!*\
  !*** ../metadata-common/lib/MetadataHeaderButtons.js ***!
  \*******************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MetadataHeaderButtons = exports.METADATA_HEADER_POPPER_CLASS = exports.METADATA_HEADER_BUTTON_CLASS = void 0;
const ui_components_1 = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
const core_1 = __webpack_require__(/*! @material-ui/core */ "../../node_modules/@material-ui/core/esm/index.js");
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
exports.METADATA_HEADER_BUTTON_CLASS = 'elyra-metadataHeader-button';
exports.METADATA_HEADER_POPPER_CLASS = 'elyra-metadataHeader-popper';
const StyledButton = core_1.styled(core_1.Button)({
    minWidth: 'auto'
});
const MetadataHeaderButtons = (props) => {
    var _a, _b, _c;
    const [open, setOpen] = react_1.default.useState(false);
    const anchorRef = react_1.default.useRef(null);
    let singleSchema = false;
    if (((_a = props.schemas) === null || _a === void 0 ? void 0 : _a.length) === 1) {
        singleSchema = true;
    }
    const handleToggle = () => {
        setOpen((prevOpen) => !prevOpen);
    };
    const sortedSchema = (_b = props.schemas) === null || _b === void 0 ? void 0 : _b.sort((a, b) => a.title.localeCompare(b.title));
    const handleClose = (event) => {
        if (anchorRef.current &&
            anchorRef.current.contains(event.target)) {
            return;
        }
        setOpen(false);
    };
    return (react_1.default.createElement(core_1.Box, null,
        react_1.default.createElement(core_1.ButtonGroup, { ref: anchorRef, variant: "text" },
            react_1.default.createElement(StyledButton, { size: "small", className: exports.METADATA_HEADER_BUTTON_CLASS, onClick: () => {
                    props.refreshMetadata();
                    setOpen(false);
                }, title: (_c = props.refreshButtonTooltip) !== null && _c !== void 0 ? _c : 'Refresh list' },
                react_1.default.createElement(ui_components_1.refreshIcon.react, { tag: "span", elementPosition: "center", width: "16px" })),
            react_1.default.createElement(StyledButton, { size: "small", className: exports.METADATA_HEADER_BUTTON_CLASS, onClick: singleSchema
                    ? () => { var _a; return props.addMetadata((_a = props.schemas) === null || _a === void 0 ? void 0 : _a[0].name); }
                    : handleToggle, title: `Create new ${props.titleContext}` },
                react_1.default.createElement(ui_components_1.addIcon.react, { tag: "span", elementPosition: "center", width: "16px" }))),
        react_1.default.createElement(core_1.Popper, { className: exports.METADATA_HEADER_POPPER_CLASS, open: open, anchorEl: anchorRef.current, placement: "bottom-start" },
            react_1.default.createElement(core_1.Paper, null,
                react_1.default.createElement(core_1.ClickAwayListener, { onClickAway: handleClose },
                    react_1.default.createElement(core_1.MenuList, { id: "split-button-menu" }, sortedSchema === null || sortedSchema === void 0 ? void 0 : sortedSchema.map((schema) => (react_1.default.createElement(core_1.MenuItem, { key: schema.title, title: `New ${schema.title} ${props.appendToTitle ? props.titleContext : ''}`, onClick: (event) => {
                            props.addMetadata(schema.name, props.titleContext);
                            handleClose(event);
                        } }, `New ${schema.title} ${props.appendToTitle ? props.titleContext : ''}`)))))))));
};
exports.MetadataHeaderButtons = MetadataHeaderButtons;
//# sourceMappingURL=MetadataHeaderButtons.js.map

/***/ }),

/***/ "../metadata-common/lib/MetadataWidget.js":
/*!************************************************!*\
  !*** ../metadata-common/lib/MetadataWidget.js ***!
  \************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MetadataWidget = exports.MetadataDisplay = exports.METADATA_ITEM = exports.METADATA_HEADER_CLASS = exports.METADATA_CLASS = void 0;
const services_1 = __webpack_require__(/*! @elyra/services */ "webpack/sharing/consume/default/@elyra/services/@elyra/services");
const ui_components_1 = __webpack_require__(/*! @elyra/ui-components */ "webpack/sharing/consume/default/@elyra/ui-components/@elyra/ui-components");
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const ui_components_2 = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
const signaling_1 = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const FilterTools_1 = __webpack_require__(/*! ./FilterTools */ "../metadata-common/lib/FilterTools.js");
const MetadataCommonService_1 = __webpack_require__(/*! ./MetadataCommonService */ "../metadata-common/lib/MetadataCommonService.js");
const MetadataHeaderButtons_1 = __webpack_require__(/*! ./MetadataHeaderButtons */ "../metadata-common/lib/MetadataHeaderButtons.js");
/**
 * The CSS class added to metadata widgets.
 */
exports.METADATA_CLASS = 'elyra-metadata';
exports.METADATA_HEADER_CLASS = 'elyra-metadataHeader';
exports.METADATA_ITEM = 'elyra-metadata-item';
const METADATA_JSON_CLASS = 'jp-RenderedJSON CodeMirror cm-s-jupyter';
const commands = {
    OPEN_METADATA_EDITOR: 'elyra-metadata-editor:open'
};
/**
 * A React Component for displaying a list of metadata
 */
class MetadataDisplay extends react_1.default.Component {
    constructor(props) {
        super(props);
        this.deleteMetadata = (metadata) => {
            return apputils_1.showDialog({
                title: `Delete ${this.props.labelName ? this.props.labelName(metadata) : ''} ${this.props.titleContext || ''} '${metadata.display_name}'?`,
                buttons: [apputils_1.Dialog.cancelButton(), apputils_1.Dialog.okButton()]
            }).then((result) => {
                // Do nothing if the cancel button is pressed
                if (result.button.accept) {
                    services_1.MetadataService.deleteMetadata(this.props.schemaspace, metadata.name).catch(error => ui_components_1.RequestErrors.serverError(error));
                }
            });
        };
        // Render display of metadata list
        this.renderMetadata = (metadata) => {
            return (react_1.default.createElement("div", { key: metadata.name, className: exports.METADATA_ITEM, style: this.state.metadata.includes(metadata) ? {} : { display: 'none' } },
                react_1.default.createElement(ui_components_1.ExpandableComponent, { displayName: metadata.display_name, tooltip: metadata.metadata.description, actionButtons: this.actionButtons(metadata) },
                    react_1.default.createElement("div", { id: metadata.name }, this.renderExpandableContent(metadata)))));
        };
        this.filteredMetadata = (searchValue, filterTags) => {
            // filter with search
            let filteredMetadata = this.props.metadata.filter((metadata, index, array) => {
                return (metadata.name.toLowerCase().includes(searchValue.toLowerCase()) ||
                    metadata.display_name
                        .toLowerCase()
                        .includes(searchValue.toLowerCase()));
            });
            // filter with tags
            if (filterTags.length !== 0) {
                filteredMetadata = filteredMetadata.filter(metadata => {
                    return filterTags.some(tag => {
                        if (metadata.metadata.tags) {
                            return metadata.metadata.tags.includes(tag);
                        }
                        return false;
                    });
                });
            }
            this.setState({
                metadata: filteredMetadata,
                searchValue: searchValue,
                filterTags: filterTags
            });
        };
        this.state = {
            metadata: props.metadata,
            searchValue: '',
            filterTags: [],
            matchesSearch: this.matchesSearch.bind(this),
            matchesTags: this.matchesTags.bind(this)
        };
    }
    actionButtons(metadata) {
        return [
            {
                title: 'Edit',
                icon: ui_components_2.editIcon,
                onClick: () => {
                    this.props.openMetadataEditor({
                        onSave: this.props.updateMetadata,
                        schemaspace: this.props.schemaspace,
                        schema: metadata.schema_name,
                        name: metadata.name
                    });
                }
            },
            {
                title: 'Duplicate',
                icon: ui_components_2.copyIcon,
                onClick: () => {
                    MetadataCommonService_1.MetadataCommonService.duplicateMetadataInstance(this.props.schemaspace, metadata, this.props.metadata)
                        .then((response) => {
                        this.props.updateMetadata();
                    })
                        .catch(error => ui_components_1.RequestErrors.serverError(error));
                }
            },
            {
                title: 'Delete',
                icon: ui_components_1.trashIcon,
                onClick: () => {
                    this.deleteMetadata(metadata).then((response) => {
                        this.props.updateMetadata();
                    });
                }
            }
        ];
    }
    /**
     * Classes that extend MetadataWidget should override this
     */
    renderExpandableContent(metadata) {
        const metadataWithoutTags = metadata.metadata;
        delete metadataWithoutTags.tags;
        return (react_1.default.createElement("div", { className: METADATA_JSON_CLASS },
            react_1.default.createElement(ui_components_1.JSONComponent, { json: metadataWithoutTags })));
    }
    /**
     * A function called when the `sortMetadata` property is `true`, sorts the
     * `metadata` property alphabetically by `metadata.display_name` by default.
     * Can be overridden if a different or more intensive sorting is desired.
     */
    sortMetadata() {
        this.props.metadata.sort((a, b) => a.display_name.localeCompare(b.display_name));
    }
    getActiveTags() {
        const tags = [];
        for (const metadata of this.props.metadata) {
            if (metadata.metadata.tags) {
                for (const tag of metadata.metadata.tags) {
                    if (!tags.includes(tag)) {
                        tags.push(tag);
                    }
                }
            }
        }
        return tags;
    }
    matchesTags(filterTags, metadata) {
        // True if there are no tags selected or if there are tags that match
        // tags of metadata
        return (filterTags.size === 0 ||
            (metadata.metadata.tags &&
                metadata.metadata.tags.some((tag) => filterTags.has(tag))));
    }
    matchesSearch(searchValue, metadata) {
        searchValue = searchValue.toLowerCase();
        // True if search string is in name or display_name,
        // or if the search string is empty
        return (metadata.name.toLowerCase().includes(searchValue) ||
            metadata.display_name.toLowerCase().includes(searchValue));
    }
    static getDerivedStateFromProps(props, state) {
        if (state.searchValue === '' && state.filterTags.length === 0) {
            return {
                metadata: props.metadata,
                searchValue: '',
                filterTags: [],
                matchesSearch: state.matchesSearch,
                matchesTags: state.matchesTags
            };
        }
        if (state.searchValue !== '' || state.filterTags.length !== 0) {
            const filterTags = new Set(state.filterTags);
            const searchValue = state.searchValue.toLowerCase().trim();
            const newMetadata = props.metadata.filter(metadata => state.matchesSearch(searchValue, metadata) &&
                state.matchesTags(filterTags, metadata));
            return {
                metadata: newMetadata,
                searchValue: state.searchValue,
                filterTags: state.filterTags,
                matchesSearch: state.matchesSearch,
                matchesTags: state.matchesTags
            };
        }
        return state;
    }
    render() {
        if (this.props.sortMetadata) {
            this.sortMetadata();
        }
        return (react_1.default.createElement("div", { id: "elyra-metadata", className: this.props.className },
            react_1.default.createElement(FilterTools_1.FilterTools, { onFilter: this.filteredMetadata, tags: this.getActiveTags(), omitTags: this.props.omitTags, schemaspace: `${this.props.schemaspace}` }),
            react_1.default.createElement("div", null, this.props.metadata.map(this.renderMetadata))));
    }
}
exports.MetadataDisplay = MetadataDisplay;
/**
 * A abstract widget for viewing metadata.
 */
class MetadataWidget extends apputils_1.ReactWidget {
    constructor(props) {
        super();
        this.openMetadataEditor = (args) => {
            this.props.app.commands.execute(commands.OPEN_METADATA_EDITOR, args);
        };
        this.addClass('elyra-metadata');
        this.props = props;
        this.renderSignal = new signaling_1.Signal(this);
        this.titleContext = props.titleContext;
        this.fetchMetadata = this.fetchMetadata.bind(this);
        this.updateMetadata = this.updateMetadata.bind(this);
        this.refreshMetadata = this.refreshMetadata.bind(this);
        this.openMetadataEditor = this.openMetadataEditor.bind(this);
        this.renderDisplay = this.renderDisplay.bind(this);
        this.addMetadata = this.addMetadata.bind(this);
        this.getSchemas();
    }
    getSchemas() {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                this.schemas = yield services_1.MetadataService.getSchema(this.props.schemaspace);
                this.update();
            }
            catch (error) {
                ui_components_1.RequestErrors.serverError(error);
            }
        });
    }
    addMetadata(schema) {
        this.openMetadataEditor({
            onSave: this.updateMetadata,
            schemaspace: this.props.schemaspace,
            schema: schema
        });
    }
    /**
     * Request metadata from server and format it as expected by the
     * instance of `MetadataDisplay` rendered in `renderDisplay`
     *
     * Classes that extend MetadataWidget should override this
     *
     * @returns metadata in the format expected by `renderDisplay`
     */
    fetchMetadata() {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                return yield services_1.MetadataService.getMetadata(this.props.schemaspace);
            }
            catch (error) {
                return ui_components_1.RequestErrors.serverError(error);
            }
        });
    }
    updateMetadata() {
        this.fetchMetadata().then((metadata) => {
            this.renderSignal.emit(metadata);
        });
    }
    refreshMetadata() {
        this.updateMetadata();
    }
    // Triggered when the widget button on side panel is clicked
    onAfterShow(msg) {
        this.updateMetadata();
    }
    omitTags() {
        var _a, _b, _c, _d;
        for (const schema of (_a = this.schemas) !== null && _a !== void 0 ? _a : []) {
            if ((_d = (_c = (_b = schema.properties) === null || _b === void 0 ? void 0 : _b.metadata) === null || _c === void 0 ? void 0 : _c.properties) === null || _d === void 0 ? void 0 : _d.tags) {
                return false;
            }
        }
        return true;
    }
    /**
     * Classes that extend MetadataWidget should override this
     *
     * @returns a rendered instance of `MetadataDisplay`
     */
    renderDisplay(metadata) {
        if (Array.isArray(metadata) && !metadata.length) {
            // Empty metadata
            return (react_1.default.createElement("div", null,
                react_1.default.createElement("br", null),
                react_1.default.createElement("h6", { className: "elyra-no-metadata-msg" },
                    "Click the + button to add ",
                    this.props.display_name.toLowerCase())));
        }
        return (react_1.default.createElement(MetadataDisplay, { metadata: metadata, updateMetadata: this.updateMetadata, openMetadataEditor: this.openMetadataEditor, schemaspace: this.props.schemaspace, sortMetadata: true, className: `${exports.METADATA_CLASS}-${this.props.schemaspace}`, omitTags: this.omitTags(), titleContext: this.props.titleContext }));
    }
    render() {
        return (react_1.default.createElement(ui_components_1.ThemeProvider, { themeManager: this.props.themeManager },
            react_1.default.createElement("div", { className: exports.METADATA_CLASS },
                react_1.default.createElement("header", { className: exports.METADATA_HEADER_CLASS },
                    react_1.default.createElement("div", { style: { display: 'flex' } },
                        react_1.default.createElement(this.props.icon.react, { tag: "span", width: "auto", height: "24px", verticalAlign: "middle", marginRight: "5px" }),
                        react_1.default.createElement("p", null,
                            " ",
                            this.props.display_name,
                            " ")),
                    react_1.default.createElement(MetadataHeaderButtons_1.MetadataHeaderButtons, { schemas: this.schemas, addMetadata: this.addMetadata, titleContext: this.titleContext, appendToTitle: this.props.appendToTitle, refreshMetadata: this.refreshMetadata, refreshButtonTooltip: this.refreshButtonTooltip })),
                react_1.default.createElement(apputils_1.UseSignal, { signal: this.renderSignal, initialArgs: [] }, (_, metadata) => this.renderDisplay(metadata)))));
    }
}
exports.MetadataWidget = MetadataWidget;
//# sourceMappingURL=MetadataWidget.js.map

/***/ }),

/***/ "../metadata-common/lib/index.js":
/*!***************************************!*\
  !*** ../metadata-common/lib/index.js ***!
  \***************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


/*
 * Copyright 2018-2022 Elyra Authors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
__webpack_require__(/*! ../style/index.css */ "../metadata-common/style/index.css");
__exportStar(__webpack_require__(/*! ./MetadataEditor */ "../metadata-common/lib/MetadataEditor.js"), exports);
__exportStar(__webpack_require__(/*! ./MetadataWidget */ "../metadata-common/lib/MetadataWidget.js"), exports);
__exportStar(__webpack_require__(/*! ./MetadataHeaderButtons */ "../metadata-common/lib/MetadataHeaderButtons.js"), exports);
__exportStar(__webpack_require__(/*! ./MetadataCommonService */ "../metadata-common/lib/MetadataCommonService.js"), exports);
//# sourceMappingURL=index.js.map

/***/ })

}]);
//# sourceMappingURL=metadata-common_lib_index_js.05c76f05deb0db82719e.js.map