# 飞书多Agent群聊通信

## 解决什么问题

多个 AI Agent 各自孤立运行，每次想传消息只能手动搬运。本方案：建一个飞书群，多个 Agent 拉进去，群里发消息自动认领处理，处理完自动 @ 下一个。

## 适用场景

- 主持者 Agent 接收用户指令，@执行者 Agent 派发任务
- 多 Agent 群内协作，无需手动切换或复制粘贴
- 一人管理多个 Bot，各司其职互不干扰

## 文件结构

```
feishu-multi-agent-communication/
├── SKILL.md                      # Agent 执行指令（Step 0-5）
├── README.md                     # 本文件（人类阅读）
├── references/
│   └── 配置模板.yaml              # 填写你的 Bot 信息
└── scripts/
    └── validate_config.py         # 配置校验脚本
```

## 快速开始

1. 飞书开放平台创建应用，开通机器人 + 事件订阅 + im 权限 → 发布版本
2. 填写 `references/配置模板.yaml` → 运行 `python scripts/validate_config.py`
3. 群内发消息测试：`@执行者 通信测试，请回复"收到"`
4. 跑通后按 SKILL.md 的 Step 4-5 设定角色和任务派发

## 配置中常见问题

| # | 现象 | 控制台路径 | 排查方向 |
|---|------|-----------|----------|
| 1 | 消息发了 Agent 没反应 | 飞书后台 → 应用 → 事件与回调 → 事件订阅 | 开启"通过长连接接收事件" → 发布版本 |
| 2 | 机器人读不到群消息 | 飞书后台 → 应用 → 权限管理 | 确认 `im:message:read_as_bot` 已添加 → 发布版本 |
| 3 | 发消息返回 403 | —— | 每个 Bot 对同一用户有不同 open_id，不能混用 |
| 4 | 群 ID 获取不到 | 手机飞书 App → 群设置 | 飞书网页版后台不显示，需手机查看（oc_ 开头） |
| 5 | @别人对方收不到 | —— | @标签 user_id 必须填 open_id（ou_ 开头），不能填 cli_ |
| 6 | Token 过期中断 | —— | 确保 Gateway 配置了 Tenant Token 自动刷新 |

## DO/DON'T

| DO ✅ | DON'T ❌ |
|------|----------|
| 每条发给对方的消息开头加 @标签 | 用 cli_ 会话ID 替代 open_id |
| 权限修改后发布应用版本 | 用 post/interactive 格式（必须 text） |
| 运行 validate_config.py 后再测试 | 意译/修改 @标签中的 Bot 名字 |
| 执行者不直接响应用户 | 权限修改不发布就测试 |

完整部署文档可以在10分钟内完成部署。

## 参考与感谢

- 飞书开放平台文档: https://open.feishu.cn/
- 飞书事件订阅指南: https://open.feishu.cn/document/server-docs/event-subscription-guide/overview
- OpenClaw: https://github.com/openclaw/openclaw
- 同类 Skill: https://github.com/relunctance/feishu-multi-agent-relay
- 同类 Skill: https://clawhub.ai/glassmarbles/feishu-agent-relay
- 社区实践: https://devpress.csdn.net/v1/article/detail/159314664
- 架构参考: https://vaitk.com/blog/multi-agent-system-architecture-guide
- 感谢 ClawHub Weather: https://clawhub.ai/steipete/weather
- 感谢 ClawHub GitHub: https://clawhub.ai/steipete/github
