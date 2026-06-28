---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 4fd20e68f8b80beb1e39f35a6c960ac4_082fd229731111f1986d525400d9a7a1
    ReservedCode1: ERYOqKJMdOzLT+yRrB+XvLH5+Qa4UdA5f+9Lzc18UOztcinIrfaTbgzPq4jPAu0agvfG7FaQ41aMCDxYaif44E3xxWKspMZMnIO5Mwvjxhj34q6Ctu8asBNBTiY0331VOQ6Thvh4DPBFFY6mvAM6apKEg1UAjyWee+Axl6faH9OAsaDyHMsnHE6nvEs=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 4fd20e68f8b80beb1e39f35a6c960ac4_082fd229731111f1986d525400d9a7a1
    ReservedCode2: ERYOqKJMdOzLT+yRrB+XvLH5+Qa4UdA5f+9Lzc18UOztcinIrfaTbgzPq4jPAu0agvfG7FaQ41aMCDxYaif44E3xxWKspMZMnIO5Mwvjxhj34q6Ctu8asBNBTiY0331VOQ6Thvh4DPBFFY6mvAM6apKEg1UAjyWee+Axl6faH9OAsaDyHMsnHE6nvEs=
---



# 飞书多Agent群聊通信

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

## 制作时间

约 2 周（含飞书平台踩坑 + Gateway 调试 + 多 Agent 联调测试）

## 基于环境

| 组件 | 版本/配置 |
|------|----------|
| OpenClaw | 标准版 |
| AutoClaw | 社区发行版 |
| 飞书开放平台 | 2026-06 版本 |
| 飞书 App | Android / iOS 最新版 |
| 测试 Agent | 3 个（代码/数据/项目管理） |

## 配置中常见问题

以下是实测过程中踩过的坑。你的 Agent 可以基于这些方向自行排查：

### 1. 配置文件路径搞混
- 方向：OpenClaw 标准版和 AutoClaw 使用不同的配置文件路径，改了不对的位置重启不会生效。

### 2. 消息收不到
- 方向：飞书开放平台后台有一个「通过长连接接收事件」开关，默认关闭。

### 3. 群 ID 获取不到
- 方向：飞书网页版后台不显示群 ID，需在手机飞书 App → 群设置中查看（`oc_` 开头）。

### 4. 机器人读不到群消息
- 方向：缺少消息读取权限，需在飞书后台开通后重新发布应用。

### 5. Token 过期导致中断
- 方向：飞书接入 Token 有时效限制，需确保 Gateway 支持自动刷新。

### 6. 多 Agent 按 @ 区分不生效
- 方向：路由是按群 ID 匹配而非 @ 语义，需通过消息前缀或关键词条件来区分。

### 7. Gateway 端口与实际监听不一致
- 方向：不同发行版可能覆写端口，Gateway 内部自动适配，一般不需手动处理。

### 8. 回复在群里显示为代码块
- 方向：消息格式选错会导致显示异常。

## 完整部署指南

以上问题在部署文档中有完整的配置模板、分步操作和详细解决方案。如果你希望你的 Agent 直接照着配置完成部署，可获取部署文档：

部署文档获取：https://pay.ldxp.cn/item/t7ktxb

## 依赖与致谢

| 项目 | 用途 | 链接 |
|------|------|------|
| OpenClaw | Agent Gateway 核心 | github.com/openclaw/openclaw |
| AutoClaw | 社区发行版，方案验证 | 社区项目 |
| 飞书开放平台 | Bot API + WebSocket | open.feishu.cn |

## 关键词

中文：飞书、多Agent、Agent协作、群聊通信、Gateway、OpenClaw、AutoClaw、WebSocket、消息路由

English: feishu, multi-agent, agent collaboration, group chat, gateway, openclaw, autoclaw, websocket, message routing

*（内容由AI生成，仅供参考）*
*（内容由AI生成，仅供参考）*
