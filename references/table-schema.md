# 宠物对话内容信息表结构

## 表基本信息

| 属性 | 值 |
|------|-----|
| **表名** | `redods.ods_shequ_cny_cnypet_pet_message_di` |
| **中文名** | 新版本宠物对话内容信息表 |
| **数据库** | redods |
| **创建时间** | 2024-08-20 |
| **生命周期** | 366天 |
| **负责人** | 本间(刘华) |
| **存储格式** | Avro |

## 数据说明

- **20240819分区**：历史全量数据
- **20240820及以后**：增量同步
- **总分区数**：368+（持续增长）
- **最新分区**：20260304

## 字段列表

| 字段名 | 类型 | 中文名 | 说明 |
|--------|------|--------|------|
| id | bigint | id | 主键id |
| session_id | bigint | session_id | 会话session_id |
| uuid | string | uuid | 消息流水id |
| from_id | bigint | from_id | 消息发送者id |
| from_role | string | from_role | 消息发送者角色（PET/USER）|
| target_id | bigint | target_id | 消息接受者id |
| target_role | string | target_role | 消息接受者角色 |
| chat_id | string | chat_id | 由 from_id 和 target_id 拼接成会话id |
| content | string | content | 消息内容（JSON格式）|
| type | int | type | 消息类型 |
| sub_type | string | sub_type | 消息子类型 |
| content_status | int | content_status | 消息内容审核状态 |
| follow_uuid | string | follow_uuid | 依赖的消息流水id |
| store_id | int | store_id | store id |
| extra_info | string | extra_info | 预留字段 |
| create_time | string | create_time | 创建时间 |
| update_time | string | update_time | 更新时间 |
| **dtm** | string | - | **分区字段** |

## 消息类型 (sub_type)

| sub_type | 说明 | 示例场景 |
|---------|------|---------|
| `simple_text` | 普通文本消息 | 用户/宠物发送文字 |
| `emoji` | 表情消息 | 发送表情包 |
| `note_card` | 分享笔记卡片 | 用户分享笔记给宠物 |
| `note_card_fb` | 分享笔记卡片反馈 | 宠物对笔记的反馈 |
| `voice_with_text` | 语音转文字 | 发送语音消息 |
| `instant_reply` | 即时回复 | 快速回复选项 |
| `image_text` | 图文消息 | 发送图片+文字 |
| `ref_text` | 引用文本 | 引用前文回复 |

## 分享笔记统计口径

**UV（去重用户数）**: `COUNT(DISTINCT from_id)`
- 统计当天分享笔记的去重用户
- 需过滤 `sub_type IN ('note_card', 'note_card_fb')`

**PV（分享次数）**: `COUNT(*)`
- 统计当天分享笔记的总次数

## 典型数据示例

```json
{
  "id": 137824944678413784,
  "session_id": 137824944661743644,
  "uuid": "137824944678413784.208380386445383692.7407042552213617505",
  "from_id": 7407042552213617505,
  "from_role": "PET",
  "target_id": 208380386445383692,
  "target_role": "USER",
  "chat_id": "208380386445383692.7407042552213617505",
  "content": "{\"original_content\":\"嗨，你今天遇见了什么让你心动的事情吗？\"}",
  "type": 1,
  "sub_type": "simple_text",
  "content_status": 1,
  "follow_uuid": null,
  "store_id": 243,
  "extra_info": "{\"model_name\": \"qwen3_sft_dpo_v1_1_ideal_1_12_wo9_online_1_tolan_1_20250724\"}",
  "create_time": "2026-03-04 00:38:44.598000",
  "update_time": "2026-03-04 00:38:45",
  "dtm": "20260304"
}
```
