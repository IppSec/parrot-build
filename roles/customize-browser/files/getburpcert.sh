#!/bin/bash
# ==============================================================================
#  Retriever script to headlessly launch Burp Suite and download its CA Certificate
# ==============================================================================

# Search for the Burp Suite jar in a localized, standard path (much faster than root find)
burp=$(find /usr/share/burpsuite -name "burpsuite*.jar" -o -name "burp*.jar" 2>/dev/null | head -n 1)

if [ -z "$burp" ]; then
    # Fallback search if not in standard directory
    burp=$(find /usr/share/ -name "burpsuite*.jar" -o -name "burp*.jar" 2>/dev/null | head -n 1)
fi

# Locate the appropriate Java binary (bundled JRE vs system-wide fallback)
java_bin="/usr/share/burpsuite/jre/bin/java"
if [ ! -f "$java_bin" ]; then
    java_bin=$(which java)
fi

if [ -n "$burp" ] && [ -n "$java_bin" ]; then
    echo "[*] Found Burp Suite Jar: $burp"
    echo "[*] Using Java binary: $java_bin"
    
    # Start Burp headlessly in background. It automatically listens on port 8080
    timeout 45 "$java_bin" -Djava.awt.headless=true -jar "$burp" --headless < <(echo y) &
    
    # Loop and check if the port is open and we can download the certificate
    echo "[*] Waiting for Burp Suite web server to start up..."
    for i in {1..15}; do
        if curl -s http://localhost:8080/cert -o /tmp/cacert.der; then
            echo "[+] Successfully downloaded Burp Suite CA Certificate!"
            exit 0
        fi
        sleep 2
    done
    
    echo "[-] Error: Failed to retrieve Burp Suite CA Certificate (Timeout)."
    exit 1
else
    echo "[-] Error: Could not locate Burp Suite or Java."
    exit 1
fi
