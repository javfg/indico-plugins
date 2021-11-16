# This file is part of the Indico plugins.
# Copyright (C) 2002 - 2021 CERN
#
# The Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License;
# see the LICENSE file for more details.

from werkzeug.exceptions import ServiceUnavailable

from indico.core.config import config
from indico.core.plugins import url_for_plugin


def is_configured():
    """Check whether the plugin is properly configured."""
    from indico_owncloud.plugin import OwncloudPlugin

    server_host = OwncloudPlugin.settings.get('server_host')
    client_id = OwncloudPlugin.settings.get('client_id')
    client_secret = OwncloudPlugin.settings.get('client_secret')

    return bool(server_host and client_id and client_secret)


def get_auth_settings():
    from indico_owncloud.plugin import OwncloudPlugin

    server_host = OwncloudPlugin.settings.get('server_host')
    client_id = OwncloudPlugin.settings.get('client_id')
    client_secret = OwncloudPlugin.settings.get('client_secret', None)
    in_memory_token = OwncloudPlugin.settings.get('in_memory_token', None)

    redirect_uri = url_for_plugin('owncloud.owncloud_auth_callback')
    silent_redirect_uri = url_for_plugin('owncloud.owncloud_auth_renew_callback')

    if not server_host or not client_id:
        raise ServiceUnavailable('Not configured')

    return {
        'server': server_host,
        'storage': 'memory' if in_memory_token else None,
        'openIdConnect': {
            'metadata_url': f'{server_host}/.well-known/openid-configuration',
            'authority': server_host,
            'client_id': client_id,
            'client_secret': client_secret,
            'response_type': 'code',
            'scope': 'openid profile email',
            'redirect_uri': f'{config.BASE_URL}{redirect_uri}',
            'silent_redirect_uri': f'{config.BASE_URL}{silent_redirect_uri}',
        }
    }
