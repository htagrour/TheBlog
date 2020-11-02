service mysql start
mysql -u root -p"root" -e "CREATE DATABASE my_blog DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;";
mysql -u root -p"root" -e "GRANT ALL ON my_blog.* TO 'hamza'@'localhost' IDENTIFIED BY '1234'; FLUSH PRIVILEGES;";
mysql -u hamza -p"1234" my_blog < database.sql;
#pip install -r requirements.txt
python /my_blog/my_blog.py
