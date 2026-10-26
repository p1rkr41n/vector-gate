# ==============================================================================
# STAGE 1: Build Vector Smart Gate Engine from Rust source
# ==============================================================================
FROM rust:slim AS builder

WORKDIR /usr/src/vector-gate

# Copy manifests
COPY vector-gate/Cargo.toml vector-gate/Cargo.lock* ./

# Pre-build dependencies for caching
RUN mkdir -p src && \
    echo "fn main() {}" > src/main.rs && \
    cargo build --release && \
    rm -rf src target/release/vector-gate target/release/deps/vector_gate*

# Copy real source code and build optimized release binary
COPY vector-gate/src ./src
RUN touch src/*.rs && \
    cargo build --release && \
    strip target/release/vector-gate && \
    cp target/release/vector-gate /usr/local/bin/vector-gate

# ==============================================================================
# STAGE 2: Production Vector Smart Gate Runtime Container
# ==============================================================================
FROM timberio/vector:latest-debian

LABEL maintainer="Antigravity Senior AI Architect"
LABEL description="Vector Smart Gate (Multi-Protocol Ingress & Transpiler)"

USER root

# Install runtime dependencies (libssl, curl for healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy compiled vector-gate binary from builder stage
COPY --from=builder /usr/local/bin/vector-gate /usr/local/bin/vector-gate
RUN chmod +x /usr/local/bin/vector-gate

# Copy unified Vector configuration
COPY deploy/config/vector.yaml /etc/vector/vector.yaml

# Create directory structure for vector logs, vrl plugins, and state
RUN mkdir -p /var/log/vector /var/lib/vector /etc/vector/vrl /tmp && \
    chmod 777 /var/log/vector /var/lib/vector /etc/vector/vrl /tmp

# Copy default hierarchical VRL plugins
COPY deploy/vrl/ /etc/vector/vrl/
RUN chmod -R 777 /etc/vector/vrl

# Expose the polymorphic ingress port
EXPOSE 5000

# Health check ensuring single-port gate is responding
HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
  CMD curl -sf http://127.0.0.1:5000/ -X POST -d 'healthcheck' || exit 1

# Supervised entrypoint: Vector Gate launches and supervises Vector Core
ENTRYPOINT ["/usr/local/bin/vector-gate", "run", "-c", "/etc/vector/vector.yaml"]
