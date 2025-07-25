# Raspberry Pi Lane Tracking Robot Car

This project showcases the development of an autonomous lane-tracking robot car. Powered by a **Raspberry Pi 3 B+**, this robot uses computer vision to navigate a track, providing a hands-on introduction to robotics and control theory.

---

## The Idea 💡

The goal was to create a simple and affordable robotics platform. The Raspberry Pi was the perfect brain for the project. It's powerful enough for real-time image processing with **OpenCV** and accessible for hobbyists. The concept was to use a webcam to see the road, process the image to find the lane and steer the motors to follow the desired path.

---

## The Build: Hardware & Software

### **Hardware Components:**
* **Raspberry Pi 3 Model B+**
* **L298N Motor Driver**: Dual H-bridge driver to control the speed and direction of the DC motors.
* **Four 6V DC motors + wheels**
* **USB Webcam**
* **9-10V Battery Pack**:
* **Jumper wires & custon 3D-printed chassis**

### **Software Stack:**
* **Python 3.10+**:
* **OpenCV**
* **uv Package Manager**: To ensure a fast, clean, and reproducible development environment, all dependencies (listed in `pyproject.toml`) are managed with a single command.

---

## v5 (Frame Threshold)

The initial camera-based version, **v5**, was built on a simple and intuitive principle: frame-threshold logic.

**How it works:** The camera captures the view ahead, and the software divides the frame into sections. If it detects more lane pixels in one of the sections, it interprets that as the car being off-center and steers it toward the other side.

**The Result:** The car made it through the track. But, the movement was choppy and inefficient. The car constantly overcorrected, zigzagging all the way through. This version served as a good proof-of-concept but highlighted the limitations of a purely reactive control system.

### **v5 Demo** (Click below to open video)

[![No PID](https://img.youtube.com/vi/7RflPm-o-J4/0.jpg)](https://www.youtube.com/watch?v=7RflPm-o-J4)

*As you can see in the demo, the threshold-based approach leads to jerky, inefficient movement. The next version fixes this*

---

## v6 (PID Control)

Version **v6** incorporates a **Proportional-Integral-Derivative (PID) controller**, a cornerstone of control systems engineering.

**How it works:** Instead of just reacting to the presence of lane lines, this version calculates the precise center of the lane (the "centroid"). This centroid position becomes the input for the PID controller, which continuously calculates the "error" between the car's current position and the desired center. It then adjusts the steering smoothly to minimize this error over time.

* **Proportional (P)**: Corrects for the current error.
* **Integral (I)**: Corrects for past, accumulated errors.
* **Derivative (D)**: Predicts future errors based on the rate of change.

**The Result:** The PID controller allows the car to make more gradual adjustments, resulting in a much smoother and more efficient path through the track

### **v6 Demo** (Click below to open video)

[![PID Controller](https://img.youtube.com/vi/XqOyrmPmw9Y/0.jpg)](https://www.youtube.com/watch?v=XqOyrmPmw9Y)

*This demo showcases the benefit of PID control. The car's movement is smooth and precise as it corrects for errors over time.*

---

## Get Started Yourself!

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/TechNotebookYT/Lane-Tracking-Robot-Car.git](https://github.com/TechNotebookYT/Lane-Tracking-Robot-Car.git)
    cd Lane-Tracking-Robot-Car
    ```
2.  **Install uv:** Follow the instructions at [astral.sh/uv](https://astral.sh/uv).

### Usage

* **To run the non-PID version:**
    ```bash
    cd v5-cv_NO_PID
    uv run python main.py
    ```
* **To run the PID version:**
    ```bash
    cd v6-PID
    uv run python main.py
    ```

---

## Screenshots

<p align="center">
  <img alt="Figure 1: Robot car setup" src="https://github.com/TechNotebookYT/Lane-Tracking-Robot-Car/raw/main/assets/car.jpg" width="45%">
  &nbsp; &nbsp; &nbsp; &nbsp;
  <img alt="Figure 2: Real-time lane overlay" src="https://github.com/TechNotebookYT/Lane-Tracking-Robot-Car/raw/main/assets/lane_overlay.png" width="45%">
</p>
<p align="center">
  <em>Figure 1: The robot car setup. &nbsp; &nbsp; &nbsp; &nbsp; Figure 2: The real-time lane overlay from the car's perspective.</em>
</p>

---

## Contact & Future Directions

Future improvements could include using more advanced path-planning algorithms, training a neural network for lane detection, or adding obstacle avoidance.

For questions or feedback, feel free to open an issue on GitHub or email me at [**technotebook@yahoo.com**](mailto:technotebook@yahoo.com).
