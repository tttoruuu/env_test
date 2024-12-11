import os
from dotenv import load_dotenv
import openai
import streamlit as st
from firebase_admin import credentials, initialize_app

# 環境変数をロード（ローカル環境用）
if os.path.exists(".env"):
    load_dotenv()

# 環境変数を確認
firebase_key_path = os.getenv("FIREBASE_KEY_PATH")
st.write(f"FIREBASE_KEY_PATH: {firebase_key_path}")

# 環境の判別
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")  # デフォルトは "production"

try:
    if ENVIRONMENT == "local":
        # ローカル環境の設定
        st.write("Running in Local Environment")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        firebase_key_path = os.getenv("FIREBASE_KEY_PATH")
        
        if firebase_key_path and os.path.exists(firebase_key_path):
            cred = credentials.Certificate(firebase_key_path)
            initialize_app(cred)
        else:
            raise FileNotFoundError(
            f"Firebaseキーが見つかりません。ローカル環境の設定を確認してください。\n"
            f"指定されたパス: {firebase_key_path}"
            )           

    else:
        # デプロイ環境の設定
        st.write("Running in Production Environment")
        if "openai" in st.secrets:
            openai.api_key = st.secrets["openai"]["OPENAI_API_KEY"]
        else:
            raise FileNotFoundError("OpenAI APIキーが secrets.toml に設定されていません。")
        
        if "firebase" in st.secrets:
            cred = credentials.Certificate(st.secrets["firebase"])
            initialize_app(cred)
        else:
            raise FileNotFoundError("Firebase 設定が secrets.toml に設定されていません。")

except FileNotFoundError as e:
    st.error("設定ファイルが見つかりません。ローカル環境の場合は .env を、デプロイ環境の場合は secrets.toml を確認してください。")
    st.error(str(e))
