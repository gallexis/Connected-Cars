# CCP
Car communication Protocol in Golang


###Cross compile to raspberry 1 (& 2?): 
env GOOS=linux GOARCH=arm GOARM=6 go build -v

###Cross compile to raspberry 3:
env GOOS=linux GOARCH=arm64 GOARM=7 go build -v


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

