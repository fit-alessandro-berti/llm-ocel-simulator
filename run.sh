#!/bin/bash
nohup streamlit run interface.py --server.address 31.14.134.197 --server.port 15000 > streamlit.log 2>&1 &
