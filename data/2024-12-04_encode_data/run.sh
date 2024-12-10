#!/bin/bash
set -x -e
cat url_links.txt | while read sample assay url
do
	mkdir -p "${sample}/${assay}"
	wget -P "${sample}/${assay}" "${url}"
done < url_links.txt
