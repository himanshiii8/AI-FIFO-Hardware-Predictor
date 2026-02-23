import subprocess
import random
import os
import multiprocessing
import time
import glob

# --- CONFIGURATION ---
TOTAL_SAMPLES = 5000
MAX_WIDTH = 128
MAX_DEPTH = 1024       # <--- Kept at 1024 as you requested
CORES_TO_USE = 8       # <--- Increased to 8 (Faster than 4, safer than 12)
CSV_FILE = "dataset_12.csv" 
VERILOG_FILE = "alu_fifo.v" 

# --- WORKER FUNCTION ---
def generate_one_sample(sample_id):
    width = random.randint(8, MAX_WIDTH)
    depth = random.randint(2, MAX_DEPTH)
    
    # Unique file name
    job_file = f"temp_job_{sample_id}_{random.randint(1,99999)}.ys"
    
    yosys_commands = f"""
    read_verilog {VERILOG_FILE}
    hierarchy -top alu_fifo -chparam WIDTH {width} -chparam DEPTH {depth}
    synth_xilinx
    stat
    """
    
    try:
        with open(job_file, "w") as f:
            f.write(yosys_commands)
            
        # Run Yosys with a TIMEOUT. If it takes >45s, kill it.
        try:
            result = subprocess.run(
                ["yosys", "-Q", "-s", job_file], 
                capture_output=True, 
                text=True,
                timeout=45  # <--- Safety Timeout
            )
        except subprocess.TimeoutExpired:
            # If it takes too long, just delete and skip. Speed is priority.
            if os.path.exists(job_file):
                try: os.remove(job_file)
                except: pass
            return None

        area = 0
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if "Estimated number of LCs" in line:
                    parts = line.split()
                    area = int(parts[-1])
                    break
                elif "Number of cells:" in line:
                    parts = line.split()
                    area = int(parts[-1])
                    break
        
        # Cleanup
        if os.path.exists(job_file):
            try: os.remove(job_file)
            except: pass 
            
        return (width, depth, area)

    except Exception:
        return None

# --- MAIN ---
if __name__ == "__main__":
    # Clean up old temp files
    for f in glob.glob("temp_job_*.ys"):
        try: os.remove(f)
        except: pass

    # If CSV doesn't exist, create it with header
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w") as f:
            f.write("Width,Depth,Area\n")

    print(f"--- LIVE TURBO MODE (BALANCED) ---")
    print(f"Target: {TOTAL_SAMPLES} samples")
    print(f"Max Depth: {MAX_DEPTH}")
    print(f"Using: {CORES_TO_USE} CPU Cores")
    print("-" * 30)

    start_time = time.time()
    counter = 0
    
    pool = multiprocessing.Pool(processes=CORES_TO_USE)
    
    with open(CSV_FILE, "a") as f:
        for result in pool.imap_unordered(generate_one_sample, range(TOTAL_SAMPLES)):
            if result is not None and result[2] > 0:
                f.write(f"{result[0]},{result[1]},{result[2]}\n")
                f.flush()
                
                counter += 1
                if counter % 5 == 0: 
                    elapsed = time.time() - start_time
                    speed = counter / elapsed if elapsed > 0 else 0
                    print(f"[{counter}/{TOTAL_SAMPLES}] Saved. Speed: {speed:.2f} samples/sec")

    print(f"\n--- DONE! Generated {counter} samples. ---")
