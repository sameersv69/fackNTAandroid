how to make it work:

s1) download termux apk and also, termux:api apk from fdroid or github (not Playstore, that version is broke)
s2) run the following commands one by one:
pkg update && pkg upgrade -y

pkg install python git -y


git clone https://github.com/{MY CURRENT USERNAME, Without these brackets}/fackNTAandroid.git

cd facknta
pkg install libxml2 libxslt clang -y
pip install -r requirements.txt

pkg install termux-api -y

termux-wake-lock

python Main_tracker.py

thats it. leave termux running in the background and it will continuously (every 60(+- 15) seconds)  check nta website for new update in the background.
