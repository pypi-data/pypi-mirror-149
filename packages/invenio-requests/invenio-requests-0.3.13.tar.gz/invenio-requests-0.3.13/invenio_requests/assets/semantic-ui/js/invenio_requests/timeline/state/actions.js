// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { updateRequest } from "../../request/state/actions";

export const IS_LOADING = "timeline/IS_LOADING";
export const SUCCESS = "timeline/SUCCESS";
export const HAS_ERROR = "timeline/HAS_ERROR";
export const IS_REFRESHING = "timeline/REFRESHING";
export const CHANGE_PAGE = "timeline/CHANGE_PAGE";

class intervalManager {
  static IntervalId = undefined;

  static setIntervalId(intervalId) {
    this.intervalId = intervalId;
  }
}

export const fetchTimeline = (loadingState = true) => {
  return async (dispatch, getState, config) => {
    const state = getState();
    const { size, page, data: timelineData } = state.timeline;

    if (loadingState) {
      dispatch({
        type: IS_LOADING,
      });
    }
    dispatch({
      type: IS_REFRESHING,
    });

    try {
      const response = await config.requestsApi.getTimeline({
        size: size,
        page: page,
        sort: "oldest",
      });

      // Check if timeline has more events than the current state
      const hasMoreEvents =
        response.data?.hits?.total > timelineData?.hits?.total;
      if (hasMoreEvents) {
        // Check if a LogEvent was added and fetch request
        const actionEventFound = response.data.hits.hits.some(
          (event) =>
            event.type === "L" &&
            config.requestsApi.availableRequestStatuses.includes(
              event?.payload?.event
            )
        );

        if (actionEventFound) {
          const response = await config.requestsApi.getRequest();
          dispatch(updateRequest(response.data));
        }
      }

      dispatch({
        type: SUCCESS,
        payload: response.data,
      });
    } catch (error) {
      dispatch({
        type: HAS_ERROR,
        payload: error,
      });
    }
  };
};

export const setPage = (page) => {
  return async (dispatch, getState, config) => {
    dispatch({
      type: CHANGE_PAGE,
      payload: page,
    });

    dispatch(fetchTimeline());
  };
};

const timelineReload = (dispatch, getState, config) => {
  const state = getState();
  const { loading, refreshing, error } = state.timeline;
  const { isLoading: isSubmitting } = state.timelineCommentEditor;

  const intervalId = intervalManager.intervalId;
  if (error) {
    // stop requesting if error
    clearInterval(intervalId);
  }

  // avoid concurrent requests if the previous one did not finish
  return (
    !loading && !refreshing && !isSubmitting && dispatch(fetchTimeline(false))
  );
};

export const getTimelineWithRefresh = () => {
  return async (dispatch, getState, config) => {
    dispatch(fetchTimeline(true));

    const intervalAlreadySet = intervalManager.intervalId;

    if (!intervalAlreadySet) {
      const intervalId = setInterval(
        () => timelineReload(dispatch, getState, config),
        config.refreshIntervalMs
      );
      intervalManager.setIntervalId(intervalId);
    }
  };
};

export const timelineStopRefresh = () => {
  return (dispatch, getState, config) => {
    const intervalId = intervalManager.intervalId;
    clearInterval(intervalId);
  };
};
