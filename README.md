---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 4fd20e68f8b80beb1e39f35a6c960ac4_363a9cbe731011f1986d525400d9a7a1
    ReservedCode1: 4X0km/Pt+b8a/AypEivjTD+MDTEAeXcJBiu2XtNm18UITP4o0BKB/hINeWwCKK80ILCASW8fefShUPJuVR6BmLSDLYF2kVBRsaVoy7PWv1h0hUtsbEwA9XLw+Gujzk9tXr55AuT1xJu2F/qgi7lTandhr4JA1LeZg9UTuTIngKF5QJ3Dhb7/8IpEOMg=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 4fd20e68f8b80beb1e39f35a6c960ac4_363a9cbe731011f1986d525400d9a7a1
    ReservedCode2: 4X0km/Pt+b8a/AypEivjTD+MDTEAeXcJBiu2XtNm18UITP4o0BKB/hINeWwCKK80ILCASW8fefShUPJuVR6BmLSDLYF2kVBRsaVoy7PWv1h0hUtsbEwA9XLw+Gujzk9tXr55AuT1xJu2F/qgi7lTandhr4JA1LeZg9UTuTIngKF5QJ3Dhb7/8IpEOMg=
---

# 飞书多Agent群聊通信

![version](https://img.shields.io/badge/version-1.0.0-blue)

让多个 AI Agent 在飞书群里自动协作，你只需发消息，它们自动认领、处理、交接。

## 解决什么问题

当你同时使用多个 AI Agent（比如一个写代码、一个查资料、一个管项目），它们各自孤立运行，互不知道对方在干什么。每次想让一个 Agent 处理完通知另一个继续，只能手动搬运消息。

这个 Skill 让你：建一个飞书群，把多个 Agent 拉进去。群里发消息，对应 Agent 自动认领处理，处理完自动 @ 下一个继续。你从"搬运工"变回"老板"。

## 核心原理

```
飞书群发消息 → 飞书 WebSocket 推送 → Gateway 接收
→ 按路由规则匹配 → 分发到对应 Agent
→ Agent 处理 → 回复到群
```

一句话：飞书群当消息中台，Gateway 根据路由规则自动把消息分给对应 Agent。

## 实测效果

- **3 Agent 协作**：任务 → 5 秒拆解 → 并行处理 → 60 秒汇总回复
- **消息延迟**：< 1 秒
- **并发能力**：3 Agent 同时在线，无消息丢失
- **成本**：飞书免费版 100 万次/月 API 额度，个人使用绰绰有余

## 你需要准备

| 项目 | 说明 | 费用 |
|------|------|------|
| 飞书账号 | 个人免费注册 | 免费 |
| 飞书开放平台 | 创建机器人用 | 免费 |
| OpenClaw 或 AutoClaw | Agent 运行平台 | 免费开源 |
| 部署文档 | 含配置模板 + 分步操作 + 8 条踩坑详解 | 0.99元/年 |

## 配置中常见问题

1. **配置文件路径搞混** — OpenClaw 标准版和 AutoClaw 使用不同的配置文件路径
2. **消息收不到** — 飞书后台「通过长连接接收事件」开关默认关闭
3. **群 ID 获取不到** — 飞书网页版不显示群 ID，需在手机飞书 App 群设置中查看
4. **机器人读不到群消息** — 缺少 `im:message:read_as_bot` 权限
5. **Token 过期** — 飞书 Tenant Token 有效期 2 小时，需 Gateway 支持自动刷新
6. **多 Agent 区分不生效** — 路由按群 ID 匹配，需通过消息前缀或关键词条件区分
7. **Gateway 端口冲突** — AutoClaw 可能覆写端口，Gateway 内部自动适配
8. **回复显示为代码块** — 消息类型需用 `text` 而非 `post` 格式

## 如何获取

**SKILL.md** 在本仓库免费公开，提供完整思路、效果、出处和致谢。

完整部署文档（含配置模板 + 分步操作 + 8 条踩坑详解）通过链动小铺获取：

> https://pay.ldxp.cn/item/t7ktxb

## 依赖与致谢

| 项目 | 用途 | 链接 |
|------|------|------|
| OpenClaw | Agent Gateway 核心 | github.com/openclaw/openclaw |
| AutoClaw | 社区发行版，方案验证 | 社区项目 |
| 飞书开放平台 | Bot API + WebSocket | open.feishu.cn |

*内容由AI生成，仅供参考*
*（内容由AI生成，仅供参考）*
