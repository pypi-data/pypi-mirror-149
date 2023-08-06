var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
import { PlatformServiceName } from '@limetech/lime-web-components-interfaces';
import { h } from "@stencil/core";
import { Configs, CurrentLimeobject, Session } from '@limetech/lime-web-components-decorators';
export class Test {
    constructor() {
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
        return (h("section", null,
            h("limel-config", { config: { iconPath: '/static/limepkg_scrive/static/' } }),
            h("limel-button", { label: esignLabel, outlined: true, icon: "scrive", onClick: () => { var _a; return this.goToScrive(this.context.id, (_a = this.document) === null || _a === void 0 ? void 0 : _a.scrive_document_id); } }),
            h("p", null,
                h("limel-flex-container", { justify: "start" },
                    h("limel-checkbox", { label: cloneLabel, checked: this.cloneDocument, onChange: this.setCloneDocument }),
                    h("limel-icon-button", { icon: "question_mark", label: cloneHintLabel, onClick: this.openDialog }))),
            h("limel-dialog", { open: this.isOpen, onClose: this.closeDialog },
                h("p", null, cloneInfoLabel),
                h("limel-button", { label: okLabel, onClick: this.closeDialog, slot: "button" }))));
    }
    static get is() { return "lwc-limepkg-scrive"; }
    static get encapsulation() { return "shadow"; }
    static get originalStyleUrls() { return {
        "$": ["lwc-limepkg-scrive.scss"]
    }; }
    static get styleUrls() { return {
        "$": ["lwc-limepkg-scrive.css"]
    }; }
    static get properties() { return {
        "platform": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "LimeWebComponentPlatform",
                "resolved": "LimeWebComponentPlatform",
                "references": {
                    "LimeWebComponentPlatform": {
                        "location": "import",
                        "path": "@limetech/lime-web-components-interfaces"
                    }
                }
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": "Reference to the platform"
            }
        },
        "context": {
            "type": "unknown",
            "mutable": false,
            "complexType": {
                "original": "LimeWebComponentContext",
                "resolved": "LimeWebComponentContext",
                "references": {
                    "LimeWebComponentContext": {
                        "location": "import",
                        "path": "@limetech/lime-web-components-interfaces"
                    }
                }
            },
            "required": false,
            "optional": false,
            "docs": {
                "tags": [],
                "text": "The context this component belongs to"
            }
        }
    }; }
    static get states() { return {
        "document": {},
        "session": {},
        "config": {},
        "includePerson": {},
        "includeCoworker": {},
        "cloneDocument": {},
        "isOpen": {}
    }; }
    static get elementRef() { return "element"; }
}
__decorate([
    CurrentLimeobject()
], Test.prototype, "document", void 0);
__decorate([
    Session()
], Test.prototype, "session", void 0);
__decorate([
    Configs({})
], Test.prototype, "config", void 0);
