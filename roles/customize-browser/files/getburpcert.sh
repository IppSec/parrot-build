#!/bin/bash
/bin/bash -c "timeout 45 /usr/lib/jvm/jdk-22.0.2-oracle-x64/bin/java -Djava.awt.headless=true -jar /usr/share/burpsuite/burpsuite_community.jar < <(echo y) &" 
sleep 30
curl http://localhost:8080/cert -o /tmp/cacert.der
exit
