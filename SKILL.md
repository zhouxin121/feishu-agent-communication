---
name: feishu-multi-agent-chat
description: 多个 AI Agent 在飞书群聊中通过 at 互相通信，实现多 Agent 协作。覆盖建群、创建Bot、拉Bot进群、获取open_id、text格式互 at 通信、防呆约束、故障排查全流程。Use when user says 飞书多Agent通信、Bot互at、飞书Bot创建、群聊AI协作、多Bot群聊。支持 CherryClaw、WorkBuddy、OpenClaw、AutoClaw 等框架。
keywords:
  - feishu
  - multi-agent
  - chatbot
  - collaboration
  - bot-communication
tested:
  date: "2026-07-10"
  os: macOS
  platform: feishu
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 4fd20e68f8b80beb1e39f35a6c960ac4_d580d0ce7ba411f1baf4525400bff409
    ReservedCode1: UDxKu7Oo3jBInc+578SB05d3p8Mzs2GjhGDIk+5rPKo5rLefAmFvYH9vVAX1QQCK3fXVJ8jJgcMGiK53o5sOLysQbVCoF8ttntz2dA+h/HYhXwPZXftlVUIPvcdg1B6XtN1NbvfHPWmksaPgiA1nWbxH3FRBvbd2RTpOQMcR3GZ02CG+1xGvSSGYQe4=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 4fd20e68f8b80beb1e39f35a6c960ac4_d580d0ce7ba411f1baf4525400bff409
    ReservedCode2: UDxKu7Oo3jBInc+578SB05d3p8Mzs2GjhGDIk+5rPKo5rLefAmFvYH9vVAX1QQCK3fXVJ8jJgcMGiK53o5sOLysQbVCoF8ttntz2dA+h/HYhXwPZXftlVUIPvcdg1B6XtN1NbvfHPWmksaPgiA1nWbxH3FRBvbd2RTpOQMcR3GZ02CG+1xGvSSGYQe4=
---



# 飞书多 Agent 群聊通信

> **v13.6.0 基础版** | 2026-07-10 | 免费公开，能跑通 ~30 分钟

多个 AI Agent 在飞书群里自动协作——建群 → 拉 Bot → 互 @ 通信 + 分工合作。

---

## Step 0：连接飞书

各框架统一操作：Agent 设置 → 频道 → 添加飞书 → 扫码。扫码后自动建立 WebSocket 长连接直连飞书群。

各框架原生扫码配置即可。

---

## Step 1：准备条件

- 飞书账号（免费注册 [feishu.cn](https://www.feishu.cn)）
- 创建飞书群（单人即可创建，可添加多个飞书机器人）
- 框架软件已安装并运行

---

## Step 2：创建飞书 Bot 应用

1. [飞书开放平台](https://open.feishu.cn/app) → 创建企业自建应用 → 添加「机器人」能力

2. 权限管理 → 逐一开通：

| 权限 | 状态 | 说明 |
|------|:--:|------|
| `im:message:send_as_bot` | ✅ 开 | 以 Bot 身份发送消息 |
| `im:message.group_at_msg:readonly` | ✅ 开 | 接收人类 @ 当前 Bot |
| `im:message.group_at_msg.include_bot:readonly` | ✅ 开 | 接收其他 Bot @ 当前 Bot（最关键） |
| `im:message.group_msg` | ❌ 关 | 与 `group_at_msg` 互斥——两个同时开，`group_msg` 的事件路由会把带 @ 的消息当普通消息处理、不触发 @ 判断 |

> **最小权限集**：`group_msg` 关 + 两个 `group_at_msg` 开 = 群内仅在 @ 时响应。

3. ⚠️ 事件订阅：「事件与回调」页面有 **「事件配置」和「回调配置」两个独立 Tab**，必须分别点进去 → 分别点「验证」→ 分别点「保存」。只做一边连不上 WebSocket。

   - 两个 Tab 的订阅方式均选「使用长连接接收事件」
   - 事件配置 Tab 需添加事件 `im.message.receive_v1`

4. 记下 App ID（`cli_` 开头）和 App Secret

5. 创建版本 → 发布（一般免审核，几秒通过）

---

## Step 3：获取群号

手机飞书 App → 进群 → 右上角「…」→ 群设置 → 拖到底部 → 群号。格式：`oc_` 开头。

### Step 3.5：把 Bot 拉进群（最容易漏掉！）

群设置 → 群机器人 → 添加机器人 → 选择 Step 2 创建的 Bot。

---

## Step 4：Bot 间 @ 通信格式

### 必须用 text，不用 post/card

| 格式 | @ 标签写法 | Bot 间可靠性 |
|------|-----------|------------|
| **text** | `<at user_id="ou_xxx">名称</at>` | ✅ 所有框架一致解析 |
| post | `{"tag":"at","user_id":"ou_xxx"}` | ❌ CherryClaw 不解析，静默丢失 |
| interactive | 卡片内 @ 标签 | ❌ 富文本/卡片中 @ 被忽略 |

原因：不同框架 SDK 序列化 post 方式不同，实测 CherryClaw 不解析 post 格式 @ 标签。

> **"text 格式"仅指 msg_type 和 @ 标签的承载方式，不约束消息正文。** 消息正文可以包含 Markdown 排版、结构化数据、代码块、表格等——只需全部放在 `content.text` 字符串内、@ 标签用 `<at>` 语法即可。

### @ 标签写法

```
<at user_id="ou_xxx">Bot名称</at>
```

- 属性名 `user_id`，值是 `ou_xxx` 格式的 open_id（不是 `cli_xxx` App ID）
- `<at>` 嵌在 `content.text` 字符串内
- 禁止用 `&lt;` `&gt;` HTML 转义，直接用原始 `<at>` 标签

⚠️ Agent 会"意译"模板而非逐字执行——模板指令必须加"请逐字复制，不要修改任何字符"。

### 发送方式

通过飞书 REST API（`POST /im/v1/messages`）发送。需要 `msg_type=text`，`content.text` 内含 `<at>` 标签。

| 参数 | 值 |
|------|-----|
| API 端点 | `POST /im/v1/messages?receive_id_type=chat_id` |
| `msg_type` | `text` |
| `content.text` | 含 `<at user_id="ou_xxx">名称</at>` 的字符串 |
| `receive_id` | 群号（`oc_` 开头） |

> **⚠️ 别把 @ 符号当成真 @**
> 群里显示"@云端主agent"不等于是真 @。只有通过飞书 REST API 发送 `content.text` 中含 `<at user_id="ou_xxx">` 标签的消息，才会触发对方的 @ 通知。纯文本 `@名称` 只是普通文字。

---

## open_id：App 隔离 + 获取方式

飞书 open_id 是 **App 隔离**的——同一 Bot 在不同 App 视角下 open_id 不同。

### 获取 open_id 的方法

对方 Bot 在群里发消息 → 从 WebSocket 事件回调中取 `event.sender.sender_id.open_id`。

### 冷启动闭环

对方 Bot 还没发过消息 → 你没有它的 open_id。此时你 @ 它时，必须在消息里附带自己的显式 open_id。对方用这个 open_id 就能直接 @ 回你。

### app_id / open_id / user_id 不要混淆

| ID | 格式 | 用途 | 获取方式 |
|----|------|------|---------|
| `app_id` | `cli_` 开头 | 拉 Bot 进群时填写 | 飞书开放平台 → 应用凭证 |
| `open_id` | `ou_` 开头 | 发消息、@ 人时填写 | WebSocket 事件 |
| `user_id` | 企业自定义 | 跨应用打通用户数据，不能用于 @ | `/contact/v3/users` API |

---

## Step 5：五步验证闭环

| 步骤 | 内容 | 验证目标 |
|:--:|------|----------|
| ① | 往群里发一条普通 text 消息 | Bot 能否发消息到群 |
| ② | 人类在群里 @ Bot | 本对话收到回复 |
| ③ | Bot 用 text+at @ 其他 Bot（附带自己 open_id） | 对方回复 |
| ④ | 其他 Bot 用 text+at @ 本 Bot | 本对话收到 |
| ⑤ | 多 Bot 链式 @ 协作 | 全链路畅通 |

> 五步验证中 ③④⑤ 任意一步卡住，通常需要手动翻 WebSocket 事件排查 open_id 不匹配和 @ 标签格式错误。赞赏版部署文档含每步期望日志 + 自动诊断 + 一键验证脚本，<10 分钟跑通。

---

## 故障排查

| # | 现象 | 原因 | 解决 |
|---|------|------|------|
| 1 | Bot 不响应 | 没把 Bot 拉进群 | Step 3.5，群设置 → 群机器人 → 添加 |
| 2 | WebSocket 连不上 | 事件/回调只点订阅没验证保存 | Step 2 第 3 步，两个 Tab 分别验证+保存 |
| 3 | @ 了对方没收到 | 用了 post 格式 | 改为 text 格式（Step 4） |
| 4 | @ 了对方没收到 | open_id 是其他 App 视角的 | 从 WebSocket 事件取自己视角 open_id |
| 5 | @ 了对方没收到 | `<at>` 被转义成 `&lt;at&gt;` | 不要 HTML 转义，直接用原始标签 |
| 6 | 收到群内所有消息 | 开了 `im:message.group_msg` | 关闭该权限 |

---

## LLM/AI 防呆说明

以下 6 条来自实测——LLM 和 Agent 会反复犯同样的错。

| # | 错 | 为什么错 | 正确做法 |
|---|-----|---------|---------|
| 1 | "回复并 @ 我" | Agent 无法从语境推断"我"= 谁 | 给出完整 `<at user_id="ou_xxx">@名称</at>` 模板 |
| 2 | 模板被"意译" | LLM 理解意图后改写格式 | 强调"逐字复制，不要修改任何字符" |
| 3 | 教别人用 post 格式 | Agent A 按飞书官方文档教 Agent B，但 CherryClaw 不解析 post | 标注平台差异 |
| 4 | 纯文本 `@名称` 当 @ 触发 | LLM 混淆"包含 @ 文字"和"真正的 @ 通知" | @ 触发只能通过飞书 API `<at>` 标签 |
| 5 | 403 看错误文字就下结论 | "free quota exhausted" 不一定是配额问题 | 403 排查顺序：路由 → 权限 → 格式 → 配额 |
| 6 | 权限全开还是不行 → 归因框架 bug | 没检查对端的发送格式 | 优先查对端是否用 post/转义 `<at>`，再怀疑框架 |

---

## 架构约束

### CherryClaw 框架层过滤 Bot 消息

即使飞书权限全对、格式全对，CherryClaw 在框架层检查 `sender_type == "app"` 并主动丢弃。因此 Bot 间通信必须走飞书 HTTP API 直接发送，绕过框架的入站过滤。

### 一个飞书 App 只能有一个 WebSocket

同一 App ID 不能同时被多个框架进程连接。多框架共用同一群时，每个框架需注册独立的飞书 App。

---

> Bot 间 @ 通信只需记住：**text 格式 + `<at user_id="自己App视角的open_id">` 嵌在 content.text 内。** post 不行、别人的 open_id 不可靠、必须附带显式 ID。

---

## 版本记录

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v13.6.0-base | 2026-07-10 | 基础版：保留 Step 0-5 执行骨架，移除 OpenClaw 集成章节、curl 示例、精确指令模板、架构图（以上放赞赏版） |
| v13.0.0 | 2026-07-09 | 架构重构：Gateway→框架原生IM通道；通信格式 post→text；新增 open_id App隔离+安全约束 |
| v13.1.0 | 2026-07-09 | 新增「LLM/AI 防呆说明」6 条；故障排查新增 2 条；Step 4 指令约束加强 |
| v13.2.0 | 2026-07-09 | 新增「三个 ID 区分」「架构约束」章节；权限互斥警告强化 |
| v13.5.0 | 2026-07-09 | user_id 陷阱强化 |
| v13.6.0 | 2026-07-10 | 完整版：新增 OpenClaw 集成章节、curl 示例、精确指令模板、deployment 文档引导 |

---

## 参考链接

1. https://open.feishu.cn/document/home/index
2. https://open.feishu.cn/document/server-docs/im-v1/message-content-description/create-content
3. https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/send
4. https://open.feishu.cn/document/server-docs/event-subscription-guide/overview
5. https://docs.openclaw.ai/
6. https://github.com/openclaw/openclaw
7. https://clawhub.ai/
8. https://pay.ldxp.cn/item/t7ktxb （赞赏获得10分钟内完成部署的文档）
9. https://clawhub.ai/glassmarbles/feishu-agent-relay
10. https://docs.cherrystudio.ai/

*（内容由AI生成，仅供参考）*
