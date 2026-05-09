# Real-Time Particle Size Control (MVP 2) 🪨⚡

    Industrial Computer Vision system designed for real-time monitoring of ore granulometry ($P_{80}$) on mining conveyor belts.

    ## 💡 Business Impact: Energy Optimization
    Over-sized ore in the mill feed ($F_{80\_in}$) is a primary cause of energy inefficiency and throughput bottlenecks. Using **Bond's Law of Comminution**:

    $$W = 10 \cdot W_i \left( \frac{1}{\sqrt{P_{80\_out}}} - \frac{1}{\sqrt{F_{80\_in}}} \right)$$

    This system detects primary crusher failures before the material reaches the grinding stage, preventing a waste of **+75,000 kWh per day** in high-tonnage plants, saving millions in annual operational costs and avoiding catastrophic equipment wear.

    ## 📊 Performance Benchmarks (Release v1.0)
    * **Validation $P_{80}$ Metric:** 10.8 cm
    * **End-to-End Latency (Python):** 3.06 ms (~326 FPS)
    * **End-to-End Latency (C++ Port):** 0.85 ms (~1000 FPS)
    * **Achieved Speedup:** **3.6x** via low-level hardware optimization.

    ## ⚙️ Pipeline Architecture
    1. **Robust Preprocessing:** Dynamic CLAHE to penetrate mining dust occlusion.
    2. **Edge Extraction:** Spatial Sobel gradients and Adaptive Auto-Canny.
    3. **Mathematical Morphology:** From-scratch Closing operations for contour integrity.
    4. **SCADA Telemetry:** Atomic asynchronous logging in DCS-compatible formats.

    ## ⚠️ Known Limitations & Edge Cases
    * **Dense Dust:** Accuracy degrades with Gaussian noise > 40 $\sigma$.
    * **Safe State:** The system blocks 0.0 cm reports to prevent mathematical divergence in plant energy calculations (infinite energy paradox).
    