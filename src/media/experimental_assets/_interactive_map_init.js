// IIFE is used intentionally to isolate namespaces between cards of a review session
(function () {
  const cardSide = document.currentScript.dataset.cardSide,
    interactiveEnabled = sessionStorage.getItem("interactiveEnabled"),
    isMobile = document.documentElement.classList.contains("mobile"),
    interactiveMobileEnabled = sessionStorage.getItem("interactiveMobileEnabled"),
    regionCode = sessionStorage.getItem("regionCode"),
    toolTipEnabled = sessionStorage.getItem("showTooltipOnAnswer"),
    commonSelectors = {
      interactiveMap: ".value--map",
      staticMap: ".value--image",
      mapTooltip: "body > div.jvm-tooltip",
      hiddenTextarea: "textarea#typeans"
    },
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
      selector: commonSelectors.interactiveMap,
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

  clearTooltips();

  if (+interactiveEnabled
    && ((isMobile && +interactiveMobileEnabled) || !isMobile)
    && regionCode) {
    if (cardSide === "question")
      initFrontMap();
    else if (cardSide === "answer")
      initBackMap();
  }


  /**
   * Initialization of the map displayed on the front side of the card
   */
  function initFrontMap() {
    enableInteractiveMapMode();

    new jsVectorMap({
      ...commonMapProps,
      regionsSelectable: true,
      regionsSelectableOne: true,
      showTooltip: false,

      regionStyle: {
        ...commonMapProps.regionStyle,
        selected: {fill: commonMapHexColors.selectedLandMass}
      },

      onRegionSelected: swapToBackSide,
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
        tooltip._tooltip.style.backgroundColor = commonMapHexColors.tooltipBackground;
        tooltip._tooltip.style.color = commonMapHexColors.tooltipText;
      }
    });
  }

  /**
   * Jsvectormap logic incompatibility with project specifics - tooltips are inserted
   * as direct children of &lt;body&gt; element and get persisted during cards review session
   * accumulating and littering the canvas. Current handling is temporary fix until library issue is resolved
   */
  function clearTooltips() {
    document.querySelectorAll(commonSelectors.mapTooltip).forEach(x => x.remove());
  }

  /**
   * Hide the display of static fallback and show the interactive map.
   * Note, that static fallback is specifically displayed by default in case interactive map initialization fails
   */
  function enableInteractiveMapMode() {
    document.querySelector(commonSelectors.staticMap).style.display = "none";
    document.querySelector(commonSelectors.interactiveMap).style.display = "block";
  }

  /**
   * After region on the front card side is selected persist its region code and
   * swap the card to back side if configuration allows to do so. The action is
   * achieved via sending "Enter" key event on manually defined hidden text area
   */
  function swapToBackSide(selectedRegionCode) {
    sessionStorage.setItem("selectedRegion", selectedRegionCode);

    if (!+sessionStorage.getItem("showAnswerOnRegionSelectEnabled"))
      return

    let hiddenTextarea = document.querySelector(commonSelectors.hiddenTextarea);

    if (!hiddenTextarea.onkeypress)
      hiddenTextarea.onkeypress = () => _typeAnsPress();

    if (typeof AnkiDroidJS !== "undefined") {
      showAnswer();
    } else {
      hiddenTextarea.dispatchEvent(new KeyboardEvent("keypress", {code: "Enter"}));
    }
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
