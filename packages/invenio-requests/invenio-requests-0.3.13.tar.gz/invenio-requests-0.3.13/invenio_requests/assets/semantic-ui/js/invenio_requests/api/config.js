// This file is part of Invenio-requests
// Copyright (C) 2022 CERN.
//
// Invenio-requests is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import axios from "axios";

const apiConfig = {
  withCredentials: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X_CSRFTOKEN",
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
};

export const http = axios.create(apiConfig);

/**
 * Wrap a promise to be cancellable and avoid potential memory leaks
 * https://reactjs.org/blog/2015/12/16/ismounted-antipattern.html
 * @param promise the promise to wrap
 * @returns {Object} an object containing the promise to resolve and a `cancel` fn to reject the promise
 */
export const withCancel = (promise) => {
  let isCancelled = false;

  const wrappedPromise = new Promise((resolve, reject) => {
    promise.then(
      (val) => (isCancelled ? reject("UNMOUNTED") : resolve(val)),
      (error) => (isCancelled ? reject("UNMOUNTED") : reject(error))
    );
  });

  return {
    promise: wrappedPromise,
    cancel() {
      isCancelled = true;
    },
  };
};
