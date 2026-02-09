# CLI Command Contracts: Phase 1 Todo Console App

**Date**: 2025-01-25
**Branch**: `001-phase1-todo-console`

## Overview

All commands follow the pattern: `<command> [arguments...]`

Commands are case-insensitive. Arguments are space-separated. Quoted strings supported for titles with spaces.

## Commands

### add

Create a new task.

**Syntax**: `add <title> [--priority <high|medium|low>] [--tags <tag1,tag2,...>]`

**Arguments**:
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| title | Yes | - | Task title (quote if contains spaces) |
| --priority | No | medium | Priority level |
| --tags | No | (none) | Comma-separated tags |

**Success Output**:
```
Created task #<id>: "<title>" [<priority>]
```

**Error Outputs**:
| Condition | Message |
|-----------|---------|
| Empty title | Error: Title cannot be empty |
| Invalid priority | Error: Priority must be high, medium, or low |

**Examples**:
```
> add "Buy groceries"
Created task #1: "Buy groceries" [medium]

> add "Urgent meeting" --priority high --tags work,urgent
Created task #2: "Urgent meeting" [high] (tags: work, urgent)
```

---

### list

Display all tasks or filtered results.

**Syntax**: `list [--status <complete|incomplete>] [--priority <high|medium|low>] [--tag <tag>] [--sort <priority|alpha|id>]`

**Arguments**:
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| --status | No | (all) | Filter by completion status |
| --priority | No | (all) | Filter by priority level |
| --tag | No | (all) | Filter by tag |
| --sort | No | id | Sort order |

**Success Output**:
```
Tasks (<count>):
  [<status>] #<id> <title> [<priority>] (tags: <tag1>, <tag2>)
  ...
```

Status indicators: `[ ]` = incomplete, `[x]` = complete

**Empty List Output**:
```
No tasks found.
```

**Examples**:
```
> list
Tasks (3):
  [ ] #1 Buy groceries [high] (tags: shopping)
  [x] #2 Review PR [medium] (tags: work, code)
  [ ] #3 Call mom [low]

> list --status incomplete --sort priority
Tasks (2):
  [ ] #1 Buy groceries [high] (tags: shopping)
  [ ] #3 Call mom [low]
```

---

### complete

Mark a task as complete.

**Syntax**: `complete <id>`

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| id | Yes | Task ID (positive integer) |

**Success Output**:
```
Completed task #<id>: "<title>"
```

**Already Complete Output**:
```
Task #<id> is already complete.
```

**Error Outputs**:
| Condition | Message |
|-----------|---------|
| Invalid ID format | Error: ID must be a positive integer |
| Task not found | Error: Task #<id> not found |

**Examples**:
```
> complete 1
Completed task #1: "Buy groceries"

> complete 1
Task #1 is already complete.

> complete 99
Error: Task #99 not found
```

---

### uncomplete

Mark a task as incomplete.

**Syntax**: `uncomplete <id>`

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| id | Yes | Task ID (positive integer) |

**Success Output**:
```
Marked task #<id> as incomplete: "<title>"
```

**Already Incomplete Output**:
```
Task #<id> is already incomplete.
```

**Error Outputs**:
| Condition | Message |
|-----------|---------|
| Invalid ID format | Error: ID must be a positive integer |
| Task not found | Error: Task #<id> not found |

---

### update

Update task title or priority.

**Syntax**: `update <id> [--title <new_title>] [--priority <high|medium|low>]`

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| id | Yes | Task ID |
| --title | No | New title |
| --priority | No | New priority |

At least one of `--title` or `--priority` must be provided.

**Success Output**:
```
Updated task #<id>: "<title>" [<priority>]
```

**Error Outputs**:
| Condition | Message |
|-----------|---------|
| Task not found | Error: Task #<id> not found |
| Empty title | Error: Title cannot be empty |
| Invalid priority | Error: Priority must be high, medium, or low |
| No changes | Error: Provide --title or --priority to update |

**Examples**:
```
> update 1 --title "Buy organic groceries"
Updated task #1: "Buy organic groceries" [high]

> update 1 --priority medium
Updated task #1: "Buy organic groceries" [medium]
```

---

### delete

Remove a task.

**Syntax**: `delete <id>`

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| id | Yes | Task ID |

**Success Output**:
```
Deleted task #<id>: "<title>"
```

**Error Outputs**:
| Condition | Message |
|-----------|---------|
| Task not found | Error: Task #<id> not found |

---

### tag

Add or remove tags from a task.

**Syntax**: `tag <id> <add|remove> <tag>`

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| id | Yes | Task ID |
| action | Yes | "add" or "remove" |
| tag | Yes | Tag name |

**Success Output**:
```
Added tag "<tag>" to task #<id>
Removed tag "<tag>" from task #<id>
```

**Error Outputs**:
| Condition | Message |
|-----------|---------|
| Task not found | Error: Task #<id> not found |
| Empty tag | Error: Tag cannot be empty |
| Invalid action | Error: Action must be "add" or "remove" |

---

### search

Find tasks by keyword.

**Syntax**: `search <keyword>`

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| keyword | Yes | Search term (case-insensitive) |

**Success Output**:
```
Search results for "<keyword>" (<count>):
  [<status>] #<id> <title> [<priority>]
  ...
```

**No Results Output**:
```
No tasks found matching "<keyword>".
```

**Examples**:
```
> search groceries
Search results for "groceries" (1):
  [ ] #1 Buy organic groceries [medium]
```

---

### help

Display available commands.

**Syntax**: `help [<command>]`

**Arguments**:
| Argument | Required | Description |
|----------|----------|-------------|
| command | No | Specific command for detailed help |

**General Help Output**:
```
Todo App - Available Commands:
  add <title>         Create a new task
  list                Display all tasks
  complete <id>       Mark task as complete
  uncomplete <id>     Mark task as incomplete
  update <id>         Update task details
  delete <id>         Remove a task
  tag <id>            Add or remove tags
  search <keyword>    Find tasks by keyword
  help [command]      Show this help
  exit                Quit the application

Use "help <command>" for detailed usage.
```

---

### exit

Quit the application.

**Syntax**: `exit` or `quit`

**Output**:
```
Goodbye!
```

---

## Error Handling

### Unknown Command

```
> foobar
Unknown command: "foobar". Type "help" for available commands.
```

### Parse Errors

```
> add
Error: Missing required argument: title. Usage: add <title> [--priority <level>] [--tags <tags>]
```

## Input/Output Format

- **Input**: Single line text commands via stdin
- **Output**: Human-readable text to stdout
- **Errors**: Prefixed with "Error:" to stderr
- **Encoding**: UTF-8
