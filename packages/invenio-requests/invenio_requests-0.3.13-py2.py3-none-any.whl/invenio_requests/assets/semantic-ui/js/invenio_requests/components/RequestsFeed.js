// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React from "react";
import { Feed, Container, Icon } from "semantic-ui-react";
import PropTypes from "prop-types";
import { Image } from "react-invenio-forms";

// Wrapper component for the custom styles being used inside the request events timeline
// Enables centralizing the styles and abstracts it away from the template
export const RequestsFeed = ({ children }) => (
  <Container className="requests-feed-container">
    <Feed>{children}</Feed>
  </Container>
);

export const RequestEventItem = ({ children }) => (
  <div className="requests-event-item">
    <div className="requests-event-container">{children}</div>
  </div>
);

export const RequestEventInnerContainer = ({ children, isEvent }) => (
  <div className={`requests-event-inner-container${isEvent ? " thread" : ""}`}>{children}</div>
);

export const RequestEventAvatarContainer = ({ src, ...uiProps }) => (
  <div className="requests-avatar-container">
    <Image
      src="/static/images/square-placeholder.png"
      as={Image}
      rounded
      avatar
      {...uiProps}
    />
  </div>
);

export const RequestEventItemIconContainer = ({ name, size, color }) => (
  <div className="requests-action-event-icon">
    <Icon name={name} size={size} color={color} />
  </div>
);

export const RequestEventItemBody = ({ isActionEvent, ...props }) => (
  <Feed.Event
    {...props}
    className={isActionEvent ? "requests-action-event" : ""}
  />
);

RequestEventItemBody.propTypes = {
  isActionEvent: PropTypes.bool,
};
RequestEventItemBody.defaultProps = {
  isActionEvent: false,
};

RequestsFeed.Content = RequestEventInnerContainer;
RequestsFeed.Avatar = RequestEventAvatarContainer;
RequestsFeed.Icon = RequestEventItemIconContainer;
RequestsFeed.Item = RequestEventItem;
RequestsFeed.Event = RequestEventItemBody;

export default RequestsFeed;
