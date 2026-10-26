.PHONY: all build build-local run stop status logs test test-all test-matrix test-onion clean

IMAGE_NAME ?= l1ghtg3m/vector-gate:2.4.3
IMAGE_LATEST ?= l1ghtg3m/vector-gate:latest

all: build

# Build complete Vector Gate Docker image from source (multi-stage Rust + Vector)
build:
	docker build -t $(IMAGE_NAME) -t $(IMAGE_LATEST) .

# Build raproxy binary locally on host (requires Rust/Cargo)
build-local:
	cargo build --release --manifest-path raproxy/Cargo.toml
	mkdir -p docker_gate/bin
	cp raproxy/target/release/raproxy docker_gate/bin/vector-gate
	strip docker_gate/bin/vector-gate

# Start Vector Gate production container stack
run:
	docker compose up -d

# Stop Vector Gate container stack
stop:
	docker compose down

# Check container status
status:
	docker compose ps

# View live container logs
logs:
	docker compose logs -f

# Verify gate health check on port 5000
test:
	curl -sf http://127.0.0.1:5000/ -X POST -H "Content-Type: application/json" -d '{"ping":"vector-gate-ok"}' && echo "\n✅ Vector Gate Health Check Passed!"

# Run automated QA test suites in tests/
test-all:
	python3 tests/run_all_tests.py --all

test-matrix:
	python3 tests/run_all_tests.py --suite matrix

test-onion:
	python3 tests/run_all_tests.py --suite onion

# Clean build artifacts
clean:
	rm -rf raproxy/target docker_gate/output/*.log docker_gate/output/*.ndjson
