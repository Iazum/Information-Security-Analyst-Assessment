#!/bin/bash
# Benign ransomware behavior simulation - LAB USE ONLY
# Creates dummy files only; nothing real is encrypted.

TARGET="/home/ubuntu/tes"

echo "[*] Creating test folder: $TARGET"
mkdir -p "$TARGET"
cd "$TARGET" || exit 1

echo "[*] Stage 1: creating 50 normal files"
for i in $(seq 1 50); do echo "data $i" > file$i.txt; done
sleep 10

echo "[*] Stage 2: mass modification (rule 100100)"
for i in $(seq 1 50); do echo "changed" >> file$i.txt; done

echo "[*] Stage 3: renaming to .locked (rule 100101)"
for f in file*.txt; do mv "$f" "$f.locked"; done

echo "[*] Stage 4: dropping ransom note (rule 100102)"
touch HOW_TO_DECRYPT.txt

echo "[+] Simulation complete. Check the Wazuh dashboard for alerts."
