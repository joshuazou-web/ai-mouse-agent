# AI Mouse

> Point / Speak / Do — 零说明书，最多三功能。Do 只出草稿、出图、写本地记录，**绝不自动发送邮件**。

录屏分镜（≤3 分钟）：[docs/RECORDING_SCRIPT.md](docs/RECORDING_SCRIPT.md)  
操作说明与产物路径：[docs/DEMO_NOTES.md](docs/DEMO_NOTES.md)

## 一键演示

在仓库根目录（与 `demo.sh` 同级）执行，不需要 API key：

```bash
./demo.sh
```

当前没有 `OPENAI_API_KEY`、也没有 `ANTHROPIC_API_KEY` 时，理解层是关键词 mock，不是视觉模型：

- 意图 JSON 的 `source` 为 `"mock"`，`confidence` 为 `0.0`。`0.0` 表示没有调用模型，录屏里不要把它讲成准确率。
- 三步都传入 `tests/sample.png`（400×200 占位图，画面文字是 “Q3 revenue up 12%”）。邮件、表格、收据的样例在 `tests/sample_email.txt`、`tests/sample_table.csv`、`tests/sample_receipt.txt`。
- Do 仍写出真实文件。图表数据来自 `tests/sample_table.csv` 的 `units` 列。报销行在 mock 下是占位：商家 `unknown`，金额 `0.0`。

跑完：

1. `out/drafts/reply_*.md` — 回复草稿（不发送）
2. `out/charts/chart_*.png` — 柱状图 PNG
3. `out/expenses.json` — 本地报销记录（JSON 数组，每次追加一条）

Mac 上可选：`osascript out/drafts/open_mail_reply.applescript` 打开回复窗并填入正文，**发送仍要人手点**。脚本里没有发送动作。Linux 只有 `--image` 这条路，没有交互选区。

真实视觉：在同一个 shell 的进程环境里设置 `OPENAI_API_KEY` 后再跑同一条命令。程序不读取 `.env`。不要把 key 写进仓库或录屏。可选变量名是 `OPENAI_BASE_URL`、`VISION_MODEL`。未设置 `OPENAI_API_KEY` 时才看 `ANTHROPIC_API_KEY`（可选 `ANTHROPIC_MODEL`）。接上之后 `source` 应为 `vision_llm`，`auto_send` 仍为 `false`。

---
## 硬约束 (Hard constraints)
1. **Do 默认只出草稿 / 出图 / 写本地记录，绝不自动发送邮件或对外提交。** (`proposed_action.auto_send` 在 schema 中固定为 `false`，代码强制执行。)
2. **UI 固定三按钮：Point / Speak / Do，不加第四功能。**
3. **链路：选区截图 → 意图 JSON → Do（草稿/出图/本地记录）；绝不 auto_send。**
4. **命令在仓库根目录执行**（含 `demo.sh` 的 `ai-mouse-agent` 目录）。

## 今日链路：如何跑通
```bash
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
# Linux / 非 Mac：必须传入已有截图
python -m src.pipeline.run --image tests/sample.png --transcript "帮我总结这段内容"
# Mac：不传 --image 即调用 `screencapture -i` 交互选区。没有 vision key 时结果仍是 mock
python -m src.pipeline.run --transcript "解释一下"
```
- 无 key：输出 `source: "mock"`（关键词路由三任务），内容带 `[MOCK]` 标注，`confidence` 为 `0.0`。
- `OPENAI_API_KEY`（优先）：OpenAI 兼容 vision；可设 `OPENAI_BASE_URL`、`VISION_MODEL`。
- 否则 `ANTHROPIC_API_KEY`：Claude vision；可设 `ANTHROPIC_MODEL`（默认 `claude-sonnet-4-5`）。
- 输出均经 `jsonschema` 校验符合 `schema/intent_schema.json`；`auto_send` 恒为 `false`。

## 结构
- `src/pipeline/capture.py` — 截图（Mac screencapture -i / --image）
- `src/pipeline/understand.py` — 读图+transcript → INTENT JSON
- `src/pipeline/run.py` — CLI 入口
- `src/do/` — Do 层（草稿 / 出图 / 本地报销记录，绝不发送）；`python -m src.do.run --intent x.json`
- `schema/intent_schema.json`, `docs/ARCHITECTURE.md`


## Speak / 麦克风
Speak 的产品入口是电脑麦克风，硬件板载麦可选。当前仓库没有语音识别程序：能跑通的 Speak 是 `--transcript` 这句文本。录屏时嘴里说的和这个参数用同一句。

## Do (no API key)
无需任何 API key，mock 路由即可产出真实产物到 `out/`：
```bash
python -m src.pipeline.run --image tests/sample.png --transcript "回复并接受" --mode do --do   # out/drafts/reply_*.md (+ Mac: open_mail_reply.applescript)
python -m src.pipeline.run --image tests/sample.png --transcript "做成图表" --mode do --do     # out/charts/chart_*.png (tests/sample_table.csv 的 units 列)
python -m src.pipeline.run --image tests/sample.png --transcript "归档报销" --mode do --do     # 追加到 out/expenses.json（mock 行是占位金额）
```
- `auto_send` 不为 `false` 或未知 task_type 时 Do 直接拒绝（退出码 2）。
- Mac 上邮件：手动运行 `osascript out/drafts/open_mail_reply.applescript` 打开 Mail 回复窗口并填入正文，**需你自己点发送**，脚本绝不发送。
- 上面三句与 `./demo.sh` 相同。英文对照在 `docs/RECORDING_SCRIPT.md`。

## Ask 旁路（非第四卖点）
对外仍只打 Point / Speak / Do。Ask 键：hold-to-talk + 可选区域截图（`capture_region`），给复杂题用；与 point 进入同一 Do。录屏脚本不演示这条。

```bash
# mock：框选/区域截图入口 → 同一 Do
python -m src.pipeline.run --image tests/sample.png --entry capture_region --transcript "做成图表" --mode do --do
```
