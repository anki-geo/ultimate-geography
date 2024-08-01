// IIFE is used intentionally to isolate namespaces between cards of a review session
(function () {
  clearTooltips();

  const cardSide = document.currentScript.dataset.cardSide,
    interactiveEnabled = sessionStorage.getItem("interactiveEnabled"),
    isMobile = document.documentElement.classList.contains("mobile"),
    interactiveMobileEnabled = sessionStorage.getItem("interactiveMobileEnabled"),
    regionCode = sessionStorage.getItem("regionCode"),
    toolTipEnabled = sessionStorage.getItem("showTooltipOnAnswer"),
    commonMapHexColors = {
      bodyOfWater: "#b3dff5",
      landMass: "#fdfbe5",
      selectedLandMass: "#e7f3ea",
      border: "#757674",
      highlightedRegion: "#c02637",
      highlightedCorrectRegion: "#329446",
      tooltipBackground: "#fdfbe5",
      tooltipText: "#000000"
    },
    commonMapProps = {
      selector: "#map",
      map: "world",
      zoomButtons: false,
      backgroundColor: commonMapHexColors.bodyOfWater,
      regionStyle: {
        initial: {
          fill: commonMapHexColors.landMass,
          stroke: commonMapHexColors.border,
          strokeWidth: 1
        }
      }
    };

  if (+interactiveEnabled
    && ((isMobile && +interactiveMobileEnabled) || !isMobile)
    && regionCode) {
    if (cardSide === "question")
      initFrontMap();
    else if (cardSide === "answer")
      initBackMap();
  }


  /**
   * Jsvectormap logic incompatibility with project specifics - tooltips are inserted
   * as direct children of &lt;body&gt; element and get persisted during cards review session
   * accumulating and littering the canvas. Current handling is temporary fix until library issue is resolved
   */
  function clearTooltips() {
    document.querySelectorAll("body > div.jvm-tooltip").forEach(x => x.remove());
  }

  /**
   * Initialization of the map displayed on the front side of the card
   */
  function initFrontMap() {
    enableInteractiveMapMode();

    // Set event handler to swap card to answer side on "Enter" press
    document.querySelector("textarea#typeans").onkeypress = () => _typeAnsPress();

    new jsVectorMap({
      ...commonMapProps,
      regionsSelectable: true,
      regionsSelectableOne: true,
      showTooltip: false,

      regionStyle: {
        ...commonMapProps.regionStyle,
        selected: {fill: commonMapHexColors.selectedLandMass}
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

  /**
   * Initialization of the map displayed on the back side of the card
   */
  function initBackMap() {
    enableInteractiveMapMode();

    new jsVectorMap({
      ...commonMapProps,
      selectedRegions: [regionCode],
      showTooltip: !!+toolTipEnabled,

      regionStyle: {
        ...commonMapProps.regionStyle,
        selected: {fill: getGreenRedRegionColor()}
      },
      focusOn: {
        region: regionCode,
        animate: true
      },

      onRegionTooltipShow(event, tooltip) {
        tooltip._tooltip.style["background-color"] = commonMapHexColors.tooltipBackground;
        tooltip._tooltip.style["color"] = commonMapHexColors.tooltipText;
      }
    });
  }

  /**
   * Hide the display of static fallback and show the interactive map.
   * Note, that static fallback is specifically displayed by default in case interactive map initialization fails
   */
  function enableInteractiveMapMode() {
    document.querySelector(".value--image").style.display = "none";
    document.querySelector(".value--map").style.display = "block";
  }

  /**
   * Retrieve region highlighting color for answer card side
   * @returns {string} - Green hex code if and only if green highlighting
   * mode is enabled and region is selected correctly, red hex code otherwise
   */
  function getGreenRedRegionColor() {
    return !!+sessionStorage.getItem("greenRedRegionEnabled")
    && regionCode === sessionStorage.getItem("selectedRegion")
      ? commonMapHexColors.highlightedCorrectRegion
      : commonMapHexColors.highlightedRegion;
  }
}())
