mkdir -p scrapper

python -m grpc_tools.protoc -I. --python_out=./scrapper --pyi_out=./scrapper --grpc_python_out=./scrapper ./scrapper.proto
