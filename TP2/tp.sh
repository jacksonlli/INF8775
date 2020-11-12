#!/bin/sh
while getopts a:e:pt flag
do
    case "${flag}" in
        a) algo=${OPTARG};;
        e) ext=${OPTARG};;
        p) marker1='p';;
        t) marker2='t';;      
    esac
done
python3 main.py $algo $ext $marker1 $marker2