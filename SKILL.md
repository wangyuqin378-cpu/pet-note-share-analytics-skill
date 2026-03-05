---
name: pet-note-share-analytics
description: 分析宠物小伙伴（宠物 AI 对话）中用户分享笔记的 UV/PV 数据。用于查询每日分享笔记的用户数、分享次数，支持自定义时间范围统计。使用场景：宠物小伙伴产品数据监控、运营效果评估、分享功能使用率分析。
---

# Pet Note Share Analytics

用于分析宠物小伙伴（宠物 AI 对话功能）中用户分享笔记的数据。

## 数据表信息

**主数据表**: `redods.ods_shequ_cny_cnypet_pet_message_di`
- 表中文名：新版本宠物对话内容信息表
- 分区字段：`dtm` (格式: YYYYMMDD)
- 数据范围：2024-08-20 起

**关键字段**:
- `from_id`: 消息发送者 ID（用户/宠物）
- `sub_type`: 消息子类型，分享笔记为 `note_card` 和 `note_card_fb`
- `dtm`: 日期分区

## 常用查询

### 1. 查询每日分享笔记 UV/PV

```sql
SELECT 
    dtm, 
    COUNT(DISTINCT from_id) as uv, 
    COUNT(*) as pv 
FROM redods.ods_shequ_cny_cnypet_pet_message_di 
WHERE sub_type IN ('note_card', 'note_card_fb') 
    AND dtm BETWEEN '20260201' AND '20260304'
GROUP BY dtm 
ORDER BY dtm
```

### 2. 查看所有消息类型分布

```sql
SELECT sub_type, COUNT(*) as cnt 
FROM redods.ods_shequ_cny_cnypet_pet_message_di 
WHERE dtm = '20260304' 
GROUP BY sub_type 
ORDER BY cnt DESC
```

### 3. 查询特定日期范围的人均分享次数

```sql
SELECT 
    dtm,
    COUNT(DISTINCT from_id) as uv,
    COUNT(*) as pv,
    ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT from_id), 2) as avg_per_user
FROM redods.ods_shequ_cny_cnypet_pet_message_di 
WHERE sub_type IN ('note_card', 'note_card_fb') 
    AND dtm >= '20260201'
GROUP BY dtm 
ORDER BY dtm DESC
LIMIT 30
```

## 消息类型说明

| sub_type | 说明 |
|---------|------|
| `simple_text` | 普通文本消息 |
| `emoji` | 表情消息 |
| `note_card` | 分享笔记卡片 |
| `note_card_fb` | 分享笔记卡片（反馈）|
| `voice_with_text` | 语音转文字 |
| `instant_reply` | 即时回复 |
| `image_text` | 图文消息 |
| `ref_text` | 引用文本 |

## 使用流程

1. **确认表结构**（如需）：
   ```bash
   npx mcporter call crux.get_table_schema table_name="redods.ods_shequ_cny_cnypet_pet_message_di"
   ```

2. **确认分区范围**（如需）：
   ```bash
   npx mcporter call crux.get_table_partitions table_name="redods.ods_shequ_cny_cnypet_pet_message_di" size:10
   ```

3. **执行查询**：
   ```bash
   npx mcporter call dor.execute_sql sql="SELECT ..." label="宠物分享笔记统计"
   ```

## 注意事项

- 日期格式使用 `YYYYMMDD`（如 `20260304`）
- 分享笔记类型包含 `note_card` 和 `note_card_fb`
- 大表查询必须添加 `dtm` 分区过滤
- 数据从 2024-08-20 开始增量同步，此前为历史全量

## 参考文件

- [表结构详情](references/table-schema.md)
- [查询示例](references/query-examples.md)
- [数据分析脚本](scripts/daily_uv_report.py)
