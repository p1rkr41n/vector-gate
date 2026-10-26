# ==============================================================================
# VECTOR SMART GATE CONTAINER: MULTI-PROTOCOL INGRESS (TYPE: ANY)
# ==============================================================================
FROM timberio/vector:latest-debian

LABEL maintainer="Antigravity Senior AI Architect"
LABEL description="Vector with Integrated Phase 0 Smart Gate (type: any)"

USER root

# Install libssl and curl for healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy pre-compiled stripped Turbo-Kernel Vector Gate binary
COPY bin/vector-gate /usr/local/bin/vector-gate
RUN chmod +x /usr/local/bin/vector-gate

# Copy unified Vector configuration with Phase 0 Gate
COPY config/vector.yaml /etc/vector/vector.yaml

# Create directory for vector logs, vrl plugins, and state
RUN mkdir -p /var/log/vector /var/lib/vector /etc/vector/vrl /tmp && \
    chmod 777 /var/log/vector /var/lib/vector /etc/vector/vrl /tmp

# Copy default hierarchical VRL plugins
COPY vrl/ /etc/vector/vrl/
RUN chmod -R 777 /etc/vector/vrl

# Expose the single polymorphic ingress port
EXPOSE 5000

# Health check ensuring single-port gate is responding
HEALTHCHECK --interval=5s --timeout=3s --retries=3 \
  CMD curl -sf http://127.0.0.1:5000/ -X POST -d 'healthcheck' || exit 1

# Supervised entrypoint: Vector Gate Phase 0 launches and supervises Vector Core
ENTRYPOINT ["/usr/local/bin/vector-gate", "run", "-c", "/etc/vector/vector.yaml"]

