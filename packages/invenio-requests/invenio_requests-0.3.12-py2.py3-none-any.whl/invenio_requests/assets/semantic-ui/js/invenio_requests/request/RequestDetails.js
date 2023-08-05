// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import RequestMetadata from "./RequestMetadata";
import React, { Component } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import { Grid } from "semantic-ui-react";
import { Timeline } from "../timeline";

class RequestDetails extends Component {
  render() {
    const { request } = this.props;
    return (
      <Overridable id="InvenioRequests.RequestDetails.layout" {...this.props}>
        <>
          <Grid stackable reversed="mobile">
            <Grid.Column width={13}>
              <Timeline />
            </Grid.Column>
            <Grid.Column width={3}>
              <RequestMetadata request={request} />
            </Grid.Column>
          </Grid>
        </>
      </Overridable>
    );
  }
}

RequestDetails.propTypes = {
  request: PropTypes.object.isRequired,
};

export default Overridable.component(
  "InvenioRequests.RequestDetails",
  RequestDetails
);
