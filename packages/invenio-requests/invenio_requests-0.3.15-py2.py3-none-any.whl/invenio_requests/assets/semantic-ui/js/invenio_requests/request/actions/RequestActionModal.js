// This file is part of InvenioRequests
// Copyright (C) 2022 CERN.
//
// Invenio RDM Records is free software; you can redistribute it and/or modify it
// under the terms of the MIT License; see LICENSE file for more details.

import { RequestActionContext } from "@js/invenio_requests/request/actions/context";
import { i18next } from "@translations/invenio_requests/i18next";
import PropTypes from "prop-types";
import React, { Component } from "react";
import { Trans } from "react-i18next";
import Overridable from "react-overridable";
import { Button, Modal } from "semantic-ui-react";
import Error from "../../components/Error";

export class RequestActionModal extends Component {
  static contextType = RequestActionContext;

  componentDidMount() {
    this.subscribeToContext();
  }

  subscribeToContext = () => {
    const { modalId } = this.props;
    const { modalOpen } = this.context;
    if (modalId in modalOpen) {
      modalOpen[modalId] = false;
    }
  };

  render() {
    const { action, handleActionClick, modalId, children } = this.props;
    const { modalOpen, loading, toggleModal, error, cleanError } = this.context;

    const currentModalOpen = modalOpen[modalId];

    return (
      <Overridable
        id="InvenioRequests.RequestActionModal.layout"
        {...this.props}
      >
        {/*currentModalOpen prevents mounting multiple instances*/}
        {currentModalOpen && (
          <Modal open={currentModalOpen}>
            <Modal.Header>
              <Trans
                defaults="{{action}} request"
                values={{ action: action }}
              />
            </Modal.Header>
            <Modal.Content>
              <Modal.Description>
                {error && <Error error={error.message} />}
                {children}
              </Modal.Description>
            </Modal.Content>
            <Modal.Actions>
              <Button
                onClick={() => {
                  cleanError();
                  toggleModal(modalId, false);
                }}
                loading={loading}
                floated="left"
              >
                {i18next.t("Cancel")}
              </Button>
              <Button onClick={handleActionClick} loading={loading}>
                <Trans defaults="{{action}}" values={{ action: action }} />
              </Button>
            </Modal.Actions>
          </Modal>
        )}
      </Overridable>
    );
  }
}

RequestActionModal.propTypes = {
  handleActionClick: PropTypes.func.isRequired,
  modalId: PropTypes.string.isRequired,
};

RequestActionModal.defaultProps = {
  loading: false,
  modalOpen: false,
};

export default Overridable.component(
  "InvenioRequests.RequestActionModal",
  RequestActionModal
);
