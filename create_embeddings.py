
### YOU WILL NOT NEED TO RUN THIS AGAIN ###
# Script for creating the embedding for the csv.
import pandas as pd
import requests
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os
from pathlib import Path

def create_embeddings():
    """Download Quran data from GitHub and create embeddings"""
    
    print("🔄 Starting embedding creation process...")
    
    # GitHub URL for the Quran data
    GITHUB_CSV_URL = "https://raw.githubusercontent.com/ZaynIkhlaq/Ayats_Tagged/main/quran_emotion_tagged.csv"
    
    try:
        # Step 1: Download CSV from GitHub
        print("📥 Downloading Quran data from GitHub...")
        response = requests.get(GITHUB_CSV_URL)
        response.raise_for_status()
        
        # Save CSV locally
        with open("quran_emotion_tagged.csv", "wb") as f:
            f.write(response.content)
        
        print(f"✅ Downloaded {len(response.content)} bytes of data")
        
    except Exception as e:
        print(f"❌ Failed to download data: {e}")
        return False
    
    try:
        # Step 2: Load and process data
        print("📖 Loading Quran data...")
        df = pd.read_csv("quran_emotion_tagged.csv")
        ayahs = df['ayah_en'].astype(str).tolist()
        
        print(f"📊 Loaded {len(ayahs)} verses")
        print(f"📋 Sample verse: {ayahs[0][:100]}...")
        
    except Exception as e:
        print(f"❌ Failed to load CSV: {e}")
        return False
    
    try:
        # Step 3: Load sentence transformer model
        print("🧠 Loading sentence transformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Model loaded successfully")
        
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False
    
    try:
        # Step 4: Create embeddings
        print("🔄 Creating embeddings (this may take a few minutes)...")
        embeddings = model.encode(ayahs, convert_to_tensor=False, show_progress_bar=True)
        
        print(f"✅ Created {len(embeddings)} embeddings")
        print(f"📏 Embedding shape: {embeddings.shape}")
        
    except Exception as e:
        print(f"❌ Failed to create embeddings: {e}")
        return False
    
    try:
        # Step 5: Save embeddings and metadata
        print("💾 Saving embeddings...")
        
        cache_data = {
            'df': df,
            'ayahs': ayahs,
            'embeddings': embeddings,
            'metadata': {
                'total_verses': len(ayahs),
                'embedding_dimension': embeddings.shape[1],
                'model_name': 'all-MiniLM-L6-v2',
                'created_at': pd.Timestamp.now().isoformat()
            }
        }
        
        with open("quran_embeddings.pkl", "wb") as f:
            pickle.dump(cache_data, f)
        
        # Get file size
        file_size = os.path.getsize("quran_embeddings.pkl")
        print(f"✅ Saved embeddings to quran_embeddings.pkl")
        print(f"📁 File size: {file_size / (1024*1024):.2f} MB")
        
    except Exception as e:
        print(f"❌ Failed to save embeddings: {e}")
        return False
    
    # Step 6: Create a smaller version for testing
    try:
        print("🧪 Creating test version with first 100 verses...")
        test_data = {
            'df': df.head(100),
            'ayahs': ayahs[:100],
            'embeddings': embeddings[:100],
            'metadata': {
                'total_verses': 100,
                'embedding_dimension': embeddings.shape[1],
                'model_name': 'all-MiniLM-L6-v2',
                'is_test': True,
                'created_at': pd.Timestamp.now().isoformat()
            }
        }
        
        with open("quran_embeddings_test.pkl", "wb") as f:
            pickle.dump(test_data, f)
        
        test_size = os.path.getsize("quran_embeddings_test.pkl")
        print(f"✅ Created test file: quran_embeddings_test.pkl ({test_size / 1024:.2f} KB)")
        
    except Exception as e:
        print(f"⚠️ Failed to create test file: {e}")
    
    # Step 7: Print summary and next steps
    print("\n" + "="*50)
    print("🎉 EMBEDDINGS CREATED SUCCESSFULLY!")
    print("="*50)
    print("\n📋 Next steps:")
    print("1. Upload quran_embeddings.pkl to your GitHub repository")
    print("2. Get the raw URL for the file")
    print("3. Update the Streamlit app with the GitHub URL")
    print("\n📁 Files created:")
    print(f"   - quran_embeddings.pkl ({file_size / (1024*1024):.2f} MB)")
    print(f"   - quran_embeddings_test.pkl ({test_size / 1024:.2f} KB)")
    print("\n🔗 GitHub upload instructions:")
    print("   - Go to your GitHub repository")
    print("   - Click 'Add file' > 'Upload files'")
    print("   - Drag and drop quran_embeddings.pkl")
    print("   - Commit the file")
    print("   - Get the raw URL: https://raw.githubusercontent.com/username/repo/main/quran_embeddings.pkl")
    
    return True

if __name__ == "__main__":
    success = create_embeddings()
    if success:
        print("\n✅ Ready to upload to GitHub!")
    else:
        print("\n❌ Failed to create embeddings. Please check the errors above.") 