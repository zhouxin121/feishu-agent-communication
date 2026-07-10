# 飞书多Agent群聊通信

## 解决什么问题

多个 AI Agent 各自孤立运行。建一个飞书群，把 Agent 拉进去，群里发消息对应 Agent 自动认领处理，处理完自动 @ 下一个继续。

## 核心原理

```
飞书群发消息 → 飞书 WebSocket 推送 → Gateway 按路由规则分发 → 对应 Agent 处理 → 回复到群
```

## Step 0: 准备清单

| 项目 | 说明 |
|------|------|
| 飞书账号 | 个人免费注册 |
| 飞书开放平台应用 | 创建企业自建应用，开启机器人能力 |
| OpenClaw/AutoClaw | Agent 运行平台 |
| 飞书群 | 已创建，群 ID 已知（oc_ 开头） |

## Step 1: 飞书应用创建

1. 登录飞书开放平台，创建企业自建应用
2. 添加机器人能力
3. 开通权限：`im:message`、`im:message:read_as_bot`、`im:message.group:readonly`
4. 事件订阅：订阅 `im.message.receive_v1` 事件，开启"通过长连接接收事件"
5. **发布应用版本**（未发布版本权限不生效）

## Step 2: 填写配置模板

打开 `references/配置模板.yaml`，将占位符替换为实际值。

运行配置校验：
```bash
python scripts/validate_config.py
```

## Step 3: @标签格式（防呆铁律）

**唯一正确格式**：
```xml
<at user_id="ou_对方的open_id">对方名字</at> 消息内容
```

**三条铁律**：
1. 消息类型必须用 `text` 格式，严禁 `post` / `interactive`
2. @标签 `user_id` 必须用 `open_id`（`ou_` 开头），严禁用 `cli_` 会话ID
3. 禁止意译 `display_name`，必须原样复制飞书群内显示的 Bot 名字

## Step 4: 角色分工

| 角色 | 职责 |
|------|------|
| 主持者 | 接收用户指令、分析拆解任务、@执行者派发、把关合规、代表用户决策 |
| 执行者 | 接收主持者@的任务、执行操作、完成后@主持者汇报、不直接响应用户 |

**消息模板**：
```
执行者名字 任务：xxxxx
要求：1. xxx 2. xxx
完成后@我汇报
```

## Step 5: 通信验证

```
1. 主持者发：执行者名字 通信测试，请回复"收到"
2. 执行者回：主持者名字 收到，通信正常
3. 无回复 → 查配置中常见问题 → 运行校验脚本 → 重试
```

## 配置中常见问题

### 1. 消息发到群里，Agent 没反应
方向：飞书开放平台 → 应用 → 事件与回调 → 事件订阅 → 开启"通过长连接接收事件" → 发布版本后重试

### 2. 机器人读不到群消息
方向：飞书开放平台 → 应用 → 权限管理 → 确认已添加 `im:message:read_as_bot` → 发布应用版本（未发布版本权限不生效）

### 3. 发消息返回 403 错误
方向：每个 Bot 对同一用户有不同 `open_id`，不能用 A 的 `open_id` 去给 B 发消息。核对 `open_id` 是否属于当前 Bot

### 4. 群 ID 获取不到
方向：飞书网页版后台不显示群 ID，需在手机飞书 App → 群设置 → 复制群 ID（`oc_` 开头）

### 5. @别人对方收不到
方向：@标签 `user_id` 必须为 `open_id`（`ou_`开头），不能填 `cli_` 会话ID。核对配置模板中的 ID 对照表

### 6. Token 过期导致中断
方向：飞书 Tenant Token 有效期 2 小时，确保 Gateway 配置了自动刷新机制

## DO

- 每条发给对方的消息开头必须包含 `<at>` 标签
- 发布权限修改后必须创建并发布应用版本
- 配置修改后运行 `validate_config.py` 校验
- 执行者不直接响应用户，由主持者转发

## DON'T

- 不要用 `cli_` 会话ID 替代 `open_id` 填入 @标签
- 不要用 `post`/`interactive` 格式发群消息
- 不要意译/修改 @标签中的 Bot 名字
- 不要忘记发布应用版本（权限修改不发布不生效）
- 不要混淆不同 Bot 的 `open_id`

## 参考与感谢

- 飞书开放平台文档: https://open.feishu.cn/
- 飞书事件订阅指南: https://open.feishu.cn/document/server-docs/event-subscription-guide/overview
- OpenClaw: https://github.com/openclaw/openclaw
- 同类 Skill: https://github.com/relunctance/feishu-multi-agent-relay
- 同类 Skill: https://clawhub.ai/glassmarbles/feishu-agent-relay
- 社区实践: https://devpress.csdn.net/v1/article/detail/159314664
- 架构参考: https://vaitk.com/blog/multi-agent-system-architecture-guide
- 基础版能跑通。如需一键替换参数模板 + 防呆指令，升级完整版: https://pay.ldxp.cn/item/t7ktxb
- 感谢 ClawHub Weather: https://clawhub.ai/steipete/weather
- 感谢 ClawHub GitHub: https://clawhub.ai/steipete/github
