# AI Mouse — 录屏分镜（总长 ≤ 3:00）

产品名只说 **AI Mouse**。画面上的功能只有 **Point / Speak / Do**。Do 的成功画面是草稿、PNG、本地 JSON。发送权留在人手（`auto_send=false`）。

两条成片，不要混在一条里假装：

| 成片 | 何时拍 | 时长 | 观众会以为模型做了什么 |
|------|--------|------|------------------------|
| **Pass M** | 今天就能拍。没有 vision key | 1:50 | 关键词路由 + 本地产物。没有读屏 |
| **Pass V** | `OPENAI_API_KEY` 已进当前 shell 之后 | 2:40 | 选区里的邮件 / 表格 / 收据被读懂 |

操作备注用中文。对镜头口播给了英文和中文两套，**一套拍到底**。口播和 `--transcript` 用同一句，这样意图 JSON 里的 `intent` 跟嘴里说的一致。

仓库里没有语音识别。Speak 在这条 CLI 里就是 `--transcript`。镜头里先说完这句，再让命令里出现同一句。不要做假的麦克风波形 UI。

---

## 开拍前（不入画）

```bash
# 仓库根目录，和 demo.sh 同级
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python -c 'import os; print("OPENAI_API_KEY", "set" if os.getenv("OPENAI_API_KEY") else "unset"); print("ANTHROPIC_API_KEY", "set" if os.getenv("ANTHROPIC_API_KEY") else "unset")'
```

- Pass M：两行都要是 `unset`。若是 `set`，在这个 shell 里 `unset OPENAI_API_KEY ANTHROPIC_API_KEY`。不要把值打出来。
- Pass V：`OPENAI_API_KEY` 为 `set`。设置方式只在 [DEMO_NOTES.md](DEMO_NOTES.md)。录屏里不要出现赋值过程。
- 先在镜头外跑通一次 `./demo.sh`，确认 `.venv` 已装好。再 `rm -rf out`，正式那条才是干净的三个新文件。
- 终端：大字号、`clear` 过、当前目录是仓库根。提示符里不要带密钥。
- 三个 Point 目标事先打开，字号放大到录屏能读：
  - 邮件 `tests/sample_email.txt`
  - 表格 `tests/sample_table.csv`
  - 收据 `tests/sample_receipt.txt`
- Linux / 非 Mac 只有 `--image`。下面每条命令都带了 `--image`，本机可以直接拍。Mac 在 Pass V 里可以去掉 `--image`，改用 `screencapture -i` 真框选；没有 key 时框选仍是 mock。

`tests/sample.png` 是 400×200 占位图，画面只有 “Q3 revenue up 12%”。Pass M 的命令用它，因为 mock 不看像素。不要把它讲成邮件、表格或收据。

---

## 不要入画

- `OPENAI_API_KEY`、`ANTHROPIC_API_KEY` 的值，`.env`，`export`，`env`，shell history。不要打假 key 充数。
- mock 的 `"confidence": 0.0` 不要讲成准确率、置信度或“模型很有把握 / 没把握”。这是“没有调用模型”的哨兵。JSON 若必须扫过，口播只说 “source 是 mock”。
- 不要把 Pass M 的选区讲成“它看见了这封邮件 / 这张表 / 这张收据”。
- 不要点发送，不要出现“已发送”，不要把报销提交到任何网站。Mail 窗口的发送按钮不进这条成片。
- 不要介绍 Ask，不要跑 `--entry capture_region`。那是内部旁路，不是第四个功能。
- 不要拍 `pip` 滚动、报错、`.venv`。

---

## 口播句（整段只用一套）

| 镜头 | English（产品） | 中文 |
|------|-----------------|------|
| 开场 | AI Mouse. Point, Speak, Do. | AI Mouse。指哪，说哪，做哪。 |
| 邮件 | `Reply and accept.` | `回复并接受` |
| 图表 | `Chart the units column.` | `把 units 做成图表` |
| 收据 | `Archive this expense.` | `归档报销` |
| 收尾 | Draft, chart, local record. You send. | 草稿，图表，本地记录。发送留给人。 |

`./demo.sh` 内写死的是中文三句。英文成片不要直接录 `./demo.sh` 的滚屏，改用下面 Pass 里的英文命令。中文成片可以录 `./demo.sh`。

路由就认这些词（大小写不敏感）：邮件 `回复|接受|reply|accept`；图表 `图表|做成图|chart|graph`；报销 `报销|归档|收据|账单|expense|receipt`。图表这句写成 `Chart the units column.` / `把 units 做成图表`，是为了点名 `units` 列，同时仍含 `chart` / `图表`，mock 会进 `make_chart`。换句式之前先在镜头外跑一遍，确认 `task_type` 分别是 `draft_email`、`make_chart`、`log_record`。

---

## Pass M — 今天（mock）1:50

画面是终端 + 三个产物文件。三个任务都用 `--image tests/sample.png`。口播把 Speak 那句说出来，同时命令里有同一句。

成功标准：草稿文件头有 `auto_send=false, NOT sent`；出现一张柱状 PNG；`out/expenses.json` 多一条，且商家是 `unknown`、金额是 `0.0`。把这条讲成占位记录。

### M0 开场 — 0:00–0:08（8s）可今天拍

- 画面：终端标题或第一行注释可见 `AI Mouse`，以及即将执行的 `./demo.sh`（中文）或三条 `python`（英文）。不要开 `.env`。
- 口播：开场句。
- 备注：不要指着菜单栏第四个按钮。本仓库 UI 还是 CLI，就拍终端，不要 P 一张不存在的三按钮界面充数。

### M1 邮件草稿 — 0:08–0:38（30s）可今天拍

- 画面：只留终端。执行下面一条。JSON 扫过即可，停在 `WROTE .../out/drafts/reply_*.md`。打开该文件，让首行注释和 `Subject:` 停两秒。
- 口播：Speak 句 `Reply and accept.` 或 `回复并接受`。然后补半句：“草稿留在本地。”
- 命令（英文成片）：

```bash
python -m src.pipeline.run --image tests/sample.png --transcript "Reply and accept." --mode do --do
```

- 命令（中文成片，与 `./demo.sh` 第 1 步相同）：

```bash
python -m src.pipeline.run --image tests/sample.png --transcript "回复并接受" --mode do --do
```

- 今天的产物就是 [demo_draft.md](demo_draft.md) 这一份模板：`Subject: Re: your request`，正文是接受意向，没有 Priya、没有周四。`tests/sample_email.txt` 不要在这条成片里冒充“被读过的邮件”。
- 备注：`confidence` 若进画，不要解释成百分比。Mac 上若同时生成 `out/drafts/open_mail_reply.applescript`，这条 1:50 里不要 `osascript`，避免送出按钮入画。

### M2 图表 PNG — 0:38–1:08（30s）可今天拍

- 画面：执行命令，停在 `WROTE .../out/charts/chart_*.png`，打开 PNG。柱子是 Notebook 最高、Monitor 最短。可以并排打开 `tests/sample_table.csv`，但下一句口播要跟上。
- 口播：`Chart the units column.` 或 `把 units 做成图表`。接着说：“这张图按仓库里的 sample_table.csv 画，第二列 units。不是从屏幕认出来的。”
- 命令（英文）：

```bash
python -m src.pipeline.run --image tests/sample.png --transcript "Chart the units column." --mode do --do
```

- 命令（中文，与 `./demo.sh` 第 2 步相同）：

```bash
python -m src.pipeline.run --image tests/sample.png --transcript "把 units 做成图表" --mode do --do
```

- 今天就能给观众看的是真实 PNG 文件。数据来源是 CSV，不是占位图。`revenue_usd` 列留在表上，图里没有这列。

### M3 本地报销记录 — 1:08–1:40（32s）可今天拍

- 画面：执行命令，打开 `out/expenses.json`。镜头停在 `merchant: unknown` 和 `amount: 0.0`。
- 口播：`Archive this expense.` 或 `归档报销`。接着说：“本地多了一条占位记录，没有提交到任何地方。”
- 命令（英文）：

```bash
python -m src.pipeline.run --image tests/sample.png --transcript "Archive this expense." --mode do --do
```

- 命令（中文，与 `./demo.sh` 第 3 步相同）：

```bash
python -m src.pipeline.run --image tests/sample.png --transcript "归档报销" --mode do --do
```

- 中文 `./demo.sh` 这条的 `note` 是 `[MOCK] 归档报销`。英文命令的 `note` 是 `[MOCK] Archive this expense.`。`date` 是运行当天。币种默认 `CNY`。不要把这条念成 Northwind Cafe 或 26.91。那是 Pass V 的期望，见 `tests/sample_expense_expected.json`。

### M4 收尾 — 1:40–1:50（10s）可今天拍

- 画面：三个路径同时在（`ls` 即可），与 `./demo.sh` 结尾一致。

```bash
ls -1 out/drafts/reply_*.md | tail -1
ls -1 out/charts/chart_*.png | tail -1
echo out/expenses.json
```

- 口播：收尾句。
- 中文一条龙：镜头外确认 `.venv` 后，正式镜头里可以改跑 `./demo.sh`（约 1 分钟内跑完三步），再按 M1–M3 打开三件产物，总长仍控制在 1:50。`./demo.sh` 不会读邮件、表格、收据样例。

---

## Pass V — 有真实 vision 之后 2:40

前提：当前 shell 里 `OPENAI_API_KEY` 已设置，镜头外用 Pass M 的 python 一行确认是 `set`，且 `source` 试跑一条是 `vision_llm` 而不是 `mock`。试跑不入画。

这一条才允许“指着屏幕上的内容”。Linux 仍用 `--image`：开拍前把三个样例各截一张，放到 `/tmp`（不要放进仓库，避免把选区图提交）：

- `/tmp/email_region.png` ← `tests/sample_email.txt`
- `/tmp/table_region.png` ← `tests/sample_table.csv`
- `/tmp/receipt_region.png` ← `tests/sample_receipt.txt`

不要拿 `tests/sample.png` 代替这三张。Mac 可以去掉 `--image`，用系统选区框住目标，再说话。框选取消会直接失败，正式镜头前先框一次。

每次只放一个目标，字号大到 1080p 能读。命令里的 `--transcript` 仍与口播同一句。

### V0 开场 — 0:00–0:10（10s）需要真实 vision 的成片，开场本身不调用模型

- 画面：桌面只留邮件样例窗口的一角 + 终端。终端里不要有 key。
- 口播：开场句。
- 备注：产品只有 Point、Speak、Do。口播按这个顺序走，不要加 Ask。

### V1 指邮件，说回复并接受 — 0:10–1:00（50s）需要真实 vision

1. **Point（0:10–0:22）** 全屏只有 `tests/sample_email.txt`：Priya Shah，主题 “Thursday design review — please accept”，周四 3:00pm，Studio B。Mac：开始框选。Linux：展示即将传入的那张邮件截图。
2. **Speak（0:22–0:32）** 口播 `Reply and accept.` 或 `回复并接受`。
3. **Do（0:32–1:00）** 切到终端执行命令，打开新的 `out/drafts/reply_*.md`。停住。不要打开 Mail 的发送按钮。

```bash
# Linux / 预先截好的邮件图。Mac 真框选时删掉 --image
python -m src.pipeline.run --image /tmp/email_region.png --transcript "Reply and accept." --mode do --do
```

中文把 transcript 换成 `回复并接受`。

- 期望：`task_type` 为 `draft_email`，`proposed_action.auto_send` 为 `false`，`source` 为 `vision_llm`。草稿主题接近 `Re: Thursday design review — please accept`，正文是接受周四评审的回复。有 sender 实体时问候会带上 Priya。文件头仍是 `NOT sent`。
- 这条若仍是 `source: mock` 或主题仍是 `Re: your request`：停，不要把这条剪进 Pass V。

### V2 指表格，说把 units 做成图表 — 1:00–1:45（45s）需要真实 vision

1. **Point（1:00–1:12）** 全屏 `tests/sample_table.csv`。六行产品，第二列 `units`（Notebook 420 … Monitor 48），第三列 `revenue_usd` 留在表上。
2. **Speak（1:12–1:20）** `Chart the units column.` 或 `把 units 做成图表`。点名 units：表上还有 `revenue_usd`，Do 会把意图里的每个数字实体都画出来。
3. **Do（1:20–1:45）** 打开 `out/charts/chart_*.png`，和表格并排。

```bash
python -m src.pipeline.run --image /tmp/table_region.png --transcript "Chart the units column." --mode do --do
```

- 期望：柱高跟屏幕上的 **units** 一致（Notebook 最高，Monitor 最短）。图是本地 PNG，没有上传。
- 备注：Do 在意图里没有数字实体时，会回退去画 `tests/sample_table.csv`。那张回退图跟这张表长得一样，所以不能只用“图和 CSV 一致”证明视觉成功。Pass V 要用一张**数字不同、且不是这个 CSV 文件**的表再拍一条备用镜头；柱高跟着那张表走，才说明读的是选区。备用镜头换不进 2:40 就放进彩排，不拿 mock 回退冒充。

### V3 指收据，说归档报销 — 1:45–2:28（43s）需要真实 vision

1. **Point（1:45–1:57）** 全屏 `tests/sample_receipt.txt`。Northwind Cafe，Receipt 1842，日期 2026-10-21，Total USD 26.91。
2. **Speak（1:57–2:05）** `Archive this expense.` 或 `归档报销`。
3. **Do（2:05–2:28）** 打开 `out/expenses.json` 最后一条。

```bash
python -m src.pipeline.run --image /tmp/receipt_region.png --transcript "Archive this expense." --mode do --do
```

- 期望字段（与 `tests/sample_expense_expected.json` 对齐）：`merchant` = `Northwind Cafe`，`amount` = `26.91`，`currency` = `USD`，`date` = `2026-10-21`。`note` 是模型写的意图句，不是收据页脚。没有网页提交，没有支付信息。
- 明细（浓缩咖啡 4.50、牛油果吐司 14.00、燕麦拿铁 6.25、税 2.16）留在收据画面上即可。Do 目前不把明细拆成独立字段。
- `unknown` / `0.0` / `CNY` 出现就停，这仍是 mock 占位，不能剪进 Pass V。

### V4 收尾 — 2:28–2:40（12s）可与 Pass M 相同的收尾画面

- 画面：草稿首行 `NOT sent`、图表 PNG、`expenses.json` 最后一条的商家和金额。三个文件路径用 `ls` 带过。
- 口播：收尾句。
- 计时：0:10+0:50+0:45+0:43+0:12 = 2:40，留 20 秒给口误重切。不要加第四个任务。

---

## 命令对照

| 任务 | `./demo.sh`（中文，mock，Linux 可用） | 英文 transcript（把最后的句号保留，与口播一致） |
|------|--------------------------------------|--------------------------------------------------|
| 邮件 | `--transcript "回复并接受"` | `--transcript "Reply and accept."` |
| 图表 | `--transcript "把 units 做成图表"` | `--transcript "Chart the units column."` |
| 报销 | `--transcript "归档报销"` | `--transcript "Archive this expense."` |

三条都要带 `--mode do --do`。Pass M 的 `--image` 固定 `tests/sample.png`。Pass V 换成该镜头的选区图；Mac 真框选时省略 `--image`。

产物路径：

| 任务 | 路径 |
|------|------|
| 草稿 | `out/drafts/reply_YYYYMMDD_HHMMSS.md` |
| Mac 可选，本片不录 | `out/drafts/open_mail_reply.applescript` |
| 图表 | `out/charts/chart_YYYYMMDD_HHMMSS.png` |
| 报销 | `out/expenses.json`（数组，每次追加） |

静帧对照：草稿 [demo_draft.md](demo_draft.md)，mock 图表 [demo_chart.png](demo_chart.png)，mock 报销行 [demo_expense_sample.json](demo_expense_sample.json)。操作细节在 [DEMO_NOTES.md](DEMO_NOTES.md)。
