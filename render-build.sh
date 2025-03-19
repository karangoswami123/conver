#!/bin/bash
pip install -r requirements.txt
python -m streamlit run app.py --server.maxUploadSize 1024
