'use strict';

Object.defineProperty(exports, '__esModule', { value: true });

const core = require('./core-12852af1.js');

const defineCustomElements = (win, options) => {
  return core.patchEsm().then(() => {
    core.bootstrapLazy([["lwc-limepkg-scrive.cjs",[[1,"lwc-limepkg-scrive",{"platform":[16],"context":[16],"document":[32],"session":[32],"config":[32],"includePerson":[32],"includeCoworker":[32],"cloneDocument":[32],"isOpen":[32]}]]],["lwc-limepkg-scrive-loader.cjs",[[1,"lwc-limepkg-scrive-loader",{"platform":[16],"context":[16]}]]]], options);
  });
};

exports.defineCustomElements = defineCustomElements;
