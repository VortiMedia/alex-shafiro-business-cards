# Business Card Generator v4.0 - Iterative Design Frontend

**Next.js Frontend for AI-Powered Iterative Business Card Design**

✨ **Transform from "generate and pray" to iterative perfection** - Guide users through 4 phases of refinement until the design is exactly right.

---

## 🎯 **What This Is**

This Next.js frontend implements the complete **Iterative Design Workflow** for A Stronger Life business cards:

1. **Concept Selection** (A, B, C, D) - Choose design direction
2. **Layout Refinement** (1, 2, 3, 4) - Arrange elements 
3. **Typography Treatment** (a, b, c, d) - Select font styles
4. **Color & Accents** (i, ii, iii, iv) - Place emerald highlights
5. **Final Production** - Generate high-res files

**Design Philosophy**: "Equinox meets Mayo Clinic" - Premium medical luxury with deep black (#0A0A0A) and emerald (#00C9A7) accents.

---

## 🚀 **Quick Start**

### **1. Install & Run**
```bash
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000)

### **2. Experience the Workflow**
- Choose from 4 concept variations
- Refine through layout, typography, and color phases  
- Track design history and costs
- Generate production-ready files

---

## 🏗️ **Architecture**

### **Technology Stack**
- **Framework**: Next.js 15.5.3 + TypeScript
- **UI**: ShadCN UI with custom premium theme
- **Styling**: Tailwind CSS v4
- **Animations**: Framer Motion
- **Icons**: Lucide React

### **Key Components**
- `business-card-generator.tsx` - Main iterative workflow
- `variation-selector.tsx` - 4-option selection interface
- `workflow-progress.tsx` - Phase tracking
- `design-history.ts` - Session tracking hook
- `api/generate/` - AI integration endpoints

### **Design System**
```css
/* Premium Medical Theme */
--background: #0A0A0A;     /* Deep obsidian black */
--primary: #00C9A7;        /* Emerald glow */
--foreground: #FAFAFA;     /* Arctic white */
--card: #1A1A1A;          /* Charcoal shadow */
```

---

## 🎨 **User Experience Flow**

```
🎯 Step 1: Concept Selection
├── A: Clinical Precision (Medical authority)
├── B: Athletic Edge (Performance focus)  
├── C: Luxury Wellness (Premium spa)
└── D: Minimalist Pro (Clean elegance)

🎯 Step 2: Layout Refinement 
├── 1: Logo top-left, contact bottom-right
├── 2: Centered logo, contact below
├── 3: Vertical layout, logo left side
└── 4: Horizontal split, balanced

🎯 Step 3: Typography Treatment
├── a: Bold sans-serif, high contrast
├── b: Light weight, more spacing
├── c: Mixed weights, visual hierarchy  
└── d: Condensed font, compact

🎯 Step 4: Color & Accents
├── i: Emerald accent on name only
├── ii: Emerald accent on company name
├── iii: Emerald glow background
└── iv: Emerald border accent

🎯 Step 5: Final Production
└── High-res PNG files ready for print
```

**Selection Path Example**: `B-3-b-ii` = Athletic + Vertical + Light Typography + Company Accent

---

## 💰 **Cost Optimization**

### **Smart Model Selection**
- **Concepts & Iterations**: Gemini ($0.005 each)
- **Final Production**: GPT Image 1 ($0.19)
- **Total per Perfect Card**: ~$0.25

### **Real-Time Tracking**
- Session cost display
- Per-iteration breakdown
- Production cost warnings
- History export for accounting

---

## 🔗 **Backend Integration**

### **API Endpoints**
- `POST /api/generate` - Single variation generation
- `POST /api/generate/batch` - 4-variation batch processing
- `GET /api/generate` - Model availability check

### **Ready for Connection**
```typescript
// Mock responses ready to replace with actual AI calls
interface GenerationResponse {
  success: boolean
  imageUrl?: string
  jobId: string
  cost: number
  model: 'openai' | 'gemini'
}
```

---

## 🛠️ **Development**

### **Available Scripts**
```bash
npm run dev        # Development server
npm run build      # Production build
npm run start      # Production server
npm run lint       # ESLint check
npm run type-check # TypeScript validation
```

### **Project Structure**
```
src/
├── app/
│   ├── api/generate/     # AI generation endpoints
│   ├── globals.css       # Premium theme
│   └── page.tsx         # Main entry
├── components/
│   ├── ui/              # ShadCN components
│   └── business-card-*  # Custom components
├── hooks/
│   └── use-design-history.ts
├── types/
│   └── index.ts         # TypeScript definitions
└── lib/
    └── utils.ts
```

---

## 🎯 **Features Implemented**

### ✅ **Core Workflow**
- 4-phase iterative refinement
- 4-option selection per phase
- Smooth phase transitions
- Progress tracking

### ✅ **User Experience** 
- Premium medical aesthetic
- Responsive mobile-first design
- Framer Motion animations
- Real-time cost tracking

### ✅ **Technical Excellence**
- TypeScript safety throughout
- ShadCN UI component system
- Design history tracking
- API integration ready

---

## 📚 **Documentation**

- **[PRD_V4_ITERATIVE.md](../PRD_V4_ITERATIVE.md)** - Complete requirements
- **[FRONTEND_SETUP_COMPLETE.md](../aidocs/FRONTEND_SETUP_COMPLETE.md)** - Setup documentation
- **[Component API](src/types/index.ts)** - TypeScript interfaces

---

## 🚀 **Production Deployment**

Ready to deploy to:
- **Vercel** (Recommended)
- **Netlify**
- **AWS Amplify** 
- **Google Cloud Run**
- **Self-hosted Docker**

```bash
npm run build
# Deploy dist/ to your platform of choice
```

---

## 🎊 **Status: Complete & Ready**

**The frontend implements the complete iterative design workflow as specified in PRD_V4_ITERATIVE.md. Ready for backend integration and deployment!**
