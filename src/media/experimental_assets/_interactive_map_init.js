// IIFE is used intentionally to isolate namespaces between cards of a review session
(function () {
  const mapConfig = getMapConfig();
  const commonConfig = mapConfig.commonConfig;
  const commonColors = mapConfig.commonColors;
  const commonElements = mapConfig.commonElements;
  const commonMap = mapConfig.commonMap;

  clearTooltips();

  if (resolveInteractiveEnabled()) {
    interactiveMapMode(true);
    try {
      if (cardSide(commonConfig.questionCardSideName))
        initFrontMap();
      else if (cardSide(commonConfig.answerCardSideName)) {
        failInvalidRegionCode()
        initBackMap();
      }
    } catch (e) {
      interactiveMapMode(false);
      throw e;
    }
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
   * Set interactive display map mode based on passed boolean argument
   * Note, that static fallback is specifically displayed by default in case current script fails to be loaded
   */
  function interactiveMapMode(enabled) {
    commonElements.staticMap.style.display = enabled ? "none" : "block";
    commonElements.interactiveMap.style.display = enabled ? "block" : "none";
  }

  function cardSide(cardSideName) {
    return commonConfig.cardSide === cardSideName;
  }

  /**
   * Throw an error if region code specified in the card field is absent in the map object to indicate
   * the reason of static map display and to automatically undo enabled interactive map mode
   */
  function failInvalidRegionCode() {
    let usedMapObj = window[commonConfig.mapSvgId];
    if (!usedMapObj.paths[commonConfig.regionCode])
      throw Error(`Region code "${commonConfig.regionCode || "empty"}" does not exist in the map`);
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
        selected: {fill: commonColors.selectedRegion}
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
    return commonConfig.regionCode === sessionStorage.getItem(commonConfig.selectedRegionSessionKey)
      ? commonColors.correctRegionHighlight
      : commonColors.incorrectRegionHighlight;
  }
}())
