# QUY TRÌNH LÀM THỰC NGHIỆM AI CHUYÊN NGHIỆP

## 1. Thực nghiệm AI chuyên nghiệp là gì?

Một thực nghiệm AI không chỉ là:

> Chạy mô hình → lấy accuracy cao nhất → đưa vào báo cáo.

Một thực nghiệm khoa học phải cho phép trả lời rõ ràng:

1. Ta đang kiểm chứng giả thuyết nào?
2. Biến nào được thay đổi?
3. Những yếu tố nào được giữ cố định?
4. Kết quả có tốt hơn baseline một cách đáng tin cậy không?
5. Kết quả thay đổi bao nhiêu giữa các lần chạy?
6. Người khác có thể tái tạo kết quả bằng code, dữ liệu và hướng dẫn được cung cấp không?

Theo ACM, cần phân biệt:

- **Repeatability**: cùng nhóm nghiên cứu, cùng thiết lập, chạy lại và thu được kết quả tương tự.
- **Reproducibility**: nhóm khác sử dụng artifact của tác giả và thu được kết quả tương tự.
- **Replicability**: nhóm khác tự xây dựng lại hệ thống bằng thiết lập riêng nhưng vẫn xác nhận được kết luận khoa học.

Artifact có thể bao gồm source code, script chạy thí nghiệm, dữ liệu đầu vào, dữ liệu thô, checkpoint, log và script phân tích kết quả.

Một nguyên tắc thực hành quan trọng là:

> **Một kết quả phải truy ngược được về đúng phiên bản code, dữ liệu, cấu hình, môi trường và tài nguyên tính toán đã tạo ra nó.**

Có thể biểu diễn một experimental run như sau:

```text
Run
├── research_question
├── hypothesis
├── code_commit
├── data_version
├── configuration
├── random_seed
├── environment
├── hardware
├── metrics
├── logs
├── checkpoint
└── generated_artifacts
```

NeurIPS yêu cầu tác giả mô tả đủ chi tiết để người đọc hiểu cách tái tạo kết quả, bao gồm data split, hyperparameter, cách chọn hyperparameter, lệnh chạy, môi trường và tài nguyên tính toán.

---

# 2. Tổng quan quy trình

Một quy trình thực nghiệm AI có thể được chia thành 13 giai đoạn:

```text
Research question
        ↓
Hypothesis
        ↓
Experimental protocol
        ↓
Dataset audit and splitting
        ↓
Baseline implementation
        ↓
Reproducible environment
        ↓
Modular implementation
        ↓
Sanity checks
        ↓
Pilot experiment
        ↓
Main experiments
        ↓
Statistical analysis
        ↓
Ablation and error analysis
        ↓
Artifact packaging and reporting
```

Không nên bắt đầu bằng việc chỉnh model. Trước tiên phải xác định **câu hỏi khoa học và giao thức đánh giá**.

---

# 3. Giai đoạn 1 — Xác định câu hỏi nghiên cứu

Câu hỏi nghiên cứu phải cụ thể, có thể kiểm chứng và có khả năng bị bác bỏ.

## Câu hỏi chưa tốt

```text
Liệu Transformer có tốt không?
```

Câu hỏi này không xác định:

- Tốt trên bài toán nào?
- Tốt hơn phương pháp nào?
- Theo metric nào?
- Trong điều kiện tài nguyên nào?

## Câu hỏi tốt hơn

```text
Khi giữ nguyên dữ liệu huấn luyện, preprocessing và ngân sách tính toán,
mô hình Transformer có cải thiện Macro-F1 trên tập kiểm thử so với
BiLSTM hay không?
```

## Mẫu viết research question

```text
Trong điều kiện [điều kiện kiểm soát],
việc thay đổi [biến độc lập]
có làm thay đổi [biến phụ thuộc]
so với [baseline]
trên [dataset hoặc phân phối dữ liệu]
hay không?
```

## Ví dụ

```text
Khi sử dụng cùng dữ liệu, tokenizer, số epoch và chiến lược tối ưu,
việc bổ sung cross-modal attention có cải thiện Recall@10
so với late fusion trên benchmark video-text retrieval hay không?
```

---

# 4. Giai đoạn 2 — Xây dựng giả thuyết

Mỗi thực nghiệm chính nên gắn với một giả thuyết.

## Giả thuyết nghiên cứu

```text
Cross-modal attention giúp mô hình học được tương tác giữa frame và
văn bản tốt hơn late fusion, do đó làm tăng Recall@10.
```

## Giả thuyết không

```text
H0: Không có khác biệt đáng kể về Recall@10 giữa cross-modal attention
và late fusion trong giao thức đánh giá đã xác định.
```

## Biến trong thực nghiệm

| Thành phần          | Ví dụ                                              |
| ------------------- | -------------------------------------------------- |
| Biến độc lập        | Kiến trúc fusion                                   |
| Biến phụ thuộc      | Recall@1, Recall@5, Recall@10                      |
| Biến kiểm soát      | Dataset, split, seed, optimizer, epoch, batch size |
| Nguồn biến thiên    | Khởi tạo trọng số, data shuffle, augmentation      |
| Baseline            | Late fusion                                        |
| Phương pháp đề xuất | Cross-modal attention                              |

Việc xác định biến trước khi chạy giúp tránh tình trạng thay đổi đồng thời nhiều thành phần nhưng vẫn quy kết cải thiện cho một thành phần duy nhất.

---

# 5. Giai đoạn 3 — Viết experimental protocol trước khi code

Trước khi triển khai thí nghiệm chính, nên tạo một file:

```text
docs/experimental_protocol.md
```

Nội dung tối thiểu:

```markdown
# Experimental Protocol

## Research question

Cross-modal attention có cải thiện Recall@10 so với late fusion không?

## Primary hypothesis

Cross-modal attention cải thiện Recall@10.

## Primary metric

Recall@10.

## Secondary metrics

Recall@1, Recall@5, median rank, inference latency.

## Dataset

Dataset name and version.

## Data split

Train: ...
Validation: ...
Test: ...

## Baselines

1. Random retrieval
2. Late fusion
3. Published baseline

## Controlled variables

- Same training data
- Same backbone
- Same optimizer
- Same training budget
- Same evaluation code

## Hyperparameter search

- Search space: ...
- Number of trials: ...
- Selection metric: validation Recall@10

## Random seeds

17, 29, 43, 59, 71

## Stopping rule

Early stopping based on validation Recall@10 with patience = 5.

## Final evaluation

Test set is evaluated only after model and hyperparameters are frozen.

## Success criterion

Mean Recall@10 improves over the strongest baseline,
with uncertainty and per-seed results reported.
```

NeurIPS yêu cầu báo cáo data split, training detail, hyperparameter và cách chọn hyperparameter. Các nghiên cứu về reporting cũng chỉ ra rằng chỉ đưa ra điểm test cuối cùng là không đủ để so sánh công bằng, đặc biệt khi các phương pháp sử dụng ngân sách tuning khác nhau.

---

# 6. Giai đoạn 4 — Chọn baseline công bằng

Một thực nghiệm AI thường nên có ba loại baseline.

## 6.1. Baseline ngẫu nhiên hoặc đơn giản

Ví dụ:

- Random prediction.
- Majority class.
- Mean predictor.
- BM25 cho text retrieval.
- Nearest neighbor đơn giản.
- Linear classifier trên frozen embeddings.

scikit-learn khuyến nghị sử dụng `DummyClassifier` hoặc `DummyRegressor` như một sanity baseline để kiểm tra mô hình có thực sự học được điều gì tốt hơn quy tắc đơn giản hay không.

## 6.2. Baseline chuẩn trong lĩnh vực

Đây là phương pháp được cộng đồng sử dụng rộng rãi hoặc được bài báo trước sử dụng.

Khi tái hiện baseline từ bài báo:

```text
Baseline source:
Paper:
Code repository:
Commit:
Dataset version:
Configuration:
Any deviations from original setup:
```

## 6.3. Strong baseline

Strong baseline là phương pháp cạnh tranh gần nhất với đề xuất của bạn.

Không nên chỉ so sánh phương pháp mới với một baseline quá yếu.

## Nguyên tắc so sánh công bằng

Các phương pháp phải dùng cùng:

- Data split.
- Preprocessing.
- Evaluation code.
- Training budget, nếu có thể.
- Hyperparameter tuning budget.
- Hardware hoặc giới hạn compute tương đương.
- Tiêu chí early stopping.
- Metric definition.

Các hướng dẫn về benchmarking nhấn mạnh việc xác định rõ phạm vi benchmark, chọn phương pháp và dataset đại diện, đồng thời tránh thiết kế so sánh thiên vị cho phương pháp mới.

---

# 7. Giai đoạn 5 — Quản lý dữ liệu

## 7.1. Không sửa trực tiếp raw data

Cấu trúc nên có:

```text
data/
├── raw/
├── interim/
├── processed/
├── splits/
└── metadata/
```

Ý nghĩa:

- `raw/`: dữ liệu gốc, bất biến.
- `interim/`: dữ liệu trung gian.
- `processed/`: dữ liệu đã sẵn sàng cho model.
- `splits/`: ID hoặc manifest của train, validation và test.
- `metadata/`: nguồn, license, checksum, schema và thống kê.

Các hướng dẫn scientific computing khuyến nghị lưu dữ liệu thô, ghi lại toàn bộ bước xử lý và sử dụng script cho từng giai đoạn thay vì chỉnh dữ liệu thủ công. Việc giữ intermediate outputs cũng giúp chạy lại từng phần của pipeline dễ dàng hơn.

## 7.2. Mỗi dữ liệu cần có version

Ví dụ metadata:

```yaml
dataset:
  name: ai_challenge_video
  version: "2026-07-01"
  source: kaggle
  source_version: kaggle_current
  manifest_sha256: "..."
  preprocessing_version: "v3"
  split_version: "split_v2"
```

Không nên dùng tên như:

```text
data_final/
data_final_v2/
data_final_v2_really_final/
```

DVC cho phép liên kết phiên bản dữ liệu và model với Git commit, trong khi file lớn được lưu trên object storage hoặc remote storage. Điều này tạo ra một lịch sử chung cho code, data và model.

## 7.3. Khóa data split

Sau khi tạo split:

```text
splits/
├── train.jsonl
├── validation.jsonl
├── test.jsonl
└── split_metadata.yaml
```

`split_metadata.yaml`:

```yaml
split_id: split_v2
strategy: stratified_group_split
seed: 17
group_key: video_id
train_samples: 80000
validation_samples: 10000
test_samples: 10000
```

Với dữ liệu có quan hệ nhóm, chẳng hạn nhiều frame thuộc cùng video hoặc nhiều mẫu thuộc cùng bệnh nhân, không được để các mẫu cùng nhóm xuất hiện ở cả train và test.

scikit-learn lưu ý rằng giả định dữ liệu độc lập và đồng phân phối thường không hoàn toàn đúng trong thực tế; với dữ liệu có cấu trúc nhóm hoặc thời gian, nên sử dụng group-wise hoặc time-aware splitting.

## 7.4. Không để test set ảnh hưởng đến quá trình phát triển

Test set không được sử dụng để:

- Chọn kiến trúc.
- Chọn feature.
- Chọn checkpoint.
- Chọn threshold.
- Chọn hyperparameter.
- Quyết định dừng huấn luyện.
- Chọn augmentation.

scikit-learn cảnh báo rằng việc điều chỉnh mô hình dựa trên test set làm thông tin từ test “rò rỉ” vào model, khiến điểm số không còn phản ánh khả năng generalization. Test set nên được giữ lại cho đánh giá cuối cùng.

## 7.5. Tránh preprocessing leakage

Sai:

```python
scaler.fit(all_data)
train_data = scaler.transform(train_data)
test_data = scaler.transform(test_data)
```

Đúng:

```python
scaler.fit(train_data)
train_data = scaler.transform(train_data)
test_data = scaler.transform(test_data)
```

Mọi thao tác học tham số từ dữ liệu phải chỉ được fit trên training data:

- Standardization.
- Imputation.
- Feature selection.
- PCA.
- Vocabulary construction.
- Target encoding.
- Sampling hoặc oversampling.

scikit-learn khuyến nghị sử dụng `Pipeline` để giảm nguy cơ preprocessing không nhất quán và data leakage.

---

# 8. Giai đoạn 6 — Tạo môi trường tái lập

Mỗi dự án phải khai báo rõ:

- Phiên bản Python.
- Phiên bản framework.
- Phiên bản CUDA và cuDNN.
- Dependency.
- Hệ điều hành.
- GPU hoặc CPU.
- Driver, khi cần thiết.

Cấu trúc tối thiểu:

```text
pyproject.toml
requirements.lock
Dockerfile
```

`pyproject.toml` là file cấu hình chuẩn được các công cụ đóng gói Python và nhiều công cụ linting, type checking sử dụng. PyPA khuyến nghị khai báo build system và project metadata trong file này.

Ví dụ:

```toml
[build-system]
requires = ["hatchling>=1.26"]
build-backend = "hatchling.build"

[project]
name = "ai-research-project"
version = "0.1.0"
requires-python = ">=3.11,<3.13"
dependencies = [
    "numpy",
    "pandas",
    "scipy",
    "scikit-learn",
    "torch",
    "pyyaml",
    "mlflow"
]

[project.optional-dependencies]
dev = [
    "pytest",
    "ruff",
    "mypy"
]

[tool.ruff]
line-length = 100

[tool.pytest.ini_options]
testpaths = ["tests"]
```

Dependency dùng cho run chính nên được khóa phiên bản bằng lock file hoặc container image digest.

Ví dụ thông tin môi trường cần lưu:

```json
{
  "python": "3.11.x",
  "torch": "installed version",
  "cuda": "runtime version",
  "cudnn": "installed version",
  "platform": "Linux",
  "gpu": "GPU model",
  "git_commit": "commit hash"
}
```

---

# 9. Giai đoạn 7 — Cấu trúc project như scientific software

Một cấu trúc phù hợp:

```text
ai-research-project/
├── README.md
├── LICENSE
├── CITATION.cff
├── pyproject.toml
├── requirements.lock
├── Dockerfile
│
├── configs/
│   ├── base.yaml
│   ├── baseline.yaml
│   └── proposed_model.yaml
│
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   ├── splits/
│   └── metadata/
│
├── src/
│   └── project/
│       ├── __init__.py
│       ├── data.py
│       ├── models.py
│       ├── losses.py
│       ├── metrics.py
│       ├── training.py
│       ├── evaluation.py
│       ├── reproducibility.py
│       └── tracking.py
│
├── scripts/
│   ├── prepare_data.py
│   ├── train.py
│   ├── evaluate.py
│   ├── summarize_runs.py
│   └── reproduce_main_results.sh
│
├── tests/
│   ├── test_data.py
│   ├── test_metrics.py
│   └── test_model.py
│
├── notebooks/
│   ├── exploratory_analysis.ipynb
│   └── error_analysis.ipynb
│
├── artifacts/
│   ├── checkpoints/
│   ├── predictions/
│   └── logs/
│
└── reports/
    ├── figures/
    ├── tables/
    └── experiment_log.md
```

Bài báo về scientific computing của Wilson và cộng sự khuyến nghị tách source code vào `src`, data vào thư mục dữ liệu, kết quả sinh ra vào thư mục kết quả và có README, LICENSE, dependency cùng script điều khiển toàn bộ workflow.

## Vai trò của notebook

Notebook phù hợp cho:

- Khám phá dữ liệu.
- Visualize.
- Error analysis.
- Trình bày kết quả.

Logic tạo ra kết quả chính nên nằm trong module và script có thể chạy tự động.

Không nên để kết quả chính phụ thuộc vào việc:

```text
Run cell 3
Run cell 7
Sửa một biến trong cell 2
Run lại cell 9
```

---

# 10. Giai đoạn 8 — Configuration-driven experiments

Không nên thay đổi hyperparameter bằng cách sửa trực tiếp source code.

Sai:

```python
learning_rate = 0.0001  # sửa bằng tay mỗi lần chạy
batch_size = 64
```

Đúng:

```yaml
# configs/proposed_model.yaml

experiment:
  name: cross_modal_attention
  seed: 17
  deterministic: true

data:
  dataset_name: ai_challenge_video
  dataset_version: "2026-07-01"
  split_version: split_v2
  train_manifest: data/splits/train.jsonl
  validation_manifest: data/splits/validation.jsonl
  test_manifest: data/splits/test.jsonl

model:
  architecture: cross_modal_transformer
  hidden_dim: 512
  num_layers: 6
  dropout: 0.1

training:
  epochs: 30
  batch_size: 64
  learning_rate: 0.0001
  weight_decay: 0.01
  optimizer: adamw
  scheduler: cosine
  gradient_clip_norm: 1.0
  early_stopping_patience: 5

evaluation:
  primary_metric: recall_at_10
  metrics:
    - recall_at_1
    - recall_at_5
    - recall_at_10
    - median_rank
```

Lệnh chạy:

```bash
python scripts/train.py --config configs/proposed_model.yaml
```

Mỗi run nên sử dụng một config bất biến. Config phải được lưu cùng artifacts của run.

---

# 11. Giai đoạn 9 — Kiểm soát randomness

PyTorch cung cấp các cơ chế đặt random seed để tăng khả năng tái lập, nhưng seed không loại bỏ mọi nguồn nondeterminism. Một số thuật toán và môi trường phần cứng có thể vẫn sinh ra khác biệt.

## Mẫu utility

```python
# src/project/reproducibility.py

from __future__ import annotations

import hashlib
import json
import platform
import random
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np
import torch


def seed_everything(seed: int, deterministic: bool = False) -> None:
    """Seed common random number generators."""

    if seed < 0:
        raise ValueError("seed must be non-negative")

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    if deterministic:
        torch.use_deterministic_algorithms(True, warn_only=True)

        if torch.backends.cudnn.is_available():
            torch.backends.cudnn.benchmark = False


def get_git_commit() -> str:
    """Return the current Git commit, or 'unknown' outside a Git repository."""

    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "unknown"


def sha256_file(path: str | Path) -> str:
    """Calculate the SHA-256 checksum of a file."""

    file_path = Path(path)

    if not file_path.is_file():
        raise FileNotFoundError(file_path)

    digest = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def environment_metadata() -> dict[str, Any]:
    """Collect environment metadata needed to investigate a run."""

    return {
        "python": sys.version,
        "platform": platform.platform(),
        "torch": torch.__version__,
        "cuda_runtime": torch.version.cuda,
        "cudnn": torch.backends.cudnn.version(),
        "cuda_available": torch.cuda.is_available(),
        "git_commit": get_git_commit(),
    }


def save_json(data: dict[str, Any], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
```

Ngoài việc đặt seed, cần báo cáo **kết quả trên nhiều seed** để đo độ ổn định của phương pháp.

Ví dụ:

```yaml
seeds:
  - 17
  - 29
  - 43
  - 59
  - 71
```

---

# 12. Giai đoạn 10 — Viết code theo module

Các hàm nên:

- Có một trách nhiệm chính.
- Có input và output rõ ràng.
- Không phụ thuộc quá nhiều vào global state.
- Có tên mô tả đúng chức năng.
- Có assertion hoặc validation cho giả định quan trọng.
- Có unit test cho metric, split và preprocessing.

Scientific computing guidelines khuyến nghị chia chương trình thành các hàm ngắn, loại bỏ code lặp, đặt tên có ý nghĩa, khai báo dependency rõ ràng và cung cấp test hoặc dữ liệu ví dụ.

## Ví dụ Dataset validation

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class Sample:
    sample_id: str
    feature_path: str
    label: int


def validate_samples(samples: list[Sample]) -> None:
    if not samples:
        raise ValueError("Dataset is empty")

    sample_ids = [sample.sample_id for sample in samples]

    if len(sample_ids) != len(set(sample_ids)):
        raise ValueError("Duplicate sample_id detected")

    labels = [sample.label for sample in samples]

    if any(label < 0 for label in labels):
        raise ValueError("Labels must be non-negative")
```

## Kiểm tra split leakage

```python
def assert_disjoint_splits(
    train_ids: set[str],
    validation_ids: set[str],
    test_ids: set[str],
) -> None:
    if train_ids & validation_ids:
        raise ValueError("Train-validation leakage detected")

    if train_ids & test_ids:
        raise ValueError("Train-test leakage detected")

    if validation_ids & test_ids:
        raise ValueError("Validation-test leakage detected")
```

## Test metric

```python
import pytest

from project.metrics import accuracy


def test_accuracy_perfect_predictions() -> None:
    predictions = [0, 1, 2]
    targets = [0, 1, 2]

    assert accuracy(predictions, targets) == pytest.approx(1.0)


def test_accuracy_rejects_mismatched_lengths() -> None:
    with pytest.raises(ValueError):
        accuracy([0, 1], [0])
```

---

# 13. Giai đoạn 11 — Tracking từng experiment

Mỗi lần chạy cần lưu:

```text
Run ID
Start time
End time
Git commit
Data version
Configuration
Random seed
Training metrics
Validation metrics
Test metrics
Hardware
Runtime
Checkpoint
Predictions
Logs
Figures
```

MLflow Tracking được thiết kế để ghi lại parameters, code version, metrics và output artifacts của từng run. Một experiment có thể nhóm nhiều run của cùng một bài toán.

## Hàm flatten config

```python
from collections.abc import Mapping
from typing import Any


def flatten_dict(
    data: Mapping[str, Any],
    parent_key: str = "",
    separator: str = ".",
) -> dict[str, Any]:
    output: dict[str, Any] = {}

    for key, value in data.items():
        full_key = f"{parent_key}{separator}{key}" if parent_key else key

        if isinstance(value, Mapping):
            output.update(flatten_dict(value, full_key, separator))
        else:
            output[full_key] = value

    return output
```

## Skeleton cho một experimental run

```python
# scripts/train.py

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import mlflow
import yaml

from project.data import build_dataloaders
from project.models import build_model
from project.reproducibility import (
    environment_metadata,
    seed_everything,
)
from project.tracking import flatten_dict
from project.training import train_model


def load_config(path: str | Path) -> dict[str, Any]:
    config_path = Path(path)

    if not config_path.is_file():
        raise FileNotFoundError(config_path)

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("Configuration must be a mapping")

    return config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--seed", type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    if args.seed is not None:
        config["experiment"]["seed"] = args.seed

    seed = int(config["experiment"]["seed"])
    deterministic = bool(config["experiment"].get("deterministic", False))

    seed_everything(seed, deterministic)

    experiment_name = config["experiment"]["name"]
    run_name = f"{experiment_name}-seed-{seed}"

    mlflow.set_experiment(experiment_name)

    with mlflow.start_run(run_name=run_name):
        mlflow.log_params(flatten_dict(config))

        metadata = environment_metadata()

        for key, value in metadata.items():
            mlflow.set_tag(key, str(value))

        config_artifact = Path("artifacts/current_run/config.json")
        config_artifact.parent.mkdir(parents=True, exist_ok=True)
        config_artifact.write_text(
            json.dumps(config, indent=2),
            encoding="utf-8",
        )
        mlflow.log_artifact(str(config_artifact))

        dataloaders = build_dataloaders(config["data"])
        model = build_model(config["model"])

        results = train_model(
            model=model,
            dataloaders=dataloaders,
            training_config=config["training"],
            evaluation_config=config["evaluation"],
        )

        for metric_name, metric_value in results["final_metrics"].items():
            mlflow.log_metric(metric_name, float(metric_value))

        mlflow.log_artifact(results["checkpoint_path"])
        mlflow.log_artifact(results["prediction_path"])


if __name__ == "__main__":
    main()
```

Điểm quan trọng của skeleton này:

- Config được lưu lại.
- Seed được lưu trong tên run.
- Git commit và environment được ghi nhận.
- Metric không được copy thủ công từ terminal.
- Checkpoint và prediction được lưu như artifacts.
- Một run thất bại vẫn có log để điều tra.

---

# 14. Giai đoạn 12 — Sanity check trước khi chạy lớn

Trước khi dùng nhiều GPU hoặc chạy nhiều giờ, thực hiện các kiểm tra nhỏ.

## 14.1. Overfit một batch nhỏ

Mô hình phải có khả năng giảm loss rất thấp trên một batch nhỏ.

Nếu không thể overfit một batch, có thể tồn tại lỗi trong:

- Loss.
- Label.
- Forward pass.
- Gradient.
- Data preprocessing.
- Metric.
- Optimizer.

## 14.2. Kiểm tra gradient

```python
def assert_gradients_exist(model) -> None:
    missing = [
        name
        for name, parameter in model.named_parameters()
        if parameter.requires_grad and parameter.grad is None
    ]

    if missing:
        raise RuntimeError(f"Missing gradients: {missing}")
```

## 14.3. Kiểm tra output shape

```python
logits = model(batch_inputs)

assert logits.ndim == 2
assert logits.shape[0] == batch_labels.shape[0]
assert logits.shape[1] == number_of_classes
```

## 14.4. Kiểm tra baseline ngẫu nhiên

Mô hình chưa train không nên đạt kết quả cao bất thường.

Kết quả quá cao trước training có thể là dấu hiệu:

- Label leakage.
- Duplicate samples.
- Test contamination.
- Metric implementation sai.
- Dữ liệu được sắp theo label.

## 14.5. Kiểm tra pipeline bằng dữ liệu nhỏ

Chạy toàn bộ pipeline trên một subset:

```bash
python scripts/train.py \
    --config configs/debug.yaml
```

`debug.yaml`:

```yaml
experiment:
  name: debug_run
  seed: 17
  deterministic: true

data:
  max_train_samples: 128
  max_validation_samples: 64

training:
  epochs: 2
  batch_size: 8
```

---

# 15. Giai đoạn 13 — Pilot experiment

Pilot experiment nhằm kiểm tra:

- Pipeline có chạy từ đầu đến cuối không?
- Loss có giảm không?
- Metric có hợp lý không?
- Memory có đủ không?
- Runtime dự kiến là bao nhiêu?
- Checkpoint có load lại được không?
- Run có được tracking đầy đủ không?

Pilot không dùng để đưa ra kết luận khoa học cuối cùng.

Sau pilot, có thể sửa lỗi triển khai. Tuy nhiên, khi bắt đầu main experiment, nên khóa:

```text
Evaluation code
Test split
Primary metric
Baseline definition
Search space
Search budget
Stopping rule
```

---

# 16. Chạy main experiments

## 16.1. Một seed không đủ để kết luận

Một kết quả duy nhất có thể phụ thuộc vào:

- Weight initialization.
- Data order.
- Augmentation.
- Sampling.
- Dropout.
- Non-deterministic GPU operations.

Nên chạy nhiều seed và giữ nguyên các yếu tố còn lại.

```bash
for seed in 17 29 43 59 71
do
    python scripts/train.py \
        --config configs/proposed_model.yaml \
        --seed "$seed"
done
```

Thực hiện tương tự cho baseline:

```bash
for seed in 17 29 43 59 71
do
    python scripts/train.py \
        --config configs/baseline.yaml \
        --seed "$seed"
done
```

Phải dùng cùng danh sách seed khi điều kiện cho phép.

## 16.2. Không chỉ lưu best run

Phải giữ lại:

- Tất cả seed.
- Tất cả kết quả hợp lệ.
- Run bị lỗi.
- Run bị loại và lý do loại.
- Hyperparameter trials.
- Thời gian và compute của từng trial.

Không được chỉ chọn seed tốt nhất rồi trình bày như kết quả đại diện.

## 16.3. Báo cáo ngân sách tuning

Ví dụ:

```text
Baseline:
- 20 hyperparameter trials
- 2 GPU-hours per trial

Proposed method:
- 20 hyperparameter trials
- 2 GPU-hours per trial
```

Nếu ngân sách khác nhau, phải công khai sự khác biệt.

NeurIPS yêu cầu báo cáo loại compute worker, memory, runtime cho từng run và ước tính tổng compute của dự án, bao gồm cả thí nghiệm sơ bộ hoặc thất bại khi phù hợp.

---

# 17. Phân tích thống kê

NeurIPS khuyến nghị các kết quả hỗ trợ kết luận chính phải có error bar, confidence interval hoặc kiểm định thống kê phù hợp. Tác giả phải nói rõ error bar biểu diễn nguồn biến thiên nào, được tính bằng phương pháp gì và là standard deviation hay standard error.

## 17.1. Không chỉ báo cáo mean

Nên báo cáo:

```text
Mean
Standard deviation
Number of runs
Per-seed values
Confidence interval, khi phù hợp
```

Ví dụ:

```text
Recall@10 = 72.4 ± 0.8
mean ± standard deviation over 5 random seeds
```

Không được viết:

```text
Recall@10 = 72.4 ± 0.8
```

mà không giải thích `±` là gì.

## 17.2. Hàm tổng hợp kết quả

```python
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats


@dataclass(frozen=True)
class MetricSummary:
    count: int
    mean: float
    standard_deviation: float
    confidence_interval_low: float
    confidence_interval_high: float


def summarize_metric(
    values: list[float],
    confidence: float = 0.95,
) -> MetricSummary:
    array = np.asarray(values, dtype=float)

    if array.ndim != 1:
        raise ValueError("values must be one-dimensional")

    if len(array) < 2:
        raise ValueError("At least two observations are required")

    mean = float(array.mean())
    standard_deviation = float(array.std(ddof=1))
    standard_error = standard_deviation / np.sqrt(len(array))

    critical_value = stats.t.ppf(
        (1.0 + confidence) / 2.0,
        df=len(array) - 1,
    )

    margin = float(critical_value * standard_error)

    return MetricSummary(
        count=len(array),
        mean=mean,
        standard_deviation=standard_deviation,
        confidence_interval_low=mean - margin,
        confidence_interval_high=mean + margin,
    )
```

Việc dùng t-interval ở trên giả định các quan sát độc lập và phân phối của trung bình phù hợp với phương pháp. Với phân phối bất đối xứng hoặc metric bị giới hạn, có thể cần bootstrap hoặc phương pháp khác. Phương pháp và giả định phải được ghi rõ.

## 17.3. Báo cáo per-seed

| Method   | Seed 17 | Seed 29 | Seed 43 | Seed 59 | Seed 71 |    Mean ± SD |
| -------- | ------: | ------: | ------: | ------: | ------: | -----------: |
| Baseline |    68.1 |    68.7 |    67.9 |    68.4 |    68.3 | 68.28 ± 0.30 |
| Proposed |    71.9 |    72.7 |    72.1 |    73.0 |    72.3 | 72.40 ± 0.45 |

Per-seed values giúp phát hiện:

- Outlier.
- Seed không ổn định.
- Một phương pháp chỉ thắng ở một số run.
- Lỗi thu thập kết quả.

---

# 18. Hyperparameter tuning đúng cách

Hyperparameter phải được chọn bằng validation set hoặc cross-validation, không chọn bằng test set.

scikit-learn khuyến nghị giữ test set cho đánh giá cuối cùng và sử dụng validation hoặc cross-validation cho model selection.

## Quy trình

```text
Training data
    ↓
Train candidate configurations
    ↓
Validation evaluation
    ↓
Select configuration
    ↓
Freeze model and configuration
    ↓
Evaluate once on test
```

## Search space phải được công bố

```yaml
search_space:
  learning_rate:
    type: log_uniform
    low: 0.00001
    high: 0.001

  weight_decay:
    values:
      - 0.0
      - 0.001
      - 0.01

  dropout:
    values:
      - 0.0
      - 0.1
      - 0.2
```

Cần lưu:

- Search algorithm.
- Search space.
- Number of trials.
- Seed của sampler.
- Metric dùng để chọn.
- Trial bị lỗi.
- Best validation configuration.
- Tổng compute.

---

# 19. Ablation study

Ablation trả lời:

> Thành phần nào thực sự tạo ra cải thiện?

Ví dụ mô hình đầy đủ:

```text
Backbone
+ Temporal encoder
+ Cross-modal attention
+ Contrastive loss
+ Hard negative mining
```

Bảng ablation:

| Temporal encoder | Cross-modal attention | Hard negatives | Recall@10 |
| ---------------- | --------------------- | -------------- | --------: |
| Không            | Không                 | Không          |      65.1 |
| Có               | Không                 | Không          |      68.4 |
| Có               | Có                    | Không          |      71.2 |
| Có               | Có                    | Có             |      72.4 |

## Nguyên tắc

Mỗi ablation chỉ nên thay đổi một thành phần chính trong một lần so sánh, trừ khi mục tiêu là kiểm tra interaction giữa nhiều thành phần.

Các ablation phải dùng:

- Cùng split.
- Cùng evaluation.
- Cùng seed hoặc tập seed.
- Cùng training budget.
- Cùng selection rule.

---

# 20. Error analysis

Metric tổng hợp không giải thích tại sao mô hình đúng hoặc sai.

Error analysis nên phân loại lỗi theo:

- Class.
- Độ dài input.
- Chất lượng hình ảnh.
- Loại video.
- Ngôn ngữ.
- Mức độ nhiễu.
- Rare hoặc frequent categories.
- In-distribution và out-of-distribution.
- False positive và false negative.

Ví dụ lưu predictions:

```json
{
  "sample_id": "video_001",
  "target": 4,
  "prediction": 7,
  "confidence": 0.83,
  "split": "test",
  "checkpoint": "run_20260703_seed17"
}
```

Prediction file nên được sinh tự động và liên kết với run đã tạo ra nó.

---

# 21. Lưu checkpoint đúng cách

Không nên chỉ lưu `model.state_dict()` mà không có metadata.

```python
from pathlib import Path
from typing import Any

import torch


def save_checkpoint(
    output_path: str | Path,
    *,
    model: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    epoch: int,
    config: dict[str, Any],
    metrics: dict[str, float],
    git_commit: str,
    data_version: str,
) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    checkpoint = {
        "epoch": epoch,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "config": config,
        "metrics": metrics,
        "git_commit": git_commit,
        "data_version": data_version,
    }

    torch.save(checkpoint, path)
```

Checkpoint cần trả lời được:

```text
Model này được train bằng code nào?
Dữ liệu nào?
Config nào?
Seed nào?
Đạt metric nào?
Ở epoch nào?
```

---

# 22. Experiment log

Ngoài hệ thống tracking, nên duy trì một research log.

```markdown
# Experiment EXP-024

## Date

2026-07-03

## Question

Hard-negative mining có cải thiện Recall@10 không?

## Change

Bổ sung in-batch hard-negative mining.

## Constant settings

- Dataset: video_dataset_v3
- Split: split_v2
- Backbone: ViT-B/16
- Seeds: 17, 29, 43, 59, 71

## Expected result

Recall@10 tăng nhưng training có thể không ổn định hơn.

## Results

Baseline: 71.2 ± 0.4
Proposed: 72.4 ± 0.5

## Observation

Cải thiện chủ yếu xuất hiện ở các query có nhiều video tương tự.

## Decision

Giữ hard-negative mining cho mô hình chính.

## Follow-up

Phân tích theo negative-set difficulty.
```

Research log cần ghi cả kết quả không thành công. Thí nghiệm thất bại vẫn cung cấp thông tin khoa học và ngăn việc lặp lại cùng một hướng không hiệu quả.

---

# 23. Tái tạo kết quả bằng một lệnh

Một artifact tốt nên có lệnh rõ ràng như:

```bash
bash scripts/reproduce_main_results.sh
```

Ví dụ:

```bash
#!/usr/bin/env bash

set -euo pipefail

python scripts/prepare_data.py \
    --config configs/data.yaml

for seed in 17 29 43 59 71
do
    python scripts/train.py \
        --config configs/baseline.yaml \
        --seed "$seed"

    python scripts/train.py \
        --config configs/proposed_model.yaml \
        --seed "$seed"
done

python scripts/summarize_runs.py \
    --experiment baseline \
    --experiment proposed_model \
    --output reports/tables/main_results.csv

python scripts/generate_figures.py \
    --results reports/tables/main_results.csv \
    --output-dir reports/figures
```

NeurIPS checklist nói rằng hướng dẫn tái tạo nên chứa **lệnh chính xác và môi trường cần thiết** để chạy lại kết quả.

---

# 24. Báo cáo tài nguyên tính toán

Mỗi thí nghiệm chính nên ghi:

```yaml
compute:
  gpu_model: "GPU model"
  number_of_gpus: 1
  gpu_memory_gb: 24
  cpu_model: "CPU model"
  ram_gb: 64
  training_time_hours: 3.4
  inference_time_seconds: 120
  total_hyperparameter_trials: 20
```

Trong báo cáo:

```text
Mỗi run được huấn luyện trên một GPU với 24 GB bộ nhớ.
Thời gian trung bình cho một run là 3,4 giờ.
Mỗi phương pháp sử dụng 20 hyperparameter trials và 5 final-seed runs.
```

NeurIPS yêu cầu cung cấp đủ thông tin về CPU hoặc GPU, memory, storage, thời gian cho từng run và ước tính tổng compute.

---

# 25. Artifact cuối cùng cần công bố

Một research artifact hoàn chỉnh nên có:

```text
README.md
LICENSE
CITATION.cff
Environment specification
Source code
Data preparation scripts
Data split manifests
Configuration files
Training scripts
Evaluation scripts
Random seeds
Model checkpoints
Raw per-run metrics
Aggregated results
Prediction files
Figures and tables
Exact reproduction commands
Known limitations
```

ACM đánh giá artifact dựa trên các tiêu chí như:

- Được tài liệu hóa.
- Nhất quán với bài báo.
- Đủ thành phần cần thiết.
- Có thể thực thi.
- Có bằng chứng xác minh và validation.

NeurIPS cũng yêu cầu tác giả ghi rõ version và license của code, dữ liệu hoặc model được sử dụng, đồng thời trích dẫn người tạo ra asset gốc.

---

# 26. Checklist trước khi công bố kết quả

## Research design

- [ ] Câu hỏi nghiên cứu cụ thể.
- [ ] Giả thuyết được viết trước main experiment.
- [ ] Primary metric được xác định.
- [ ] Baseline phù hợp.
- [ ] Biến độc lập, phụ thuộc và kiểm soát rõ ràng.
- [ ] Search space và tuning budget được xác định.

## Data

- [ ] Raw data không bị chỉnh sửa.
- [ ] Dataset có version.
- [ ] Split có manifest và seed.
- [ ] Train, validation và test không chồng lấn.
- [ ] Không có group leakage.
- [ ] Preprocessing chỉ được fit trên training data.
- [ ] Test set không được dùng để chọn model.

## Code

- [ ] Logic chính nằm trong module hoặc script.
- [ ] Hyperparameter nằm trong config.
- [ ] Metric có unit test.
- [ ] Split có leakage test.
- [ ] Có debug configuration.
- [ ] Có một lệnh tái tạo kết quả.
- [ ] Dependency được khai báo rõ.
- [ ] Code được quản lý bằng version control.

## Experiment tracking

- [ ] Mỗi run có ID.
- [ ] Git commit được lưu.
- [ ] Data version được lưu.
- [ ] Config được lưu.
- [ ] Seed được lưu.
- [ ] Environment được lưu.
- [ ] Hardware và runtime được lưu.
- [ ] Checkpoint và prediction được lưu.
- [ ] Run thất bại không bị xóa khỏi lịch sử.

## Evaluation

- [ ] Chạy nhiều seed.
- [ ] Báo cáo per-seed values.
- [ ] Báo cáo mean và độ biến thiên.
- [ ] Giải thích error bar.
- [ ] Baseline và proposed method có cùng protocol.
- [ ] Có ablation study.
- [ ] Có error analysis.
- [ ] Không chỉ báo cáo best run.

## Reporting

- [ ] Có exact command.
- [ ] Có environment specification.
- [ ] Có data và model license.
- [ ] Có compute report.
- [ ] Có limitations.
- [ ] Có README.
- [ ] Có hướng dẫn tái tạo bảng và hình chính.

---

# 27. Những lỗi phổ biến cần tránh

## Chạy model trước, đặt câu hỏi sau

Hậu quả: dễ chọn giả thuyết phù hợp với kết quả đã thấy.

## Sửa code trực tiếp cho từng thí nghiệm

Hậu quả: không biết kết quả thuộc cấu hình nào.

## Dùng test set để tuning

Hậu quả: điểm test bị thiên lệch và không còn phản ánh generalization.

## Chỉ báo cáo seed tốt nhất

Hậu quả: phóng đại hiệu quả và che giấu instability.

## Baseline dùng ít tuning hơn phương pháp mới

Hậu quả: so sánh không công bằng.

## Chỉ lưu checkpoint

Hậu quả: không biết checkpoint được tạo bởi code, data và config nào.

## Copy metric thủ công vào bảng

Hậu quả: dễ copy nhầm, làm tròn không nhất quán hoặc dùng nhầm run.

## Toàn bộ code nằm trong một notebook

Hậu quả: khó chạy tự động, khó test và phụ thuộc vào thứ tự cell.

## Dùng tên file như `final_v5_really_final`

Hậu quả: không có lịch sử thay đổi đáng tin cậy.

## Không lưu kết quả thất bại

Hậu quả: không có audit trail và dễ lặp lại những thử nghiệm không hiệu quả.

---

# 28. Nguyên tắc “code như nhà khoa học”

Có thể tóm tắt thành mười nguyên tắc:

1. **Một experiment trả lời một câu hỏi rõ ràng.**
2. **Một lần so sánh chỉ thay đổi những biến đã được tuyên bố.**
3. **Một run phải có config bất biến.**
4. **Một kết quả phải truy ngược được về code, data và environment.**
5. **Test set phải được khóa cho đến đánh giá cuối cùng.**
6. **Mọi preprocessing có học tham số phải fit trên training data.**
7. **Kết quả phải được chạy trên nhiều nguồn randomness phù hợp.**
8. **Phải báo cáo độ biến thiên, không chỉ điểm tốt nhất.**
9. **Bảng và hình phải được sinh tự động từ raw results.**
10. **Người khác phải có con đường rõ ràng để tái tạo kết quả.**

---

# 29. Nguồn chính

1. NeurIPS, _Paper Checklist Guidelines_: hướng dẫn về reproducibility, experimental setting, thống kê, compute, license và artifact.

2. Pineau và cộng sự, _Improving Reproducibility in Machine Learning Research_, Journal of Machine Learning Research, 2021.

3. ACM, _Artifact Review and Badging_: định nghĩa repeatability, reproducibility, replicability và tiêu chuẩn artifact.

4. Wilson và cộng sự, _Good Enough Practices in Scientific Computing_, PLOS Computational Biology, 2017.

5. scikit-learn, _Common Pitfalls and Recommended Practices_: preprocessing consistency và data leakage.

6. scikit-learn, _Cross-validation: Evaluating Estimator Performance_: validation, test set, cross-validation và group-aware splitting.

7. MLflow, _ML Experiment Tracking_: tracking parameters, code versions, metrics và artifacts.

8. DVC, _Versioning Data and Models_: liên kết version của code, data và model.

9. PyTorch, _Reproducibility_: random seed và deterministic operations.

10. Weber và cộng sự, _Essential Guidelines for Computational Method Benchmarking_, Genome Biology, 2019.

11. Dodge và cộng sự, _Show Your Work: Improved Reporting of Experimental Results_, EMNLP, 2019.
