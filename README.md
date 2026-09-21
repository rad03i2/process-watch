# Process Watch

A small, read-only, cross-platform command-line tool for inspecting and monitoring local processes. Process Watch turns `psutil` process metadata into a predictable CLI and reusable Python API with filtering, sorting, repeated snapshots, and JSON output.

> Author: **Radwan Abdulhadi Ahmed** · GitHub: **@rad03i2**

## Why it exists

Task managers are excellent for interactive inspection, but scripts and troubleshooting workflows often need stable, machine-readable process snapshots. Process Watch provides that narrow capability without process termination, remote agents, telemetry, or privileged defaults.

## Key features

- Inspect visible local processes with PID, name, status, CPU, memory, RSS, username and UTC creation time.
- Filter by process-name or username substring and minimum CPU/memory usage.
- Sort by CPU, memory, PID or name and cap output to 1–1000 rows.
- Repeated monitoring with a configurable 0.2–3600 second interval and optional finite snapshot count.
- Human-readable table or JSON output for automation.
- Gracefully skips processes that disappear or become inaccessible while being inspected.
- Read-only behavior: no kill, suspend, priority-changing, injection or remote-control operations.
- Reusable Python API and automated cross-platform test workflow.

## Requirements

- Python 3.10 or newer
- `psutil` 5.9–7.x (installed automatically)
- Windows, Linux or macOS

## Installation

```bash
git clone https://github.com/rad03i2/process-watch.git
cd process-watch
python -m venv .venv
```

Activate the environment (`.venv\\Scripts\\activate` on Windows or `source .venv/bin/activate` on Linux/macOS), then:

```bash
python -m pip install -e .
```

For development and tests:

```bash
python -m pip install -e ".[dev]"
```

## Usage

One snapshot, highest CPU first:

```bash
process-watch snapshot
```

Find Python processes and sort by memory:

```bash
process-watch snapshot --name python --sort memory --limit 10
```

Show processes using at least 2% memory:

```bash
process-watch snapshot --min-memory 2
```

Take five snapshots two seconds apart:

```bash
process-watch watch --interval 2 --count 5
```

Machine-readable output:

```bash
process-watch snapshot --json
process-watch watch --interval 1 --count 3 --json
```

Version/about metadata:

```bash
process-watch --version
```

### Python API

```python
from process_watch import collect_processes

rows = collect_processes(name="python", sort_by="memory", limit=5)
for process in rows:
    print(process.pid, process.name, process.memory_percent)
```

## Configuration

Process Watch has no configuration file, environment variables, network service, or credentials. Options are explicit CLI flags. Run `process-watch snapshot --help` or `process-watch watch --help` for the complete interface.

## Preview / screenshots

This is a terminal application. A useful project screenshot should show `process-watch snapshot --sort memory --limit 10` with any private usernames or process names redacted. No screenshot is bundled because repository screenshots should represent real output from the user's own machine rather than fabricated process data.

## Project structure

```text
process-watch/
├── .github/workflows/ci.yml
├── src/process_watch/
│   ├── __init__.py
│   ├── cli.py
│   └── core.py
├── tests/
│   ├── test_cli.py
│   └── test_core.py
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
├── pyproject.toml
└── README.md
```

## Testing

```bash
python -m compileall -q src tests
python -m pytest
```

GitHub Actions runs compilation, tests, and a read-only CLI smoke test on Ubuntu, Windows and macOS with Python 3.10, 3.12 and 3.13.

## Security & privacy

All collection is local. Nothing is uploaded and there is no telemetry. Process names and usernames can still reveal sensitive information, so review output before sharing it. Normal user privileges are recommended; inaccessible processes are skipped. See [SECURITY.md](SECURITY.md).

## Limitations

- CPU percentages come from the operating-system/`psutil` snapshot and may be zero or approximate depending on platform and sampling state.
- Visibility depends on OS permissions; some system processes may not expose all metadata.
- This is not a historical metrics database, alerting service, remote monitor, profiler, or task manager.
- Watch mode prints snapshots; it does not persist them automatically.
- Filtering is substring-based rather than regular-expression based.

## Optional roadmap

Future work may add opt-in CSV export, snapshot diffing, and configurable local alert thresholds. These are not claimed as current features.

## Contributing

Contributions are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md), keep monitoring read-only by default, add tests, and keep English/Arabic documentation aligned.

## License

MIT License. See [LICENSE](LICENSE).

## Author

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**

---

# العربية

## نبذة عن المشروع

**Process Watch** أداة سطر أوامر صغيرة ومتعددة المنصات لفحص العمليات المحلية ومراقبتها بصورة آمنة وللقراءة فقط. تحوّل بيانات العمليات التي توفرها مكتبة `psutil` إلى واجهة واضحة يمكن استخدامها يدويًا أو داخل السكربتات، مع التصفية والترتيب والمراقبة المتكررة وإخراج JSON.

## لماذا وُجد المشروع؟

مديرو المهام مناسبون للفحص التفاعلي، لكن الأتمتة واستكشاف الأعطال يحتاجان أحيانًا إلى لقطة ثابتة وقابلة للمعالجة آليًا. يوفر المشروع هذه الوظيفة دون قتل العمليات أو التحكم عن بعد أو التتبع أو طلب صلاحيات مرتفعة افتراضيًا.

## الميزات الرئيسية

- عرض PID والاسم والحالة واستهلاك CPU والذاكرة وRSS واسم المستخدم ووقت بدء العملية بتوقيت UTC عند توفرها.
- تصفية حسب جزء من اسم العملية أو المستخدم، أو حسب حد أدنى لاستهلاك المعالج أو الذاكرة.
- ترتيب حسب CPU أو الذاكرة أو PID أو الاسم، مع حد أقصى من 1 إلى 1000 نتيجة.
- وضع مراقبة متكرر بفاصل من 0.2 إلى 3600 ثانية، مع إمكانية تحديد عدد اللقطات.
- إخراج جدولي للبشر أو JSON للأتمتة.
- تجاوز العمليات التي تختفي أثناء الفحص أو التي لا يملك المستخدم صلاحية قراءتها بدل إيقاف البرنامج.
- الأداة للقراءة فقط: لا تقتل العمليات ولا توقفها ولا تغير أولويتها ولا تحقن كودًا فيها.
- Python API قابلة لإعادة الاستخدام واختبارات آلية متعددة المنصات.

## المتطلبات

- Python 3.10 أو أحدث.
- مكتبة `psutil` بإصدار 5.9 إلى 7.x، وتثبت تلقائيًا.
- Windows أو Linux أو macOS.

## التثبيت

```bash
git clone https://github.com/rad03i2/process-watch.git
cd process-watch
python -m venv .venv
python -m pip install -e .
```

فعّل البيئة الافتراضية قبل أمر التثبيت. وللتطوير والاختبارات:

```bash
python -m pip install -e ".[dev]"
```

## أمثلة الاستخدام

لقطة واحدة مرتبة حسب CPU:

```bash
process-watch snapshot
```

البحث عن عمليات Python وترتيبها حسب الذاكرة:

```bash
process-watch snapshot --name python --sort memory --limit 10
```

خمس لقطات بفاصل ثانيتين:

```bash
process-watch watch --interval 2 --count 5
```

إخراج JSON:

```bash
process-watch snapshot --json
```

## الإعداد

لا يحتاج المشروع إلى ملف إعداد أو متغيرات بيئة أو مفاتيح API أو خدمة شبكية. جميع الخيارات تمرر صراحة عبر CLI. استخدم `--help` لعرض الخيارات.

## المعاينة والصور

المشروع طرفي؛ أفضل صورة معاينة هي نتيجة حقيقية للأمر `process-watch snapshot --sort memory --limit 10` بعد إخفاء أي أسماء عمليات أو مستخدمين حساسة. لم تتم إضافة صورة مصطنعة إلى المستودع.

## بنية المشروع

الكود الأساسي موجود في `src/process_watch/core.py`، وواجهة الأوامر في `src/process_watch/cli.py`، والاختبارات في `tests/`، وCI في `.github/workflows/ci.yml`.

## الاختبارات

```bash
python -m compileall -q src tests
python -m pytest
```

يختبر GitHub Actions المشروع على Ubuntu وWindows وmacOS باستخدام Python 3.10 و3.12 و3.13، إضافة إلى اختبار تشغيل CLI للقراءة فقط.

## الخصوصية والأمان

الفحص محلي بالكامل ولا توجد Telemetry أو عملية رفع بيانات. رغم ذلك، قد تكشف أسماء العمليات والمستخدمين معلومات حساسة، لذلك راجع الناتج قبل مشاركته. يوصى بالتشغيل بصلاحيات المستخدم العادية. راجع [SECURITY.md](SECURITY.md).

## القيود

- نسب CPU تعتمد على لقطة النظام و`psutil` وقد تكون صفرية أو تقريبية حسب المنصة وحالة أخذ العينة.
- العمليات المرئية تعتمد على صلاحيات نظام التشغيل.
- المشروع ليس قاعدة بيانات تاريخية ولا نظام تنبيهات أو مراقبة عن بعد أو profiler أو مدير مهام.
- وضع المراقبة يطبع اللقطات ولا يحفظها تلقائيًا.
- البحث النصي يعتمد على substring وليس Regex.

## التطوير المستقبلي الاختياري

يمكن مستقبلًا إضافة تصدير CSV اختياري، ومقارنة اللقطات، وتنبيهات محلية قابلة للضبط. هذه ليست ميزات حالية.

## المساهمة

راجع [CONTRIBUTING.md](CONTRIBUTING.md). يجب الحفاظ على مبدأ القراءة فقط افتراضيًا، وإضافة اختبارات لأي تغيير وظيفي، وتحديث التوثيق الإنجليزي والعربي معًا.

## الترخيص

المشروع مرخص وفق MIT. راجع [LICENSE](LICENSE).

## المؤلف

**Radwan Abdulhadi Ahmed**  
**رضوان عبدالهادي أحمد**  
GitHub: **@rad03i2**
