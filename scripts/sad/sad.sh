#!/bin/bash

num=$((RANDOM % 3))

if [ $num -eq 0 ]; then
    path="./assets/images/sad/sad1.jpg"
elif [ $num -eq 1 ]; then
    path="./assets/images/sad/sad2.jpg"
else
    path="./assets/images/sad/sad3.jpg"
fi
display -resize '50%' $path &