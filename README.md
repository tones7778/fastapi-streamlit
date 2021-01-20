[auth]

username = XXXXX
password = XXXXX
mydevice = XXXXXXX

----------------------------
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
streamlit run frontend.py
