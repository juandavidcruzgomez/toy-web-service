#!/usr/bin/bash

echo "Clean the environment up and start over"
echo "Removing metrics..."
rm -rf metrics
echo "Removing models..."
rm -rf models
echo "Removing prepared data..."
rm -rf data/prepared
echo "Recreating directories..."
mkdir -p data/prepared
mkdir -p models
mkdir -p metrics
echo "Done."