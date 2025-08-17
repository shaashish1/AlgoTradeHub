#!/usr/bin/env python3
"""
Project Structure Organizer
Cleans up the root directory by organizing files into logical folders
"""

import os
import shutil
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def organize_project():
    """Organize project files into logical structure"""
    
    console.print(Panel.fit("🗂️  Project Structure Organizer", style="bold blue"))
    
    # Define organization structure
    organization_plan = {
        "docs/": [
            "README.md", "FRONTEND_README.md", "FEATURES_IMPLEMENTED.md",
            "install_nodejs_guide.md", "replit.md", "COMMIT_MESSAGE.md",
            "LICENSE"
        ],
        "scripts/": [
            "quick_start.py", "simple_test.py", "launch_full_app.py",
            "organize_project.py", "start_application.py", "system_status.py",
            "CCXT_ListofExchange.py"
        ],
        "assets/": [
            "backtest dashboard.png", "demo_realtime trade dashboard.png",
            "landing_page.png", "login dashboard.png", 
            "user input configuration dashboard.png",
            "ChatGPT Image Jul 17, 2025, 05_37_38 PM.png"
        ],
        "config/": [
            # config/ already exists, just mention it
        ],
        "core/": [
            "app.py", "main.py", "main_fixed.py", "backtest.py", 
            "strategy.py", "database.py", "models.py"
        ],
        "archive/": [
            # For old/unused files
            ".replit", "AlgoTradeHub.code-workspace", "uv.lock", "pyproject.toml"
        ]
    }
    
    # Show current structure
    console.print("\n📁 Current root directory files:")
    root_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    table = Table(title="Files to Organize")
    table.add_column("File", style="cyan")
    table.add_column("Proposed Location", style="green")
    table.add_column("Action", style="yellow")
    
    moves_planned = []
    
    for target_dir, files in organization_plan.items():
        for file in files:
            if file in root_files:
                table.add_row(file, target_dir, "Move")
                moves_planned.append((file, target_dir))
    
    # Show files that will stay in root
    core_files = [
        "config.yaml", "requirements.txt", "requirements_core.txt",
        "webapp.log", "algotrading.db"
    ]
    
    for file in root_files:
        if file not in [item[0] for item in moves_planned] and file not in core_files:
            if not any(file.endswith(ext) for ext in ['.pyc', '.log', '.db']):
                table.add_row(file, "root/", "Keep")
    
    console.print(table)
    
    # Ask for confirmation
    if not moves_planned:
        console.print("✅ Project is already well organized!", style="green")
        return
    
    console.print(f"\n📋 Planning to move {len(moves_planned)} files")
    
    proceed = input("\nProceed with organization? (y/N): ").lower().strip()
    if proceed != 'y':
        console.print("❌ Organization cancelled", style="yellow")
        return
    
    # Perform organization
    console.print("\n🔄 Organizing files...", style="bold blue")
    
    for file, target_dir in moves_planned:
        try:
            # Create target directory if it doesn't exist
            Path(target_dir).mkdir(exist_ok=True)
            
            # Move file
            source = Path(file)
            target = Path(target_dir) / file
            
            if source.exists():
                shutil.move(str(source), str(target))
                console.print(f"✅ Moved {file} → {target_dir}", style="green")
            
        except Exception as e:
            console.print(f"❌ Failed to move {file}: {e}", style="red")
    
    # Create a new simplified structure overview
    console.print("\n📊 New Project Structure:", style="bold green")
    
    structure_table = Table(title="Organized Project Structure")
    structure_table.add_column("Directory", style="cyan")
    structure_table.add_column("Purpose", style="green")
    structure_table.add_column("Key Files", style="yellow")
    
    structure_info = [
        ("root/", "Core application", "config.yaml, requirements.txt"),
        ("core/", "Main application files", "app.py, main.py, models.py"),
        ("scripts/", "Utility scripts", "launch_full_app.py, quick_start.py"),
        ("docs/", "Documentation", "README.md, guides"),
        ("assets/", "Images and media", "screenshots, diagrams"),
        ("frontend/", "Next.js application", "React components, pages"),
        ("utils/", "Helper modules", "config_manager.py, data_fetcher.py"),
        ("crypto/", "Trading strategies", "strategies, scripts"),
        ("test/", "Testing framework", "test scripts"),
        ("templates/", "Flask templates", "HTML templates"),
        ("static/", "Static assets", "CSS, JavaScript"),
        ("config/", "Configuration files", "credentials.yaml"),
    ]
    
    for directory, purpose, key_files in structure_info:
        if Path(directory.rstrip('/')).exists() or directory == "root/":
            structure_table.add_row(directory, purpose, key_files)
    
    console.print(structure_table)
    
    console.print("\n🎉 Project organization complete!", style="bold green")
    console.print("💡 Use 'python scripts/launch_full_app.py' to start the application", style="cyan")

if __name__ == "__main__":
    organize_project()