# AI Mouse — Demo 一页纸

**产品：** AI Mouse。对外只有 Point / Speak / Do。  
**安全：** Do 写草稿、写 PNG、追加本地 JSON。`auto_send` 在 schema 里固定为 `false`，代码再强制一次。没有发送、没有对外提交。  
**录屏分镜：** [RECORDING_SCRIPT.md](RECORDING_SCRIPT.md)（Pass M 今天就能拍，Pass V 等视觉模型）。

在仓库根目录（与 `demo.sh` 同级）执行：

```bash
./demo.sh
```

第一次会建 `.venv` 并安装依赖。镜头外先跑通，再 `rm -rf out` 拍正式的。Linux 和非 Mac 走 `--image`，`demo.sh` 已经带了 `tests/sample.png`。

## `./demo.sh` 的三步

脚本依次调用 `python -m src.pipeline.run --image tests/sample.png --mode do --do`，transcript 为：

| 步 | transcript | task_type | 写到哪里 |
|----|------------|-----------|----------|
| 1/3 | `回复并接受` | `draft_email` | `out/drafts/reply_YYYYMMDD_HHMMSS.md` |
| 2/3 | `把 units 做成图表` | `make_chart` | `out/charts/chart_YYYYMMDD_HHMMSS.png` |
| 3/3 | `归档报销` | `log_record` | `out/expenses.json`（没有就新建，有则往数组末尾加一条） |

结束时脚本会 `ls` 最新的草稿和 PNG，并打印 `out/expenses.json`。Mac 上第 1 步还会写 `out/drafts/open_mail_reply.applescript`。手动 `osascript out/drafts/open_mail_reply.applescript` 只是打开回复窗并填正文，脚本里没有发送。默认定时录屏不要跑这句。

`out/` 被 gitignore，产物留在本机。

## 每个产物里实际是什么

### 草稿 `out/drafts/reply_*.md`

与仓库静帧 [demo_draft.md](demo_draft.md) 同文：

- 首行：`<!-- AI Mouse DRAFT — auto_send=false, NOT sent -->`
- mock 主题：`Subject: Re: your request`
- 正文是接受意向的模板，不引用画面里的发件人或主题

mock 不读 `tests/sample_email.txt`。那封邮件是 Pass V 的 Point 目标（Priya Shah，主题 “Thursday design review — please accept”）。视觉模型若返回 `subject` / `sender` 实体，草稿主题和问候才会换成那封邮件的内容。

### 图表 `out/charts/chart_*.png`

mock 不从截图里取数。意图里没有数字实体时，Do 读取 `tests/sample_table.csv`，用第 1 列当标签、第 2 列 `units` 当柱高。第 3 列 `revenue_usd` 留在表上。`./demo.sh` 的口播是 `把 units 做成图表`（英文 `Chart the units column.`），点名 units，因为意图里若同时有两列数字，Do 会把每个数字实体都画上。

六根柱：Notebook 420、Pens 180、Lamp 95、Chair 64、Monitor 48、Headset 210。静帧 [demo_chart.png](demo_chart.png) 就是这张表生成的图。

### 报销 `out/expenses.json`

一次 `./demo.sh` 之后，文件是只含一条的 JSON 数组，形状同 [demo_expense_sample.json](demo_expense_sample.json)：

| 字段 | mock 今天 | 含义 |
|------|-----------|------|
| merchant | `unknown` | 没有 merchant 实体 |
| amount | `0.0` | 没有 amount 实体 |
| currency | `CNY` | 没有 currency 实体时的默认 |
| date | 运行当天的 `YYYY-MM-DD` | 没有 date 实体时用本机日期。静帧里的 `2026-10-28` 是示例日期 |
| note | `[MOCK] 归档报销` | 意图字符串，等于 `[MOCK]` 加 transcript |
| source_image | `sample.png` | `--image` 的文件名 |

再跑一次会再追加一条，不会覆盖。英文 transcript `Archive this expense.` 时，`note` 变成 `[MOCK] Archive this expense.`。

真实收据在 `tests/sample_receipt.txt`（Northwind Cafe，Receipt 1842，2026-10-21，合计 26.91 USD）。视觉模型应当抽出的字段写在 `tests/sample_expense_expected.json`。mock 不会产生那份商家和金额。Do 不把咖啡、吐司、拿铁、税额拆成独立字段。

## 样例文件

| 路径 | 用途 |
|------|------|
| `tests/sample.png` | `./demo.sh` 的占位图。400×200，文字是 “Q3 revenue up 12%” |
| `tests/sample_email.txt` | Pass V 对着念的邮件 |
| `tests/sample_table.csv` | 图表数据。图用 `product` + `units` |
| `tests/sample_receipt.txt` | Pass V 对着念的收据 |
| `tests/sample_expense_expected.json` | 视觉模型读收据后，报销行应接近的字段 |
| `docs/demo_draft.md` | mock 草稿静帧 |
| `docs/demo_chart.png` | mock 图表静帧 |
| `docs/demo_expense_sample.json` | mock 报销文件静帧（一条数组） |

## 接上 OPENAI_API_KEY

程序只读进程环境，不会自己加载 `.env`。`.env` 已被 gitignore，不要提交，也不要拍进录屏。

镜头外、在跑 `./demo.sh` 的同一个 shell 里设置变量 `OPENAI_API_KEY`。值从密码管理器来，不要写进仓库、不要写进分镜、不要出现在命令回显里。

可选变量名（仍不要把值写进 git）：

- `OPENAI_BASE_URL` — 兼容端点；不设就用官方默认
- `VISION_MODEL` — 不设时代码用 `gpt-4o-mini`

没有 `OPENAI_API_KEY` 时才使用 `ANTHROPIC_API_KEY`，可选 `ANTHROPIC_MODEL`（默认 `claude-sonnet-4-5`）。

确认时只打印是否存在，不打印值：

```bash
python -c 'import os; print("OPENAI_API_KEY", "set" if os.getenv("OPENAI_API_KEY") else "unset")'
```

设上之后同一条 `./demo.sh` 会走视觉模型，意图里 `source` 应为 `vision_llm`。`auto_send` 仍是 `false`。Pass V 不要再用 `tests/sample.png` 充当邮件、表格和收据，换成三张真正的选区图，见录屏分镜。

拍 mock 时这个变量保持 unset，避免一条成片里混进真实调用。

## 转述用的一句

指哪、说哪、做哪。三个动作准备好草稿、图和本地记录，发送权留在人手。

## Ask 旁路（对内）

`--entry capture_region` 仍进同一条 Do。对外不说成第四个功能，录屏里不演示。
