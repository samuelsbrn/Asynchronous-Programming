"""
Simulasi Event Loop - Program untuk menunjukkan mekanisme event loop
yang menjalankan tugas-tugas secara parallel tanpa blocking

Author: Educational Simulation
Tujuan: Mendemonstrasikan konsep event loop, task queue, dan non-blocking I/O
"""

import time
import random
from collections import deque
from enum import Enum
from dataclasses import dataclass
from typing import Callable, Any, List
from datetime import datetime


class TaskStatus(Enum):
    """Status untuk setiap task"""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


@dataclass
class Task:
    """Representasi satu task dalam event loop"""
    id: int
    name: str
    operation: Callable
    args: tuple = ()
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: str = None
    start_time: float = None
    end_time: float = None
    
    def __repr__(self):
        return f"Task(id={self.id}, name='{self.name}', status={self.status.value})"


class EventLoop:
    """
    Implementasi custom event loop yang mengelola task queue
    dan menjalankan task secara non-blocking
    """
    
    def __init__(self, max_concurrent: int = 3):
        """
        Inisialisasi event loop
        
        Args:
            max_concurrent: Jumlah maksimal task yang bisa berjalan bersamaan
        """
        self.task_queue = deque()
        self.running_tasks: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.max_concurrent = max_concurrent
        self.task_counter = 0
        self.is_running = False
        self.start_time = None
        
    def add_task(self, name: str, operation: Callable, args: tuple = ()) -> int:
        """
        Tambahkan task baru ke queue
        
        Args:
            name: Nama task
            operation: Fungsi/operasi yang akan dijalankan
            args: Argument untuk fungsi
            
        Returns:
            Task ID
        """
        self.task_counter += 1
        task = Task(
            id=self.task_counter,
            name=name,
            operation=operation,
            args=args
        )
        self.task_queue.append(task)
        print(f"[QUEUE] Task '{name}' ditambahkan (ID: {task.id})")
        return task.id
    
    def _get_elapsed_time(self) -> float:
        """Dapatkan waktu yang telah berlalu sejak event loop dimulai"""
        return time.time() - self.start_time
    
    def _format_time(self, elapsed: float) -> str:
        """Format waktu dalam format ms"""
        return f"{elapsed*1000:.0f}ms"
    
    def run(self):
        """
        Jalankan event loop utama
        Event loop akan terus berjalan sampai semua task selesai
        """
        self.is_running = True
        self.start_time = time.time()
        
        print("\n" + "="*70)
        print(f"🚀 EVENT LOOP DIMULAI - {datetime.now().strftime('%H:%M:%S')}")
        print("="*70 + "\n")
        
        while self.task_queue or self.running_tasks:
            elapsed = self._get_elapsed_time()
            
            # Cek task yang sudah selesai
            self._check_completed_tasks()
            
            # Mulai task baru jika ada slot kosong
            while (len(self.running_tasks) < self.max_concurrent and 
                   self.task_queue):
                task = self.task_queue.popleft()
                self._start_task(task, elapsed)
            
            # Simulasi waktu untuk event loop cycle
            time.sleep(0.05)  # 50ms per cycle
        
        self.is_running = False
        self._print_summary()
    
    def _start_task(self, task: Task, elapsed: float):
        """
        Mulai menjalankan task
        
        Args:
            task: Task yang akan dijalankan
            elapsed: Waktu yang telah berlalu
        """
        task.status = TaskStatus.RUNNING
        task.start_time = elapsed
        self.running_tasks.append(task)
        print(f"[{self._format_time(elapsed):>6}] ▶️  Task '{task.name}' mulai dijalankan")
    
    def _check_completed_tasks(self):
        """Cek apakah ada task yang sudah selesai"""
        completed = []
        
        for task in self.running_tasks:
            # Simulasi task execution
            elapsed_since_start = self._get_elapsed_time() - task.start_time
            
            # Task dianggap selesai ketika operasinya return
            try:
                result = task.operation(*task.args)
                
                # Jika operasi mengembalikan nilai (tidak infinite), task selesai
                if result is not None or result == 0:
                    task.result = result
                    task.status = TaskStatus.COMPLETED
                    task.end_time = self._get_elapsed_time()
                    
                    elapsed_total = task.end_time - task.start_time
                    print(f"[{self._format_time(task.end_time):>6}] ✅ Task '{task.name}' "
                          f"selesai dalam {self._format_time(elapsed_total)}")
                    
                    completed.append(task)
                    self.completed_tasks.append(task)
                    
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                task.end_time = self._get_elapsed_time()
                print(f"[{self._format_time(task.end_time):>6}] ❌ Task '{task.name}' "
                      f"gagal: {e}")
                completed.append(task)
                self.completed_tasks.append(task)
        
        # Hapus task yang sudah selesai dari running tasks
        for task in completed:
            self.running_tasks.remove(task)
    
    def _print_summary(self):
        """Cetak ringkasan eksekusi"""
        total_time = self._get_elapsed_time()
        successful = sum(1 for t in self.completed_tasks if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in self.completed_tasks if t.status == TaskStatus.FAILED)
        
        print("\n" + "="*70)
        print("📊 RINGKASAN EKSEKUSI EVENT LOOP")
        print("="*70)
        print(f"Total waktu eksekusi: {self._format_time(total_time)}")
        print(f"Total task selesai: {len(self.completed_tasks)}")
        print(f"  ✅ Berhasil: {successful}")
        print(f"  ❌ Gagal: {failed}")
        print(f"Jumlah prosesor paralel: {self.max_concurrent}")
        print("\nDetail Task:")
        
        for task in self.completed_tasks:
            status_symbol = "✅" if task.status == TaskStatus.COMPLETED else "❌"
            duration = self._format_time(task.end_time - task.start_time)
            print(f"  {status_symbol} {task.name:<20} | Durasi: {duration:>6} | "
                  f"Hasil: {task.result}")
        
        # Hitung efisiensi
        if self.completed_tasks:
            total_work_time = sum(t.end_time - t.start_time for t in self.completed_tasks)
            efficiency = (total_work_time / (total_time * self.max_concurrent)) * 100
            print(f"\nEfisiensi penggunaan prosesor: {efficiency:.1f}%")
        
        print("="*70 + "\n")


# ============================================================================
# SIMULASI OPERASI YANG BERBEDA (Simulasi I/O berlainan durasi)
# ============================================================================

def simulate_network_request(task_name: str, delay: float = None) -> str:
    """
    Simulasi network request (I/O operation)
    Dalam real-world, operasi ini akan async tanpa blocking main thread
    
    Args:
        task_name: Nama task
        delay: Durasi dalam detik (random jika None)
    
    Returns:
        Response string
    """
    if delay is None:
        delay = random.uniform(1.0, 3.0)
    
    time.sleep(delay)
    return f"Response dari {task_name}"


def simulate_database_query(query_name: str, delay: float = None) -> str:
    """Simulasi database query"""
    if delay is None:
        delay = random.uniform(0.5, 2.0)
    
    time.sleep(delay)
    return f"Data dari {query_name}"


def simulate_file_operation(file_name: str, delay: float = None) -> str:
    """Simulasi file read/write operation"""
    if delay is None:
        delay = random.uniform(0.3, 1.5)
    
    time.sleep(delay)
    return f"File {file_name} diproses"


def simulate_computation(calc_name: str, delay: float = None) -> int:
    """Simulasi CPU-intensive computation"""
    if delay is None:
        delay = random.uniform(0.5, 1.5)
    
    time.sleep(delay)
    return random.randint(100, 1000)


def simulate_image_processing(image_name: str, delay: float = None) -> str:
    """Simulasi image processing task"""
    if delay is None:
        delay = random.uniform(1.5, 3.5)
    
    time.sleep(delay)
    return f"Image {image_name} diproses"


# ============================================================================
# DEMONSTRASI EVENT LOOP
# ============================================================================

def demo_basic_event_loop():
    """Demo 1: Event loop dasar dengan berbagai jenis task"""
    print("\n" + "█"*70)
    print("█ DEMO 1: Event Loop Dasar - Multiple Tasks Berjalan Parallel")
    print("█"*70)
    
    event_loop = EventLoop(max_concurrent=3)
    
    # Tambahkan berbagai task
    event_loop.add_task("API Request 1", simulate_network_request, ("API_GetUser",))
    event_loop.add_task("Database Query", simulate_database_query, ("SELECT * FROM users",))
    event_loop.add_task("File Read", simulate_file_operation, ("data.txt",))
    event_loop.add_task("API Request 2", simulate_network_request, ("API_GetProducts",))
    event_loop.add_task("Image Process", simulate_image_processing, ("photo.jpg",))
    event_loop.add_task("Computation", simulate_computation, ("Heavy calculation",))
    
    # Jalankan event loop
    event_loop.run()


def demo_controlled_delays():
    """Demo 2: Event loop dengan durasi yang dikontrol untuk visualisasi lebih jelas"""
    print("\n" + "█"*70)
    print("█ DEMO 2: Event Loop dengan Durasi Terkontrol")
    print("█" * 70)
    
    event_loop = EventLoop(max_concurrent=2)
    
    # Task dengan durasi tertentu
    event_loop.add_task("Task A (2s)", simulate_network_request, ("TaskA", 2.0))
    event_loop.add_task("Task B (3s)", simulate_network_request, ("TaskB", 3.0))
    event_loop.add_task("Task C (1s)", simulate_network_request, ("TaskC", 1.0))
    event_loop.add_task("Task D (2.5s)", simulate_network_request, ("TaskD", 2.5))
    
    event_loop.run()


def demo_high_concurrency():
    """Demo 3: Event loop dengan concurrency tinggi"""
    print("\n" + "█"*70)
    print("█ DEMO 3: Event Loop dengan High Concurrency (4 prosesor)")
    print("█"*70)
    
    event_loop = EventLoop(max_concurrent=4)
    
    # Banyak task
    for i in range(1, 9):
        event_loop.add_task(
            f"Task_{i}",
            simulate_network_request,
            (f"Request_{i}", random.uniform(1.0, 2.5))
        )
    
    event_loop.run()


def demo_mixed_workloads():
    """Demo 4: Mixed workloads dengan berbagai tipe operasi"""
    print("\n" + "█"*70)
    print("█ DEMO 4: Event Loop dengan Mixed Workloads")
    print("█"*70)
    
    event_loop = EventLoop(max_concurrent=3)
    
    # Berbagai jenis workload
    event_loop.add_task("Network: API Call", simulate_network_request, ("API_1",))
    event_loop.add_task("Database: Query", simulate_database_query, ("Query_1",))
    event_loop.add_task("File: Read config", simulate_file_operation, ("config.json",))
    event_loop.add_task("Network: Download", simulate_network_request, ("Download_1",))
    event_loop.add_task("Image: Resize", simulate_image_processing, ("image.png",))
    event_loop.add_task("Compute: Math", simulate_computation, ("Calculate",))
    event_loop.add_task("Database: Update", simulate_database_query, ("UPDATE users",))
    event_loop.add_task("File: Write log", simulate_file_operation, ("app.log",))
    
    event_loop.run()


def main():
    """Main program"""
    print("\n" + "═"*70)
    print("╔" + "═"*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "SIMULASI EVENT LOOP - Non-Blocking Task Execution".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "═"*68 + "╝")
    print("═"*70)
    
    print("""
Demonstrasi ini menunjukkan bagaimana Event Loop bekerja:

1️⃣  Task Queue: Antrian task yang menunggu untuk dijalankan
2️⃣  Running Tasks: Task yang sedang dijalankan (sampai max_concurrent)
3️⃣  Non-Blocking: Saat satu task menunggu (I/O), task lain dapat berjalan
4️⃣  Parallelism: Multiple task berjalan secara concurrent (tidak sequential)

Keuntungan:
  ✅ Efisiensi tinggi (tidak ada blocking)
  ✅ Responsiveness tinggi
  ✅ Resource utilization optimal
  ✅ Scalability lebih baik
    """)
    
    print("\n" + "═"*70)
    print("Memulai demonstrasi...")
    print("="*70)
    
    # Jalankan berbagai demo
    demo_basic_event_loop()
    input("\n[Tekan ENTER untuk melanjutkan ke demo selanjutnya...]")
    
    demo_controlled_delays()
    input("\n[Tekan ENTER untuk melanjutkan ke demo selanjutnya...]")
    
    demo_high_concurrency()
    input("\n[Tekan ENTER untuk melanjutkan ke demo selanjutnya...]")
    
    demo_mixed_workloads()
    
    print("\n" + "═"*70)
    print("✨ Semua demonstrasi selesai!")
    print("═"*70)


if __name__ == "__main__":
    main()
