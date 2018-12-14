set -x
sudo yum -y install nfs-utils nfs-utils-lib

sudo mkdir -p /users/ag899460/software
sudo chmod 777 /users/ag899460/software

sudo mkdir -p /scratch
sudo chmod 777 /scratch

sudo systemctl enable nfs-server
sudo service nfs start

sudo mount -t nfs 192.168.1.1:/software /users/ag899460/software
sudo mount -t nfs 192.168.1.3:/scratch /scratch

echo '192.168.1.1:/software /users/ag899460/software  nfs defaults 0 0' >> /etc/fstab
echo '192.168.1.3:/scratch /scratch  nfs defaults 0 0' >> /etc/fstab

echo "export PATH='$PATH:/software/openmpi/3.1.2/bin'" >> /users/ag899460/.bashrc
echo "export LD_LIBRARY_PATH='$LD_LIBRARY_PATH:/software/openmpi/3.1.2/lib/'" >> /users/ag899460/.bashrc
