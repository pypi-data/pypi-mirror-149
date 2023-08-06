'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const core = require('./core-12852af1.js');

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
    const config = {
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
function CurrentLimeobject(options = {}) {
    const config = {
        name: PlatformServiceName.LimeobjectsState,
    };
    options.map = [currentLimeobject, ...(options.map || [])];
    return createStateDecorator(options, config);
}
function currentLimeobject(limeobjects) {
    const { limetype, id } = this.context; // tslint:disable-line:no-invalid-this
    if (!limeobjects[limetype]) {
        return undefined;
    }
    return limeobjects[limetype].find(object => object.id === id);
}

/**
 * Get the application session
 *
 * @param {StateOptions} [options] state decorator options
 *
 * @returns {Function} state decorator
 */
function Session(options = {}) {
    const config = {
        name: PlatformServiceName.ApplicationState,
    };
    options.map = [getSession, ...(options.map || [])];
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
    return (component, property) => {
        const componentMapping = getComponentMapping(component, property, options, config);
        if (componentMapping.properties.length === 1) {
            extendLifecycleMethods(component, componentMapping.properties);
        }
    };
}
const componentMappings = [];
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
    let mapping = componentMappings.find(item => item.component === component);
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
    const originalComponentWillLoad = component.componentWillLoad;
    const originalComponentDidUnload = component.componentDidUnload;
    const subscriptions = [];
    component.componentWillLoad = function (...args) {
        properties.forEach(property => {
            subscribe.apply(this, [subscriptions, property]);
        });
        if (originalComponentWillLoad) {
            return originalComponentWillLoad.apply(this, args);
        }
    };
    component.componentDidUnload = function (...args) {
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
    let subscription = subscriptions.find(item => item.instance === this);
    if (!subscription) {
        subscription = {
            instance: this,
            unsubscribes: [],
        };
        subscriptions.push(subscription);
    }
    const unsubscribe = createSubscription.apply(this, [
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
function unsubscribeAll(subscriptions = []) {
    const subscription = subscriptions.find(item => item.instance === this);
    subscription.unsubscribes.forEach(unsubscribe => unsubscribe());
    for (let i = subscriptions.length - 1; i >= 0; i--) {
        const item = subscriptions[i];
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
    return (state) => {
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
    const myOptions = Object.assign({}, options);
    bindFunctions(myOptions, this);
    const platform = this.platform;
    if (!platform.has(name)) {
        throw new Error(`Service ${name} does not exist`);
    }
    const service = platform.get(name);
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
        options.filter = options.filter.map(func => func.bind(scope));
    }
    if (options.map) {
        options.map = options.map.map(func => func.bind(scope));
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
const Test = class {
    constructor(hostRef) {
        core.registerInstance(this, hostRef);
        this.document = {};
        this.session = {};
        this.config = {};
        this.includePerson = true;
        this.includeCoworker = true;
        this.cloneDocument = true;
        this.isOpen = false;
        this.allowedExtensions = Object.freeze(["PDF", "DOC", "DOCX"]);
        this.setCloneDocument = (event) => {
            event.stopPropagation();
            this.cloneDocument = event.detail;
        };
        this.openDialog = () => {
            this.isOpen = true;
        };
        this.closeDialog = () => {
            this.isOpen = false;
        };
    }
    goToScrive(id, scriveDocId) {
        const host = this.config.limepkg_scrive.scriveHost;
        const lang = this.session.language;
        window.open(`${host}/public/?limeDocId=${id}&lang=${lang}&usePerson=${this.includePerson}&useCoworker=${this.includeCoworker}&cloneDocument=${this.cloneDocument}&scriveDocId=${scriveDocId}`);
    }
    files() {
        var _a;
        const fileMap = ((_a = this.document) === null || _a === void 0 ? void 0 : _a._files) || {};
        const fileIds = Object.keys(fileMap);
        return fileIds.map(id => fileMap[id]);
    }
    isSignable(file) {
        return this.allowedExtensions.includes((file.extension || "").toUpperCase());
    }
    render() {
        if (this.context.limetype !== 'document') {
            return;
        }
        const signableFiles = this.files().filter(this.isSignable, this);
        const noSignableFiles = signableFiles.length === 0;
        const tooManySignableFiles = signableFiles.length > 1;
        if (noSignableFiles || tooManySignableFiles) {
            return;
        }
        const translate = this.platform.get(PlatformServiceName.Translate);
        const esignLabel = translate.get("limepkg_scrive.primary_action");
        const cloneLabel = translate.get("limepkg_scrive.clone_document");
        const cloneHintLabel = translate.get("limepkg_scrive.clone_hint");
        const cloneInfoLabel = translate.get("limepkg_scrive.clone_info");
        const okLabel = translate.get("limepkg_scrive.ok");
        return (core.h("section", null, core.h("limel-config", { config: { iconPath: '/static/limepkg_scrive/static/' } }), core.h("limel-button", { label: esignLabel, outlined: true, icon: "scrive", onClick: () => { var _a; return this.goToScrive(this.context.id, (_a = this.document) === null || _a === void 0 ? void 0 : _a.scrive_document_id); } }), core.h("p", null, core.h("limel-flex-container", { justify: "start" }, core.h("limel-checkbox", { label: cloneLabel, checked: this.cloneDocument, onChange: this.setCloneDocument }), core.h("limel-icon-button", { icon: "question_mark", label: cloneHintLabel, onClick: this.openDialog }))), core.h("limel-dialog", { open: this.isOpen, onClose: this.closeDialog }, core.h("p", null, cloneInfoLabel), core.h("limel-button", { label: okLabel, onClick: this.closeDialog, slot: "button" }))));
    }
    get element() { return core.getElement(this); }
    static get style() { return ".container{margin-left:1.25rem;margin-right:1.25rem}"; }
};
__decorate([
    CurrentLimeobject()
], Test.prototype, "document", void 0);
__decorate([
    Session()
], Test.prototype, "session", void 0);
__decorate([
    Configs({})
], Test.prototype, "config", void 0);

exports.lwc_limepkg_scrive = Test;
