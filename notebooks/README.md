# CUA Notebooks

This folder contains Jupyter notebooks that demonstrate the core functionality of the CUA (Computer Use Automation) system. These notebooks serve as interactive examples and quickstart guides for different components of the CUA platform.

## Available Notebooks

### Core Components
- **`computer_nb.ipynb`** - Demonstrates the Computer API for programmatically operating sandbox VMs using either Cua Cloud Containers or local Lume VMs on Apple Silicon macOS systems
- **`agent_nb.ipynb`** - Shows how to use CUA's Agent to run automated workflows in virtual sandboxes with various AI models (OpenAI, Anthropic, local models)
- **`pylume_nb.ipynb`** - Quickstart guide for the pylume Python library, which handles VM creation, management, and image operations
- **`computer_server_nb.ipynb`** - Demonstrates how to host and configure the Computer server that powers the Computer API

### Evaluation & Benchmarking
- **`eval_osworld.ipynb`** - Shows ComputerAgent integration with HUD for OSWorld benchmarking, supporting both Claude and OpenAI models

### Tutorials
- **`blog/`** - Tutorial notebooks from blog posts:
  - `build-your-own-operator-on-macos-1.ipynb` - Part 1: Building a CUA operator using OpenAI's computer-use-preview model
  - `build-your-own-operator-on-macos-2.ipynb` - Part 2: Using the cua-agent package for more advanced automation

## Purpose

These notebooks provide:
- **Hands-on examples** of CUA's core functionality
- **Step-by-step setup instructions** for different components
- **Code snippets** you can copy and adapt for your own projects
- **Working demonstrations** of computer automation tasks
- **Integration examples** with various AI providers and models

## Getting Started

1. Choose a notebook based on what you want to learn
2. Follow the installation instructions in each notebook
3. Run the cells sequentially to see CUA in action
4. Adapt the code examples for your specific use cases

Most notebooks include both cloud-based (Cua Cloud Containers) and local setup options, making them accessible regardless of your environment.