import time
import httpx
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def run_benchmark():
    """
    Simulates a throughput benchmark against the local LLM endpoint.
    If the endpoint is unavailable (e.g. running outside Docker), it mocks the result.
    """
    endpoint = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen2.5:0.5b",
        "prompt": "Explain the significance of structured data in AI.",
        "stream": False
    }

    logging.info("Warming up local inference engine...")
    try:
        start_time = time.time()
        response = httpx.post(endpoint, json=payload, timeout=10.0)
        response.raise_for_status()
        duration = time.time() - start_time
        tokens = len(response.json().get("response", "").split())
        tps = tokens / duration if duration > 0 else 0
        logging.info(f"Real Benchmark Success: {tps:.2f} tokens/sec")
    except httpx.RequestError:
        logging.warning("Local engine not reachable at localhost:11434. Running simulated benchmark results.")
        # Mock results for quickstart demonstration
        time.sleep(1.5)
        logging.info("Simulated Benchmark: Model loaded successfully into VRAM constraints.")
        logging.info("Simulated Benchmark: Throughput: 42.5 tokens/sec")
        logging.info("Simulated Benchmark: Latency (TTFT): 240ms")

if __name__ == "__main__":
    run_benchmark()
