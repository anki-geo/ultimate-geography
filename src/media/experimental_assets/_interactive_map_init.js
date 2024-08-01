// IIFE is used intentionally to isolate namespaces between cards of a review session
(function () {
  const commonConfig = {
      regionCode: sessionStorage.getItem("regionCode"),
      cardSide: document.currentScript.dataset.cardSide,
      interactiveEnabled: sessionStorage.getItem("interactiveEnabled"),
      interactiveMobileEnabled: sessionStorage.getItem("interactiveMobileEnabled"),
      isMobile: document.documentElement.classList.contains("mobile"),
      toolTipEnabled: sessionStorage.getItem("showTooltipOnAnswer")
    },
    commonElements = {
      interactiveMap: document.querySelector(".value--map"),
      staticMap: document.querySelector(".value--image"),
      mapTooltips: document.querySelectorAll("body > div.jvm-tooltip"),
      hiddenTextarea: document.querySelector("textarea#typeans")
    },
    commonColors = {
      bodyOfWater: "#b3dff5",
      landMass: "#fdfbe5",
      selectedLandMass: "#e7f3ea",
      border: "#757674",
      highlightedRegion: "#c02637",
      highlightedCorrectRegion: "#329446",
      tooltipBackground: "#fdfbe5",
      tooltipText: "#000000"
    },
    commonMap = {
      selector: commonElements.interactiveMap,
      map: "world",
      zoomButtons: false,
      backgroundColor: commonColors.bodyOfWater,
      regionStyle: {
        initial: {
          fill: commonColors.landMass,
          stroke: commonColors.border,
          strokeWidth: 1
        }
      }
    };

  clearTooltips();

  if (+commonConfig.interactiveEnabled
    && ((commonConfig.isMobile && +commonConfig.interactiveMobileEnabled) || !commonConfig.isMobile)
    && commonConfig.regionCode) {
    if (commonConfig.cardSide === "question")
      initFrontMap();
    else if (commonConfig.cardSide === "answer")
      initBackMap();
  }


  /**
   * Initialization of the map displayed on the front side of the card
   */
  function initFrontMap() {
    enableInteractiveMapMode();

    new jsVectorMap({
      ...commonMap,
      regionsSelectable: true,
      regionsSelectableOne: true,

      regionStyle: {
        ...commonMap.regionStyle,
        selected: {fill: commonColors.selectedLandMass}
      },

      onRegionSelected: swapToBackSide,

      ...mobileDraggingHack(false)
    });
  }

  /**
   * Initialization of the map displayed on the back side of the card
   */
  function initBackMap() {
    enableInteractiveMapMode();

    new jsVectorMap({
      ...commonMap,
      selectedRegions: [commonConfig.regionCode],

      regionStyle: {
        ...commonMap.regionStyle,
        selected: {fill: getGreenRedRegionColor()}
      },
      focusOn: {
        region: commonConfig.regionCode,
        animate: true
      },

      ...mobileDraggingHack(!!+commonConfig.toolTipEnabled, (event, tooltip) => {
        tooltip._tooltip.style.backgroundColor = commonColors.tooltipBackground;
        tooltip._tooltip.style.color = commonColors.tooltipText;
      }),
    });
  }

  /**
   * Jsvectormap logic incompatibility with project specifics - tooltips are inserted
   * as direct children of &lt;body&gt; element and get persisted during cards review session
   * accumulating and littering the canvas. Current handling is temporary fix until library issue is resolved
   */
  function clearTooltips() {
    commonElements.mapTooltips.forEach(x => x.remove());
  }

  /**
   * Hide the display of static fallback and show the interactive map.
   * Note, that static fallback is specifically displayed by default in case interactive map initialization fails
   */
  function enableInteractiveMapMode() {
    commonElements.staticMap.style.display = "none";
    commonElements.interactiveMap.style.display = "block";
  }

  /**
   * Jsvectormap library bug - map dragging does not work on mobile with disabled tooltip.
   * Enable tooltip and hide it in case original tooltip is not displayable.
   * Current handling is temporary fix until library issue is resolved
   */
  function mobileDraggingHack(tooltipEnabled, tooltipShowHandler) {
    return commonConfig.isMobile
      ? {
        showTooltip: true,
        onRegionTooltipShow(event, tooltip) {
          if (tooltipEnabled && tooltipShowHandler)
            tooltipShowHandler(event, tooltip)
          else
            tooltip._tooltip.style.display = "none";
        }
      }
      : {
        showTooltip: tooltipEnabled,
        onRegionTooltipShow: tooltipShowHandler
      }
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

    if (!commonElements.hiddenTextarea.onkeypress)
      commonElements.hiddenTextarea.onkeypress = () => _typeAnsPress();

    if (typeof AnkiDroidJS !== "undefined") {
      showAnswer();
    } else {
      commonElements.hiddenTextarea.dispatchEvent(new KeyboardEvent("keypress", {code: "Enter"}));
    }
  }

  /**
   * Retrieve region highlighting color for answer card side
   * @returns {string} - Green hex code if and only if green highlighting
   * mode is enabled and region is selected correctly, red hex code otherwise
   */
  function getGreenRedRegionColor() {
    return !!+sessionStorage.getItem("greenRedRegionEnabled")
    && commonConfig.regionCode === sessionStorage.getItem("selectedRegion")
      ? commonColors.highlightedCorrectRegion
      : commonColors.highlightedRegion;
  }
}())
