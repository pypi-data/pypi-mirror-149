# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Request views decorators module."""

from functools import wraps

from flask import g

from invenio_requests.proxies import current_requests


def service():
    """Get the requests service."""
    return current_requests.requests_service


def pass_request(f):
    """Retrieve request record to the view."""

    @wraps(f)
    def view(**kwargs):
        """Decorated view."""
        pid_value = kwargs['pid_value']
        request = service().read(
            id_=pid_value, identity=g.identity
        )
        kwargs['request'] = request
        return f(**kwargs)

    return view
