#!/bin/bash

if $VSCODE_DEBUGGING ; then
  echo "⏳ Waiting for VS Code debugger to attach ⏳"
  python -m debugpy --wait-for-client --listen 0.0.0.0:5678 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
else
  echo "If you want to debug with VS Code set VSCODE_DEBUGGING=true"
  uvicorn main:app --reload --host 0.0.0.0 --port 8000
fi
