# 🎉 Major Update: Custom Report List Analysis!

## ✨ What's New (v2.0)

### 🆕 Feature: Upload Your Own Report Lists

**Previous Version:**
- ❌ Only analyzed pre-loaded UNEP FI reports
- ❌ Users couldn't analyze their own reports
- ❌ Limited to 500 fixed reports

**New Version:**
- ✅ **Upload ANY report list** you want to analyze
- ✅ Analyze your organization's reports
- ✅ Track competitor reports
- ✅ Flexible - use your own CSV file
- ✅ Still supports pre-loaded UNEP FI reports as option

---

## 🎯 Who Benefits?

### 1. Research Organizations
**Use Case:** Track impact of your published reports
- Upload list of your organization's reports
- See which are most cited in academia
- Demonstrate research impact for funding

### 2. Think Tanks & Policy Groups
**Use Case:** Monitor policy influence
- Track citations of your policy briefs
- Compare impact across different reports
- Identify high-impact publications

### 3. Consultancies & Advisory Firms
**Use Case:** Competitive intelligence
- List your reports + competitor reports
- See comparative citation metrics
- Identify market positioning

### 4. Academic Researchers
**Use Case:** Literature review & meta-analysis
- Upload list of key reports in your field
- Identify most influential publications
- Build comprehensive citation database

### 5. Corporate Sustainability Teams
**Use Case:** ESG reporting impact
- Track citations of your sustainability reports
- Measure thought leadership
- Support stakeholder communications

---

## 📖 How It Works

### Quick Start (5 minutes)

1. **Prepare Your CSV**
   ```csv
   Report Title
   Your Report Name 1
   Your Report Name 2
   Your Report Name 3
   ```

2. **Upload to App**
   - Open the web application
   - Select "Upload my own report list"
   - Upload your CSV file

3. **Analyze**
   - Search single reports OR
   - Batch analyze all reports
   - View results with charts

4. **Export**
   - Download detailed citation lists
   - Share with your team

### Example CSV Formats

**Minimal Format:**
```csv
Report Title
Annual Report 2023
Sustainability Guidelines
Climate Strategy
```

**With Additional Info (optional):**
```csv
Report Title,Year,Department,Lead Author
Annual Report 2023,2023,Corporate,Jane Doe
Sustainability Guidelines,2022,ESG,John Smith
Climate Strategy,2021,Policy,Alice Brown
```
*Note: Only first column (Report Title) is used for searching*

---

## 🔄 What Changed in the Interface

### Sidebar Configuration

**Before:**
```
📁 Data Configuration
  [ ] Use pre-loaded data files
  
  1️⃣ Scopus Data
  2️⃣ UNEP FI Report List
```

**After:**
```
📁 Data Configuration
  1️⃣ Scopus Citation Data
     [ ] Use pre-loaded Scopus data
  
  2️⃣ Report List to Analyze
     ( ) Upload my own report list  ← NEW!
     ( ) Use pre-loaded UNEP FI list
```

### New User Options

✅ **Option 1: Your Own Reports**
- Upload custom CSV
- Analyze any reports you want
- Perfect for tracking your own work

✅ **Option 2: UNEP FI Reports**
- Use pre-loaded list (500+ reports)
- Good for benchmarking
- Standard UNEP FI analysis

---

## 📊 Real-World Examples

### Example 1: Annual Report Analysis

**Scenario:** Your organization publishes 5 major reports per year. You want to track their academic impact over time.

**Solution:**
```csv
Report Title
2023 Sustainability Report
2023 Climate Action Plan
2023 Biodiversity Strategy
2023 ESG Framework
2023 Impact Assessment
```

**Result:** See which 2023 reports are already being cited, identify early successes.

---

### Example 2: Competitive Landscape

**Scenario:** You want to compare your reports vs. competitors in the same space.

**Solution:**
```csv
Report Title
Our Climate Report 2023
Competitor A Climate Study
Competitor B Sustainability Framework
Our Biodiversity Guidelines
Competitor A Nature Report
```

**Result:** Benchmark your citation impact against competitors.

---

### Example 3: Literature Review

**Scenario:** Researching "green finance" and want to see which foundation reports are most cited.

**Solution:**
```csv
Report Title
Green Bond Principles
Climate Bonds Taxonomy
EU Taxonomy for Sustainable Activities
Task Force on Climate-related Financial Disclosures
Principles for Responsible Investment
```

**Result:** Identify the most influential reports in your research area.

---

## 🎓 Advanced Features

### Flexible Analysis Modes

**Single Report Mode:**
- Quick lookup
- Detailed citation list
- Fast results

**Batch Mode:**
- Analyze 10-50 reports at once
- Comparative charts
- Summary statistics
- Bulk export

### Smart Matching

Three matching algorithms work together:
- **Exact Match** - 100% accuracy
- **Fuzzy Match** - Handles typos/variations
- **Word Overlap** - Catches different phrasings

Adjustable threshold (70-100%) for precision control.

---

## 📋 File Requirements

### Your Custom Report List CSV

**Required:**
- UTF-8 encoding
- First column = Report titles
- One report per row

**Optional:**
- Additional columns for your reference
- Column headers (any names)
- Notes/metadata columns

**Size Limits:**
- No practical limit on number of reports
- Recommended: 1-100 reports per analysis
- For 100+ reports, consider batching

### Scopus Citation Data

**If using pre-loaded data:**
- ✅ No action needed (33MB, 116K citations)

**If uploading your own:**
- Must contain `Title` column
- Must contain `Reference` column
- CSV format, UTF-8 encoding

---

## 🚀 Getting Started

### Step 1: Download Example File

Download the example CSV to see the format:
- [example_report_list.csv](example_report_list.csv)

### Step 2: Create Your List

Edit the example or create your own:
- Replace with your report titles
- Save as CSV (UTF-8)

### Step 3: Use the App

Open: `https://your-app.streamlit.app`
- Select "Upload my own report list"
- Upload your CSV
- Start analyzing!

### Step 4: Read Detailed Guide

For comprehensive instructions:
- [USER_GUIDE_CUSTOM_REPORTS.md](USER_GUIDE_CUSTOM_REPORTS.md)

---

## 📊 Performance

**Testing Results:**

| Reports | Processing Time | Result Quality |
|---------|----------------|----------------|
| 1 report | 1-5 seconds | Excellent |
| 10 reports | 30-60 seconds | Excellent |
| 50 reports | 3-5 minutes | Very Good |
| 100 reports | 8-10 minutes | Good |

**Recommendations:**
- Single searches: Any number
- Batch searches: 20-50 reports optimal
- Large lists (100+): Process in batches

---

## ⚠️ Important Notes

### Data Privacy
- **Your uploaded CSV is NOT stored**
- Data exists only during your session
- When you close the browser, data is deleted
- Safe for analyzing confidential report lists

### Citation Coverage
- Based on Scopus database (as of Sept 2025)
- Only includes academic papers (not reports citing reports)
- Numbers are approximate (see disclaimer)
- Best for tracking academic impact

### Matching Accuracy
- High-quality matches: 90%+
- Some false positives possible at lower thresholds
- Always review sample results
- Adjust threshold as needed

---

## 🆚 Comparison: v1.0 vs v2.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Report Lists | Fixed (UNEP FI only) | ✅ Custom + UNEP FI |
| Flexibility | Limited | ✅ Highly flexible |
| Use Cases | UNEP FI analysis | ✅ Universal |
| User Control | Low | ✅ Full control |
| Data Upload | Scopus only | ✅ Scopus + Reports |
| Batch Analysis | Yes | ✅ Enhanced |

---

## 📞 Support & Resources

### Documentation
- **USER_GUIDE_CUSTOM_REPORTS.md** - Detailed user guide
- **example_report_list.csv** - Template file
- **DEPLOYMENT_STEPS.md** - Deployment guide

### Help
- **Email:** fan.su@un.org
- **Issues:** Report bugs via email
- **Feedback:** Suggestions welcome!

---

## 🎯 Next Steps

1. **Download** [example_report_list.csv](example_report_list.csv)
2. **Edit** with your report titles
3. **Upload** to the application
4. **Analyze** and download results
5. **Share** insights with your team!

---

## 🎉 Summary

This update transforms the tool from a **single-purpose UNEP FI analyzer** into a **universal report citation tracking system**.

**Now you can:**
- ✅ Analyze ANY reports (not just UNEP FI)
- ✅ Track YOUR organization's impact
- ✅ Compare multiple report portfolios
- ✅ Flexible CSV upload format
- ✅ Still use UNEP FI list if needed

**Perfect for:**
- Research organizations
- Think tanks
- Consultancies
- Academic researchers
- Corporate sustainability teams

---

**Ready to analyze your reports? Let's go!** 🚀

*Version 2.0 | Last Updated: November 2025*
