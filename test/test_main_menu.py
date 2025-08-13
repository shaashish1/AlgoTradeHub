#!/usr/bin/env python3
"""
Test the main menu functionality
"""

import asyncio
import sys
from rich.console import Console

console = Console()

async def test_menu():
    """Test the main menu"""
    try:
        console.print("🧪 Testing main menu functionality...")
        
        # Import the main components
        from main import TradingSystemMenu, FeatureBrowser
        
        console.print("✅ Imports successful")
        
        # Test feature browser
        browser = FeatureBrowser()
        scripts = browser.get_available_scripts()
        
        console.print(f"✅ Found {len(scripts)} script categories")
        for category, items in scripts.items():
            console.print(f"  - {category}: {len(items)} scripts")
        
        # Test menu display
        menu = TradingSystemMenu()
        menu.display_welcome()
        
        console.print("✅ Menu display works")
        
        # Test script paths
        for category, items in scripts.items():
            for key, script in items.items():
                import os
                if os.path.exists(script['file']):
                    console.print(f"✅ {script['file']} exists")
                else:
                    console.print(f"❌ {script['file']} missing", style="red")
        
        console.print("\n🎉 Main menu test completed!")
        
    except Exception as e:
        console.print(f"❌ Test failed: {e}", style="red")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(test_menu())