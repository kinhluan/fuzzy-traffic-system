# 📜 Scripts Directory

Thư mục này chứa các shell scripts để chạy các tác vụ phổ biến của dự án.

## 📋 Available Scripts

### 🔧 setup.sh

Cài đặt dependencies và chuẩn bị môi trường.

```bash
./scripts/setup.sh
```

**Thực hiện:**

- Kiểm tra Poetry đã cài đặt chưa
- Cài đặt tất cả dependencies
- Tạo virtual environment

---

### 🧪 test.sh

Chạy tất cả system tests.

```bash
./scripts/test.sh
```

**Thực hiện:**

- Chạy `test_system.py`
- Kiểm tra tất cả components
- Hiển thị kết quả test

---

### 🚀 run.sh

Chạy full simulation so sánh tất cả scenarios.

```bash
./scripts/run.sh
```

**Thực hiện:**

- Chạy `src/main.py`
- So sánh Fuzzy vs Fixed-Time controllers
- Tạo `web/data/comparison_results.json`
- **Thời gian:** ~5-10 phút

---

### ⚡ demo.sh

Chạy demo nhanh 2 phút.

```bash
./scripts/demo.sh
```

**Thực hiện:**

- Chạy `examples/simple_comparison.py`
- Demo nhanh với 1 scenario
- **Thời gian:** ~2 phút

---

### 🌐 serve.sh

Khởi động web server cho dashboard.

```bash
./scripts/serve.sh [PORT]
```

**Ví dụ:**

```bash
./scripts/serve.sh        # Default: port 8000
./scripts/serve.sh 3000   # Custom port
```

**Thực hiện:**

- Khởi động HTTP server
- Mở dashboard tại <http://localhost:8000>
- Press Ctrl+C để dừng

---

### 🎨 visualize.sh

Tạo visualization cho membership functions.

```bash
./scripts/visualize.sh
```

**Thực hiện:**

- Chạy `src/fuzzy_controller/membership_functions.py`
- Tạo `docs/membership_functions.png`

---

### 🧹 clean.sh

Xóa generated files và caches.

```bash
./scripts/clean.sh
```

**Thực hiện:**

- Xóa `__pycache__` folders
- Xóa `.pyc`, `.pyo` files
- Xóa `.pytest_cache`

---

## 🔐 Making Scripts Executable

Nếu scripts không executable, chạy:

```bash
chmod +x scripts/*.sh
```

---

## 📖 Usage Workflow

### Lần đầu tiên sử dụng

```bash
# 1. Setup
./scripts/setup.sh

# 2. Activate environment
poetry shell

# 3. Run tests
./scripts/test.sh

# 4. Run quick demo
./scripts/demo.sh

# 5. View dashboard
./scripts/serve.sh
```

### Chạy full simulation

```bash
# Activate environment
poetry shell

# Run full comparison
./scripts/run.sh

# View results
./scripts/serve.sh
```

### Development workflow

```bash
# Generate visualizations
./scripts/visualize.sh

# Test changes
./scripts/test.sh

# Clean caches
./scripts/clean.sh
```

---

## 🛠️ Troubleshooting

### Permission Denied

```bash
chmod +x scripts/*.sh
```

### Poetry not found

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -
```

### Scripts not working in Windows

Dùng Git Bash hoặc WSL, hoặc chạy trực tiếp:

```bash
poetry run python test_system.py
poetry run python src/main.py
```

---

**Author:** Luân B
