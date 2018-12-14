set -x

sudo yum -y install nfs-utils-lib
sudo mount -t nfs 192.168.1.3:/scratch /users/ag899460/scratch

echo "192.168.1.3:users/ag899460/scratch /scratch  nfs defaults 0 0" >> /etc/fstab
