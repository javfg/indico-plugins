// This file is part of Indico.
// Copyright (C) 2002 - 2021 CERN
//
// Indico is free software; you can redistribute it and/or
// modify it under the terms of the MIT License; see the
// LICENSE file for more details.

import Oidc from 'oidc-client';

window.signinCallback = function signinCallback() {
  const mgr = new Oidc.UserManager({userStore: new Oidc.WebStorageStateStore()});
  mgr.signinPopupCallback(window.location.href.split('?')[1]);
};

window.renewCallback = function renewCallback() {
  const mgr = new Oidc.UserManager({
    userStore: new Oidc.WebStorageStateStore(),
    loadUserInfo: true,
    filterProtocolClaims: true,
  });
  mgr.signinSilentCallback();
};
