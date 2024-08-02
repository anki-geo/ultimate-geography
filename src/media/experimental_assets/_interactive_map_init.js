// IIFE is used intentionally to isolate namespaces between cards of a review session
(function () {
  const commonConfig = {
      interactiveEnabled: sessionGetBool("interactiveEnabled"),
      interactiveMobileEnabled: sessionGetBool("interactiveMobileEnabled"),
      toolTipEnabled: sessionGetBool("showTooltipOnAnswer"),
      autoAnswerEnabled: sessionGetBool("showAnswerOnRegionSelectEnabled"),
      greenRedEnabled: sessionGetBool("greenRedRegionEnabled"),
      isMobile: document.documentElement.classList.contains("mobile"),

      mapHighDetail: sessionGetBool("mapHighDetail"),
      regionCode: sessionGetString("regionCode"),
      cardSide: document.currentScript.dataset.cardSide,

      questionCardSideName: "question",
      answerCardSideName: "answer",
      mapSvgId: sessionGetBool("mapHighDetail") ? "world_high_detail" : "world_low_detail",
      selectedRegionSessionKey: "selectedRegion"
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
      map: commonConfig.mapSvgId,
      zoomButtons: false,
      zoomMax: 25,
      backgroundColor: commonColors.bodyOfWater,
      regionStyle: {
        initial: {
          fill: commonColors.landMass,
          stroke: commonColors.border,
          strokeWidth: commonConfig.mapHighDetail ? 0.2 : 1
        }
      }
    };

  clearTooltips();

  if (resolveInteractiveEnabled() && commonConfig.regionCode) {
    interactiveMapMode(true);
    try {
      if (commonConfig.cardSide === commonConfig.questionCardSideName)
        initFrontMap();
      else if (commonConfig.cardSide === commonConfig.answerCardSideName)
        initBackMap();
    } catch (e) {
      interactiveMapMode(false);
      throw e;
    }
  }


  /**
   * Shortcut function of value retrieval from sessionStorage
   */
  function sessionGetString(key) {
    return sessionStorage.getItem(key);
  }

  /**
   * Returns true if and only if key is equal to "1" and false otherwise
   */
  function sessionGetBool(key) {
    return +sessionGetString(key) === 1;
  }

  /**
   * Using configuration options determine whether to display interactive map
   */
  function resolveInteractiveEnabled() {
    return commonConfig.interactiveEnabled && (nonMobile() || interactiveMobileEnabled())
  }

  /**
   * @returns {boolean} true when device is not mobile, false otherwise
   */
  function nonMobile() {
    return !commonConfig.isMobile
  }

  /**
   * @returns {boolean} true if and only if the device is mobile
   * and interactive map is enabled
   */
  function interactiveMobileEnabled() {
    return commonConfig.isMobile && commonConfig.interactiveMobileEnabled;
  }

  /**
   * Initialization of the map displayed on the front side of the card
   */
  function initFrontMap() {
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

      ...mobileDraggingHack(commonConfig.toolTipEnabled, (event, tooltip) => {
        tooltip._tooltip.style.backgroundColor = commonColors.tooltipBackground;
        tooltip._tooltip.style.color = commonColors.tooltipText;
      })
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
   * Set interactive display map mode based on passed boolean argument
   * Note, that static fallback is specifically displayed by default in case current script fails to be loaded
   */
  function interactiveMapMode(enabled) {
    commonElements.staticMap.style.display = enabled ? "none" : "block";
    commonElements.interactiveMap.style.display = enabled ? "block" : "none";
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
    sessionStorage.setItem(commonConfig.selectedRegionSessionKey, selectedRegionCode);

    if (!commonConfig.autoAnswerEnabled)
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
    return commonConfig.greenRedEnabled
    && commonConfig.regionCode === sessionGetString(commonConfig.selectedRegionSessionKey)
      ? commonColors.highlightedCorrectRegion
      : commonColors.highlightedRegion;
  }
}())
