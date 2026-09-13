import time
import torch
import torch.multiprocessing as mp


# ============================================================
# K40 FP32 TORTURE / TFLOPS BENCHMARK
# ============================================================

MATRIX_N = 8192
STREAMS = 4
WARMUP_SECONDS = 20
TEST_SECONDS = 300
REPORT_INTERVAL = 5


def worker(gpu, result_queue):
    torch.cuda.set_device(gpu)
    device = torch.device(f"cuda:{gpu}")

    props = torch.cuda.get_device_properties(gpu)

    print(
        f"\nGPU {gpu}: {props.name}\n"
        f"  Compute capability : {props.major}.{props.minor}\n"
        f"  SMs                : {props.multi_processor_count}\n"
        f"  VRAM               : {props.total_memory / 1024**3:.2f} GiB\n"
        f"  Matrix size        : {MATRIX_N} x {MATRIX_N}\n"
        f"  Parallel GEMMs     : {STREAMS}\n",
        flush=True
    )

    # --------------------------------------------------------
    # Allocate independent matrices
    # --------------------------------------------------------

    A = []
    B = []
    C = []

    print(f"GPU {gpu}: allocating...", flush=True)

    for _ in range(STREAMS):
        A.append(torch.randn(
            MATRIX_N, MATRIX_N,
            dtype=torch.float32,
            device=device
        ))

        B.append(torch.randn(
            MATRIX_N, MATRIX_N,
            dtype=torch.float32,
            device=device
        ))

        C.append(torch.empty(
            MATRIX_N, MATRIX_N,
            dtype=torch.float32,
            device=device
        ))

    print(f"GPU {gpu}: allocation complete", flush=True)

    # --------------------------------------------------------
    # Warmup
    # --------------------------------------------------------

    print(f"GPU {gpu}: warming up for {WARMUP_SECONDS}s...", flush=True)

    warmup_end = time.perf_counter() + WARMUP_SECONDS

    while time.perf_counter() < warmup_end:
        for i in range(STREAMS):
            torch.mm(A[i], B[i], out=C[i])

    torch.cuda.synchronize()

    print(f"GPU {gpu}: warmup complete", flush=True)

    # --------------------------------------------------------
    # Benchmark
    # --------------------------------------------------------

    print(
        f"GPU {gpu}: BEGIN {TEST_SECONDS}s FP32 TORTURE",
        flush=True
    )

    start = time.perf_counter()
    last_report = start

    total_flops = 0

    try:
        while True:

            for i in range(STREAMS):
                torch.mm(A[i], B[i], out=C[i])

                # GEMM performs approximately 2*N^3 FLOPs.
                total_flops += 2 * MATRIX_N**3

            now = time.perf_counter()

            if now - last_report >= REPORT_INTERVAL:

                # Make sure all queued GPU work is actually finished.
                torch.cuda.synchronize()

                elapsed = time.perf_counter() - start

                tflops = (
                    total_flops /
                    elapsed /
                    1e12
                )

                print(
                    f"GPU {gpu} | "
                    f"{elapsed:8.1f}s | "
                    f"{tflops:6.3f} TFLOP/s",
                    flush=True
                )

                last_report = now

            if now - start >= TEST_SECONDS:
                break

    except RuntimeError as e:

        print(
            f"\nGPU {gpu} !!! CUDA FAILURE !!!\n{e}\n",
            flush=True
        )

        result_queue.put((gpu, None))
        return

    torch.cuda.synchronize()

    elapsed = time.perf_counter() - start

    final_tflops = (
        total_flops /
        elapsed /
        1e12
    )

    print(
        f"\n"
        f"============================================================\n"
        f"GPU {gpu} COMPLETE\n"
        f"------------------------------------------------------------\n"
        f"Runtime       : {elapsed:.2f} s\n"
        f"Total FLOPs   : {total_flops / 1e15:.3f} PFLOP\n"
        f"Average       : {final_tflops:.3f} TFLOP/s\n"
        f"============================================================",
        flush=True
    )

    result_queue.put((gpu, final_tflops))


def main():

    gpu_count = torch.cuda.device_count()

    print("\n" + "=" * 60)
    print("        KEPLER FP32 TFLOPS TORTURE TEST")
    print("=" * 60)
    print(f"GPUs detected: {gpu_count}")

    for gpu in range(gpu_count):
        print(
            f"GPU {gpu}: {torch.cuda.get_device_name(gpu)}"
        )

    print("=" * 60 + "\n")

    mp.set_start_method("spawn", force=True)

    result_queue = mp.Queue()
    processes = []

    for gpu in range(gpu_count):

        p = mp.Process(
            target=worker,
            args=(gpu, result_queue)
        )

        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    # --------------------------------------------------------
    # Results
    # --------------------------------------------------------

    results = []

    while not result_queue.empty():
        results.append(result_queue.get())

    results.sort()

    print("\n" + "#" * 60)
    print("                    FINAL RESULTS")
    print("#" * 60)

    aggregate = 0.0

    for gpu, tflops in results:

        if tflops is None:
            print(f"GPU {gpu}: CUDA FAILURE")
        else:
            print(f"GPU {gpu}: {tflops:.3f} TFLOP/s")
            aggregate += tflops

    print("-" * 60)
    print(f"AGGREGATE: {aggregate:.3f} TFLOP/s")
    print("#" * 60)


if __name__ == "__main__":
    main()
