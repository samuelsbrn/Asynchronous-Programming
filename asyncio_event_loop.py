"""
Simulasi Event Loop dengan Python's asyncio
Menunjukkan implementasi modern event loop menggunakan async/await

Perbedaan dengan implementasi sebelumnya:
- Menggunakan coroutines dan async/await syntax
- Ditenagai oleh asyncio library (production-ready)
- Demonstrasi concurrent.futures untuk simulasi I/O
"""

import asyncio
import time
import random
from datetime import datetime
from typing import List, Tuple


class AsyncEventLoopSimulator:
    """Simulator untuk mendemonstrasikan asyncio event loop"""
    
    def __init__(self):
        self.start_time = None
        self.tasks_summary = []
    
    def _get_elapsed(self) -> float:
        """Dapatkan waktu berlalu sejak start"""
        if self.start_time is None:
            return 0
        return time.time() - self.start_time
    
    def _format_time(self, elapsed: float) -> str:
        """Format waktu ke ms"""
        return f"{elapsed*1000:.0f}ms"
    
    async def simulate_network_request(self, 
                                      name: str, 
                                      delay: float = None) -> Tuple[str, float]:
        """
        Simulasi async network request
        Dalam async, ini tidak akan memblokir event loop
        
        Args:
            name: Nama request
            delay: Durasi simulasi (random jika None)
        
        Returns:
            Tuple berisi (result, duration)
        """
        if delay is None:
            delay = random.uniform(1.0, 3.0)
        
        elapsed_start = self._get_elapsed()
        print(f"[{self._format_time(elapsed_start):>6}] 📡 Network request '{name}' dimulai...")
        
        # Await sleep (non-blocking)
        await asyncio.sleep(delay)
        
        elapsed_end = self._get_elapsed()
        print(f"[{self._format_time(elapsed_end):>6}] ✅ Network request '{name}' "
              f"selesai setelah {self._format_time(delay)}")
        
        return (f"Response dari {name}", delay)
    
    async def simulate_database_query(self, 
                                     query_name: str, 
                                     delay: float = None) -> Tuple[str, float]:
        """Simulasi async database query"""
        if delay is None:
            delay = random.uniform(0.5, 2.0)
        
        elapsed_start = self._get_elapsed()
        print(f"[{self._format_time(elapsed_start):>6}] 🗄️  Database query '{query_name}' dimulai...")
        
        await asyncio.sleep(delay)
        
        elapsed_end = self._get_elapsed()
        print(f"[{self._format_time(elapsed_end):>6}] ✅ Database query '{query_name}' "
              f"selesai setelah {self._format_time(delay)}")
        
        return (f"Data dari {query_name}", delay)
    
    async def simulate_file_operation(self, 
                                     file_name: str, 
                                     delay: float = None) -> Tuple[str, float]:
        """Simulasi async file operation"""
        if delay is None:
            delay = random.uniform(0.3, 1.5)
        
        elapsed_start = self._get_elapsed()
        print(f"[{self._format_time(elapsed_start):>6}] 📁 File operation '{file_name}' dimulai...")
        
        await asyncio.sleep(delay)
        
        elapsed_end = self._get_elapsed()
        print(f"[{self._format_time(elapsed_end):>6}] ✅ File operation '{file_name}' "
              f"selesai setelah {self._format_time(delay)}")
        
        return (f"File {file_name} diproses", delay)
    
    async def simulate_computation(self, 
                                  calc_name: str, 
                                  delay: float = None) -> Tuple[int, float]:
        """Simulasi async computation"""
        if delay is None:
            delay = random.uniform(0.5, 1.5)
        
        elapsed_start = self._get_elapsed()
        print(f"[{self._format_time(elapsed_start):>6}] ⚙️  Computation '{calc_name}' dimulai...")
        
        await asyncio.sleep(delay)
        
        elapsed_end = self._get_elapsed()
        result = random.randint(100, 1000)
        print(f"[{self._format_time(elapsed_end):>6}] ✅ Computation '{calc_name}' "
              f"selesai setelah {self._format_time(delay)}")
        
        return (result, delay)
    
    async def run_demo_1(self):
        """Demo 1: Concurrent tasks menggunakan asyncio.gather"""
        print("\n" + "█"*70)
        print("█ DEMO 1: Asyncio - Multiple Tasks Concurrent")
        print("█"*70)
        
        self.start_time = time.time()
        
        print(f"\n[START] Waktu: {datetime.now().strftime('%H:%M:%S')}\n")
        
        # Buat multiple coroutines
        tasks = [
            self.simulate_network_request("API_GetUser"),
            self.simulate_database_query("SELECT * FROM users"),
            self.simulate_file_operation("data.txt"),
            self.simulate_network_request("API_GetProducts"),
            self.simulate_computation("Heavy calc"),
        ]
        
        # Jalankan semua task secara concurrent
        results = await asyncio.gather(*tasks)
        
        # Print summary
        total_time = self._get_elapsed()
        print(f"\n" + "="*70)
        print(f"Total waktu eksekusi: {self._format_time(total_time)}")
        total_sequential = sum(r[1] for r in results)
        efficiency = (total_sequential / total_time) * 100
        print(f"Jika sequential: {self._format_time(total_sequential)}")
        print(f"Efisiensi paralelism: {efficiency:.1f}%")
        print("="*70)
    
    async def run_demo_2(self):
        """Demo 2: Task dengan durasi terkontrol"""
        print("\n" + "█"*70)
        print("█ DEMO 2: Asyncio - Controlled Task Durations")
        print("█"*70)
        
        self.start_time = time.time()
        
        print(f"\n[START] Waktu: {datetime.now().strftime('%H:%M:%S')}\n")
        
        tasks = [
            self.simulate_network_request("Task_A", 2.0),
            self.simulate_network_request("Task_B", 3.0),
            self.simulate_network_request("Task_C", 1.0),
            self.simulate_network_request("Task_D", 2.5),
        ]
        
        results = await asyncio.gather(*tasks)
        
        total_time = self._get_elapsed()
        print(f"\n" + "="*70)
        print(f"Total waktu eksekusi: {self._format_time(total_time)}")
        total_sequential = sum(r[1] for r in results)
        print(f"Jika sequential: {self._format_time(total_sequential)}")
        print(f"Time saved: {self._format_time(total_sequential - total_time)}")
        print("="*70)
    
    async def run_demo_3(self):
        """Demo 3: Langsung menjalankan task (fire and forget)"""
        print("\n" + "█"*70)
        print("█ DEMO 3: Asyncio - Create Tasks (Fire and Forget)")
        print("█"*70)
        
        self.start_time = time.time()
        
        print(f"\n[START] Waktu: {datetime.now().strftime('%H:%M:%S')}\n")
        
        # Create tasks tanpa menunggu
        task1 = asyncio.create_task(self.simulate_network_request("Request_1"))
        task2 = asyncio.create_task(self.simulate_database_query("Query_1"))
        task3 = asyncio.create_task(self.simulate_file_operation("File_1"))
        task4 = asyncio.create_task(self.simulate_computation("Calc_1"))
        
        # Tunggu semua task selesai
        results = await asyncio.gather(task1, task2, task3, task4)
        
        total_time = self._get_elapsed()
        print(f"\n" + "="*70)
        print(f"Total waktu eksekusi: {self._format_time(total_time)}")
        print("="*70)
    
    async def run_demo_4(self):
        """Demo 4: asyncio.Queue for producer-consumer pattern"""
        print("\n" + "█"*70)
        print("█ DEMO 4: Asyncio - Producer-Consumer Pattern")
        print("█"*70)
        
        self.start_time = time.time()
        
        async def producer(queue: asyncio.Queue, num_items: int):
            """Producer yang menambahkan items ke queue"""
            for i in range(num_items):
                item = f"Item_{i+1}"
                await queue.put(item)
                elapsed = self._get_elapsed()
                print(f"[{self._format_time(elapsed):>6}] 📦 Producer: Created {item}")
                await asyncio.sleep(0.5)
            
            # Signal bahwa producer selesai
            await queue.put(None)
        
        async def consumer(queue: asyncio.Queue, consumer_id: int):
            """Consumer yang memproses items dari queue"""
            while True:
                item = await queue.get()
                
                if item is None:
                    # Producer sudah selesai
                    await queue.put(None)  # Untuk consumer lain
                    break
                
                elapsed = self._get_elapsed()
                print(f"[{self._format_time(elapsed):>6}] 🔄 Consumer_{consumer_id}: Processing {item}")
                
                # Simulasi pemrosesan
                await asyncio.sleep(random.uniform(0.5, 1.5))
                
                elapsed = self._get_elapsed()
                print(f"[{self._format_time(elapsed):>6}] ✅ Consumer_{consumer_id}: Completed {item}")
                
                queue.task_done()
        
        # Jalankan producer-consumer
        queue = asyncio.Queue(maxsize=3)
        
        producer_task = asyncio.create_task(producer(queue, 6))
        consumer_tasks = [
            asyncio.create_task(consumer(queue, i+1))
            for i in range(2)
        ]
        
        await asyncio.gather(producer_task, *consumer_tasks)
        
        total_time = self._get_elapsed()
        print(f"\n" + "="*70)
        print(f"Total waktu eksekusi: {self._format_time(total_time)}")
        print("="*70)
    
    async def run_demo_5(self):
        """Demo 5: Timeout dan cancellation"""
        print("\n" + "█"*70)
        print("█ DEMO 5: Asyncio - Timeout & Cancellation")
        print("█"*70)
        
        self.start_time = time.time()
        
        print(f"\n[START] Waktu: {datetime.now().strftime('%H:%M:%S')}\n")
        
        async def long_running_task(name: str, duration: float):
            """Task yang lama"""
            try:
                elapsed_start = self._get_elapsed()
                print(f"[{self._format_time(elapsed_start):>6}] ⏳ Task '{name}' (duration: {duration}s) dimulai...")
                
                await asyncio.sleep(duration)
                
                elapsed_end = self._get_elapsed()
                print(f"[{self._format_time(elapsed_end):>6}] ✅ Task '{name}' selesai")
            except asyncio.CancelledError:
                elapsed_end = self._get_elapsed()
                print(f"[{self._format_time(elapsed_end):>6}] ⚠️  Task '{name}' dibatalkan!")
                raise
        
        # Create tasks
        task1 = asyncio.create_task(long_running_task("Fast Task", 1.0))
        task2 = asyncio.create_task(long_running_task("Slow Task", 5.0))
        task3 = asyncio.create_task(long_running_task("Medium Task", 3.0))
        
        try:
            # Tunggu sampai timeout 3 detik
            await asyncio.wait_for(
                asyncio.gather(task1, task2, task3),
                timeout=3.0
            )
        except asyncio.TimeoutError:
            elapsed = self._get_elapsed()
            print(f"\n[{self._format_time(elapsed):>6}] ⏱️  TIMEOUT! Membatalkan semua task...")
            
            # Batalkan semua task yang masih running
            task2.cancel()
            task3.cancel()
            
            # Tunggu sampai semua task selesai
            await asyncio.gather(task1, task2, task3, return_exceptions=True)
        
        total_time = self._get_elapsed()
        print(f"\n" + "="*70)
        print(f"Total waktu eksekusi: {self._format_time(total_time)}")
        print("="*70)
    
    async def run_all_demos(self):
        """Jalankan semua demo"""
        await self.run_demo_1()
        input("\n[Tekan ENTER untuk melanjutkan...]")
        
        await self.run_demo_2()
        input("\n[Tekan ENTER untuk melanjutkan...]")
        
        await self.run_demo_3()
        input("\n[Tekan ENTER untuk melanjutkan...]")
        
        await self.run_demo_4()
        input("\n[Tekan ENTER untuk melanjutkan...]")
        
        await self.run_demo_5()


async def main():
    """Main async function"""
    print("\n" + "═"*70)
    print("╔" + "═"*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "SIMULASI ASYNCIO EVENT LOOP - Python Modern Async".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "═"*68 + "╝")
    print("═"*70)
    
    print("""
Demonstrasi Python's asyncio - True Event Loop:

🔄 asyncio.gather() - Jalankan multiple coroutines concurrently
🚀 asyncio.create_task() - Create tasks yang berjalan independent
📦 asyncio.Queue - Async queue untuk producer-consumer pattern
⏱️  asyncio.wait_for() - Set timeout untuk task execution
❌ asyncio.CancelledError - Batalkan task yang sedang running

Key Concepts:
  • async/await: Syntax untuk define dan consume coroutines
  • Non-blocking: I/O operations tidak memblokir event loop
  • Single-threaded: Satu thread, banyak coroutines
  • Efficient: Lower overhead dibanding threading

Perbandingan dengan threading:
  ✅ Async: Lebih ringan, easier to debug
  ❌ Async: Hanya satu thread (limited CPU-bound parallelism)
  ✅ Threading: True parallelism untuk CPU-bound
  ❌ Threading: Overhead tinggi, synchronization kompleks
    """)
    
    print("\n" + "═"*70)
    print("Memulai demonstrasi asyncio...")
    print("="*70)
    
    simulator = AsyncEventLoopSimulator()
    await simulator.run_all_demos()
    
    print("\n" + "═"*70)
    print("✨ Semua demonstrasi asyncio selesai!")
    print("═"*70)


if __name__ == "__main__":
    asyncio.run(main())
