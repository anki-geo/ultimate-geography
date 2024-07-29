// IIFE used specifically to isolate namespaces between cards
(function () {
  let regionCode = sessionStorage.getItem("regionCode");

  if (+sessionStorage.getItem("interactiveEnabled") && regionCode)
    interactiveMapMode();
  else
    staticMapFallbackMode();

  function interactiveMapMode() {
    document.querySelector(".value--map").style.display = "block";

    // Green/Red region highlighting color depending on user answer
    let color = !!+sessionStorage.getItem("greenRedRegionEnabled")
    && regionCode === sessionStorage.getItem("selectedRegion")
      ? "#329446" // green if both enabled and region selected is correct
      : "#c02637"; // red otherwise

    new jsVectorMap({
      selector: "#map-back",
      map: "world",
      zoomButtons: false,
      selectedRegions: [regionCode],
      backgroundColor: "#b3dff5",

      focusOn: {
        region: regionCode,
        animate: true
      },
      regionStyle: {
        initial: {
          fill: "#fdfbe5",
          stroke: "#757674",
          strokeWidth: 1
        },
        selected: {fill: color}
      },

      onRegionTooltipShow(event, tooltip) {
        tooltip._tooltip.style["background-color"] = "#fdfbe5";
        tooltip._tooltip.style["color"] = "black";
      }
    });
  }

  function staticMapFallbackMode() {
    document.querySelector(".value--image").style.display = "block";
  }
}())
