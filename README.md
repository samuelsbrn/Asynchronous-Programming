
# 🚀 Simulasi Event Loop - Program Event Loop Non-Blocking

Implementasi lengkap simulasi event loop dalam Python yang mendemonstrasikan bagaimana tugas-tugas dapat diselesaikan secara paralel tanpa saling mengunci (blocking).

## 📋 File-File di Repository

### 1. `event_loop_simulator.py` - Custom Event Loop Implementation
Implementasi event loop dari nol dengan mekanisme:
- **Task Queue**: Antrian task yang menunggu untuk dijalankan
- **Running Tasks Pool**: Task yang sedang berjalan dengan batas concurrency
- **Non-blocking Execution**: Task dijalankan secara concurrent
- **Cycle-based Processing**: Event loop cycle dengan interval 50ms

**Fitur:**
```
✅ Custom event loop implementation
✅ Task queue management
✅ Concurrent execution dengan max_concurrent limit
✅ Task status tracking (PENDING, RUNNING, COMPLETED, FAILED)
✅ Performance metrics dan efficiency calculation
✅ Multiple demo scenarios
```

**Cara menjalankan:**
```bash
python event_loop_simulator.py
```

**Demo yang disertakan:**
1. **Basic Event Loop** - Multiple tasks berbeda tipe paralel
2. **Controlled Delays** - Task dengan durasi spesifik untuk visualisasi jelas
3. **High Concurrency** - Banyak task dengan concurrency tinggi
4. **Mixed Workloads** - Kombinasi berbagai jenis operasi

---

### 2. `asyncio_event_loop.py` - Python's asyncio Event Loop
Demonstrasi menggunakan Python's built-in asyncio library (production-ready):
- **True Async/Await**: Menggunakan modern async/await syntax
- **Coroutine-based**: True event loop dengan coroutines
- **Queue Pattern**: Producer-consumer pattern dengan asyncio.Queue
- **Timeout & Cancellation**: Advanced async features

**Fitur:**
```
✅ asyncio.gather() - Concurrent execution
✅ asyncio.create_task() - Fire and forget pattern
✅ asyncio.Queue - Producer-consumer pattern
✅ asyncio.wait_for() - Timeout handling
✅ Task cancellation support
✅ Advanced async demonstrations
```

**Cara menjalankan:**
```bash
python asyncio_event_loop.py
```

**Demo yang disertakan:**
1. **Concurrent Tasks** - Multiple coroutines dengan gather()
2. **Controlled Durations** - Coroutines dengan durasi spesifik
3. **Create Tasks** - Fire and forget dengan create_task()
4. **Producer-Consumer** - Queue-based async pattern
5. **Timeout & Cancellation** - Timeout dan task cancellation

---

## 🔍 Konsep Utama Event Loop

### Apa itu Event Loop?

Event loop adalah mekanisme untuk menjalankan banyak task secara concurrent dalam satu thread:

```
┌─────────────────────────────────────────────┐
│           Event Loop (Main Thread)          │
├─────────────────────────────────────────────┤
│                                             │
│  1. Check task queue                        │
│  2. Start new tasks (jika ada slot)         │
│  3. Check completed tasks                   │
│  4. Remove completed from running pool      │
│  5. Sleep brief moment (don't hog CPU)      │
│  6. Repeat (back to step 1)                 │
│                                             │
└─────────────────────────────────────────────┘

Time:  0ms      100ms     200ms     300ms
Task A: [===Network I/O===]
Task B:         [===DB Query===]
Task C:                    [===File Op===]

Result: 3 tasks berjalan dalam ~300ms
        (Jika sequential: ~900ms)
```

### Perbedaan: Blocking vs Non-blocking

```
BLOCKING (Sequential - Lambat):
Task A: ████████████ (300ms)
Task B:             ████████ (200ms)
Task C:                     ████ (100ms)
────────────────────────────────────────
Total: 600ms (serial execution)

NON-BLOCKING (Concurrent - Cepat):
Task A: ████████████
Task B: ████████
Task C: ████
────────────────────────────────────────
Total: 300ms (parallel execution)
```

### Why Event Loop?

| Aspek | Threading | Event Loop |
|-------|-----------|-----------|
| **Concurrency** | True (OS level) | Cooperative (single-thread) |
| **Memory** | Heavy (stack per thread) | Light (simpler data structures) |
| **Synchronization** | Kompleks (locks, mutexes) | Simpler (single execution context) |
| **CPU-bound** | ✅ Excellent | ❌ Poor (single-thread bottleneck) |
| **I/O-bound** | ✅ Good | ✅ Excellent |
| **Debugging** | ❌ Difficult (race conditions) | ✅ Easier (predictable execution) |

---

## 📊 Visualisasi Output

Saat menjalankan program, output akan menunjukkan:

```
[START]  0ms  ▶️  Task 'Network: API' dimulai
[START]  0ms  ▶️  Task 'Database: Query' dimulai
[START] 50ms  ▶️  Task 'File: Read' dimulai

[  540ms] ✅ Task 'File: Read' selesai dalam 492ms
[  540ms] ▶️  Task 'Computation: Math' dimulai

[ 1234ms] ✅ Task 'Network: API' selesai dalam 1234ms
[ 1234ms] ▶️  Task 'Database: Update' dimulai

[ 2100ms] ✅ Task 'Database: Query' selesai dalam 2099ms

📊 RINGKASAN:
  ✅ Berhasil: 8 dari 8 task
  Total waktu: 2100ms (bukan 6500ms jika sequential)
  Efisiensi: 75.3%
```

---

## 🎯 Skenario Penggunaan Real-World

### 1. Web Server (Handling Multiple Requests)
```
Server dengan Event Loop:
- Client 1 request → Server mulai process (non-blocking)
- Client 2 request → Server handle juga (concurrent)
- Client 3 request → Server handle juga (concurrent)

Satu client menunggu I/O (Database)
↓ Server tidak idle, handle client lain
Saat I/O selesai, kembali ke client pertama
```

### 2. Data Pipeline
```
Event Loop Data Processing:
- Task 1: Fetch data dari API
- Task 2: Process data (transformation)
- Task 3: Write ke database
- Task 4: Generate report
- Task 5: Send notification

Semua ini berjalan concurrent tanpa saling menunggu!
```

### 3. Microservices
```
Service A  ──┐
Service B  ──┼──> Event Loop ──> Response
Service C  ──┘

Satu event loop menunggu response dari 3 services secara parallel
```

---

## 💡 Perbandingan Implementasi

### Custom Event Loop (`event_loop_simulator.py`)

**Keuntungan:**
- ✅ Educational - Pahami mekanisme internal
- ✅ Customizable - Sesuaikan dengan kebutuhan
- ✅ No dependencies - Pure Python

**Kelemahan:**
- ❌ Limited features - Tidak sepanjang asyncio
- ❌ Production risky - Bugs mungkin terjadi

### asyncio Event Loop (`asyncio_event_loop.py`)

**Keuntungan:**
- ✅ Production-ready - Tested thoroughly
- ✅ Modern syntax - async/await
- ✅ Rich features - Timeout, cancellation, queues
- ✅ Performance - Optimized C extension

**Kelemahan:**
- ❌ Complexity - Lebih banyak konsep
- ❌ Single-thread limitation - CPU-bound task buruk

---

## 🚀 Menjalankan Program

### Prerequisite
Python 3.7+ (asyncio built-in)

### Langkah-langkah

1. **Clone atau download repository**
```bash
cd "c:\Tugas spt"
```

2. **Jalankan Event Loop Simulator (Custom)**
```bash
python event_loop_simulator.py
```

3. **Jalankan Asyncio Event Loop**
```bash
python asyncio_event_loop.py
```

4. **Lihat output dan tekan ENTER untuk lanjut ke demo berikutnya**

---

## 📈 Key Metrics Explanation

### Efficiency Percentage
```
Total work time: Jumlah semua task duration
Elapsed time: Waktu dari start sampai finish
Max concurrent: Jumlah prosesor paralel

Efficiency = (Total work time) / (Elapsed time × Max concurrent) × 100%

Contoh:
- Task A: 2 detik (berjalan 0-2s)
- Task B: 1 detik (berjalan 2-3s setelah A)
Total work: 3 detik
Elapsed: 3 detik (sequential = 100%)

Dengan parallelism:
- Task A: 2 detik (berjalan 0-2s)
- Task B: 1 detik (berjalan 0-1s, parallel)
Total work: 3 detik
Elapsed: 2 detik (parallel = 150% ideal, capped at efficiency metric)
```

---

## 🔧 Customization

### Menambah Task Baru ke Custom Event Loop
```python
# Define operasi
def my_operation(name: str) -> str:
    # Simulasi I/O dengan sleep
    time.sleep(random.uniform(0.5, 2.0))
    return f"Result dari {name}"

# Tambah ke event loop
event_loop = EventLoop(max_concurrent=3)
event_loop.add_task("My Task", my_operation, ("Task A",))
event_loop.run()
```

### Menambah Coroutine ke Asyncio
```python
async def my_coroutine(name: str) -> str:
    # Async I/O dengan asyncio.sleep
    await asyncio.sleep(random.uniform(0.5, 2.0))
    return f"Result dari {name}"

# Gunakan dalam asyncio
async def main():
    result = await my_coroutine("My Async Task")
    
asyncio.run(main())
```

---

## 📚 Bacaan Lebih Lanjut

1. **Event Loop Concepts**
   - https://en.wikipedia.org/wiki/Event_loop
   - Event loop dalam browser: JavaScript

2. **Python asyncio Documentation**
   - https://docs.python.org/3/library/asyncio.html
   - Tutorial async/await patterns

3. **Concurrency Models**
   - Threading vs async vs multiprocessing
   - Goroutines (Go)
   - Reactive programming

---

## 📝 Notes untuk Development

### Saat menggunakan Event Loop:
- ✅ **Ideal untuk I/O-bound tasks** (network, file, database)
- ❌ **Tidak ideal untuk CPU-bound** (berat komputasi → use threading/multiprocessing)
- ⚠️  **Avoid blocking operations** (jangan gunakan time.sleep(), gunakan asyncio.sleep())
- ⚠️  **Single-threaded** - CPU-heavy task akan block other tasks

### Best Practices:
1. Gunakan `async/await` untuk I/O operations
2. Hindari blocking calls dalam event loop
3. Gunakan `asyncio.create_task()` untuk independen tasks
4. Implement proper error handling dengan try/except
5. Monitor memory usage untuk long-running loops

---

## 🐛 Troubleshooting

### Program hang / tidak responsif?
- Check jika ada blocking call tanpa await
- Gunakan `asyncio.TimeoutError` untuk handle long tasks

### High memory usage?
- Check queue size, mungkin producer lebih cepat dari consumer
- Implement backpressure dengan Queue(maxsize=...)

### Tasks tidak berjalan paralel?
- Pastikan menggunakan `await asyncio.sleep()` bukan `time.sleep()`
- Verify struktur kode adalah async

---

## 🎓 Learning Outcomes

Setelah menjalankan program ini, Anda akan memahami:

1. ✅ Bagaimana event loop bekerja secara internal
2. ✅ Perbedaan blocking vs non-blocking
3. ✅ Konsep concurrency dan parallelism
4. ✅ Bagaimana async/await memungkinkan efficient I/O
5. ✅ Producer-consumer pattern
6. ✅ Task scheduling dan context switching
7. ✅ Performance optimization dengan parallelism

---

## 📄 License

Educational purpose - Feel free to modify and use for learning

---

**Created**: 2026 | **Python Version**: 3.7+

Selamat belajar Event Loop! 🚀
