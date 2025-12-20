#!/bin/bash

docker build -t c_judge     judge_images/c
docker build -t cpp_judge   judge_images/cpp
docker build -t py_judge    judge_images/python
