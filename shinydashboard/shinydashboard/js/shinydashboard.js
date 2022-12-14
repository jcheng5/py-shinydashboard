(() => {
  // tabs.ts
  function deactivateOtherTabs() {
    var $tablinks = $(
      ".nav-sidebar a[data-toggle='tab'],.nav-sidebar li.treeview > a"
    );
    $tablinks.not($(this)).parent("li").removeClass("active");
    var $obj = $(".sidebarMenuSelectedTabItem");
    var inputBinding = $obj.data("shiny-input-binding");
    if (typeof inputBinding !== "undefined") {
      inputBinding.setValue($obj, $(this).attr("data-value"));
      $obj.trigger("change");
    }
  }
  $(document).on(
    "shown.bs.tab",
    '.nav-sidebar a[data-toggle="tab"]',
    deactivateOtherTabs
  );
  function ensureActivatedTab() {
    var $tablinks = $(".nav-sidebar a[data-bs-toggle='tab']");
    var $startTab = $tablinks.filter("[data-start-selected='1']");
    if ($startTab.length === 0) {
      $startTab = $tablinks.first();
    }
    if ($startTab.length !== 0) {
      $startTab.tab("show");
      $(".sidebarMenuSelectedTabItem").attr(
        "data-value",
        $startTab.attr("data-value")
      );
    }
  }
  document.addEventListener("DOMContentLoaded", () => ensureActivatedTab());

  // output_binding_menu.ts
  var menuOutputBinding = new Shiny.OutputBinding();
  $.extend(menuOutputBinding, {
    find: function(scope) {
      return $(scope).find(".shinydashboard-menu-output");
    },
    onValueError: function(el, err) {
      Shiny.unbindAll(el);
      this.renderError(el, err);
    },
    renderValue: function(el, data) {
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
      Shiny.renderHtml($html.html(), el, dependencies);
      el.className = "shinydashboard-menu-output shiny-bound-output " + $html.attr("class");
      Shiny.initializeInputs(el);
      Shiny.bindAll(el);
      if ($(el).hasClass("sidebar-menu"))
        ensureActivatedTab();
    }
  });
  Shiny.outputBindings.register(
    menuOutputBinding,
    "shinydashboard.menuOutputBinding"
  );
})();
