---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: 4fd20e68f8b80beb1e39f35a6c960ac4_f61e4a0d7c0811f1938f5254006c9bbf
    ReservedCode1: c9FLwKbOANadA/Snt8OowjFcdubTXv2/PkP6OMgJ4cVnDatsiImWfOMohJD5m0roYlMprh1hgsfsPI7M5JIxr+ZNsDtdHDQ56RiIcCaBBFT/NyDDgvcs94mV5i8a9d3Gy2YlxprvHF285Bq8r2jddGbNnCLtIbKLwBSIU5gNsjhdJZfTvM7hggwOBIQ=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: 4fd20e68f8b80beb1e39f35a6c960ac4_f61e4a0d7c0811f1938f5254006c9bbf
    ReservedCode2: c9FLwKbOANadA/Snt8OowjFcdubTXv2/PkP6OMgJ4cVnDatsiImWfOMohJD5m0roYlMprh1hgsfsPI7M5JIxr+ZNsDtdHDQ56RiIcCaBBFT/NyDDgvcs94mV5i8a9d3Gy2YlxprvHF285Bq8r2jddGbNnCLtIbKLwBSIU5gNsjhdJZfTvM7hggwOBIQ=
---

# 飞书多 Agent 群聊通信

多个 AI Agent 在飞书群聊中通过 @ 互相通信，实现多 Bot 协作——建群、创建 Bot、拉 Bot 进群、互 @ 通信 + 分工合作。

## 痛点与场景

飞书不原生支持 Bot 间对话，CherryClaw 等框架在框架层过滤 Bot 消息。本项目提供完整的 text 格式互 @ 通信方案，让多个 Agent 在飞书群中协作：代码审查 Agent + 云端主 Agent + 部署 Agent 等。

## 核心流程（Step 0-5）

| 步骤 | 内容 |
|------|------|
| Step 0 | 连接飞书（扫码建立 WebSocket） |
| Step 1 | 准备条件（飞书账号、群、框架） |
| Step 2 | 创建飞书 Bot 应用（权限配置、事件订阅、发布上线） |
| Step 3 | 获取群号 + 拉 Bot 进群 |
| Step 4 | Bot 间 @ 通信格式（text + `<at>` 标签 + HTTP API） |
| Step 5 | 五步验证闭环 |

## 关键技术点

- **text 格式（非 post）**：CherryClaw 不解析 post 格式 @ 标签，必须用 text 格式 + `<at user_id="ou_xxx">` 嵌在 `content.text` 内
- **open_id App 隔离**：同一 Bot 在不同 App 视角下 open_id 不同，必须从 WebSocket 事件取自己视角的 open_id
- **CherryClaw 框架层过滤**：框架检查 `sender_type == "app"` 并主动丢弃，Bot 间通信必须走飞书 HTTP API

## 踩坑方向

| # | 现象 | 控制台/路径 | 排查方向 |
|---|------|-----------|---------|
| 1 | Bot 不响应 | 群设置 → 群机器人 | 检查 Bot 是否已拉进群 |
| 2 | WebSocket 连不上 | 飞书开放平台 → 事件与回调 | 两个 Tab 分别验证+保存 |
| 3 | @ 了对方没收到 | 发送端消息日志 | 检查是否用了 post 格式 |
| 4 | @ 了对方没收到 | WebSocket 事件 JSON | open_id 是否为自己 App 视角 |
| 5 | @ 了对方没收到 | 发送端 content.text | `<at>` 是否被 HTML 转义 |
| 6 | 收到群内所有消息 | 飞书开放平台 → 权限管理 | `group_msg` 是否误开 |

## 时间成本对比

| 版本 | 调试时间 | 适用场景 |
|------|---------|---------|
| 基础版（本仓库） | ~30 分钟 | 有飞书开发经验，愿意手动排查 open_id/格式问题 |
| 完整版（含部署文档） | <10 分钟 | 含每步期望日志 + 自动诊断 + 一键验证脚本 |

## 文件结构

```
feishu-agent-communication/
├── SKILL.md      # 完整技术文档（Step 0-5 + 故障排查 + 防呆约束 + 集成路径）
└── README.md     # 本文件（概览与决策层信息）
```

## 参考链接

1. [飞书开放平台文档](https://open.feishu.cn/document/home/index)
2. [消息内容结构](https://open.feishu.cn/document/server-docs/im-v1/message-content-description/create-content)
3. [发送消息 API](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/message/send)
4. [事件订阅概览](https://open.feishu.cn/document/server-docs/event-subscription-guide/overview)
5. [OpenClaw 文档](https://docs.openclaw.ai/)
6. [OpenClaw GitHub](https://github.com/openclaw/openclaw)
7. [CherryStudio 文档](https://docs.cherrystudio.ai/)
8. [ClawHub](https://clawhub.ai/)
9. [feishu-agent-relay](https://clawhub.ai/glassmarbles/feishu-agent-relay)
10. [飞书官网](https://www.feishu.cn/)
*（内容由AI生成，仅供参考）*
