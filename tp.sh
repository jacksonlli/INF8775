#!/bin/sh
while getopts a:e:pt flag
do
    case "${flag}" in
        a) algo=${OPTARG};;
        e) ext=${OPTARG};;
        p) marker=p;;
        t) marker=t;;      
    esac
done
python3 main.py $algo $ext $marker