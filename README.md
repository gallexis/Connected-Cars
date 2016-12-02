# Connected Cars

School project of assembling 2 cars with a Raspberry in each of them, controlled by a computer.



## SCP from PC to raspberry without password
[PC]# ssh-keygen -t rsa -b 2048
Generating public/private rsa key pair.  
Enter file in which to save the key (/root/.ssh/id_rsa): # Hit Enter  
Enter passphrase (empty for no passphrase): # Hit Enter  
Enter same passphrase again: # Hit Enter  
Your identification has been saved in /root/.ssh/id_rsa.  
Your public key has been saved in /root/.ssh/id_rsa.pub.  

**Now copy your public key to the raspberry:**  
ssh-copy-id pi@RASPI_IP  
[OR]  
cat ~/.ssh/id_rsa.pub | ssh pi@RASPI_IP "mkdir -p ~/.ssh && cat >>  ~/.ssh/authorized_keys"

#Protocol de communication
##3 types d'objets

### Une machine qui lance le programme principal
Ce sera un ordi qui devra lancer le programme principal et attendre qu'une car "Server" se connecte à lui

### Un car Server
Il doit recevoir des ordres à partir de la machine principale en se connectant sur son interface1
C'est celui qui va se charger de traiter les images et prendre les décisions qui s'imposent. 
Ensuite, il devra informer la voiture qui lui est connecté(sur l'interface2) en lui envoyant un ordre précis

###les cars master-slave

Ces voitures, ont également deux interfaces:
- une première pour se connecter au car qui est devant lui, et qui devient ainsi son maitre
- Il attend une connection sur son deuxième port et devient ainsi maitre de celui qui se connecte à lui
