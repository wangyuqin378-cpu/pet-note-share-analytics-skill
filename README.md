# Pet Note Share Analytics Skill

OpenClaw Skill for analyzing pet note sharing UV data from the pet companion feature.

## Overview

This skill helps analyze user engagement with the note sharing feature in the pet companion AI chat functionality.

## Files

```
├── SKILL.md                      # Main skill documentation
├── references/
│   ├── table-schema.md          # Database table schema details
│   └── query-examples.md        # SQL query examples
└── scripts/
    └── daily_uv_report.py       # Daily UV report generation script
```

## Quick Start

### Query Daily UV

```bash
npx mcporter call dor.execute_sql \
    sql="SELECT dtm, COUNT(DISTINCT from_id) as uv, COUNT(*) as pv FROM redods.ods_shequ_cny_cnypet_pet_message_di WHERE sub_type IN ('note_card', 'note_card_fb') AND dtm >= '20260301' GROUP BY dtm ORDER BY dtm" \
    label="宠物分享笔记UV查询"
```

### Using the Python Script

```bash
# Query last 7 days
python scripts/daily_uv_report.py --days 7

# Query specific date range
python scripts/daily_uv_report.py --start 20260201 --end 20260304

# Query with message type distribution
python scripts/daily_uv_report.py --days 7 --type-dist
```

## Data Table

**Table**: `redods.ods_shequ_cny_cnypet_pet_message_di`

| Field | Description |
|-------|-------------|
| `from_id` | User ID |
| `sub_type` | Message type (`note_card`, `note_card_fb` for note sharing) |
| `dtm` | Date partition (YYYYMMDD) |

## Metrics

- **UV**: Unique users who shared notes
- **PV**: Total note sharing events
- **Avg per user**: Average shares per user

## Author

Created for 玉斧 (wangyuqin2@xiaohongshu.com)
