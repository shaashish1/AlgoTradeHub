# Single Port Application Consolidation Design

## Overview

This design consolidates the AlgoTradeHub application from a dual-port architecture (Flask on 5000 + Next.js on 3000) to a single-port Next.js application running exclusively on port 3000. All backend functionality will be migrated to Next.js API routes, with Python trading logic executed as child processes or through serverless functions.

## Architecture

### Current Architecture (To Be Replaced)
```
┌─────────────────┐    ┌─────────────────┐
│   Next.js       │    │   Flask         │
│   Frontend      │───▶│   Backend       │
│   Port 3000     │    │   Port 5000     │
└─────────────────┘    └─────────────────┘
```

### New Consolidated Architecture
```
┌─────────────────────────────────────────┐
│           Next.js Application           │
│              Port 3000                  │
├─────────────────────────────────────────┤
│  Frontend Pages  │  API Routes         │
│  - Trading       │  - /api/trading/*   │
│  - Portfolio     │  - /api/exchange/*  │
│  - Exchanges     │  - /api/portfolio/* │
│  - Dashboard     │  - /api/market/*    │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│        Python Trading Engine           │
│        (Child Process/Serverless)      │
│  - CCXT Integration                     │
│  - Order Execution                      │
│  - Market Data                          │
└─────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Next.js API Routes
Replace Flask endpoints with Next.js API routes:

**Trading API Routes:**
- `GET /api/trading/balance/[exchange]` - Get account balance
- `POST /api/trading/execute` - Execute trading orders
- `GET /api/trading/orders/[exchange]` - Get order history
- `POST /api/trading/cancel` - Cancel orders

**Exchange API Routes:**
- `GET /api/exchanges/available` - List available exchanges
- `POST /api/exchange/configure` - Configure exchange credentials
- `POST /api/exchange/test/[exchange]` - Test exchange connection
- `GET /api/exchange/status` - Get exchange connection status

**Portfolio API Routes:**
- `POST /api/portfolio/refresh` - Refresh portfolio data
- `GET /api/portfolio/summary` - Get portfolio summary
- `GET /api/portfolio/positions` - Get all positions
- `GET /api/portfolio/history` - Get portfolio history

**Market Data API Routes:**
- `GET /api/market/data/[symbol]` - Get market data for symbol
- `GET /api/market/pairs/[exchange]` - Get trading pairs
- `GET /api/market/ticker/[symbol]` - Get ticker data
- `POST /api/market/subscribe` - Subscribe to real-time data

### 2. Python Integration Layer
Create a Python execution service that can be called from Next.js:

**Option A: Child Process Execution**
```typescript
// In Next.js API route
import { spawn } from 'child_process'

const executePythonScript = (script: string, args: any[]) => {
  return new Promise((resolve, reject) => {
    const python = spawn('python', [script, ...args])
    // Handle response
  })
}
```

**Option B: Python HTTP Microservice**
```typescript
// Keep Python as internal microservice on different port
// Only accessible from Next.js API routes, not externally
const PYTHON_SERVICE_URL = 'http://localhost:8000' // Internal only
```

### 3. Database Integration
Migrate database operations to Next.js:

**Database Connection:**
```typescript
// lib/database.ts
import sqlite3 from 'sqlite3'
import { open } from 'sqlite'

export async function getDatabase() {
  return open({
    filename: './instance/algotrading.db',
    driver: sqlite3.Database
  })
}
```

**Database Operations:**
- User preferences and settings
- Exchange configurations (encrypted)
- Trading history and logs
- Portfolio snapshots

### 4. Configuration Management
Centralize all configuration in Next.js:

**Environment Variables:**
```env
# .env.local
DATABASE_URL=./instance/algotrading.db
ENCRYPTION_KEY=your-encryption-key
PYTHON_SCRIPT_PATH=./python-scripts
NODE_ENV=development
```

**Configuration Structure:**
```typescript
interface AppConfig {
  database: DatabaseConfig
  exchanges: ExchangeConfig[]
  trading: TradingConfig
  security: SecurityConfig
}
```

## Data Models

### Exchange Configuration
```typescript
interface ExchangeConfig {
  id: string
  name: string
  credentials: EncryptedCredentials
  isActive: boolean
  lastConnected: Date
  features: string[]
}
```

### Trading Order
```typescript
interface TradingOrder {
  id: string
  exchange: string
  symbol: string
  side: 'buy' | 'sell'
  type: 'market' | 'limit'
  amount: number
  price?: number
  status: OrderStatus
  timestamp: Date
}
```

### Portfolio Position
```typescript
interface Position {
  symbol: string
  exchange: string
  amount: number
  averagePrice: number
  currentPrice: number
  unrealizedPnL: number
  realizedPnL: number
}
```

## Error Handling

### API Error Responses
Standardize error responses across all API routes:

```typescript
interface ApiError {
  error: string
  code: string
  details?: any
  timestamp: Date
}
```

### Error Categories
1. **Authentication Errors** - Invalid API credentials
2. **Exchange Errors** - Exchange API failures
3. **Validation Errors** - Invalid request parameters
4. **System Errors** - Internal server errors
5. **Network Errors** - Connection timeouts

### Error Recovery
- Automatic retry for transient errors
- Fallback to cached data when appropriate
- Graceful degradation of features
- User-friendly error messages

## Testing Strategy

### Unit Tests
- Test all API routes independently
- Mock Python script execution
- Test database operations
- Test error handling scenarios

### Integration Tests
- Test complete trading workflows
- Test exchange connectivity
- Test portfolio calculations
- Test real-time data flow

### End-to-End Tests
- Test user journeys through the application
- Test cross-browser compatibility
- Test mobile responsiveness
- Test performance under load

### Migration Testing
- Verify data migration from Flask to Next.js
- Test backward compatibility
- Validate feature parity
- Performance comparison testing

## Security Considerations

### API Security
- Rate limiting on all API endpoints
- Input validation and sanitization
- CORS configuration for production
- API key encryption and secure storage

### Data Protection
- Encrypt sensitive configuration data
- Secure credential storage
- Audit logging for all trading operations
- Session management and authentication

### Network Security
- HTTPS enforcement in production
- Secure headers configuration
- Content Security Policy
- Protection against common attacks (XSS, CSRF)

## Performance Optimization

### Caching Strategy
- Cache market data for short periods
- Cache exchange metadata
- Cache user preferences
- Implement Redis for production caching

### Database Optimization
- Index frequently queried fields
- Optimize portfolio calculation queries
- Implement connection pooling
- Regular database maintenance

### API Performance
- Implement request/response compression
- Optimize JSON serialization
- Use streaming for large datasets
- Implement pagination for large results

## Deployment Strategy

### Development Environment
```bash
# Single command to start everything
npm run dev
# Starts Next.js on port 3000 with all functionality
```

### Production Environment
```bash
# Build and start production server
npm run build
npm run start
# Single process serving everything on port 3000
```

### Docker Configuration
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## Migration Plan

### Phase 1: API Route Creation
1. Create all Next.js API routes
2. Implement Python script execution
3. Test API endpoints individually

### Phase 2: Database Migration
1. Migrate database operations to Next.js
2. Update data models and schemas
3. Test data persistence

### Phase 3: Frontend Integration
1. Update frontend to use new API routes
2. Remove references to port 5000
3. Test all user interfaces

### Phase 4: Python Integration
1. Integrate Python trading scripts
2. Test order execution and market data
3. Validate exchange connectivity

### Phase 5: Testing and Validation
1. Run comprehensive test suite
2. Performance testing and optimization
3. Security audit and validation

### Phase 6: Cleanup
1. Remove Flask application files
2. Update documentation
3. Clean up unused dependencies