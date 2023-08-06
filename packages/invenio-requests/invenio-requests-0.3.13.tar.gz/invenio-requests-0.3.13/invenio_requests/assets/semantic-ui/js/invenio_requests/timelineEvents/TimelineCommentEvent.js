// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import Error from "../components/Error";
import FormattedInputEditor from "../components/FormattedInputEditor";
import React, { Component } from "react";
import { Feed, Image, Container, Dropdown, Grid } from "semantic-ui-react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import { SaveButton, CancelButton } from "../components/Buttons";
import { TimelineEventBody } from "../components/TimelineEventBody";
import { i18next } from "@translations/invenio_requests/i18next";
import RequestsFeed from "../components/RequestsFeed";
import { timestampToRelativeTime } from "../timelineEvents/utils";

class TimelineCommentEvent extends Component {
  constructor(props) {
    super(props);

    const { event } = props;

    this.state = {
      commentContent: event?.payload?.content,
    };
  }

  eventToType = ({ type, payload }) => {
    switch (type) {
      case "L":
        return payload?.event || "unknown";
      case "C":
        return "comment";
      default:
        return "unknown";
    }
  };

  render() {
    const {
      isLoading,
      isEditing,
      error,
      event,
      updateComment,
      deleteComment,
      toggleEditMode,
    } = this.props;
    const { commentContent } = this.state;

    const commentHasBeenEdited = event?.revision_id > 1 && event?.payload;
    const commentHasBeenDeleted = !event?.payload;
    const commentCanBeDeleted = event?.payload;

    const canDelete = event?.permissions?.can_delete_comment;
    const canUpdate = event?.permissions?.can_update_comment;

    return (
      <Overridable
        id={`TimelineEvent.layout.${this.eventToType(event)}`}
        event={event}
      >
        <RequestsFeed.Item>
          <RequestsFeed.Content>
            <RequestsFeed.Avatar
              src="/static/images/square-placeholder.png"
              as={Image}
              circular
            />
            <RequestsFeed.Event>
              <Feed.Content>
                {commentCanBeDeleted && (canDelete || canUpdate) && (
                  <Dropdown
                    icon="ellipsis horizontal"
                    className="right-floated"
                  >
                    <Dropdown.Menu>
                      {canUpdate && (
                        <Dropdown.Item onClick={() => toggleEditMode()}>
                          {i18next.t("Edit")}
                        </Dropdown.Item>
                      )}
                      {canDelete && (
                        <Dropdown.Item onClick={() => deleteComment()}>
                          {i18next.t("Delete")}
                        </Dropdown.Item>
                      )}
                    </Dropdown.Menu>
                  </Dropdown>
                )}
                <Feed.Summary>
                  {/*TODO replace with event.icon and add a translated event description*/}
                  <Feed.User as="a">{event.created_by?.user}</Feed.User>{" "}
                  {i18next.t("commented")}
                  <Feed.Date>
                    {timestampToRelativeTime(event.created)}
                  </Feed.Date>
                </Feed.Summary>

                <Feed.Extra text={!isEditing}>
                  {error && <Error error={error} />}

                  {isEditing ? (
                    <FormattedInputEditor
                      data={event?.payload?.content}
                      onChange={(event, editor) =>
                        this.setState({ commentContent: editor.getData() })
                      }
                      minHeight="100%"
                    />
                  ) : (
                    <TimelineEventBody
                      content={event?.payload?.content}
                      format={event?.payload?.format}
                    />
                  )}

                  {isEditing && (
                    <Container className="mt-15" textAlign="right">
                      <CancelButton onClick={() => toggleEditMode()} />
                      <SaveButton
                        onClick={() => updateComment(commentContent, "html")}
                        loading={isLoading}
                      />
                    </Container>
                  )}
                </Feed.Extra>
                {commentHasBeenEdited ||
                  (commentHasBeenDeleted && (
                    <Feed.Meta>
                      {commentHasBeenEdited && i18next.t("Edited")}
                      {commentHasBeenDeleted && i18next.t("Deleted")}
                    </Feed.Meta>
                  ))}
              </Feed.Content>
            </RequestsFeed.Event>
          </RequestsFeed.Content>
        </RequestsFeed.Item>
      </Overridable>
    );
  }
}

TimelineCommentEvent.propTypes = {
  event: PropTypes.object.isRequired,
  deleteComment: PropTypes.func.isRequired,
  updateComment: PropTypes.func.isRequired,
  toggleEditMode: PropTypes.func.isRequired,
  isLoading: PropTypes.bool,
  isEditing: PropTypes.bool,
  error: PropTypes.string,
};

TimelineCommentEvent.defaultProps = {
  isLoading: false,
  isEditing: false,
  error: undefined,
};

export default Overridable.component("TimelineEvent", TimelineCommentEvent);
