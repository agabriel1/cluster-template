set -x

sudo yum -y install nfs-utils-lib
sudo mount -t nfs 192.168.1.3:/scratch /mnt/scratch

vi /etc/fstab
192.168.1.3:/scratch /mnt  nfs defaults 0 0
