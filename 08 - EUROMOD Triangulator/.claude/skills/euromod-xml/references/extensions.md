# EUROMOD Extensions

Extensions (switchable policies) come in two flavours:

| Type | Definition location | Name storage |
|---|---|---|
| **Global** | `XMLParam/Config/SWITCHABLEPOLICYCONFIG.xml` | `<NamePattern>` (CDATA) + `<LongName>` inside `<SwitchablePolicy>` |
| **Country-specific (local)** | `{CC}_DataConfig.xml` | `<Name>` + `<ShortName>` inside `<Extension>` |

### Global extension structure (SWITCHABLEPOLICYCONFIG.xml)

```xml
<SwitchablePolicy>
  <ID>8b258cd1-804e-4c9d-adc2-2d3e609c162a</ID>
  <NamePattern><![CDATA[BTA]]></NamePattern>
  <LongName>Benefit Take-up Adjustments</LongName>
</SwitchablePolicy>
```

### Local extension structure ({CC}_DataConfig.xml)

```xml
<!-- Definition block — gives the extension its name -->
<Extension>
  <ID>abfb2064-9189-43e7-9f61-f3886ae327b1</ID>
  <Name>SORESI web-based model</Name>
  <ShortName>SORESI</ShortName>
</Extension>

<!-- Usage block — links extension to a system×dataset combination -->
<PolicySwitch>
  <SwitchablePolicyID>abfb2064-9189-43e7-9f61-f3886ae327b1</SwitchablePolicyID>
  <SystemID>...</SystemID>
  <DataBaseID>...</DataBaseID>
  <Value><![CDATA[on]]></Value>   <!-- on / off / n/a -->
</PolicySwitch>
```

**Local extension names are NOT stored in `{CC}.xml`** — only in the DataConfig `<Extension>` blocks.

### Linking extensions to policies/functions ({CC}.xml)

`<Extension_Policy>` and `<Extension_Function>` are **flat root-level records** in `{CC}.xml` — they are NOT nested inside any `<System>`. They map an extension GUID to a policy or function GUID across all systems.

```xml
<!-- Most common: links extension to a policy -->
<Extension_Policy>
  <ExtensionID>abfb2064-...</ExtensionID>
  <PolicyID>some-policy-guid</PolicyID>
  <BaseOff>true</BaseOff>
</Extension_Policy>

<!-- Less common: links extension to a function directly -->
<Extension_Function>
  <ExtensionID>4e653e98-...</ExtensionID>
  <FunctionID>some-function-guid</FunctionID>
  <BaseOff>false</BaseOff>
</Extension_Function>

<!-- Rarest: links extension to an individual parameter row -->
<Extension_Parameter>
  <ExtensionID>9376be16-...</ExtensionID>
  <ParameterID>9d31235a-...</ParameterID>
  <BaseOff>false</BaseOff>
</Extension_Parameter>
```

**Cloning implication:** When cloning a system, new policy/function GUIDs are generated. The corresponding `Extension_Policy` / `Extension_Function` root-level records must be replicated with the new GUIDs — otherwise the EUROMOD UI shows plain on/off toggles instead of extension-controlled ones.

### BaseOff semantics (all three Extension_* types)

| `BaseOff` value | Meaning |
|---|---|
| `true` | This record is the *base* version — the item turns **off** when the extension is ON |
| `false` | This record is the *extension-ON* version — the item is **only active** when the extension is ON |

**Baseline exclusion rule:** An item (policy / function / parameter) should be excluded from baseline if ANY of its controlling Extension_* records has `BaseOff=false` AND the extension's switch in the best-match DataConfig dataset is `off`.

Example: `tlx` in Greece's `ils_taxin` has an `Extension_Parameter` entry with `BaseOff=false` for extension `9376be16`. The EL_2025 best-match dataset sets that extension to `off` → `tlx` is excluded from the baseline.

### Detecting whether a country implements an extension

A country *implements* an extension if it has at least one `<PolicySwitch>` block with a matching `<SwitchablePolicyID>` whose `<Value>` is not `n/a`.

```python
import re

def country_uses_extension(dc_content: str, guid: str) -> bool:
    for m in re.finditer(r'<PolicySwitch>.*?</PolicySwitch>', dc_content, re.DOTALL):
        id_m  = re.search(r'<SwitchablePolicyID>([^<]+)</SwitchablePolicyID>', m.group())
        val_m = re.search(r'<Value><!\[CDATA\[([^\]]+)\]\]></Value>', m.group())
        if id_m and val_m and id_m.group(1).strip().lower() == guid.lower():
            if val_m.group(1).strip() != 'n/a':
                return True
    return False
```
