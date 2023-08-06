// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import Error from "../components/Error";
import Loader from "../components/Loader";
import { Pagination } from "../components/Pagination";
import React, { Component } from "react";
import PropTypes from "prop-types";
import Overridable from "react-overridable";
import { Container, Feed, Segment, Divider } from "semantic-ui-react";
import { TimelineCommentEventControlled } from "../timelineCommentEventControlled";
import { TimelineCommentEditor } from "../timelineCommentEditor";
import { DeleteConfirmationModal } from "../components/modals/DeleteConfirmationModal";
import RequestsFeed from "../components/RequestsFeed";

class TimelineFeed extends Component {
  constructor(props) {
    super(props);

    this.state = {
      modalOpen: false,
      modalAction: null,
    };
  }

  componentDidMount() {
    const { getTimelineWithRefresh } = this.props;
    getTimelineWithRefresh();
  }

  componentWillUnmount() {
    const { timelineStopRefresh } = this.props;
    timelineStopRefresh();
  }

  onOpenModal = (action) => {
    this.setState({ modalOpen: true, modalAction: action });
  };

  render() {
    const { timeline, loading, error, setPage, size, page } = this.props;
    const { modalOpen, modalAction } = this.state;

    return (
      <Loader isLoading={loading}>
        <Error error={error}>
          <Overridable id="TimelineFeed.layout" {...this.props}>
            <Container id="requests-timeline">
              <RequestsFeed>
                {timeline.hits?.hits.map((event) => (
                  <TimelineCommentEventControlled
                    key={event.id}
                    event={event}
                    openConfirmModal={this.onOpenModal}
                  />
                ))}
              </RequestsFeed>
              <Divider fitted />
              <Container textAlign="center" className="mb-15 mt-15">
                <Pagination
                  page={page}
                  size={size}
                  setPage={setPage}
                  totalLength={timeline.hits?.total}
                />
              </Container>
              <TimelineCommentEditor />
              <DeleteConfirmationModal
                open={modalOpen}
                action={modalAction}
                onOpen={() => this.setState({ modalOpen: true })}
                onClose={() => this.setState({ modalOpen: false })}
              />
            </Container>
          </Overridable>
        </Error>
      </Loader>
    );
  }
}

TimelineFeed.propTypes = {
  getTimelineWithRefresh: PropTypes.func.isRequired,
  timelineStopRefresh: PropTypes.func.isRequired,
  timeline: PropTypes.object,
  error: PropTypes.object,
  isSubmitting: PropTypes.bool,
  setPage: PropTypes.func.isRequired,
  page: PropTypes.number,
  size: PropTypes.number,
};

export default Overridable.component("TimelineFeed", TimelineFeed);
