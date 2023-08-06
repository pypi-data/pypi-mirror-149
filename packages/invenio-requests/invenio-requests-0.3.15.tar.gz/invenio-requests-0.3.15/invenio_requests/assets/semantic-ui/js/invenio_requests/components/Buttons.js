// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.
import { i18next } from "@translations/invenio_requests/i18next";

import React from "react";
import { Button } from "semantic-ui-react";

export const SaveButton = (props) => (
  <Button icon="save" positive size="mini" content={i18next.t("Save")} {...props} />
);

export const CancelButton = (props) => (
  <Button icon="cancel" content={i18next.t("Cancel")} size="mini" {...props} />
);
