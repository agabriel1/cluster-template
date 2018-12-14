# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg
import geni.rspec.igext as IG

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()


tourDescription = \
"""
This profile provides the template for a full research cluster with head node, scheduler, compute nodes, and shared file systems.
First node (head) should contain: 
- Shared home directory using Networked File System
- Management server for SLURM
Second node (metadata) should contain:
- Metadata server for SLURM
Third node (storage):
- Shared software directory (/software) using Networked File System
Remaining three nodes (computing):
- Compute nodes  
"""

#
# Setup the Tour info with the above description and instructions.
#  
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
request.addTour(tour)

prefixForIP = "192.168.1."

link = request.LAN("lan")

for i in range(0,15):
  if i == 0:
    node = request.XenVM("head")
    node.routable_control_ip = "true"
    
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/setupNFS_head.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/install_mpi.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/mountHead.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/setupNFS_head.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/mountHead.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/install_mpi.sh"))
    
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/slurm/slurm.conf /usr/local/etc/"))
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/slurm/cgroup.conf /usr/local/etc/"))
    node.addService(pg.Execute(shell="sh", command="sudo bash /local/repository/slurm_install.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /usr/local/etc/slurmctld"))

    
    node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/passwordless.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/passwordless.sh"))
    
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* /scratch"))
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* /users/AG899460/scratch"))
  elif i == 1:
    node = request.XenVM("metadata")
    node.addService(pg.Execute(shell="sh", command="sudo bash /local/repository/slurm_install.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/slurm/slurmdbd.conf /usr/local/etc/"))
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/slurm/cgroup.conf /usr/local/etc/"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl enable mariadb"))
    node.addService(pg.Execute(shell="sh", command="sudo systemctl start mariadb"))
    node.addService(pg.Execute(shell="sh", command="mysql -u root < /local/repository/slurm/sqlSetup.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /usr/local/etc/slurmdbd"))
    
  elif i == 2:
    node = request.XenVM("storage")
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/mountHead.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/mountHead.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/setupNFS_Storage.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/setupNFS_Storage.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* /scratch"))
  else:
    node = request.XenVM("compute-" + str(i-2))
    node.addService(pg.Execute(shell="sh", command="sudo chmod 755 /local/repository/client.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/client.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/source/* /scratch"))
    
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/slurm/slurm.conf /usr/local/etc/"))
    node.addService(pg.Execute(shell="sh", command="sudo cp /local/repository/slurm/cgroup.conf /usr/local/etc/"))
    node.addService(pg.Execute(shell="sh", command="sudo bash /local/repository/slurm_install.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /usr/local/etc/slurmd"))

    
  node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops:CENTOS7-64-STD"
  node.cores = 4
  node.ram = 4096
  iface = node.addInterface("if" + str(i))
  iface.component_id = "eth1"
  iface.addAddress(pg.IPv4Address(prefixForIP + str(i + 1), "255.255.255.0"))
  link.addInterface(iface)
  if i != 0:
    node.addService(pg.Execute(shell="sh", command="sudo chmod 777 /local/repository/passwordless.sh"))
    node.addService(pg.Execute(shell="sh", command="sudo /local/repository/passwordless.sh"))

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
