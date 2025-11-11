"""
UNEP FI Citation Search Engine
核心搜索和匹配逻辑模块
"""

import pandas as pd
import numpy as np
from thefuzz import fuzz
from collections import Counter
import re


def normalize_text(text):
    """标准化文本用于匹配"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = ' '.join(text.split())
    return text


def preprocess_titles(unep_titles):
    """预处理UNEP FI报告标题"""
    processed_titles = {}
    for title in unep_titles:
        if pd.notna(title):
            normalized = normalize_text(title)
            processed_titles[title] = {
                'normalized': normalized,
                'words': set(normalized.split())
            }
    return processed_titles


def check_match(reference_text, report_title, processed_data, threshold=85):
    """
    检查引用文本是否匹配报告标题
    
    Args:
        reference_text: 引用文本
        report_title: 报告标题
        processed_data: 预处理的标题数据
        threshold: 相似度阈值
        
    Returns:
        dict: 包含匹配信息的字典，如果不匹配则返回None
    """
    if pd.isna(reference_text) or pd.isna(report_title):
        return None
    
    ref_normalized = normalize_text(reference_text)
    title_data = processed_data[report_title]
    title_normalized = title_data['normalized']
    
    # Method 1: 直接字符串包含
    if title_normalized in ref_normalized:
        return {
            'match_method': 'exact_substring',
            'similarity_score': 100.0
        }
    
    # Method 2: 模糊匹配
    similarity = fuzz.partial_ratio(title_normalized, ref_normalized)
    if similarity >= threshold:
        return {
            'match_method': 'fuzzy_match',
            'similarity_score': float(similarity)
        }
    
    # Method 3: 词语重叠匹配
    ref_words = set(ref_normalized.split())
    title_words = title_data['words']
    
    if len(title_words) >= 3:
        common_words = title_words & ref_words
        overlap_ratio = len(common_words) / len(title_words) * 100
        
        if overlap_ratio >= 70:
            return {
                'match_method': 'word_overlap',
                'similarity_score': float(overlap_ratio)
            }
    
    return None


def search_single_report(report_title, scopus_df, threshold=85):
    """
    搜索单个报告的引用情况
    
    Args:
        report_title: 报告标题
        scopus_df: Scopus引用数据DataFrame (必须包含 'Title' 和 'Reference' 列)
        threshold: 相似度阈值
        
    Returns:
        dict: 包含引用信息的字典
    """
    # 预处理标题
    processed_titles = preprocess_titles([report_title])
    
    matches = []
    reference_col = 'Reference'
    citing_paper_col = 'Title'
    
    # 检查必需的列
    if reference_col not in scopus_df.columns or citing_paper_col not in scopus_df.columns:
        raise ValueError(f"DataFrame必须包含 '{reference_col}' 和 '{citing_paper_col}' 列")
    
    # 搜索匹配
    for idx, row in scopus_df.iterrows():
        reference_text = row[reference_col]
        citing_paper = row[citing_paper_col]
        
        match_info = check_match(reference_text, report_title, processed_titles, threshold)
        
        if match_info:
            matches.append({
                'citing_paper': citing_paper,
                'reference_text': reference_text,
                'similarity_score': match_info['similarity_score'],
                'match_method': match_info['match_method']
            })
    
    # 计算统计信息
    if matches:
        citation_count = len(matches)
        avg_similarity = np.mean([m['similarity_score'] for m in matches])
        method_counts = Counter([m['match_method'] for m in matches])
        
        return {
            'report_title': report_title,
            'citation_count': citation_count,
            'average_similarity': round(avg_similarity, 2),
            'match_methods': dict(method_counts),
            'matches': matches
        }
    else:
        return {
            'report_title': report_title,
            'citation_count': 0,
            'average_similarity': 0,
            'match_methods': {},
            'matches': []
        }


def search_multiple_reports(report_titles, scopus_df, threshold=85, progress_callback=None):
    """
    批量搜索多个报告的引用情况
    
    Args:
        report_titles: 报告标题列表
        scopus_df: Scopus引用数据DataFrame
        threshold: 相似度阈值
        progress_callback: 进度回调函数
        
    Returns:
        list: 包含每个报告搜索结果的列表
    """
    results = []
    total = len(report_titles)
    
    for i, title in enumerate(report_titles, 1):
        result = search_single_report(title, scopus_df, threshold)
        results.append(result)
        
        if progress_callback:
            progress_callback(i, total, result)
    
    return results


def load_data_with_encoding(file_path):
    """
    尝试多种编码方式加载CSV文件
    """
    encodings = ['utf-8', 'utf-8-sig', 'gbk', 'gb18030', 'latin1']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding)
            return df
        except (UnicodeDecodeError, Exception):
            continue
    
    raise ValueError(f"无法读取文件 {file_path}，尝试了所有常见编码方式")
