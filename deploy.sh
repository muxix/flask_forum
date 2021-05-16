# 1. 拉代码到 /var/www/forum
# 2. 执行 bash deploy.sh

# 遇到错误立即停止执行
# 显示执行到哪一行
set -ex

# 换源
cp /var/www/forum/misc/sources.list /etc/apt/sources.list
mkdir -p /root/.pip
cp /var/www/forum/misc/pip.conf /root/.pip/pip.conf

# 装依赖 第三方仓库
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update

# 系统设置
apt-get -y install zsh curl ufw
# sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
ufw allow 22
ufw allow 80
ufw allow 443
# ufw allow 25
ufw default deny incoming
ufw default allow outgoing
ufw status verbose
ufw -f enable

# 装依赖
debconf-set-selections /var/www/forum/database_secret.conf
apt-get install -y mysql-server

apt-get install -y git supervisor nginx python3.6
python3.6 /var/www/forum/get-pip.py
pip3 install jinja2 flask gevent gunicorn pymysql flask_sqlalchemy flask_admin

# debconf-set-selections /var/www/forum/postfix.conf
# apt-get install -y postfix
# pip3 install flask_mail

# apt-get install -y redis-server
# pip3 install redis

# 删掉 nginx default 设置
rm -f /etc/nginx/sites-enabled/default
rm -f /etc/nginx/sites-available/default

# supervisor
cp /var/www/forum/forum.conf /etc/supervisor/conf.d/forum.conf

# nginx
# 不要在 sites-available 里面放任何东西
cp /var/www/forum/forum.nginx /etc/nginx/sites-enabled/forum
chmod -R o+rwx /var/www/forum

# 初始化
cd /var/www/forum
python3.6 reset.py

# 重启服务器
service supervisor restart
service nginx restart

echo 'deploy success'
echo 'ip'
hostname -I