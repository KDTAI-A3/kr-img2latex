#!/bin/bash

curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=1v9ZR34aPj6OCBemjocxfYnhy2kh72m8Y" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=1v9ZR34aPj6OCBemjocxfYnhy2kh72m8Y" -o train.zip

curl -c ./cookie -s -L "https://drive.google.com/uc?export=download&id=12YaxkcwqqJBMT28Q6tOcwbo7o8QPooFh" > /dev/null
curl -Lb ./cookie "https://drive.google.com/uc?export=download&confirm=`awk '/download/ {print $NF}' ./cookie`&id=12YaxkcwqqJBMT28Q6tOcwbo7o8QPooFh" -o test.zip

exit 0