import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


EXPECTED_LENGTH = 600
ALLOWED_DATA_CHARACTERS = frozenset("0134")
ALLOWED_CHILDREN = {"data", "text"}


def validate(path: Path) -> list[str]:
    errors = []

    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        return [f"cannot parse XML: {exc}"]

    if root.tag != "waveform":
        errors.append(f"root must be <waveform>, found <{root.tag}>")
    if root.attrib:
        errors.append("<waveform> must not have attributes")

    signals = list(root)
    if not signals:
        errors.append("<waveform> must contain at least one <signal>")

    names = set()
    lengths = set()
    for index, signal in enumerate(signals):
        if signal.tag != "signal":
            errors.append(f"unexpected element under <waveform>: <{signal.tag}>")
            continue

        name = signal.get("name")
        label = name or f"signal[{index}]"
        if set(signal.attrib) != {"name"} or not name:
            errors.append(f"signal[{index}] must have exactly one nonempty name attribute")
        elif name in names:
            errors.append(f"duplicate signal name: {name}")
        else:
            names.add(name)

        children = list(signal)
        data_children = [c for c in children if c.tag == "data"]
        text_children = [c for c in children if c.tag == "text"]
        unexpected = [c.tag for c in children if c.tag not in ALLOWED_CHILDREN]

        if len(data_children) != 1:
            errors.append(f"{label}: must contain exactly one <data>, found {len(data_children)}")
            continue

        if unexpected:
            errors.append(f"{label}: unexpected child elements: {unexpected}")
            continue

        data = data_children[0]
        if set(data.attrib) != {"value"}:
            errors.append(f"{label}: <data> must have exactly one value attribute")

        value = data.get("value")
        if value is None:
            continue

        if not value:
            errors.append(f"{label}: data value must be nonempty")

        lengths.add(len(value))
        if len(value) != EXPECTED_LENGTH:
            errors.append(
                f"{label}: data length must be {EXPECTED_LENGTH}, found {len(value)}"
            )

        invalid = sorted(set(value) - ALLOWED_DATA_CHARACTERS)
        if invalid:
            errors.append(f"{label}: invalid data characters: {invalid}")

        for text in text_children:
            if set(text.attrib) != {"cycle", "value"}:
                errors.append(f"{label}: <text> must have exactly cycle and value attributes")
                continue

            cycle_value = text.get("cycle")
            try:
                cycle = int(cycle_value)
            except (ValueError, TypeError):
                errors.append(f"{label}: <text> cycle must be a nonnegative integer, got {cycle_value!r}")
                continue

            if cycle < 0:
                errors.append(f"{label}: <text> cycle must be nonnegative, got {cycle}")
            elif cycle >= len(value):
                errors.append(
                    f"{label}: <text> cycle {cycle} exceeds data length {len(value)}"
                )

            text_value = text.get("value")
            if not text_value:
                errors.append(f"{label}: <text> value must be nonempty")

    if len(lengths) > 1:
        errors.append(f"inconsistent data lengths: {sorted(lengths)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate minimal TimeGen 3.2 XML"
    )
    parser.add_argument("xml_file", type=Path)
    args = parser.parse_args()

    errors = validate(args.xml_file)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        print(f"FAILED: {len(errors)} error(s)", file=sys.stderr)
        return 1

    root = ET.parse(args.xml_file).getroot()
    text_count = sum(len(signal.findall("text")) for signal in root)
    print(f"OK: {len(root)} signal(s), {EXPECTED_LENGTH} data characters, {text_count} text(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
