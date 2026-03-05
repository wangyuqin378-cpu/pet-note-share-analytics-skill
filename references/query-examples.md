# 查询示例

## 基础查询

### 1. 查询最近7天分享笔记 UV

```sql
SELECT 
    dtm, 
    COUNT(DISTINCT from_id) as uv, 
    COUNT(*) as pv 
FROM redods.ods_shequ_cny_cnypet_pet_message_di 
WHERE sub_type IN ('note_card', 'note_card_fb') 
    AND dtm >= CAST(DATE_SUB(CURRENT_DATE, 7) AS STRING FORMAT 'yyyyMMdd')
GROUP BY dtm 
ORDER BY dtm DESC
```

### 2. 查询指定月份每日数据

```sql
SELECT 
    dtm,
    COUNT(DISTINCT from_id) as uv,
    COUNT(*) as pv,
    ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT from_id), 2) as avg_per_user
FROM redods.ods_shequ_cny_cnypet_pet_message_di 
WHERE sub_type IN ('note_card', 'note_card_fb') 
    AND dtm LIKE '202602%'
GROUP BY dtm 
ORDER BY dtm
```

### 3. 对比不同消息类型的占比

```sql
SELECT 
    sub_type,
    COUNT(*) as msg_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as pct
FROM redods.ods_shequ_cny_cnypet_pet_message_di 
WHERE dtm = '20260304'
GROUP BY sub_type 
ORDER BY msg_count DESC
```

## 进阶分析

### 4. 周环比分析

```sql
WITH daily_stats AS (
    SELECT 
        dtm,
        COUNT(DISTINCT from_id) as uv,
        COUNT(*) as pv
    FROM redods.ods_shequ_cny_cnypet_pet_message_di 
    WHERE sub_type IN ('note_card', 'note_card_fb')
        AND dtm >= '20260201'
    GROUP BY dtm
),
weekly_stats AS (
    SELECT 
        SUBSTR(dtm, 1, 6) as year_month,
        FLOOR((CAST(SUBSTR(dtm, 7, 2) AS INT) - 1) / 7) + 1 as week_num,
        AVG(uv) as avg_uv,
        AVG(pv) as avg_pv
    FROM daily_stats
    GROUP BY SUBSTR(dtm, 1, 6), FLOOR((CAST(SUBSTR(dtm, 7, 2) AS INT) - 1) / 7) + 1
)
SELECT * FROM weekly_stats ORDER BY year_month, week_num
```

### 5. 活跃用户分层

```sql
-- 统计某段时间内用户的分享频次分布
SELECT 
    share_freq,
    COUNT(*) as user_count
FROM (
    SELECT 
        from_id,
        COUNT(*) as share_freq
    FROM redods.ods_shequ_cny_cnypet_pet_message_di 
    WHERE sub_type IN ('note_card', 'note_card_fb')
        AND dtm BETWEEN '20260201' AND '20260228'
    GROUP BY from_id
) t
GROUP BY share_freq
ORDER BY share_freq
```

### 6. 时段分析（需结合 create_time）

```sql
SELECT 
    HOUR(create_time) as hour_of_day,
    COUNT(DISTINCT from_id) as uv,
    COUNT(*) as pv
FROM redods.ods_shequ_cny_cnypet_pet_message_di 
WHERE sub_type IN ('note_card', 'note_card_fb')
    AND dtm = '20260304'
GROUP BY HOUR(create_time)
ORDER BY hour_of_day
```

## 使用 mcporter 执行

```bash
# 基础查询
npx mcporter call dor.execute_sql \
    sql="SELECT dtm, COUNT(DISTINCT from_id) as uv FROM redods.ods_shequ_cny_cnypet_pet_message_di WHERE sub_type IN ('note_card', 'note_card_fb') AND dtm >= '20260301' GROUP BY dtm ORDER BY dtm" \
    label="宠物分享笔记UV查询" \
    max_rows=30

# 异步查询（大数据量）
npx mcporter call dor.submit_sql \
    sql="SELECT ..." \
    label="宠物数据分析"

# 查询任务状态
npx mcporter call dor.get_task_status msg_id="<msg_id>"

# 获取结果
npx mcporter call dor.get_result msg_id="<msg_id>" max_rows=100
```
