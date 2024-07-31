// IIFE used specifically to isolate namespaces between cards
(function () {
  //temporary hack to remove jvm tooltip
  document.querySelectorAll("body > div.jvm-tooltip").forEach(x => x.remove());

  let interactiveEnabled = sessionStorage.getItem("interactiveEnabled"),
    isMobile = document.documentElement.classList.contains("mobile"),
    interactiveMobileEnabled = sessionStorage.getItem("interactiveMobileEnabled"),
    regionCode = sessionStorage.getItem("regionCode");

  if (+interactiveEnabled
    && ((isMobile && +interactiveMobileEnabled) || !isMobile)
    && regionCode)
    interactiveMapMode();

  function interactiveMapMode() {
    // Static fallback is specifically enabled by default (if script fails to load)
    // And gets hidden when interactive map succeeds to proceed
    document.querySelector(".value--image").style.display = "none";
    document.querySelector(".value--map").style.display = "block";

    // Set event handler to swap card to answer side on "Enter" press
    document.querySelector("textarea#typeans").onkeypress = () => _typeAnsPress();

    new jsVectorMap({
      selector: "#map-front",
      map: "world",
      zoomButtons: false,
      backgroundColor: "#b3dff5",
      regionsSelectable: true,
      regionsSelectableOne: true,
      showTooltip: false,

      regionStyle: {
        initial: {
          fill: "#fdfbe5",
          stroke: "#757674",
          strokeWidth: 1
        },
        selected: {fill: "#e7f3ea"}
      },

      onRegionSelected(code) {
        // Persist selected region for Green/Red logic (see Back Template)
        sessionStorage.setItem("selectedRegion", code);

        if (+sessionStorage.getItem("showAnswerOnRegionSelectEnabled")) {
          // Show answer hack
          //AnkiDroid requires use of API instead of event dispatch
          if (typeof AnkiDroidJS !== "undefined") {
            showAnswer();
          } else {
            // Simulate pressing "Enter" on the input element to show the answer
            let input = document.querySelector("textarea#typeans");
            let ev = new KeyboardEvent("keypress", {code: "Enter"});
            input.dispatchEvent(ev);
          }
        }
      },
    });
  }
}())
