export interface BusinessCardConcept {
  id: string
  name: string
  description: string
  imageUrl?: string
  style: 'Clinical-Precision' | 'Athletic-Edge' | 'Luxury-Wellness' | 'Minimalist-Pro'
}

export interface DesignIteration {
  id: string
  parentId?: string
  concept: BusinessCardConcept
  phase: 'concept' | 'layout' | 'typography' | 'colors' | 'final'
  variations: DesignVariation[]
  selectedVariation?: string
  timestamp: Date
}

export interface DesignVariation {
  id: string
  label: string // A, B, C, D or 1, 2, 3, 4, etc.
  description: string
  imageUrl?: string
  isSelected?: boolean
  prompt: string
}

export interface DesignHistory {
  sessionId: string
  iterations: DesignIteration[]
  finalDesign?: DesignVariation
  clientInfo: {
    name: string
    company: string
    email: string
    tagline: string
    website: string
    location: string
  }
}

export interface GenerationRequest {
  concept: string
  side: 'front' | 'back'
  quality: 'draft' | 'review' | 'production'
  model?: 'openai' | 'gemini' | 'auto'
  customPrompt?: string
}

export interface GenerationResponse {
  success: boolean
  imageUrl?: string
  jobId: string
  estimatedTime: number
  cost: number
  model: string
  error?: string
}

export type WorkflowPhase = 'concept' | 'layout' | 'typography' | 'colors' | 'final'

export interface WorkflowState {
  currentPhase: WorkflowPhase
  selectedConcept?: BusinessCardConcept
  designHistory: DesignHistory
  isGenerating: boolean
  progress: number
}