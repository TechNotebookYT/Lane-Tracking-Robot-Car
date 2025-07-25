# Raspberry Pi Lane Tracking Robot Car

## Table of Contents

* [Project Overview](#project-overview)
* [Features](#features)
* [Hardware Requirements](#hardware-requirements)
* [Software Requirements](#software-requirements)
* [Installation](#installation)
* [Usage](#usage)

  * [Non‑PID Version — v5](#non‑pid-version-ndash-v5)
  * [PID Version — v6](#pid-version-ndash-v6)
* [Demo Videos](#demo-videos)
* [Screenshots](#screenshots)
* [Project Structure](#project-structure)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

## Project Overview

A line‑tracking robot car powered by a Raspberry Pi 3 B+, L298N driver, and OpenCV.

* **v5 (Non‑PID)** uses simple frame‑threshold logic: if pixels appear on one side, the car steers to the other.
* **v6 (PID)** computes the lane centroid and feeds it through a PID controller for smoother tracking.

Dependencies are managed with the [Astral.sh uv tool](https://astral.sh/uv), giving you fast installs and reproducible environments.

## Features

* **Real‑time lane detection** via USB webcam + OpenCV
* **Two control modes**: threshold‑based (v5) and PID+centroid (v6)
* **L298N dual H‑bridge** for DC motor control
* **Light, battery‑powered chassis**
* **One‑command setup** with `uv sync` + `uv run`

## Hardware Requirements

* Raspberry Pi 3 Model B+
* L298N Motor Driver
* Two 6 V DC motors + wheels
* USB webcam (e.g. Logitech C270)
* 5–6 V battery pack
* Jumper wires & chassis

## Software Requirements

* Python 3.10+
* [uv package manager](https://astral.sh/uv)
* OpenCV (`uv add opencv-python`)
* Other deps in `pyproject.toml`

## Installation

```bash
# 1. Clone
git clone https://github.com/TechNotebookYT/Lane-Tracking-Robot-Car.git
cd Lane-Tracking-Robot-Car

# 2. Install uv (see https://astral.sh/uv) and sync dependencies
uv sync

# (Optional) Activate venv
source .venv/bin/activate
```

## Usage

### Non‑PID Version — v5

```bash
cd v5-cv_NO_PID
uv run python main.py
```

### PID Version — v6

```bash
cd v6-PID
uv run python main.py
```

> If you’re iterating and want to skip the auto‑sync step, append `--no-sync`:
>
> ```bash
> uv run --no-sync python main.py
> ```

## Demo Videos

* **v5 (Threshold‑based) Demo**\\

* **v6 (PID‑based) Demo**\\

*Replace **`YOUR_V5_VIDEO_ID`** & **`YOUR_V6_VIDEO_ID`** with your actual YouTube IDs.*

## Screenshots


*Figure 1: Robot car setup*


*Figure 2: Real‑time lane overlay*

*Add more images under **`docs/images/`** as needed.*

## Contact

For questions or feedback, email me at [**technotebook@yahoo.com**](mailto:technotebook@yahoo.com)
(or open an issue on GitHub)
