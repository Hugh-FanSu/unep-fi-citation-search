"""
UNEP FI Report Citation Search System
Web Application with Streamlit - Professional Edition
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from citation_search_engine import (
    search_single_report, 
    search_multiple_reports,
    load_data_with_encoding
)
import os
import re
from typing import Set

st.set_page_config(
    page_title="UNEP FI Citation Search",
    page_icon="🇺🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Professional CSS
st.markdown("""<style>
    /* Main color scheme - UN Blue theme */
    :root {
        --un-blue: #009edb;
        --un-dark-blue: #00689d;
        --success-green: #56c02b;
        --warning-yellow: #f9c642;
        --text-dark: #2c3e50;
        --bg-light: #f8f9fa;
        --border-light: #e1e8ed;
    }
    
    /* Main header styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: var(--un-blue);
        text-align: center;
        margin-bottom: 1rem;
        padding: 2rem 0 1rem 0;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Card-based sections */
    .info-card {
        background: white;
        border: 1px solid var(--border-light);
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    /* Keyword search box */
    .keyword-search-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        color: #1565c0;
        padding: 1.8rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 2px solid #90caf9;
        box-shadow: 0 2px 8px rgba(33, 150, 243, 0.15);
    }
    
    .keyword-search-box strong {
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.8rem;
        color: #0d47a1;
    }
    
    .keyword-search-box code {
        background: white;
        color: #1976d2;
        padding: 3px 10px;
        border-radius: 4px;
        font-family: 'Monaco', 'Menlo', monospace;
        border: 1px solid #90caf9;
    }
    
    /* Filter active banner */
    .filter-active {
        background: linear-gradient(135deg, #fff9c4 0%, #fff59d 100%);
        color: #f57f17;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 2px solid #ffd54f;
        box-shadow: 0 2px 8px rgba(255, 193, 7, 0.2);
    }
    
    .filter-active strong {
        font-size: 1.15rem;
        display: block;
        margin-bottom: 0.5rem;
        color: #e65100;
    }
    
    /* Database selection */
    .database-selection {
        background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%);
        color: #00695c;
        padding: 1.8rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border: 2px solid #80cbc4;
        box-shadow: 0 2px 8px rgba(0, 150, 136, 0.15);
    }
    
    .database-selection strong {
        font-size: 1.1rem;
        display: block;
        margin-bottom: 0.8rem;
        color: #004d40;
    }
    
    /* Disclaimer */
    .disclaimer {
        background: #f8f9fa;
        border-left: 4px solid var(--un-blue);
        padding: 1.2rem 1.5rem;
        border-radius: 8px;
        margin-top: 2rem;
        font-size: 0.95rem;
        color: #495057;
        line-height: 1.6;
    }
    
    /* Buttons enhancement */
    .stButton button {
        border-radius: 8px;
        font-weight: 500;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Metrics styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
        color: var(--un-blue);
    }
    
    /* Dataframe styling */
    .dataframe {
        font-size: 0.9rem;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
    }
    
    [data-testid="stSidebar"] h2 {
        color: var(--un-blue);
        font-weight: 600;
    }
    
    /* Radio buttons */
    .stRadio > label {
        font-weight: 500;
        color: var(--text-dark);
    }
    
    /* Section headers */
    h3 {
        color: var(--un-dark-blue);
        font-weight: 600;
        margin-top: 2rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-light);
    }
    
    /* Success/Info messages */
    .stSuccess {
        background: rgba(86, 192, 43, 0.1);
        border-left: 4px solid var(--success-green);
        border-radius: 8px;
    }
    
    .stInfo {
        background: rgba(0, 158, 219, 0.1);
        border-left: 4px solid var(--un-blue);
        border-radius: 8px;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
        }
    }
</style>""", unsafe_allow_html=True)

def normalize_keyword(keyword: str) -> str:
    return keyword.strip().lower()

def generate_word_variants(word: str) -> Set[str]:
    """生成单词的各种变形，包括复数、动词时态、名词化等"""
    variants = {word}
    
    # ==================== 名词复数变化 ====================
    # 已有的复数规则
    if word.endswith('y') and len(word) > 2 and word[-2] not in 'aeiou':
        variants.add(word[:-1] + 'ies')  # policy → policies
    elif word.endswith(('s', 'x', 'z', 'ch', 'sh')):
        variants.add(word + 'es')  # glass → glasses
    elif word.endswith('f'):
        variants.add(word[:-1] + 'ves')  # leaf → leaves
    elif word.endswith('fe'):
        variants.add(word[:-2] + 'ves')  # life → lives
    else:
        variants.add(word + 's')  # bank → banks
    
    # 单数化（从复数推导单数）
    if word.endswith('ies') and len(word) > 3:
        variants.add(word[:-3] + 'y')  # policies → policy
    elif word.endswith('ves'):
        variants.add(word[:-3] + 'f')  # leaves → leaf
        variants.add(word[:-3] + 'fe')  # lives → life
    elif word.endswith('es') and len(word) > 2:
        variants.add(word[:-2])  # glasses → glass
        if not word[:-2].endswith(('s', 'x', 'z')):
            variants.add(word[:-1])  # games → game
    elif word.endswith('s') and len(word) > 1:
        variants.add(word[:-1])  # banks → bank
    
    # ==================== 动词时态变化 ====================
    # -ing 形式
    if word.endswith('e') and len(word) > 2:
        variants.add(word[:-1] + 'ing')  # invest → investing, finance → financing
    elif word.endswith(('t', 'n', 'p', 'g', 'm')) and len(word) > 2:
        # 双写末尾辅音字母
        if word[-2] in 'aeiou' and word[-3] not in 'aeiou':
            variants.add(word + word[-1] + 'ing')  # run → running, plan → planning
    variants.add(word + 'ing')  # bank → banking, invest → investing
    
    # -ed 形式
    if word.endswith('e') and len(word) > 2:
        variants.add(word + 'd')  # finance → financed
    elif word.endswith(('t', 'n', 'p', 'g', 'm')) and len(word) > 2:
        if word[-2] in 'aeiou' and word[-3] not in 'aeiou':
            variants.add(word + word[-1] + 'ed')  # plan → planned
    variants.add(word + 'ed')  # invest → invested, bank → banked
    
    # 第三人称单数（动词）
    if word.endswith(('s', 'x', 'z', 'ch', 'sh')):
        variants.add(word + 'es')  # reach → reaches
    elif word.endswith('y') and len(word) > 1 and word[-2] not in 'aeiou':
        variants.add(word[:-1] + 'ies')  # study → studies
    else:
        variants.add(word + 's')  # invest → invests
    
    # ==================== 名词化 ====================
    # -ment 名词
    if word.endswith('e'):
        variants.add(word[:-1] + 'ment')  # finance → financement (虽然不常用)
    variants.add(word + 'ment')  # invest → investment, develop → development
    
    # -tion/-ation 名词
    if word.endswith('e'):
        variants.add(word[:-1] + 'ation')  # operate → operation
        variants.add(word[:-1] + 'ion')  # finance → financement
    variants.add(word + 'ation')  # invest → investation (虽然不是标准词)
    
    # -er/-or 名词（执行者）
    if word.endswith('e'):
        variants.add(word + 'r')  # finance → financer
    variants.add(word + 'er')  # bank → banker, invest → invester
    variants.add(word + 'or')  # invest → investor
    
    # -ness 名词（特质）
    variants.add(word + 'ness')  # aware → awareness
    
    # ==================== 逆向推导：从变形推导原形 ====================
    # 从 -ing 推导原形
    if word.endswith('ing') and len(word) > 3:
        base = word[:-3]
        variants.add(base)  # banking → bank
        if base.endswith(base[-1]) and base[-1] in 'tnpgm':
            variants.add(base[:-1])  # running → run
        variants.add(base + 'e')  # financing → finance
    
    # 从 -ed 推导原形
    if word.endswith('ed') and len(word) > 2:
        base = word[:-2]
        variants.add(base)  # invested → invest
        if base.endswith(base[-1]) and base[-1] in 'tnpgm':
            variants.add(base[:-1])  # planned → plan
        variants.add(base[:-1])  # financed → finance
    
    # 从 -ment 推导原形
    if word.endswith('ment') and len(word) > 4:
        variants.add(word[:-4])  # investment → invest
        variants.add(word[:-4] + 'e')  # engagement → engage
    
    # 从 -tion/-ation 推导原形
    if word.endswith('ation') and len(word) > 5:
        variants.add(word[:-5])  # operation → operate
        variants.add(word[:-5] + 'e')  # organization → organize
    elif word.endswith('tion') and len(word) > 4:
        variants.add(word[:-3] + 'e')  # creation → create
    
    # 从 -er/-or 推导原形
    if word.endswith('er') and len(word) > 2:
        variants.add(word[:-2])  # banker → bank, investor → invest
        variants.add(word[:-1])  # financer → finance
    elif word.endswith('or') and len(word) > 2:
        variants.add(word[:-2])  # investor → invest
    
    # ==================== 特殊规则和清理 ====================
    # 移除明显不合理的变体（太短的词）
    variants = {v for v in variants if len(v) >= 2}
    
    # 移除重复的变体
    return variants

def parse_keyword_query(query: str) -> dict:
    query = query.strip()
    
    # 检查是否包含 AND 或 OR 运算符
    has_and = re.search(r'\band\b', query, re.IGNORECASE)
    has_or = re.search(r'\bor\b', query, re.IGNORECASE)
    
    if has_and:
        operator = 'AND'
        keywords = re.split(r'\band\b', query, flags=re.IGNORECASE)
    elif has_or:
        operator = 'OR'
        keywords = re.split(r'\bor\b', query, flags=re.IGNORECASE)
    else:
        # 如果没有 AND/OR，把整个查询当作一个短语
        operator = 'PHRASE'
        keywords = [query]
    
    # 清理关键词
    keywords = [normalize_keyword(kw) for kw in keywords if kw.strip()]
    return {'operator': operator, 'keywords': keywords}

def search_papers_by_keywords(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame()
    parsed = parse_keyword_query(query)
    operator = parsed['operator']
    keywords = parsed['keywords']
    if not keywords:
        return pd.DataFrame()
    
    all_variants = []
    keyword_info = []
    for keyword in keywords:
        # 检查是否是短语（包含空格）
        if ' ' in keyword:
            # 短语不生成变体，直接使用
            variants = {keyword}
            keyword_info.append(f'"{keyword}" (phrase)')
        else:
            # 单个词生成变体
            variants = generate_word_variants(keyword)
            keyword_info.append(f"{keyword} ({', '.join(sorted(variants))})")
        all_variants.append(variants)
    
    def text_contains_variants(text, variants):
        if pd.isna(text):
            return False
        text_lower = str(text).lower()
        for variant in variants:
            # 对于包含空格的短语，使用更灵活的匹配
            if ' ' in variant:
                # 短语匹配，允许标点符号
                pattern = r'\b' + re.escape(variant).replace(r'\ ', r'\s+') + r'\b'
            else:
                # 单词匹配
                pattern = r'\b' + re.escape(variant) + r'\b'
            if re.search(pattern, text_lower):
                return True
        return False
    
    title_col = None
    abstract_col = None
    for col in df.columns:
        col_stripped = col.strip().lower()
        if col_stripped == 'title':
            title_col = col
        elif col_stripped == 'abstract':
            abstract_col = col
    
    if title_col is None:
        st.error("❌ 'Title' column not found")
        return pd.DataFrame()
    
    if operator == 'AND' or operator == 'PHRASE':
        # AND 或 PHRASE: 所有关键词/短语都必须匹配
        mask = pd.Series([True] * len(df), index=df.index)
        for variants in all_variants:
            keyword_mask = df[title_col].apply(lambda x: text_contains_variants(x, variants))
            if abstract_col:
                keyword_mask |= df[abstract_col].apply(lambda x: text_contains_variants(x, variants))
            mask &= keyword_mask
    else:
        # OR: 任一关键词匹配即可
        mask = pd.Series([False] * len(df), index=df.index)
        for variants in all_variants:
            keyword_mask = df[title_col].apply(lambda x: text_contains_variants(x, variants))
            if abstract_col:
                keyword_mask |= df[abstract_col].apply(lambda x: text_contains_variants(x, variants))
            mask |= keyword_mask
    
    result_df = df[mask].copy()
    st.session_state['keyword_search_info'] = {'query': query, 'operator': operator, 'keywords': keyword_info, 'result_count': len(result_df)}
    return result_df

@st.cache_data
def load_reference_regions_data():
    try:
        if os.path.exists("all reference with regions.csv"):
            df = pd.read_csv("all reference with regions.csv")
            df['Title_normalized'] = df['Title'].str.strip().str.lower()
            return df
        else:
            st.warning("⚠️ 'all reference with regions.csv' not found")
            return None
    except Exception as e:
        st.warning(f"⚠️ Could not load file: {str(e)}")
        return None

def display_disclaimer():
    st.markdown("""<div class="disclaimer"><strong>⚠️ Disclaimer</strong><br>
    • Numbers are approximate and for reference only. Actual citations may be slightly higher.<br>
    • Data includes papers indexed in Scopus up to September 2025, excluding various reports.<br>
    • For questions, please contact: <a href="mailto:fan.su@un.org">fan.su@un.org</a></div>""", unsafe_allow_html=True)

def get_column_value(row, possible_names, default='N/A'):
    for name in possible_names:
        if name in row.index:
            val = row[name]
            return val if pd.notna(val) else default
        for col in row.index:
            if col.strip() == name.strip():
                val = row[col]
                return val if pd.notna(val) else default
    return default

def enrich_matches_with_regions_data(matches, regions_df):
    if regions_df is None or regions_df.empty:
        enriched_matches = []
        for match in matches:
            enriched_match = match.copy()
            for key in ['first_author', 'year', 'source_title', 'doi', 'cited_by', 'country']:
                enriched_match[key] = 'N/A'
            enriched_matches.append(enriched_match)
        return enriched_matches
    enriched_matches = []
    for match in matches:
        citing_title_normalized = match['citing_paper'].strip().lower()
        matching_rows = regions_df[regions_df['Title_normalized'] == citing_title_normalized]
        if not matching_rows.empty:
            row = matching_rows.iloc[0]
            enriched_match = match.copy()
            enriched_match['first_author'] = get_column_value(row, ['First author', 'First author ', 'Authors'])
            enriched_match['year'] = get_column_value(row, ['Year', 'Year '])
            enriched_match['source_title'] = get_column_value(row, ['Source title', 'Source title ', 'Source'])
            enriched_match['doi'] = get_column_value(row, ['DOI', 'DOI ', 'doi'])
            enriched_match['cited_by'] = get_column_value(row, ['Cited by', 'Cited by ', 'Citations'])
            enriched_match['country'] = get_column_value(row, ['Country (First Author)', 'Country (First Author) ', 'Country'])
        else:
            enriched_match = match.copy()
            for key in ['first_author', 'year', 'source_title', 'doi', 'cited_by', 'country']:
                enriched_match[key] = 'N/A'
        enriched_matches.append(enriched_match)
    return enriched_matches

def display_search_results(result, regions_df=None):
    st.markdown("---")
    exact_citations = sum(1 for m in result['matches'] if m['similarity_score'] == 100.0)
    potential_similar = result['citation_count'] - exact_citations
    total_possible = result['citation_count']
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("✅ Exact Citation", exact_citations, help="Citations with 100% similarity score")
    with col2:
        st.metric("🔍 Potential Similar", potential_similar, help="Citations with similarity score < 100%")
    with col3:
        st.metric("📊 Total Citations", total_possible, help="Total citations found as of September 2025")
    if result['matches']:
        st.markdown("### 📋 Citing Papers")
        enriched_matches = enrich_matches_with_regions_data(result['matches'], regions_df) if regions_df is not None else result['matches']
        matches_df = pd.DataFrame([{
            'No.': i + 1,
            'Citing Paper Title': m['citing_paper'][:100] + '...' if len(m['citing_paper']) > 100 else m['citing_paper'],
            'First Author': m.get('first_author', 'N/A'),
            'Year': m.get('year', 'N/A'),
            'Source Title': m.get('source_title', 'N/A'),
            'DOI': m.get('doi', 'N/A'),
            'Cited By': m.get('cited_by', 'N/A'),
            'Country': m.get('country', 'N/A'),
            'Reference Text': m['reference_text'][:150] + '...' if len(m['reference_text']) > 150 else m['reference_text'],
            'Similarity': f"{m['similarity_score']:.1f}%",
            'Match Method': m['match_method']
        } for i, m in enumerate(enriched_matches)])
        st.dataframe(matches_df, use_container_width=True, height=400)
        csv = matches_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button("📥 Download Citation List (CSV)", data=csv, file_name=f"citations_{result['report_title'][:30]}.csv", mime="text/csv")
        if result['match_methods']:
            st.markdown("### 📊 Match Method Distribution")
            method_df = pd.DataFrame([{'Match Method': k, 'Count': v} for k, v in result['match_methods'].items()])
            method_labels = {'exact_substring': 'Exact Match', 'fuzzy_match': 'Fuzzy Match', 'word_overlap': 'Word Overlap'}
            method_df['Match Method'] = method_df['Match Method'].map(method_labels)
            fig = px.bar(method_df, x='Match Method', y='Count', title='Citation Count by Match Method', color='Match Method',
                        color_discrete_sequence=['#009edb', '#56c02b', '#f9c642'])
            fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family="Arial, sans-serif"))
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No citations found for this report in the selected database")
    display_disclaimer()

def display_keyword_filter_info():
    if 'filtered_regions_df' in st.session_state and st.session_state['filtered_regions_df'] is not None:
        info = st.session_state.get('keyword_search_info', {})
        operator_display = info.get('operator', 'N/A')
        if operator_display == 'PHRASE':
            operator_display = 'PHRASE (exact phrase search)'
        st.markdown(f"""<div class="filter-active">
        <strong>🔍 Keyword Filter Active</strong><br>
        <strong>Search Query:</strong> {info.get('query', 'N/A')}<br>
        <strong>Search Type:</strong> {operator_display}<br>
        <strong>Keywords & Variants:</strong> {'; '.join(info.get('keywords', []))}<br>
        <strong>Filtered Papers:</strong> {info.get('result_count', 0):,} papers<br>
        <em>You can choose to limit citation search to these filtered papers below.</em></div>""", unsafe_allow_html=True)

def main():
    if 'filtered_regions_df' not in st.session_state:
        st.session_state['filtered_regions_df'] = None
    if 'keyword_query' not in st.session_state:
        st.session_state['keyword_query'] = ''
    
    # Header
    st.markdown('<h1 class="main-header">🌍 UNEP FI Report Citation Search</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Analyze academic citations of UNEP FI reports in Scopus-indexed literature</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    regions_df = load_reference_regions_data()
    
    with st.sidebar:
        st.header("📁 Data Configuration")
        import glob
        default_scopus = "Complete_References_Scopus_FULL.csv"
        default_unep = "UNEP FI Reports Title.csv"
        
        def find_file(filename):
            if os.path.exists(filename):
                return True
            if os.path.exists(os.path.join(os.getcwd(), filename)):
                return True
            pattern = filename.replace(' ', '*')
            matches = glob.glob(pattern) or glob.glob(f'*/{pattern}')
            return len(matches) > 0
        
        has_default_scopus = find_file(default_scopus)
        has_default_unep = find_file(default_unep)
        
        st.subheader("1️⃣ Scopus Citation Data")
        if has_default_scopus:
            use_default_scopus = st.checkbox("Use pre-loaded Scopus data", value=True)
            if use_default_scopus:
                scopus_file = default_scopus
                st.success("✅ Using pre-loaded data")
            else:
                scopus_file = st.file_uploader("Upload Scopus data (CSV)", type=['csv'], key="scopus_upload")
        else:
            scopus_file = st.file_uploader("Upload Scopus data (CSV)", type=['csv'], key="scopus_upload_2")
        
        st.markdown("---")
        st.subheader("2️⃣ Report List")
        report_list_option = st.radio("Choose source:", ["📤 Upload my own report list", "📋 Use pre-loaded UNEP FI list"])
        
        if report_list_option == "📤 Upload my own report list":
            unep_file = st.file_uploader("Upload report list (CSV)", type=['csv'], key="report_upload")
        else:
            if has_default_unep:
                unep_file = default_unep
                st.success("✅ Using pre-loaded list")
            else:
                st.warning("⚠️ Pre-loaded list not found")
                unep_file = st.file_uploader("Upload report list (CSV)", type=['csv'], key="fallback_reports")
        
        st.markdown("---")
        st.subheader("⚙️ Search Parameters")
        threshold = st.slider("Similarity Threshold", min_value=70, max_value=100, value=85, step=5,
                            help="Minimum similarity score for matching citations (higher = stricter)")
        
        st.markdown("---")
        st.markdown("### 📖 About")
        st.markdown("""
        This tool helps analyze how UNEP FI reports are cited in academic literature.
        
        **Features:**
        - Smart word variants (invest→investment)
        - Phrase & keyword filtering
        - Flexible database selection
        - Single & batch report analysis
        - Export results to CSV
        
        **Search Examples:**
        - `banking` - finds bank, banks, banking, banker
        - `climate risk` - exact phrase search
        - `ocean AND finance` - both required
        """)
    
    if scopus_file is None or unep_file is None:
        st.warning("⚠️ Please configure data files in the sidebar to begin")
        st.info("""
        ### Getting Started
        
        1. **Load Data**: Configure Scopus citation data and report list in the sidebar
        2. **Filter Papers** (Optional): Use Keywords Search to narrow down papers by topic
        3. **Select Database**: Choose to search in all papers or filtered papers only
        4. **Search Citations**: Analyze single reports or batch process multiple reports
        5. **Export Results**: Download detailed citation data as CSV files
        """)
        return
    
    try:
        with st.spinner("Loading data files..."):
            if isinstance(scopus_file, str):
                scopus_df = pd.read_csv(scopus_file)
            else:
                scopus_df = pd.read_csv(scopus_file)
            if isinstance(unep_file, str):
                unep_titles = pd.read_csv(unep_file).iloc[:, 0].dropna().tolist()
                list_source = "pre-loaded UNEP FI list"
            else:
                unep_titles = pd.read_csv(unep_file).iloc[:, 0].dropna().tolist()
                list_source = "your custom list"
        st.success(f"✅ Data loaded successfully | Scopus: {len(scopus_df):,} citations | Reports: {len(unep_titles)} from {list_source}")
    except Exception as e:
        st.error(f"❌ Data loading failed: {str(e)}")
        return
    
    st.markdown("---")
    st.markdown("### 🔍 Keywords Search (Optional)")
    st.markdown("""<div class="keyword-search-box">
    <strong>Filter papers by keywords before searching citations</strong><br>
    <span style="font-size: 0.95rem;">Search within Title and Abstract fields with intelligent matching</span>
    <ul style="margin-top: 12px; margin-bottom: 0; padding-left: 20px; list-style-type: disc;">
        <li style="margin-bottom: 6px;"><strong>Phrase search:</strong> <code>climate risk</code> searches for the exact phrase</li>
        <li style="margin-bottom: 6px;"><strong>AND logic:</strong> <code>climate AND risk</code> requires both words (anywhere)</li>
        <li style="margin-bottom: 6px;"><strong>OR logic:</strong> <code>ocean OR sea</code> matches any keyword</li>
        <li style="margin-bottom: 6px;"><strong>Smart variants:</strong> <code>bank</code> → bank, banks, banking, banked, banker</li>
        <li style="margin-bottom: 6px;"><strong>Smart variants:</strong> <code>invest</code> → invest, invested, investing, investment, investor</li>
        <li style="margin-bottom: 0;"><strong>Tip:</strong> Use AND/OR only when you want to split terms; otherwise keep as phrase</li>
    </ul>
    </div>""", unsafe_allow_html=True)
    
    if regions_df is not None and not regions_df.empty:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            keyword_input = st.text_input("Enter keywords", value=st.session_state.get('keyword_query', ''),
                                         placeholder='e.g., "climate risk" or "ocean AND finance"', key='keyword_input')
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            apply_filter_button = st.button("🔍 Apply Filter", type="primary", use_container_width=True)
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            reset_filter_button = st.button("🔄 Reset Filter", use_container_width=True)
        
        if apply_filter_button and keyword_input.strip():
            with st.spinner("Filtering papers by keywords..."):
                try:
                    filtered_df = search_papers_by_keywords(regions_df, keyword_input)
                    st.session_state['filtered_regions_df'] = filtered_df
                    st.session_state['keyword_query'] = keyword_input
                    if not filtered_df.empty:
                        st.success(f"✅ Found {len(filtered_df):,} papers matching your keywords")
                        
                        # 显示筛选结果预览
                        with st.expander("📋 View Filtered Papers (Preview - First 100 of {0:,} total)".format(len(filtered_df)), expanded=True):
                            st.markdown(f"**Total papers found:** {len(filtered_df):,}")
                            st.markdown("**Showing preview of first 100 papers** (download CSV for complete list)")
                            st.markdown("---")
                            
                            preview_df = filtered_df.head(100).copy()
                            display_cols = []
                            col_name_mapping = {
                                'Title': 'Title',
                                'First author': 'First Author', 
                                'Year': 'Year',
                                'Source title': 'Source Title',
                                'DOI': 'DOI',
                                'Cited by': 'Cited By',
                                'Country (First Author)': 'Country'
                            }
                            
                            for col_name in col_name_mapping.keys():
                                for col in preview_df.columns:
                                    if col.strip().lower() == col_name.lower():
                                        display_cols.append(col)
                                        break
                            
                            if display_cols:
                                display_df = preview_df[display_cols].copy()
                                # 重命名列以保证一致性
                                rename_dict = {}
                                for col in display_cols:
                                    for original, new_name in col_name_mapping.items():
                                        if col.strip().lower() == original.lower():
                                            rename_dict[col] = new_name
                                            break
                                display_df = display_df.rename(columns=rename_dict)
                                display_df.insert(0, 'No.', range(1, len(display_df) + 1))
                                
                                st.dataframe(display_df, use_container_width=True, height=500)
                                
                                st.markdown("---")
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("📄 Papers in Preview", len(display_df))
                                with col2:
                                    st.metric("📊 Total Filtered Papers", len(filtered_df))
                                
                                # 下载完整列表
                                full_download_df = filtered_df[display_cols].copy()
                                full_download_df = full_download_df.rename(columns=rename_dict)
                                full_download_df.insert(0, 'No.', range(1, len(full_download_df) + 1))
                                
                                st.download_button(
                                    "📥 Download Complete Filtered Papers List (CSV)",
                                    data=full_download_df.to_csv(index=False, encoding='utf-8-sig'),
                                    file_name=f"filtered_papers_{len(filtered_df)}_papers.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
                            else:
                                st.warning("⚠️ Could not find expected columns in the data")
                    else:
                        st.warning("⚠️ No papers found matching your keywords. Please try different search terms.")
                        st.session_state['filtered_regions_df'] = None
                except Exception as e:
                    st.error(f"❌ Keyword search error: {str(e)}")
        
        if reset_filter_button:
            st.session_state['filtered_regions_df'] = None
            st.session_state['keyword_query'] = ''
            st.session_state['keyword_search_info'] = {}
            st.success("✅ Filter reset successfully")
            st.rerun()
        
        if st.session_state['filtered_regions_df'] is not None:
            display_keyword_filter_info()
    else:
        st.info("ℹ️ 'all reference with regions.csv' not found. Keywords Search feature is unavailable.")
    
    st.markdown("---")
    
    # Database Selection
    st.markdown("### 📊 Citation Database Selection")
    st.markdown("""<div class="database-selection">
    <strong>Choose the scope of your citation search</strong>
    Select whether to search citations across all available papers or limit to your filtered keyword results.
    </div>""", unsafe_allow_html=True)
    
    active_regions_df = st.session_state.get('filtered_regions_df', regions_df)
    has_filtered_data = st.session_state.get('filtered_regions_df') is not None
    
    if has_filtered_data:
        filtered_count = len(st.session_state['filtered_regions_df'])
        total_count = len(regions_df) if regions_df is not None else 0
        
        database_option = st.radio(
            "**Select citation database:**",
            [
                f"📚 Full Database ({total_count:,} papers - all papers pre-loaded up to 2025.9)",
                f"🔍 Filtered Database ({filtered_count:,} papers - from Keywords Search results)"
            ],
            help="This determines which papers will be searched for citations to your selected reports",
            key="database_selection"
        )
        
        if "Filtered Database" in database_option:
            filtered_titles = set(st.session_state['filtered_regions_df']['Title_normalized'].unique())
            scopus_title_col = None
            for col in scopus_df.columns:
                if col.strip().lower() == 'title':
                    scopus_title_col = col
                    break
            if scopus_title_col:
                active_scopus_df = scopus_df[scopus_df[scopus_title_col].str.strip().str.lower().isin(filtered_titles)].copy()
                st.success(f"✅ **Filtered Database Selected**: Citation search limited to {filtered_count:,} filtered papers")
                st.info(f"ℹ️ Citations will only be counted if they appear in these {filtered_count:,} filtered papers. This allows for domain-specific impact analysis.")
            else:
                st.error("❌ Could not locate 'Title' column in Scopus data. Defaulting to full database.")
                active_scopus_df = scopus_df
        else:
            active_scopus_df = scopus_df
            st.success(f"✅ **Full Database Selected**: Searching across all {total_count:,} available papers")
    else:
        st.info("ℹ️ **Full database mode**: No keyword filter applied. Use Keywords Search above to enable filtered database option.")
        active_scopus_df = scopus_df
    
    st.markdown("---")
    
    search_mode = st.radio("**Search Mode**", ["🔍 Single Report Search", "📊 Batch Report Search"], horizontal=True)
    
    if search_mode == "🔍 Single Report Search":
        st.markdown("### 🔍 Single Report Search")
        col1, col2 = st.columns([3, 1])
        with col1:
            report_title = st.selectbox("Select report from list", options=[""] + unep_titles,
                                       help="Choose a report from the pre-loaded list")
            manual_input = st.text_input("Or enter report title manually", placeholder="Type report name...")
            if manual_input:
                report_title = manual_input
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            search_button = st.button("🚀 Search Citations", type="primary", use_container_width=True)
        
        if search_button and report_title:
            with st.spinner(f"Searching citations for '{report_title[:50]}...'"):
                try:
                    result = search_single_report(report_title, active_scopus_df, threshold)
                    display_search_results(result, active_regions_df)
                except Exception as e:
                    st.error(f"❌ Search error: {str(e)}")
        elif search_button and not report_title:
            st.warning("⚠️ Please select or enter a report title")
    
    else:
        st.markdown("### 📊 Batch Report Search")
        selected_reports = st.multiselect("Select multiple reports for batch analysis", options=unep_titles,
                                         help="You can select multiple reports to analyze simultaneously")
        col1, col2 = st.columns([1, 4])
        with col1:
            batch_search_button = st.button("🚀 Start Batch Search", type="primary", use_container_width=True)
        
        if batch_search_button and selected_reports:
            progress_bar = st.progress(0)
            status_text = st.empty()
            results = []
            
            def progress_callback(current, total, result):
                progress = current / total
                progress_bar.progress(progress)
                status_text.text(f"Processing: {current}/{total} - {result['report_title'][:50]}...")
            
            try:
                with st.spinner("Running batch search..."):
                    results = search_multiple_reports(selected_reports, active_scopus_df, threshold, progress_callback)
                progress_bar.empty()
                status_text.empty()
                
                st.markdown("### 📊 Batch Search Results")
                summary_df = pd.DataFrame([{
                    'Report Name': r['report_title'][:60] + '...' if len(r['report_title']) > 60 else r['report_title'],
                    'Exact Citations (100% Similarity)': sum(1 for m in r['matches'] if m['similarity_score'] == 100.0)
                } for r in results]).sort_values('Exact Citations (100% Similarity)', ascending=False)
                
                st.dataframe(summary_df, use_container_width=True)
                
                fig = px.bar(summary_df.head(20), x='Exact Citations (100% Similarity)', y='Report Name',
                           orientation='h', title='Top 20 Reports by Citation Count',
                           labels={'Exact Citations (100% Similarity)': 'Citation Count', 'Report Name': 'Report'},
                           color_discrete_sequence=['#009edb'])
                fig.update_layout(height=600, plot_bgcolor='white', paper_bgcolor='white',
                                font=dict(family="Arial, sans-serif"))
                st.plotly_chart(fig, use_container_width=True)
                
                csv = summary_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button("📥 Download Summary Report (CSV)", data=csv,
                                 file_name="batch_citation_summary.csv", mime="text/csv")
                display_disclaimer()
            except Exception as e:
                st.error(f"❌ Batch search error: {str(e)}")
        elif batch_search_button and not selected_reports:
            st.warning("⚠️ Please select at least one report for batch analysis")

if __name__ == "__main__":
    main()
