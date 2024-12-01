<p align="center">
  <a href="https://github.com/GabrielJuan349/TraceXR/">
    <img src="./assets/traceXR-logo.png" alt="Logo" width=150 height=150>
  </a>

  <h3 align="center">TraceXR</h3>

  <p align="center">
    Meta Quest application for Vitol challenge to track and recognize objects and patterns in Mixed Reality.
    <br>
    <a href="https://github.com/GabrielJuan349/TraceXR/issues/new?template=bug.md">Report bug</a>
    ·
    <a href="https://github.com/GabrielJuan349/TraceXR/issues/new?template=feature.md&labels=feature">Request feature</a>
  </p>
</p>


## Table of contents

- [Quick start](#quick-start)
- [About this project](#about-this-project)
- [Status](#status)
- [What's included](#whats-included)
- [Bugs and feature requests](#bugs-and-feature-requests)
- [Creators](#creators)
- [Copyright and license](#copyright-and-license)


## Quick start

### Model download - ONNX format
You can find our ONNX model for EfficientNet B7 trained on TU-Berlin Sketch dataset in [Google Drive](https://drive.google.com/file/d/1s6j8zwpggz0hqwEiRSArXn19FGD4639y/view?usp=sharing).

## About this project

This project combines multiple challenges from [LauzHack](https://lauzhack.com/) of [EPFL, Switzerland](https://www.epfl.ch/en/), which are proposed by companies such as [AXA Group](https://axa.com/) (an Artificial Intelligence model that can run on a laptop, mobile device, or immersive device), [Logitech](https://www.logitech.com/) (using the [MX Ink](https://www.logitech.com/es-es/products/vr/mx-ink.html) together with the [Meta Quest 3/3S](https://www.meta.com/ch/en/quest/quest-3/) to create a Mixed Reality (XR) application), and primarily [Vitol](https://www.vitol.com/) (creating an AI service for recognizing static and moving objects and/or a chatbot capable of interacting with the user).

As shown in the image below, this project is a multi-agent AI system combining Speech-To-Text with [OpenAI Whisper](https://openai.com/index/whisper/) for multi-agent routing and generating written responses when necessary using [Qwen2.5-0.5b](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF). It also utilizes [YoLo11](https://github.com/ultralytics/ultralytics) for object detection in images, an [EfficientNet-B7](https://pytorch.org/vision/main/models/efficientnet.html) ([Arxiv](https://arxiv.org/pdf/1905.11946)) for recognizing patterns or drawings made with the MX Ink, and finally, [OpenAI TTS](https://platform.openai.com/docs/guides/text-to-speech) for Text-to-Speech.

<img src="./assets/Multi-Agent Graph.png" alt="Multi Agent Architecture" width=100% height=225>

The implementation within the Meta Quest has been done using WebXR. For more information... [WebXR]( https://github.com/JG03dev/WebXR)

## Status

During the LauzHack is in development

## What's included


```text
agent-src/
│  ├── agent/
│  │    ├── image_prepos.py
│  │    ├── router.py
│  │    └── main.py
│  └── data-models/
│       ├── label_mapping.pkl
│       └── efficientnet_b7.onnx
├── models/
│    ├──efficient_net_b7.ipynb
│    ├──mobile_net.ipynb
│    └──yolov8.ipynb
├── assets/
├── examples/
├── .env.example
├── requirements.txt
```

## Bugs and feature requests

Have a bug or a feature request? Please first read the [issue guidelines](https://reponame/blob/master/CONTRIBUTING.md) and search for existing and closed issues. If your problem or idea is not addressed yet, [please open a new issue](https://reponame/issues/new).


## Creators

 **Gabriel Juan**
  - GitHub: [@GabrielJuan349](https://github.com/GabrielJuan349)
  - LinkedIn: [in/gabi-juan](https://www.linkedin.com/in/gabi-juan)

**Jan Gras**
  - GitHub: [@JG03dev](https://github.com/JG03dev)
  - LinkedIn: [in/jangras](https://www.linkedin.com/in/jangras/)

**Yeray Cordero**
  - GitHub: [@yeray142](https://github.com/yeray142)
  - LinkedIn: [in/yeray142](https://www.linkedin.com/in/yeray142/)

**Nikalas Boyanov**
  - GitHub: [@finnithegamer](https://github.com/finnithegamer)
  - LinkedIn: [in/nikalas-boyanov-nunev](https://www.linkedin.com/in/nikalas-boyanov-nunev)

## Copyright and license

Code and documentation copyright 2024-2036 the authors. Code released under the [MIT License](https://reponame/blob/master/LICENSE).

Enjoy :metal:
