#!/bin/bash
sudo systemctl start redis-server
python3 generate_book_html.py
python3 generate_static_book_pages.py
python3 webserver.py
