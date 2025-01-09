import sys

def main():
    # Force immediate output
    print("Test 1", flush=True)
    sys.stdout.flush()
    
    # Write directly to stderr
    sys.stderr.write("Test 2\n")
    sys.stderr.flush()
    
    # Try different print methods
    print("Test 3", file=sys.stdout, flush=True)
    print("Test 4", file=sys.stderr, flush=True)

if __name__ == "__main__":
    print("Starting basic test...", flush=True)
    main()
    print("Basic test complete!", flush=True) 