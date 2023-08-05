import React from "react";

export const RequestActionContext = React.createContext({
  modalOpen: false,
  toggleModal: () => {},
  linkExtractor: undefined,
  requestApi: undefined,
  performAction: () => {},
  error: undefined,
  loading: false,
});
