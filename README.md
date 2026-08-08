# TimeGen Timing Diagram Skill

[中文](#中文) | [English](#english)

## 中文

这是一个用于生成和校验 TimeGen 3.2 XML 时序图的 OpenCode Skill。

本项目刻意只支持已经由精简 TimeGen 示例证明可渲染的最小格式：

- XML 只有 `<waveform>`、`<signal>` 和 `<data>`。
- 每条波形固定为 600 个字符。
- 单比特信号只使用 `0` 和 `1`。
- 总线只使用 `3` 和 `4`，在需要显示边界时二者切换。
- `<text>` 用于波形标注，`cycle` 是数据字符索引（不是完整时钟周期）。
- 不生成 `<flood>`、`<timebreak>` 或其他未验证元素。

Skill 会从目标 RTL 或规范推导信号变化，不套用固定协议示例。

### 目录

```text
timegen-timing-diagram-skill/
├── .github/workflows/validate.yml
├── examples/example.xml
├── references/timegen-xml-format.md
├── scripts/validate_timegen_xml.py
├── templates/minimal.xml
├── tests/test_validator.py
├── LICENSE
├── README.md
└── SKILL.md
```

### 安装

全局安装：

```powershell
git clone <repository-url> "$HOME\.config\opencode\skills\timegen-timing-diagram"
```

项目级安装：

```powershell
git clone <repository-url> ".opencode\skills\timegen-timing-diagram"
```

安装或更新后重启 OpenCode。

### 校验

```powershell
python scripts\validate_timegen_xml.py path\to\waveform.xml
python -m unittest discover -s tests -v
```

通过结构校验后，仍应在 TimeGen 中打开 XML，确认实际渲染结果。

### 限制

极简格式不表达总线文字、TextBox、Arrow、Setup/Hold Label、颜色、字体或 TIM 工程对象。需要这些内容时，在 TimeGen 导入 XML 后手工添加。

### 声明

本项目是非官方社区工具，与 TimeGen 软件的作者、所有者或发行方没有隶属或背书关系。仓库不包含 TimeGen 可执行文件、专有二进制文件或 TIM 研究资料。

## English

This OpenCode Skill generates and validates minimal TimeGen 3.2 XML timing diagrams.

It intentionally supports only the smallest format confirmed by the simplified TimeGen example:

- XML contains only `<waveform>`, `<signal>`, and `<data>`.
- Every waveform contains exactly 600 characters.
- Single-bit signals use only `0` and `1`.
- Buses use only `3` and `4`, switching between them where a visible boundary is required.
- `<text>` provides waveform annotations; `cycle` is a data character index (not a full clock cycle).
- No `<flood>`, `<timebreak>`, or other unverified elements are generated.

The Skill derives transitions from the target RTL or specification instead of applying a fixed protocol example.

### Installation

Global:

```powershell
git clone <repository-url> "$HOME\.config\opencode\skills\timegen-timing-diagram"
```

Project-local:

```powershell
git clone <repository-url> ".opencode\skills\timegen-timing-diagram"
```

Restart OpenCode after installation or update.

### Validation

```powershell
python scripts\validate_timegen_xml.py path\to\waveform.xml
python -m unittest discover -s tests -v
```

After structural validation, open the XML in TimeGen to confirm the actual rendering.

### Limits

The minimal format does not represent bus text, TextBox, Arrow, Setup/Hold Label, color, font, or native TIM project objects. Add presentation objects manually after importing XML into TimeGen.

### Disclaimer

This is an unofficial community project. It is not affiliated with or endorsed by the authors, owners, or distributors of TimeGen. It does not distribute TimeGen executables, proprietary binaries, or TIM research materials.

## License

[MIT](LICENSE)
