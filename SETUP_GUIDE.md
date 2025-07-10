# 🚀 Quran Journal - Optimized Setup Guide

This guide will help you create embeddings, upload them to GitHub, and run the optimized Streamlit app.

## 📋 Prerequisites

1. **Python Environment**: Make sure you have Python 3.8+ installed
2. **Required Packages**: Install the dependencies
3. **GitHub Account**: You'll need to upload files to GitHub
4. **OpenRouter API Key**: For emotion detection and comfort messages

## 🔧 Step 1: Install Dependencies

```bash
# Install required packages
pip install streamlit pandas requests torch sentence-transformers python-dotenv
```

## 📊 Step 2: Create Embeddings

### Run the Embedding Creation Script

```bash
python create_embeddings.py
```

This script will:
1. Download the Quran data from your GitHub repository
2. Load the sentence transformer model
3. Create embeddings for all verses
4. Save two files:
   - `quran_embeddings.pkl` (full dataset)
   - `quran_embeddings_test.pkl` (first 100 verses for testing)

### Expected Output

```
🔄 Starting embedding creation process...
📥 Downloading Quran data from GitHub...
✅ Downloaded 1234567 bytes of data
📖 Loading Quran data...
📊 Loaded 6236 verses
📋 Sample verse: In the name of Allah, the Entirely Merciful, the Especially Merciful...
🧠 Loading sentence transformer model...
✅ Model loaded successfully
🔄 Creating embeddings (this may take a few minutes)...
✅ Created 6236 embeddings
📏 Embedding shape: (6236, 384)
💾 Saving embeddings...
✅ Saved embeddings to quran_embeddings.pkl
📁 File size: 15.23 MB
🧪 Creating test version with first 100 verses...
✅ Created test file: quran_embeddings_test.pkl (45.67 KB)

==================================================
🎉 EMBEDDINGS CREATED SUCCESSFULLY!
==================================================

📋 Next steps:
1. Upload quran_embeddings.pkl to your GitHub repository
2. Get the raw URL for the file
3. Update the Streamlit app with the GitHub URL
```

## 📤 Step 3: Upload to GitHub

### Option A: Using GitHub Web Interface

1. **Go to your GitHub repository**
2. **Click "Add file" > "Upload files"**
3. **Drag and drop** `quran_embeddings.pkl`
4. **Add commit message**: "Add Quran embeddings for fast loading"
5. **Click "Commit changes"**

### Option B: Using Git Command Line

```bash
# Add the file to your repository
git add quran_embeddings.pkl
git commit -m "Add Quran embeddings for fast loading"
git push origin main
```

## 🔗 Step 4: Get the Raw URL

After uploading, get the raw URL:

1. **Click on** `quran_embeddings.pkl` in your repository
2. **Click "Raw"** button
3. **Copy the URL** (it should look like):
   ```
   https://raw.githubusercontent.com/yourusername/quran-journal/main/quran_embeddings.pkl
   ```

## ⚙️ Step 5: Update the Streamlit App

Edit `streamlit_app_github.py` and update the GitHub URLs:

```python
# Update these URLs with your actual GitHub URLs
GITHUB_EMBEDDINGS_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/quran_embeddings.pkl"
GITHUB_EMBEDDINGS_TEST_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/quran_embeddings_test.pkl"
```

## 🚀 Step 6: Run the Optimized App

```bash
streamlit run streamlit_app_github.py
```

## 📈 Performance Comparison

| Approach | Loading Time | Memory Usage | Reliability |
|----------|--------------|--------------|-------------|
| **Original** | 3-5 minutes | High | Low |
| **GitHub Embeddings** | 10-30 seconds | Low | High |
| **Test Embeddings** | 5-10 seconds | Very Low | High |

## 🔍 Troubleshooting

### Issue: "Failed to download data"
**Solution**: Check your internet connection and the GitHub URL

### Issue: "Model loading error"
**Solution**: Make sure you have enough RAM (at least 4GB)

### Issue: "Cache corrupted"
**Solution**: Delete the cache file and re-run the script

### Issue: "GitHub URL not found"
**Solution**: 
1. Check that the file was uploaded correctly
2. Verify the raw URL is correct
3. Make sure the repository is public

## 🎯 Advanced Options

### Option 1: Use Test Embeddings First

For faster testing, use the test embeddings:

```python
# In streamlit_app_github.py, change the order:
# Try test embeddings first
GITHUB_EMBEDDINGS_TEST_URL = "your_test_url"
GITHUB_EMBEDDINGS_URL = "your_full_url"
```

### Option 2: Local Caching

For even faster loading, enable local caching:

```python
# Add to streamlit_app_github.py
import os
from pathlib import Path

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

# Save downloaded embeddings locally
if not (CACHE_DIR / "embeddings.pkl").exists():
    # Download and save locally
    with open(CACHE_DIR / "embeddings.pkl", "wb") as f:
        f.write(response.content)
```

### Option 3: Environment Variables

Set up environment variables for easier configuration:

```bash
# Create .env file
OPENROUTER_API_KEY=your_api_key_here
GITHUB_EMBEDDINGS_URL=https://raw.githubusercontent.com/yourusername/repo/main/quran_embeddings.pkl
```

## 📊 Monitoring and Analytics

The app includes built-in monitoring:

- **Loading time**: Shows how long it takes to load embeddings
- **Cache status**: Indicates whether using cached or fresh data
- **Error handling**: Graceful fallbacks if GitHub is unavailable
- **Performance metrics**: Shows total verses and embedding dimensions

## 🔄 Updating Embeddings

To update the embeddings:

1. **Run** `python create_embeddings.py` again
2. **Upload** the new `quran_embeddings.pkl` to GitHub
3. **Restart** the Streamlit app

The app will automatically detect and use the updated embeddings.

## 🎉 Success Indicators

You'll know everything is working when you see:

- ✅ "Loaded X verses!" message
- ✅ Fast loading (under 30 seconds)
- ✅ No error messages
- ✅ Smooth verse matching functionality

## 📞 Support

If you encounter issues:

1. **Check the console output** for error messages
2. **Verify GitHub URLs** are correct
3. **Ensure sufficient memory** (4GB+ recommended)
4. **Test with smaller dataset** first (use test embeddings)

---

**Happy Coding! 🕊️** 