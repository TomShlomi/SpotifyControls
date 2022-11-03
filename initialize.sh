#!/bin/sh

#Get relevant paths
PTH=`pwd`
NODE=`which node`
#Create addsong.applescript
cp addsong.applescript.template addsong.applescript
sed -i '' "s|PTH|\"$PTH\"|g" addsong.applescript
#Create addsong.sh
cp addsong.sh.template addsong.sh
sed -i '' "s|PTH|$PTH|g" addsong.sh
sed -i '' "s|NODE|$NODE|g" addsong.sh
#Create app.js
cp app.js.template app.js