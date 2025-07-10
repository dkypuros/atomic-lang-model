# Getting Started

# 🛠️ Installation and Setup Guide

> **Complete setup instructions for all platforms and use cases**

This guide covers everything needed to install, build, and run the Atomic Language Model on your system.

## 📋 System Requirements

### Minimum Requirements
- **OS**: Linux, macOS, or Windows
- **RAM**: 2GB available memory
- **Storage**: 500MB free space
- **Internet**: For initial setup only

### Recommended Requirements  
- **OS**: Linux (Ubuntu 20.04+), macOS (10.15+), Windows 10+
- **RAM**: 4GB+ available memory
- **Storage**: 2GB free space (for development)
- **CPU**: Multi-core processor for faster compilation

## 🚀 Quick Installation

### Method 1: One-Line Setup (Recommended)
```bash
# Install Rust and clone project
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh && \
source ~/.cargo/env && \
git clone https://github.com/user/atomic-lang-model.git && \
cd atomic-lang-model/atomic-lang-model && \
cargo run --release
```

### Method 2: Step-by-Step Setup
```bash
# 1. Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# 2. Verify installation
rustc --version && cargo --version

# 3. Clone repository
git clone https://github.com/user/atomic-lang-model.git
cd atomic-lang-model/atomic-lang-model

# 4. Build and run
cargo build --release
cargo run --release
```

## 🔧 Platform-Specific Instructions

### Linux (Ubuntu/Debian)
```bash
# Update package manager
sudo apt update

# Install build essentials (if needed)
sudo apt install build-essential git curl

# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Continue with clone and build...
```

### macOS
```bash
# Install Xcode command line tools (if needed)
xcode-select --install

# Install Rust via rustup
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env

# Continue with clone and build...
```

### Windows
```powershell
# Option 1: Using Windows Subsystem for Linux (WSL) - Recommended
wsl --install
# Then follow Linux instructions inside WSL

# Option 2: Native Windows
# 1. Download and install rustup-init.exe from https://rustup.rs/
# 2. Open Command Prompt or PowerShell
# 3. Run: rustup-init.exe
# 4. Follow installation prompts
# 5. Restart terminal and continue with git clone...
```

## 🔬 Advanced Setup Options

### Development Environment
```bash
# Install additional tools for development
rustup component add rustfmt clippy

# Install Coq for formal verification (optional)
# Ubuntu/Debian:
sudo apt install coq

# macOS:
brew install coq

# Windows:
# Download from https://coq.inria.fr/
```

### Performance Optimization
```bash
# Install LLVM for better optimization (optional)
# Ubuntu/Debian:
sudo apt install llvm

# macOS:
brew install llvm

# Configure Rust to use system LLVM
export RUSTFLAGS="-C link-arg=-fuse-ld=lld"
```

### Cross-Compilation Setup
```bash
# Add targets for different architectures
rustup target add x86_64-unknown-linux-musl    # Static Linux
rustup target add aarch64-unknown-linux-gnu    # ARM64 Linux
rustup target add x86_64-pc-windows-gnu        # Windows
rustup target add wasm32-unknown-unknown       # WebAssembly

# Build for specific target
cargo build --release --target x86_64-unknown-linux-musl
```

## ✅ Verification Steps

### Test Installation
```bash
# 1. Check Rust installation
rustc --version
# Expected: rustc 1.70.0 (or newer)

cargo --version  
# Expected: cargo 1.70.0 (or newer)

# 2. Clone and enter directory
git clone https://github.com/user/atomic-lang-model.git
cd atomic-lang-model/atomic-lang-model

# 3. Build project
cargo build --release
# Expected: Successful compilation

# 4. Run demo
cargo run --release
# Expected: Recursive language generation demo

# 5. Run tests
cargo test --release
# Expected: All tests pass
```

### Verify Mathematical Properties
```bash
# Test core recursive functionality
cargo test test_an_bn_generation
cargo test test_recursive_capability
cargo test test_complete_recursive_proof

# All should show: test result: ok
```

### Check Binary Size
```bash
# Build optimized binary
cargo build --release --profile min-size

# Check size (should be <50kB)
ls -lh target/release/atomic-lm
# or on Windows: dir target\release\atomic-lm.exe
```

## 🔧 Configuration Options

### Build Profiles
```toml
# In Cargo.toml, these profiles are available:

[profile.release]        # Standard optimized build
[profile.min-size]      # Smallest possible binary
[profile.dev]           # Fast compilation, debug symbols
```

### Feature Flags
```bash
# Available features:
cargo build --features "std"         # Standard library (default)
cargo build --features "no_std"      # No standard library
cargo build --features "wasm"        # WebAssembly target
cargo build --features "bench"       # Benchmarking tools
```

### Environment Variables
```bash
# Compilation settings
export RUSTFLAGS="-C opt-level=z -C link-arg=-s"  # Maximum size optimization
export CARGO_BUILD_JOBS=4                         # Parallel compilation

# Runtime settings  
export RUST_LOG=debug                             # Debug logging
export RUST_BACKTRACE=1                          # Error backtraces
```

## 🚨 Troubleshooting

### Common Issues

**"rustc: command not found"**
```bash
# Solution: Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source ~/.cargo/env
```

**"linker not found"**
```bash
# Ubuntu/Debian:
sudo apt install build-essential

# macOS:
xcode-select --install

# Windows: Install Visual Studio Build Tools
```

**"failed to compile"**
```bash
# Update Rust to latest version
rustup update

# Clean and rebuild
cargo clean
cargo build --release
```

**"tests are failing"**
```bash
# Run with verbose output
cargo test -- --nocapture

# Run specific test
cargo test test_an_bn_generation -- --nocapture
```

**Binary size too large**
```bash
# Use size-optimized profile
cargo build --release --profile min-size

# Strip symbols manually (Linux/macOS)
strip target/release/atomic-lm
```

### Platform-Specific Issues

**Linux: Missing dependencies**
```bash
sudo apt update
sudo apt install build-essential pkg-config libssl-dev
```

**macOS: Outdated Xcode**
```bash
xcode-select --install
sudo xcode-select --reset
```

**Windows: Compilation errors**
```powershell
# Install Visual Studio Build Tools
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Or use WSL for Linux compatibility
wsl --install
```

## 🎯 Verification Checklist

After setup, verify these work:

- [ ] `rustc --version` shows 1.70+
- [ ] `cargo --version` shows 1.70+  
- [ ] `git clone` completes successfully
- [ ] `cargo build --release` compiles without errors
- [ ] `cargo run --release` shows demo output
- [ ] `cargo test` passes all tests
- [ ] Binary size is <50kB when optimized
- [ ] Mathematical properties are verified

## 🚀 Next Steps

Once installation is complete:

1. **🎮 Try the Demo**: `cargo run --release`
2. **📖 Read the Guide**: [Quick Start Guide](../atomic-lang-model/QUICKSTART.md)
3. **🧪 Run Tests**: `cargo test --release`
4. **💻 Explore Code**: Browse `src/lib.rs`
5. **📚 Learn Theory**: [Recursive Language Overview](recursive-language-overview.md)

## 🤝 Getting Help

If you encounter issues:

1. **📖 Check**: This troubleshooting section
2. **🔍 Search**: [GitHub Issues](https://github.com/user/atomic-lang-model/issues)
3. **💬 Ask**: Open a new issue with your system details
4. **📧 Contact**: Maintainers for installation support

Include this information when reporting issues:
- Operating system and version
- Rust version (`rustc --version`)
- Complete error message
- Steps you followed

---

**Ready to explore recursive language processing? Your environment is now set up for mathematical discovery!**