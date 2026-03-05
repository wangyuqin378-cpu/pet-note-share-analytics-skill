#!/usr/bin/env python3
"""
宠物小伙伴分享笔记 UV 日报生成脚本

用法:
    python daily_uv_report.py --start 20260201 --end 20260304
    python daily_uv_report.py --days 30
"""

import argparse
import subprocess
import json
import sys
from datetime import datetime, timedelta


def run_query(sql, label="宠物分享笔记统计"):
    """执行 SQL 查询并返回结果"""
    cmd = [
        "npx", "mcporter", "call", "dor.execute_sql",
        f"sql={sql}",
        f"label={label}",
        "max_rows=100"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="/home/node/.openclaw/workspace")
    return result.stdout


def get_daily_uv(start_date, end_date):
    """获取指定日期范围的每日 UV 数据"""
    sql = f"""
    SELECT 
        dtm, 
        COUNT(DISTINCT from_id) as uv, 
        COUNT(*) as pv 
    FROM redods.ods_shequ_cny_cnypet_pet_message_di 
    WHERE sub_type IN ('note_card', 'note_card_fb') 
        AND dtm BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY dtm 
    ORDER BY dtm
    """
    return run_query(sql, f"宠物分享笔记UV_{start_date}_{end_date}")


def get_msg_type_distribution(date):
    """获取指定日期的消息类型分布"""
    sql = f"""
    SELECT sub_type, COUNT(*) as cnt 
    FROM redods.ods_shequ_cny_cnypet_pet_message_di 
    WHERE dtm = '{date}' 
    GROUP BY sub_type 
    ORDER BY cnt DESC
    """
    return run_query(sql, f"消息类型分布_{date}")


def format_date(date_str):
    """将 YYYYMMDD 格式化为 YYYY-MM-DD"""
    return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"


def calculate_change(current, previous):
    """计算环比变化"""
    if previous == 0:
        return "N/A"
    change = ((current - previous) / previous) * 100
    return f"{change:+.1f}%"


def main():
    parser = argparse.ArgumentParser(description="生成宠物小伙伴分享笔记 UV 日报")
    parser.add_argument("--start", help="开始日期 (YYYYMMDD)")
    parser.add_argument("--end", help="结束日期 (YYYYMMDD)")
    parser.add_argument("--days", type=int, help="最近 N 天")
    parser.add_argument("--type-dist", action="store_true", help="同时输出消息类型分布")
    
    args = parser.parse_args()
    
    # 计算日期范围
    if args.days:
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y%m%d")
    elif args.start and args.end:
        start_date = args.start
        end_date = args.end
    else:
        # 默认最近 7 天
        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y%m%d")
    
    print(f"📊 宠物小伙伴分享笔记 UV 统计")
    print(f"📅 统计时间: {format_date(start_date)} ~ {format_date(end_date)}")
    print("-" * 50)
    
    # 获取 UV 数据
    result = get_daily_uv(start_date, end_date)
    print(result)
    
    # 如果需要消息类型分布
    if args.type_dist:
        print("\n📈 消息类型分布 (最新一天):")
        print("-" * 50)
        type_result = get_msg_type_distribution(end_date)
        print(type_result)


if __name__ == "__main__":
    main()
