# Wasabi Node Modules Management

This document explains how to use the Wasabi Node Modules Manager to save, restore, and sync `node_modules` directories with Wasabi cloud storage.

## Overview

The Wasabi Node Modules Manager provides intelligent caching and backup of `node_modules` directories to Wasabi cloud storage. This is useful for:

- **Team Collaboration**: Share exact dependency versions across team members
- **CI/CD Optimization**: Cache dependencies to speed up build times
- **Storage Management**: Keep large `node_modules` out of Git while maintaining backups
- **Environment Consistency**: Ensure identical dependencies across development/production

## Features

- ✅ Smart compression using tar.gz for efficient storage
- ✅ Hash-based cache validation using package.json
- ✅ Automatic project detection and metadata tagging
- ✅ Version management with cleanup of old archives
- ✅ Team sync capabilities
- ✅ Integration with existing Wasabi deployment pipeline

## Prerequisites

1. **Wasabi Configuration**: Ensure Wasabi credentials are configured
   ```bash
   ./configure_wasabi_keys.sh
   ```

2. **Python Dependencies**: Required packages
   ```bash
   pip install boto3 python-dotenv
   ```

3. **Node.js Projects**: Projects must have a `package.json` file

## Quick Start

### 1. Initialize a Project

```bash
# Initialize current directory
./wasabi_node_modules.sh init

# Initialize specific project
./wasabi_node_modules.sh init ./frontend
```

This will:
- Add cache files to `.gitignore`
- Create npm scripts for Wasabi management
- Set up project for node_modules syncing

### 2. Upload node_modules

```bash
# Upload current project
./wasabi_node_modules.sh upload

# Upload specific project
./wasabi_node_modules.sh upload ./frontend
```

### 3. Download node_modules

```bash
# Download to current project
./wasabi_node_modules.sh download

# Download to specific project  
./wasabi_node_modules.sh download ./frontend
```

### 4. Smart Sync

```bash
# Sync current project (upload if local newer, download if remote newer)
./wasabi_node_modules.sh sync

# Sync all projects in workspace
./wasabi_node_modules.sh sync --all
```

## Commands Reference

### Basic Commands

| Command | Description | Example |
|---------|-------------|---------|
| `upload` | Upload node_modules to Wasabi | `./wasabi_node_modules.sh upload` |
| `download` | Download node_modules from Wasabi | `./wasabi_node_modules.sh download` |
| `sync` | Smart sync (auto upload/download) | `./wasabi_node_modules.sh sync` |
| `list` | List all cached modules in Wasabi | `./wasabi_node_modules.sh list` |
| `cleanup` | Remove old archives | `./wasabi_node_modules.sh cleanup 5` |

### Management Commands

| Command | Description | Example |
|---------|-------------|---------|
| `init` | Initialize project for Wasabi management | `./wasabi_node_modules.sh init ./frontend` |
| `status` | Show sync status for project(s) | `./wasabi_node_modules.sh status --all` |
| `help` | Show detailed help | `./wasabi_node_modules.sh help` |

### Options

| Option | Description |
|--------|-------------|
| `--all`, `-a` | Process all Node.js projects in workspace |
| `--force`, `-f` | Force download even if local node_modules exists |
| `--keep N` | Keep N latest archives during cleanup (default: 3) |

## Use Cases

### 1. Team Development Workflow

```bash
# Developer A: Share dependencies
npm install
./wasabi_node_modules.sh upload

# Developer B: Get exact same dependencies
./wasabi_node_modules.sh download
# No need to run npm install!
```

### 2. CI/CD Pipeline Integration

```bash
# In your CI/CD script
./wasabi_node_modules.sh download || npm install
./wasabi_node_modules.sh upload  # Cache for next build
```

### 3. Multi-Project Workspace

```bash
# Check status of all projects
./wasabi_node_modules.sh status --all

# Sync all projects at once  
./wasabi_node_modules.sh sync --all
```

### 4. Storage Cleanup

```bash
# List all cached modules
./wasabi_node_modules.sh list

# Clean up old archives, keep 3 latest per project
./wasabi_node_modules.sh cleanup 3
```

## Advanced Usage

### Direct Python Script Usage

For advanced control, use the Python script directly:

```bash
# Upload with explicit project path
python3 wasabi_node_modules_manager.py upload --project ./frontend

# Force download even if local exists
python3 wasabi_node_modules_manager.py download --project ./backend --force

# Cleanup keeping only 1 latest archive
python3 wasabi_node_modules_manager.py cleanup --keep 1
```

### Integration with Package.json

After running `init`, projects get npm scripts:

```json
{
  "scripts": {
    "wasabi:upload": "wasabi-node-modules upload",
    "wasabi:download": "wasabi-node-modules download", 
    "wasabi:sync": "wasabi-node-modules sync"
  }
}
```

Use with:
```bash
npm run wasabi:sync
```

## How It Works

### 1. Hash-Based Validation

The system calculates an MD5 hash of `package.json` to determine if dependencies have changed:

- If hash matches cached version → no sync needed
- If hash differs → upload new version
- If no local `package.json` → download from cache

### 2. Archive Naming

Archives are named using the pattern:
```
{project-name}-{version}-{package-json-hash}.tar.gz
```

Example: `my-app-1.2.0-abc123def456.tar.gz`

### 3. Metadata Storage

Each archive includes metadata:
- Project name and version
- Package.json hash
- Upload timestamp
- Original local path

### 4. Smart Matching

When downloading, the system finds the best match:
1. Exact hash match (preferred)
2. Name + version match
3. Name match (fallback)

## Troubleshooting

### Common Issues

1. **"Wasabi not configured"**
   ```bash
   ./configure_wasabi_keys.sh
   ```

2. **"boto3 not found"**
   ```bash
   pip install boto3 python-dotenv
   ```

3. **"No matching node_modules found"**
   - Ensure the project was uploaded first
   - Check project name in `package.json`
   - Use `list` command to see available archives

4. **Large upload/download times**
   - Node modules can be large (100MB+)
   - Consider using `cleanup` to remove old archives
   - Wasabi provides fast transfers but size matters

### Debug Mode

For detailed logging, set environment variable:
```bash
export WASABI_DEBUG=1
./wasabi_node_modules.sh sync
```

## Integration with Existing Workflow

### With Docker

```dockerfile
# In your Dockerfile
COPY package.json package-lock.json ./
RUN ./wasabi_node_modules.sh download || npm install
RUN ./wasabi_node_modules.sh upload  # Cache for next build
```

### With GitHub Actions

```yaml
- name: Restore node_modules cache
  run: ./wasabi_node_modules.sh download || npm install

- name: Save node_modules cache  
  run: ./wasabi_node_modules.sh upload
  if: success()
```

### With Git Hooks

```bash
# In .git/hooks/post-checkout
#!/bin/bash
./wasabi_node_modules.sh sync

# In .git/hooks/pre-push  
#!/bin/bash
./wasabi_node_modules.sh upload
```

## Security Considerations

- Wasabi credentials are stored in `.env.wasabi` (not committed to Git)
- Archives include only `node_modules` content, no source code
- Metadata includes project info but no sensitive data
- Use Wasabi IAM policies to restrict bucket access

## Performance Tips

1. **Regular Cleanup**: Run cleanup weekly to manage storage costs
2. **Project-Specific Buckets**: Use different buckets for different environments
3. **Compression**: Archives are automatically gzipped for optimal transfer
4. **Parallel Processing**: Use `--all` flag to process multiple projects efficiently

## Monitoring and Analytics

Use `status` and `list` commands to monitor usage:

```bash
# Check status of all projects
./wasabi_node_modules.sh status --all

# See all cached modules with sizes and dates
./wasabi_node_modules.sh list
```

This provides visibility into:
- Which projects have cached dependencies
- Storage usage per project
- Upload/sync activity
- Archive age and cleanup needs
