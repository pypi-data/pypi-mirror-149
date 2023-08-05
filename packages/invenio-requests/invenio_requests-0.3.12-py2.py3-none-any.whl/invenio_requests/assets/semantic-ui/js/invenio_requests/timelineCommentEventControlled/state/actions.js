// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { IS_REFRESHING, SUCCESS } from "../../timeline/state/actions";
import { payloadSerializer } from "../../api/serializers";
import _cloneDeep from "lodash/cloneDeep";

export const updateComment = ({ content, format, event }) => {
  return async (dispatch, getState, config) => {
    const commentsApi = config.requestEventsApi(event.links);

    const payload = payloadSerializer(content, format);

    dispatch({ type: IS_REFRESHING });

    const response = await commentsApi.updateComment(payload);

    dispatch({
      type: SUCCESS,
      payload: _newStateWithUpdate(response.data, getState().timeline.data),
    });

    return response.data;
  };
};

export const deleteComment = ({ event }) => {
  return async (dispatch, getState, config) => {
    const commentsApi = config.requestEventsApi(event.links);

    dispatch({ type: IS_REFRESHING });

    const response = await commentsApi.deleteComment();

    dispatch({
      type: SUCCESS,
      payload: _newStateWithDelete(event.id, getState().timeline.data),
    });

    return response.data;
  };
};

const _newStateWithUpdate = (updatedComment, currentState) => {
  const timelineState = _cloneDeep(currentState);

  const currentHits = timelineState.hits.hits;

  const currentCommentKey = currentHits.findIndex(
    (comment) => comment.id === updatedComment.id
  );

  currentHits[currentCommentKey] = updatedComment;

  return timelineState;
};

const _newStateWithDelete = (eventId, currentState) => {
  const timelineState = _cloneDeep(currentState);

  const currentHits = timelineState.hits.hits;

  const currentComment = currentHits.find((comment) => comment.id === eventId);

  delete currentComment.payload;

  return timelineState;
};
