/*
 * This file is part of Invenio.
 * Copyright (C) 2017-2020 CERN.
 * Copyright (C) 2021      TU Wien.
 *
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */

// eslint-disable-next-line no-unused-vars
import jquery from "jquery";
import "semantic-ui-css/semantic.js";
import "semantic-ui-less/semantic.less";

// Initialize Semantic UI components
jquery(".ui.dropdown").dropdown();
jquery(".ui.accordion").accordion();

jquery(".message .close").on("click", function () {
  jquery(this).closest(".message").transition({
    animation: "fade",
    duration: 0,
    interval: 0,
  });
});
