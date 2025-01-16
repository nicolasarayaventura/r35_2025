#!/bin/bash
set -x -e

cat url_links.txt | while read sample assay url
do
	mkdir -p "${sample}/${assay}"
	wget -P "${sample}/${assay}" "${url}"
done < url_links.txt

cat avocado_model.txt | while read model h5_url json_url; do
    mkdir -p "${model}"
    wget -P "${model}" "${h5_url}"
    wget -P "${model}" "${json_url}"
done < avocado_model.txt
