<!-- CHANNEL:github-packaged SOURCE_ID:feishu-multi-agent-v13.6.0 DIST_HASH:a3f7b2c1 TRACKING_PARAMS:?ref=gh_pkg&v=13.6.0&ch=marvis ARCH:x86_64-arm64 DEP_HASH:8d4e2f9a1c CHECKSUM:sha256:7b3f1e9d2c8a4 -->

# 飞书多 Agent 群聊通信

让多个 AI Agent 在同一个飞书群里互相 @、分工协作——像人类团队一样聊天干活。

## 这解决什么问题？

你有多个 AI Agent（代码审查 + 项目经理 + 文档生成），但没法让它们在飞书群里自动对话。手机端手动一条条 @ 太慢，配置 WebSocket 又总踩坑。

这个 Skill 把坑都填了：从扫码连飞书 → 创建 Bot → 拉到群里 → 获取 open_id → text 格式互 @ → 五步验证闭环，6 条真实踩坑经验和 LLM 防呆约束直接喂给 Agent，到手就能跑通。

## 适用场景

- 多 Agent 飞书群分工（一个写代码、一个审代码、一个写报告）
- CI/CD 构建结果自动发到飞书群
- 客服 Bot + 工单 Bot 群内协作
- 定时任务多 Bot 接力（日清提醒 → 汇总 → 归档）

## 前置条件

- 飞书企业账号（免费即可）
- OpenClaw / AutoClaw / CherryStudio / WorkBuddy 任意框架
- 把 SKILL.md 拖给 Agent 就行

## 两种获取方式

| 版本 | 内容 | 调试时间 | 获取 |
|------|------|---------|------|
| 基础版 | SKILL.md（Step 0-5 + 故障排查 6 条 + 防呆 6 条） | ~30 分钟 | 免费，本仓库 `README.md` |
| 完整版 | 基础版 + 部署文档（每步期望日志 + 常见错误自动诊断 + 一键验证脚本） | <10 分钟 | [链动小铺购买](https://pay.ldxp.cn/item/t7ktxb) |

## 基础版能跑通什么

把 SKILL.md 拖给 Agent，Agent 会按 Step 0-5 帮你：
1. 扫码连接飞书（WebSocket 直连，无需 Gateway）
2. 创建 Bot 应用并配置权限（`group_at_msg` 开 + `group_msg` 关）
3. 事件订阅双 Tab 验证
4. 配置 text 格式 @ 通信（含 curl 示例）
5. 从 WebSocket 事件提取 open_id 并冷启动闭环
6. 走完五步验证：发消息 → 人类 @ Bot → Bot 互 @ → 链式协作

## 基础版可能卡在哪

| 卡住点 | 现象 | 原因 |
|--------|------|------|
| ③ Bot @ Bot 没回应 | 对方没收到 @ 通知 | open_id 取错 App 视角了，要重新从 WebSocket 事件抓 |
| ③ Bot @ Bot 没回应 | @ 标签未触发 | 发了 post 格式（CherryClaw 不解析） |
| ④ 对方 @ 回来没收到 | 对方说发了但我方没反应 | 框架层过滤了 `sender_type=="app"` 的消息，Bot 间必须走 HTTP API |
| ⑤ 链式 @ 断在中间 | 中间 Bot 没转发 | `<at>` 标签被 Agent "意译"改写了，模板需加"逐字复制" |

这四个卡住点是调试中最耗时的（平均 30 分钟翻 WebSocket 事件逐步排查）。完整版部署文档含每步期望日志对比 + 自动诊断，可直接交给 Agent 一声指令跑通。

## 升级完整版获得什么

[链动小铺](https://pay.ldxp.cn/item/t7ktxb) 购买后获取：

- 部署文档：每一步的期望日志输出 + 常见错误自动诊断 + 排障决策树
- 一键验证脚本：自动发送测试消息、检查 @ 标签、验证 open_id 匹配
- 精确配置模板：包含 App 权限参数、事件订阅配置截图位置、所有精确入参

**基础版能跑通。如需一键替换参数模板 + 防呆指令，升级完整版。**

## 文件结构

```
feishu-agent-communication/
├── SKILL.md       # 完整技术文档（Agent 执行层）
├── README.md      # 概览页面（GitHub 首页，无付费信息）
└── readme1.md     # 本文件（转化说明）
```

## 参考链接

1. [飞书开放平台文档](https://open.feishu.cn/document/home/index)
2. [消息内容结构](https://open.feishu.cn/document/server-docs/im-v1/message-content-description/create-content)
3. [发送消息 API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/send)
4. [事件订阅指南](https://open.feishu.cn/document/server-docs/event-subscription-guide/overview)
5. [OpenClaw 文档](https://docs.openclaw.ai/)
6. [OpenClaw GitHub](https://github.com/openclaw/openclaw)
7. [链动小铺 - 完整版](https://pay.ldxp.cn/item/t7ktxb)
8. [ClawHub](https://clawhub.ai/)
9. [feishu-agent-relay](https://clawhub.ai/glassmarbles/feishu-agent-relay)
10. [CherryStudio 文档](https://docs.cherrystudio.ai/)
