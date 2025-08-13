# Quick Setup Guide

## Step 1: Install Dependencies

Open terminal/command prompt in the `frontend` directory and run:

```bash
npm install
```

If you encounter any issues, try:
```bash
npm install --legacy-peer-deps
```

## Step 2: Start Development Server

```bash
npm run dev
```

## Step 3: Open Browser

Navigate to: [http://localhost:3000](http://localhost:3000)

## Troubleshooting

### If localhost:3000 doesn't open:

1. **Check if the server started successfully**:
   - Look for "Ready - started server on 0.0.0.0:3000" in terminal
   - If you see errors, read them carefully

2. **Port might be in use**:
   ```bash
   npm run dev -- -p 3001
   ```
   Then try: [http://localhost:3001](http://localhost:3001)

3. **Clear npm cache**:
   ```bash
   npm cache clean --force
   rm -rf node_modules
   npm install
   ```

4. **Check Node.js version**:
   ```bash
   node --version
   ```
   Should be 18+ or 20+

### Common Issues:

- **"Module not found"**: Run `npm install` again
- **TypeScript errors**: Ignore for now, focus on getting it running
- **Port 3000 busy**: Use different port with `-p 3001`

## What You Should See:

1. **Dashboard Page** with:
   - Header with navigation
   - Portfolio stats cards
   - Quick actions sidebar
   - Charts and tables

2. **Feature Browser** at `/features`
3. **Backtesting Suite** at `/backtest/comprehensive`

## Need Help?

If you're still having issues, please share:
1. The exact error message from terminal
2. Your Node.js version (`node --version`)
3. Your operating system