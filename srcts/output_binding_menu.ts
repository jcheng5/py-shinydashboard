import { BindScope } from "rstudio-shiny/srcts/types/src/shiny/bind";
import { ErrorsMessageValue } from "rstudio-shiny/srcts/types/src/shiny/shinyapp";
import { ensureActivatedTab, deactivateOtherTabs } from "./tabs";

// menuOutputBinding
// ------------------------------------------------------------------
// Based on Shiny.htmlOutputBinding, but instead of putting the result in a
// wrapper div, it replaces the origin DOM element with the new DOM elements,
// copying over the ID and class.
var menuOutputBinding = new Shiny.OutputBinding();
$.extend(menuOutputBinding, {
  find: function (scope: BindScope) {
    return $(scope).find(".shinydashboard-menu-output");
  },
  onValueError: function (el: HTMLElement, err: ErrorsMessageValue) {
    Shiny.unbindAll(el);
    this.renderError(el, err);
  },
  renderValue: function (el: HTMLElement, data: any) {
    Shiny.unbindAll(el);

    var html;
    var dependencies = [];
    if (data === null) {
      return;
    } else if (typeof data === "string") {
      html = data;
    } else if (typeof data === "object") {
      html = data.html;
      dependencies = data.deps;
    }

    var $html = $($.parseHTML(html));

    // Convert the inner contents to HTML, and pass to renderHtml
    Shiny.renderHtml($html.html(), el, dependencies);

    // Extract class of wrapper, and add them to the wrapper element
    el.className =
      "shinydashboard-menu-output shiny-bound-output " + $html.attr("class");

    Shiny.initializeInputs(el);
    Shiny.bindAll(el);
    if ($(el).hasClass("sidebar-menu")) ensureActivatedTab(); // eslint-disable-line
  },
});
Shiny.outputBindings.register(
  menuOutputBinding,
  "shinydashboard.menuOutputBinding"
);
