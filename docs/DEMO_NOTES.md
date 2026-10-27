# AI Mouse — Demo 一页纸（内审 / 投资人转述用）

**产品：** AI Mouse｜Point / Speak / Do｜零说明书，最多三功能  
**安全：** Do 只出草稿、出图、写本地记录；`auto_send=false`（代码强制）；绝不自动发邮件  
**代码：** `/workspace/simtech-ai-mouse-agent`  
**一键跑：** `cd /workspace/simtech-ai-mouse-agent && ./demo.sh`（无需 API key）

## 三分钟看什么

| 口令 | 产物 | 路径示例 |
|------|------|----------|
| 回复并接受 | 邮件回复草稿（不发送） | `out/drafts/reply_20261027_143633.md` |
| 做成图表 | 图表 PNG | `out/charts/chart_20261027_143634.png` |
| 归档报销 | 本地费用 JSON 追加一行 | `out/expenses.json` |

## 当前状态（诚实）
- ✅ 选区截图 → 意图 JSON → Do 全链路可本地跑  
- ✅ mock 下三任务路由 + 真实产物  
- ⏳ 真实 vision 等 `OPENAI_API_KEY` 或 `ANTHROPIC_API_KEY`  
- ⏳ Mac 上 AppleScript 开 Mail 回复窗需实机测（脚本不发送）  
- Speak：电脑麦克风即可；硬件板载麦可选  

## 给转述的一句话
*指哪、说哪、做哪——三个动作完成办公闭环，系统只准备结果，发送权留在人手。*

## Ask 旁路（对内）
复杂题：`--entry capture_region` 区域截图，仍进同一 Do；对外不打成第四功能。
