(self["webpackChunkipypetrinet"] = self["webpackChunkipypetrinet"] || []).push([["lib_widget_js"],{

/***/ "./lib/customTrans.js":
/*!****************************!*\
  !*** ./lib/customTrans.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Jakob Bucksch
// Distributed under the terms of the Modified BSD License.
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
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.customTransition = void 0;
const joint = __importStar(__webpack_require__(/*! ../node_modules/jointjs/dist/joint */ "./node_modules/jointjs/dist/joint.js"));
// Extending the joint.shapes.pn.Transition:
// Set some constants to structure it clearly
const PADDING_S = 4;
const PADDING_L = 4;
const FONT_FAMILY = 'sans-serif';
const LIGHT_COLOR = '#FFF';
const DARK_COLOR = '#333';
const ACTION_COLOR = '#7c68fc';
const LINE_WIDTH = 2;
const HEADER_HEIGHT = 15;
const LIST_MAX_PORT_COUNT = 5;
const LIST_GROUP_NAME = 'conditions';
const LIST_ITEM_HEIGHT = 23;
const LIST_ITEM_WIDTH = 120;
const LIST_ITEM_LABEL = 'Condition Item';
const LIST_ITEM_GAP = 1;
const LIST_BUTTON_RADIUS = 16;
const LIST_ADD_BUTTON_SIZE = 20;
const LIST_REMOVE_BUTTON_SIZE = 16;
const itemPosition = (portsArgs, elBBox) => {
    return portsArgs.map((_port, index, { length }) => {
        const bottom = elBBox.height - (LIST_ITEM_HEIGHT + LIST_ADD_BUTTON_SIZE) / 2 - PADDING_S;
        const y = (length - 1 - index) * (LIST_ITEM_HEIGHT + LIST_ITEM_GAP);
        return new joint.g.Point(0, bottom - y);
    });
};
const conditionAttributes = {
    attrs: {
        portBody: {
            width: 'calc(w)',
            height: 'calc(h)',
            x: '2',
            y: 'calc(-0.5*h)',
            fill: '#333',
            rx: 3,
            ry: 3
        },
        portRemoveButton: {
            cursor: 'pointer',
            event: 'element:port:remove',
            transform: `translate(${PADDING_L},0)`,
            title: 'Remove Condition'
        },
        portRemoveButtonBody: {
            width: LIST_REMOVE_BUTTON_SIZE,
            height: LIST_REMOVE_BUTTON_SIZE,
            x: 1,
            y: -LIST_REMOVE_BUTTON_SIZE / 2,
            fill: LIGHT_COLOR,
            rx: LIST_BUTTON_RADIUS,
            ry: LIST_BUTTON_RADIUS
        },
        portRemoveButtonIcon: {
            d: 'M 5 -4 13 4 M 5 4 13 -4',
            stroke: DARK_COLOR,
            strokeWidth: LINE_WIDTH
        },
        portLabel: {
            pointerEvents: 'none',
            fontFamily: FONT_FAMILY,
            fontWeight: 400,
            fontSize: 10,
            fill: LIGHT_COLOR,
            textAnchor: 'start',
            textVerticalAnchor: 'middle',
            textWrap: {
                width: -LIST_REMOVE_BUTTON_SIZE - PADDING_L - 2 * PADDING_S,
                maxLineCount: 1,
                ellipsis: true
            },
            x: PADDING_L + LIST_REMOVE_BUTTON_SIZE + PADDING_S
        },
    },
    size: {
        width: LIST_ITEM_WIDTH,
        height: LIST_ITEM_HEIGHT
    },
    markup: [{
            tagName: 'rect',
            selector: 'portBody'
        }, {
            tagName: 'text',
            selector: 'portLabel',
        }, {
            tagName: 'g',
            selector: 'portRemoveButton',
            children: [{
                    tagName: 'rect',
                    selector: 'portRemoveButtonBody'
                }, {
                    tagName: 'path',
                    selector: 'portRemoveButtonIcon'
                }]
        }]
};
const bodyAttributes = {
    attrs: {
        ".root": {
            magnet: true
        },
        body: {
            width: 'calc(w)',
            height: 'calc(h)',
            fill: "#9586fd",
            strokeWidth: LINE_WIDTH + 1,
            stroke: "#7c68fc",
            rx: 3,
            ry: 3,
        },
        label: {
            'text-anchor': 'middle',
            'ref-x': .5,
            'ref-y': -15,
            'ref': 'rect',
            'text': "",
            'fill': '#fe854f',
            'font-size': 12,
            'font-weight': 600,
        },
        portAddButton: {
            title: 'Add Condition',
            cursor: 'pointer',
            event: 'element:port:add',
            transform: `translate(calc(w-${3 * PADDING_S}),calc(h))`,
        },
        portAddButtonBody: {
            width: LIST_ADD_BUTTON_SIZE,
            height: LIST_ADD_BUTTON_SIZE,
            rx: LIST_BUTTON_RADIUS,
            ry: LIST_BUTTON_RADIUS,
            x: -LIST_ADD_BUTTON_SIZE / 2,
            y: -LIST_ADD_BUTTON_SIZE / 2,
        },
        portAddButtonIcon: {
            d: 'M -4 0 4 0 M 0 -4 0 4',
            stroke: LIGHT_COLOR,
            strokeWidth: LINE_WIDTH
        }
    },
    markup: [{
            tagName: 'rect',
            selector: 'body',
        }, {
            tagName: 'text',
            selector: 'label',
        }, {
            tagName: 'g',
            selector: 'portAddButton',
            children: [{
                    tagName: 'rect',
                    selector: 'portAddButtonBody'
                }, {
                    tagName: 'path',
                    selector: 'portAddButtonIcon'
                }]
        }]
};
// Actual Extension of the Transition:
class customTransition extends joint.shapes.pn.Transition {
    defaults() {
        return Object.assign(Object.assign(Object.assign({}, super.defaults), bodyAttributes), { type: "customTransition", size: { width: LIST_ITEM_WIDTH + 4, height: 0 }, exectime: "1", eventAttrs: [], ports: {
                groups: {
                    [LIST_GROUP_NAME]: Object.assign({ position: itemPosition }, conditionAttributes)
                },
                items: []
            } });
    }
    initialize(...args) {
        this.on('change:ports', () => this.resizeToFitPorts());
        this.resizeToFitPorts();
        this.toggleAddPortButton(LIST_GROUP_NAME);
        super.initialize.call(this, ...args);
    }
    resizeToFitPorts() {
        const { length } = this.getPorts();
        this.toggleAddPortButton(LIST_GROUP_NAME);
        const height = HEADER_HEIGHT + (LIST_ITEM_HEIGHT + LIST_ITEM_GAP) * length + PADDING_L;
        this.prop(['size', 'height'], HEADER_HEIGHT + (LIST_ITEM_HEIGHT + LIST_ITEM_GAP) * length + PADDING_L);
        return height;
    }
    addDefaultPort(label) {
        if (!this.canAddPort(LIST_GROUP_NAME))
            return;
        this.addPort({
            group: LIST_GROUP_NAME,
            attrs: { portLabel: { text: label } }
        });
    }
    getDefaultPortName() {
        const ports = this.getGroupPorts(LIST_GROUP_NAME);
        let portName;
        let i = 1;
        do {
            portName = `${LIST_ITEM_LABEL} ${i++}`;
        } while (ports.find(port => port.attrs.portLabel.text === portName));
        return portName;
    }
    canAddPort(group) {
        return Object.keys(this.getGroupPorts(group)).length < LIST_MAX_PORT_COUNT;
    }
    toggleAddPortButton(group) {
        const buttonAttributes = this.canAddPort(group)
            ? { fill: ACTION_COLOR, cursor: 'pointer' }
            : { fill: 'lightgray', cursor: 'not-allowed' };
        this.attr(['portAddButton'], buttonAttributes, {
            isolate: true
        });
    }
}
exports.customTransition = customTransition;
//# sourceMappingURL=customTrans.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Jakob Bucksch
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Jakob Bucksch
// Distributed under the terms of the Modified BSD License.
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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.PetriView = exports.PetriModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const customTrans_1 = __webpack_require__(/*! ./customTrans */ "./lib/customTrans.js");
const joint = __importStar(__webpack_require__(/*! ../node_modules/jointjs/dist/joint */ "./node_modules/jointjs/dist/joint.js"));
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
const graphlib_1 = __importDefault(__webpack_require__(/*! graphlib */ "webpack/sharing/consume/default/graphlib/graphlib"));
const dagre_1 = __importDefault(__webpack_require__(/*! dagre */ "./node_modules/dagre/index.js"));
// very important for loading a saved graph (namespace problem)
window.joint = joint;
// Make sure graph.fromJSON() will find the custom shape
Object.assign(joint.shapes, { customTransition: customTrans_1.customTransition });
class PetriModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: PetriModel.model_name, _model_module: PetriModel.model_module, _model_module_version: PetriModel.model_module_version, _view_name: PetriModel.view_name, _view_module: PetriModel.view_module, _view_module_version: PetriModel.view_module_version, graph: [], caseAttrs: [] });
    }
}
exports.PetriModel = PetriModel;
PetriModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
PetriModel.model_name = 'PetriModel';
PetriModel.model_module = version_1.MODULE_NAME;
PetriModel.model_module_version = version_1.MODULE_VERSION;
PetriModel.view_name = 'PetriView'; // Set to null if no view
PetriModel.view_module = version_1.MODULE_NAME; // Set to null if no view
PetriModel.view_module_version = version_1.MODULE_VERSION;
class PetriView extends base_1.DOMWidgetView {
    render() {
        // DROPDOWN GRAPH-BUTTON
        var dropdown = document.createElement("div");
        dropdown.className = "dropdown";
        var graphsButton = document.createElement("button");
        graphsButton.className = "button button2";
        graphsButton.innerHTML = '<i class="fa fa-list"></i>' + " Graphs";
        var dropdownContent = document.createElement("div");
        dropdownContent.id = "dropdown-content";
        dropdownContent.className = "dropdown-content";
        var firstExample = document.createElement("a");
        firstExample.textContent = "Example 1";
        firstExample.addEventListener("click", (e) => this.firstExample());
        var secondExample = document.createElement("a");
        secondExample.textContent = "Example 2";
        secondExample.addEventListener("click", (e) => this.secondExample());
        dropdownContent.appendChild(firstExample);
        dropdownContent.appendChild(secondExample);
        dropdown.appendChild(graphsButton);
        dropdown.appendChild(dropdownContent);
        // BUTTONS
        var addToken = document.createElement("button");
        addToken.className = "button button1";
        addToken.addEventListener("click", (e) => this.addToken());
        addToken.innerHTML = '<i class="fa fa-plus"></i>';
        var removeToken = document.createElement("button");
        removeToken.className = "button button1";
        removeToken.addEventListener("click", (e) => this.removeToken());
        removeToken.innerHTML = '<i class="fa fa-minus"></i>';
        var addPlace = document.createElement("button");
        addPlace.className = "button button1";
        addPlace.addEventListener("click", (e) => this.addPlace());
        addPlace.innerHTML = '<i class="fa fa-plus"></i>' + " Place";
        var addTrans = document.createElement("button");
        addTrans.className = "button button1";
        addTrans.addEventListener("click", (e) => this.addTrans());
        addTrans.innerHTML = '<i class="fa fa-plus"></i>' + " Transition";
        var setLayout = document.createElement("button");
        setLayout.className = "button button1";
        setLayout.addEventListener("click", (e) => PetriView.showPopup("layoutPopup"));
        setLayout.innerHTML = '<i class="fa fa-sitemap"></i>' + " Layout";
        var clearAll = document.createElement("button");
        clearAll.className = "button button1";
        clearAll.addEventListener("click", (e) => this.clearAll());
        clearAll.innerHTML = '<i class="fa fa-eraser"></i>' + " Clear";
        var simulate = document.createElement("button");
        simulate.className = "button button1";
        simulate.addEventListener("click", (e) => this.simulate());
        simulate.innerHTML = '<i class="fa fa-caret-right icon-large"></i>' + " Play";
        var stopSimulation = document.createElement("button");
        stopSimulation.className = "button button1";
        stopSimulation.addEventListener("click", (e) => this.stopSimulation());
        stopSimulation.innerHTML = '<i class="fa fa-stop"></i>' + " Stop";
        var lockModel = document.createElement("button");
        lockModel.className = "button button1";
        lockModel.id = "lock";
        lockModel.addEventListener("click", (e) => this.lockModel());
        lockModel.innerHTML = '<i class="fa fa-unlock"></i>' + " Lock";
        var reloadSim = document.createElement("button");
        reloadSim.className = "button button1";
        reloadSim.addEventListener("click", (e) => this.resetSim());
        reloadSim.innerHTML = '<i class="fa fa-refresh"></i>' + " Reset";
        var saveGraph = document.createElement("button");
        saveGraph.className = "button button2";
        saveGraph.addEventListener("click", (e) => PetriView.showPopup("savePopup"));
        saveGraph.innerHTML = '<i class="fa fa-save"></i>' + " Save Graph";
        var saveIMG = document.createElement("button");
        saveIMG.className = "button button2";
        saveIMG.addEventListener("click", (e) => this.saveIMG());
        saveIMG.innerHTML = '<i class="fa fa-download"></i>' + " Download SVG";
        var importJSON = document.createElement("button");
        importJSON.className = "button button2";
        importJSON.addEventListener("click", (e) => PetriView.showPopup("uploadPopup"));
        importJSON.innerHTML = '<i class="fa fa-upload"></i>' + " Import Graph";
        var downloadJSON = document.createElement("button");
        downloadJSON.className = "button button2";
        downloadJSON.addEventListener("click", (e) => PetriView.showPopup("DownloadPopup"));
        downloadJSON.innerHTML = '<i class="fa fa-download"></i>' + " Download Graph";
        var zoomIn = document.createElement("button");
        zoomIn.className = "button button2";
        zoomIn.addEventListener("click", (e) => PetriView.zoomIt(1));
        zoomIn.innerHTML = '<i class="fa fa-search-plus"></i>' + " Zoom in";
        var zoomOut = document.createElement("button");
        zoomOut.className = "button button2";
        zoomOut.addEventListener("click", (e) => PetriView.zoomIt(-1));
        zoomOut.innerHTML = '<i class="fa fa-search-minus"></i>' + " Zoom out";
        var addAttrs = document.createElement("button");
        addAttrs.className = "button button1";
        addAttrs.addEventListener("click", (e) => PetriView.showPopup("attrPopup"));
        addAttrs.innerHTML = '<i class="fa fa-plus"></i>' + " Attributes";
        // DOWNLOAD-POPUP
        var downPopup = document.createElement("div");
        downPopup.id = "DownloadPopup";
        downPopup.className = "popup";
        downPopup.style.display = "none";
        var downPopupContent = document.createElement("div");
        downPopupContent.id = "DownloadPopupContent";
        downPopupContent.className = "popup-content";
        downPopupContent.style.display = "flex";
        var JSONButton = document.createElement("button");
        JSONButton.id = "JSONButton";
        JSONButton.className = "button button1";
        JSONButton.innerHTML = "JSON";
        JSONButton.addEventListener("click", (e) => this.downloadJSON());
        var PNMLButton = document.createElement("button");
        PNMLButton.id = "PNMLButton";
        PNMLButton.className = "button button1";
        PNMLButton.innerHTML = "PNML";
        PNMLButton.addEventListener("click", (e) => this.downloadPNML());
        downPopupContent.append(JSONButton, PNMLButton);
        downPopup.appendChild(downPopupContent);
        // ATTRIBUTES-POPUP
        var attrPopup = document.createElement("div");
        attrPopup.id = "attrPopup";
        attrPopup.className = "popup";
        attrPopup.style.display = "none";
        var attrPopupContent = document.createElement("div");
        attrPopupContent.className = "popup-content attributes";
        attrPopupContent.id = "attrPopupContent";
        var caseTab = document.createElement("button");
        caseTab.id = "caseTab";
        caseTab.className = "tablinks active";
        caseTab.textContent = "Add Case-Attributes";
        caseTab.addEventListener("click", (e) => PetriView.showTab(caseTab.id));
        var eventTab = document.createElement("button");
        eventTab.id = "eventTab";
        eventTab.className = "tablinks";
        eventTab.textContent = "Add Event-Attributes";
        eventTab.addEventListener("click", (e) => PetriView.showTab(eventTab.id));
        var tabBar = document.createElement("div");
        tabBar.id = "tabBar";
        tabBar.className = "tab";
        tabBar.style.display = "flex";
        tabBar.append(caseTab, eventTab);
        var caseAttrsList = document.createElement('ul');
        caseAttrsList.id = "caseAttrsList";
        var observer = new MutationObserver(() => this.updateCaseAttrs());
        observer.observe(caseAttrsList, { childList: true });
        var attrName = document.createElement("input");
        attrName.id = "attrName";
        attrName.type = "text";
        attrName.placeholder = "Name your attribute...";
        attrName.oninput = this.enableAttributeButtons;
        var check0 = document.createElement("input");
        check0.type = "radio";
        check0.id = "staticAttr";
        check0.name = "dist";
        check0.addEventListener("change", (e) => this.toggleFields(check0.id));
        var label0 = document.createElement("label");
        label0.htmlFor = "staticAttr";
        label0.textContent = "List with probabilities";
        var div0 = document.createElement("div");
        div0.style.display = "flex";
        div0.append(check0, label0);
        var staticValue = document.createElement("input");
        staticValue.id = "staticVal";
        staticValue.placeholder = '"item0", "item1", "item2", ...';
        staticValue.style.display = "none";
        var staticProbs = document.createElement("input");
        staticProbs.id = "staticProbs";
        staticProbs.placeholder = "Probabilities summing to one...";
        staticProbs.style.display = "none";
        var check1 = document.createElement("input");
        check1.type = "radio";
        check1.id = "normalDist";
        check1.name = "dist";
        check1.addEventListener("change", (e) => this.toggleFields(check1.id));
        var label1 = document.createElement("label");
        label1.htmlFor = "normalDist";
        label1.textContent = "Normal Distribution";
        var div1 = document.createElement("div");
        div1.style.display = "flex";
        div1.append(check1, label1);
        var mue = document.createElement("input");
        mue.id = "mue";
        mue.type = "number";
        mue.placeholder = "Select mean...";
        mue.style.display = "none";
        var sigma = document.createElement("input");
        sigma.id = "sigma";
        sigma.type = "number";
        sigma.placeholder = "Select sigma...";
        sigma.style.display = "none";
        var check2 = document.createElement("input");
        check2.type = "radio";
        check2.id = "bernDist";
        check2.name = "dist";
        check2.addEventListener("change", (e) => this.toggleFields(check2.id));
        var label2 = document.createElement("label");
        label2.htmlFor = "bernDist";
        label2.textContent = "Bernoulli Distribution";
        label2.append(check2);
        var div2 = document.createElement("div");
        div2.style.display = "flex";
        div2.append(check2, label2);
        var n = document.createElement("input");
        n.id = "n";
        n.placeholder = "Choose n...";
        n.type = "number";
        n.min = "0";
        n.step = "1";
        n.style.display = "none";
        var p = document.createElement("input");
        p.id = "p";
        p.placeholder = "Choose p...";
        p.type = "number";
        p.min = "0";
        p.max = "1";
        p.step = "0.01";
        p.style.display = "none";
        var check3 = document.createElement("input");
        check3.type = "radio";
        check3.id = "gammaDist";
        check3.name = "dist";
        check3.addEventListener("change", (e) => this.toggleFields(check3.id));
        var label3 = document.createElement("label");
        label3.htmlFor = "gammaDist";
        label3.textContent = "Gamma Distribution";
        var div3 = document.createElement("div");
        div3.style.display = "flex";
        div3.append(check3, label3);
        var k = document.createElement("input");
        k.id = "k";
        k.placeholder = "Choose k...";
        k.type = "number";
        k.min = "0";
        k.style.display = "none";
        var theta = document.createElement("input");
        theta.id = "theta";
        theta.placeholder = "Choose theta...";
        theta.type = "number";
        theta.min = "0";
        theta.style.display = "none";
        var check4 = document.createElement("input");
        check4.type = "radio";
        check4.id = "expoDist";
        check4.name = "dist";
        check4.addEventListener("change", (e) => this.toggleFields(check4.id));
        var label4 = document.createElement("label");
        label4.htmlFor = "expoDist";
        label4.textContent = "Exponential Distribution";
        var div4 = document.createElement("div");
        div4.style.display = "flex";
        div4.append(check4, label4);
        var beta = document.createElement("input");
        beta.id = "beta";
        beta.placeholder = "Choose beta...";
        beta.type = "number";
        beta.min = "0";
        beta.style.display = "none";
        var addCaseAttributes = document.createElement("button");
        addCaseAttributes.className = "button button1";
        addCaseAttributes.id = "addCaseAttributes";
        addCaseAttributes.textContent = "Add Case-Attribute!";
        addCaseAttributes.disabled = true;
        addCaseAttributes.addEventListener("click", (e) => this.addAttributes());
        var caseTabContent = document.createElement("div");
        caseTabContent.id = "caseTabContent";
        caseTabContent.style.display = "block";
        var eventTabContent = document.createElement("div");
        eventTabContent.id = "eventTabContent";
        eventTabContent.style.display = "none";
        var eventHeader = document.createElement("p");
        eventHeader.id = "eventHeader";
        eventHeader.style.marginLeft = "1px";
        eventHeader.textContent = "Select the transition to be linked:";
        var transList = document.createElement("ul");
        transList.id = "transList";
        transList.style.columns = "2";
        var addEventAttributes = document.createElement("button");
        addEventAttributes.className = "button button1";
        addEventAttributes.id = "addEventAttributes";
        addEventAttributes.textContent = "Add Event-Attribute!";
        addEventAttributes.disabled = true;
        addEventAttributes.addEventListener("click", (e) => this.addAttributes());
        var eventAttrsList = document.createElement('ul');
        eventAttrsList.id = "eventAttrsList";
        caseTabContent.append(addCaseAttributes, caseAttrsList);
        eventTabContent.append(eventHeader, transList, addEventAttributes, eventAttrsList);
        attrPopupContent.append(tabBar, attrName, div0, staticValue, staticProbs, div1, mue, sigma, div2, n, p, div3, k, theta, div4, beta, caseTabContent, eventTabContent);
        attrPopup.append(attrPopupContent);
        // LAYOUT-POPUP
        var layoutPopup = document.createElement("div");
        layoutPopup.id = "layoutPopup";
        layoutPopup.className = "popup";
        layoutPopup.style.display = "none";
        var layoutContent = document.createElement("div");
        layoutContent.className = "popup-content";
        var nodeSep = document.createElement("input");
        nodeSep.min = "1";
        nodeSep.max = "200";
        nodeSep.value = "50";
        nodeSep.type = "range";
        nodeSep.id = "nodeSepInput";
        nodeSep.className = "slider";
        nodeSep.oninput = (e) => { nodeSpan.innerHTML = nodeSep.value; };
        var nodeP = document.createElement("p");
        nodeP.innerHTML = "Node Separation: ";
        var nodeSpan = document.createElement("span");
        nodeSpan.innerHTML = nodeSep.value;
        nodeP.appendChild(nodeSpan);
        var edgeSep = document.createElement("input");
        edgeSep.min = "1";
        edgeSep.max = "200";
        edgeSep.value = "50";
        edgeSep.type = "range";
        edgeSep.id = "edgeSepInput";
        edgeSep.className = "slider";
        edgeSep.oninput = (e) => { edgeSpan.innerHTML = edgeSep.value; };
        var edgeP = document.createElement("p");
        edgeP.innerHTML = "Edge Separation: ";
        var edgeSpan = document.createElement("span");
        edgeSpan.innerHTML = edgeSep.value;
        edgeP.appendChild(edgeSpan);
        var rankSep = document.createElement("input");
        rankSep.min = "1";
        rankSep.max = "200";
        rankSep.value = "50";
        rankSep.type = "range";
        rankSep.id = "rankSepInput";
        rankSep.className = "slider";
        rankSep.oninput = (e) => { rankSpan.innerHTML = rankSep.value; };
        var rankP = document.createElement("p");
        rankP.innerHTML = "Rank Separation: ";
        var rankSpan = document.createElement("span");
        rankSpan.innerHTML = rankSep.value;
        rankP.appendChild(rankSpan);
        var orientationP = document.createElement("p");
        orientationP.innerHTML = "Orientation: ";
        var selectDiv = document.createElement("div");
        selectDiv.className = "select";
        var layoutDir = document.createElement("select");
        layoutDir.id = "layoutDir";
        layoutDir.value = "LR";
        var dirOption1 = document.createElement("option");
        dirOption1.label = "Left-Right";
        dirOption1.value = "LR";
        dirOption1.selected = true;
        var dirOption2 = document.createElement("option");
        dirOption2.label = "Bottom-Top";
        dirOption2.value = "BT";
        var dirOption3 = document.createElement("option");
        dirOption3.label = "Top-Bottom";
        dirOption3.value = "TB";
        var dirOption4 = document.createElement("option");
        dirOption4.label = "Right-Left";
        dirOption4.value = "RL";
        layoutDir.append(dirOption1, dirOption2, dirOption3, dirOption4);
        selectDiv.appendChild(layoutDir);
        var confirmButton = document.createElement("button");
        confirmButton.className = "button button1";
        confirmButton.style.marginTop = "5px";
        confirmButton.innerHTML = "Set Layout!";
        confirmButton.addEventListener("click", (e) => this.resetLayout());
        layoutContent.append(orientationP, selectDiv, nodeP, nodeSep, edgeP, edgeSep, rankP, rankSep, confirmButton);
        layoutPopup.appendChild(layoutContent);
        // UPLOAD-POPUP
        var uploadPopup = document.createElement("div");
        uploadPopup.id = "uploadPopup";
        uploadPopup.className = "popup";
        uploadPopup.style.display = "none";
        var uploadPopupContent = document.createElement("div");
        uploadPopupContent.className = "popup-content";
        var fileInput = document.createElement("input");
        fileInput.className = "fileinput";
        fileInput.id = "fileInput";
        fileInput.type = "file";
        fileInput.accept = "application/JSON,.pnml";
        fileInput.style.display = "none";
        fileInput.addEventListener("change", (e) => this.showFileName());
        var label = document.createElement("label");
        label.htmlFor = "fileInput";
        label.className = "uploadLabel";
        label.textContent = "JSON or PNML-File...";
        var uploadJSON = document.createElement("button");
        uploadJSON.id = "uploadJSON";
        uploadJSON.className = "button button1";
        uploadJSON.textContent = "Import Graph!";
        uploadJSON.addEventListener("click", (e) => PetriView.importJSON());
        uploadPopupContent.append(label, fileInput, uploadJSON);
        uploadPopup.appendChild(uploadPopupContent);
        // LINK-POPUP
        var linkPopup = document.createElement("div");
        linkPopup.id = "linkPopup";
        linkPopup.className = "popup";
        linkPopup.style.display = "none";
        var linkInput = document.createElement("input");
        linkInput.placeholder = "Enter probability...";
        linkInput.id = "linkInput";
        linkInput.type = "number";
        linkInput.step = "0.01";
        linkInput.min = "0.00";
        linkInput.max = "1.00";
        linkInput.defaultValue = "1.00";
        var changeProb = document.createElement("button");
        changeProb.id = "changeProb";
        changeProb.className = "button button1";
        changeProb.addEventListener("click", (e) => PetriView.changeProb());
        changeProb.textContent = "Change Probability!";
        var linkPopupContent = document.createElement("div");
        linkPopupContent.className = "popup-content";
        linkPopupContent.append(linkInput, changeProb);
        linkPopup.appendChild(linkPopupContent);
        // LABEL-POPUP
        var popup = document.createElement("div");
        popup.id = "popup";
        popup.className = "popup";
        popup.style.display = "none";
        var headerText = document.createElement("p");
        headerText.textContent = "Label:";
        var input = document.createElement("input");
        input.placeholder = "Enter label...";
        input.id = "input";
        input.type = "text";
        input.oninput = this.enableLabelButton;
        var changeLabel = document.createElement("button");
        changeLabel.id = "changelabel";
        changeLabel.className = "button button1";
        changeLabel.addEventListener("click", (e) => PetriView.saveChanges());
        changeLabel.disabled = true;
        changeLabel.textContent = "Save!";
        var headerText1 = document.createElement("p");
        headerText1.id = "timeLabel";
        headerText1.textContent = "Duration in seconds:";
        headerText1.style.display = "none";
        var addTime = document.createElement("input");
        addTime.placeholder = "In seconds...";
        addTime.id = "timeInput";
        addTime.type = "number";
        addTime.min = "1";
        addTime.defaultValue = "1";
        addTime.style.display = "none";
        var popupContent = document.createElement("div");
        popupContent.className = "popup-content";
        popupContent.append(headerText, input, headerText1, addTime, changeLabel);
        popup.appendChild(popupContent);
        // CONDITION-POPUP
        var condPopup = document.createElement("div");
        condPopup.className = "popup";
        condPopup.id = "condPopup";
        condPopup.style.display = "none";
        var description = document.createElement("p");
        description.textContent = "Add conditions:";
        description.id = "descriptionID";
        var conditions = document.createElement("input");
        conditions.placeholder = "E.g.: costs > 500, ...";
        conditions.id = "conditionInput";
        var addConditions = document.createElement("button");
        addConditions.id = "addConditions";
        addConditions.className = "button button1";
        addConditions.textContent = "Add Conditions!";
        addConditions.addEventListener("click", (e) => PetriView.saveConditions());
        var condPopupContent = document.createElement("div");
        condPopupContent.className = "popup-content";
        condPopupContent.append(description, conditions, addConditions);
        condPopup.appendChild(condPopupContent);
        // SAVE-POPUP
        var savePopup = document.createElement("div");
        savePopup.id = "savePopup";
        savePopup.className = "popup";
        savePopup.style.display = "none";
        var savePopupContent = document.createElement("div");
        savePopupContent.className = "popup-content";
        var saveInput = document.createElement("input");
        saveInput.placeholder = "Enter graphname...";
        saveInput.id = "graphNameInput";
        saveInput.type = "text";
        saveInput.oninput = this.enableSaveButton;
        var saveGraphAs = document.createElement("button");
        saveGraphAs.id = "saveGraphAs";
        saveGraphAs.className = "button button1";
        saveGraphAs.addEventListener("click", (e) => PetriView.saveGraph());
        saveGraphAs.disabled = true;
        saveGraphAs.textContent = "Save Graph!";
        savePopupContent.append(saveInput, saveGraphAs);
        savePopup.appendChild(savePopupContent);
        // ADD EVERYTHING TO NOTEBOOK HTML CODE
        this.el.append(dropdown, saveGraph, importJSON, saveIMG, downloadJSON, zoomIn, zoomOut, addPlace, addTrans, addToken, removeToken, setLayout, clearAll, lockModel, simulate, stopSimulation, reloadSim, addAttrs);
        this.el.append(popup, linkPopup, savePopup, uploadPopup, downPopup, condPopup, attrPopup, layoutPopup);
        // Init paper, give it the respective ID, restrict its elements moving area and append it
        this.initWidget();
        PetriView.paper.el.id = "paper";
        PetriView.paper.options.restrictTranslate = function (cellView) { return cellView.paper.getArea(); };
        this.el.appendChild(PetriView.paper.el);
        // If clicked outside of any popup-form, do not display it anymore (under conditions)
        window.onclick = function (event) {
            if (PetriView.selectedCell) {
                if (event.target.className === "popup" && (PetriView.selectedCell.attributes.type != "customTransition" ||
                    PetriView.selectedCell.attributes.attrs["label"]["text"] != "")) {
                    event.target.style.display = "none";
                    $("#changelabel").prop("disabled", true);
                    PetriView.selectedCell = null;
                }
            } // to disable savegraph-popup:
            else if (event.target.className == "popup") {
                event.target.style.display = "none";
                document.getElementById("graphNameInput").value = "";
                $("#saveGraphAs").prop("disabled", true);
            }
        };
        // Click popup-buttons on keyboardinput "enter"
        document.addEventListener("keydown", function (e) {
            if (e.key == "Enter") {
                if (popup.style.display != "none" && !document.getElementById("changelabel").disabled) {
                    PetriView.saveChanges();
                }
                else if (savePopup.style.display != "none" && !document.getElementById("saveGraphAs").disabled) {
                    PetriView.saveGraph();
                }
                else if (uploadPopup.style.display != "none") {
                    PetriView.importJSON();
                }
                else if (condPopup.style.display != "none") {
                    PetriView.saveConditions();
                }
                else if (linkPopup.style.display != "none") {
                    PetriView.changeProb();
                }
            }
        });
        // Paper on-click, -doubleclick, -drag, -alt-drag and on-hover functionalities
        PetriView.paper.on({
            // while alt-key is pressed cell is locked and you can connect it by dragging with mouseclick
            // otherwise the cell stroke is simply colored red
            'cell:pointerdown': function (cellView, evt) {
                if (evt.altKey) {
                    jQuery('.joint-element').css("cursor", "crosshair");
                    evt.data = cellView.model.position();
                    this.findViewByModel(cellView.model).setInteractivity(false);
                }
                else {
                    jQuery('.joint-element').css("cursor", "move");
                }
                // Reset "old" selectedCell-stroke if slectedCell is not the same as cellView
                if (PetriView.selectedCell != null && PetriView.selectedCell != cellView.model) {
                    if (PetriView.selectedCell.attributes.type == "pn.Place") {
                        PetriView.selectedCell.attr({ ".root": { "stroke": "#7c68fc" } });
                    }
                    else {
                        PetriView.selectedCell.attr({ "body": { "stroke": "#7c68fc" } });
                    }
                }
                if (cellView.model.attributes.type == "pn.Place") {
                    cellView.model.attr({ ".root": { "stroke": (cellView.model.attributes.attrs[".root"]["stroke"] == "red") ? "#7c68fc" : "red" } });
                }
                else if (cellView.model.attributes.type == "customTransition") {
                    cellView.model.attr({ "body": { "stroke": (cellView.model.attributes.attrs["body"]["stroke"] == "red") ? "#7c68fc" : "red" } });
                }
                PetriView.selectedCell = cellView.model;
            },
            // if a blank part of paper is clicked, disselect the cell and set dragStartPosition
            'blank:pointerdown': function (evt, x, y) {
                PetriView.dragStartPosition = { x: x, y: y };
                if (PetriView.selectedCell) {
                    if (PetriView.selectedCell.attributes.type == "pn.Place") {
                        PetriView.selectedCell.attr({ ".root": { "stroke": "#7c68fc" } });
                    }
                    else {
                        PetriView.selectedCell.attr({ "body": { "stroke": "#7c68fc" } });
                    }
                    PetriView.selectedCell = null;
                }
            },
            // Reset dragStartPosition
            'blank:pointerup cell:pointerup': function () {
                PetriView.dragStartPosition = null;
            },
            // Make paper draggable (mind the scaling)
            'blank:pointermove element:pointermove': function (event) {
                if (document.querySelector('#lock').textContent == " Lock") {
                    if (PetriView.dragStartPosition) {
                        var scale = PetriView.paper.scale();
                        PetriView.paper.translate(event.offsetX - PetriView.dragStartPosition.x * scale.sx, event.offsetY - PetriView.dragStartPosition.y * scale.sy);
                    }
                }
            },
            // when mousebutton is lifted up while altkey is pressed a link is created between source and destination
            // if altkey is not pressed simply unlock the cell again (only if Lock-Button was not pressed)
            'cell:pointerup': function (cellView, evt, x, y) {
                jQuery('.joint-element').css("cursor", "move");
                if (document.querySelector('#lock').textContent == " Lock") {
                    this.findViewByModel(cellView.model).setInteractivity(true);
                }
                if (evt.altKey) {
                    var connect = true;
                    var coordinates = new joint.g.Point(x, y);
                    var elementAbove = cellView.model;
                    var elementBelow = this.model.findModelsFromPoint(coordinates).find(function (cell) {
                        return (cell.id !== elementAbove.id);
                    });
                    if (typeof (elementAbove) == 'undefined') {
                        PetriView.graph.getConnectedLinks(elementBelow).forEach(link => {
                            if (link.attributes.source.id == elementAbove.id) {
                                connect = false;
                            }
                        });
                    }
                    // If the two elements are connected in that direction already or have the same cell type, don't connect them (again).
                    if (elementBelow && (elementAbove.attributes.type != elementBelow.attributes.type) &&
                        (elementAbove.attributes.type != "pn.Link") && (elementBelow.attributes.type != "pn.Link") && connect) {
                        // Move the cell to the position before dragging and create a connection afterwards.
                        elementAbove.position(evt.data.x, evt.data.y);
                        PetriView.graph.addCell(PetriView.link(elementAbove, elementBelow));
                    }
                }
            },
            // Add small remove-options on hover above places and transitions
            'cell:mouseenter': (elementView) => {
                if (document.querySelector('#lock').textContent == " Lock") {
                    var x = "95%";
                    var y = "30%";
                    if (elementView.model.attributes.type == "customTransition") {
                        var x = "98%";
                        var y = "0%";
                    }
                    if (elementView.model.attributes.type != "pn.Link") {
                        elementView.addTools(new joint.dia.ToolsView({
                            tools: [
                                new joint.elementTools.Remove({
                                    useModelGeometry: true,
                                    x: x,
                                    y: y,
                                    action: function (evt) {
                                        if (elementView.model.attributes.type == "customTransition") {
                                            var transName = elementView.model.attributes.attrs["label"]["text"];
                                            PetriView.eventAttrs = PetriView.eventAttrs.filter(attr => attr.split(" -> ")[0] !== transName);
                                            PetriView.updateAttrsFrontend("eventAttrsList");
                                        }
                                        elementView.model.remove({ ui: true });
                                        PetriView.updateTransList();
                                    },
                                }),
                            ],
                        }));
                    }
                }
            },
            // remove small remove-options as soon as mouse leaves the cell
            'element:mouseleave': (elementView) => {
                elementView.removeTools();
            },
            // Allow changing the label upon doubleclicking a place or transition
            'cell:pointerdblclick': function () {
                if (PetriView.selectedCell.attributes.type == "pn.Link") {
                    PetriView.showPopup("linkPopup");
                }
                else if (PetriView.selectedCell.attributes.type == "pn.Place") {
                    document.getElementById("timeLabel").style.display = "none";
                    document.getElementById("timeInput").style.display = "none";
                    $("#changelabel").prop("disabled", false);
                    PetriView.showPopup("popup");
                }
                else if (PetriView.selectedCell.attributes.type == "customTransition" && PetriView.selectedCell.attributes.attrs["body"]["text"] != "") {
                    document.getElementById("timeLabel").style.display = "flex";
                    document.getElementById("timeInput").style.display = "flex";
                    document.getElementById("timeInput").value = PetriView.selectedCell.attributes.exectime;
                    $("#changelabel").prop("disabled", false);
                    PetriView.showPopup("popup");
                }
            },
            'element:port:remove': function (elementView, evt) {
                evt.stopPropagation();
                const portId = elementView.findAttribute('port', evt.target);
                const message = elementView.model;
                message.removePort(portId);
            },
            'element:port:add': function (elementView, evt) {
                evt.stopPropagation();
                if (PetriView.selectedCell) {
                    if (PetriView.selectedCell.attributes.type == "pn.Place") {
                        PetriView.selectedCell.attr({ ".root": { "stroke": "#7c68fc" } });
                    }
                    else {
                        PetriView.selectedCell.attr({ "body": { "stroke": "#7c68fc" } });
                    }
                }
                PetriView.selectedCell = elementView.model;
                if (elementView.model.attributes.attrs["portAddButton"]["fill"] != "lightgray") {
                    PetriView.showPopup("condPopup");
                }
            },
        });
        // UPDATE TYPESCRIPT FROM PYTHON: (alternatively on_some_change)
        this.model.on("change:graph", this.updateGraph, this);
        // UPDATING PYTHON BASED ON TYPESCRIPT
        PetriView.graph.on("change", this.updateGraph.bind(this), this);
        PetriView.graph.on('change:property', this.updateGraph.bind(this), this);
    }
    initWidget() {
        const namespace = joint.shapes;
        PetriView.graph = new joint.dia.Graph({ cellNamespace: namespace });
        PetriView.gridSize = 1;
        PetriView.selectedCell = null;
        PetriView.backupTokens = null;
        this.simulationId = 0;
        this.width = jQuery('#paper').width;
        this.height = jQuery('#paper').height;
        PetriView.paper = new joint.dia.Paper({
            el: document.createElement("div"),
            width: this.width,
            height: this.height,
            drawGrid: false,
            gridSize: PetriView.gridSize,
            defaultAnchor: { name: 'perpendicular' },
            defaultConnectionPoint: { name: 'boundary' },
            model: PetriView.graph,
            cellViewNamespace: namespace,
            linkPinning: false,
            snapLabels: true,
            interactive: {
                "linkMove": true,
                "labelMove": true,
                "arrowheadMove": false,
                "vertexMove": false,
                "vertexAdd": false,
                "vertexRemove": false,
                "useLinkTools": false
            }
        });
    }
    updateCaseAttrs() {
        this.model.set("caseAttrs", PetriView.caseAttrs);
        this.model.save_changes();
        this.model.sync("update", this.model);
    }
    updateGraph() {
        var allCells = PetriView.graph.getCells();
        // allCells.concat(PetriView.graph.getLinks());
        var res = [];
        allCells.forEach(function (cell) {
            if (cell.attributes.type == "pn.Place") {
                var id = cell.attributes.id;
                var name = cell.attributes.attrs[".label"]["text"];
                var tokens = cell.attributes.tokens;
                var type = "Place";
                res.push({ type, id, name, tokens });
            }
            else if (cell.attributes.type == "pn.Link") {
                var id = cell.attributes.id;
                var prob = Number(cell.attributes.labels[0]["attrs"]["text"]["text"]);
                var source = cell.attributes.source.id;
                var target = cell.attributes.target.id;
                var type = "Link";
                res.push({ type, id, prob, source, target });
            }
            else if (cell.attributes.type == "customTransition") {
                var id = cell.id;
                var name = cell.attributes.attrs["label"]["text"];
                var type = "Transition";
                var exectime = cell.attributes.exectime;
                var eventattrs = cell.attributes.eventAttrs;
                var conditions = [];
                cell.attributes.ports.items.forEach(function (item) {
                    conditions.push(item["attrs"]["portLabel"]["text"]);
                });
                res.push({ type, id, name, exectime, conditions, eventattrs });
            }
        });
        PetriView.updateTransList();
        this.model.set("graph", res);
        this.model.save_changes();
    }
    showFileName() {
        var file = $('#fileInput')[0].files[0].name;
        $('#fileInput').prev('label').text(file);
    }
    static zoomIt(delta) {
        var MIN_ZOOM = 0.2;
        var MAX_ZOOM = 3;
        var currentZoom = PetriView.paper.scale().sx;
        if (document.querySelector('#lock').textContent == " Lock") {
            var newZoom = currentZoom + 0.2 * delta;
            if (newZoom >= MIN_ZOOM && newZoom <= MAX_ZOOM) {
                // PetriView.paper.translate(0, 0);
                PetriView.paper.scale(newZoom, newZoom);
            }
        }
    }
    static getTokenlist(cells) {
        var tokenlist = [];
        cells.forEach(function (c) {
            if (c.attributes.type == "pn.Place") {
                tokenlist.push(c.get("tokens"));
            }
        });
        return tokenlist;
    }
    firstExample() {
        this.clearAll();
        // Define Places
        var pReady = new joint.shapes.pn.Place({
            position: { x: 140, y: 50 },
            attrs: {
                '.label': {
                    'text': 'ready',
                    'fill': '#7c68fc',
                    'font-size': 20,
                    'font-weight': 'bold'
                },
                '.root': {
                    'stroke': '#7c68fc',
                    'stroke-width': 3,
                },
                '.alot > text': {
                    'fill': '#fe854c',
                    'font-family': 'Courier New',
                    'font-size': 20,
                    'font-weight': 'bold',
                    'ref-x': 0.5,
                    'ref-y': 0.5,
                    'y-alignment': -0.5,
                    'transform': null
                },
                '.tokens > circle': {
                    'fill': '#7a7e9b'
                }
            },
            tokens: 1,
        });
        var pIdle = pReady.clone()
            .attr('.label/text', 'idle')
            .position(140, 260)
            .set('tokens', 2);
        var buffer = pReady.clone()
            .position(363, 150)
            .set('tokens', 12)
            .attr({
            '.label': {
                'text': 'buffer'
            },
        });
        var cAccepted = pReady.clone()
            .attr('.label/text', 'accepted')
            .position(600, 50)
            .set('tokens', 1);
        var cReady = pReady.clone()
            .attr('label/text', 'accepted')
            .position(600, 260)
            .set('ready', 3);
        // Define Transitions
        var tProduce = new customTrans_1.customTransition({
            position: { x: 20, y: 170 },
            attrs: {
                'label': {
                    'text': 'produce',
                    'fill': '#fe854f'
                },
            },
        });
        var tSend = tProduce.clone()
            .attr('label/text', 'send')
            .position(180, 170);
        var tAccept = tProduce.clone()
            .attr('label/text', 'accept')
            .position(485, 170);
        var tConsume = tProduce.clone()
            .attr('label/text', 'consume')
            .position(645, 170);
        // add cells to graph and create links
        PetriView.graph.addCell([pReady, pIdle, buffer, cAccepted, cReady, tProduce, tSend, tAccept, tConsume]);
        PetriView.graph.addCell([
            PetriView.link(tProduce, pReady), PetriView.link(pReady, tSend), PetriView.link(tSend, pIdle), PetriView.link(pIdle, tProduce),
            PetriView.link(tSend, buffer), PetriView.link(buffer, tAccept), PetriView.link(tAccept, cAccepted),
            PetriView.link(cAccepted, tConsume), PetriView.link(tConsume, cReady), PetriView.link(cReady, tAccept)
        ]);
        this.updateGraph();
        PetriView.backupTokens = PetriView.getTokenlist(PetriView.graph.getCells());
    }
    secondExample() {
        this.clearAll();
        var pA1 = new joint.shapes.pn.Place({
            position: { x: 50, y: 150 },
            attrs: {
                '.label': {
                    'text': 'A1',
                    'fill': '#7c68fc',
                    'font-size': 12,
                    'font-weight': 'bold'
                },
                '.root': {
                    'stroke': '#7c68fc',
                    'stroke-width': 3,
                },
                '.alot > text': {
                    'fill': '#fe854c',
                    'font-family': 'Courier New',
                    'font-size': 20,
                    'font-weight': 'bold',
                    'ref-x': 0.5,
                    'ref-y': 0.5,
                    'y-alignment': -0.5,
                    'transform': null
                },
                '.tokens > circle': {
                    'fill': '#7a7e9b',
                }
            },
            tokens: 1,
        });
        var pA2 = pA1.clone()
            .attr('.label/text', 'A2')
            .position(200, 150)
            .set('tokens', 0);
        var pConnector = pA1.clone()
            .position(350, 150)
            .attr({
            '.label': {
                'text': 'Connector'
            },
        });
        var pB1 = pA1.clone()
            .attr('.label/text', 'B1')
            .position(650, 150);
        var pB2 = pA1.clone()
            .position(500, 150)
            .set('tokens', 0)
            .attr('.label/text', 'B2');
        // Define Transitions
        var tA1 = new customTrans_1.customTransition({
            position: { x: 160, y: 30 },
            attrs: {
                'label': {
                    'fill': '#fe854f',
                    'text': "Transition A1"
                },
                'body': {
                    'fill': '#9586fd',
                    'stroke': '#7c68fc'
                },
            },
        });
        var tA2 = tA1.clone()
            .position(160, 300)
            .attr('label/text', 'Transition A2');
        var tB1 = tA1.clone()
            .position(460, 300)
            .attr('label/text', 'Transition B1');
        var tB2 = tA1.clone()
            .position(460, 30)
            .attr('label/text', 'Transition B2');
        // add cells to graph and create links
        PetriView.graph.addCell([pA1, pA2, pConnector, pB1, pB2, tA1, tA2, tB1, tB2]);
        PetriView.graph.addCell([
            PetriView.link(pA1, tA1), PetriView.link(tA1, pA2), PetriView.link(pA2, tA2), PetriView.link(tA2, pA1), PetriView.link(tA2, pConnector),
            PetriView.link(pConnector, tA1), PetriView.link(pConnector, tB1), PetriView.link(tB1, pB2), PetriView.link(pB2, tB2), PetriView.link(tB2, pConnector),
            PetriView.link(tB2, pB1), PetriView.link(pB1, tB1)
        ]);
        this.updateGraph();
        PetriView.backupTokens = PetriView.getTokenlist(PetriView.graph.getCells());
    }
    static link(a, b) {
        return new joint.shapes.pn.Link({
            source: { id: a.id, selector: '.root' },
            target: { id: b.id, selector: '.root' },
            // creates little jumps over other links
            connector: { name: 'jumpover',
                args: { size: 5 }
            },
            z: -1,
            attrs: {
                text: {
                    fill: '#000000',
                    fontSize: 10,
                    textAnchor: 'middle',
                    textVerticalAnchor: 'middle',
                    yAlignment: 'bottom',
                    pointerEvents: 'cell:pointerdblclick',
                    cursor: "move",
                },
                '.connection': {
                    'fill': 'none',
                    'stroke-linejoin': 'round',
                    'stroke-width': '2',
                    'stroke': '#4b4a67',
                },
                '.connection-wrap': {
                    'fill': 'none'
                },
            },
            // Hides the standard background-rect of the label
            defaultLabel: {
                markup: [{ tagName: 'text', selector: 'text' }],
                attrs: {
                    text: {
                        fill: '#000000',
                        fontSize: 10,
                        textAnchor: 'middle',
                        textVerticalAnchor: 'middle',
                        yAlignment: 'bottom',
                        pointerEvents: 'none'
                    }
                },
            },
            labels: [
                {
                    attrs: { text: { text: "1.00" } },
                    position: { args: { keepGradient: true, ensureLegibility: true } }
                }
            ]
        });
    }
    addToken() {
        try {
            if (PetriView.selectedCell.attributes.type != "pn.Place") {
                return "You cannot add tokens to transitions! Please select a place instead.";
                // console.log("You cannot add tokens to transitions! Please select a place instead.");
            }
            else {
                PetriView.selectedCell.set('tokens', PetriView.selectedCell.get('tokens') + 1);
                PetriView.backupTokens = PetriView.getTokenlist(PetriView.graph.getCells());
            }
        }
        catch (e) {
            return "Nothing selected! Please select a place before adding a token.";
        }
    }
    removeToken() {
        try {
            if (PetriView.selectedCell.attributes.type != "pn.Place") {
                return "You cannot remove tokens from transitions! Please select a place instead.";
            }
            else {
                if (PetriView.selectedCell.get('tokens') > 0) {
                    PetriView.selectedCell.set('tokens', PetriView.selectedCell.get('tokens') - 1);
                    PetriView.backupTokens = PetriView.getTokenlist(PetriView.graph.getCells());
                }
            }
        }
        catch (e) {
            return "Nothing selected! Please select a place before removing a token.";
        }
    }
    static showPopup(id) {
        var _a;
        document.getElementById(id).style.display = "flex";
        // set focus to first input-field in popup
        if (id != "layoutPopup" && id != "downloadPopup") {
            var inputField = (_a = document.getElementById(id)) === null || _a === void 0 ? void 0 : _a.getElementsByTagName("input")[0];
            document.getElementById(inputField.id).focus();
            // Set value of labelPopup-Input based on selected Link
            // slice creates a copy of last element --> so actually "labels" is not changed by "pop()"
            if (id == "linkPopup") {
                inputField.value = PetriView.selectedCell.attributes.labels.slice(-1).pop()["attrs"]["text"]["text"];
            }
        }
    }
    addPlace() {
        var x = PetriView.paper.paperToLocalPoint(0, 0).x + 20;
        var y = PetriView.paper.paperToLocalPoint(0, 0).y + 20;
        PetriView.graph.addCell(new joint.shapes.pn.Place({ attrs: { '.label': { 'text': '', 'fill': '#7c68fc' },
                '.root': { 'stroke': '#7c68fc', 'stroke-width': 3 },
                '.tokens > circle': { 'fill': '#7a7e9b' }, '.alot > text': {
                    'fill': '#fe854c',
                    'font-family': 'Courier New',
                    'font-size': 20,
                    'font-weight': 'bold',
                    'ref-x': 0.5,
                    'ref-y': 0.5,
                    'y-alignment': -0.5,
                    'transform': null
                }
            }, tokens: 0,
            position: { x: x, y: y } }));
        PetriView.backupTokens = PetriView.getTokenlist(PetriView.graph.getCells());
        this.updateGraph();
    }
    addTrans() {
        var x = PetriView.paper.paperToLocalPoint(0, 0).x + 90;
        var y = PetriView.paper.paperToLocalPoint(0, 0).y + 35;
        if (PetriView.selectedCell) {
            if (PetriView.selectedCell.attributes.type == "pn.Place") {
                PetriView.selectedCell.attr({ ".root": { "stroke": "#7c68fc" } });
            }
            else {
                PetriView.selectedCell.attr({ "body": { "stroke": "#7c68fc" } });
            }
        }
        PetriView.selectedCell = new customTrans_1.customTransition({
            position: { x: x, y: y }
        });
        PetriView.graph.addCell(PetriView.selectedCell);
        document.getElementById("timeLabel").style.display = "flex";
        document.getElementById("timeInput").style.display = "flex";
        PetriView.showPopup("popup");
        this.updateGraph();
    }
    resetLayout() {
        $("#layoutPopup").css("display", "none");
        var nodeSep = Number($("#nodeSepInput").prop("value"));
        var edgeSep = Number($("#edgeSepInput").prop("value"));
        var rankSep = Number($("#rankSepInput").prop("value"));
        var orientation = $("#layoutDir").prop("value");
        var options = { dagre: dagre_1.default, graphlib: graphlib_1.default, nodeSep: nodeSep, edgeSep: edgeSep,
            rankSep: rankSep, rankDir: orientation, setVertices: true, marginX: 20, marginY: 30 };
        joint.layout.DirectedGraph.layout(PetriView.graph, options);
    }
    clearAll() {
        // Reset Zoom and empty Graph
        PetriView.paper.translate(0, 0);
        PetriView.paper.scale(1, 1, 0, 0);
        PetriView.graph.clear();
        PetriView.updateTransList();
        this.updateGraph();
        // Delete all Event-Attributes!
        $("#eventAttrsList").empty();
        PetriView.eventAttrs = [];
    }
    simulate() {
        var transitions = [];
        for (const c of PetriView.graph.getCells()) {
            if (c.attributes.type == "customTransition") {
                transitions.push(c);
            }
        }
        // shuffle transitions to randomize which one is chosen first
        transitions = transitions.map((value) => ({ value, sort: Math.random() }))
            .sort((a, b) => a.sort - b.sort)
            .map(({ value }) => value);
        function fireTransition(t, sec) {
            var inbound = PetriView.graph.getConnectedLinks(t, { inbound: true });
            var outbound = PetriView.graph.getConnectedLinks(t, { outbound: true });
            var placesBefore = inbound.map(function (link) { return link.getSourceElement(); });
            var placesAfter = outbound.map(function (link) { return link.getTargetElement(); });
            var isFirable = true;
            // shuffle Places before to ensure it is random which places get checked first
            placesBefore = placesBefore.map((value) => ({ value, sort: Math.random() }))
                .sort((a, b) => a.sort - b.sort)
                .map(({ value }) => value);
            placesBefore.forEach(function (p) {
                if (p.get('tokens') === 0) {
                    isFirable = false;
                }
            });
            if (isFirable) {
                placesBefore.forEach(function (p) {
                    // Let the execution finish before adjusting the value of tokens. So that we can loop over all transitions
                    // and call fireTransition() on the original number of tokens. --> partially leads to negative tokens --> disabled for now
                    // setTimeout(function() {
                    //     p.set('tokens', p.get('tokens') - 1);
                    // }, 0);
                    p.set('tokens', p.get('tokens') - 1);
                    var links = inbound.filter(function (l) { return l.getSourceElement() === p; });
                    links.forEach(function (l) {
                        var token = joint.V('circle', { r: 5, fill: '#feb662' }).node;
                        l.findView(PetriView.paper).sendToken(token, sec * 1000);
                    });
                });
                placesAfter.forEach(function (p) {
                    var links = outbound.filter(function (l) { return l.getTargetElement() === p; });
                    links.forEach(function (l) {
                        var token = joint.V('circle', { r: 5, fill: '#feb662' }).node;
                        l.findView(PetriView.paper).sendToken(token, sec * 1000, function () {
                            p.set('tokens', p.get('tokens') + 1);
                        });
                    });
                });
            }
        }
        // if (Math.random() < 0.7)
        transitions.forEach(function (t) {
            fireTransition(t, 1);
        });
        this.simulationId = setInterval(function () {
            transitions.forEach(function (t) {
                fireTransition(t, 1);
            });
        }, 2000);
    }
    stopSimulation() {
        clearInterval(this.simulationId);
    }
    lockModel() {
        if (document.querySelector('#lock').textContent == " Lock") {
            document.querySelector('#lock').innerHTML = '<i class="fa fa-lock"></i>' + " Unlock";
            PetriView.paper.setInteractivity(function () { return false; });
            jQuery('.joint-element').css("cursor", "pointer");
            jQuery('.marker-arrowheads').css("cursor", "pointer");
            jQuery('.marker-vertices').css("cursor", "pointer");
            jQuery('.joint-link.joint-theme-dark .connection-wrap').css("cursor", "pointer");
        }
        else {
            document.querySelector('#lock').innerHTML = '<i class="fa fa-unlock"></i>' + " Lock";
            PetriView.paper.setInteractivity(function () { return true; });
        }
    }
    resetSim() {
        PetriView.paper.translate(0, 0);
        PetriView.paper.scale(1, 1, 0, 0);
        var i = 0;
        PetriView.graph.getCells().forEach(function (c) {
            if (c.attributes.type == "pn.Place") {
                c.set('tokens', PetriView.backupTokens[i]);
                i += 1;
            }
        });
    }
    static saveGraph() {
        document.getElementById("savePopup").style.display = "none";
        const fileName = document.getElementById("graphNameInput").value;
        const jsonstring = JSON.stringify(PetriView.graph.toJSON());
        localStorage.setItem(fileName, jsonstring);
        // Check for links existing with the same fileName and overwrite them
        if ($("a").filter(function () { return $(this).text() == fileName; }).length == 0) {
            var newLink = document.createElement("a");
            newLink.textContent = fileName;
            newLink.addEventListener("click", (e) => PetriView.unJSONify(fileName));
            document.getElementById("dropdown-content").appendChild(newLink);
        }
        // Reset the value of the graphNameInput-field and disable button again
        document.getElementById("graphNameInput").value = "";
        document.getElementById("saveGraphAs").disabled = true;
    }
    static parsePNML(xmlPnml) {
        var placePos = new Set();
        var transPos = new Set();
        for (let childId in xmlPnml.childNodes) {
            let child = xmlPnml.childNodes[childId];
            if (child.tagName == "net") {
                for (let child2Id in child.childNodes) {
                    let child2 = child.childNodes[child2Id];
                    if (child2.tagName == "caseattr") {
                        PetriView.caseAttrs.push(child2.getAttribute("label"));
                    }
                }
                PetriView.parsePNML(child);
            }
            else if (child.tagName == "page") {
                PetriView.parsePNML(child);
            }
            else {
                if (child.tagName == "place") {
                    let placeId = child.getAttribute("id");
                    var placeName = "";
                    var placeTokens = 0;
                    var xPos = 20;
                    var yPos = 25;
                    for (let child2Id in child.childNodes) {
                        let child2 = child.childNodes[child2Id];
                        if (child2.tagName == "name") {
                            for (let child3Id in child2.childNodes) {
                                let child3 = child2.childNodes[child3Id];
                                if (child3.tagName == "text") {
                                    placeName = child3.textContent;
                                }
                            }
                        }
                        else if (child2.tagName == "graphics") {
                            for (let child3Id in child2.childNodes) {
                                let child3 = child2.childNodes[child3Id];
                                if (child3.tagName == "position") {
                                    xPos = parseInt(child3.getAttribute("x")) * 10;
                                    yPos = parseInt(child3.getAttribute("y")) * 10;
                                }
                            }
                        }
                        else if (child2.tagName != null && child2.tagName.toLowerCase() == "initialmarking") {
                            for (let child3Id in child2.childNodes) {
                                let child3 = child2.childNodes[child3Id];
                                if (child3.tagName == "text") {
                                    placeTokens = parseInt(child3.textContent);
                                }
                            }
                        }
                    }
                    let newPlace = new joint.shapes.pn.Place({ attrs: { '.label': { 'text': placeName, 'fill': '#7c68fc' },
                            '.root': { 'stroke': '#7c68fc', 'stroke-width': 3 },
                            '.tokens > circle': { 'fill': '#7a7e9b' }, '.alot > text': {
                                'fill': '#fe854c',
                                'font-family': 'Courier New',
                                'font-size': 20,
                                'font-weight': 'bold',
                                'ref-x': 0.5,
                                'ref-y': 0.5,
                                'y-alignment': -0.5,
                                'transform': null
                            }
                        }, tokens: placeTokens,
                        position: { x: xPos, y: yPos },
                        id: placeId });
                    PetriView.graph.addCell(newPlace);
                    placePos.add(xPos).add(yPos);
                }
                else if (child.tagName == "transition") {
                    let transId = child.getAttribute("id");
                    var transLabel = transId;
                    var xPos = 20;
                    var yPos = 25;
                    var conditions = [];
                    var eventattrs = [];
                    for (let child2Id in child.childNodes) {
                        let child2 = child.childNodes[child2Id];
                        if (child2.tagName == "name") {
                            for (let child3Id in child2.childNodes) {
                                let child3 = child2.childNodes[child3Id];
                                if (child3.tagName == "text") {
                                    transLabel = child3.textContent;
                                }
                            }
                        }
                        else if (child2.tagName == "toolspecific") {
                            if (child2.getAttribute("tool") == "ipypetrinet") {
                                var exectime = child2.getAttribute("exectime");
                                for (let child3Id in child2.childNodes) {
                                    let child3 = child2.childNodes[child3Id];
                                    if (child3.tagName == "condition") {
                                        conditions.push(child3.getAttribute("label"));
                                    }
                                    else if (child3.tagName == "eventattr") {
                                        eventattrs.push(child3.getAttribute("label"));
                                    }
                                }
                            }
                        }
                        else if (child2.tagName == "graphics") {
                            for (let child3Id in child2.childNodes) {
                                let child3 = child2.childNodes[child3Id];
                                if (child3.tagName == "position") {
                                    xPos = parseInt(child3.getAttribute("x")) * 10;
                                    yPos = parseInt(child3.getAttribute("y")) * 10;
                                }
                            }
                        }
                    }
                    let newTrans = new customTrans_1.customTransition({
                        attrs: {
                            label: {
                                text: transLabel
                            }
                        },
                        exectime: exectime,
                        eventAttrs: eventattrs,
                        position: { x: xPos, y: yPos },
                        id: transId,
                    });
                    conditions.forEach((cond) => { newTrans.addDefaultPort(cond); });
                    PetriView.graph.addCell(newTrans);
                    transPos.add(xPos).add(yPos);
                }
                else if (child.tagName == "arc") {
                    // Dictonaries only to be able to use existing PetriView.link function
                    let arcSource = { id: child.getAttribute("source") };
                    let arcTarget = { id: child.getAttribute("target") };
                    var arcProb = "1.00";
                    for (let child2Id in child.childNodes) {
                        let child2 = child.childNodes[child2Id];
                        if (child2.tagName == "name") {
                            for (let child3Id in child2.childNodes) {
                                let child3 = child2.childNodes[child3Id];
                                if (child3.tagName == "text") {
                                    arcProb = child3.textContent;
                                }
                            }
                        }
                    }
                    var newLink = PetriView.link(arcSource, arcTarget);
                    newLink.attributes.labels.pop();
                    newLink.appendLabel({
                        attrs: { text: { text: arcProb } },
                        position: { distance: 0.5, args: { keepGradient: true, ensureLegibility: true } }
                    });
                    PetriView.graph.addCell(newLink);
                }
            }
        }
        PetriView.graph.getCells().forEach((cell) => {
        });
        // Check if auto-layout should apply (note that the method is called recursive, so != 0 is crucial)
        if ((placePos.size <= 2 && placePos.size != 0) || (transPos.size <= 2 && transPos.size != 0)) {
            joint.layout.DirectedGraph.layout(PetriView.graph, { dagre: dagre_1.default, graphlib: graphlib_1.default, setVertices: true, marginX: 20, marginY: 30 });
        }
    }
    static importJSON() {
        PetriView.paper.translate(0, 0);
        PetriView.paper.scale(1, 1, 0, 0);
        PetriView.showTab("caseTab");
        PetriView.eventAttrs = [];
        PetriView.updateAttrsFrontend("caseAttrsList");
        var files = document.getElementById("fileInput").files;
        if (files.length <= 0) {
            return false;
        }
        let fileType = files[0]["name"].split(".")[1];
        var reader = new FileReader();
        reader.onload = function (e) {
            if (fileType == "pnml") {
                PetriView.graph.clear();
                PetriView.caseAttrs = [];
                let parser = new DOMParser();
                var xmlDoc = parser.parseFromString(e.target.result, "text/xml");
                let xmlPnml = xmlDoc.getElementsByTagName("pnml")[0];
                PetriView.parsePNML(xmlPnml);
                PetriView.backupTokens = PetriView.getTokenlist(PetriView.graph.getCells());
                PetriView.updateAttrsFrontend("caseAttrsList");
            }
            else {
                var jsonstring = JSON.parse(e.target.result);
                PetriView.caseAttrs = jsonstring["caseAttributes"] ? jsonstring["caseAttributes"] : [];
                PetriView.updateAttrsFrontend("caseAttrsList");
                delete jsonstring["caseAttributes"];
                PetriView.graph.fromJSON(jsonstring);
                PetriView.backupTokens = PetriView.getTokenlist(PetriView.graph.getCells());
            }
            PetriView.graph.getCells().forEach(function (c) {
                if (c.attributes.type == "customTransition") {
                    // Just to trigger PetriView.graph.on("change", ...)
                    c.attr({ "body": { "stroke": "#7c68fc" } });
                    c.attributes.eventAttrs.forEach(function (event) {
                        PetriView.eventAttrs.push(c.attributes.attrs["label"]["text"] + " -> " + event);
                    });
                }
            });
            PetriView.updateAttrsFrontend("eventAttrsList");
            document.getElementById("uploadPopup").style.display = "none";
            var fileName = files[0]["name"].split(".")[0];
            // Check for links existing with the same fileName and overwrite them
            if ($("a").filter(function () { return $(this).text() == fileName; }).length == 0) {
                var newLink = document.createElement("a");
                newLink.textContent = fileName;
                if (fileType == "pnml") {
                    localStorage.setItem(fileName, JSON.stringify(PetriView.graph));
                    newLink.addEventListener("click", (e) => PetriView.unPNMLify(fileName));
                }
                else {
                    localStorage.setItem(fileName, e.target.result);
                    newLink.addEventListener("click", (e) => PetriView.unJSONify(fileName));
                }
                document.getElementById("dropdown-content").appendChild(newLink);
            }
        };
        reader.readAsText(files.item(0));
    }
    downloadPNML() {
        var pnmlString = '<?xml version="1.0" encoding="ISO-8859-1"?>\n\
                      <pnml>\
                        <net id="net" type="https://www.pnml.org">';
        PetriView.caseAttrs.forEach((caseAttr) => { pnmlString += ` <caseattr label='${caseAttr.replace("<", "&lt;").replace(">", "&gt;")}'/>`; });
        pnmlString += '<name>\
                     <text>PetriNet</text>\
                   </name>\
                   <page id="Page0">\
                     <name>\
                       <text/>\
                     </name>';
        PetriView.graph.getCells().forEach(function (cell) {
            if (cell.attributes.type == "pn.Place") {
                var id = cell.attributes.id;
                var name = cell.attributes.attrs[".label"]["text"];
                var tokens = cell.attributes.tokens;
                var width = cell.attributes.size["width"];
                var height = cell.attributes.size["height"];
                var x = cell.attributes.position["x"] / 10;
                var y = cell.attributes.position["y"] / 10;
                pnmlString += `<place id="${id}">\
                        <name>\
                          <text>${name}</text>\
                        </name>\
                        <toolspecific tool="ipypetrinet"/>\
                        <graphics>\
                          <position x="${x}" y="${y}"/>\
                          <dimension x="${width}" y="${height}"/>\
                        </graphics>\
                        <initialMarking>\
                          <text>${tokens}</text>\
                        </initialMarking>\
                      </place>`;
            }
            else if (cell.attributes.type == "customTransition") {
                var id = cell.id;
                var name = cell.attributes.attrs["label"]["text"];
                var width = cell.attributes.size["width"];
                var height = cell.attributes.size["height"];
                var x = cell.attributes.position["x"] / 10;
                var y = cell.attributes.position["y"] / 10;
                var exectime = cell.attributes.exectime;
                var eventattrs = cell.attributes.eventAttrs;
                var conditions = [];
                cell.attributes.ports.items.forEach(function (item) {
                    conditions.push(item["attrs"]["portLabel"]["text"].replace("<", "&lt;").replace(">", "&gt;"));
                });
                pnmlString += `<transition id="${id}">\
                        <name>\
                          <text>${name}</text>\
                        </name>\
                        <toolspecific tool="ipypetrinet" exectime="${exectime}">`;
                conditions.forEach((cond) => { pnmlString += ` <condition label='${cond}'/>`; });
                eventattrs.forEach((eventAttr) => { pnmlString += ` <eventattr label='${eventAttr.replace("<", "&lt;").replace(">", "&gt;")}'/>`; });
                pnmlString += `</toolspecific><graphics>\
                        <position x="${x}" y="${y}"/>\
                        <dimension x="${width}" y="${height}"/>\
                        <fill color="#9586fd"/>\
                      </graphics>\
                      </transition>`;
            }
        });
        PetriView.graph.getLinks().forEach(function (link) {
            var id = link.attributes.id;
            var prob = link.attributes.labels[0]["attrs"]["text"]["text"];
            var source = link.attributes.source.id;
            var target = link.attributes.target.id;
            pnmlString += `<arc id="${id}" source="${source}" target="${target}">\
                        <name>\
                          <text>${prob}</text>\
                        </name>\
                        <toolspecific tool="ipypetrinet"/>\
                        <arctype>\
                          <text>normal</text>\
                        </arctype>\
                      </arc>`;
        });
        pnmlString += `</page><finalmarkings><marking></marking></finalmarkings></net></pnml>`;
        let blob = new Blob([pnmlString], { type: 'data:.pnml;charset=utf-8' });
        let url = URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.setAttribute('download', 'PetriNet.pnml');
        a.setAttribute('href', url);
        a.setAttribute('target', '_blank');
        a.click();
        document.getElementById("DownloadPopup").style.display = "none";
    }
    downloadJSON() {
        var jsonstring = JSON.stringify(PetriView.graph.toJSON());
        if (jsonstring == null) {
            console.log("There is no JSON file to be saved.");
        }
        else {
            // Add Case-Attributes to String if not empty
            if (PetriView.caseAttrs) {
                var caseString = "";
                caseString += ',"caseAttributes":[';
                var i = 0;
                PetriView.caseAttrs.forEach(function (attr) {
                    caseString += '"' + attr + '"';
                    if (i < PetriView.caseAttrs.length - 1) {
                        caseString += ",";
                    }
                    else {
                        caseString += "]";
                    }
                });
                jsonstring = jsonstring.substring(0, jsonstring.length - 1) + caseString + "}";
            }
            let blob = new Blob([jsonstring], { type: 'data:text/json;charset=utf-8' });
            let url = URL.createObjectURL(blob);
            let a = document.createElement("a");
            a.setAttribute('download', 'graph.json');
            a.setAttribute('href', url);
            a.setAttribute('target', '_blank');
            a.click();
        }
        document.getElementById("DownloadPopup").style.display = "none";
    }
    static unPNMLify(fileName) {
        PetriView.graph.clear();
        const pnmlString = localStorage.getItem(fileName);
        PetriView.graph.fromJSON(JSON.parse(pnmlString));
        // let parser = new DOMParser();
        // var xmlDoc = parser.parseFromString(pnmlString, "text/xml");
        // let xmlPnml = xmlDoc.getElementsByTagName("pnml")[0];
        // PetriView.parsePNML(xmlPnml);
    }
    static unJSONify(fileName) {
        const jsonstring = localStorage.getItem(fileName);
        PetriView.graph.fromJSON(JSON.parse(jsonstring));
    }
    saveIMG() {
        // make sure the link-tools are disabled for a clean SVG
        $(".marker-arrowhead").css("display", "none");
        $(".tool-remove").css("display", "none");
        $(".tool-options").css("display", "none");
        $(".marker-vertices").css("display", "none");
        let svg = document.querySelector('svg');
        if (svg == null) {
            console.log("There is no SVG to be saved.");
        }
        else {
            let data = (new XMLSerializer()).serializeToString(svg);
            let blob = new Blob([data], { type: 'image/svg+xml;charset=utf-8' });
            let url = URL.createObjectURL(blob);
            let a = document.createElement('a');
            a.setAttribute('download', 'image.svg');
            a.setAttribute('href', url);
            a.setAttribute('target', '_blank');
            a.click();
        }
        // reenable certain options again
        $(".marker-arrowhead").css("display", "flex");
        $(".tool-remove").css("display", "flex");
        $(".marker-vertices").css("display", "flex");
    }
    enableLabelButton(input) {
        if (PetriView.selectedCell.attributes.type == "customTransition" && PetriView.selectedCell.attributes.attrs["label"]["text"] == "") {
            $("#changelabel").prop("disabled", !(document.getElementById("input").value));
        }
    }
    enableSaveButton(input) {
        $("#saveGraphAs").prop("disabled", !(document.getElementById("graphNameInput").value));
    }
    static saveChanges() {
        document.getElementById("popup").style.display = "none";
        var newLabel = document.getElementById("input").value;
        if (PetriView.selectedCell.attributes.type == "customTransition") {
            PetriView.selectedCell.attributes.exectime = document.getElementById("timeInput").value;
        }
        if (newLabel != "") {
            (PetriView.selectedCell.attributes.type == "pn.Place") ? PetriView.selectedCell.attr('.label/text', newLabel)
                : PetriView.selectedCell.attr('label/text', newLabel);
            document.getElementById("input").value = "";
            $("#changelabel").prop("disabled", true);
        }
    }
    static saveConditions() {
        document.getElementById("condPopup").style.display = "none";
        var input = document.getElementById("conditionInput");
        var conds = input.value.split(",");
        conds.forEach(function (c) {
            PetriView.selectedCell.addDefaultPort(c.trim());
        });
        input.value = "";
        PetriView.selectedCell = null;
    }
    addAttributes() {
        var attr = $("#attrName").val();
        var checked = $("input[name='dist']:checked").prop("id");
        var isEvtTab = document.getElementsByClassName("tablinks active")[0].id == "eventTab";
        if (isEvtTab) {
            var trans = document.getElementsByClassName("transListEl active")[0].getElementsByTagName("li")[0].innerHTML;
        }
        if (checked == "staticAttr") {
            var staticVal = $("#staticVal").val();
            var p = $("#staticProbs").val();
            (staticVal == "") ? staticVal = [] : [staticVal];
            if (p == "") {
                var str = `${attr}: np.random.choice([${staticVal}])`;
            }
            else {
                var str = `${attr}: np.random.choice([${staticVal}], p=[${p}])`;
            }
        }
        else if (checked == "normalDist") {
            var mue = $("#mue").val();
            var sigma = $("#sigma").val();
            (mue == "") ? mue = "1" : mue;
            (sigma == "") ? sigma = "0.5" : sigma;
            var str = `${attr}: np.random.normal(loc=${mue}, scale=${sigma})`;
        }
        else if (checked == "bernDist") {
            var n = $("#n").val();
            var p = $("#p").val();
            (n == "") ? n = "1" : n;
            (p == "") ? p = "0.5" : p;
            var str = `${attr}: np.random.binomial(n=${n}, p=${p})`;
        }
        else if (checked == "gammaDist") {
            var k = $("#k").val();
            var theta = $("#theta").val();
            (k == "") ? k = "9" : k;
            (theta == "") ? theta = "0.5" : theta;
            var str = `${attr}: np.random.gamma(shape=${k}, scale=${theta})`;
        }
        else if (checked == "expoDist") {
            var beta = $("#beta").val();
            (beta == "") ? beta = "3" : beta;
            var str = `${attr}: np.random.exponential(scale=${beta})`;
        }
        if (isEvtTab) {
            PetriView.eventAttrs.push(trans + " -> " + str);
            PetriView.updateGraphEventAttrs();
            PetriView.updateAttrsFrontend("eventAttrsList");
        }
        else {
            PetriView.caseAttrs.push(str);
            PetriView.updateAttrsFrontend("caseAttrsList");
        }
        this.updateGraph();
        PetriView.resetDistForms();
    }
    toggleFields(id) {
        $('#staticVal, #staticProbs, #mue, #sigma, #n, #p, #k, #theta, #beta').css("display", "none");
        this.enableAttributeButtons();
        if (id == "staticAttr") {
            $("#staticVal").css("display", "flex");
            $("#staticProbs").css("display", "flex");
        }
        else if (id == "normalDist") {
            $("#mue").css("display", "flex");
            $("#sigma").css("display", "flex");
        }
        else if (id == "bernDist") {
            $("#n").css("display", "flex");
            $("#p").css("display", "flex");
        }
        else if (id == "gammaDist") {
            $("#k").css("display", "flex");
            $("#theta").css("display", "flex");
        }
        else if (id == "expoDist") {
            $("#beta").css("display", "flex");
        }
    }
    enableAttributeButtons() {
        var radioChecked = $("input[name='dist']:checked").prop("id");
        // Do if EventTab is active
        if ($("#eventTab").prop("className") == "tablinks active") {
            var checkTrans = document.getElementsByClassName("transListEl active").length > 0;
            if (checkTrans && radioChecked && $("#attrName").prop("value")) {
                $("#addEventAttributes").prop("disabled", false);
            }
            else {
                $("#addEventAttributes").prop("disabled", true);
            }
            // Do if CaseTab is active
        }
        else {
            if (radioChecked && $("#attrName").prop("value")) {
                $("#addCaseAttributes").prop("disabled", false);
            }
            else {
                $("#addCaseAttributes").prop("disabled", true);
            }
        }
    }
    static updateAttrsFrontend(id) {
        var list = [];
        $(`#${id}`).empty();
        (id == "caseAttrsList") ? list = PetriView.caseAttrs : list = PetriView.eventAttrs;
        list.forEach(function (item) {
            var listEl = document.createElement("div");
            listEl.style.display = "flex";
            let li = document.createElement('li');
            li.innerHTML = item;
            var dismissButton = document.createElement("button");
            dismissButton.className = "dismissbutton";
            dismissButton.innerHTML = "<i class='fa fa-times-circle'></i>";
            dismissButton.addEventListener("click", (e) => PetriView.deleteListEl(id, item));
            listEl.append(dismissButton, li);
            document.getElementById(id).appendChild(listEl);
        });
    }
    static deleteListEl(id, content) {
        if (id == "caseAttrsList") {
            PetriView.caseAttrs.forEach(function (el, index) {
                if (content == el) {
                    PetriView.caseAttrs.splice(index, 1);
                }
            });
        }
        else {
            PetriView.eventAttrs.forEach(function (el, index) {
                if (content == el) {
                    PetriView.eventAttrs.splice(index, 1);
                }
            });
            PetriView.updateGraphEventAttrs();
        }
        PetriView.updateAttrsFrontend(id);
    }
    static updateGraphEventAttrs() {
        PetriView.graph.getCells().forEach(function (c) {
            if (c.attributes.type == "customTransition") {
                c.attributes.eventAttrs = [];
                PetriView.eventAttrs.forEach(function (item) {
                    var event = item.replace(": ", "=").split(" -> ");
                    if (event[0] == c.attributes.attrs["label"]["text"]) {
                        c.attributes.eventAttrs.push(event[1]);
                    }
                });
            }
        });
        PetriView.graph.set('cellNamespace', joint.shapes);
    }
    static resetDistForms() {
        document.getElementById("addCaseAttributes").disabled = true;
        document.getElementById("addEventAttributes").disabled = true;
        $("#attrName").prop("value", "");
        $("input[name=dist]").prop("checked", false);
        $("#staticVal, #staticProbs, #mue, #sigma, #n, #p, #k, #theta, #beta").css("display", "none");
        $("#staticVal, #staticProbs, #mue, #sigma, #n, #p, #k, #theta, #beta").prop("value", "");
    }
    static showTab(id) {
        PetriView.resetDistForms();
        $("#caseTab, #eventTab").prop("className", "tablinks");
        $("#caseTabContent, #eventTabContent").css("display", "none");
        if (id == "eventTab") {
            PetriView.updateTransList();
            $("#eventTabContent").css("display", "block");
            $("#eventTab").prop("className", "tablinks active");
        }
        else if (id == "caseTab") {
            $("#caseTabContent").css("display", "block");
            $("#caseTab").prop("className", "tablinks active");
        }
    }
    static updateTransList() {
        $("#transList").empty();
        var transitions = [];
        PetriView.graph.getCells().forEach(function (c) {
            if (c.attributes.type == "customTransition") {
                transitions.push(c.attributes.attrs["label"]["text"]);
            }
        });
        transitions.forEach(function (trans) {
            var listEl = document.createElement("div");
            listEl.className = "transListEl";
            listEl.style.display = "flex";
            listEl.style.cursor = "pointer";
            listEl.addEventListener("click", (e) => PetriView.selectTrans(listEl));
            let li = document.createElement('li');
            li.innerHTML = trans;
            var addEventAttrButton = document.createElement("button");
            addEventAttrButton.className = "dismissbutton";
            addEventAttrButton.innerHTML = "<i class='fa fa-plus-circle'></i>";
            listEl.append(addEventAttrButton, li);
            document.getElementById("transList").appendChild(listEl);
        });
        if (document.getElementById("transList").innerHTML.trim() == "") {
            document.getElementById("eventHeader").textContent = "Currently there are no transitions available.";
        }
        else {
            document.getElementById("eventHeader").textContent = "Select the transition to be linked:";
        }
    }
    static selectTrans(div) {
        var activeElements = Array.from(document.getElementsByClassName("transListEl active"));
        activeElements.forEach((el) => {
            el.style.backgroundColor = "white";
            el.className = "transListEl";
        });
        div.style.backgroundColor = "#DCDCDC";
        div.className = "transListEl active";
        // check if button should be enabled
        var checkTrans = document.getElementsByClassName("transListEl active").length > 0;
        var checkRadio = $("input[name='dist']:checked").prop("id");
        if (checkTrans && $("#attrName").val() != "" && checkRadio) {
            $("#addEventAttributes").prop("disabled", false);
        }
        else {
            $("#addEventAttributes").prop("disabled", true);
        }
    }
    static changeProb() {
        document.getElementById("linkPopup").style.display = "none";
        var inputEl = document.getElementById("linkInput");
        PetriView.selectedCell.attributes.labels.pop();
        PetriView.selectedCell.appendLabel({
            attrs: { text: { text: inputEl.value } },
            position: { distance: 0.5, args: { keepGradient: true, ensureLegibility: true } }
        });
    }
}
exports.PetriView = PetriView;
PetriView.caseAttrs = [];
PetriView.eventAttrs = [];
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, "/*\nA complete list of SVG properties that can be set through CSS is here:\nhttp://www.w3.org/TR/SVG/styling.html\n\nImportant note: Presentation attributes have a lower precedence over CSS style rules.\n*/\n\n/* Own CSS-Styles by me */\n/* Style everything button related */\n.button {\n  border: none;\n  color: white;\n  padding: 8px 18px;\n  text-align: center;\n  text-decoration: none;\n  display: inline-block;\n  font-size: 14px;\n  margin: 2px 1px;\n  cursor: pointer;\n  background-color: unset;\n}\n.button1 {background-color: #7c68fc;}\n.button2 {background-color: #303030;}\n\n/* On click button styling */\n.button:active {\n  position: relative;\n  top: 1px;\n}\n\n/* Darker background on mouse-over */\n.button1:hover { background-color: #6656d1; }\n.button2:hover { background-color: #fe854f; } /* Alternativ darkorange? */\n\n.button:disabled {\n  opacity: 0.4;\n}\n\n.dismissbutton {\n  border: none;\n  font-size: 20px;\n  color: #7c68fc;\n  background-color: inherit;\n  cursor: pointer;\n}\n\n.tab button {\n  background-color: whitesmoke;\n  float: left;\n  border: 1px solid black;\n  color: black;\n  outline: none;\n  cursor: pointer;\n  margin-right: 2px;\n  margin-bottom: 10px;\n}\n\n.tab button:hover { background-color: darkgray; }\n.tab button.active { background-color: darkgray; }\n\n/* Hide bullet points in list */\nul, li {\n  align-items: center;\n  list-style-type: none;\n  padding: 0;\n  padding-top: 2px;\n}\n\n/* Style input field */\ninput {\n  padding: 15px;\n  width: 100%;\n  margin: 8px 0;\n  box-sizing: border-box;\n  box-shadow: 0 0 15px 4px rgba(0,0,0,0.06);\n}\n\ninput:focus {\n  outline: none;\n  border: 2px solid #555;\n}\n\ninput[type=radio],\ninput.radio {\n  padding: 0px;\n  margin: 4px;\n  /* clear: none; */\n  /* box-sizing: auto; */\n  width: auto;\n}\n\n.uploadLabel {\n  padding: 15px;\n  background-color: whitesmoke;\n  border: 1px solid gray;\n  color: black;\n}\n\n.uploadLabel:hover {\n  border: 1px solid black;\n  cursor: pointer;\n}\n\n/* CSS for PopUp-Form */\n.popup {\n  display: none;       /* Hidden by default */\n  position: absolute;  /* Center in parental div */\n  z-index: 10;         /* Sit on top */\n  justify-content: center; /* Center childs */\n  align-items: center;     /* Center childs */\n  left: 0;\n  top: 0;\n  width: 100%;         /* Full width */\n  height: 100%;        /* Full height */\n  overflow: auto;      /* Enable scroll if needed */\n  background-color: rgb(0,0,0);       /* Fallback color */\n  background-color: rgba(0,0,0,0.4);  /* Black w/ opacity */\n}\n\n/* CSS for PopUp-Content */\n.popup-content {\n  background-color: #fefefe;\n  justify-content: center;\n  align-items: center;\n  margin: auto;\n  padding: 25px;\n  border: 2px solid #888;\n  border-radius: 4px;\n  width: 25%;\n}\n\n.attributes {\n  width: 50%;\n}\n\n/* The container <div> - needed to position the dropdown content */\n.dropdown {\n  position: relative;\n  display: inline-block;\n}\n\n/* Dropdown Content (Hidden by Default) */\n.dropdown-content {\n  display: none;\n  position: absolute;\n  background-color: #f1f1f1;\n  min-width: 160px;\n  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);\n  z-index: 1;\n}\n\n/* Links inside the dropdown */\n.dropdown-content a {\n  color: black;\n  padding: 12px 16px;\n  text-decoration: none;\n  display: block;\n  cursor: pointer;\n}\n\n/* Change color of dropdown links on hover */\n.dropdown-content a:hover {background-color: #ddd;}\n.dropdown-content a:active {    \n  position: relative;\n  top: 1px;\n}\n\n/* Show the dropdown menu on hover */\n.dropdown:hover .dropdown-content {display: block;}\n\n/* SLIDER */\n.slider {\n  -webkit-appearance: none;\n  width: 100%;\n  height: 5px;\n  padding: 0px;\n  border-radius: 3px;\n  background: #d3d3d3;\n  outline: none;\n  opacity: 0.7;\n  -webkit-transition: .2s;\n  transition: opacity .2s;\n}\n\n.slider:hover {\n  opacity: 1;\n}\n\n.slider::-webkit-slider-thumb {\n  -webkit-appearance: none;\n  appearance: none;\n  width: 15px;\n  height: 15px;\n  border-radius: 50%;\n  background: #7c68fc;\n  cursor: pointer;\n}\n\n.slider::-moz-range-thumb {\n  width: 15px;\n  height: 15px;\n  border-radius: 50%;\n  background: #7c68fc;\n  cursor: pointer;\n}\n\n/* CUSTOM SELECT */\n/* A reset of styles, including removing the default dropdown arrow */\nselect {\n  -moz-appearance: none;\n  -webkit-appearance: none;\n  appearance: none;\n  border-radius: 3px;\n  border-color: #d3d3d3;\n  cursor: pointer;\n  line-height: 1.5;\n  padding-left: 5px;\n  width: 100%;\n  margin-bottom: 5px;\n}\n\n.select {\n  position: relative;\n  width: 100%;\n  margin-bottom: 5px;\n}\n\n.select::before {\n  color: #0000;\n  font-size: 20px;\n  pointer-events: none;\n  position: absolute;\n  right: 15px;\n  top: 10px;\n}\n\n/* Style the arrow inside the select element: */\n.select::after {\n  position: absolute;\n  content: \"\";\n  top: 9px;\n  right: 10px;\n  border: 6px solid transparent;\n  border-color: #000000 transparent transparent transparent;\n}\n\n/* Style the paper where the graph is rendered on */\n#paper {\n  position: relative;\n  background-color: whitesmoke;\n  border: 2px solid grey;\n  resize: vertical;\n  width: auto;\n  height: 400px;\n  overflow: hidden;\n  display: flex;\n}\n\n/* THIS WAS ALREADY GIVEN (exeption: transform: scale() was added in some places by myself) */\n/* .viewport is a <g> node wrapping all diagram elements in the paper */\n.joint-viewport {\n -webkit-user-select: none;\n -moz-user-select: none;\n user-select: none;\n}\n\n.joint-paper > svg,\n.joint-paper-background {\n  transform: scale(0.98);\n  max-width: 100%;\n  max-height: 100%;\n}\n.joint-paper-grid {\n  position: absolute;\n  transform: scale(0.98);\n  max-width: 100%;\n  max-height: 100%;\n  top: 0;\n  left: 0;\n  right: 0;\n  bottom: 0;\n}\n\n/*\n1. IE can't handle paths without the `d` attribute for bounding box calculation\n2. IE can't even handle 'd' attribute as a css selector (e.g path[d]) so the following rule will\n break the links rendering.\n\npath:not([d]) {\n  display: none;\n}\n\n*/\n\n\n/* magnet is an element that can be either source or a target of a link */\n[magnet=true]:not(.joint-element) {\n cursor: crosshair;\n}\n[magnet=true]:not(.joint-element):hover {\n opacity: .7;\n}\n\n/*\n\nElements have CSS classes named by their types. E.g. type: basic.Rect has a CSS class \"element basic Rect\".\nThis makes it possible to easilly style elements in CSS and have generic CSS rules applying to\nthe whole group of elements. Each plugin can provide its own stylesheet.\n\n*/\n\n.joint-element {\n /* Give the user a hint that he can drag&drop the element. */\n cursor: move;\n}\n\n.joint-element * {\n user-drag: none;\n}\n\n.joint-element .scalable * {\n /* The default behavior when scaling an element is not to scale the stroke in order to prevent the ugly effect of stroke with different proportions. */\n vector-effect: non-scaling-stroke;\n}\n/*\n\nconnection-wrap is a <path> element of the joint.dia.Link that follows the .connection <path> of that link.\nIn other words, the `d` attribute of the .connection-wrap contains the same data as the `d` attribute of the\n.connection <path>. The advantage of using .connection-wrap is to be able to catch pointer events\nin the neighborhood of the .connection <path>. This is especially handy if the .connection <path> is\nvery thin.\n\n*/\n\n.marker-source,\n.marker-target {\n /* This makes the arrowheads point to the border of objects even though the transform: scale() is applied on them. */\n vector-effect: non-scaling-stroke;\n}\n\n/* Paper */\n.joint-paper {\n  position: relative;\n}\n/* Paper */\n\n/*  Highlighting  */\n.joint-highlight-opacity {\n  opacity: 0.3;\n}\n/*  Highlighting  */\n\n/*\n\nVertex markers are `<circle>` elements that appear at connection vertex positions.\n\n*/\n\n.joint-link .connection-wrap,\n.joint-link .connection {\n fill: none;\n}\n\n/* <g> element wrapping .marker-vertex-group. */\n.marker-vertices {\n opacity: 0;\n cursor: move;\n}\n.marker-arrowheads {\n opacity: 0;\n cursor: move;\n cursor: -webkit-grab;\n cursor: -moz-grab;\n/*   display: none;   */   /* setting `display: none` on .marker-arrowheads effectivelly switches of links reconnecting */\n}\n.link-tools {\n opacity: 0;\n cursor: pointer;\n}\n.link-tools .tool-options {\n display: none;       /* by default, we don't display link options tool */\n}\n.joint-link:hover .marker-vertices,\n.joint-link:hover .marker-arrowheads,\n.joint-link:hover .link-tools {\n opacity: 1;\n}\n\n/* <circle> element used to remove a vertex */\n.marker-vertex-remove {\n cursor: pointer;\n opacity: .1;\n}\n\n.marker-vertex-group:hover .marker-vertex-remove {\n opacity: 1;\n}\n\n.marker-vertex-remove-area {\n opacity: .1;\n cursor: pointer;\n}\n.marker-vertex-group:hover .marker-vertex-remove-area {\n opacity: 1;\n}\n\n/*\nExample of custom changes (in pure CSS only!):\n\nDo not show marker vertices at all:  .marker-vertices { display: none; }\nDo not allow adding new vertices: .connection-wrap { pointer-events: none; }\n*/\n\n/* foreignObject inside the elements (i.e joint.shapes.basic.TextBlock) */\n.joint-element .fobj {\n  overflow: hidden;\n}\n.joint-element .fobj body {\n  background-color: transparent;\n  margin: 0px;\n  position: static;\n}\n.joint-element .fobj div {\n  text-align: center;\n  vertical-align: middle;\n  display: table-cell;\n  padding: 0px 5px 0px 5px;\n}\n\n/* Paper */\n.joint-paper.joint-theme-dark {\n  background-color: #18191b;\n}\n/* Paper */\n\n/*  Links  */\n.joint-link.joint-theme-dark .connection-wrap {\n  stroke: #8F8FF3;\n  stroke-width: 15;\n  stroke-linecap: round;\n  stroke-linejoin: round;\n  opacity: 0;\n  cursor: move;\n}\n.joint-link.joint-theme-dark .connection-wrap:hover {\n  opacity: .4;\n  stroke-opacity: .4;\n}\n.joint-link.joint-theme-dark .connection {\n  stroke-linejoin: round;\n}\n.joint-link.joint-theme-dark .link-tools .tool-remove circle {\n  fill: #F33636;\n}\n.joint-link.joint-theme-dark .link-tools .tool-remove path {\n  fill: white;\n}\n.joint-link.joint-theme-dark .link-tools [event=\"link:options\"] circle {\n  fill: green;\n}\n/* <circle> element inside .marker-vertex-group <g> element */\n.joint-link.joint-theme-dark .marker-vertex {\n  fill: #5652DB;\n}\n.joint-link.joint-theme-dark .marker-vertex:hover {\n  fill: #8E8CE1;\n  stroke: none;\n}\n.joint-link.joint-theme-dark .marker-arrowhead {\n  fill: #5652DB;\n}\n.joint-link.joint-theme-dark .marker-arrowhead:hover {\n  fill: #8E8CE1;\n  stroke: none;\n}\n/* <circle> element used to remove a vertex */\n.joint-link.joint-theme-dark .marker-vertex-remove-area {\n  fill: green;\n  stroke: darkgreen;\n}\n.joint-link.joint-theme-dark .marker-vertex-remove {\n  fill: white;\n  stroke: white;\n}\n/*  Links  */\n/* Paper */\n.joint-paper.joint-theme-default {\n  background-color: #FFFFFF;\n}\n/* Paper */\n\n/*  Links  */\n.joint-link.joint-theme-default .connection-wrap {\n  stroke: #000000;\n  stroke-width: 15;\n  stroke-linecap: round;\n  stroke-linejoin: round;\n  opacity: 0;\n  cursor: move;\n}\n.joint-link.joint-theme-default .connection-wrap:hover {\n  opacity: .4;\n  stroke-opacity: .4;\n}\n.joint-link.joint-theme-default .connection {\n  stroke-linejoin: round;\n}\n.joint-link.joint-theme-default .link-tools .tool-remove circle {\n  fill: #FF0000;\n}\n.joint-link.joint-theme-default .link-tools .tool-remove path {\n  fill: #FFFFFF;\n}\n\n/* <circle> element inside .marker-vertex-group <g> element */\n.joint-link.joint-theme-default .marker-vertex {\n  fill: #1ABC9C;\n}\n.joint-link.joint-theme-default .marker-vertex:hover {\n  fill: #34495E;\n  stroke: none;\n}\n\n.joint-link.joint-theme-default .marker-arrowhead {\n  fill: #1ABC9C;\n}\n.joint-link.joint-theme-default .marker-arrowhead:hover {\n  fill: #F39C12;\n  stroke: none;\n}\n\n/* <circle> element used to remove a vertex */\n.joint-link.joint-theme-default .marker-vertex-remove {\n  fill: #FFFFFF;\n}\n/*  Links  */\n\n@font-face {\n  font-family: 'lato-light';\n  src: url(data:application/font-woff;charset=utf-8;base64,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) format('woff');\n  font-weight: normal;\n  font-style: normal;\n}\n\n/*  Links  */\n.joint-link.joint-theme-material .connection-wrap {\n  stroke: #000000;\n  stroke-width: 15;\n  stroke-linecap: round;\n  stroke-linejoin: round;\n  opacity: 0;\n  cursor: move;\n}\n.joint-link.joint-theme-material .connection-wrap:hover {\n  opacity: .4;\n  stroke-opacity: .4;\n}\n.joint-link.joint-theme-material .connection {\n  stroke-linejoin: round;\n}\n.joint-link.joint-theme-material .link-tools .tool-remove circle {\n  fill: #C64242;\n}\n.joint-link.joint-theme-material .link-tools .tool-remove path {\n  fill: #FFFFFF;\n}\n\n/* <circle> element inside .marker-vertex-group <g> element */\n.joint-link.joint-theme-material .marker-vertex {\n  fill: #d0d8e8;\n}\n.joint-link.joint-theme-material .marker-vertex:hover {\n  fill: #5fa9ee;\n  stroke: none;\n}\n\n.joint-link.joint-theme-material .marker-arrowhead {\n  fill: #d0d8e8;\n}\n.joint-link.joint-theme-material .marker-arrowhead:hover {\n  fill: #5fa9ee;\n  stroke: none;\n}\n\n/* <circle> element used to remove a vertex */\n.joint-link.joint-theme-material .marker-vertex-remove-area {\n  fill: #5fa9ee;\n}\n.joint-link.joint-theme-material .marker-vertex-remove {\n  fill: white;\n}\n/*  Links  */\n\n/*  Links  */\n.joint-link.joint-theme-modern .connection-wrap {\n  stroke: #000000;\n  stroke-width: 15;\n  stroke-linecap: round;\n  stroke-linejoin: round;\n  opacity: 0;\n  cursor: move;\n}\n.joint-link.joint-theme-modern .connection-wrap:hover {\n  opacity: .4;\n  stroke-opacity: .4;\n}\n.joint-link.joint-theme-modern .connection {\n  stroke-linejoin: round;\n}\n.joint-link.joint-theme-modern .link-tools .tool-remove circle {\n  fill: #FF0000;\n}\n.joint-link.joint-theme-modern .link-tools .tool-remove path {\n  fill: #FFFFFF;\n}\n\n/* <circle> element inside .marker-vertex-group <g> element */\n.joint-link.joint-theme-modern .marker-vertex {\n  fill: #1ABC9C;\n}\n.joint-link.joint-theme-modern .marker-vertex:hover {\n  fill: #34495E;\n  stroke: none;\n}\n\n.joint-link.joint-theme-modern .marker-arrowhead {\n  fill: #1ABC9C;\n}\n.joint-link.joint-theme-modern .marker-arrowhead:hover {\n  fill: #F39C12;\n  stroke: none;\n}\n\n/* <circle> element used to remove a vertex */\n.joint-link.joint-theme-modern .marker-vertex-remove {\n  fill: white;\n}\n/*  Links  */\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"ipypetrinet","version":"1.2.0","description":"A custom petrinet widget.","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/LordHeImchen/ipypetrinet","bugs":{"url":"https://github.com/LordHeImchen/ipypetrinet/issues"},"license":"BSD-3-Clause","author":{"name":"Jakob Bucksch","email":"jakob.bucksch@dfki.de"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/LordHeImchen/ipypetrinet"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipypetrinet/labextension","clean:nbextension":"rimraf ipypetrinet/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","@types/filesystem":"^0.0.32","@types/react":"^17.0.37","fs":"^0.0.1-security","graphlib":"^2.1.8","jointjs":"^3.4.4"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/dagre":"^0.7.47","@types/graphlib":"^2.1.8","@types/jest":"^26.0.0","@types/node":"^16.11.11","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","dagre":"^0.8.5","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.0.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipypetrinet/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.a0d8d9492615002f5afb.js.map