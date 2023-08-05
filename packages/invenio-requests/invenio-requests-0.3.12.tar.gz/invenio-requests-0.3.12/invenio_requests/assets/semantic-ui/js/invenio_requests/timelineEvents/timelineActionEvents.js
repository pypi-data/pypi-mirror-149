// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import TimelineActionEvent from "../components/TimelineActionEvent";
import { i18next } from "@translations/invenio_requests/i18next";

export const TimelineAcceptEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="check circle"
    iconColor="green"
    event={event}
    eventContent={i18next.t("accepted this request")}
  />
);

export const TimelineDeclineEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="close"
    event={event}
    eventContent={i18next.t("declined this request")}
    iconColor="red"
  />
);

export const TimelineExpireEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="calendar times"
    event={event}
    eventContent={i18next.t("this request expired")}
    userAction={false}
    iconColor="red"
  />
);

export const TimelineCancelEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="close"
    event={event}
    eventContent={i18next.t("cancelled this request")}
    iconColor="red"
  />
);

export const TimelineUnknownEvent = ({ event }) => (
  <TimelineActionEvent
    iconName="close"
    iconColor="red"
    event={event}
    eventContent={i18next.t("unknown event")}
    userAction={false}
  />
);
