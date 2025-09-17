# Client Projects Organization

This folder contains all client assets and requirements for business card design projects.

## 📁 Folder Structure

```
client_projects/
├── current_cards/          # Original business cards from clients
├── logos/                  # Client logos and brand assets
├── requirements/           # Client briefs and design requirements
└── generated/              # AI-generated business card variations
    ├── drafts/            # Initial concept variations
    ├── revisions/         # Client-requested revisions  
    └── final/             # Approved final designs
```

## 🎯 How to Use

### 1. New Client Project Setup

1. **Create client brief**: Copy `requirements/client_brief_template.md` to `requirements/[client_name]_brief.md`
2. **Collect assets**: 
   - Add current business card to `current_cards/[client_name]_current.png`
   - Add logo files to `logos/[client_name]_logo.[ext]`
3. **Fill out brief**: Complete all sections of the client brief

### 2. File Naming Convention

**Current Cards:**
- `[client_name]_current_front.png`
- `[client_name]_current_back.png`

**Logos:**
- `[client_name]_logo_primary.svg` (preferred format)
- `[client_name]_logo_primary.png`
- `[client_name]_logo_horizontal.svg`
- `[client_name]_logo_icon.svg`

**Requirements:**
- `[client_name]_brief.md`
- `[client_name]_brand_guidelines.pdf` (if available)

**Generated Designs:**
- `[client_name]_v1_concept_a.png`
- `[client_name]_v2_revision_a.png`
- `[client_name]_final.png`

### 3. Client Brief Template

Use the comprehensive client brief template in `requirements/client_brief_template.md` to capture:
- ✅ Brand colors and typography preferences
- ✅ Current assets and improvement areas
- ✅ Contact information and hierarchy
- ✅ Design style direction and inspiration
- ✅ Technical specifications and deliverables
- ✅ Project timeline and workflow preferences

## 🎨 Quick Start Workflow

```bash
# 1. Create new client project
cp requirements/client_brief_template.md requirements/pace_homebuyers_brief.md

# 2. Add client assets
# Upload current card: current_cards/pace_homebuyers_current.png  
# Upload logo: logos/pace_homebuyers_logo.svg

# 3. Fill out brief and generate AI prompts
# Edit pace_homebuyers_brief.md with client requirements

# 4. Generate business cards using the AI system
python src/main.py --client="pace_homebuyers" --variations=4
```

## 📊 Project Tracking

Each client brief includes a project checklist:
- [ ] **Pre-Design**: Assets collected, brief completed
- [ ] **Design Phase**: Concepts created, feedback integrated  
- [ ] **Delivery**: Files prepared and delivered

## 🔐 Client Confidentiality

**Important**: Client assets may contain sensitive information.
- Never commit actual client files to version control
- Use `.gitignore` patterns to exclude client data
- Store sensitive assets in secure, encrypted locations
- Follow your agency's data protection policies

## 💡 Pro Tips

### Efficient Asset Management
- Always request SVG logos when possible
- Get brand guidelines PDF if available
- Ask for current card in high-resolution scan
- Confirm exact contact information with client

### AI Prompt Optimization
- Use specific hex color codes from client brief
- Include industry context for better results
- Mention competitor styles to avoid or emulate
- Specify exact dimensions and print requirements

### Client Communication
- Share AI-generated concepts as low-res previews first
- Use the brief checklist to ensure nothing is missed
- Document all feedback and revision requests
- Archive completed projects with final files

---

**Template Status**: Ready for use  
**Last Updated**: December 17, 2025  
**Version**: 1.0