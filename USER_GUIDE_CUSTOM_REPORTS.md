# 📖 User Guide: Analyzing Your Own Reports

## 🎯 Overview

This system now supports **two modes**:

1. **Analyze Your Own Reports** - Upload a CSV with your report titles
2. **Use UNEP FI Reports** - Search from pre-loaded 500+ UNEP FI reports

---

## 📤 How to Analyze Your Own Reports

### Step 1: Prepare Your Report List

Create a CSV file with your report titles. Only one column is needed:

**Example (example_report_list.csv):**
```csv
Report Title
Principles for Responsible Banking
Climate Risk Assessment 2023
Sustainable Finance Guidelines
Net-Zero Banking Alliance Progress Report
ESG Integration Framework
```

**Requirements:**
- ✅ First row: Column header (any name, e.g., "Report Title")
- ✅ Each subsequent row: One report title
- ✅ UTF-8 encoding
- ✅ No special formatting needed

**You can include:**
- Your organization's internal reports
- Industry reports you want to track
- Competitor reports
- Any publications you're interested in

### Step 2: Open the Web Application

Navigate to your deployed app URL:
```
https://your-app.streamlit.app
```

### Step 3: Configure Data Source

In the **sidebar**:

1. **Scopus Citation Data**
   - If available: Check "Use pre-loaded Scopus data" ✅
   - Or upload your own Scopus export

2. **Report List to Analyze**
   - Select: **"📤 Upload my own report list"**
   - Click "Browse files"
   - Select your CSV file
   - Upload complete! 🎉

### Step 4: Search Your Reports

**Option A: Single Report Search**
1. Select or type a report name from your list
2. Click "🚀 Search"
3. View citation count and citing papers
4. Download results if needed

**Option B: Batch Analysis**
1. Switch to "📊 Batch Report Search"
2. Select multiple reports from your list
3. Click "🚀 Batch Search"
4. View summary with charts
5. Download combined results

---

## 📊 What You'll Get

For each report in your list, you'll see:

### Citation Metrics
- **Total Citations** - How many papers cite this report
- **Average Similarity** - Match quality (higher = more confident)
- **Match Method** - How citations were found

### Citing Papers List
- Paper titles that cite your report
- Reference text (how they cited it)
- Similarity scores
- Downloadable CSV

### Visualizations
- Bar charts of citation counts
- Match method distribution
- Easy comparison across reports

---

## 💡 Use Cases

### Use Case 1: Track Your Organization's Impact
**Scenario:** You work at a think tank and want to track academic citations of your 20 flagship reports.

**Steps:**
1. Create CSV with your 20 report titles
2. Upload to the system
3. Run batch search
4. Get comprehensive citation report
5. Share with leadership!

### Use Case 2: Competitive Intelligence
**Scenario:** Monitor how often competitor reports are cited vs. yours.

**Steps:**
1. List your reports + competitor reports in CSV
2. Upload and batch search
3. Compare citation counts
4. Identify gaps and opportunities

### Use Case 3: Literature Review
**Scenario:** You're writing a paper and want to see which foundational reports are most cited in your field.

**Steps:**
1. List key reports in your domain
2. Upload and search
3. Identify most influential works
4. Use in your literature review

### Use Case 4: Grant Applications
**Scenario:** Need to demonstrate research impact for grant renewal.

**Steps:**
1. List your published reports
2. Search citations
3. Export detailed citation list
4. Include in grant application as evidence of impact

---

## 📋 CSV Format Details

### Minimum Format (Recommended)
```csv
Report Title
Your First Report Name
Your Second Report Name
Your Third Report Name
```

### Can Include Additional Columns (Optional)
The system only reads the first column, but you can include others for your reference:

```csv
Report Title,Year,Authors,Department
Principles for Responsible Banking,2019,UNEP FI,Finance
Climate Risk Assessment,2020,John Doe,Research
Sustainable Finance,2021,Jane Smith,Policy
```

**Note:** Only the first column ("Report Title") is used for searching.

### Common Mistakes to Avoid

❌ **Wrong:** Empty first column
```csv
,Report Title
,Report 1
,Report 2
```

✅ **Correct:** Title in first column
```csv
Report Title
Report 1
Report 2
```

❌ **Wrong:** Multiple titles per cell (comma-separated)
```csv
Report Title
"Report 1, Report 2, Report 3"
```

✅ **Correct:** One title per row
```csv
Report Title
Report 1
Report 2
Report 3
```

---

## 🔍 How Matching Works

The system uses three methods to find citations:

### 1. Exact Match (Most Reliable)
Report title appears exactly as-is in the citation
```
Your title: "Principles for Responsible Banking"
Citation: "...UNEP FI (2019). Principles for Responsible Banking..."
✅ Match: 100% similarity
```

### 2. Fuzzy Match (Very Good)
Similar but not identical (typos, abbreviations)
```
Your title: "Principles for Responsible Banking"
Citation: "...Principle for Responsible Bank (UNEP FI, 2019)..."
✅ Match: 92% similarity
```

### 3. Word Overlap (Good)
Key words match even if order differs
```
Your title: "Climate Risk Assessment 2023"
Citation: "...2023 Assessment of Climate Risks (Authors)..."
✅ Match: 75% similarity
```

**Threshold:** Default 85% (adjustable in sidebar)
- Higher = stricter, fewer false positives
- Lower = more lenient, might include some borderline matches

---

## 📊 Sample Workflow

### Example: Analyzing 10 Internal Reports

**Starting Point:**
- You have 10 reports published by your organization
- Want to see their academic citation impact

**Workflow:**

1. **Prepare CSV (5 minutes)**
   ```csv
   Report Title
   Annual Sustainability Report 2023
   ESG Investment Guidelines
   Climate Transition Roadmap
   Green Finance Framework
   Biodiversity Action Plan
   Net-Zero Strategy 2030
   Circular Economy Principles
   Social Impact Assessment Tool
   Governance Best Practices
   Renewable Energy Policy Brief
   ```

2. **Upload and Configure (2 minutes)**
   - Open app
   - Select "Upload my own report list"
   - Upload your CSV
   - Confirm data loaded

3. **Batch Search (5-10 minutes)**
   - Switch to "Batch Report Search"
   - Select all 10 reports
   - Click "Batch Search"
   - Wait for processing

4. **Review Results (10 minutes)**
   - See which reports are most cited
   - Identify trends
   - Note which papers cite your work

5. **Export and Share (2 minutes)**
   - Download summary CSV
   - Create charts for presentation
   - Share with stakeholders

**Total Time:** ~25-30 minutes for comprehensive analysis!

---

## 🎓 Advanced Tips

### Tip 1: Standardize Report Titles
For best results, use the **exact official title** as it appears in publications:
- ✅ "Principles for Responsible Banking: Implementation Guidance"
- ❌ "PRB Guidance" (too short, might miss citations)

### Tip 2: Include Variations
If a report is known by multiple names, include both:
```csv
Report Title
Principles for Responsible Banking
PRB Implementation Guidance
UNEP FI Responsible Banking Principles
```

### Tip 3: Batch Processing
For large lists (50+ reports):
- Process in batches of 20-30
- Download results after each batch
- Combine in Excel/Sheets later

### Tip 4: Regular Monitoring
- Save your report list CSV
- Re-run analysis quarterly/annually
- Track citation growth over time

---

## 🚨 Troubleshooting

### Problem: "No citations found" for all reports

**Possible Causes:**
1. Report titles don't match citation format
2. Threshold too high
3. Reports not yet widely cited

**Solutions:**
- Try lowering similarity threshold to 75-80%
- Check if report titles are exact official names
- Search one report manually to verify format

### Problem: CSV upload fails

**Possible Causes:**
1. Wrong file encoding
2. Special characters in titles
3. File corrupted

**Solutions:**
- Save as UTF-8 CSV in Excel
- Remove special symbols
- Try with example_report_list.csv first

### Problem: Too many false positives

**Solutions:**
- Increase similarity threshold to 90-95%
- Review match methods (exact > fuzzy > word overlap)
- Check if report titles are too generic

---

## 📞 Support

- **Questions:** fan.su@un.org
- **Example File:** Download [example_report_list.csv](example_report_list.csv)
- **Video Tutorial:** [Coming soon]

---

## ✅ Quick Checklist

Before you start:
- [ ] CSV file prepared with report titles
- [ ] File saved as UTF-8 encoding
- [ ] Report titles are official/exact names
- [ ] Scopus data available (pre-loaded or uploaded)

Ready to analyze:
- [ ] Opened web application
- [ ] Uploaded report list
- [ ] Verified data loaded successfully
- [ ] Selected search mode (single/batch)

After analysis:
- [ ] Reviewed citation counts
- [ ] Checked sample citing papers
- [ ] Downloaded results CSV
- [ ] Noted insights for follow-up

---

**Ready to track your impact? Upload your report list and start analyzing!** 🚀
