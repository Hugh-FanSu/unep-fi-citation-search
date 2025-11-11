"""
UNEP FI Report Citation Search System
Web Application with Streamlit
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

# Page configuration
st.set_page_config(
    page_title="UNEP FI Citation Search",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .disclaimer {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #6c757d;
        margin-top: 2rem;
        font-size: 0.9rem;
        color: #6c757d;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_scopus_data(file_path):
    """Load Scopus data (with cache)"""
    return load_data_with_encoding(file_path)


@st.cache_data
def load_unep_titles(file_path):
    """Load UNEP FI report titles list (with cache)"""
    df = load_data_with_encoding(file_path)
    # Assume titles are in the first column
    titles = df.iloc[:, 0].dropna().tolist()
    return titles


@st.cache_data
def load_reference_regions_data():
    """Load all reference with regions.csv file (with cache)"""
    try:
        if os.path.exists("all reference with regions.csv"):
            df = pd.read_csv("all reference with regions.csv")
            # Normalize the title column for matching
            df['Title_normalized'] = df['Title'].str.strip().str.lower()
            return df
        else:
            st.warning("⚠️ 'all reference with regions.csv' not found. Additional citation details will not be available.")
            return None
    except Exception as e:
        st.warning(f"⚠️ Could not load 'all reference with regions.csv': {str(e)}")
        return None


def display_disclaimer():
    """Display disclaimer at the bottom of results"""
    st.markdown("""
        <div class="disclaimer">
        <strong>⚠️ Disclaimer:</strong><br>
        • Numbers are approximate and for reference only. Actual citations may be slightly higher.<br>
        • Only includes papers indexed in Scopus as of September 2025, excluding various reports.<br>
        • For questions, please contact: <a href="mailto:fan.su@un.org">fan.su@un.org</a>
        </div>
    """, unsafe_allow_html=True)


def enrich_matches_with_regions_data(matches, regions_df):
    """
    Enrich match data with information from all reference with regions.csv
    
    Args:
        matches: List of match dictionaries
        regions_df: DataFrame from all reference with regions.csv
    
    Returns:
        List of enriched match dictionaries
    """
    if regions_df is None:
        return matches
    
    enriched_matches = []
    
    for match in matches:
        # Normalize the citing paper title for matching
        citing_title_normalized = match['citing_paper'].strip().lower()
        
        # Try to find matching row in regions_df
        matching_rows = regions_df[regions_df['Title_normalized'] == citing_title_normalized]
        
        if not matching_rows.empty:
            # Get the first matching row
            row = matching_rows.iloc[0]
            
            # Add additional information
            enriched_match = match.copy()
            enriched_match['first_author'] = row.get('First author', 'N/A')
            enriched_match['year'] = row.get('Year', 'N/A')
            enriched_match['source_title'] = row.get('Source title', 'N/A')
            enriched_match['doi'] = row.get('DOI', 'N/A')
            enriched_match['cited_by'] = row.get('Cited by', 'N/A')
            enriched_match['country'] = row.get('Country (First Author)', 'N/A')
        else:
            # No match found, use N/A
            enriched_match = match.copy()
            enriched_match['first_author'] = 'N/A'
            enriched_match['year'] = 'N/A'
            enriched_match['source_title'] = 'N/A'
            enriched_match['doi'] = 'N/A'
            enriched_match['cited_by'] = 'N/A'
            enriched_match['country'] = 'N/A'
        
        enriched_matches.append(enriched_match)
    
    return enriched_matches


def display_search_results(result, regions_df=None):
    """Display search results"""
    st.markdown("---")
    
    # Calculate statistics
    exact_citations = sum(1 for m in result['matches'] if m['similarity_score'] == 100.0)
    potential_similar = result['citation_count'] - exact_citations
    total_possible = result['citation_count']  # Total as of Sept 2025
    
    # Display basic statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="✅ Exact Citation",
            value=exact_citations,
            help="Citations with 100% similarity score"
        )
    
    with col2:
        st.metric(
            label="🔍 Potential Similar Citation",
            value=potential_similar,
            help="Citations with similarity score < 100%"
        )
    
    with col3:
        st.metric(
            label="📊 Total Possible Citations (Sept 2025)",
            value=total_possible,
            help="Total citations found as of September 2025"
        )
    
    # Display citation list if available
    if result['matches']:
        st.markdown("### 📋 Citing Papers")
        
        # Enrich matches with regions data if available
        if regions_df is not None:
            enriched_matches = enrich_matches_with_regions_data(result['matches'], regions_df)
        else:
            enriched_matches = result['matches']
        
        # Create DataFrame
        matches_df = pd.DataFrame([
            {
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
            }
            for i, m in enumerate(enriched_matches)
        ])
        
        st.dataframe(
            matches_df,
            use_container_width=True,
            height=400
        )
        
        # Download option
        csv = matches_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Download Citation List (CSV)",
            data=csv,
            file_name=f"citations_{result['report_title'][:30]}.csv",
            mime="text/csv"
        )
        
        # Visualize match method distribution
        if result['match_methods']:
            st.markdown("### 📊 Match Method Distribution")
            method_df = pd.DataFrame([
                {'Match Method': k, 'Count': v}
                for k, v in result['match_methods'].items()
            ])
            
            method_labels = {
                'exact_substring': 'Exact Match',
                'fuzzy_match': 'Fuzzy Match',
                'word_overlap': 'Word Overlap'
            }
            method_df['Match Method'] = method_df['Match Method'].map(method_labels)
            
            fig = px.bar(
                method_df,
                x='Match Method',
                y='Count',
                title='Citation Count by Match Method',
                color='Match Method'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("😔 No citations found for this report")
    
    # Display disclaimer
    display_disclaimer()


def main():
    """Main function"""
    # Title
    st.markdown('<h1 class="main-header">📚 UNEP FI Report Citation Search</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Load regions data once at the start
    regions_df = load_reference_regions_data()
    
    # Sidebar - Data file settings
    with st.sidebar:
        st.header("📁 Data Configuration")
        
        # Check if default data files exist
        import os
        import glob
        
        # Try to find CSV files
        default_scopus = "Complete_References_Scopus_FULL.csv"
        default_unep = "UNEP FI Reports Title.csv"
        
        # Check in current directory and parent directory
        def find_file(filename):
            # Try current directory
            if os.path.exists(filename):
                return True
            # Try with explicit path
            if os.path.exists(os.path.join(os.getcwd(), filename)):
                return True
            # Try finding by glob pattern
            pattern = filename.replace(' ', '*')
            matches = glob.glob(pattern) or glob.glob(f'*/{pattern}')
            return len(matches) > 0
        
        has_default_scopus = find_file(default_scopus)
        has_default_unep = find_file(default_unep)
        
        # Scopus citation data
        st.subheader("1️⃣ Scopus Citation Data")
        
        if has_default_scopus:
            use_default_scopus = st.checkbox("Use pre-loaded Scopus data", value=True)
            if use_default_scopus:
                scopus_file = default_scopus
                st.success("✅ Using pre-loaded Scopus data")
            else:
                scopus_file = st.file_uploader(
                    "Upload your Scopus citation data (CSV)",
                    type=['csv'],
                    help="Must contain 'Title' and 'Reference' columns",
                    key="scopus_upload"
                )
        else:
            scopus_file = st.file_uploader(
                "Upload Scopus citation data (CSV)",
                type=['csv'],
                help="Must contain 'Title' and 'Reference' columns",
                key="scopus_upload_2"
            )
        
        st.markdown("---")
        
        # Report list
        st.subheader("2️⃣ Report List to Analyze")
        
        report_list_option = st.radio(
            "Choose report list source:",
            ["📤 Upload my own report list", "📋 Use pre-loaded UNEP FI list"],
            help="You can analyze your own list of reports or use the pre-loaded UNEP FI reports"
        )
        
        if report_list_option == "📤 Upload my own report list":
            unep_file = st.file_uploader(
                "Upload report list (CSV)",
                type=['csv'],
                help="First column should contain report titles",
                key="report_upload"
            )
        else:
            # Try to use pre-loaded UNEP FI list
            if has_default_unep:
                unep_file = default_unep
                st.success("✅ Using pre-loaded UNEP FI list")
            else:
                st.warning("⚠️ Pre-loaded UNEP FI list not found")
                unep_file = st.file_uploader(
                    "Upload report list (CSV) as fallback",
                    type=['csv'],
                    help="First column should contain report titles",
                    key="fallback_reports"
                )
        
        st.markdown("---")
        
        # Search parameters
        st.subheader("⚙️ Search Parameters")
        threshold = st.slider(
            "Similarity Threshold",
            min_value=70,
            max_value=100,
            value=85,
            step=5,
            help="Minimum similarity requirement for matching (higher = stricter)"
        )
        
        st.markdown("---")
        st.markdown("### 📖 How to Use")
        st.markdown("""
        **Option 1: Analyze Your Own Reports**
        1. Upload Scopus citation data (or use pre-loaded)
        2. Select "Upload my own report list"
        3. Upload CSV with your report titles
        4. Search individual or batch reports
        
        **Option 2: Use UNEP FI Reports**
        1. Select "Use pre-loaded UNEP FI list"
        2. Search from 500+ UNEP FI reports
        3. View citations and download results
        
        **CSV Format for Custom Lists:**
        ```
        Report Title
        Your Report Name 1
        Your Report Name 2
        Your Report Name 3
        ```
        """)
    
    # Main interface
    if scopus_file is None or unep_file is None:
        st.warning("⚠️ Please configure data files in the sidebar")
        st.info("""
        ### 🎯 System Features
        - 📊 **Analyze ANY report citations** - Upload your own report list or use UNEP FI reports
        - 🔍 **Single report search** - Quick lookup for individual reports
        - 📈 **Batch analysis** - Analyze multiple reports at once with statistics
        - 🎯 **Three matching methods** - Exact match, fuzzy match, and word overlap
        - 📥 **Export results** - Download detailed citation data as CSV
        - 📊 **Visualizations** - Interactive charts showing citation patterns
        
        ### 📋 How It Works
        
        **Step 1: Scopus Data**
        - Use pre-loaded data (33MB, 116K+ citations)
        - Or upload your own Scopus export
        - Must contain `Title` and `Reference` columns
        
        **Step 2: Your Report List**
        - **Option A:** Upload your own CSV with report titles
        - **Option B:** Use pre-loaded UNEP FI report list (500+ reports)
        
        **Step 3: Search & Analyze**
        - Search individual reports
        - Or batch analyze multiple reports
        - View results with disclaimer
        - Download CSV exports
        
        ### 📄 Custom Report List Format
        Your CSV should have report titles in the first column:
        ```
        Report Title
        Principles for Responsible Banking
        Climate Risk Assessment 2023
        Sustainable Finance Guidelines
        ...
        ```
        No other columns are required - just your report titles!
        """)
        return
    
    # Load data
    try:
        with st.spinner("📂 Loading data files..."):
            if isinstance(scopus_file, str):
                scopus_df = pd.read_csv(scopus_file)
            else:
                scopus_df = pd.read_csv(scopus_file)
            
            if isinstance(unep_file, str):
                unep_titles = pd.read_csv(unep_file).iloc[:, 0].dropna().tolist()
                list_source = "pre-loaded UNEP FI list"
            else:
                unep_titles = pd.read_csv(unep_file).iloc[:, 0].dropna().tolist()
                list_source = "your custom report list"
        
        st.success(f"✅ Data loaded successfully! Scopus: {len(scopus_df):,} citations | Reports: {len(unep_titles)} from {list_source}")
        
    except Exception as e:
        st.error(f"❌ Data loading failed: {str(e)}")
        return
    
    # Search mode selection
    st.markdown("---")
    search_mode = st.radio(
        "Select Search Mode",
        ["🔍 Single Report Search", "📊 Batch Report Search"],
        horizontal=True
    )
    
    if search_mode == "🔍 Single Report Search":
        # Single report search
        st.markdown("### 🔍 Single Report Search")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Report name input (with autocomplete)
            report_title = st.selectbox(
                "Select or enter report name",
                options=[""] + unep_titles,
                help="Select from list or enter report name directly"
            )
            
            # Manual input option
            manual_input = st.text_input(
                "Or enter report name manually",
                placeholder="Enter report name..."
            )
            
            if manual_input:
                report_title = manual_input
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            search_button = st.button("🚀 Search", type="primary", use_container_width=True)
        
        if search_button and report_title:
            with st.spinner(f"🔍 Searching citations for '{report_title[:50]}...'"):
                try:
                    result = search_single_report(report_title, scopus_df, threshold)
                    display_search_results(result, regions_df)
                except Exception as e:
                    st.error(f"❌ Search error: {str(e)}")
        
        elif search_button and not report_title:
            st.warning("⚠️ Please enter or select a report name")
    
    else:
        # Batch report search
        st.markdown("### 📊 Batch Report Search")
        
        selected_reports = st.multiselect(
            "Select reports to search (multiple selection)",
            options=unep_titles,
            help="You can select multiple reports for batch search"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            batch_search_button = st.button("🚀 Batch Search", type="primary", use_container_width=True)
        
        if batch_search_button and selected_reports:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            
            def progress_callback(current, total, result):
                progress = current / total
                progress_bar.progress(progress)
                status_text.text(f"Progress: {current}/{total} - Current: {result['report_title'][:50]}...")
            
            try:
                with st.spinner("🔍 Batch searching..."):
                    results = search_multiple_reports(
                        selected_reports,
                        scopus_df,
                        threshold,
                        progress_callback
                    )
                
                progress_bar.empty()
                status_text.empty()
                
                # Display summary results - only show 100% similarity citations
                st.markdown("### 📊 Batch Search Summary")
                
                summary_df = pd.DataFrame([
                    {
                        'Report Name': r['report_title'][:60] + '...' if len(r['report_title']) > 60 else r['report_title'],
                        'Exact Citations (100% Similarity)': sum(1 for m in r['matches'] if m['similarity_score'] == 100.0)
                    }
                    for r in results
                ]).sort_values('Exact Citations (100% Similarity)', ascending=False)
                
                st.dataframe(summary_df, use_container_width=True)
                
                # Visualization
                fig = px.bar(
                    summary_df.head(20),
                    x='Exact Citations (100% Similarity)',
                    y='Report Name',
                    orientation='h',
                    title='Top 20 Reports by Exact Citations (100% Similarity)',
                    labels={'Exact Citations (100% Similarity)': 'Exact Citations', 'Report Name': 'Report Name'}
                )
                fig.update_layout(height=600)
                st.plotly_chart(fig, use_container_width=True)
                
                # Download summary results
                csv = summary_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 Download Summary (CSV)",
                    data=csv,
                    file_name="batch_citation_summary.csv",
                    mime="text/csv"
                )
                
                # Display disclaimer
                display_disclaimer()
                
            except Exception as e:
                st.error(f"❌ Batch search error: {str(e)}")
        
        elif batch_search_button and not selected_reports:
            st.warning("⚠️ Please select reports to search")


if __name__ == "__main__":
    main()
