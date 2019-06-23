#!/bin/bash -xe
  exec > >(tee /var/log/user_data.log|logger -t user-data -s 2>/dev/console) 2>&1
  # Settings -> enable tracing for commands
  set -x

  echo "StartUpScript Quorum executing...." >> ~/user_data.log
  sudo apt-get update

  echo 'Y' | apt-get install golang-go

  sudo git clone https://github.com/jpmorganchase/quorum.git /home/ubuntu/quorum

  (cd /home/ubuntu/quorum && sudo make all)
  echo 'Building Quorum binaries...'

  # create skeleton genesis block
  sudo printf '{
  "alloc": {
    "0xsubstitute_address": {
      "balance": "10000000000000000000000"
    }
  },
  "coinbase": "0x0000000000000000000000000000000000000000",
  "config": {
    "homesteadBlock": 0,
    "byzantiumBlock": 0,
    "chainId": 10,
    "eip150Block": 0,
    "eip155Block": 0,
    "eip150Hash": "0x0000000000000000000000000000000000000000000000000000000000000000",
    "eip158Block": 0,
    "isQuorum": true
  },
  "difficulty": "0x0",
  "extraData": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "gasLimit": "0xE0000000000000",
  "mixhash": "0x00000000000000000000000000000000000000647572616c65787365646c6578",
  "nonce": "0x0",
  "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
  "timestamp": "0x00"
}\n' | sudo tee -a /home/ubuntu/genesis_raw.json

  # =======  Create success indicator at end of this script ==========
  touch /var/log/user_data_success.log

  exit 1



#curl -o /home/ubuntu/java-jdk-8.tar.gz https://download.oracle.com/otn/java/jdk/8u211-b12/478a62b7d4e34b78b671c754eaaf38ab/jdk-8u211-linux-x64.tar.gz
#wget --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie;" https://download.oracle.com/otn/java/jdk/8u211-b12/478a62b7d4e34b78b671c754eaaf38ab/jdk-8u211-linux-x64.tar.gz
#wget --no-check-certificate --no-cookies --header "Cookie: HACK" https://download.oracle.com/otn/java/jdk/8u211-b12/478a62b7d4e34b78b671c754eaaf38ab/jdk-8u211-linux-x64.tar.gz
#wget --continue --no-check-certificate -O jdk-8u191-linux-x64.tar.gz --header "Cookie: oraclelicense=a" https://download.oracle.com/otn/java/jdk/8u211-b12/478a62b7d4e34b78b671c754eaaf38ab/jdk-8u211-linux-x64.tar.gz
#curl -o /home/ubuntu/java-jdk-8 https://download.oracle.com/otn/java/jdk/8u211-b12/478a62b7d4e34b78b671c754eaaf38ab/jdk-8u211-docs-all.zip
#curl -L -C --b "oraclelicense=accept-securebackup-cookie" -o /home/ubuntu/java-jdk-8 https://download.oracle.com/otn/java/jdk/8u211-b12/478a62b7d4e34b78b671c754eaaf38ab/jdk-8u211-linux-x64.tar.gz
#sudo tar -xvzf /home/ubuntu/java-jdk-8
# wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn/java/jdk/8u211-b12/478a62b7d4e34b78b671c754eaaf38ab/jdk-8u211-linux-x64.tar.gz

sudo apt update
sudo apt install -y openjdk-8-jdk

# export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/bin/
# echo JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64/bin" | sudo tee -a /etc/environment

sudo apt install -y curl

sudo curl -o /apache-maven-3.6.1-bin.tar.gz https://www-us.apache.org/dist/maven/maven-3/3.6.1/binaries/apache-maven-3.6.1-bin.tar.gz

sudo tar -xvzf /apache-maven-3.6.1-bin.tar.gz --directory /opt
echo M2_HOME="/opt/apache-maven-3.6.1" | sudo tee -a /etc/environment
PATH=$PATH:/opt/apache-maven-3.6.1/bin

sudo update-alternatives --install "/usr/bin/mvn" "mvn" "/opt/apache-maven-3.6.1/bin/mvn" 0
sudo update-alternatives --set mvn /opt/apache-maven-3.6.1/bin/mvn

sudo wget https://raw.github.com/dimaj/maven-bash-completion/master/bash_completion.bash --output-document /etc/bash_completion.d/mvn
echo ($mvn --version)


sudo -u ubuntu curl -o /home/ubuntu/libsodium-1.0.18-stable.tar.gz https://download.libsodium.org/libsodium/releases/libsodium-1.0.18-stable.tar.gz
sudo -u ubuntu tar -xvzf /home/ubuntu/libsodium-1.0.18-stable.tar.gz --directory /home/ubuntu/
(cd /home/ubuntu/libsodium-stable && sudo ./configure)

(cd /home/ubuntu/libsodium-stable && sudo make)
(cd /home/ubuntu/libsodium-stable && sudo make check)
(cd /home/ubuntu/libsodium-stable && sudo make install)

sudo -u ubuntu mkdir /home/ubuntu/tessera

sudo -u ubuntu git clone https://github.com/jpmorganchase/tessera /home/ubuntu/tessera

(cd /home/ubuntu/tessera && sudo -u ubuntu mvn install)

# java -jar tessera-dist/tessera-app/target/tessera-app-0.10-SNAPSHOT-jdk8_app.jar -configfile /path/to/config.json

# alias tessera="java -jar /home/ubuntu/tessera-dist/tessera-app/target/tessera-app-0.10-SNAPSHOT-jdk8_app.jar"

# tessera -configfile /path/to/config.json

# tessera help

# java -cp some-jdbc-driver.jar:/path/to/tessera-app.jar:. com.quorum.tessera.Launcher




  # =======  Create success indicator at end of this script ==========
  touch /var/log/user_data_success.log

# [ERROR] No .editorconfig properties applicable for files under '/home/ubuntu/tessera'