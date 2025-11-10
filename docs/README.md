# 📚 Documentation & Assets

This folder contains documentation, diagrams, and generated visualizations for the Fuzzy Traffic Light Control System.

## 📊 Generated Visualizations

### Membership Functions

![Membership Functions](membership_functions.png)

**File:** `membership_functions.png`

This visualization shows the fuzzy membership functions used in the traffic control system.

#### 📈 Biểu Đồ Hàm Thuộc (Membership Functions)

**1. Vehicle Density Membership Functions (Hàm thuộc mật độ xe - trên bên trái)**

Biểu đồ này mô tả cách hệ thống phân loại mật độ xe cộ thành 3 mức:

- **Low (Thấp - màu xanh dương)**: Từ 0-40 xe
  - Độ thuộc = 1.0 khi có 0 xe
  - Giảm dần xuống 0 khi đạt 40 xe
  - Đại diện cho tình trạng giao thông thưa thớt

- **Medium (Trung bình - màu cam)**: Từ 20-60 xe
  - Đỉnh độ thuộc = 1.0 tại 40 xe
  - Hình tam giác với overlap ở hai đầu
  - Đại diện cho lưu lượng giao thông bình thường

- **High (Cao - màu xanh lá)**: Từ 40-100 xe
  - Độ thuộc = 0 khi có 40 xe
  - Tăng dần lên 1.0 khi đạt 100 xe
  - Đại diện cho tình trạng ùn tắc

**Overlap Design:** Các vùng overlap (20-40 và 40-60 xe) cho phép hệ thống xử lý mượt mà các trường hợp biên giới giữa các mức.

**2. Waiting Time Membership Functions (Hàm thuộc thời gian chờ - trên bên phải)**

Biểu đồ này phân loại thời gian chờ thành 4 mức chi tiết hơn:

- **Short (Ngắn - màu xanh dương)**: 0-100 giây
  - Thời gian chờ chấp nhận được
  - Độ thuộc giảm dần từ 1.0 xuống 0

- **Medium (Trung bình - màu cam)**: 50-150 giây
  - Đỉnh tại 100 giây
  - Thời gian chờ bắt đầu gây khó chịu

- **Long (Dài - màu xanh lá)**: 100-250 giây
  - Đỉnh tại 200 giây
  - Cần ưu tiên xử lý

- **Very Long (Rất dài - màu đỏ)**: 200-300 giây
  - Tăng từ 0 lên 1.0
  - Tình trạng khẩn cấp, cần can thiệp ngay

**Thiết kế 4 mức:** Cho phép hệ thống ưu tiên các hướng có thời gian chờ quá lâu để tránh "starvation" (xe chờ mãi không được đi).

**3. Green Light Duration Membership Functions (Hàm thuộc thời lượng đèn xanh - dưới bên trái)**

Biểu đồ này định nghĩa thời gian đèn xanh output thành 4 mức:

- **Short (Ngắn - màu xanh dương)**: 10-30 giây
  - Độ thuộc = 1.0 tại 10 giây
  - Dùng khi mật độ thấp hoặc cần cân bằng giữa các hướng

- **Medium (Trung bình - màu cam)**: 20-50 giây
  - Đỉnh tại 40 giây
  - Thời gian mặc định cho lưu lượng bình thường

- **Long (Dài - màu xanh lá)**: 40-70 giây
  - Đỉnh tại 60 giây
  - Dùng khi mật độ cao ở một hướng

- **Very Long (Rất dài - màu đỏ)**: 60-90 giây
  - Độ thuộc tăng dần lên 1.0
  - Dùng cho tình trạng ùn tắc nghiêm trọng hoặc thời gian chờ quá lâu

**Range Design (10-90s):** Đủ linh hoạt để xử lý từ giao thông thưa (10s) đến ùn tắc (90s), đồng thời tránh thời gian đèn xanh quá ngắn (gây nguy hiểm) hoặc quá dài (gây bất công).

#### 🔍 Phân Tích Thiết Kế Hệ Thống

**Ưu điểm của thiết kế này:**

1. **Smooth Transitions (Chuyển đổi mượt mà):**
   - Các hàm overlap nhau tạo ra chuyển đổi mềm mại
   - Tránh thay đổi đột ngột trong điều khiển
   - Hệ thống phản ứng tự nhiên với thay đổi giao thông

2. **Asymmetric Ranges (Phạm vi bất đối xứng):**
   - Input có phạm vi rộng (0-100 xe, 0-300s)
   - Output bị giới hạn hẹp hơn (10-90s)
   - Thiết kế an toàn, tránh thời gian đèn quá cực đoan

3. **4-Level Granularity for Critical Variables:**
   - Waiting time có 4 mức thay vì 3
   - Cho phép logic ưu tiên tinh tế hơn
   - Cải thiện fairness (công bằng giữa các hướng)

4. **Mamdani Inference Compatibility:**
   - Các hàm tam giác/trapezoid chuẩn
   - Dễ tính toán centroid defuzzification
   - Hiệu suất tính toán tốt

**Cách hệ thống sử dụng:**

```
Input: 65 xe chờ ở hướng Bắc, thời gian chờ 180 giây

Bước 1 - Fuzzification:
- Density: 65 xe → Medium (0.5) + High (0.5)
- Waiting: 180s → Long (0.8) + Very_Long (0.2)

Bước 2 - Rule Activation:
- Rule: "IF density HIGH AND waiting LONG THEN green VERY_LONG"
- Activation strength = min(0.5, 0.8) = 0.5

Bước 3 - Defuzzification:
- Aggregate tất cả rules được kích hoạt
- Tính centroid → Output: ~75 giây đèn xanh
```

#### 📊 So Sánh Với Fixed-Time Controller

**Fixed-Time:** Luôn đèn xanh 30s mỗi hướng
- ❌ Không thích ứng với mật độ thực tế
- ❌ Lãng phí thời gian khi giao thông thưa
- ❌ Không đủ thời gian khi ùn tắc

**Fuzzy Controller:** Thời gian 10-90s tùy tình huống
- ✅ Ngắn (10-20s) khi ít xe → giảm chờ đợi không cần thiết
- ✅ Dài (70-90s) khi đông xe → tăng throughput
- ✅ Cân bằng (40-50s) khi cần fairness

**Kết quả thực tế:** Cải thiện 14-47% về thời gian chờ trung bình (xem README.md chính)

## 🔄 Regenerating Visualizations

To regenerate the membership functions diagram:

```bash
poetry shell
python src/fuzzy_controller/membership_functions.py
```

The image will be saved to `docs/membership_functions.png`.

## 📁 Future Assets

Additional documentation assets can be placed here:

- System architecture diagrams
- Performance comparison charts
- Rule activation visualizations
- Traffic flow animations
- Simulation screenshots

## 🎨 Image Formats

All visualizations are saved as PNG files with:

- Resolution: 300 DPI
- Format: RGB
- Dimensions: Optimized for documentation

---

*Generated by Fuzzy Traffic Light Control System*
*Author: Luân B*
