# Configuration Files Reference

## Table of Contents
- [VARCONFIG.xml](#varconfigxml)
- [HICPCONFIG.xml](#hicpconfigxml)
- [EXCHANGERATESCONFIG.xml](#exchangeratesconfigxml)
- [SWITCHABLEPOLICYCONFIG.xml](#switchablepolicyconfigxml)
- [DataConfig Files](#dataconfig-files)

## VARCONFIG.xml

Variable acronym dictionary (~20 MB). Maps hierarchical acronym prefixes to meanings.

**Structure:**
```xml
<VarConfig xmlns="http://euromod.com/VarConfig.xsd">
  <AcronymType>
    <ShortName><![CDATA[d]]></ShortName>
    <LongName><![CDATA[demographic]]></LongName>
    <AcronymLevel>
      <Name><![CDATA[main]]></Name>
      <Acronym>
        <Name><![CDATA[ag]]></Name>
        <Description><![CDATA[age]]></Description>
      </Acronym>
    </AcronymLevel>
  </AcronymType>
</VarConfig>
```

Too large to load entirely. Search with:
```bash
grep -A2 'CDATA\[{acronym}\]' VARCONFIG.xml
```

## HICPCONFIG.xml

Harmonized Index of Consumer Prices by country and year (base 2015 = 100).

```xml
<HICPConfig xmlns="http://euromod.com/HICPConfig.xsd">
  <HICP>
    <Country>ro</Country>
    <Year>2007</Year>
    <Value>72.58</Value>
    <Comment>EUROSTAT - AMECO 2025 spring forecasts</Comment>
  </HICP>
</HICPConfig>
```

Used for price-level adjustments and understanding uprating factors.

## EXCHANGERATESCONFIG.xml

Exchange rates for non-Euro countries (BG, CZ, DK, HU, PL, RO, SE):

```xml
<ExchangeRatesConfig xmlns="http://euromod.com/ExchangeRatesConfig.xsd">
  <ExchangeRate>
    <Country>bg</Country>
    <June30>1.9558</June30>
    <YearAverage>1.9558</YearAverage>
    <Default>June30</Default>
    <ValidFor>bg_2022,bg_2023,bg_2024,bg_2025</ValidFor>
  </ExchangeRate>
</ExchangeRatesConfig>
```

## SWITCHABLEPOLICYCONFIG.xml

Toggleable policy extensions countries can implement:

| Code | Name | Purpose |
|------|------|---------|
| BTA | Benefit Take-up Adjustments | Model non-take-up of benefits |
| TCA | Tax Compliance Adjustments | Model tax evasion |
| FYA | Full Year Adjustments | Partial-year effects |
| UAA | Uprating by Average Adjustment | Alternative uprating |
| MWA | Minimum Wage Adjustments | Minimum wage simulations |
| EPS | Extended Policy Simulation | Extended scenarios |
| PBE | Parental leave benefits | Parental leave modeling |
| BCA | Benefit Calibration Adjustments | Calibrate to external data |
| CIA | Consumption Inflation Adjustment | Consumption tax inflation |

## DataConfig Files

Located at `XMLParam/Countries/{CC}/{CC}_DataConfig.xml`. Link datasets to systems:

```xml
<DataConfig xmlns="http://euromod.com/DataConfig.xsd">
  <DataBase>
    <Name>SL_training_data</Name>
    <YearCollection>1996</YearCollection>
    <YearInc>1996</YearInc>
    <Currency>euro</Currency>
    <DBSystemConfig>
      <SystemName>SL_1996</SystemName>
      <BestMatch>yes</BestMatch>
      <!-- Extension switch values for this dataset×system combination -->
      <PolicySwitch>
        <SwitchablePolicyID>9376be16-...</SwitchablePolicyID>
        <Value><![CDATA[off]]></Value>   <!-- on / off / n/a -->
      </PolicySwitch>
    </DBSystemConfig>
  </DataBase>
</DataConfig>
```

- `BestMatch=yes` → recommended system-dataset combination
- `YearInc` → income reference year of the data
- `UseCommonDefault=yes` → missing variables default to zero
- `PolicySwitch` elements are **inside `DBSystemConfig`** (not at `DataBase` level). They record the on/off/n/a switch value for each extension for that specific dataset × system combination.

### Reading extension switches for a best-match dataset (Python)

Namespace differs from CC.xml — use `DC_NS`:

```python
DC_NS = "{http://euromod.com/DataConfig.xsd}"

def load_ext_switches(cc, sys_name, base_path):
    """Return {ext_id_lower: switch_value} for the best-match dataset of sys_name."""
    import xml.etree.ElementTree as ET, os
    dc_path = os.path.join(base_path, cc, f"{cc}_DataConfig.xml")
    if not os.path.isfile(dc_path):
        return {}
    root = ET.parse(dc_path).getroot()
    for db in root.findall(f"{DC_NS}DataBase"):
        for dsc in db.findall(f"{DC_NS}DBSystemConfig"):
            sn = (dsc.findtext(f"{DC_NS}SystemName") or "").strip()
            bm = (dsc.findtext(f"{DC_NS}BestMatch") or "").strip()
            if sn != sys_name or bm != "yes":
                continue
            switches = {}
            for psw in dsc.findall(f"{DC_NS}PolicySwitch"):
                eid = (psw.findtext(f"{DC_NS}SwitchablePolicyID") or "").strip().lower()
                val = (psw.findtext(f"{DC_NS}Value") or "n/a").strip()
                if eid:
                    switches[eid] = val
            return switches
    return {}
```

### Reading Extension_Parameter index from CC.xml (Python)

```python
def build_ext_param_index(root, ns):
    """Returns {param_id: [(ext_id_lower, base_off_str)]}."""
    index = {}
    for ep in root.findall(f"{ns}Extension_Parameter"):
        pid  = (ep.findtext(f"{ns}ParameterID") or "").strip()
        eid  = (ep.findtext(f"{ns}ExtensionID")  or "").strip().lower()
        boff = (ep.findtext(f"{ns}BaseOff")      or "").strip()
        if pid and eid:
            index.setdefault(pid, []).append((eid, boff))
    return index

def is_item_baseline_active(item_id, ext_index, ext_switches):
    """False if any Extension_* entry has BaseOff=false and the switch is off."""
    for eid, base_off in ext_index.get(item_id, []):
        if base_off == "false" and ext_switches.get(eid, "n/a") == "off":
            return False
    return True
```

### Add-Ons

Add-ons use the same XML schema with placeholders: `=cc=` (country code), `=sys=` (system name), replaced at runtime to work across all countries.
