// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import React, { Component } from "react";
import { Feed } from "semantic-ui-react";
import { TimelineEventBody } from "./TimelineEventBody";
import { Image } from "react-invenio-forms";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import RequestsFeed from "./RequestsFeed";
import { timestampToRelativeTime } from "../timelineEvents/utils";

class TimelineActionEvent extends Component {
  render() {
    const { event, iconName, iconColor, userAction, eventContent } = this.props;

    return (
      <Overridable
        id="TimelineActionEvent.layout"
        event={event}
        iconName={iconName}
        iconColor={iconColor}
        userAction={userAction}
      >
        <RequestsFeed.Item>
          <RequestsFeed.Content isEvent={true}>
            <RequestsFeed.Icon name={iconName} size="large" color={iconColor} />
            <RequestsFeed.Event isActionEvent={true}>
              <Feed.Label>
                {userAction && (
                  <Image
                    src="/static/images/square-placeholder.png"
                    as={Image}
                    avatar
                  />
                )}
              </Feed.Label>
              <Feed.Content>
                <Feed.Summary>
                  {userAction && (
                    <Feed.User as="a">{event.created_by?.user}</Feed.User>
                  )}{" "}
                  <TimelineEventBody
                    content={eventContent}
                    format={event?.payload?.format}
                  />
                  <Feed.Date>
                    {timestampToRelativeTime(event.created)}
                  </Feed.Date>
                </Feed.Summary>
              </Feed.Content>
            </RequestsFeed.Event>
          </RequestsFeed.Content>
        </RequestsFeed.Item>
      </Overridable>
    );
  }
}

TimelineActionEvent.propTypes = {
  event: PropTypes.object.isRequired,
  iconName: PropTypes.string.isRequired,
  eventContent: PropTypes.string.isRequired,
  iconColor: PropTypes.string,
  userAction: PropTypes.bool,
};

TimelineActionEvent.defaultProps = {
  iconColor: "grey",
  userAction: true,
};

export default Overridable.component(
  "TimelineActionEvent",
  TimelineActionEvent
);
