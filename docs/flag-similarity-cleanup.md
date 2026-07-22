# Flag-similarity cleanup audit

This reviewed source cleanup intentionally corrects legacy flag-similarity translation and punctuation anomalies while adopting the field-level list message pattern. The inventory below was produced by exporting all 74 main and 26 companion targets before and after the cleanup with Brain Brew `77b092ddb82fb0dfdaf64713ed081a4ac9f2eb97`, parsing every `deck.json`, and recursively comparing every supported JSON property.

- Compared targets: **100**
- Changed targets: **28**
- Changed note fields: **74** occurrences across target variants
- Unique `(GUID, field index, old value, new value)` tuples: **17**
- Non-field JSON differences: **0**
- Every changed field index is `6` (`Flag similarity`).

## Exact reviewed deltas

### 1. `B,]AC/PAz1` field `6`

- Targets (5): `nb-experimental`, `nb-extended`, `nb-hardcore-extended`, `nb-hardcore-standard`, `nb-standard`
- Before: `Jemen (blank midstripe), Egypt (emblem)`
- After: `Egypt (blank midstripe), Jemen (emblem)`

### 2. `EH/@$WQER7` field `6`

- Targets (3): `zh-tw-experimental`, `zh-tw-extended`, `zh-tw-standard`
- Before: `挪威(紅底、藍十字)`
- After: `挪威(紅底、藍十字)、法羅群島(白底、紅藍十字)`

### 3. `EW8MT$$Do=` field `6`

- Targets (5): `zh-experimental`, `zh-extended`, `zh-hardcore-extended`, `zh-hardcore-standard`, `zh-standard`
- Before: `印度尼西亚(更宽，红色更亮)，波兰(红色和白色翻转，更宽)`
- After: `印度尼西亚(更宽，红色更亮)、波兰(红色和白色翻转，更宽)`

### 4. `FTq&ip7kv.` field `6`

- Targets (5): `zh-experimental`, `zh-extended`, `zh-hardcore-extended`, `zh-hardcore-standard`, `zh-standard`
- Before: `摩纳哥(更窄，红色更深)，波兰(红白翻转，红色更深)`
- After: `摩纳哥(更窄，红色更深)、波兰(红白翻转，红色更深)`

### 5. `Gir-4TL#W$` field `6`

- Targets (5): `ru-experimental`, `ru-extended`, `ru-hardcore-extended`, `ru-hardcore-standard`, `ru-standard`
- Before: `Кот-д'Ивуар (зеленый и оранжевый перевернутый, более узкий)`
- After: `Кот-д’Ивуар (зеленый и оранжевый перевернутый, более узкий)`

### 6. `KOyffK#a5H` field `6`

- Targets (5): `pt-experimental`, `pt-extended`, `pt-hardcore-extended`, `pt-hardcore-standard`, `pt-standard`
- Before: ` Bolívia (brasão de armas em vez de estrela)`
- After: `Bolívia (brasão de armas em vez de estrela)`

### 7. `Lk811V}xOV` field `6`

- Targets (4): `zh-hardcore-companion-extended`, `zh-hardcore-companion-standard`, `zh-hardcore-extended`, `zh-hardcore-standard`
- Before: `Sierra Leone (slightly lighter blue)`
- After: `塞拉利昂(略浅蓝色)`

### 8. `N(,;S#&N9e` field `6`

- Targets (5): `nb-experimental`, `nb-extended`, `nb-hardcore-extended`, `nb-hardcore-standard`, `nb-standard`
- Before: `Jemen (blank midstripe), Irak (tekst)`
- After: `Irak (blank midstripe), Jemen (tekst)`

### 9. `h=:xts:/of` field `6`

- Targets (5): `zh-experimental`, `zh-extended`, `zh-hardcore-extended`, `zh-hardcore-standard`, `zh-standard`
- Before: `印度尼西亚(白色和红色翻转，红色更亮)，摩纳哥(白色和红色翻转，更窄)`
- After: `印度尼西亚(白色和红色翻转，红色更亮)、摩纳哥(白色和红色翻转，更窄)`

### 10. `jJMevp,*!q` field `6`

- Targets (5): `pt-experimental`, `pt-extended`, `pt-hardcore-extended`, `pt-hardcore-standard`, `pt-standard`
- Before: `Egito (com emblema), e Iraque (com texto)`
- After: `Egito (com emblema) e Iraque (com texto)`

### 11. `l.0D<A/ul3` field `6`

- Targets (5): `zh-experimental`, `zh-extended`, `zh-hardcore-extended`, `zh-hardcore-standard`, `zh-standard`
- Before: `冰岛(蓝底，红十字)，法罗群岛(白底，红蓝交叉)`
- After: `冰岛(蓝底，红十字)、法罗群岛(白底，红蓝交叉)`

### 12. `l7l~M4fz$?` field `6`

- Targets (3): `zh-tw-experimental`, `zh-tw-extended`, `zh-tw-standard`
- Before: `俄羅斯(沒徽章)、斯洛維尼亞(更寬、更小的徽章)`
- After: `俄羅斯(無徽章)、斯洛維尼亞(更寬、更小的徽章)`

### 13. `lO0wObq%O:` field `6`

- Targets (3): `da-experimental`, `da-extended`, `da-standard`
- Before: `Andora (smallere, våbenskjold med motto)`
- After: `Andorra (smallere, våbenskjold med motto)`

### 14. `mcx~q)C#fp` field `6`

- Targets (3): `zh-tw-experimental`, `zh-tw-extended`, `zh-tw-standard`
- Before: `圭亞那(綠紅對調、稍微深綠)`
- After: `幾內亞(綠紅對調、稍微深綠)`

### 15. `xy{u)[Y5T.` field `6`

- Targets (3): `zh-tw-experimental`, `zh-tw-extended`, `zh-tw-standard`
- Before: `波利維亞(徽章、非星星)`
- After: `玻利維亞(徽章、非星星)`

### 16. `y3XH$Vv!}O` field `6`

- Targets (5): `zh-experimental`, `zh-extended`, `zh-hardcore-extended`, `zh-hardcore-standard`, `zh-standard`
- Before: `库拉索岛(左上角的两颗星)`
- After: `库拉索(左上角的两颗星)`

### 17. `yOxL^*11zC` field `6`

- Targets (5): `zh-experimental`, `zh-extended`, `zh-hardcore-extended`, `zh-hardcore-standard`, `zh-standard`
- Before: `冰岛(蓝底，红白交叉)，挪威(红底，蓝白交叉)`
- After: `冰岛(蓝底，红白交叉)、挪威(红底，蓝白交叉)`

## Verification

- `python scripts/check-translation-profile.py` confirms the two profile copies are identical.
- Strict native verification passes all 74 main and 26 companion targets against real media hashes and configured goldens.
- `scripts/collect-pr736-equivalence-evidence.py` rebuilds immutable historical inputs and exact-allowlists only the six reviewed `zh-standard` historical tuples exercised by its representative matrix.
- The all-target comparison rejects any changed deck metadata, note identity, note model, tag, non-flag field, template, configuration, or other JSON property.
