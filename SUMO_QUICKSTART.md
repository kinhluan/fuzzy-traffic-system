# 🚦 SUMO Quick Start Guide

Chạy fuzzy traffic controller với SUMO trong 5 phút.

---

## 📦 Cài đặt

### 1. Cài SUMO

**macOS:**
```bash
brew install sumo
```

**Ubuntu:**
```bash
sudo apt install sumo sumo-tools
```

**Windows:** Tải từ https://sumo.dlr.de/docs/Downloads.php

### 2. Cài Python packages

```bash
pip install traci numpy scikit-fuzzy
```

### 3. Set SUMO_HOME (nếu cần)

```bash
export SUMO_HOME="/usr/local/share/sumo"
```

---

## 🚀 Chạy Demo (2 bước)

### Bước 1: Tạo SUMO network

```bash
./scripts/sumo_setup.sh
```

### Bước 2: Chạy demo

```bash
./scripts/sumo_run.sh
```

Xong! SUMO-GUI sẽ mở và hiển thị giao lộ với fuzzy controller.

---

## 📝 Scripts Khác

**Chạy SUMO-GUI riêng (không có fuzzy controller):**
```bash
./scripts/sumo_gui.sh
```

**Chạy headless (không có GUI, nhanh hơn):**
```bash
./scripts/sumo_headless.sh
```

---

## 📊 Kết Quả

Sau khi chạy, bạn sẽ thấy:

**Console output:**
```
Time(s) | Phase       | N-Density | S-Density | E-Density | W-Density | Green(s)
     0  | north_south |         5 |         4 |         3 |         6 |    45.2
    10  | east_west   |         7 |         6 |         8 |         5 |    52.1
```

**Final metrics:**
```
Avg Waiting Time:     18.25 seconds
Avg Queue Length:     5.67 vehicles
Throughput:           2670.00 vehicles/hour
Fairness Index:       0.9234
```

---

## 🎮 SUMO-GUI Controls

| Phím | Chức năng |
|------|-----------|
| **Space** | Pause/Resume |
| **Mouse Wheel** | Zoom |
| **Right-drag** | Pan |
| **Ctrl + A** | Fit view |

---

## ❓ Troubleshooting

**Lỗi: "SUMO_HOME not set"**
```bash
export SUMO_HOME="/usr/local/share/sumo"
```

**Lỗi: "TraCI not installed"**
```bash
pip install traci
```

**Lỗi: "network file not found"**
- Chạy lại: `./scripts/sumo_setup.sh`

**Không có xe trong SUMO**
- Test thủ công: `./scripts/sumo_gui.sh`

---

## 📚 Tài Liệu Khác

- Chi tiết đầy đủ: `docs/SUMO_INTEGRATION.md`
- Web Dashboard: `WEB_DASHBOARD_GUIDE.md`
- SUMO Docs: https://sumo.dlr.de/docs/

---

**Version:** 1.0 | **Author:** Luân B
