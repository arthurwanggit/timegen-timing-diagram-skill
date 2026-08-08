# Minimal Verified TimeGen 3.2 XML

This reference intentionally documents only the smallest format confirmed by the simplified TimeGen example.

## Exact Structure

```xml
<waveform>
    <signal name="Clock">
        <data value="0101..."></data>
    </signal>
    <signal name="Signal">
        <data value="0011..."></data>
    </signal>
</waveform>
```

Only these elements are allowed:

- one root `<waveform>`;
- one or more `<signal>` children;
- one `name` attribute on each `<signal>`;
- exactly one `<data>` child in each `<signal>`;
- one `value` attribute on each `<data>`;
- zero or more `<text>` children, placed after `<data>`.

Do not add `<flood>`, `<timebreak>`, or other untested elements.

## Verified Data Characters

Use only:

| Character | Verified use |
|-----------|--------------|
| `0` | Single-bit low portion or clock portion |
| `1` | Single-bit high portion or clock portion |
| `3` | One bus rendering state |
| `4` | The other bus rendering state |

No other digit is considered valid by this Skill.

For a continuously toggling clock, repeat `01`:

```text
010101010101...
```

Align data transitions to the PCLK rising edge. In `01` encoding, `0` is the low half and `1` is the rising half. Non-clock signals should transition at an **odd** data character index (where PCLK = `1`):

```text
char:     0 1 2 3 4 5 6 7
PCLK:     0 1 0 1 0 1 0 1
PSEL:     0 0 0 0 0 1 1 1
              ^       ↑
            d.c.5    d.c.5
           rising   rising
```

For a single-bit signal, create the required low and high intervals using only `0` and `1`.

For a bus, use only `3` and `4`. Switch between them at a required visible bus boundary:

```text
3333444433334444...
```

The Skill does not assign numeric or semantic bus values to `3` or `4`. Use `<text>` to label bus values.

## Text

```xml
<text cycle="4" value="Write Setup"></text>
```

- `cycle` is a 0-based **data character index**, not a full clock cycle. With `01` clock encoding, full clock cycle C starts at data character `C * 2`.
- `value` is the displayed annotation text.
- `<text>` must appear inside a `<signal>`, after `<data>`.
- Multiple `<text>` elements may belong to the same signal.
- Text is attached to the signal/cycle position but may not be independently movable or editable in the TimeGen GUI.

Example for a Write Setup at full clock cycle 2 (data chars 4-5):

```xml
<signal name="PSEL">
    <data value="0000111100001111..."></data>
    <text cycle="4" value="Write Setup"></text>
</signal>
```

## Length

- Every `<data value>` must contain exactly 600 characters.
- Every signal therefore has the same length.
- Do not infer clock-cycle mapping from string length alone.

## Encoding

- Save as UTF-8 XML.
- Keep data on one attribute value without spaces or line breaks.
- Prefer ASCII signal names for compatibility.
- Use an XML library when generating names from external input.

## Not Represented

The XML does not preserve:

- movable/editable independent TextBox objects (XML `<text>` is attached to a signal/cycle);
- arrows or setup/hold labels;
- colors, fonts, and coordinates;
- native TIM project objects.

Add presentation objects manually in TimeGen after importing the XML.

## Checklist

- Root is exactly `<waveform>`.
- Root contains only `<signal>` elements.
- Signal names are present and unique.
- Every signal contains exactly one `<data>`, optionally followed by `<text>` nodes.
- Every data value is exactly 600 characters.
- Every data character is one of `0`, `1`, `3`, or `4`.
- Every `<text cycle>` is a valid data character index within the waveform.
- The validator passes.
- TimeGen successfully renders the intended waveform.
