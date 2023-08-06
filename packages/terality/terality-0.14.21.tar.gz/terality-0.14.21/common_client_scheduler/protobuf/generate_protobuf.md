Protobuf classes located in `common_client_scheduler/common_client_scheduler/protobuf/generated/` are generated using the protobuf compiler.  
Do not modify manually!

How to update protobuf classes:  
1- Make your changes to the proto messages inside the `messages.proto` file  
2- Make sure you have installed the protoc python compiler -> find the list of releases here `https://github.com/protocolbuffers/protobuf/releases`  
3- Install the mypy plugin for protoc [in your virtual env] to generate the right type annotations for python `pip install mypy-protobuf`  
4- Compile your updated protobuf files using:    
```bash
	cd common_client_scheduler/common_client_scheduler/protobuf/ && [/path/to/your]/bin/protoc -I. --python_out=./generated/ --mypy_out=./generated/ ./client_scheduler_messages.proto
```
