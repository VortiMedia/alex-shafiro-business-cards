# WARP.md

## Project Overview

**Business Card Generator v4.0** - Iterative design system where users guide AI through refinement rounds until perfect.

**Core Innovation**: 4-phase workflow (Concept → Layout → Typography → Production)

## Architecture

### Tech Stack
- **Frontend**: Next.js + TypeScript + ShadCN UI + Tailwind CSS
- **Backend**: Python + FastAPI, dual AI models (OpenAI + Gemini)
- **Database**: PostgreSQL/Supabase with iterative workflow tracking

### Design System
- **4 Concepts**: Clinical, Athletic, Luxury, Minimalist
- **Brand**: Deep black (#0A0A0A) + emerald accent (#00C9A7)
- **Style**: "Equinox meets Mayo Clinic" - premium medical

## Commands

### Current (V3.0)
```bash
# Web interface
python simple_app.py  # http://localhost:8000

# CLI
python generate_business_cards.py
```

### Development (V4.0)
```bash
# Frontend
cd frontend/ && npm install && npm run dev  # http://localhost:3000

# Backend
pip install -r requirements.txt
export OPENAI_API_KEY="your-key"
export GOOGLE_API_KEY="your-key"
python generate_cards_v4.py --interactive
```

### Database
```bash
# Deploy schema
supabase db push schema_v4_iterative.sql
supabase db push schema_v4_enhancements.sql
```

## File Structure

```
frontend/src/
├── app/page.tsx              # Main iterative interface
├── components/
│   ├── business-card-generator.tsx
│   └── variation-selector.tsx
├── hooks/use-design-history.ts
└── types/index.ts

backend/
├── generate_business_cards.py  # Legacy CLI
├── generate_cards_v4.py       # V4.0 iterative
├── src/hybrid/modern_workflow.py
└── requirements.txt

schema/
├── schema_v4_iterative.sql
└── schema_v4_enhancements.sql
```

## Business Logic

### Brand Information
- **Client**: Alex Shafiro PT / DPT / OCS / CSCS
- **Company**: A Stronger Life
- **Tagline**: "Revolutionary Rehabilitation"
- **Contact**: admin@aslstrong.com, www.aslstrong.com, Stamford CT
- **Output**: 3.5" × 2.0" at 300+ DPI

### Iterative Workflow (v4.0)
- **Phase 1**: Concept Selection (A, B, C, D)
- **Phase 2**: Layout Refinement (1, 2, 3, 4)
- **Phase 3**: Typography Treatment (a, b, c, d)
- **Phase 4**: Color & Accent Placement (i, ii, iii, iv)
- **Phase 5**: Final Production (high-res generation)

### Cost Structure
- **Draft**: $0.001-0.005 (Gemini)
- **Production**: $0.19 (GPT Image 1)
- **Total per perfect card**: ~$0.25
