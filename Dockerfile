# ==========================================
# STAGE 1: BUILDER (C++)
# ==========================================
FROM ubuntu:22.04 AS builder

# Avoid apt interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install heavy toolchain
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY CMakeLists.txt .
COPY src/cpp/ src/cpp/

# Compile C++
RUN mkdir build && cd build && cmake .. && make hot_path

# ==========================================
# STAGE 2: RUNTIME C++ (PRODUCTION SLIM)
# ==========================================
# LEVEL 2 - DESIGN GAP
FROM ubuntu:22.04 AS cpp_prod

ENV DEBIAN_FRONTEND=noninteractive

# Install ONLY the runtime (no -dev, no gcc, no cmake)
RUN apt-get update && apt-get install -y \
    libopencv-core4.5d \
    libopencv-imgproc4.5d \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# LEVEL 1 - MECHANICAL GAP
COPY --from=builder /app/build/hot_path /app/hot_path

# LEVEL 3 - EDGE CASE GAP
CMD ["./hot_path"]

# ==========================================
# STAGE 3: RUNTIME PYTHON (PROTOTYPE / UI)
# ==========================================
FROM python:3.9-slim AS python_dev

WORKDIR /app

# OpenCV in Python requires libgl1
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY main.py .

CMD ["python", "main.py"]