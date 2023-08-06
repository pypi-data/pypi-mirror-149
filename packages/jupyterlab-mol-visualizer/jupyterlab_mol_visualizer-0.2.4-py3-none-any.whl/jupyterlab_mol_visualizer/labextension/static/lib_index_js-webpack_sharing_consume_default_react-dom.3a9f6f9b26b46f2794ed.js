"use strict";
(self["webpackChunkjupyterlab_mol_visualizer"] = self["webpackChunkjupyterlab_mol_visualizer"] || []).push([["lib_index_js-webpack_sharing_consume_default_react-dom"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__);





/**
 * The command IDs used by the react-widget plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = 'create-react-widget';
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the react-widget extension.
 */
const extension = {
    id: 'react-widget',
    autoStart: true,
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__.ILauncher, _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_3__.IFileBrowserFactory],
    activate: (app, launcher, browserFactory) => {
        const { commands } = app;
        const command = CommandIDs.create;
        commands.addCommand(command, {
            caption: 'Create a new React Widget',
            label: 'MOL Visualizer',
            icon: args => _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_2__.reactIcon,
            execute: () => {
                const content = new _widget__WEBPACK_IMPORTED_MODULE_4__.CounterWidget(browserFactory);
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content });
                widget.title.label = 'MOL Visualizer';
                app.shell.add(widget, 'main');
            }
        });
        if (launcher) {
            launcher.add({
                command
            });
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (extension);


/***/ }),

/***/ "./lib/inputs.js":
/*!***********************!*\
  !*** ./lib/inputs.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ Inputs)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/core/esm/styles/makeStyles.js");
/* harmony import */ var _material_ui_core_Paper__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @material-ui/core/Paper */ "./node_modules/@material-ui/core/esm/Paper/Paper.js");
/* harmony import */ var _material_ui_core_Divider__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @material-ui/core/Divider */ "./node_modules/@material-ui/core/esm/Divider/Divider.js");
/* harmony import */ var _material_ui_core_IconButton__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @material-ui/core/IconButton */ "./node_modules/@material-ui/core/esm/IconButton/IconButton.js");
/* harmony import */ var _material_ui_icons_Search__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @material-ui/icons/Search */ "./node_modules/@material-ui/icons/Search.js");
/* harmony import */ var _material_ui_lab_Autocomplete__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @material-ui/lab/Autocomplete */ "./node_modules/@material-ui/lab/esm/Autocomplete/Autocomplete.js");
/* harmony import */ var _material_ui_core_TextField__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @material-ui/core/TextField */ "./node_modules/@material-ui/core/esm/TextField/TextField.js");








const useStyles = (0,_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_1__["default"])(theme => ({
    root: {
        padding: '2px 4px',
        display: 'flex',
        alignItems: 'center',
        width: 250,
        height: 30
    },
    input: {
        marginLeft: theme.spacing(1),
        flex: 1
    },
    iconButton: {
        padding: 10
    },
    divider: {
        height: 28,
        margin: 4
    }
}));
function Inputs(Props) {
    const classes = useStyles();
    const [value, setValue] = react__WEBPACK_IMPORTED_MODULE_0___default().useState(Props.options[0]);
    const [inputValue, setInputValue] = react__WEBPACK_IMPORTED_MODULE_0___default().useState('');
    const [files, setFiles] = react__WEBPACK_IMPORTED_MODULE_0___default().useState(Props.options);
    const handerClick = () => {
        Props.inputHandler(value);
    };
    Props.factory.defaultBrowser.model.pathChanged.connect((value) => {
        console.log('The path is changed: OK');
        const f = Props.getFiles(Props.types);
        setFiles(f);
        setValue(f[0]);
    });
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Paper__WEBPACK_IMPORTED_MODULE_2__["default"], { component: "form", className: classes.root },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_lab_Autocomplete__WEBPACK_IMPORTED_MODULE_3__["default"], { value: value, onChange: (event, newValue) => {
                setValue(newValue);
            }, inputValue: inputValue, onInputChange: (event, newInputValue) => {
                setInputValue(newInputValue);
            }, id: "controllable-states-demo", options: files, style: { width: 300 }, renderInput: params => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_TextField__WEBPACK_IMPORTED_MODULE_4__["default"], { ...params, label: Props.label, variant: "outlined" })) }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Divider__WEBPACK_IMPORTED_MODULE_5__["default"], { className: classes.divider, orientation: "vertical" }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_IconButton__WEBPACK_IMPORTED_MODULE_6__["default"], { color: "primary", className: classes.iconButton, "aria-label": "directions", onClick: handerClick },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_icons_Search__WEBPACK_IMPORTED_MODULE_7__["default"], null))));
}


/***/ }),

/***/ "./lib/sliders.js":
/*!************************!*\
  !*** ./lib/sliders.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ VerticalSlider)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/core/esm/styles/makeStyles.js");
/* harmony import */ var _material_ui_core_Slider__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @material-ui/core/Slider */ "./node_modules/@material-ui/core/esm/Slider/Slider.js");
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/core/esm/styles/createTheme.js");
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/styles/esm/ThemeProvider/ThemeProvider.js");
/* harmony import */ var _material_ui_core_CssBaseline__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @material-ui/core/CssBaseline */ "./node_modules/@material-ui/core/esm/CssBaseline/CssBaseline.js");
/* harmony import */ var _material_ui_core_Box__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @material-ui/core/Box */ "./node_modules/@material-ui/core/esm/Box/Box.js");
/* harmony import */ var _material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @material-ui/core/Grid */ "./node_modules/@material-ui/core/esm/Grid/Grid.js");
/* harmony import */ var _material_ui_core_useMediaQuery__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @material-ui/core/useMediaQuery */ "./node_modules/@material-ui/core/esm/useMediaQuery/useMediaQuery.js");








function VerticalSlider(Props) {
    const useStyles = (0,_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_1__["default"])({
        root: {
            flexGrow: 1,
            marginTop: '40px',
            width: '900px',
            margin: '0 auto'
        }
    });
    function valuetext(value) {
        return `${value}°C`;
    }
    const marks2 = [
        {
            value: -0.04,
            label: '-0.04'
        },
        {
            value: -0.02,
            label: '-0.02'
        },
        {
            value: 0,
            label: '0'
        },
        {
            value: 0.02,
            label: '0.02'
        },
        {
            value: 0.04,
            label: '0.04'
        }
    ];
    const marks1 = [
        {
            value: 0,
            label: '0%'
        },
        {
            value: 20,
            label: '20%'
        },
        {
            value: 40,
            label: '40%'
        },
        {
            value: 60,
            label: '60%'
        },
        {
            value: 80,
            label: '80%'
        },
        {
            value: 100,
            label: '100%'
        }
    ];
    const classes = useStyles();
    const prefersDarkMode = (0,_material_ui_core_useMediaQuery__WEBPACK_IMPORTED_MODULE_2__["default"])('(prefers-color-scheme: dark)');
    const theme = react__WEBPACK_IMPORTED_MODULE_0___default().useMemo(() => (0,_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_3__["default"])({
        palette: {
            type: prefersDarkMode ? 'dark' : 'light'
        }
    }), [prefersDarkMode]);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_4__["default"], { theme: theme },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_CssBaseline__WEBPACK_IMPORTED_MODULE_5__["default"], null),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: classes.root },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_6__["default"], { container: true, spacing: 3, justify: "center" },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_6__["default"], { item: true, sm: 8 },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Box__WEBPACK_IMPORTED_MODULE_7__["default"], { id: Props.uuid, style: {
                                width: '600px',
                                height: '350px',
                                backgroundColor: 'black'
                            } })),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_6__["default"], { item: true, sm: 1 },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Slider__WEBPACK_IMPORTED_MODULE_8__["default"], { orientation: "vertical", getAriaValueText: valuetext, valueLabelDisplay: "auto", defaultValue: 30, "aria-labelledby": "vertical-slider", min: 0, max: 100, marks: marks1, onChange: Props.changeHandler1, color: 'primary' })),
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_6__["default"], { item: true, sm: 1 },
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Slider__WEBPACK_IMPORTED_MODULE_8__["default"], { orientation: "vertical", defaultValue: [0.01, -0.01], "aria-labelledby": "vertical-slider", getAriaValueText: valuetext, valueLabelDisplay: "on", marks: marks2, min: -0.04, max: 0.04, step: 0.001, onChange: Props.changeHandler2, color: 'secondary' })))))));
}


/***/ }),

/***/ "./lib/switches.js":
/*!*************************!*\
  !*** ./lib/switches.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ SwitchLabels)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _material_ui_core_FormGroup__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @material-ui/core/FormGroup */ "./node_modules/@material-ui/core/esm/FormGroup/FormGroup.js");
/* harmony import */ var _material_ui_core_FormControlLabel__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @material-ui/core/FormControlLabel */ "./node_modules/@material-ui/core/esm/FormControlLabel/FormControlLabel.js");
/* harmony import */ var _material_ui_core_Switch__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @material-ui/core/Switch */ "./node_modules/@material-ui/core/esm/Switch/Switch.js");
/* harmony import */ var _material_ui_core_styles__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @material-ui/core/styles */ "./node_modules/@material-ui/core/esm/styles/makeStyles.js");
/* harmony import */ var _material_ui_core_Button__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @material-ui/core/Button */ "./node_modules/@material-ui/core/esm/Button/Button.js");
/* harmony import */ var _material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @material-ui/core/Grid */ "./node_modules/@material-ui/core/esm/Grid/Grid.js");







function SwitchLabels(Props) {
    const useStyles = (0,_material_ui_core_styles__WEBPACK_IMPORTED_MODULE_1__["default"])(theme => ({
        container: {
            display: 'flex',
            flexWrap: 'wrap',
            position: 'absolute',
            top: 0,
            left: 0,
            height: '100%',
            width: '100%',
            alignItems: 'center'
        },
        textField: {
            marginLeft: theme.spacing(1),
            marginRight: theme.spacing(1),
            width: 200
        },
        formGroup: {
            alignItems: 'center'
        }
    }));
    const classes = useStyles();
    const [state, setState] = react__WEBPACK_IMPORTED_MODULE_0___default().useState({
        checkedA: false,
        checkedB: true,
        checkedC: true
    });
    const handleChange = (event) => {
        setState({ ...state, [event.target.name]: event.target.checked });
        if (event.target.name === 'checkedA') {
            Props.clickHandler1();
        }
        if (event.target.name === 'checkedB') {
            Props.clickHandler2();
        }
        if (event.target.name === 'checkedC') {
            Props.clickHandler3();
        }
    };
    const handleClick = () => {
        Props.bclick1();
        setState({
            checkedA: state.checkedA,
            checkedB: !state.checkedB,
            checkedC: !state.checkedC
        });
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_2__["default"], { container: true, spacing: 3, justify: "center" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_2__["default"], { item: true, sm: 3 },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Button__WEBPACK_IMPORTED_MODULE_3__["default"], { style: { height: '20px' }, color: "secondary", variant: "contained", onClick: Props.bclick2 }, "Toggle structure")),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_2__["default"], { item: true, sm: 3 },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Button__WEBPACK_IMPORTED_MODULE_3__["default"], { style: { height: '20px' }, color: "primary", variant: "contained", onClick: handleClick }, "Toggle surface"))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_2__["default"], { container: true, justify: "center" },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_FormGroup__WEBPACK_IMPORTED_MODULE_4__["default"], { className: classes.formGroup, row: true },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_FormControlLabel__WEBPACK_IMPORTED_MODULE_5__["default"], { control: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Switch__WEBPACK_IMPORTED_MODULE_6__["default"], { checked: state.checkedA, onChange: handleChange, name: "checkedA" }), label: "Spin" }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_FormControlLabel__WEBPACK_IMPORTED_MODULE_5__["default"], { control: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Switch__WEBPACK_IMPORTED_MODULE_6__["default"], { checked: state.checkedB, onChange: handleChange, name: "checkedB", color: "primary" }), label: "Alpha" }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_FormControlLabel__WEBPACK_IMPORTED_MODULE_5__["default"], { control: react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_material_ui_core_Switch__WEBPACK_IMPORTED_MODULE_6__["default"], { checked: state.checkedC, onChange: handleChange, name: "checkedC", color: "secondary" }), label: "Beta" })))));
}


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "CounterWidget": () => (/* binding */ CounterWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _osscar_ngl__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @osscar/ngl */ "webpack/sharing/consume/default/@osscar/ngl/@osscar/ngl");
/* harmony import */ var _osscar_ngl__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_osscar_ngl__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! underscore */ "webpack/sharing/consume/default/underscore/underscore");
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(underscore__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _sliders__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./sliders */ "./lib/sliders.js");
/* harmony import */ var _switches__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./switches */ "./lib/switches.js");
/* harmony import */ var _inputs__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./inputs */ "./lib/inputs.js");
/* harmony import */ var _material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @material-ui/core/Grid */ "./node_modules/@material-ui/core/esm/Grid/Grid.js");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__);










/**
 * A Counter Lumino Widget that wraps a CounterComponent.
 */
class CounterWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(browserFactory) {
        var _a;
        super();
        this.addClass('jp-ReactWidget');
        this.uuid = underscore__WEBPACK_IMPORTED_MODULE_3__.uniqueId('ngl_');
        this.browserFactory = browserFactory;
        this.currentDirectory = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__.URLExt.join(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__.PageConfig.getBaseUrl() + '/files', ((_a = this.browserFactory) === null || _a === void 0 ? void 0 : _a.defaultBrowser.model.path) + '/');
        window.requestAnimationFrame(() => {
            this.visualizer();
        });
        this.addStructure = this.addStructure.bind(this);
        this.addIsosurface = this.addIsosurface.bind(this);
        this.getCurrentDirectory = this.getCurrentDirectory.bind(this);
        this.updateDatasource = this.updateDatasource.bind(this);
        this.getFileList = this.getFileList.bind(this);
    }
    getCurrentDirectory() {
        var _a;
        this.currentDirectory = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__.URLExt.join(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_4__.PageConfig.getBaseUrl() + '/files', ((_a = this.browserFactory) === null || _a === void 0 ? void 0 : _a.defaultBrowser.model.path) + '/');
    }
    getFileList(types) {
        var _a;
        const a = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__.toArray)((_a = this.browserFactory) === null || _a === void 0 ? void 0 : _a.defaultBrowser.model.items());
        const b = a.filter(item => item.type === 'file' &&
            types.includes(item.name.split('.').pop()));
        const c = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__.map)(b, x => x.name);
        return (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__.toArray)(c);
    }
    updateDatasource() {
        this.getCurrentDirectory();
        _osscar_ngl__WEBPACK_IMPORTED_MODULE_2__.DatasourceRegistry.add('data', new _osscar_ngl__WEBPACK_IMPORTED_MODULE_2__.StaticDatasource(this.currentDirectory));
    }
    visualizer() {
        this.updateDatasource();
        this.stage = new _osscar_ngl__WEBPACK_IMPORTED_MODULE_2__.Stage(this.uuid, { backgroundColor: 'black' });
        window.addEventListener('resize', event => {
            this.stage.handleResize();
        }, false);
        this.stage.viewer.container.addEventListener('dblclick', () => {
            this.stage.toggleFullscreen();
        });
    }
    addStructure(filename) {
        this.updateDatasource();
        this.stage.getComponentsByName('structure1').forEach((element) => {
            this.stage.removeComponent(element);
        });
        this.stage
            .loadFile('data://' + filename, { name: 'structure1' })
            .then((o) => {
            o.addRepresentation('ball+stick');
            o.autoView();
        });
    }
    addIsosurface(filename) {
        this.updateDatasource();
        this.stage.getComponentsByName('surface_1').forEach((element) => {
            this.stage.removeComponent(element);
        });
        this.stage.getComponentsByName('surface_2').forEach((element) => {
            this.stage.removeComponent(element);
        });
        this.stage
            .loadFile('data://' + filename, { name: 'surface_1' })
            .then((o) => {
            o.addRepresentation('surface', {
                visible: true,
                isolevelType: 'value',
                isolevel: 0.01,
                color: 'blue',
                opacity: 0.7,
                opaqueBack: false
            });
            o.signals.visibilityChanged.add((value) => {
                console.log('visibility change to:' + value);
            });
            o.autoView();
        });
        this.stage
            .loadFile('data://' + filename, { name: 'surface_2' })
            .then((o) => {
            o.addRepresentation('surface', {
                visible: true,
                isolevelType: 'value',
                isolevel: -0.01,
                color: 'red',
                opacity: 0.7,
                opaqueBack: false
            });
            o.autoView();
        });
    }
    updateIsosurface(e) {
        this.stage
            .getRepresentationsByName('surface')
            .setParameters({ opacity: e });
        this.stage.getComponentsByName('surface_1').list[0].setVisibility(true);
        this.stage.getComponentsByName('surface_2').list[0].setVisibility(true);
    }
    updateIsolevel(e, filename) {
        this.stage
            .getComponentsByName(filename)
            .list[0].eachRepresentation((reprElem) => {
            reprElem.setParameters({ isolevel: e });
        });
    }
    toggleVisibility(filename) {
        const a = this.stage.getComponentsByName(filename).list[0];
        a.setVisibility(!a.visible);
    }
    setVisibility(filename, val) {
        const a = this.stage.getComponentsByName(filename).list[0];
        a.setVisibility(val);
    }
    toggleSpin() {
        this.stage.toggleSpin();
    }
    render() {
        const func1 = () => this.stage.toggleSpin();
        const func2 = () => this.toggleVisibility('surface_1');
        const func3 = () => this.toggleVisibility('surface_2');
        const bfunc1 = () => {
            this.toggleVisibility('surface_1');
            this.toggleVisibility('surface_2');
        };
        const bfunc2 = () => {
            this.toggleVisibility('structure1');
        };
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_sliders__WEBPACK_IMPORTED_MODULE_6__["default"], { uuid: this.uuid, changeHandler1: (event, val) => {
                    const value = val / 100.0;
                    this.updateIsosurface(value);
                }, changeHandler2: (event, val) => {
                    const value = val;
                    this.updateIsolevel(value[0], 'surface_1');
                    this.updateIsolevel(value[1], 'surface_2');
                } }),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_7__["default"], { container: true, spacing: 3, justify: "center" },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_7__["default"], { item: true, sm: 4 },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_inputs__WEBPACK_IMPORTED_MODULE_8__["default"], { getFiles: this.getFileList, types: ['sdf', 'cif'], factory: this.browserFactory, label: "Structure", options: this.getFileList(['sdf', 'cif']), inputHandler: this.addStructure })),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_material_ui_core_Grid__WEBPACK_IMPORTED_MODULE_7__["default"], { item: true, sm: 4 },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_inputs__WEBPACK_IMPORTED_MODULE_8__["default"], { getFiles: this.getFileList, types: ['cube'], factory: this.browserFactory, label: "Isosurface", options: this.getFileList(['cube']), inputHandler: this.addIsosurface }))),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement(_switches__WEBPACK_IMPORTED_MODULE_9__["default"], { clickHandler1: func1, clickHandler2: func2, clickHandler3: func3, bclick1: bfunc1, bclick2: bfunc2 })));
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_react-dom.3a9f6f9b26b46f2794ed.js.map