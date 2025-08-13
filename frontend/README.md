# AlgoTradeHub Frontend

Modern, responsive frontend for the AlgoTradeHub trading platform built with Next.js 14, TypeScript, and shadcn/ui.

## 🚀 Features

- **Modern UI**: Built with shadcn/ui components and Tailwind CSS
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Real-time Updates**: Live data streaming and interactive charts
- **Comprehensive Backtesting**: Multi-dimensional strategy analysis
- **Feature Browser**: Central hub for all trading tools
- **Dark/Light Mode**: User preference support
- **TypeScript**: Full type safety and better developer experience

## 📦 Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui (Radix UI primitives)
- **Charts**: Recharts
- **Icons**: Lucide React
- **State Management**: React hooks (can be extended with Zustand/Redux)

## 🛠️ Setup Instructions

### Prerequisites

- Node.js 18+ 
- npm or yarn or pnpm

### Installation

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

3. **Run development server**:
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

4. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
npm run build
npm run start
```

## 📱 Pages & Features

### 🏠 Dashboard (`/`)
- Portfolio overview with real-time stats
- Interactive performance charts
- Open positions table
- Exchange status indicators
- Recent alerts and notifications

### 🎯 Feature Browser (`/features`)
- Organized feature categories (Crypto, Core, Testing)
- Advanced options including Comprehensive Backtesting Suite
- Quick actions and favorites
- Search and filter capabilities

### 📊 Comprehensive Backtesting (`/backtest/comprehensive`)
- Multi-strategy selection (9 built-in strategies)
- Multi-timeframe analysis (1m to 1d)
- Multi-asset support (10+ crypto pairs)
- Real-time progress tracking
- Detailed results analysis with insights

## 🎨 Design System

### Color Palette
- **Primary**: Blue (#3b82f6)
- **Success**: Green (#10b981)
- **Warning**: Yellow (#f59e0b)
- **Danger**: Red (#ef4444)
- **Muted**: Gray variants for secondary content

### Components
- **Cards**: Rounded corners with subtle shadows
- **Buttons**: Multiple variants (default, outline, ghost, etc.)
- **Tables**: Striped rows with hover effects
- **Charts**: Interactive with responsive design
- **Badges**: Status indicators with semantic colors

### Responsive Breakpoints
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🔧 Customization

### Adding New Components

1. **Create component file**:
   ```bash
   # For UI components
   touch components/ui/new-component.tsx
   
   # For feature components
   touch components/features/new-feature.tsx
   ```

2. **Follow shadcn/ui patterns**:
   ```tsx
   import { cn } from "@/lib/utils"
   
   interface ComponentProps {
     className?: string
     // other props
   }
   
   export function NewComponent({ className, ...props }: ComponentProps) {
     return (
       <div className={cn("base-styles", className)} {...props}>
         {/* component content */}
       </div>
     )
   }
   ```

### Adding New Pages

1. **Create page file**:
   ```bash
   touch app/new-page/page.tsx
   ```

2. **Follow Next.js App Router structure**:
   ```tsx
   import { Header } from '@/components/layout/header'
   
   export default function NewPage() {
     return (
       <div className="min-h-screen bg-background">
         <Header />
         <main className="container py-6">
           {/* page content */}
         </main>
       </div>
     )
   }
   ```

### Styling Guidelines

- Use Tailwind CSS utility classes
- Follow the established color system
- Use semantic class names from globals.css
- Maintain consistent spacing (4, 6, 8 units)
- Ensure responsive design with mobile-first approach

## 📊 Data Integration

The frontend is designed to work with the Python backend APIs. Key integration points:

- **Real-time data**: WebSocket connections for live updates
- **API endpoints**: RESTful APIs for data fetching
- **Authentication**: JWT token-based authentication
- **Error handling**: Comprehensive error boundaries and fallbacks

## 🚀 Deployment

### Vercel (Recommended)
```bash
npm run build
# Deploy to Vercel
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

### Static Export
```bash
npm run build
npm run export
```

## 🤝 Contributing

1. Follow the established code style
2. Use TypeScript for all new components
3. Ensure responsive design
4. Add proper error handling
5. Test on multiple devices/browsers

## 📝 License

This project is part of the AlgoTradeHub platform.

---

## 🎯 Next Steps

1. **Backend Integration**: Connect to Python APIs
2. **Real-time Features**: Implement WebSocket connections
3. **Authentication**: Add user login/logout
4. **Mobile App**: React Native version
5. **Advanced Charts**: More sophisticated visualizations
6. **Notifications**: Push notifications and alerts
7. **Offline Support**: PWA capabilities

For questions or support, please refer to the main project documentation.