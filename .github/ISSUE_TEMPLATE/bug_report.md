---
name: Bug Report
description: Report a bug
title: "[BUG] "
labels: [bug]
body:
  - type: input
    id: environment
    attributes:
      label: Environment
      description: "OS/Browser/Device details"
      placeholder: "e.g., Windows 11, Chrome 120"
  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: "Detailed steps to trigger the bug"
  - type: textarea
    id: expected-behavior
    attributes:
      label: Expected Behavior
  - type: checkboxes
    id: logs
    attributes:
      label: Include Logs?
      options:
        - label: "I included relevant logs/screenshots"
---
