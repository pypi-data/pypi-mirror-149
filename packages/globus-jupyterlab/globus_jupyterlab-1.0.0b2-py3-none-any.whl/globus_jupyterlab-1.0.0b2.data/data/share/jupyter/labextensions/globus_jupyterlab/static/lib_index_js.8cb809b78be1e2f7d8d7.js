"use strict";
(self["webpackChunkglobus_jupyterlab"] = self["webpackChunkglobus_jupyterlab"] || []).push([["lib_index_js"],{

/***/ "./lib/components/Endpoint.js":
/*!************************************!*\
  !*** ./lib/components/Endpoint.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react-router-dom */ "webpack/sharing/consume/default/react-router-dom/react-router-dom");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_router_dom__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../handler */ "./lib/handler.js");
/* harmony import */ var recoil__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! recoil */ "webpack/sharing/consume/default/recoil/recoil");
/* harmony import */ var recoil__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(recoil__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _GlobusObjects__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./GlobusObjects */ "./lib/components/GlobusObjects.js");






const useQuery = () => {
    const { search } = (0,react_router_dom__WEBPACK_IMPORTED_MODULE_0__.useLocation)();
    return react__WEBPACK_IMPORTED_MODULE_1___default().useMemo(() => new URLSearchParams(search), [search]);
};
const Endpoint = (props) => {
    // Local State
    const [apiError, setAPIError] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(null);
    const [endpointList, setEndpointList] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)({ DATA: [], path: null });
    const [endpoint, setEndpoint] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(null);
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(false);
    const [selectedEndpointItems, setSelectedEndpointItems] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)([]);
    const [transfer, setTransfer] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(null);
    const [transferDirection, setTransferDirection] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(null);
    // Recoil (global) State
    const config = (0,recoil__WEBPACK_IMPORTED_MODULE_2__.useRecoilValue)(_GlobusObjects__WEBPACK_IMPORTED_MODULE_3__.ConfigAtom);
    // React Router history and params
    let history = (0,react_router_dom__WEBPACK_IMPORTED_MODULE_0__.useHistory)();
    let params = (0,react_router_dom__WEBPACK_IMPORTED_MODULE_0__.useParams)();
    let endpointID = params.endpointID;
    let path = params.path;
    let query = useQuery();
    // ComponentDidMount Functions
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        getEndpoint(endpointID);
    }, [endpointID]);
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        listEndpointItems(endpointID, path);
    }, [endpointID, path]);
    const getEndpoint = async (endpointID) => {
        try {
            let endpoint = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)(`endpoint_detail?endpoint=${endpointID}`);
            setEndpoint(endpoint);
        }
        catch (error) {
            setAPIError(error);
        }
    };
    const listEndpointItems = async (endpointID, path = null) => {
        setAPIError(null);
        setEndpointList({ DATA: [], path: null });
        setLoading(true);
        try {
            let fullPath = query.get('full-path');
            let url = `operation_ls?endpoint=${endpointID}&show_hidden=0`;
            if (fullPath) {
                url = `${url}&path=${fullPath}`;
            }
            const listItems = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)(url);
            setEndpointList(listItems);
        }
        catch (error) {
            /* Note: This probably isn't a great UX to simply pop up a login page, but it
            does demonstrate the base functionality for picking endpoints */
            if ('login_url' in error) {
                window.open(error.login_url, 'Globus Login', 'height=600,width=800').focus();
            }
            setAPIError(error);
        }
        setLoading(false);
    };
    // Event Handlers
    const handleEndpointItemSelect = (event) => {
        if (event.target.checked) {
            setSelectedEndpointItems((selectedEndpointItems) => {
                return [JSON.parse(event.target.value), ...selectedEndpointItems];
            });
        }
        else {
            const removeItem = JSON.parse(event.target.value);
            const index = selectedEndpointItems
                .map((item) => {
                return item.name;
            })
                .indexOf(removeItem.name);
            if (index > -1) {
                selectedEndpointItems.splice(index, 1);
                setSelectedEndpointItems(selectedEndpointItems);
            }
        }
    };
    const handleTransferDirection = (event) => {
        setTransferDirection(event.currentTarget.value);
    };
    const handleTransferRequest = async (event) => {
        event.preventDefault();
        setAPIError(null);
        setLoading(true);
        setTransfer(null);
        var transferItems = [];
        var sourceEndpoint = transferDirection == 'transfer-to-jupyter' ? endpoint.id : config.collection_id;
        var destinationEndpoint = transferDirection == 'transfer-to-jupyter' ? config.collection_id : endpoint.id;
        if (transferDirection == 'transfer-from-jupyter') {
            if (selectedEndpointItems.length > 1) {
                setAPIError({ response: { status: '500', statusText: 'Please only select one remote directory to transfer data to' } });
            }
            // Loop through selectedJupyterItems from props
            if (props.selectedJupyterItems.directories.length) {
                for (let directory of props.selectedJupyterItems.directories) {
                    let destinationPath = selectedEndpointItems.length
                        ? `${endpointList.path}${selectedEndpointItems[0].name}/${directory.path}`
                        : `${endpointList.path}${directory.path}`;
                    transferItems.push({
                        source_path: `${config.collection_base_path}/${directory.path}`,
                        destination_path: destinationPath,
                        recursive: true,
                    });
                }
            }
            if (props.selectedJupyterItems.files.length) {
                for (let file of props.selectedJupyterItems.files) {
                    let destinationPath = selectedEndpointItems.length
                        ? `${endpointList.path}${selectedEndpointItems[0].name}/${file.path}`
                        : `${endpointList.path}${file.path}`;
                    transferItems.push({
                        source_path: `${config.collection_base_path}/${file.path}`,
                        destination_path: destinationPath,
                        recursive: false,
                    });
                }
            }
        }
        else {
            if (props.selectedJupyterItems.directories.length === 0 || props.selectedJupyterItems.directories.length > 1) {
                setLoading(false);
                setAPIError({ response: { status: '500', statusText: 'Please select one jupyter directory to transfer data to' } });
            }
            // Loop through selectedEndpointItems from state
            for (let selectedEndpointItem of selectedEndpointItems) {
                transferItems.push({
                    source_path: `${endpointList.path}${selectedEndpointItem.name}`,
                    destination_path: `${config.collection_base_path}/${props.selectedJupyterItems.directories[0].path}/${selectedEndpointItem.name}`,
                    recursive: selectedEndpointItem.type == 'dir' ? true : false,
                });
            }
        }
        let transferRequest = {
            source_endpoint: sourceEndpoint,
            destination_endpoint: destinationEndpoint,
            DATA: transferItems,
        };
        try {
            const transferResponse = await (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)('submit_transfer', {
                body: JSON.stringify(transferRequest),
                method: 'POST',
            });
            setLoading(false);
            setTransfer(transferResponse);
        }
        catch (error) {
            setLoading(false);
            setAPIError(error);
        }
    };
    if (apiError) {
        return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'row' },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'col-8' },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'alert alert-danger' },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("strong", null,
                        "Error ",
                        apiError.response.status,
                        ": ",
                        apiError.response.statusText,
                        "."),
                    ' ',
                    "Please try again."))));
    }
    if (loading) {
        return react__WEBPACK_IMPORTED_MODULE_1___default().createElement("h5", { className: 'mt-5' }, "Loading");
    }
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null, endpointList['DATA'].length > 0 ? (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'mt-5' },
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("h5", null,
            "Browsing Collection ",
            endpoint ? endpoint.display_name : endpointID),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { className: 'btn btn-sm btn-primary mb-4 mt-2', onClick: () => history.goBack() }, "Back"),
        transfer && (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'alert alert-success alert-dismissible fade show' },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("h4", { className: 'alert-heading' }, "Accepted!"),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", null, transfer['message']),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("hr", null),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", { className: 'mb-0' },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("a", { className: 'alert-link', href: `https://app.globus.org/activity/${transfer['task_id']}`, target: '_blank' },
                    "Check Status of Request ",
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("i", { className: 'fa-solid fa-arrow-up-right-from-square' }))))),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("br", null),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { id: 'endpoint-list', className: 'border col-8 rounded py-3' }, endpointList['DATA'].map((listItem, index) => {
            return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'form-check ms-3', key: index }, listItem['type'] == 'dir' ? (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { onChange: handleEndpointItemSelect, className: 'form-check-input', type: 'checkbox', value: JSON.stringify(listItem), "data-list-item-name": listItem['name'] }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", null,
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_0__.Link, { to: `/endpoints/${endpointID}/items/${listItem['name']}?full-path=${endpointList['path']}${listItem['name']}` },
                        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("i", { className: 'fa-solid fa-folder-open' }),
                        " ",
                        listItem['name'])))) : (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { onChange: handleEndpointItemSelect, className: 'form-check-input', type: 'checkbox', value: JSON.stringify(listItem), "data-list-item-name": listItem['name'] }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", null,
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("i", { className: 'fa-solid fa-file' }),
                    " ",
                    listItem['name'])))));
        })),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { id: 'transfer-direction' },
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'form-check form-check-inline mt-4' },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { className: 'form-check-input', onChange: handleTransferDirection, type: 'radio', name: 'transfer-direction', id: 'transfer-to-jupyter', value: 'transfer-to-jupyter' }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", { className: 'form-check-label', htmlFor: 'transfer-to-jupyter' }, "Transfer to Jupyterlab")),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'form-check form-check-inline' },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("input", { className: 'form-check-input', onChange: handleTransferDirection, type: 'radio', name: 'transfer-direction', id: 'transfer-from-jupyter', value: 'transfer-from-jupyter' }),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("label", { className: 'form-check-label', htmlFor: 'transfer-from-jupyter' }, "Transfer from Jupyterlab")),
            react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'form-check form-check-inline pl-0' },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { className: 'btn btn-sm btn-primary', onClick: handleTransferRequest, type: 'button' }, "Submit Transfer Request"))))) : (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", null,
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("button", { className: 'btn btn-sm btn-primary mb-2 mt-3', onClick: () => history.goBack() }, "Back"),
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", null, "No files or folders found")))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Endpoint);


/***/ }),

/***/ "./lib/components/EndpointSearch.js":
/*!******************************************!*\
  !*** ./lib/components/EndpointSearch.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../handler */ "./lib/handler.js");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-router-dom */ "webpack/sharing/consume/default/react-router-dom/react-router-dom");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_router_dom__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _Endpoint__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./Endpoint */ "./lib/components/Endpoint.js");
/* harmony import */ var _Endpoints__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./Endpoints */ "./lib/components/Endpoints.js");





const EndpointSearch = (props) => {
    const [apiError, setAPIError] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [endpoints, setEndpoints] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)({ DATA: [] });
    const [endpointValue, setEndpointValue] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const history = (0,react_router_dom__WEBPACK_IMPORTED_MODULE_1__.useHistory)();
    // Event Handlers
    const handleEndpointValueChange = (event) => {
        setEndpointValue(event.target.value);
    };
    const handleSearchEndpoints = async (event) => {
        let keyCode = event.keyCode;
        if (keyCode == 13) {
            setAPIError(null);
            setEndpoints({ DATA: [] });
            setLoading(true);
            try {
                let endpoints = await (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)(`endpoint_search?filter_fulltext=${endpointValue}`);
                setEndpoints(endpoints);
                setLoading(false);
                history.push('/endpoints');
            }
            catch (error) {
                setLoading(false);
                setAPIError(error);
            }
        }
    };
    if (apiError) {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'row' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'col-8' },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'alert alert-danger' },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("strong", null,
                        "Error ",
                        apiError.response.status,
                        ": ",
                        apiError.response.statusText,
                        "."),
                    ' ',
                    "Please try again."))));
    }
    if (loading) {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h5", null, "Loading");
    }
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { id: 'endpoint-search', className: 'mb-4' },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h5", null, "Search Collections for Transferring"),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'row' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'col-8' },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { id: 'endpoint-input', className: 'form-control', placeholder: 'Start typing and press enter to search', type: 'text', value: endpointValue, onChange: handleEndpointValueChange, onKeyDown: handleSearchEndpoints }))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_1__.Route, { exact: true, path: '/endpoints', render: (props) => {
                return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_Endpoints__WEBPACK_IMPORTED_MODULE_3__["default"], Object.assign({}, props, { endpoints: endpoints }));
            } }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_1__.Route, { exact: true, path: '/endpoints/:endpointID' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_Endpoint__WEBPACK_IMPORTED_MODULE_4__["default"], { selectedJupyterItems: props.selectedJupyterItems })),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_1__.Route, { path: '/endpoints/:endpointID/items/:path' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_Endpoint__WEBPACK_IMPORTED_MODULE_4__["default"], { selectedJupyterItems: props.selectedJupyterItems }))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (EndpointSearch);


/***/ }),

/***/ "./lib/components/Endpoints.js":
/*!*************************************!*\
  !*** ./lib/components/Endpoints.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react-router-dom */ "webpack/sharing/consume/default/react-router-dom/react-router-dom");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_router_dom__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);


const Endpoints = (props) => {
    return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'row' }, props.endpoints['DATA'].length > 0 && (react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'col-8' },
        react__WEBPACK_IMPORTED_MODULE_1___default().createElement("div", { className: 'list-group' }, props.endpoints['DATA'].map((endpoint) => {
            return (react__WEBPACK_IMPORTED_MODULE_1___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_0__.Link, { key: endpoint.id, to: `/endpoints/${endpoint.id}`, className: 'list-group-item list-group-item-action flex-column align-items-start' },
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("h5", { className: 'mb-1' },
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("i", { className: 'fa-solid fa-layer-group' }),
                    "\u00A0",
                    endpoint.display_name),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", { className: 'mb-0 mt-2 fw-bold' }, "Owner:"),
                react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", { className: 'mb-1' }, endpoint.owner_string),
                endpoint.description && (react__WEBPACK_IMPORTED_MODULE_1___default().createElement((react__WEBPACK_IMPORTED_MODULE_1___default().Fragment), null,
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", { className: 'mb-0 mt-2 fw-bold' }, "Description:"),
                    react__WEBPACK_IMPORTED_MODULE_1___default().createElement("p", { className: 'mb-1' }, endpoint.description)))));
        }))))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Endpoints);


/***/ }),

/***/ "./lib/components/GlobusObjects.js":
/*!*****************************************!*\
  !*** ./lib/components/GlobusObjects.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ConfigAtom": () => (/* binding */ ConfigAtom),
/* harmony export */   "TransferAtom": () => (/* binding */ TransferAtom),
/* harmony export */   "TransferSelector": () => (/* binding */ TransferSelector)
/* harmony export */ });
/* harmony import */ var recoil__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! recoil */ "webpack/sharing/consume/default/recoil/recoil");
/* harmony import */ var recoil__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(recoil__WEBPACK_IMPORTED_MODULE_0__);

const ConfigAtom = (0,recoil__WEBPACK_IMPORTED_MODULE_0__.atom)({
    key: 'ConfigAtom',
    default: {
        collection_id: '',
        collection_base_path: '',
        is_gcp: false,
        is_logged_in: false,
        collection_id_owner: ''
    },
});
const TransferAtom = (0,recoil__WEBPACK_IMPORTED_MODULE_0__.atom)({
    key: 'TransferAtom',
    default: {
        source_endpoint: '',
        destination_endpoint: '',
        transfer_items: [{
                source_path: '',
                destination_path: '',
                recursive: false
            }],
    },
});
const TransferSelector = (0,recoil__WEBPACK_IMPORTED_MODULE_0__.selector)({
    key: 'TransferSelector',
    get: ({ get }) => {
        return get(TransferAtom);
    },
    set: ({ get, set }, newTransferObject) => {
        let oldTransferObject = get(TransferAtom);
        let updatedTransferObject = Object.assign(Object.assign({}, oldTransferObject), newTransferObject);
        set(TransferAtom, updatedTransferObject);
    },
});


/***/ }),

/***/ "./lib/components/HubLoginWidget.js":
/*!******************************************!*\
  !*** ./lib/components/HubLoginWidget.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "HubLoginWidget": () => (/* binding */ HubLoginWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../handler */ "./lib/handler.js");



const HubLogin = (props) => {
    const [apiError, setAPIError] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const [hubInputCode, setHubInputCode] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(null);
    const handleHubInputChange = (event) => {
        setHubInputCode(event.target.value);
    };
    const handleHubLogin = async (event) => {
        event.preventDefault();
        try {
            let response = await (0,_handler__WEBPACK_IMPORTED_MODULE_2__.requestAPI)(`oauth_callback_manual?code=${hubInputCode}`);
            console.log(response);
        }
        catch (error) {
            setAPIError(error);
        }
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'container mt-5' },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'row' },
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: 'col-8' },
                apiError && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { id: 'api-error', className: 'alert alert-danger' },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("strong", null,
                        "Error ",
                        apiError.response.status,
                        ": ",
                        apiError.response.statusText,
                        "."),
                    ' ',
                    "Please try again.")),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("label", { htmlFor: 'code-input', className: 'form-label' }, "Paste Code and Click Login"),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: 'text', id: 'code-input', className: 'form-control mb-3', name: 'code-input', onChange: handleHubInputChange }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: 'button', className: 'btn btn-primary', onClick: handleHubLogin }, "Login")))));
};
class HubLoginWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(HubLogin, null);
    }
}


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
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'globus-jupyterlab', endPoint);
    let response;
    try {
        console.log('making request to: ' + requestUrl);
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    const data = await response.json();
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "globus": () => (/* binding */ globus)
/* harmony export */ });
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _utilities__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./utilities */ "./lib/utilities.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _components_HubLoginWidget__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./components/HubLoginWidget */ "./lib/components/HubLoginWidget.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");








const addJupyterCommands = (app, commands) => {
    for (let command of commands) {
        app.commands.addCommand(command.command, {
            label: command.label,
            caption: command.caption,
            icon: _utilities__WEBPACK_IMPORTED_MODULE_4__.GlobusIcon,
            execute: command.execute
        });
    }
};
/**
 * Globus plugin
 */
const globus = {
    id: '@jupyterlab/globus_jupyterlab',
    autoStart: true,
    requires: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_0__.IFileBrowserFactory],
    activate: activateGlobus,
};
async function activateGlobus(app, factory) {
    console.log('Globus Jupyterlab Extension Activated!');
    // GET request
    try {
        const data = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('config');
        console.log('Fetching basic data about the notebook server environment:', data);
        /*
          Commands to initiate a Globus Transfer.
          */
        let commands = [
            {
                command: 'globus-jupyterlab-transfer/context-menu:open',
                label: 'Initiate Globus Transfer',
                caption: 'Login with Globus to initiate transfers',
                execute: async () => {
                    var files = factory.tracker.currentWidget.selectedItems();
                    var jupyterToken = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.PageConfig.getToken();
                    var label = 'Globus Jupyterlab Transfer';
                    let jupyterItems = [], fileCheck = true;
                    while (fileCheck) {
                        let file = files.next();
                        if (file) {
                            jupyterItems.push(file);
                        }
                        else {
                            fileCheck = false;
                        }
                    }
                    // GET config payload which contains basic auth data
                    const config = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('config');
                    // Start creating the widget, but don't attach unless authenticated
                    const content = new _widget__WEBPACK_IMPORTED_MODULE_6__.GlobusWidget(config, jupyterToken, jupyterItems);
                    const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content });
                    widget.title.label = label;
                    widget.title.icon = _utilities__WEBPACK_IMPORTED_MODULE_4__.GlobusIcon;
                    if (config.is_logged_in) {
                        app.shell.add(widget, 'main');
                    }
                    else {
                        if (config.is_hub) {
                            const hubContent = new _components_HubLoginWidget__WEBPACK_IMPORTED_MODULE_7__.HubLoginWidget();
                            const hubWidget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.MainAreaWidget({ content: hubContent });
                            hubWidget.title.label = 'Authorization Code';
                            hubWidget.title.icon = _utilities__WEBPACK_IMPORTED_MODULE_4__.GlobusIcon;
                            app.shell.add(hubWidget, 'main');
                        }
                        // Poll for successful authentication.
                        let authInterval = window.setInterval(async () => {
                            const config = await (0,_handler__WEBPACK_IMPORTED_MODULE_5__.requestAPI)('config');
                            if (config.is_logged_in) {
                                app.shell.add(widget, 'main');
                                clearInterval(authInterval);
                            }
                        }, 1000);
                        window.open((0,_utilities__WEBPACK_IMPORTED_MODULE_4__.getBaseURL)('globus-jupyterlab/login'), 'Globus Login', 'height=600,width=800').focus();
                    }
                }
            },
        ];
        addJupyterCommands(app, commands);
    }
    catch (reason) {
        console.error(`Error on GET /globus_jupyterlab/config.\n${reason}`);
    }
}
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (globus);


/***/ }),

/***/ "./lib/utilities.js":
/*!**************************!*\
  !*** ./lib/utilities.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "GlobusIcon": () => (/* binding */ GlobusIcon),
/* harmony export */   "getBaseURL": () => (/* binding */ getBaseURL)
/* harmony export */ });
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);



const getBaseURL = (subPath = '') => {
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(settings.baseUrl, subPath);
    return requestUrl;
};
const GlobusIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_0__.LabIcon({
    name: 'globusIcon',
    svgstr: `
      <svg xmlns="http://www.w3.org/2000/svg" version="1.0" width="200.000000pt" height="200.000000pt" viewBox="0 0 200.000000 200.000000" preserveAspectRatio="xMidYMid meet">
        <g transform="translate(0.000000,200.000000) scale(0.100000,-0.100000)" fill="#000000" stroke="none">
          <path d="M480 1697 c-151 -51 -255 -148 -321 -297 -21 -49 -24 -69 -24 -180 0 -114 3 -131 28 -189 15 -36 24 -68 20 -71 -5 -4 -31 -23 -60 -44 -74 -52 -108 -123 -101 -209 12 -147 127 -268 315 -334 72 -26 90 -28 248 -29 94 0 188 -6 210 -12 146 -40 464 -41 659 -2 259 51 411 132 478 256 55 101 46 177 -30 252 -44 44 -46 49 -48 107 -2 106 -72 213 -167 256 -46 20 -167 26 -211 10 -23 -9 -27 -6 -54 43 -56 99 -149 158 -284 181 -32 5 -43 14 -71 58 -62 96 -156 167 -274 206 -88 29 -224 29 -313 -2z m307 -238 c15 -5 40 -22 56 -37 l27 -26 0 32 0 32 85 0 c69 0 85 -3 85 -15 0 -9 -9 -15 -22 -15 -12 0 -30 -7 -40 -17 -17 -15 -18 -37 -18 -272 0 -141 -4 -271 -9 -289 -5 -17 -6 -32 -2 -32 13 0 104 101 130 143 13 21 34 68 46 105 21 61 25 67 56 74 40 9 104 1 140 -18 30 -15 89 -79 89 -97 0 -7 4 -18 9 -26 7 -11 15 -10 42 10 50 36 151 39 199 7 53 -36 80 -83 80 -138 0 -40 4 -49 31 -69 74 -55 88 -132 39 -218 -79 -137 -270 -220 -535 -230 -150 -6 -282 11 -415 53 -73 23 -100 26 -193 24 -164 -3 -282 34 -352 111 -64 71 -54 141 26 181 41 22 83 23 158 4 50 -13 110 -20 151 -17 8 1 -9 12 -38 26 -41 19 -56 33 -68 60 -8 20 -12 40 -9 45 4 6 26 10 50 10 39 0 46 -4 60 -29 21 -41 53 -61 98 -61 47 0 89 21 104 52 7 12 15 58 18 101 7 77 0 93 -25 63 -6 -8 -32 -23 -56 -32 -64 -24 -141 -7 -193 45 -88 88 -96 292 -16 398 47 61 141 89 212 62z"/>
          <path d="M687 1400 c-41 -32 -62 -102 -62 -205 0 -110 21 -160 79 -189 33 -16 41 -17 74 -5 29 11 43 25 62 64 21 43 25 63 24 145 0 78 -4 104 -22 141 -33 69 -102 90 -155 49z"/>
        </g>
      </svg>
    `
});


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "GlobusWidget": () => (/* binding */ GlobusWidget)
/* harmony export */ });
/* harmony import */ var _utilities__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./utilities */ "./lib/utilities.js");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react-router-dom */ "webpack/sharing/consume/default/react-router-dom/react-router-dom");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_router_dom__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var recoil__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! recoil */ "webpack/sharing/consume/default/recoil/recoil");
/* harmony import */ var recoil__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(recoil__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _components_EndpointSearch__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./components/EndpointSearch */ "./lib/components/EndpointSearch.js");
/* harmony import */ var _components_GlobusObjects__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./components/GlobusObjects */ "./lib/components/GlobusObjects.js");
/* harmony import */ var _fortawesome_fontawesome_free_css_all_min_css__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @fortawesome/fontawesome-free/css/all.min.css */ "./node_modules/@fortawesome/fontawesome-free/css/all.min.css");
/* harmony import */ var bootstrap_dist_css_bootstrap_min_css__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! bootstrap/dist/css/bootstrap.min.css */ "./node_modules/bootstrap/dist/css/bootstrap.min.css");









const App = (props) => {
    // Local state values
    const [selectedJupyterItems, setSelectedJupyterItems] = (0,react__WEBPACK_IMPORTED_MODULE_2__.useState)({ isEmpty: true });
    // Global Recoil state values
    const setConfig = (0,recoil__WEBPACK_IMPORTED_MODULE_3__.useSetRecoilState)(_components_GlobusObjects__WEBPACK_IMPORTED_MODULE_6__.ConfigAtom);
    (0,react__WEBPACK_IMPORTED_MODULE_2__.useEffect)(() => {
        setConfig(props.config);
    }, [props.config]);
    (0,react__WEBPACK_IMPORTED_MODULE_2__.useEffect)(() => {
        getJupyterItems();
    }, [props.jupyterItems]);
    const getJupyterItems = async () => {
        let directories = [];
        let files = [];
        let selectedJupyterItemsTemp = {};
        for (let file of props.jupyterItems) {
            try {
                let response = await fetch((0,_utilities__WEBPACK_IMPORTED_MODULE_7__.getBaseURL)(`api/contents/${file.path}`), {
                    headers: {
                        Accept: 'application/json',
                        Authorization: `token ${props.jupyterToken}`,
                        'Content-Type': 'application/json',
                    },
                });
                let temp = await response.json();
                if (temp.type == 'directory') {
                    directories.push(temp);
                }
                else {
                    files.push(temp);
                }
            }
            catch (error) {
                console.log(error);
            }
        }
        selectedJupyterItemsTemp['directories'] = directories;
        selectedJupyterItemsTemp['files'] = files;
        // If we have any file or folder, the payload is not empty
        if (directories.length || files.length) {
            selectedJupyterItemsTemp['isEmpty'] = false;
        }
        // Transfer direction inferred from selected files/folders
        if ((files.length && directories.length) || (files.length && !directories.length)) {
            selectedJupyterItemsTemp['transferDirection'] = 'toEndpoint';
        }
        else {
            selectedJupyterItemsTemp['transferDirection'] = 'toFromEndpoint';
        }
        //@ts-ignore
        setSelectedJupyterItems(selectedJupyterItemsTemp);
    };
    return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("div", { className: 'container pt-5' }, !selectedJupyterItems['isEmpty'] ? (react__WEBPACK_IMPORTED_MODULE_2___default().createElement(_components_EndpointSearch__WEBPACK_IMPORTED_MODULE_8__["default"], { selectedJupyterItems: selectedJupyterItems })) : (react__WEBPACK_IMPORTED_MODULE_2___default().createElement("p", { className: 'fw-bold text-danger' }, "No files selected"))));
};
class GlobusWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(config = {}, jupyterToken = '', jupyterItems = []) {
        super();
        this.config = config;
        this.jupyterItems = jupyterItems;
        this.jupyterToken = jupyterToken;
        this.addClass('jp-ReactWidget');
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_0__.HashRouter, null,
            react__WEBPACK_IMPORTED_MODULE_2___default().createElement(recoil__WEBPACK_IMPORTED_MODULE_3__.RecoilRoot, null,
                react__WEBPACK_IMPORTED_MODULE_2___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_0__.Switch, null,
                    react__WEBPACK_IMPORTED_MODULE_2___default().createElement(react_router_dom__WEBPACK_IMPORTED_MODULE_0__.Route, { path: '/', render: (props) => {
                            return (react__WEBPACK_IMPORTED_MODULE_2___default().createElement(App, Object.assign({}, props, { config: this.config, jupyterItems: this.jupyterItems, jupyterToken: this.jupyterToken })));
                        } })))));
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.8cb809b78be1e2f7d8d7.js.map