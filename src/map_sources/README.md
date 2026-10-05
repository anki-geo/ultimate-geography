# Polynesian locator maps

These eight editable SVGs are the sources for the corresponding PNGs in
`src/media/maps`: Samoa, American Samoa, Tonga, Niue, Cook Islands, Tuvalu,
French Polynesia, and Wallis and Futuna.

The basemaps are by [TUBS on Wikimedia Commons](https://commons.wikimedia.org/wiki/User:TUBS)
and are licensed under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).
Each SVG's description links to its original file; the PNG source records and
modifications are also recorded in [`sources.csv`](../../sources.csv).
The original framing, land geometry, colours, locator inset, and red highlights
are retained. Unused off-canvas geometry and embedded Illustrator data have been
removed to reduce the source files' size.

The dashed grey lines are schematic separators between island groups, from
[Natural Earth's 1:50m Pacific Groupings, version 5.0.0](https://www.naturalearthdata.com/downloads/50m-cultural-vectors/50m-admin-0-boundary-lines-2/).
Natural Earth data is [public domain](https://www.naturalearthdata.com/about/terms-of-use/).
The exact input is available as
[GeoJSON at revision `ace5fed0`](https://github.com/nvkelso/natural-earth-vector/blob/ace5fed0eaf3c6c03c951e75b439ba8fffbc218e/geojson/ne_50m_admin_0_pacific_groupings.geojson).

Each SVG has a `Pacific_Groupings` layer containing separate polylines named for
the Natural Earth feature IDs. The lines use the basemap's Winkel Tripel
projection: central meridian 150° east and standard parallel 50°28′. Longitude
coordinates crossing the date line were unwrapped before projection. The SVG
description records the projection-to-SVG scale and offsets, calibrated against
the original hidden graticule. This keeps the lines aligned with the existing
map geometry.

At the PNG export size, the borders have a 0.7 px stroke, colour `#666868`, opacity
0.7, and a 4 px / 3 px dash pattern. The layer sits below the land and markers so
the existing coastlines and red highlights remain clear.

## Export the PNGs

With [librsvg](https://gitlab.gnome.org/GNOME/librsvg) (`rsvg-convert`) and
[ImageMagick](https://imagemagick.org/) (`magick`) available, run from the
repository root:

```sh
for map_source in src/map_sources/ug-map-*.svg; do
  map_name="${map_source##*/}"
  rsvg-convert --width 500 --height 281 "$map_source" |
    magick - -alpha off -strip -define png:color-type=2 \
      -define png:compression-level=9 "src/media/maps/${map_name%.svg}.png"
done
```

This produces 500 × 281 RGB PNGs with lossless compression. The deck continues to
reference the existing PNG filenames.
