// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import ReactDOM from "react-dom";
import { InvenioRequestsApp } from "./InvenioRequestsApp";
import {
  TimelineAcceptEvent,
  TimelineCancelEvent,
  TimelineDeclineEvent,
  TimelineExpireEvent,
  TimelineUnknownEvent,
} from "./timelineEvents";
import {
  IconSubmitStatus,
  IconDeleteStatus,
  IconAcceptStatus,
  IconDeclineStatus,
  IconCancelStatus,
  IconExpireStatus,
} from "./request";

const requestDetailsDiv = document.getElementById("request-detail");
const request = JSON.parse(requestDetailsDiv.dataset.record);
const defaultQueryParams = JSON.parse(
  requestDetailsDiv.dataset.defaultQueryConfig
);

const overriddenComponents = {
  "TimelineEvent.layout.unknown": TimelineUnknownEvent,
  "TimelineEvent.layout.declined": TimelineDeclineEvent,
  "TimelineEvent.layout.accepted": TimelineAcceptEvent,
  "TimelineEvent.layout.expired": TimelineExpireEvent,
  "TimelineEvent.layout.cancelled": TimelineCancelEvent,
  "RequestStatusIcon.layout.submitted": IconSubmitStatus,
  "RequestStatusIcon.layout.deleted": IconDeleteStatus,
  "RequestStatusIcon.layout.accepted": IconAcceptStatus,
  "RequestStatusIcon.layout.declined": IconDeclineStatus,
  "RequestStatusIcon.layout.cancelled": IconCancelStatus,
  "RequestStatusIcon.layout.expired": IconExpireStatus,
};

ReactDOM.render(
  <InvenioRequestsApp
    request={request}
    defaultQueryParams={defaultQueryParams}
    overriddenCmps={overriddenComponents}
  />,
  requestDetailsDiv
);
