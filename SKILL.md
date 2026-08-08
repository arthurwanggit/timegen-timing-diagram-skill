---
name: timegen-timing-diagram
description: Use when generating or validating minimal TimeGen 3.2 XML timing diagrams from RTL, interface specifications, protocols, state machines, or textual timing requirements. Do not use for non-TimeGen diagrams.
compatibility: Windows, TimeGen 3.2, Python 3
---

# TimeGen Timing Diagram

Generate the smallest verified TimeGen 3.2 XML for the user's actual design.

## Verified Resources

- Read `references/timegen-xml-format.md` before generating XML.
- Start from `templates/minimal.xml`.
- Use `examples/example.xml` only to confirm structure and rendering codes.
- Validate every output with `scripts/validate_timegen_xml.py`.

All paths are relative to this Skill directory.

## Required Workflow

1. Inspect the RTL or specification and identify the signals and transitions that must be shown.
2. Build a simple ordered waveform plan for those signals.
3. Generate only `<waveform>`, `<signal name="...">`, `<data value="...">`, and `<text cycle="..." value="...">`.
4. Use only `0` and `1` for single-bit signals and clocks.
5. Use only `3` and `4` for buses. Alternate between `3` and `4` when a visible bus transition is required.
6. Use `01` repeated for a continuously toggling clock.
7. Align data transitions to the clock rising edge: in `01` encoding, `1` is the rising half. Non-clock signals should change at odd data character indices.
8. Give every signal exactly 600 data characters.
9. Place `<text>` after `<data>` inside a `<signal>`. The `cycle` attribute is a 0-based data character index, not a full clock cycle. With `01` clock encoding, full clock cycle C starts at data character `C*2`.
10. Use `<text>` for bus values, phase labels, and protocol annotations. Keep text concise.
11. Run the validator and fix every error.
12. Open the XML in TimeGen for the final rendering check when TimeGen is available.

## Strict Limits

- Do not emit data characters other than `0`, `1`, `3`, and `4`.
- Do not emit `<flood>` or `<timebreak>` unless explicitly requested and verified in TimeGen.
- Do not emit any child element other than `<data>` and `<text>`.
- Do not generate `.tim` files.
- Do not claim semantic meanings for `3` and `4`; they are only the two verified bus rendering codes.
- Do not encode bus values as additional data characters. Use `<text>` for semantic bus labels.
- Do not add colors, arrows, setup/hold labels, fonts, or GUI object properties to XML.
- Do not use a data length other than 600.
- Do not use full-cycle numbers as `cycle` values; always use data character indices.

## Validation

```powershell
python "<skill-directory>\scripts\validate_timegen_xml.py" "<generated-file.xml>"
```

Structural validation does not prove visual correctness. Compare the first active portion with the design plan and perform a TimeGen import check when possible.

## Completion Report

Report the output path, included signals, modeled scenario, validator result, and whether TimeGen rendering was checked.
