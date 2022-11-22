echo " BUID START"
pip install -r requirements.txt
python3.10.2 manage.py collectstatic --noinput --clear
echo " BUID END"