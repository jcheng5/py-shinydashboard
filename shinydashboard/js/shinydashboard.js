(() => {
  // tabs.ts
  var deactivateOtherTabs = function() {
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
  };
  $(document).on(
    "shown.bs.tab",
    '.nav-sidebar a[data-toggle="tab"]',
    deactivateOtherTabs
  );
  var ensureActivatedTab = function() {
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
  };
  document.addEventListener("DOMContentLoaded", () => ensureActivatedTab());
})();
