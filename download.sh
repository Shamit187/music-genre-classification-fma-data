#!/bin/bash

cd data

# Check if a flag is provided
if [ $# -eq 0 ]; then
    echo "Please provide a flag: -s, -m, -l, or -f"
    exit 1
fi

# Function to download and verify the file
download_and_verify() {
    local url="$1"
    local filename="$2"
    local sha1_expected="$3"
    
    echo "Downloading $filename..."
    curl -O "$url"
    
    echo "Verifying $filename..."
    echo "$sha1_expected  $filename" | sha1sum -c -
    if [ $? -ne 0 ]; then
        echo "Failed to verify $filename"
        exit 1
    fi
    
    unzip "$filename"
    rm "$filename"
}

# Download and verify metadata regardless of the flag
metadata_url="https://os.unil.cloud.switch.ch/fma/fma_metadata.zip"
metadata_sha1="f0df49ffe5f2a6008d7dc83c6915b31835dfe733"
download_and_verify "$metadata_url" "fma_metadata.zip" "$metadata_sha1"

# Process the flag and download corresponding file
case $1 in
    -s)
        url="https://os.unil.cloud.switch.ch/fma/fma_small.zip"
        filename="fma_small.zip"
        sha1="ade154f733639d52e35e32f5593efe5be76c6d70"
        ;;
    -m)
        url="https://os.unil.cloud.switch.ch/fma/fma_medium.zip"
        filename="fma_medium.zip"
        sha1="c67b69ea232021025fca9231fc1c7c1a063ab50b"
        ;;
    -l)
        url="https://os.unil.cloud.switch.ch/fma/fma_large.zip"
        filename="fma_large.zip"
        sha1="497109f4dd721066b5ce5e5f250ec604dc78939e"
        ;;
    -f)
        url="https://os.unil.cloud.switch.ch/fma/fma_full.zip"
        filename="fma_full.zip"
        sha1="0f0ace23fbe9ba30ecb7e95f763e435ea802b8ab"
        ;;
    *)
        echo "Invalid flag. Please use: -s, -m, -l, or -f"
        exit 1
        ;;
esac

download_and_verify "$url" "$filename" "$sha1"

echo "Download and extraction completed."

cd ..