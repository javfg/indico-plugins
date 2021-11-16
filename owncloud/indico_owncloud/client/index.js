// This file is part of the CERN Indico plugins.
// Copyright (C) 2014 - 2021 CERN
//
// The CERN Indico plugins are free software; you can redistribute
// them and/or modify them under the terms of the MIT License; see
// the LICENSE file for more details.

// eslint-disable-next-line no-unused-vars
import FilePicker from '@ownclouders/file-picker';

window.setupOwncloudFilePickerWidget = function setupOwncloudFilePickerWidget({ config, fieldId }) {
    const filePickerComponent = document.getElementById(`${fieldId}-file-picker`);

    filePickerComponent.addEventListener('update', event => {
        const accessToken = Object.entries(localStorage)
        .filter(entry => entry[0].startsWith('oc_oAuth'))
        .map(entry => JSON.parse(entry[1]))
        .find(entry => entry.access_token).access_token;

        const fileUrl = `${config.server}/remote.php/webdav`;
        const files = event.detail[0].map(resource => `${fileUrl}${resource.path}`).join('\n');

        document.getElementById(`${fieldId}-token`).value = accessToken;
        document.getElementById(`${fieldId}-files`).value = files;
    });
};

