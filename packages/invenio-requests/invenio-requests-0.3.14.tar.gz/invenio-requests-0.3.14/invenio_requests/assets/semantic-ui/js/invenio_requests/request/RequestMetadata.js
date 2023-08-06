// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { Component } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import { Divider, Header, Image, Label } from "semantic-ui-react";
import { i18next } from "@translations/invenio_requests/i18next";
import RequestStatusIcon from "./RequestStatusIcon";

class RequestMetadata extends Component {
  render() {
    const { request } = this.props;
    return (
      <Overridable id="InvenioRequest.RequestMetadata.Layout" {...this.props}>
        <>
          <Header as="h4">{i18next.t("Requestor")}</Header>
          <Image src="/static/images/square-placeholder.png" avatar rounded />
          <span>{request.created_by.full_name}</span>
          <Divider />
          <Header as="h4">{i18next.t("Request type")}</Header>
          <Label>{request.type}</Label>
          <Divider />
          <Header as="h4">{i18next.t("Status")}</Header>
          <RequestStatusIcon status={request.status} />
          {request.status}
          {request.expires_at && (
            <>
              <Divider />
              <Header as="h4">{i18next.t("Expires")}</Header>
              {request.state}
            </>
          )}
          <Divider hidden />
        </>
      </Overridable>
    );
  }
}

RequestMetadata.propTypes = {
  request: PropTypes.object.isRequired,
};

export default Overridable.component(
  "InvenioRequests.RequestMetadata",
  RequestMetadata
);
