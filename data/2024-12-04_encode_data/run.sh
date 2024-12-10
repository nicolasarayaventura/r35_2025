#!/bin/bash
#test
set -x -e
cat url_links.txt | while read sample assay url
do
	wget ${url} .
done
