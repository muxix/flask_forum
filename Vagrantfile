# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  
  # 虚拟机镜像名字，不能改
  config.vm.box_url = "https://mirrors.tuna.tsinghua.edu.cn/ubuntu-cloud-images/xenial/current/xenial-server-cloudimg-amd64-vagrant.box"
  config.vm.box = "ubuntu/xenial"

  # 映射文件夹
  config.vm.synced_folder ".", "/var/www/forum"

  # 桥接网络
  config.vm.network "public_network"

  # 脚本
  # 为了方便测试下面脚本，把 bashrc 设置独立出来
  config.vm.provision "shell", inline: <<-SHELL
    # 换成 root 用户运行
    sudo su
    bash /var/www/forum/deploy.sh
  SHELL
  
end
