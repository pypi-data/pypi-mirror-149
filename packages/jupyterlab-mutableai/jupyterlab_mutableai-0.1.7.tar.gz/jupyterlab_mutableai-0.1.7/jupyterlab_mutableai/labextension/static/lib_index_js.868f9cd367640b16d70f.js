"use strict";
(self["webpackChunkjupyterlab_mutableai"] = self["webpackChunkjupyterlab_mutableai"] || []).push([["lib_index_js"],{

/***/ "./lib/commands.js":
/*!*************************!*\
  !*** ./lib/commands.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "context_custom": () => (/* binding */ context_custom),
/* harmony export */   "context_documentation": () => (/* binding */ context_documentation),
/* harmony export */   "context_fast_forward": () => (/* binding */ context_fast_forward),
/* harmony export */   "context_refactor": () => (/* binding */ context_refactor),
/* harmony export */   "invoke": () => (/* binding */ invoke),
/* harmony export */   "invokeNotebook": () => (/* binding */ invokeNotebook),
/* harmony export */   "select": () => (/* binding */ select),
/* harmony export */   "selectNotebook": () => (/* binding */ selectNotebook),
/* harmony export */   "toggleFlag": () => (/* binding */ toggleFlag),
/* harmony export */   "updateSettings": () => (/* binding */ updateSettings)
/* harmony export */ });
const invoke = 'completer:invoke';
const invokeNotebook = 'completer:invoke-notebook-1';
const select = 'completer:select';
const selectNotebook = 'completer:select-notebook-custom';
const toggleFlag = 'jupyterlab_mutableai/settings:toggle-flag';
const updateSettings = 'jupyterlab_mutableai/settings:update-settings';
const context_fast_forward = 'mutable-ai:prod';
const context_documentation = 'mutable-ai:doc';
const context_refactor = 'mutable-ai:refactor';
const context_custom = 'mutable-ai:custom';


/***/ }),

/***/ "./lib/connectors/connector.js":
/*!*************************************!*\
  !*** ./lib/connectors/connector.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CompletionConnector": () => (/* binding */ CompletionConnector)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__);
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.
// Modified from jupyterlab/packages/completer/src/connector.ts

/**
 * A multi-connector connector for completion handlers.
 */
class CompletionConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__.DataConnector {
    /**
     * Create a new connector for completion requests.
     *
     * @param connectors - Connectors to request matches from, ordered by metadata preference (descending).
     */
    constructor(connectors) {
        super();
        this._connectors = connectors;
    }
    /**
     * Fetch completion requests.
     *
     * @param request - The completion request text and details.
     * @returns Completion reply
     */
    fetch(request) {
        return Promise.all(this._connectors.map(connector => connector.fetch(request))).then(replies => {
            const definedReplies = replies.filter((reply) => !!reply);
            return Private.mergeReplies(definedReplies);
        });
    }
}
/**
 * A namespace for private functionality.
 */
var Private;
(function (Private) {
    /**
     * Merge results from multiple connectors.
     *
     * @param replies - Array of completion results.
     * @returns IReply with a superset of all matches.
     */
    function mergeReplies(replies) {
        // Filter replies with matches.
        const repliesWithMatches = replies.filter(rep => rep.matches.length > 0);
        // If no replies contain matches, return an empty IReply.
        if (repliesWithMatches.length === 0) {
            return replies[0];
        }
        // If only one reply contains matches, return it.
        if (repliesWithMatches.length === 1) {
            return repliesWithMatches[0];
        }
        // Collect unique matches from all replies.
        const matches = new Set();
        repliesWithMatches.forEach(reply => {
            reply.matches.forEach(match => matches.add(match));
        });
        // Note that the returned metadata field only contains items in the first member of repliesWithMatches.
        return Object.assign(Object.assign({}, repliesWithMatches[0]), { matches: [...matches] });
    }
    Private.mergeReplies = mergeReplies;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/connectors/customConnector.js":
/*!*******************************************!*\
  !*** ./lib/connectors/customConnector.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CustomConnector": () => (/* binding */ CustomConnector)
/* harmony export */ });
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../handler */ "./lib/handler.js");
/* eslint-disable @typescript-eslint/ban-ts-comment */
// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.


/**
 * A custom connector for completion handlers.
 */
class CustomConnector extends _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_0__.DataConnector {
    /**
     * Create a new custom connector for completion requests.
     *
     * @param options - The instatiation options for the custom connector.
     */
    constructor(options, panel, setting) {
        super();
        // @ts-ignore
        this._editor = options.editor;
        this._panel = panel;
        this.setting = setting;
    }
    /**
     * Fetch completion requests.
     *
     * @param request - The completion request text and details.
     * @returns Completion reply
     */
    fetch(request) {
        if (!this._editor) {
            return Promise.reject('No editor');
        }
        return new Promise(resolve => {
            const apiKey = this.setting.get('apiKey').composite;
            const flag = this.setting.get('flag').composite;
            const enabled = this.setting.get('enabled').composite;
            const autocompleteDomain = this.setting.get('autocompleteDomain')
                .composite;
            resolve(Private.completionHint(
            // @ts-ignore
            this._editor, this._panel, autocompleteDomain, apiKey, flag && enabled));
        });
    }
}
/**
 * A namespace for Private functionality.
 */
var Private;
(function (Private) {
    /**
     * Get a list of mocked completion hints.
     *
     * @param editor Editor
     * @returns Completion reply
     */
    async function completionHint(editor, panel, domain, apiKey, flag) {
        // Find the token at the cursor
        const cursor = editor.getCursorPosition();
        const token = editor.getTokenForPosition(cursor);
        // get source of all cells
        const cells = panel.content.widgets;
        // get index of active cell
        // @ts-ignore
        const index = cells.indexOf(panel.content.activeCell);
        // get all cells up to index
        const cellsUpToIndex = cells.slice(0, index + 1);
        // get all cells after index
        const cellsAfterIndex = cells.slice(index + 1);
        // append cellsUpToIndex to cellsAfterIndex
        const cellsToComplete = cellsAfterIndex.concat(cellsUpToIndex);
        // get source code of all cells
        const sources = cellsToComplete.map(cell => cell.model.value.text);
        // concatenate sources, this will be used as a prompt
        const prompt = sources.join('\n\n');
        console.log('prompt: ' + prompt);
        // Get all text in the editor
        //const activeCellText = editor.model.value.text;
        // get token string
        const tokenString = token.value;
        // Send to handler
        // TODO: rename this line to prompt
        const dataToSend = { line: prompt, domain, apiKey, flag };
        // POST request
        let reply = (0,_handler__WEBPACK_IMPORTED_MODULE_1__.requestAPI)('AUTOCOMPLETE', {
            body: JSON.stringify(dataToSend),
            method: 'POST'
        });
        const response = await reply;
        // Get size of text so that you can remove it from response
        //const size = previousText.length;
        //console.log("size of text: " + size);
        // Remove initial text in response
        // const responseText = response.slice(size);
        console.log('response: ' + response);
        // Create a list of matching tokens.
        const tokenList = [
            { value: tokenString + response, offset: token.offset, type: 'AI' }
            //{ value: token.value + 'Magic', offset: token.offset, type: 'magic' },
            //{ value: token.value + 'Neither', offset: token.offset },
        ];
        //console.log("value and offset")
        //console.log(token.value)
        //console.log(token.offset)
        // Only choose the ones that have a non-empty type field, which are likely to be of interest.
        const completionList = tokenList.filter(t => t.type).map(t => t.value);
        // Remove duplicate completions from the list
        const matches = Array.from(new Set(completionList));
        return {
            start: token.offset,
            end: token.offset + token.value.length,
            matches,
            metadata: {}
        };
    }
    Private.completionHint = completionHint;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'jupyterlab-mutableai', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/icons.js":
/*!**********************!*\
  !*** ./lib/icons.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "customDocIcon": () => (/* binding */ customDocIcon),
/* harmony export */   "documentIcon": () => (/* binding */ documentIcon),
/* harmony export */   "fastForwardIcon": () => (/* binding */ fastForwardIcon),
/* harmony export */   "refactorIcon": () => (/* binding */ refactorIcon)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);

const fastForwardIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'rocket',
    svgstr: `<svg
      viewBox="0 0 512 512"
      height="16"
      width="16"
      focusable="false"
      role="img"
      fill="#00000087"
      xmlns="http://www.w3.org/2000/svg"
    >
      <title>Rocket icon</title>
      <path d="M477.64 38.26a4.75 4.75 0 00-3.55-3.66c-58.57-14.32-193.9 36.71-267.22 110a317 317 0 00-35.63 42.1c-22.61-2-45.22-.33-64.49 8.07C52.38 218.7 36.55 281.14 32.14 308a9.64 9.64 0 0010.55 11.2l87.31-9.63a194.1 194.1 0 001.19 19.7 19.53 19.53 0 005.7 12L170.7 375a19.59 19.59 0 0012 5.7 193.53 193.53 0 0019.59 1.19l-9.58 87.2a9.65 9.65 0 0011.2 10.55c26.81-4.3 89.36-20.13 113.15-74.5 8.4-19.27 10.12-41.77 8.18-64.27a317.66 317.66 0 0042.21-35.64C441 232.05 491.74 99.74 477.64 38.26zM294.07 217.93a48 48 0 1167.86 0 47.95 47.95 0 01-67.86 0z"></path>
      <path d="M168.4 399.43c-5.48 5.49-14.27 7.63-24.85 9.46-23.77 4.05-44.76-16.49-40.49-40.52 1.63-9.11 6.45-21.88 9.45-24.88a4.37 4.37 0 00-3.65-7.45 60 60 0 00-35.13 17.12C50.22 376.69 48 464 48 464s87.36-2.22 110.87-25.75A59.69 59.69 0 00176 403.09c.37-4.18-4.72-6.67-7.6-3.66z"></path>
    </svg>`
});
const documentIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'document',
    svgstr: `<svg
    viewBox="0 0 48 48"
    height="16"
    width="16"
    focusable="false"
    role="img"
    fill="#00000087"
    xmlns="http://www.w3.org/2000/svg"
    >
    <title>Document icon</title>
    <path d="M24 4v11.25A3.75 3.75 0 0 0 27.75 19H40v21a3 3 0 0 1-3 3H11a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3h13z"></path>
    <path d="M26.5 4.46v10.79c0 .69.56 1.25 1.25 1.25h11.71L26.5 4.46z"></path>
    </svg>`
});
const refactorIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'refactor',
    svgstr: `<svg
    viewBox="0 0 512 512"
    height="16"
    width="16"
    focusable="false"
    role="img"
    fill="#787878"
    xmlns="http://www.w3.org/2000/svg"
    class="StyledIconBase-ea9ulj-0 bWRyML"
  >
    <title>Recycle icon</title>
    <path
      fill="#787878"
      d="M184.561 261.903c3.232 13.997-12.123 24.635-24.068 17.168l-40.736-25.455-50.867 81.402C55.606 356.273 70.96 384 96.012 384H148c6.627 0 12 5.373 12 12v40c0 6.627-5.373 12-12 12H96.115c-75.334 0-121.302-83.048-81.408-146.88l50.822-81.388-40.725-25.448c-12.081-7.547-8.966-25.961 4.879-29.158l110.237-25.45c8.611-1.988 17.201 3.381 19.189 11.99l25.452 110.237zm98.561-182.915 41.289 66.076-40.74 25.457c-12.051 7.528-9 25.953 4.879 29.158l110.237 25.45c8.672 1.999 17.215-3.438 19.189-11.99l25.45-110.237c3.197-13.844-11.99-24.719-24.068-17.168l-40.687 25.424-41.263-66.082c-37.521-60.033-125.209-60.171-162.816 0l-17.963 28.766c-3.51 5.62-1.8 13.021 3.82 16.533l33.919 21.195c5.62 3.512 13.024 1.803 16.536-3.817l17.961-28.743c12.712-20.341 41.973-19.676 54.257-.022zM497.288 301.12l-27.515-44.065c-3.511-5.623-10.916-7.334-16.538-3.821l-33.861 21.159c-5.62 3.512-7.33 10.915-3.818 16.536l27.564 44.112c13.257 21.211-2.057 48.96-27.136 48.96H320V336.02c0-14.213-17.242-21.383-27.313-11.313l-80 79.981c-6.249 6.248-6.249 16.379 0 22.627l80 79.989C302.689 517.308 320 510.3 320 495.989V448h95.88c75.274 0 121.335-82.997 81.408-146.88z"
    ></path>
  </svg>`
});
const customDocIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'customDoc',
    svgstr: `<svg
    viewBox="0 0 24 24"
    height="16"
    width="16"
    focusable="false"
    role="img"
    fill="#00000087"
    xmlns="http://www.w3.org/2000/svg"
    >
    <title>CommentEdit icon</title>
    <path d="M20 2H4c-1.103 0-2 .897-2 2v18l4-4h14c1.103 0 2-.897 2-2V4c0-1.103-.897-2-2-2zM8.999 14.987H7v-1.999l5.53-5.522 1.998 1.999-5.529 5.522zm6.472-6.464-1.999-1.999 1.524-1.523L16.995 7l-1.524 1.523z"></path>
    </svg>`
});


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IMutableAI": () => (/* reexport safe */ _tokens__WEBPACK_IMPORTED_MODULE_0__.IMutableAI),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _plugin__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./plugin */ "./lib/plugin.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");


/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_plugin__WEBPACK_IMPORTED_MODULE_1__["default"]);


/***/ }),

/***/ "./lib/manager.js":
/*!************************!*\
  !*** ./lib/manager.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MutableAIManager": () => (/* binding */ MutableAIManager)
/* harmony export */ });
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./commands */ "./lib/commands.js");
/* harmony import */ var _icons__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./icons */ "./lib/icons.js");
/* harmony import */ var _toolbarManager__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./toolbarManager */ "./lib/toolbarManager.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");









var mode;
(function (mode) {
    mode["FULL"] = "FULL";
    mode["DOCUMENT"] = "DOCUMENT";
    mode["FREE"] = "FREE";
    mode["REFACTOR"] = "REFACTOR";
})(mode || (mode = {}));
class MutableAIManager {
    constructor(options) {
        var _a;
        this._ready = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_3__.PromiseDelegate();
        this._mutableAI = null;
        this.mutableAiMainMenu = null;
        this._translator = (_a = options.translator) !== null && _a !== void 0 ? _a : _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_1__.nullTranslator;
        this._mainMenu = options.mainMenu;
        this._commands = options.commands;
        this._contextMenu = options.contextMenu;
        this._factory = options.factory;
        this._processFilePointer = null;
        this.onLunchToProduction = this.onLunchToProduction.bind(this);
        this.onDocToProduction = this.onDocToProduction.bind(this);
        this.onCustomCommand = this.onCustomCommand.bind(this);
        this.onRefactorToProduction = this.onRefactorToProduction.bind(this);
        this._toolbarManager = new _toolbarManager__WEBPACK_IMPORTED_MODULE_4__.ToolbarManager({
            docRegistry: options.docRegistry,
            handlers: {
                onLunchToProduction: this.onLunchToProduction,
                onDocToProduction: this.onDocToProduction,
                onCustomCommand: this.onCustomCommand,
                onRefactorToProduction: this.onRefactorToProduction
            },
            trans: options.translator
        });
        options
            .getSettings()
            .then(mutableAI => {
            this._mutableAI = mutableAI;
            this._mutableAI.changed.connect(this._mutableAISettingsChanged, this);
            this._mutableAISettingsChanged();
            this._ready.resolve();
        })
            .catch(reason => {
            console.warn(reason);
            this._ready.reject(reason);
        });
    }
    /*
      Mutable AI manager extension enable port.
    */
    enable() {
        var _a;
        (_a = this._mutableAI) === null || _a === void 0 ? void 0 : _a.set('enabled', true);
    }
    /*
      Mutable AI manager extension disable port.
    */
    disable() {
        var _a;
        (_a = this._mutableAI) === null || _a === void 0 ? void 0 : _a.set('enabled', false);
    }
    handleLunchToProductionCall(name) {
        var _a, _b;
        const apiKey = (_a = this._mutableAI) === null || _a === void 0 ? void 0 : _a.get('apiKey').composite;
        const transformDomain = (_b = this._mutableAI) === null || _b === void 0 ? void 0 : _b.get('transformDomain').composite;
        const dataToSend = { name, apiKey, transformDomain, mode: mode.FULL };
        const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('TRANSFORM_NB', {
            body: JSON.stringify(dataToSend),
            method: 'POST'
        });
        reply
            .then(response => console.log('Transformed Successfully!'))
            .catch(e => console.log('Transformation failed!', e));
    }
    onLunchToProduction(context) {
        const name = context.path;
        this.handleLunchToProductionCall(name);
    }
    handleDocToProductionCall(name) {
        var _a, _b;
        const apiKey = (_a = this._mutableAI) === null || _a === void 0 ? void 0 : _a.get('apiKey').composite;
        const transformDomain = (_b = this._mutableAI) === null || _b === void 0 ? void 0 : _b.get('transformDomain').composite;
        const dataToSend = { name, apiKey, transformDomain, mode: mode.DOCUMENT };
        const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('TRANSFORM_NB', {
            body: JSON.stringify(dataToSend),
            method: 'POST'
        });
        reply
            .then(response => console.log('Transformed doc Successfully!'))
            .catch(e => console.log('Transformation failed!', e));
    }
    onRefactorToProduction(context) {
        const name = context.path;
        this.handleRefactorToProductionCall(name);
    }
    handleRefactorToProductionCall(name) {
        var _a, _b;
        const apiKey = (_a = this._mutableAI) === null || _a === void 0 ? void 0 : _a.get('apiKey').composite;
        const transformDomain = (_b = this._mutableAI) === null || _b === void 0 ? void 0 : _b.get('transformDomain').composite;
        const dataToSend = { name, apiKey, transformDomain, mode: mode.REFACTOR };
        const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('TRANSFORM_NB', {
            body: JSON.stringify(dataToSend),
            method: 'POST'
        });
        reply
            .then(response => console.log('Transformed doc Successfully!'))
            .catch(e => console.log('Transformation failed!', e));
    }
    onDocToProduction(context) {
        const name = context.path;
        this.handleDocToProductionCall(name);
    }
    async handleCustomCommandCall(name) {
        var _a, _b;
        // Prompt the user about the statement to be executed
        const input = await _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.InputDialog.getText({
            title: 'Mutable AI Custom Command',
            okLabel: 'Execute',
            placeholder: 'Custom Commands'
        });
        // Execute the statement
        if (input.button.accept) {
            const commands = input.value;
            const apiKey = (_a = this._mutableAI) === null || _a === void 0 ? void 0 : _a.get('apiKey').composite;
            const transformDomain = (_b = this._mutableAI) === null || _b === void 0 ? void 0 : _b.get('transformDomain').composite;
            const dataToSend = {
                name,
                apiKey,
                transformDomain,
                instruction: commands,
                mode: mode.FREE
            };
            const reply = (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('TRANSFORM_NB', {
                body: JSON.stringify(dataToSend),
                method: 'POST'
            });
            reply
                .then(response => console.log('Transformed doc Successfully!'))
                .catch(e => console.log('Transformation failed!', e));
        }
    }
    onCustomCommand(context) {
        const name = context.path;
        this.handleCustomCommandCall(name);
    }
    createContextMenu() {
        /*
          Mutable AI update settings in main menu command.
        */
        this._forwardRef = this._commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_6__.context_fast_forward, {
            label: `Fast forward to production`,
            icon: _icons__WEBPACK_IMPORTED_MODULE_7__.fastForwardIcon,
            execute: () => {
                var _a;
                const file = (_a = this._factory.tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.selectedItems().next();
                if (file === null || file === void 0 ? void 0 : file.path) {
                    this.handleLunchToProductionCall(file.path);
                }
            }
        });
        this._docRef = this._commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_6__.context_documentation, {
            label: 'Document all methods',
            icon: _icons__WEBPACK_IMPORTED_MODULE_7__.documentIcon,
            execute: () => {
                var _a;
                const file = (_a = this._factory.tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.selectedItems().next();
                if (file === null || file === void 0 ? void 0 : file.path) {
                    this.handleDocToProductionCall(file.path);
                }
            }
        });
        this._refactorRef = this._commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_6__.context_refactor, {
            label: 'Refactor file',
            icon: _icons__WEBPACK_IMPORTED_MODULE_7__.refactorIcon,
            execute: () => {
                var _a;
                const file = (_a = this._factory.tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.selectedItems().next();
                if (file === null || file === void 0 ? void 0 : file.path) {
                    this.handleRefactorToProductionCall(file.path);
                }
            }
        });
        this._customRef = this._commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_6__.context_custom, {
            label: 'Custom command',
            icon: _icons__WEBPACK_IMPORTED_MODULE_7__.customDocIcon,
            execute: () => {
                var _a;
                const file = (_a = this._factory.tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.selectedItems().next();
                if (file === null || file === void 0 ? void 0 : file.path) {
                    this.handleCustomCommandCall(file.path);
                }
            }
        });
    }
    /*
      Mutable AI manager extension initialization.
    */
    initializePlugin() {
        var _a;
        this.dispose();
        const enabled = (_a = this._mutableAI) === null || _a === void 0 ? void 0 : _a.get('enabled').composite;
        if (enabled) {
            this._toolbarManager.initialize();
            this.createContextMenu();
            const trans = this._translator.load('jupyterlab');
            this.mutableAiMainMenu = _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_0__.MainMenu.generateMenu(this._commands, {
                id: 'mutable-ai-settings',
                label: 'Mutable AI Settings',
                rank: 80
            }, trans);
            this.mutableAiMainMenu.addGroup([
                {
                    command: _commands__WEBPACK_IMPORTED_MODULE_6__.toggleFlag
                },
                {
                    command: _commands__WEBPACK_IMPORTED_MODULE_6__.updateSettings
                }
            ]);
            this._mainMenu.addMenu(this.mutableAiMainMenu, { rank: 80 });
            this._processFilePointer = this._contextMenu.addItem({
                command: 'context_menu:open',
                selector: '.jp-DirListing-item[data-file-type="notebook"]',
                rank: 0
            });
        }
    }
    /*
      Mutable AI manager extension dispose.
    */
    dispose() {
        var _a, _b, _c, _d, _e, _f;
        (_a = this.mutableAiMainMenu) === null || _a === void 0 ? void 0 : _a.dispose();
        (_b = this._processFilePointer) === null || _b === void 0 ? void 0 : _b.dispose();
        this._toolbarManager.dispose();
        (_c = this._forwardRef) === null || _c === void 0 ? void 0 : _c.dispose();
        (_d = this._docRef) === null || _d === void 0 ? void 0 : _d.dispose();
        (_e = this._customRef) === null || _e === void 0 ? void 0 : _e.dispose();
        (_f = this._refactorRef) === null || _f === void 0 ? void 0 : _f.dispose();
    }
    /**
     * A promise that resolves when the settings have been loaded.
     */
    get ready() {
        return this._ready.promise;
    }
    /**
     * Mutable AI manager change extension according to settings.
     */
    _mutableAISettingsChanged() {
        var _a;
        const enabled = (_a = this._mutableAI) === null || _a === void 0 ? void 0 : _a.get('enabled').composite;
        if (enabled) {
            this.initializePlugin();
        }
        else {
            this.dispose();
        }
    }
}


/***/ }),

/***/ "./lib/plugin.js":
/*!***********************!*\
  !*** ./lib/plugin.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/completer */ "webpack/sharing/consume/default/@jupyterlab/completer");
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _widgets_Settings__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./widgets/Settings */ "./lib/widgets/Settings.js");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _connectors_connector__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./connectors/connector */ "./lib/connectors/connector.js");
/* harmony import */ var _connectors_customConnector__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./connectors/customConnector */ "./lib/connectors/customConnector.js");
/* harmony import */ var _tokens__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tokens */ "./lib/tokens.js");
/* harmony import */ var _commands__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./commands */ "./lib/commands.js");
/* harmony import */ var _manager__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./manager */ "./lib/manager.js");














const plugin = {
    id: _tokens__WEBPACK_IMPORTED_MODULE_8__.PLUGIN_ID,
    autoStart: true,
    provides: _tokens__WEBPACK_IMPORTED_MODULE_8__.IMutableAI,
    requires: [
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__.IFileBrowserFactory,
        _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry,
        _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_6__.IMainMenu,
        _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_7__.ITranslator,
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookTracker,
        _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ICompletionManager
    ],
    activate: (app, factory, settings, mainMenu, translator, notebooks, completionManager) => {
        const { commands, contextMenu, docRegistry } = app;
        /*
          Initialized main mutableAI manager object.
        */
        const manager = new _manager__WEBPACK_IMPORTED_MODULE_9__.MutableAIManager({
            translator,
            mainMenu,
            commands,
            contextMenu,
            factory,
            getSettings: () => settings.load(_tokens__WEBPACK_IMPORTED_MODULE_8__.PLUGIN_ID),
            docRegistry
        });
        console.log('Mutable AI context menu is activated!');
        let flag = true;
        /**
         * Load the settings for this extension
         *
         * @param setting Extension settings
         */
        function loadSetting(setting) {
            // Read the settings and convert to the correct type
            flag = setting.get('flag').composite;
        }
        // Wait for the application to be restored and
        // for the settings for this plugin to be loaded
        Promise.all([app.restored, settings.load(_tokens__WEBPACK_IMPORTED_MODULE_8__.PLUGIN_ID)]).then(([, setting]) => {
            // Read the settings
            loadSetting(setting);
            // Listen for your plugin setting changes using Signal
            setting.changed.connect(loadSetting);
            /*
              Mutable AI toggle AutoComplete flag in main menu command.
            */
            commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_10__.toggleFlag, {
                label: 'AutoComplete',
                isToggled: () => flag,
                execute: () => {
                    // Programmatically change a setting
                    Promise.all([setting.set('flag', !flag)])
                        .then(() => {
                        const newFlag = setting.get('flag').composite;
                        console.log(`Mutable AI updated flag to '${newFlag ? 'enabled' : 'disabled'}'.`);
                    })
                        .catch(reason => {
                        console.error(`Something went wrong when changing the settings.\n${reason}`);
                    });
                }
            });
            /*
              Mutable AI update settings in main menu command.
            */
            commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_10__.updateSettings, {
                label: 'Update Mutable AI Settings',
                execute: () => {
                    const close = () => { var _a; return (_a = app.shell.currentWidget) === null || _a === void 0 ? void 0 : _a.close(); };
                    const content = new _widgets_Settings__WEBPACK_IMPORTED_MODULE_11__.SettingsWidget(setting, close);
                    const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_4__.MainAreaWidget({ content });
                    widget.title.label = 'MutableAI Settings';
                    widget.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.settingsIcon;
                    app.shell.add(widget, 'main');
                }
            });
            // /*
            //   Mutable AI transform file in context menu command.
            // */
            // commands.addCommand(processFile, {
            //   label: 'Fast Forward to Production with MutableAI',
            //   caption: 'Mutable AI context menu.',
            //   icon: fastForwardIcon,
            //   execute: () => {
            //     const file = factory.tracker.currentWidget?.selectedItems().next();
            //     const apiKey = setting.get('apiKey').composite as string;
            //     const transformDomain = setting.get('transformDomain')
            //       .composite as string;
            //     const dataToSend = { name: file?.path, apiKey, transformDomain };
            //     // POST request
            //     const reply = requestAPI<any>('TRANSFORM_NB', {
            //       body: JSON.stringify(dataToSend),
            //       method: 'POST'
            //     });
            //     // Log to console
            //     reply
            //       .then(response => console.log('Transformed Successfully!'))
            //       .catch(e => console.log('Transformation failed!', e));
            //   }
            // });
            notebooks.widgetAdded.connect((sender, panel) => {
                var _a, _b;
                let editor = (_b = (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null;
                const session = panel.sessionContext.session;
                const options = { session, editor };
                const connector = new _connectors_connector__WEBPACK_IMPORTED_MODULE_12__.CompletionConnector([]);
                const handler = completionManager.register({
                    connector,
                    editor,
                    parent: panel
                });
                const updateConnector = () => {
                    var _a, _b;
                    editor = (_b = (_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.editor) !== null && _b !== void 0 ? _b : null;
                    options.session = panel.sessionContext.session;
                    options.editor = editor;
                    handler.editor = editor;
                    const kernel = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.KernelConnector(options);
                    const context = new _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_0__.ContextConnector(options);
                    /*
                     * The custom connector is getting initialized with settings.
                     * This is used to get the updated settings while making the
                     * completer api call.
                     */
                    const custom = new _connectors_customConnector__WEBPACK_IMPORTED_MODULE_13__.CustomConnector(options, panel, setting);
                    handler.connector = new _connectors_connector__WEBPACK_IMPORTED_MODULE_12__.CompletionConnector([
                        custom,
                        kernel,
                        context
                    ]);
                };
                // Update the handler whenever the prompt or session changes
                panel.content.activeCellChanged.connect(updateConnector);
                panel.sessionContext.sessionChanged.connect(updateConnector);
            });
            // Add notebook completer command.
            app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_10__.invokeNotebook, {
                execute: () => {
                    var _a;
                    const panel = notebooks.currentWidget;
                    if (panel && ((_a = panel.content.activeCell) === null || _a === void 0 ? void 0 : _a.model.type) === 'code') {
                        return app.commands.execute(_commands__WEBPACK_IMPORTED_MODULE_10__.invoke, {
                            id: panel.id
                        });
                    }
                }
            });
            // Add notebook completer select command.
            app.commands.addCommand(_commands__WEBPACK_IMPORTED_MODULE_10__.selectNotebook, {
                execute: () => {
                    const id = notebooks.currentWidget && notebooks.currentWidget.id;
                    if (id) {
                        return app.commands.execute(_commands__WEBPACK_IMPORTED_MODULE_10__.select, { id });
                    }
                }
            });
            // Set enter key for notebook completer select command.
            app.commands.addKeyBinding({
                command: _commands__WEBPACK_IMPORTED_MODULE_10__.selectNotebook,
                keys: ['Enter'],
                selector: '.jp-Notebook .jp-mod-completer-active'
            });
        });
        return manager;
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/tokens.js":
/*!***********************!*\
  !*** ./lib/tokens.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IMutableAI": () => (/* binding */ IMutableAI),
/* harmony export */   "PLUGIN_ID": () => (/* binding */ PLUGIN_ID)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

const BASE = 'jupyterlab_mutableai';
const PLUGIN_ID = `${BASE}:IMutableAI`;
const IMutableAI = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token(`${BASE}:IMutableAI`);


/***/ }),

/***/ "./lib/toolbarManager.js":
/*!*******************************!*\
  !*** ./lib/toolbarManager.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ToolbarManager": () => (/* binding */ ToolbarManager),
/* harmony export */   "ToolbarWidget": () => (/* binding */ ToolbarWidget)
/* harmony export */ });
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _widgets_Toolbar__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widgets/Toolbar */ "./lib/widgets/Toolbar.js");


class ToolbarWidget {
    constructor(config) {
        this._trans = config.trans;
        this._handlers = config.handlers;
    }
    /**
     * Create a new extension for the notebook panel widget.
     *
     * @param panel Notebook panel
     * @param context Notebook context
     * @returns Disposable on the added button
     */
    createNew(panel, context) {
        const button = new _widgets_Toolbar__WEBPACK_IMPORTED_MODULE_1__.MutableAiRunner(panel.content, this._handlers, context, this._trans);
        panel.toolbar.insertItem(10, 'Mutable AI', button);
        return new _lumino_disposable__WEBPACK_IMPORTED_MODULE_0__.DisposableDelegate(() => {
            button.dispose();
        });
    }
}
class ToolbarManager {
    constructor(config) {
        this._docRegistry = config.docRegistry;
        this._trans = config.trans;
        this._handlers = config.handlers;
    }
    initialize() {
        const toolbarItem = new ToolbarWidget({
            trans: this._trans,
            handlers: this._handlers
        });
        this._toolbar = this._docRegistry.addWidgetExtension('Notebook', toolbarItem);
    }
    dispose() {
        var _a;
        (_a = this._toolbar) === null || _a === void 0 ? void 0 : _a.dispose();
    }
}


/***/ }),

/***/ "./lib/widgets/Settings.js":
/*!*********************************!*\
  !*** ./lib/widgets/Settings.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SettingsWidget": () => (/* binding */ SettingsWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);



const SettingsComponent = (props) => {
    const { setting, close } = props;
    const [autoCompleteFlag, setAutoCompleteFlag] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(false);
    const [apiKey, setApiKey] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)('');
    const [autocompleteDomain, setAutocompleteDomain] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)('');
    const [transformDomain, setTransformDomain] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)('');
    const setValues = () => {
        // Read the settings and convert to the correct type
        setAutoCompleteFlag(setting.get('flag').composite);
        setApiKey(setting.get('apiKey').composite);
        setAutocompleteDomain(setting.get('autocompleteDomain').composite);
        setTransformDomain(setting.get('transformDomain').composite);
    };
    const restoreToDefault = () => {
        /*
         * This fetches the default settings from
         * user settings then sets then sets it
         * in the form. But as the form is not
         * submitted it is not saved until save
         * button is pressed.
         */
        const flagDefault = setting.default('flag');
        const apiKeyDefault = setting.default('apiKey');
        const autocompleteDomainDefault = setting.default('autocompleteDomain');
        const transformDomainDefault = setting.default('transformDomain');
        setAutoCompleteFlag(flagDefault);
        setApiKey(apiKeyDefault);
        setAutocompleteDomain(autocompleteDomainDefault);
        setTransformDomain(transformDomainDefault);
        setting.set('flag', flagDefault);
        setting.set('apiKey', apiKeyDefault);
        setting.set('autocompleteDomain', autocompleteDomainDefault);
        setting.set('transformDomain', transformDomainDefault);
    };
    /*
     * Whenever the settings object is changed from
     * outside the widget it updates the form accordingly.
     */
    setting.changed.connect(setValues);
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        /*
         * When the widget is attached.
         * It gets the last values from
         * settings object and updates the
         * settings form.
         */
        setValues();
    }, []);
    const handleSubmit = (e) => {
        /*
         * This function gets the submitted form
         * It then updates the values from form-data
         * After that the latest data is saved in user-settings.
         * Also after successful saving it shows a
         */
        e.preventDefault();
        const okButton = _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({
            className: 'btn jp-mutableai-modal-btn'
        });
        try {
            setting.set('flag', autoCompleteFlag);
            setting.set('apiKey', apiKey);
            setting.set('autocompleteDomain', autocompleteDomain);
            setting.set('transformDomain', transformDomain);
            // Success dialog.
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: 'Mutable AI Settings',
                body: 'The changes saved successfully!',
                buttons: [okButton]
            });
        }
        catch (e) {
            // Error dialog.
            (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
                title: 'Mutable AI Settings',
                body: 'Something went wrong saving settings. Reason: ' + e.toString(),
                buttons: [okButton]
            });
        }
    };
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "jp-mutableai-container" },
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("h1", null, "Mutable AI Settings"),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "jp-mutableai-header" },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { className: "btn btn-secondary", type: "button", onClick: restoreToDefault }, "Restore to Defaults")),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("form", { className: "jp-mutableai-form", onSubmit: handleSubmit },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "jp-mutableai-group " },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", null, "Autocomplete Flag"),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { type: "checkbox", checked: autoCompleteFlag, onChange: e => setAutoCompleteFlag(e.target.checked) }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("span", null, "This controls whether or not autocomplete is activated.")),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "jp-mutableai-group " },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", null, "API key"),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { className: "form-control", placeholder: "", type: "text", value: apiKey, onChange: e => setApiKey(e.target.value) }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("span", null, "This is the api key to call the endpoints.")),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "jp-mutableai-group " },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", null, "Autocomplete Domain"),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { className: "form-control", placeholder: "", type: "text", value: autocompleteDomain, onChange: e => setAutocompleteDomain(e.target.value) }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("span", null, "Used to construct url to call autocomplete endpoint")),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "jp-mutableai-group " },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", null, "Transform Domain"),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { className: "form-control", placeholder: "", type: "text", value: transformDomain, onChange: e => setTransformDomain(e.target.value) }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("span", null, "Used to construct url to call transform endpoint")),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: "jp-mutableai-footer" },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { className: "btn btn-secondary", type: "button", onClick: close }, "Cancel"),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { className: "btn btn-success", type: "submit" }, "Save")))));
};
class SettingsWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(setting, close) {
        super();
        // This is the top widget class for settings widget.
        this.addClass('jp-mutableai-widget');
        // settings object passed here is used.
        // This is used to get, set, update
        // mutable AI settings.
        this.setting = setting;
        // This is used to close the shell.
        this.closeShell = close;
    }
    render() {
        // This is the settings component passed to the widget.
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(SettingsComponent, { setting: this.setting, close: () => this.closeShell() }));
    }
}


/***/ }),

/***/ "./lib/widgets/Toolbar.js":
/*!********************************!*\
  !*** ./lib/widgets/Toolbar.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "MutableAiRunner": () => (/* binding */ MutableAiRunner),
/* harmony export */   "default": () => (/* binding */ useComponentVisible)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__);



const TOOLBAR_CELLTYPE_CLASS = 'mutable-ai-toolbar';
function useComponentVisible(initialIsVisible) {
    const [active, setActive] = react__WEBPACK_IMPORTED_MODULE_0__.useState(initialIsVisible);
    const ref = react__WEBPACK_IMPORTED_MODULE_0__.useRef(null);
    const handleClickOutside = (event) => {
        // @ts-ignore
        if (ref.current && !ref.current.contains(event.target)) {
            setActive(false);
        }
    };
    react__WEBPACK_IMPORTED_MODULE_0__.useEffect(() => {
        document.addEventListener('click', handleClickOutside, true);
        return () => {
            document.removeEventListener('click', handleClickOutside, true);
        };
    }, []);
    return { ref, active, setActive };
}
const Toolbar = (props) => {
    const { trans, handlers, context } = props;
    const { ref, active, setActive } = useComponentVisible(false);
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", { className: 'mutable-ai-container ' + (active ? 'mutable-ai-container-active' : ''), ref: ref },
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("button", { className: "bp3-button bp3-minimal mutable-ai-prod jp-ToolbarButtonComponent minimal jp-Button", onClick: () => setActive(!active) },
            trans.__('MutableAI Commands'),
            ' ',
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", { style: { marginLeft: 5, paddingTop: 5 } },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", { xmlns: "http://www.w3.org/2000/svg", width: "16", viewBox: "0 0 18 18", "data-icon": "ui-components:caret-down-empty" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("g", { xmlns: "http://www.w3.org/2000/svg", className: "jp-icon3", fill: "#616161", "shape-rendering": "geometricPrecision" },
                        react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", { d: "M5.2,5.9L9,9.7l3.8-3.8l1.2,1.2l-4.9,5l-4.9-5L5.2,5.9z" }))))),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("ul", { className: 'mutable-ai-dropdown ' +
                (active ? 'mutable-ai-show' : 'mutable-ai-hidden') },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("li", { onClick: () => {
                    setActive(false);
                    handlers.onLunchToProduction(context);
                } },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", { viewBox: "0 0 512 512", height: "16", width: "16", focusable: "false", role: "img", fill: "#00000087", xmlns: "http://www.w3.org/2000/svg", className: "StyledIconBase-ea9ulj-0 bWRyML" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", null, "Rocket icon"),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", { d: "M477.64 38.26a4.75 4.75 0 00-3.55-3.66c-58.57-14.32-193.9 36.71-267.22 110a317 317 0 00-35.63 42.1c-22.61-2-45.22-.33-64.49 8.07C52.38 218.7 36.55 281.14 32.14 308a9.64 9.64 0 0010.55 11.2l87.31-9.63a194.1 194.1 0 001.19 19.7 19.53 19.53 0 005.7 12L170.7 375a19.59 19.59 0 0012 5.7 193.53 193.53 0 0019.59 1.19l-9.58 87.2a9.65 9.65 0 0011.2 10.55c26.81-4.3 89.36-20.13 113.15-74.5 8.4-19.27 10.12-41.77 8.18-64.27a317.66 317.66 0 0042.21-35.64C441 232.05 491.74 99.74 477.64 38.26zM294.07 217.93a48 48 0 1167.86 0 47.95 47.95 0 01-67.86 0z" }),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", { d: "M168.4 399.43c-5.48 5.49-14.27 7.63-24.85 9.46-23.77 4.05-44.76-16.49-40.49-40.52 1.63-9.11 6.45-21.88 9.45-24.88a4.37 4.37 0 00-3.65-7.45 60 60 0 00-35.13 17.12C50.22 376.69 48 464 48 464s87.36-2.22 110.87-25.75A59.69 59.69 0 00176 403.09c.37-4.18-4.72-6.67-7.6-3.66z" })),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", null, trans.__('Fast forward to production'))),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("li", { onClick: () => {
                    setActive(false);
                    handlers.onDocToProduction(context);
                } },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", { viewBox: "0 0 48 48", height: "16", width: "16", focusable: "false", role: "img", fill: "#00000087", xmlns: "http://www.w3.org/2000/svg", className: "StyledIconBase-ea9ulj-0 bWRyML" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", null, "Document icon"),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", { d: "M24 4v11.25A3.75 3.75 0 0 0 27.75 19H40v21a3 3 0 0 1-3 3H11a3 3 0 0 1-3-3V7a3 3 0 0 1 3-3h13z" }),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", { d: "M26.5 4.46v10.79c0 .69.56 1.25 1.25 1.25h11.71L26.5 4.46z" })),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", null, trans.__('Document all methods'))),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("li", { onClick: () => {
                    setActive(false);
                    handlers.onRefactorToProduction(context);
                } },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", { viewBox: "0 0 512 512", height: "16", width: "16", focusable: "false", role: "img", fill: "#787878", xmlns: "http://www.w3.org/2000/svg", className: "StyledIconBase-ea9ulj-0 bWRyML" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", null, "Recycle icon"),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", { fill: "#787878", d: "M184.561 261.903c3.232 13.997-12.123 24.635-24.068 17.168l-40.736-25.455-50.867 81.402C55.606 356.273 70.96 384 96.012 384H148c6.627 0 12 5.373 12 12v40c0 6.627-5.373 12-12 12H96.115c-75.334 0-121.302-83.048-81.408-146.88l50.822-81.388-40.725-25.448c-12.081-7.547-8.966-25.961 4.879-29.158l110.237-25.45c8.611-1.988 17.201 3.381 19.189 11.99l25.452 110.237zm98.561-182.915 41.289 66.076-40.74 25.457c-12.051 7.528-9 25.953 4.879 29.158l110.237 25.45c8.672 1.999 17.215-3.438 19.189-11.99l25.45-110.237c3.197-13.844-11.99-24.719-24.068-17.168l-40.687 25.424-41.263-66.082c-37.521-60.033-125.209-60.171-162.816 0l-17.963 28.766c-3.51 5.62-1.8 13.021 3.82 16.533l33.919 21.195c5.62 3.512 13.024 1.803 16.536-3.817l17.961-28.743c12.712-20.341 41.973-19.676 54.257-.022zM497.288 301.12l-27.515-44.065c-3.511-5.623-10.916-7.334-16.538-3.821l-33.861 21.159c-5.62 3.512-7.33 10.915-3.818 16.536l27.564 44.112c13.257 21.211-2.057 48.96-27.136 48.96H320V336.02c0-14.213-17.242-21.383-27.313-11.313l-80 79.981c-6.249 6.248-6.249 16.379 0 22.627l80 79.989C302.689 517.308 320 510.3 320 495.989V448h95.88c75.274 0 121.335-82.997 81.408-146.88z" })),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", null, trans.__('Refactor File'))),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("li", { onClick: () => {
                    setActive(false);
                    handlers.onCustomCommand(context);
                } },
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("svg", { viewBox: "0 0 24 24", height: "16", width: "16", focusable: "false", role: "img", fill: "#00000087", xmlns: "http://www.w3.org/2000/svg", className: "StyledIconBase-ea9ulj-0 bWRyML" },
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("title", null, "CommentEdit icon"),
                    react__WEBPACK_IMPORTED_MODULE_0__.createElement("path", { d: "M20 2H4c-1.103 0-2 .897-2 2v18l4-4h14c1.103 0 2-.897 2-2V4c0-1.103-.897-2-2-2zM8.999 14.987H7v-1.999l5.53-5.522 1.998 1.999-5.529 5.522zm6.472-6.464-1.999-1.999 1.524-1.523L16.995 7l-1.524 1.523z" })),
                react__WEBPACK_IMPORTED_MODULE_0__.createElement("span", null, trans.__('Custom command'))))));
};
class MutableAiRunner extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(widget, handlers, context, translator) {
        super();
        this._trans = (translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_2__.nullTranslator).load('jupyterlab');
        this._handlers = handlers;
        this._context = context;
        this.addClass(TOOLBAR_CELLTYPE_CLASS);
        if (widget.model) {
            this.update();
        }
        widget.activeCellChanged.connect(this.update, this);
        // Follow a change in the selection.
        widget.selectionChanged.connect(this.update, this);
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(Toolbar, { trans: this._trans, handlers: this._handlers, context: this._context }));
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.868f9cd367640b16d70f.js.map