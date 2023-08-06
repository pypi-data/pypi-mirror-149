var __spreadArrays = (this && this.__spreadArrays) || function () {
    for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
    for (var r = Array(s), k = 0, i = 0; i < il; i++)
        for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++)
            r[k] = a[j];
    return r;
};
import { r as registerInstance, h, g as getElement } from './core-2d5e9821.js';
/**
 * Core platform service names
 */
var PlatformServiceName;
(function (PlatformServiceName) {
    PlatformServiceName["Translate"] = "translate";
    PlatformServiceName["Http"] = "http";
    PlatformServiceName["Route"] = "route";
    PlatformServiceName["Notification"] = "notifications";
    PlatformServiceName["Query"] = "query";
    PlatformServiceName["CommandBus"] = "commandBus";
    PlatformServiceName["Dialog"] = "dialog";
    PlatformServiceName["EventDispatcher"] = "eventDispatcher";
    PlatformServiceName["LimetypesState"] = "state.limetypes";
    PlatformServiceName["LimeobjectsState"] = "state.limeobjects";
    PlatformServiceName["ApplicationState"] = "state.application";
    PlatformServiceName["ConfigsState"] = "state.configs";
    PlatformServiceName["FiltersState"] = "state.filters";
    PlatformServiceName["DeviceState"] = "state.device";
    PlatformServiceName["TaskState"] = "state.tasks";
})(PlatformServiceName || (PlatformServiceName = {}));
var Operator;
(function (Operator) {
    Operator["AND"] = "AND";
    Operator["OR"] = "OR";
    Operator["EQUALS"] = "=";
    Operator["NOT"] = "!";
    Operator["GREATER"] = ">";
    Operator["LESS"] = "<";
    Operator["IN"] = "IN";
    Operator["BEGINS"] = "=?";
    Operator["LIKE"] = "?";
    Operator["LESS_OR_EQUAL"] = "<=";
    Operator["GREATER_OR_EQUAL"] = ">=";
})(Operator || (Operator = {}));
/**
 * Events dispatched by the commandbus event middleware
 */
var CommandEvent;
(function (CommandEvent) {
    /**
     * Dispatched when the command has been received by the commandbus.
     * Calling `preventDefault()` on the event will stop the command from being handled
     *
     * @detail { command }
     */
    CommandEvent["Received"] = "command.received";
    /**
     * Dispatched when the command has been handled by the commandbus
     *
     * @detail { command, result }
     */
    CommandEvent["Handled"] = "command.handled";
    /**
     * Dispatched if an error occurs while handling the command
     *
     * @detail { command, error }
     */
    CommandEvent["Failed"] = "command.failed";
})(CommandEvent || (CommandEvent = {}));
var TaskState;
(function (TaskState) {
    /**
     * Task state is unknown
     */
    TaskState["Pending"] = "PENDING";
    /**
     * Task was started by a worker
     */
    TaskState["Started"] = "STARTED";
    /**
     * Task is waiting for retry
     */
    TaskState["Retry"] = "RETRY";
    /**
     * Task succeeded
     */
    TaskState["Success"] = "SUCCESS";
    /**
     * Task failed
     */
    TaskState["Failure"] = "FAILURE";
})(TaskState || (TaskState = {}));
/**
 * Gets an object with all configs where key is used as key.
 *
 * @param {ConfigsOptions} options state decorator options
 *
 * @returns {Function} state decorator
 */
function Configs(options) {
    var config = {
        name: PlatformServiceName.ConfigsState,
    };
    return createStateDecorator(options, config);
}
/**
 * Get the limeobject for the current context
 *
 * @param {StateOptions} [options] state decorator options
 *
 * @returns {Function} state decorator
 */
function CurrentLimeobject(options) {
    if (options === void 0) { options = {}; }
    var config = {
        name: PlatformServiceName.LimeobjectsState,
    };
    options.map = __spreadArrays([currentLimeobject], (options.map || []));
    return createStateDecorator(options, config);
}
function currentLimeobject(limeobjects) {
    var _b = this.context, limetype = _b.limetype, id = _b.id; // tslint:disable-line:no-invalid-this
    if (!limeobjects[limetype]) {
        return undefined;
    }
    return limeobjects[limetype].find(function (object) { return object.id === id; });
}
/**
 * Get the application session
 *
 * @param {StateOptions} [options] state decorator options
 *
 * @returns {Function} state decorator
 */
function Session(options) {
    if (options === void 0) { options = {}; }
    var config = {
        name: PlatformServiceName.ApplicationState,
    };
    options.map = __spreadArrays([getSession], (options.map || []));
    return createStateDecorator(options, config);
}
function getSession(applicationData) {
    return applicationData.session;
}
/**
 * Create a new state decorator
 *
 * @param {StateOptions} options decorator options
 * @param {StateDecoratorConfig} config decorator configuration
 *
 * @returns {Function} state decorator
 */
function createStateDecorator(options, config) {
    return function (component, property) {
        var componentMapping = getComponentMapping(component, property, options, config);
        if (componentMapping.properties.length === 1) {
            extendLifecycleMethods(component, componentMapping.properties);
        }
    };
}
var componentMappings = [];
/**
 * Get mappings for a component, containing the properties with a state decorator for
 * the current component
 *
 * @param {Component} component the component class containing the decorator
 * @param {string} property name of the property
 * @param {StateOptions} options decorator options
 * @param {StateDecoratorConfig} config decorator configuration
 *
 * @returns {ComponentMapping} mappings for the component
 */
function getComponentMapping(component, property, options, config) {
    var mapping = componentMappings.find(function (item) { return item.component === component; });
    if (!mapping) {
        mapping = {
            properties: [],
            component: component,
        };
        componentMappings.push(mapping);
    }
    mapping.properties.push({
        options: options,
        name: property,
        service: {
            name: config.name,
            method: config.method || 'subscribe',
        },
    });
    return mapping;
}
/**
 * Extend the lifecycle methods on the component
 *
 * @param {Component} component the component to extend
 * @param {Property[]} properties the properties with which to extend the component
 *
 * @returns {void}
 */
function extendLifecycleMethods(component, properties) {
    var originalComponentWillLoad = component.componentWillLoad;
    var originalComponentDidUnload = component.componentDidUnload;
    var subscriptions = [];
    component.componentWillLoad = function () {
        var _this = this;
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        properties.forEach(function (property) {
            subscribe.apply(_this, [subscriptions, property]);
        });
        if (originalComponentWillLoad) {
            return originalComponentWillLoad.apply(this, args);
        }
    };
    component.componentDidUnload = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        if (originalComponentDidUnload) {
            originalComponentDidUnload.apply(this, args);
        }
        unsubscribeAll.apply(this, [subscriptions]);
    };
}
/**
 * Subscribe to changes from the state
 * Use as `subscription.apply(componentToAugment, [subscriptions, property])`.
 *
 * @param {Subscription[]} subscriptions existing subscriptions on the component
 * @param {Property} property property to update when subscription triggers
 *
 * @returns {void}
 */
function subscribe(subscriptions, property) {
    var _this = this;
    var subscription = subscriptions.find(function (item) { return item.instance === _this; });
    if (!subscription) {
        subscription = {
            instance: this,
            unsubscribes: [],
        };
        subscriptions.push(subscription);
    }
    var unsubscribe = createSubscription.apply(this, [
        property.options,
        property.name,
        property.service.name,
        property.service.method,
    ]);
    subscription.unsubscribes.push(unsubscribe);
}
/**
 * Unsubscribe to changes from the state
 *
 * @param {Subscription[]} subscriptions existing subscriptions on the component
 *
 * @returns {void}
 */
function unsubscribeAll(subscriptions) {
    var _this = this;
    if (subscriptions === void 0) { subscriptions = []; }
    var subscription = subscriptions.find(function (item) { return item.instance === _this; });
    subscription.unsubscribes.forEach(function (unsubscribe) { return unsubscribe(); });
    for (var i = subscriptions.length - 1; i >= 0; i--) {
        var item = subscriptions[i];
        if (item.instance !== this) {
            continue;
        }
        subscriptions.splice(i, 1);
    }
}
/**
 * Get a function that accepts a state, and updates the given property
 * on the given component with that state
 *
 * @param {any} instance the component to augment
 * @param {string} property name of the property on the component
 *
 * @returns {Function} updates the state
 */
function mapState(instance, property) {
    return function (state) {
        instance[property] = state;
    };
}
/**
 * Create a state subscription
 * Use as `createSubscription.apply(componentToAugment, [options, property, name, method])`.
 *
 * @param {StateOptions} options options for the selector
 * @param {string} property name of the property on the component
 * @param {string} name name of the state service
 * @param {string} method name of method on the state service
 *
 * @returns {Function} unsubscribe function
 */
function createSubscription(options, property, name, method) {
    var myOptions = Object.assign({}, options);
    bindFunctions(myOptions, this);
    var platform = this.platform;
    if (!platform.has(name)) {
        throw new Error("Service " + name + " does not exist");
    }
    var service = platform.get(name);
    return service[method](mapState(this, property), myOptions);
}
/**
 * Bind connect functions to the current scope
 *
 * @param {StateOptions} options options for the selector
 * @param {*} scope the current scope to bind to
 *
 * @returns {void}
 */
function bindFunctions(options, scope) {
    if (options.filter) {
        options.filter = options.filter.map(function (func) { return func.bind(scope); });
    }
    if (options.map) {
        options.map = options.map.map(function (func) { return func.bind(scope); });
    }
}
var __decorate = (undefined && undefined.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function")
        r = Reflect.decorate(decorators, target, key, desc);
    else
        for (var i = decorators.length - 1; i >= 0; i--)
            if (d = decorators[i])
                r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var Test = /** @class */ (function () {
    function Test(hostRef) {
        var _this = this;
        registerInstance(this, hostRef);
        this.document = {};
        this.session = {};
        this.config = {};
        this.includePerson = true;
        this.includeCoworker = true;
        this.cloneDocument = true;
        this.isOpen = false;
        this.allowedExtensions = Object.freeze(["PDF", "DOC", "DOCX"]);
        this.setCloneDocument = function (event) {
            event.stopPropagation();
            _this.cloneDocument = event.detail;
        };
        this.openDialog = function () {
            _this.isOpen = true;
        };
        this.closeDialog = function () {
            _this.isOpen = false;
        };
    }
    Test.prototype.goToScrive = function (id, scriveDocId) {
        var host = this.config.limepkg_scrive.scriveHost;
        var lang = this.session.language;
        window.open(host + "/public/?limeDocId=" + id + "&lang=" + lang + "&usePerson=" + this.includePerson + "&useCoworker=" + this.includeCoworker + "&cloneDocument=" + this.cloneDocument + "&scriveDocId=" + scriveDocId);
    };
    Test.prototype.files = function () {
        var _a;
        var fileMap = ((_a = this.document) === null || _a === void 0 ? void 0 : _a._files) || {};
        var fileIds = Object.keys(fileMap);
        return fileIds.map(function (id) { return fileMap[id]; });
    };
    Test.prototype.isSignable = function (file) {
        return this.allowedExtensions.includes((file.extension || "").toUpperCase());
    };
    Test.prototype.render = function () {
        var _this = this;
        if (this.context.limetype !== 'document') {
            return;
        }
        var signableFiles = this.files().filter(this.isSignable, this);
        var noSignableFiles = signableFiles.length === 0;
        var tooManySignableFiles = signableFiles.length > 1;
        if (noSignableFiles || tooManySignableFiles) {
            return;
        }
        var translate = this.platform.get(PlatformServiceName.Translate);
        var esignLabel = translate.get("limepkg_scrive.primary_action");
        var cloneLabel = translate.get("limepkg_scrive.clone_document");
        var cloneHintLabel = translate.get("limepkg_scrive.clone_hint");
        var cloneInfoLabel = translate.get("limepkg_scrive.clone_info");
        var okLabel = translate.get("limepkg_scrive.ok");
        return (h("section", null, h("limel-config", { config: { iconPath: '/static/limepkg_scrive/static/' } }), h("limel-button", { label: esignLabel, outlined: true, icon: "scrive", onClick: function () { var _a; return _this.goToScrive(_this.context.id, (_a = _this.document) === null || _a === void 0 ? void 0 : _a.scrive_document_id); } }), h("p", null, h("limel-flex-container", { justify: "start" }, h("limel-checkbox", { label: cloneLabel, checked: this.cloneDocument, onChange: this.setCloneDocument }), h("limel-icon-button", { icon: "question_mark", label: cloneHintLabel, onClick: this.openDialog }))), h("limel-dialog", { open: this.isOpen, onClose: this.closeDialog }, h("p", null, cloneInfoLabel), h("limel-button", { label: okLabel, onClick: this.closeDialog, slot: "button" }))));
    };
    Object.defineProperty(Test.prototype, "element", {
        get: function () { return getElement(this); },
        enumerable: true,
        configurable: true
    });
    Object.defineProperty(Test, "style", {
        get: function () { return ".container{margin-left:1.25rem;margin-right:1.25rem}"; },
        enumerable: true,
        configurable: true
    });
    return Test;
}());
__decorate([
    CurrentLimeobject()
], Test.prototype, "document", void 0);
__decorate([
    Session()
], Test.prototype, "session", void 0);
__decorate([
    Configs({})
], Test.prototype, "config", void 0);
export { Test as lwc_limepkg_scrive };
