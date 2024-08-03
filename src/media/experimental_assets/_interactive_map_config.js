/**
 * Customizable user properties
 */
function getUserConfig() {
  let configObj = {};
  configObj.commonFeatures = {
    interactiveEnabled: true,
    interactiveMobileEnabled: true,
    autoAnswerEnabled: true,
    greenRedEnabled: true,
    mapHighDetail: true,
    toolTipEnabled: false,
  };
  configObj.commonColors = {
    bodyOfWater: "#b3dff5",
    landMass: "#fdfbe5",
    selectedLandMass: "#e7f3ea",
    border: "#757674",
    highlightedRegion: "#c02637",
    highlightedCorrectRegion: "#329446",
    tooltipBackground: "#fdfbe5",
    tooltipText: "#000000"
  };
  return configObj;
}

/**
 * Overall configuration. Includes validated user properties
 * and core properties - program auxiliary data. Should not
 * be modified unless the author understands what they are doing
 */
function getMapConfig() {
  let userConfig = getUserConfig()
  let configObj = {};
  configObj.commonConfig = {
    interactiveEnabled: true,
    interactiveMobileEnabled: true,
    autoAnswerEnabled: true,
    greenRedEnabled: true,
    mapHighDetail: true,
    toolTipEnabled: false,
    ...filterObjValidBooleans(userConfig.commonFeatures),

    isMobile: document.documentElement.classList.contains("mobile"),
    regionCode: document.currentScript.dataset.regionCode,
    cardSide: document.currentScript.dataset.cardSide,
    questionCardSideName: "question",
    answerCardSideName: "answer",
    selectedRegionSessionKey: "selectedRegion",
    get mapSvgId() {
      return this.mapHighDetail ? "world_high_detail" : "world_low_detail"
    }
  }
  configObj.commonColors = {
    bodyOfWater: "#b3dff5",
    landMass: "#fdfbe5",
    selectedLandMass: "#e7f3ea",
    border: "#757674",
    highlightedRegion: "#c02637",
    highlightedCorrectRegion: "#329446",
    tooltipBackground: "#fdfbe5",
    tooltipText: "#000000",
    ...filterObjValidColors(userConfig.commonColors)
  };
  configObj.commonElements = {
    interactiveMap: document.querySelector(".value--map"),
    staticMap: document.querySelector(".value--image"),
    mapTooltips: document.querySelectorAll("body > div.jvm-tooltip"),
    hiddenTextarea: document.querySelector("textarea#typeans")
  };
  configObj.commonMap = {
    selector: configObj.commonElements.interactiveMap,
    map: configObj.commonConfig.mapSvgId,
    zoomButtons: false,
    zoomMax: 1000,
    backgroundColor: configObj.commonColors.bodyOfWater,
    regionStyle: {
      initial: {
        fill: configObj.commonColors.landMass,
        stroke: configObj.commonColors.border,
        strokeWidth: configObj.commonConfig.mapHighDetail ? 0.2 : 1
      }
    }
  };
  return configObj;
}

/**
 * Assemble the object from properties of original object
 * values of which match the predicate
 */
function filterObj(obj, predicate) {
  let filtered = {};
  for (let [key, value] of Object.entries(obj))
    if (predicate(value))
      filtered[key] = value;
  return filtered;
}

/**
 * Assemble the object with valid boolean property values
 * ignoring invalid and non-boolean properties
 */
function filterObjValidBooleans(obj) {
  return filterObj(obj, v => typeof v === "boolean");
}

/**
 * Assemble the object with valid HEX string property values
 * ignoring invalid and non-HEX properties
 */
function filterObjValidColors(obj) {
  return filterObj(obj, v => v.toString().match(/^#(?:[0-9a-fA-F]{3}){1,2}$/g));
}
