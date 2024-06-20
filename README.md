# """
# flask --app app run --debug
# with gunicorn: gunicorn app:app -b HOST:PORT --reload
# """
http {
        server {
                listen 80 default_server;
                server_name localhost;
                root /home/luisapegoraro/testreact/build;
                index index.html;
        }
}


#luisapegoraro@penguin:/var/www/data$ sudo cp '/home/luisapegoraro/images/beograd:4000.png' .
# THIS IS WHERE HTML IS LOCATED: luisapegoraro@penguin:/usr/share/nginx/html$ pwd
# CAREFUL WITH luisapegoraro@penguin:/etc/nginx/conf.d

# FROM BROWSER: http://100.115.92.206/beograd:4000.png
# AND : http://penguin.linux.test/

# luisapegoraro@penguin:/usr/share/nginx/html/images$ 

# sudo service nginx stop


# sudo nginx -s reload
# sudo service nginx restart

# /home/luisapegoraro/images/beograd:4000.png
