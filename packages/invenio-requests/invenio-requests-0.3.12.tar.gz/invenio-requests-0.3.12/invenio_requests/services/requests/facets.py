# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-RDM-Records is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Facet definitions."""

from flask_babelex import gettext as _
from invenio_records_resources.services.records.facets import TermsFacet

type = TermsFacet(
    field='type',
    label=_('Type'),
)

status = TermsFacet(
    field='status',
    label=_('Status'),
)
