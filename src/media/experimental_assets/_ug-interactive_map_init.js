/**
 * Interactive map initialization logic declaration.
 * Note that due to Anki Desktop web view being persistent
 * for card reviews IIFE is used to separate the namespaces
 */
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
   * Using configuration options to determine whether to display interactive map
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

  /**
   * Determine card side using predefined names from configuration.
   * Note that current card side is figured out via accessing the value of
   * data attribute of the &lt;script&gt; element invoking the program
   */
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
    sessionStorage.removeItem(commonConfig.selectedRegionSessionKey);
    sessionStorage.removeItem(commonConfig.viewStateSessionKey);

    const frontMap = new jsVectorMap({
      ...commonMap,
      regionsSelectable: true,
      regionsSelectableOne: true,

      regionStyle: {
        ...commonMap.regionStyle,
        selected: {fill: commonColors.selectedRegion}
      },

      onRegionSelected(code) {
        sessionStorage.setItem(commonConfig.viewStateSessionKey, JSON.stringify({
          scale: frontMap.scale,
          transX: frontMap.transX,
          transY: frontMap.transY
        }));
        swapToBackSide(code);
      },

      ...mobileSwipingHack(false)
    });

    attachSmoothZoom(frontMap);
  }

  /**
   * Initialization of the map displayed on the back side of the card
   */
  function initBackMap() {
    const backMap = new jsVectorMap({
      ...commonMap,
      selectedRegions: [commonConfig.regionCode],

      regionStyle: {
        ...commonMap.regionStyle,
        selected: {fill: getRegionColor()}
      },

      ...mobileSwipingHack(commonConfig.toolTipEnabled, (event, tooltip) => {
        tooltip._tooltip.style.backgroundColor = commonColors.tooltipBackground;
        tooltip._tooltip.style.color = commonColors.tooltipText;
      })
    });

    const saved = readSavedView();
    if (saved) {
      // Snap to the saved view by mutating public state directly — _setScale's
      // non-centered branch interprets its e/i args as off-center-zoom deltas
      // around the current transX/transY, not absolute translations.
      backMap.scale = saved.scale;
      backMap.transX = saved.transX;
      backMap.transY = saved.transY;
      backMap._applyTransform();
    }
    backMap.setFocus({region: commonConfig.regionCode, animate: true});

    attachSmoothZoom(backMap);

    sessionStorage.removeItem(commonConfig.viewStateSessionKey);
    sessionStorage.removeItem(commonConfig.selectedRegionSessionKey);
  }

  /**
   * Replacement wheel handler for jsVectorMap.
   *
   * The built-in handler bit-shifts deltaY by 10, defaulting to ±1, then applies
   * pow(1.003, ±112.5) ≈ 1.4x or 0.71x per event. Trackpads fire many events
   * per flick, so the multiplier explodes and clamps to zoomMin/zoomMax.
   *
   * Here we normalize across deltaMode (px/line/page) and apply a small per-pixel
   * scale so a smooth flick produces a smooth zoom.
   */
  function attachSmoothZoom(map) {
    const container = map.container;
    let pendingPixels = 0;
    let pendingX = 0;
    let pendingY = 0;
    let frame = null;

    container.addEventListener("wheel", (event) => {
      event.preventDefault();
      const rect = container.getBoundingClientRect();
      pendingX = event.pageX - rect.left - window.pageXOffset;
      pendingY = event.pageY - rect.top - window.pageYOffset;
      pendingPixels += event.deltaMode === 1 ? event.deltaY * 30
        : event.deltaMode === 2 ? event.deltaY * 300
        : event.deltaY;

      if (frame !== null) return;
      frame = requestAnimationFrame(() => {
        const factor = Math.pow(1.008, -pendingPixels);
        map._setScale(map.scale * factor, pendingX, pendingY, false, false);
        pendingPixels = 0;
        frame = null;
      });
    }, { passive: false });
  }

  /**
   * Read the front-side pan/zoom snapshot saved at click time.
   * Returns null if missing, malformed, or contains non-finite numbers.
   */
  function readSavedView() {
    const raw = sessionStorage.getItem(commonConfig.viewStateSessionKey);
    if (!raw) return null;
    try {
      const v = JSON.parse(raw);
      return v && Number.isFinite(v.scale) && Number.isFinite(v.transX) && Number.isFinite(v.transY)
        ? v
        : null;
    } catch {
      return null;
    }
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
   * Jsvectormap library bug - map swiping does not work on mobile with disabled tooltip.
   * Enable tooltip and hide it in case original tooltip is not displayable.
   * Current handling is temporary fix until library issue is resolved
   */
  function mobileSwipingHack(tooltipEnabled, tooltipShowHandler) {
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
      dispatchEnterEvent()
    }
  }

  /**
   * Trigger "Enter" key press event. Note that Anki < 24.06
   * uses `code` property and Anki >= 24.06 - `key` property
   * to query pressed key, so both properties must be present
   */
  function dispatchEnterEvent() {
    let artificialEvent = new KeyboardEvent("keypress", {code: "Enter", key: "Enter"});
    commonElements.hiddenTextarea.dispatchEvent(artificialEvent);
  }

  /**
   * Retrieve region highlighting color for answer card side
   * depending on the configuration and whether the selected
   * by the user on question side region is correct
   */
  function getRegionColor() {
    const expected = (commonConfig.regionCode || "").trim().toUpperCase();
    const actual = (sessionStorage.getItem(commonConfig.selectedRegionSessionKey) || "").trim().toUpperCase();
    return expected && expected === actual
      ? commonColors.correctRegionHighlight
      : commonColors.incorrectRegionHighlight;
  }
}())
