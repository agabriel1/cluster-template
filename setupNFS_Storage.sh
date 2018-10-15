sudo yum install nfs-utils nfs-utils-lib
sudo yum install portmap

/etc/init.d/portmap start
/etc/init.d/nfs start
chkconfig --level 35 portmap on
chkconfig --level 35 nfs on

mkdir /scratch
vi /etc/exports
/software 192.168.1.3(rw,sync,no_root_squash)
/software 192.168.1.4(rw,sync,no_root_squash)
/software 192.168.1.5(rw,sync,no_root_squash)
/software 192.168.1.6(rw,sync,no_root_squash)
/software 192.168.1.7(rw,sync,no_root_squash)
/software 192.168.1.8(rw,sync,no_root_squash)
/software 192.168.1.9(rw,sync,no_root_squash)
/software 192.168.1.10(rw,sync,no_root_squash)
/software 192.168.1.11(rw,sync,no_root_squash)
/software 192.168.1.12(rw,sync,no_root_squash)
/software 192.168.1.13(rw,sync,no_root_squash)
/software 192.168.1.14(rw,sync,no_root_squash)
/software 192.168.1.15(rw,sync,no_root_squash)


#info found:
#https://www.tecmint.com/how-to-setup-nfs-server-in-linux/