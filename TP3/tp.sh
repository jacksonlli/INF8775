#!/bin/sh
while getopts e:c:p flag
do
	case "${flag}" in
		e) ext=${OPTARG};;
		c) con=${OPTARG};;
		p) marker1='p';;
	esac
done
python3 main_12_9.py $ext $con $marker1