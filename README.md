# AI Mouse

> Point / Speak / Do — 零说明书，最多三功能。Do 只出草稿、出图、写本地记录，**绝不自动发送邮件**。

## 一键演示（给内审 / 投资人）

无需 API key。复制粘贴即可：

```bash
cd /workspace/simtech-ai-mouse-agent && ./demo.sh
```

跑完会看到三件产物：
1. `out/drafts/reply_*.md` — 回复草稿（不发送）
2. `out/charts/chart_*.png` — 表格图表
3. `out/expenses.json` — 报销本地记录

Mac 上邮件进阶（可选）：生成 AppleScript 后手动 `osascript out/drafts/open_mail_reply.applescript` 打开回复窗，**仍需人手点发送**。

---
## 硬约束 (Hard constraints)
1. **Do 默认只出草稿 / 出图 / 写本地记录，绝不自动发送邮件或对外提交。** (`proposed_action.auto_send` 在 schema 中固定为 `false`，代码强制执行。)
2. **UI 固定三按钮：Point / Speak / Do，不加第四功能。**
3. **链路：选区截图 → 意图 JSON → Do（草稿/出图/本地记录）；绝不 auto_send。**
4. **代码根目录固定：`/workspace/simtech-ai-mouse-agent`**

## 今日链路：如何跑通
```bash
cd /workspace/simtech-ai-mouse-agent
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
# 非 Mac：传入已有截图
python -m src.pipeline.run --image tests/sample.png --transcript "帮我总结这段内容"
# Mac：不传 --image 即调用 `screencapture -i` 交互选区
python -m src.pipeline.run --transcript "解释一下"
```
- 无 key：输出 `source: "mock"`（关键词路由三任务），内容带 `[MOCK]` 标注。
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
Speak 对产品很重要；软件侧使用电脑麦克风即可，不阻塞演示。硬件板载麦为可选。

## Do (no API key)
无需任何 API key，mock 路由即可产出真实产物到 `out/`：
```bash
python -m src.pipeline.run --image tests/sample.png --transcript "帮我回复并接受" --mode do --do   # out/drafts/reply_*.md (+ Mac: open_mail_reply.applescript)
python -m src.pipeline.run --image tests/sample.png --transcript "做成图表" --mode do --do          # out/charts/chart_*.png (tests/sample_table.csv)
python -m src.pipeline.run --image tests/sample.png --transcript "这张收据报销" --mode do --do      # 追加到 out/expenses.json
```
- `auto_send` 不为 `false` 或未知 task_type 时 Do 直接拒绝（退出码 2）。
- Mac 上邮件：手动运行 `osascript out/drafts/open_mail_reply.applescript` 打开 Mail 回复窗口并填入正文，**需你自己点发送**，脚本绝不发送。
- Speak 使用电脑麦克风即可。

## Ask 旁路（非第四卖点）
对外仍只打 Point / Speak / Do。Ask 键：hold-to-talk + 可选区域截图（`capture_region`），给复杂题用；与 point 进入同一 Do。

```bash
# mock：框选/区域截图入口 → 同一 Do
python -m src.pipeline.run --image tests/sample.png --entry capture_region --transcript "做成图表" --mode do --do
```
