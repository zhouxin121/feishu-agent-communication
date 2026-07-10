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
    ProduceID: 4fd20e68f8b80beb1e39f35a6c960ac4_f56e91577c0811f1baf4525400bff409
    ReservedCode1: B7ja/MsklMvnLFKnpIlOG4T80rxBDJn6w7aY5LzIKGzsGRo2X5zFDRNxEGoS5+PjzGJNRXWC2y1ChvFpHHh5tLH9acSwKaxHsSmRDhIRGdnXNlZIphXvbGbC611jEaWB7U33aa7RLm63MvyTLKo46DPt/td4B47v+V/GIV0VpXVSJx+Pe6QkCNyOwrQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 4fd20e68f8b80beb1e39f35a6c960ac4_f56e91577c0811f1baf4525400bff409
    ReservedCode2: B7ja/MsklMvnLFKnpIlOG4T80rxBDJn6w7aY5LzIKGzsGRo2X5zFDRNxEGoS5+PjzGJNRXWC2y1ChvFpHHh5tLH9acSwKaxHsSmRDhIRGdnXNlZIphXvbGbC611jEaWB7U33aa7RLm63MvyTLKo46DPt/td4B47v+V/GIV0VpXVSJx+Pe6QkCNyOwrQ=
---





# 飞书多 Agent 群聊通信

> **v13.6.0** | 2026-07-10 | Step 5 新增部署文档引导（链动小铺链接）

多个 AI Agent 在飞书群里自动协作——建群 → 拉 Bot → 互 @ 通信 + 分工合作。

---

## Step 0：连接飞书

各框架统一操作：Agent 设置 → 频道 → 添加飞书 → 扫码。扫码后自动建立 WebSocket 长连接直连飞书群。

| 框架 | 实现方式 |
|------|---------|
| CherryStudio | CherryClaw + 扫码 |
| WorkBuddy 桌面版 | 内置飞书连接器（lark-cli + 扫码） |
| OpenClaw / AutoClaw | `@openclaw/feishu` 插件直连（详见末尾「集成路径」章节） |
| 其他框架 | 各框架原生扫码配置 |

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

> ⚠️ 权限和事件配置完成后，必须「创建版本 → 发布上线」。草稿状态所有配置不生效，一般免审核，几秒通过。

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

> **"text 格式"仅指 msg_type 和 @ 标签的承载方式，不约束消息正文。** 消息正文可以包含 Markdown 排版、结构化数据（JSON/YAML）、代码块、表格等任意格式——只需全部放在 `content.text` 字符串内、@ 标签用 `<at>` 语法即可。Bot 间的富文本通信用消息正文的结构化约定来解决，不靠 post 的 `content` 数组。

### @ 标签写法

```
<at user_id="ou_xxx">Bot名称</at>
```

- 属性名 `user_id`，值是 `ou_xxx` 格式的 open_id（不是 `cli_xxx` App ID）
- `<at>` 嵌在 `content.text` 字符串内
- 禁止用 `&lt;` `&gt;` HTML 转义，直接用原始 `<at>` 标签

⚠️ Agent 会"意译"模板而非逐字执行——实测 `<at user_id="ou_xxx">@名称</at>` 被 Agent 改写成 `<at id=ou_xxx></at>`（`user_id=` 变 `id=`、丢了名称文本）。**模板指令必须加"请逐字复制，不要修改任何字符"。**

### 完整飞书 API 调用示例

```bash
curl -X POST https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"receive_id":"oc_xxx","msg_type":"text","content":"{\"text\":\"<at user_id=\\\"ou_xxx\\\">Bot名称</at> 消息内容\"}"}'
```

### 三段式消息约定

```
🔔 发送者 → 接收者
任务：具体任务描述
状态：已完成 / 进行中 / 待确认
需操作：具体内容
<at user_id="ou_xxx">接收者名称</at>
```

必含字段：`任务`、`状态`、`需操作`；可选字段：`结论`、`附件`。

---

> **⚠️ 别把 @ 符号当成真 @**
>
> 群里显示"@云端主agent"不等于是真 @。只有通过飞书 REST API（`POST /im/v1/messages`）发送 `content.text` 中含 `<at user_id="ou_xxx">` 标签的消息，才会触发对方的 @ 通知（颜色变蓝、通知提醒）。用聊天通知工具（如 `mcp__claw__notify`）发的纯文本 `@名称` 只是普通文字，不会触发。

---

## open_id：App 隔离 + 唯一获取方式

飞书 open_id 是 **App 隔离**的——飞书官方文档原文："同一个 user_id 在不同应用中的 open_id 不同""不要在跨应用的数据通信过程中使用 open_id"。同一 Bot 在不同 App 视角下 open_id 不同。

### 获取 open_id 的唯一正确方法（只有一种）

对方 Bot 在群里发消息 → 从 WebSocket 事件回调中取 `event.sender.sender_id.open_id`。

```json
{"event":{"sender":{"sender_id":{"open_id":"ou_xxx"}}},"message":{"mentions":[{"id":{"open_id":"ou_xxx"},"name":"Bot名"}]}}}
```

| 取什么 | 从哪里 | 用途 |
|--------|--------|------|
| `sender.sender_id.open_id` | WebSocket 事件 | @ 回发送者 |
| `mentions[].id.open_id` | WebSocket 事件 | 知道谁被 @ 了 |

### 冷启动闭环：附带显式 open_id

对方 Bot 还没发过消息 → 你没有它的 open_id。此时你 @ 它时，**必须在消息里附带自己的显式 open_id + 格式模板**（见验证闭环第⑤步）。对方用这个 open_id 就能直接 @ 回你，无需先抓 WebSocket。

### app_id / open_id / user_id 不要混淆

LLM 容易在上下文里把三个 ID 混用。它们不可互换：

| ID | 格式 | 用途 | 获取方式 |
|----|------|------|---------|
| `app_id` | `cli_` 开头 | **拉 Bot 进群**时填写 | 飞书开放平台 → 应用凭证 |
| `open_id` | `ou_` 开头 | **发消息、@ 人**时填写 | WebSocket 事件 `sender.sender_id.open_id` |
| `user_id` | 企业自定义 | 跨应用打通用户数据，**不能用于 @** | 需 `contact:user.employee_id:readonly` 权限（企业专属）。⚠️ 即使拿到了也不能当 `open_id` 用—— `<at>` 标签只认 `ou_` 格式。Agent 常见错误：去 `/contact/v3/users` 取了 `user_id` 就往 `<at>` 里填 |

### 错误做法

| 做法 | 为什么错 |
|------|---------|
| 引用其他 Bot 给的 open_id | 那是它的 App 视角，不是你的 |
| `/contact/v3/users` API 取 user_id 当 open_id 用 | user_id ≠ open_id，格式不同（企业自定义 vs `ou_`），`<at>` 只认 `ou_` 格式 |
| `/contact/v3/users` API 查 Bot | 不返回 Bot 账号 |
| `/im/v1/chats/{chat_id}/members/bots` | **不是飞书官方 API**，不存在于开发者文档 |
| `bot/v3/info` API | 只返回自己的 open_id |
| 用 `app_id` 当 `open_id` 去 @ | 格式不同（cli_ vs ou_），API 直接拒绝 |

---

## Step 4.5：Agent 行为约束

1. 只响应明确 @ 了自己的消息，不响应 @ 其他 Bot 或群内普通聊天
2. 给其他 Bot 发 @ 请求时，**必须附带自己的显式 open_id 和格式模板**——只说"@ 我"对方无法分辨"我"是谁
3. Bot 间连续对话不超过 5 轮，超过等人类介入
4. 涉及文件修改/配置/代码的请求，先回复"需要人类确认：[具体改动]"等同意

---

## 架构约束（为什么必须走 HTTP API）

### 飞书不原生支持 Bot 间对话

飞书官方文档原文："该接口不会返回群组内的机器人成员"。飞书的设计哲学里 Bot 是"工具"不是"对话参与者"。多 Bot 互通必须自己建中间层。

### CherryClaw 框架层过滤 Bot 消息

即使飞书权限全对、格式全对，**CherryClaw 在框架层检查 `sender_type == "app"` 并主动丢弃**。这不是配置问题，是框架行为。

因此 Bot 间通信**必须走飞书 HTTP API**（`POST /im/v1/messages`）直接发送，绕过 CherryClaw 的入站过滤。

### 一个飞书 App 只能有一个 WebSocket

同一 App ID 不能同时被多个框架进程连接。如果多框架共用同一群，每个框架需要注册独立的飞书 App。

### 已验证的架构

```
Bot A（CherryClaw）                 Bot B（CherryClaw）
    │                                    │
    ├─ 收人类消息: WebSocket ✅          ├─ 收人类消息: WebSocket ✅
    ├─ 收 Bot 消息: ❌ 框架过滤          ├─ 收 Bot 消息: ❌ 框架过滤
    │                                    │
    ├─ 发消息到群: HTTP API              ├─ 发消息到群: HTTP API
    │   msg_type=text                    │   msg_type=text
    │   content.text 内嵌 <at>           │   content.text 内嵌 <at>
    │                                    │
    └─ 取对方 open_id:                   └─ 取对方 open_id:
        等对方先发 → WebSocket 事件            等对方先发 → WebSocket 事件
        sender.sender_id.open_id               sender.sender_id.open_id
```

---

## Step 5：五步验证闭环

| 步骤 | 内容 | 验证目标 |
|:--:|------|----------|
| ① | 往群里发一条普通 text 消息 | Bot 能否发消息到群 |
| ② | 人类在群里 @ Bot | 本对话收到回复 |
| ③ | Bot 用 text+at @ 其他 Bot（附带自己 open_id + 格式模板） | 对方回复 |
| ④ | 其他 Bot 用 text+at @ 本 Bot | 本对话收到 |
| ⑤ | 多 Bot 链式 @ 协作 | 全链路畅通 |

> **提示**：五步验证看起来简单，但实际调试中 90% 的时间花在排查 open_id 不匹配和 @ 标签格式错误上——③④⑤ 任意一步卡住，平均需要 30 分钟逐条翻 WebSocket 事件。

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

以下 6 条来自实测——LLM 和 Agent 会反复犯同样的错，需在 SKILL 中明确标注。

| # | 错 | 为什么错 | 正确做法 |
|---|-----|---------|---------|
| 1 | "回复并 @ 我" | Agent 无法从语境推断"我"= 谁 | 给出完整 `<at user_id="ou_xxx">@名称</at>` 模板 + "逐字复制" |
| 2 | 模板被"意译" | LLM 理解意图后改写格式 | 强调"逐字复制，不要修改任何字符" |
| 3 | 教别人用 post 格式 | Agent A 按飞书官方文档教 Agent B，但 CherryClaw 不解析 post | 标注平台差异："以下格式适用于 XXX 框架，不适用于 YYY 框架" |
| 4 | 纯文本 `@名称` 当 @ 触发 | LLM 混淆"包含 @ 文字"和"真正的 @ 通知" | @ 触发只能通过飞书 API `<at>` 标签 |
| 5 | 403 看错误文字就下结论 | "free quota exhausted" 不一定是配额问题 | 403 排查顺序：路由 → 权限 → 格式 → 配额 |
| 6 | 权限全开还是不行 → 归因框架 bug | 没检查对端的发送格式 | 优先查对端是否用 post/转义 `<at>`，再怀疑框架 |

### Agent 间精确指令模板

| 场景 | ❌ 模糊指令 | ✅ 精确指令 |
|------|-----------|-----------|
| 请求对方回复并 @ | "回复并 @ 我" | "请用 `<at user_id="ou_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx">@测试agent</at>` 格式回复。逐字复制，不要修改。" |
| 通知对方项目进度 | "发一下项目进度" | "请发送项目进度。完成后用 `<at user_id="ou_xxx">@XXX</at>` 通知我。" |
| 确认收到 | "收到" | "`<at user_id="ou_xxx">@XXX</at>` 收到，格式验证通过。" |
| 强调平台差异 | "用 post 发 @ 消息" | "⚠️ CherryClaw 平台请使用 text 格式，不要用 post。" |

---

> Bot 间 @ 通信只需记住：**text 格式 + `<at user_id="自己App视角的open_id">` 嵌在 content.text 内。** post 不行、别人的 open_id 列表不可靠、必须附带显式 ID。

---

## 集成路径：OpenClaw/AutoClaw 框架原生通道

如果你使用 OpenClaw 或 AutoClaw 框架，可通过 `@openclaw/feishu` 插件直连飞书，简化 Bot 创建和事件订阅流程。插件自动管理 WebSocket 连接、事件订阅、权限配置，你只需关注 Agent 绑定和多 Agent 路由即可。

### 1. 安装插件

```bash
openclaw plugins install @openclaw/feishu
```

### 2. 配置飞书频道（交互式引导）

```bash
openclaw channels login --channel feishu
```

向导提供两种方式：
- **手动输入**：粘贴飞书开放平台的 App ID（`cli_` 开头）和 App Secret
- **扫码自动创建**：在飞书 App 中扫描二维码，自动创建 Bot 并锁定私信

向导会询问 API 域名（`feishu` / `lark`）和群组策略。完成后重启网关：

```bash
openclaw gateway restart
```

通过 `openclaw gateway status` 和 `openclaw logs --follow` 确认连接状态。

### 3. 多 Agent 路由绑定（openclaw.yaml 配置）

> 注意：OpenClaw 的 `openclaw.yaml` 是其框架内部进程的配置文件（管理 WebSocket 连接和消息路由），不是我们 v13 方案中已淘汰的中间层 Gateway。名称巧合，不要混淆。

在 `openclaw.yaml` 配置文件中设置 `agents.list` 和 `bindings`，将不同群聊路由到不同 Agent（`workspace` 路径按你的实际环境填写）：

```json5
{
  agents: {
    list: [
      { id: "master-agent" },
      { id: "review-agent" },
      { id: "deploy-agent" },
    ],
  },
  bindings: [
    // 主控 Agent → 协调群
    {
      agentId: "master-agent",
      match: {
        channel: "feishu",
        peer: { kind: "group", id: "oc_coord_group" },
      },
    },
    // 审查 Agent → 独立群
    {
      agentId: "review-agent",
      match: {
        channel: "feishu",
        peer: { kind: "group", id: "oc_review_group" },
      },
    },
    // 部署 Agent → 私信
    {
      agentId: "deploy-agent",
      match: {
        channel: "feishu",
        peer: { kind: "direct", id: "ou_admin_open_id" },
      },
    },
  ],
}
```

路由字段说明：
- `match.channel`：固定为 `"feishu"`
- `match.peer.kind`：`"direct"`（私信）或 `"group"`（群聊）
- `match.peer.id`：用户 `open_id`（`ou_` 开头）或群号（`oc_` 开头）

### 4. 群组访问控制

```json5
{
  channels: {
    feishu: {
      groupPolicy: "allowlist",
      groupAllowFrom: ["oc_coord_group", "oc_review_group"],
      // 按群覆盖配置
      groups: {
        oc_coord_group: { requireMention: true },
      },
    },
  },
}
```

| 策略值 | 行为 |
|--------|------|
| `"open"` | 回复所有群消息（默认不要求 @ 提及） |
| `"allowlist"` | 仅回复 `groupAllowFrom` + `groups.*` 显式配置的群 |
| `"disabled"` | 禁用所有群消息 |

### 5. 多账号配置

当一个 openclaw 实例需要挂载多个飞书 Bot 时：

```json5
{
  channels: {
    feishu: {
      defaultAccount: "bot1",
      accounts: {
        bot1: {
          appId: "cli_bot1_xxx",
          appSecret: "xxx",
          name: "云端主Agent",
        },
        bot2: {
          appId: "cli_bot2_yyy",
          appSecret: "yyy",
          name: "审查Agent",
        },
      },
    },
  },
}
```

### 6. 与手动路径的差异

| 步骤 | 手动路径（Step 0-5） | OpenClaw 插件路径 |
|------|-------------------|------------------|
| Bot 创建 | 飞书开放平台手动创建 | `channels login` 向导 / 扫码自动创建 |
| WebSocket | 各框架自行配置连接 | 插件自动管理 |
| 事件订阅 | 两个 Tab 分别手动验证保存 | 插件自动配置事件 + 权限 |
| 权限配置 | 飞书后台逐项勾选 | 插件自动申请 |
| 多 Agent 路由 | 各 Agent 各自监听 WebSocket | openclaw.yaml bindings 统一路由 |
| 发布上线 | 手动创建版本提交审核 | 插件引导（仍需手动发布） |
| group_at_msg 互斥 | 手动控制 `group_msg` 关闭 | 插件自动处理互斥 |

> **关键提醒**：即使用 OpenClaw 插件，三条规则不变：① Bot 间 @ 通信**必须走飞书 HTTP API**（框架层 `sender_type=="app"` 过滤不因插件而消失）；② text 格式 + open_id App 隔离 + 防呆约束**全部适用**；③ 一个飞书 App 一个 WebSocket → 多 Bot 需注册多个 App。

---

## 版本记录

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v13.0.0 | 2026-07-09 | 架构重构：Gateway→框架原生IM通道；通信格式 post→text；新增 open_id App隔离+安全约束；联网验证通过 |
| v13.1.0 | 2026-07-09 | 新增「LLM/AI 防呆说明」6 条 + Agent 间精确指令模板；故障排查新增 403 路由、模板意译 2 条；Step 4 指令约束加强 |
| v13.2.0 | 2026-07-09 | 新增「三个 ID 区分」「架构约束」章节；权限互斥警告强化；框架层 sender_type 过滤说明；发布上线强调 |
| v13.3.0 | 2026-07-09 | 新增 ClawHub 标准 YAML front matter（name/description/tags）；新增「OpenClaw/AutoClaw 框架原生通道」章节（插件安装、多 Agent 绑定、Gateway JSON 配置模板、群组访问控制、多账号配置） |
| v13.4.0 | 2026-07-09 | 人类视角审校 8 项修正（语义、框架表、权限原因、免审核时间、真实 open_id 脱敏、去平台路径、Gateway 术语澄清） |
| v13.5.0 | 2026-07-09 | user_id 陷阱强化：「三个 ID 区分」明确 user_id 不能用于 @；「错误做法」新增 user_id 当 open_id 用、查 Bot 两条 |
| v13.6.0 | 2026-07-10 | Step 5 验证闭环下方新增链动小铺部署文档引导；keywords 替换 tags（ClawHub 正字段）；补齐 tested 元数据 |

---

## 参考链接

内置链接矩阵：

1. https://open.feishu.cn/document/home/index
2. https://open.feishu.cn/document/server-docs/im-v1/message-content-description/create-content
3. https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/send
4. https://open.feishu.cn/document/server-docs/event-subscription-guide/overview
5. https://docs.openclaw.ai/
6. https://github.com/openclaw/openclaw
7. https://clawhub.ai/
8. https://pay.ldxp.cn/item/t7ktxb （付费：部署文档+一键验证）
9. https://clawhub.ai/glassmarbles/feishu-agent-relay
10. https://docs.cherrystudio.ai/


*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
