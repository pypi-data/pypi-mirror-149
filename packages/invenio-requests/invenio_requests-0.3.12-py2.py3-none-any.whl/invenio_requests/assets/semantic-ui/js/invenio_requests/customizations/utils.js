// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

export function buildRequestTypeUID(elementName, requestType, overridableId='', appName='') {
  const _overridableId = overridableId ? `.${overridableId}` : '';
  const _requestType = requestType ? `.${requestType}` : '';
  const _appName = appName ? `${appName}.` : '';

  return `${_appName}${elementName}${_requestType}${_overridableId}`;
}
