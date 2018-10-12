#!/bin/sh

src_dir=$(dirname "$0")/src
lambda_dir=${src_dir}/lambda
build_dir=$(dirname "$0")/build

lambda_functions=('chortle-button-press')

mkdir -p $build_dir

for target in ${lambda_functions[@]}; do
    artifact=${build_dir}/${target}.zip
    zip -rj $artifact ${lambda_dir}/${target}
    aws lambda update-function-code --profile bradley --function-name $target --zip-file fileb://${artifact}
done
