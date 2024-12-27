# GoPhish-Sprayers
This is for spraying exposed GoPhish panels on the internet. This can be extremely useful for InfoSec research.
GoPhish's default credentials are: **admin/gophish**

<img width="1512" alt="Screenshot 2024-12-27 at 6 57 24 AM" src="https://github.com/user-attachments/assets/ad8a298d-6b0f-4ec9-9609-962d56d46a82" />

# How to use
1) git clone https://github.com/BestDevOfc/GoPhish-Sprayers.git
2) cd GoPhish-Sprayers/
3) python3 -m pip install -r requirements.txt --break-system-packages
4) Go to **shodan.io**
5) make an account and use this filter: **http.title:"Gophish - Login"**
6) Click **Download your results**
7) Take the JSON file and put it in the same directory and name it **urls.json**
8) python3 ./Shodan_URLS_extractor.py
9) python3 ./main.py


<img width="1185" alt="Screenshot 2024-12-27 at 6 55 55 AM" src="https://github.com/user-attachments/assets/367f5cf1-07b5-4534-bff5-b08c2f361774" />


