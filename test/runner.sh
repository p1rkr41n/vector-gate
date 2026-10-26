#!/usr/bin/env bash
# ==============================================================================
# VECTOR STANDALONE BENCHMARK & INGESTION RUNNER
# Usage:
#   ./runner.sh -f [file_config.conf]
#   ./runner.sh                        (Auto-picks first *.conf in current dir)
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE=""

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Default parameters (can be overridden by config file or CLI flags)
TARGET_IP="127.0.0.1"
TARGET_PORT="5000"
LOG_TYPE="syslog_rfc5424"
TOTAL_EVENTS=100000
CONCURRENCY=8
BATCH_SIZE=500
MOCK_LOG_FILE=""
MUTATE="true"
OUTPUT_JSON="false"
START_VECTOR="false"
VECTOR_CONFIG=""

print_usage() {
    echo -e "${BOLD}Usage:${NC}"
    echo -e "  $0 -f <config_file.conf>      Run benchmark using specified configuration"
    echo -e "  $0                            Auto-discover first *.conf file in current directory"
    echo -e "  $0 -h, --help                 Show this help message"
    echo ""
    echo -e "${BOLD}Configuration File Format (*.conf):${NC}"
    echo -e "  TARGET_IP=127.0.0.1"
    echo -e "  TARGET_PORT=5000"
    echo -e "  LOG_TYPE=syslog_rfc5424"
    echo -e "  TOTAL_EVENTS=100000"
    echo -e "  CONCURRENCY=8"
    echo -e "  BATCH_SIZE=500"
    echo -e "  MUTATE=true"
    echo -e "  OUTPUT_JSON=false"
    exit 1
}

# Parse CLI arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -f|--file)
            CONFIG_FILE="$2"
            shift 2
            ;;
        -h|--help)
            print_usage
            ;;
        *)
            # If argument ends with .conf, treat as config file
            if [[ "$1" == *.conf ]]; then
                CONFIG_FILE="$1"
                shift
            else
                echo -e "${RED}[ERROR] Unknown option: $1${NC}"
                print_usage
            fi
            ;;
    esac
done

# If config file is not specified, auto-discover first *.conf in current dir or test/
if [[ -z "$CONFIG_FILE" ]]; then
    if [[ -f "$PWD/default.conf" ]]; then
        FOUND_CONF="$PWD/default.conf"
    elif [[ -f "$SCRIPT_DIR/default.conf" ]]; then
        FOUND_CONF="$SCRIPT_DIR/default.conf"
    else
        FOUND_CONF=$(find "$PWD" "$SCRIPT_DIR" -maxdepth 1 -name "*.conf" 2>/dev/null | sort | head -n 1)
    fi
    if [[ -n "$FOUND_CONF" && -f "$FOUND_CONF" ]]; then
        CONFIG_FILE="$FOUND_CONF"
        echo -e "${CYAN}[INFO] Auto-discovered configuration file:${NC} ${BOLD}$CONFIG_FILE${NC}"
    else
        echo -e "${RED}[ERROR] No configuration file specified (-f) and no *.conf found in $PWD or $SCRIPT_DIR${NC}"
        exit 1
    fi
fi

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo -e "${RED}[ERROR] Configuration file not found: $CONFIG_FILE${NC}"
    exit 1
fi

echo -e "${BLUE}================================================================================${NC}"
echo -e "${BOLD}${CYAN}🚀 LOADING VECTOR TEST CONFIGURATION:${NC} ${YELLOW}$CONFIG_FILE${NC}"
echo -e "${BLUE}================================================================================${NC}"

# Parse key=value from configuration file safely
while IFS='=' read -r key val || [[ -n "$key" ]]; do
    # Trim whitespace
    key=$(echo "$key" | tr -d '\r' | xargs)
    # Skip empty lines or comments
    [[ -z "$key" || "$key" =~ ^# ]] && continue
    
    val=$(echo "$val" | tr -d '\r' | xargs)
    # Remove enclosing quotes if any
    val="${val%\"}"
    val="${val#\"}"
    val="${val%\'}"
    val="${val#\'}"

    case "$key" in
        TARGET_IP|IP) TARGET_IP="$val" ;;
        TARGET_PORT|PORT) TARGET_PORT="$val" ;;
        LOG_TYPE|TYPE) LOG_TYPE="$val" ;;
        TOTAL_EVENTS|EVENTS) TOTAL_EVENTS="$val" ;;
        CONCURRENCY) CONCURRENCY="$val" ;;
        BATCH_SIZE) BATCH_SIZE="$val" ;;
        MOCK_LOG_FILE) MOCK_LOG_FILE="$val" ;;
        MUTATE) MUTATE="$val" ;;
        OUTPUT_JSON) OUTPUT_JSON="$val" ;;
        START_VECTOR) START_VECTOR="$val" ;;
        VECTOR_CONFIG) VECTOR_CONFIG="$val" ;;
    esac
done < "$CONFIG_FILE"

# Auto-resolve mock log file if not specified
if [[ -z "$MOCK_LOG_FILE" ]]; then
    case "$LOG_TYPE" in
        syslog_rfc5424) MOCK_LOG_FILE="$SCRIPT_DIR/mock_logs/syslog_rfc5424.log" ;;
        syslog_rfc3164) MOCK_LOG_FILE="$SCRIPT_DIR/mock_logs/syslog_rfc3164.log" ;;
        ndjson|ndjson_http|http) MOCK_LOG_FILE="$SCRIPT_DIR/mock_logs/ndjson_http.log" ;;
        datadog|datadog_intake) MOCK_LOG_FILE="$SCRIPT_DIR/mock_logs/datadog_intake.json" ;;
        splunk|splunk_hec) MOCK_LOG_FILE="$SCRIPT_DIR/mock_logs/splunk_hec.json" ;;
        nginx|nginx_combined) MOCK_LOG_FILE="$SCRIPT_DIR/mock_logs/nginx_combined.log" ;;
        cisco_asa) MOCK_LOG_FILE="$SCRIPT_DIR/mock_logs/cisco_asa.log" ;;
        suricata|suricata_eve) MOCK_LOG_FILE="$SCRIPT_DIR/mock_logs/suricata_eve.json" ;;
        cef|checkpoint_cef) MOCK_LOG_FILE="$SCRIPT_DIR/mock_logs/checkpoint_cef.log" ;;
        fortigate_kv) MOCK_LOG_FILE="$SCRIPT_DIR/mock_logs/fortigate_kv.log" ;;
        auditd) MOCK_LOG_FILE="$SCRIPT_DIR/mock_logs/auditd.log" ;;
        zeek) MOCK_LOG_FILE="$SCRIPT_DIR/mock_logs/zeek_conn.json" ;;
        *) MOCK_LOG_FILE="$SCRIPT_DIR/mock_logs/syslog_rfc5424.log" ;;
    esac
fi

# Resolve relative path for MOCK_LOG_FILE
if [[ ! "$MOCK_LOG_FILE" = /* ]]; then
    MOCK_LOG_FILE="$(cd "$(dirname "$CONFIG_FILE")" && pwd)/$MOCK_LOG_FILE"
fi

if [[ ! -f "$MOCK_LOG_FILE" ]]; then
    echo -e "${RED}[ERROR] Mock log file does not exist: $MOCK_LOG_FILE${NC}"
    exit 1
fi

echo -e "  • ${BOLD}Target Destination :${NC} ${GREEN}$TARGET_IP:$TARGET_PORT${NC}"
echo -e "  • ${BOLD}Log Protocol Type  :${NC} ${GREEN}$LOG_TYPE${NC}"
echo -e "  • ${BOLD}Total Events Count :${NC} ${YELLOW}$TOTAL_EVENTS${NC}"
echo -e "  • ${BOLD}Concurrency Workers:${NC} ${CYAN}$CONCURRENCY connections${NC}"
echo -e "  • ${BOLD}Batch Size         :${NC} ${CYAN}$BATCH_SIZE events / frame${NC}"
echo -e "  • ${BOLD}Mock Template File :${NC} $MOCK_LOG_FILE"
echo -e "  • ${BOLD}In-Memory Mutation :${NC} $MUTATE"
echo ""

# Handle optional local Vector start if requested
VECTOR_PID=""
cleanup() {
    if [[ -n "$VECTOR_PID" ]]; then
        echo -e "\n${YELLOW}[INFO] Stopping standalone Vector process (PID $VECTOR_PID)...${NC}"
        kill "$VECTOR_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT INT TERM

if [[ "$START_VECTOR" == "true" ]]; then
    if [[ -z "$VECTOR_CONFIG" || ! -f "$VECTOR_CONFIG" ]]; then
        echo -e "${RED}[ERROR] START_VECTOR=true but VECTOR_CONFIG not found: $VECTOR_CONFIG${NC}"
        exit 1
    fi
    VECTOR_BIN="$SCRIPT_DIR/bin/vector"
    if [[ ! -x "$VECTOR_BIN" ]]; then
        VECTOR_BIN="vector"
    fi
    echo -e "${CYAN}[INFO] Launching standalone Vector with config: $VECTOR_CONFIG${NC}"
    $VECTOR_BIN --config "$VECTOR_CONFIG" > /tmp/vector_runner.log 2>&1 &
    VECTOR_PID=$!
    sleep 1.5
    if ! kill -0 "$VECTOR_PID" 2>/dev/null; then
        echo -e "${RED}[ERROR] Vector process failed to start! Check /tmp/vector_runner.log${NC}"
        cat /tmp/vector_runner.log
        exit 1
    fi
    echo -e "${GREEN}[INFO] Vector running on PID $VECTOR_PID${NC}"
fi

# Build arguments for mixer_engine.py
MIXER_ENGINE="$SCRIPT_DIR/lib/mixer_engine.py"
ENGINE_ARGS=(
    "--target-ip" "$TARGET_IP"
    "--target-port" "$TARGET_PORT"
    "--log-file" "$MOCK_LOG_FILE"
    "--log-type" "$LOG_TYPE"
    "--total-events" "$TOTAL_EVENTS"
    "--concurrency" "$CONCURRENCY"
    "--batch-size" "$BATCH_SIZE"
)

if [[ "$MUTATE" == "true" ]]; then
    ENGINE_ARGS+=("--mutate")
else
    ENGINE_ARGS+=("--no-mutate")
fi

if [[ "$OUTPUT_JSON" == "true" ]]; then
    ENGINE_ARGS+=("--json")
fi

# Run the benchmark engine
python3 "$MIXER_ENGINE" "${ENGINE_ARGS[@]}"
EXIT_CODE=$?

exit $EXIT_CODE
