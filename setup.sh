mkdir -p ~/.streamlit/

echo "[theme]
primaryColor='#00acea'
backgroundColor='#293041'
secondaryBackgroundColor='#343c4f'
textColor='#f1f2f6'
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
