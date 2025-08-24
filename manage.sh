#!/bin/bash
# Project Management Script - Generic Template

set -e

PROJECT_NAME="Weather app"
SERVICE_NAME="weather_app"
PORT="5000"
PYTHON_COMMAND="weather_app.py"

show_help() {
    echo "🚀 $PROJECT_NAME Management"
    echo "================================"
    echo ""
    echo "Commands:"
    echo "  setup     - Set up development environment"
    echo "  start     - Start $SERVICE_NAME"
    echo "  stop      - Stop $SERVICE_NAME" 
    echo "  restart   - Restart $SERVICE_NAME"
    echo "  status    - Check $SERVICE_NAME status"
    echo "  logs      - View $SERVICE_NAME logs"
    echo "  clean     - Clean up temporary files"
    echo ""
    echo "Examples:"
    echo "  ./manage.sh setup"
    echo "  ./manage.sh start"
}

setup_environment() {
    echo "🔧 Setting up $PROJECT_NAME development environment..."
    
    # Create virtual environment
    if [ ! -d ".venv" ]; then
        echo "📦 Creating Python virtual environment..."
        python3 -m venv .venv
    fi
    
    # Install dependencies
    echo "📥 Installing dependencies..."
    .venv/bin/pip install --upgrade pip
    if [ -f "requirements.txt" ]; then
        .venv/bin/pip install -r requirements.txt
    fi
    
    # Make scripts executable
    echo "🔧 Making scripts executable..."
    chmod +x scripts/*.sh 2>/dev/null || true
    
    echo "✅ Environment setup complete!"
    echo "💡 Next: ./manage.sh start"
}

start_service() {
    echo "🚀 Starting $SERVICE_NAME..."
    
    # Check if already running
    if [ -f "${SERVICE_NAME}.pid" ]; then
        PID=$(cat "${SERVICE_NAME}.pid")
        if ps -p $PID > /dev/null 2>&1; then
            echo "⚠️  $SERVICE_NAME is already running (PID: $PID)"
            echo "🌐 Access at: http://localhost:5000"
            return 0
        else
            echo "🧹 Removing stale PID file"
            rm -f "${SERVICE_NAME}.pid"
        fi
    fi
    
    # Start the service
    .venv/bin/python $PYTHON_COMMAND &
    PID=$!
    echo $PID > "${SERVICE_NAME}.pid"
    
    # Wait a moment and verify it started
    sleep 2
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ $SERVICE_NAME started successfully (PID: $PID)"
        echo "🌐 Access at: http://localhost:5000"
    else
        echo "❌ Failed to start $SERVICE_NAME"
        rm -f "${SERVICE_NAME}.pid"
        exit 1
    fi
}

stop_service() {
    echo "🛑 Stopping $SERVICE_NAME..."
    
    if [ -f "${SERVICE_NAME}.pid" ]; then
        PID=$(cat "${SERVICE_NAME}.pid")
        if ps -p $PID > /dev/null 2>&1; then
            kill $PID
            rm -f "${SERVICE_NAME}.pid"
            echo "✅ $SERVICE_NAME stopped"
        else
            echo "⚠️  $SERVICE_NAME was not running"
            rm -f "${SERVICE_NAME}.pid"
        fi
    else
        echo "⚠️  No PID file found"
    fi
}

check_status() {
    # Check port availability
    if netstat -tuln 2>/dev/null | grep -q ":$PORT "; then
        echo "🔌 Port $PORT: In use"
    else
        echo "🔌 Port $PORT: Available"
    fi
    
    # Check service status
    if [ -f "${SERVICE_NAME}.pid" ]; then
        PID=$(cat "${SERVICE_NAME}.pid")
        if ps -p $PID > /dev/null 2>&1; then
            echo "✅ $SERVICE_NAME is running (PID: $PID)"
            echo "🌐 Access at: http://localhost:5000"
        else
            echo "❌ $SERVICE_NAME is not running (stale PID file)"
            rm -f "${SERVICE_NAME}.pid"
        fi
    else
        echo "❌ $SERVICE_NAME is not running"
    fi
}

view_logs() {
    if [ -f "${SERVICE_NAME}.log" ]; then
        tail -f "${SERVICE_NAME}.log"
    else
        echo "⚠️  No log file found"
    fi
}

clean_up() {
    echo "🧹 Cleaning up temporary files..."
    rm -f *.pid *.log
    rm -rf __pycache__/ */__pycache__/
    rm -rf .pytest_cache/
    echo "✅ Cleanup complete"
}

# Main command handling
case "${1:-help}" in
    setup)
        setup_environment
        ;;
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        stop_service
        sleep 1
        start_service
        ;;
    status)
        check_status
        ;;
    logs)
        view_logs
        ;;
    clean)
        clean_up
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
