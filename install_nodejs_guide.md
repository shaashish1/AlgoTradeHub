# Node.js Installation Guide for AlgoTradeHub Frontend

## 🚨 **Issue Detected**
Node.js is not installed on your system, which is required for the frontend to work.

## 📥 **Step 1: Install Node.js**

### **Option A: Download from Official Website (Recommended)**

1. **Visit**: https://nodejs.org/
2. **Download**: Click "Download Node.js (LTS)" - the green button
3. **Choose**: LTS version (Long Term Support) - currently v20.x.x
4. **Install**: Run the downloaded installer
5. **Follow**: Installation wizard (accept all defaults)

### **Option B: Using Package Manager (Advanced)**

**Windows (using Chocolatey):**
```powershell
# Install Chocolatey first (if not installed)
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Node.js
choco install nodejs
```

**Windows (using Winget):**
```powershell
winget install OpenJS.NodeJS
```

## ✅ **Step 2: Verify Installation**

After installation, **restart your command prompt/PowerShell** and run:

```bash
node --version
npm --version
```

You should see something like:
```
v20.10.0
10.2.3
```

## 🚀 **Step 3: Fix Frontend**

Once Node.js is installed, run the frontend fix script:

```bash
python fix_frontend.py
```

## 🎯 **What Node.js Versions Work**

- ✅ **Node.js 18.x** - Minimum supported
- ✅ **Node.js 20.x** - Recommended (LTS)
- ✅ **Node.js 21.x** - Latest (but use LTS for stability)

## 🔧 **Troubleshooting**

### **"node is not recognized" after installation**
1. **Restart** your command prompt/PowerShell
2. **Check PATH**: Node.js should be added automatically
3. **Manual PATH**: Add `C:\Program Files\nodejs` to your PATH if needed

### **Permission Issues**
1. **Run as Administrator**: Right-click command prompt → "Run as administrator"
2. **Or use**: `npm install -g npm` to update npm

### **Corporate Network Issues**
If behind a corporate firewall:
```bash
npm config set registry https://registry.npmjs.org/
npm config set strict-ssl false
```

## 📱 **After Node.js Installation**

1. **Verify**: `node --version` and `npm --version`
2. **Fix Frontend**: `python fix_frontend.py`
3. **Start Development**: `cd frontend && npm run dev`
4. **Visit**: http://localhost:3000

## 🎉 **Expected Results**

After installing Node.js and running the fix script, you should see:

```
✅ Node.js found: v20.10.0
✅ npm found: 10.2.3
✅ Dependencies installed successfully!
✅ Build test successful!
✅ Frontend is fully working!
```

## 🆘 **Need Help?**

If you encounter any issues:

1. **Check Node.js version**: Must be 18+
2. **Restart terminal**: After Node.js installation
3. **Run as admin**: If permission issues
4. **Clear npm cache**: `npm cache clean --force`

---

**Next Step**: Install Node.js from https://nodejs.org/, then run `python fix_frontend.py`