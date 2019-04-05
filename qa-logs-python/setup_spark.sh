#!/usr/bin/bash

# setup spark
wget https://www-us.apache.org/dist/spark/spark-2.4.1/spark-2.4.1-bin-hadoop2.7.tgz .
tar -xzf spark-2.4.1-bin-hadoop2.7.tgz
/opt/spark-2.4.1
ln -s /opt/spark-2.4.1 /opt/spark̀

echo "export SPARK_HOME=/opt/spark" >> ~/.bashrc
echo "export PATH=$SPARK_HOME/bin:$PATH" >> ~/.bashrc

source ~/.bashrc