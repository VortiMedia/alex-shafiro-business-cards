"use client"

import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Loader2, Sparkles, CheckCircle2, ArrowRight, RotateCcw } from 'lucide-react'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Separator } from '@/components/ui/separator'
import { Alert, AlertDescription } from '@/components/ui/alert'

import { WorkflowState, WorkflowPhase, BusinessCardConcept, DesignVariation } from '@/types'
import { ConceptSelector } from './concept-selector'
import { VariationSelector } from './variation-selector'
import { DesignPreview } from './design-preview'
import { WorkflowProgress } from './workflow-progress'

const INITIAL_CONCEPTS: BusinessCardConcept[] = [
  {
    id: 'clinical',
    name: 'Clinical Precision',
    description: 'Medical authority with symmetric layout and professional typography',
    style: 'Clinical-Precision'
  },
  {
    id: 'athletic',
    name: 'Athletic Edge', 
    description: 'Dynamic energy with performance-focused design elements',
    style: 'Athletic-Edge'
  },
  {
    id: 'luxury',
    name: 'Luxury Wellness',
    description: 'Premium spa aesthetic with sophisticated minimalism',
    style: 'Luxury-Wellness'
  },
  {
    id: 'minimal',
    name: 'Minimalist Pro',
    description: 'Clean, simple elegance with maximum impact',
    style: 'Minimalist-Pro'
  }
]

export function BusinessCardGenerator() {
  const [workflowState, setWorkflowState] = useState<WorkflowState>({
    currentPhase: 'concept',
    designHistory: {
      sessionId: `session-${Date.now()}`,
      iterations: [],
      clientInfo: {
        name: "Alex Shafiro PT / DPT / OCS / CSCS",
        company: "A Stronger Life",
        email: "admin@aslstrong.com", 
        tagline: "Revolutionary Rehabilitation",
        website: "www.aslstrong.com",
        location: "Stamford, CT"
      }
    },
    isGenerating: false,
    progress: 0
  })

  const [currentVariations, setCurrentVariations] = useState<DesignVariation[]>([])
  const [selectedVariation, setSelectedVariation] = useState<string | null>(null)

  // Phase progression mapping
  const phaseOrder: WorkflowPhase[] = ['concept', 'layout', 'typography', 'colors', 'final']
  const currentPhaseIndex = phaseOrder.indexOf(workflowState.currentPhase)

  // Generate variations for current phase
  const generateVariations = async (phase: WorkflowPhase, baseConcept?: BusinessCardConcept) => {
    setWorkflowState(prev => ({ ...prev, isGenerating: true, progress: 0 }))
    
    try {
      // Simulate AI generation with progress updates
      for (let i = 0; i <= 100; i += 10) {
        await new Promise(resolve => setTimeout(resolve, 200))
        setWorkflowState(prev => ({ ...prev, progress: i }))
      }

      // Mock variations based on phase
      let variations: DesignVariation[] = []
      
      if (phase === 'concept') {
        variations = INITIAL_CONCEPTS.map((concept, index) => ({
          id: `concept-${concept.id}`,
          label: String.fromCharCode(65 + index), // A, B, C, D
          description: concept.description,
          imageUrl: `/api/placeholder/400/250?text=${concept.name.replace(' ', '+')}&bg=1a1a1a&color=00c9a7`,
          prompt: `Professional business card design: ${concept.description}`
        }))
      } else if (phase === 'layout') {
        variations = [
          {
            id: 'layout-1',
            label: '1',
            description: 'Logo top-left, contact bottom-right',
            imageUrl: `/api/placeholder/400/250?text=Layout+1&bg=1a1a1a&color=00c9a7`,
            prompt: 'Layout variation with logo top-left positioning'
          },
          {
            id: 'layout-2', 
            label: '2',
            description: 'Centered logo, contact info below',
            imageUrl: `/api/placeholder/400/250?text=Layout+2&bg=1a1a1a&color=00c9a7`,
            prompt: 'Centered layout with contact below'
          },
          {
            id: 'layout-3',
            label: '3', 
            description: 'Vertical layout, logo left side',
            imageUrl: `/api/placeholder/400/250?text=Layout+3&bg=1a1a1a&color=00c9a7`,
            prompt: 'Vertical layout with side positioning'
          },
          {
            id: 'layout-4',
            label: '4',
            description: 'Horizontal split, balanced design',
            imageUrl: `/api/placeholder/400/250?text=Layout+4&bg=1a1a1a&color=00c9a7`,
            prompt: 'Horizontal split balanced layout'
          }
        ]
      } else {
        // Generate variations for typography, colors, etc.
        variations = Array.from({ length: 4 }, (_, index) => ({
          id: `${phase}-${index + 1}`,
          label: String.fromCharCode(97 + index), // a, b, c, d for typography, i, ii, iii, iv for colors
          description: `${phase.charAt(0).toUpperCase() + phase.slice(1)} variation ${index + 1}`,
          imageUrl: `/api/placeholder/400/250?text=${phase.charAt(0).toUpperCase() + phase.slice(1)}+${index + 1}&bg=1a1a1a&color=00c9a7`,
          prompt: `${phase} refinement variation ${index + 1}`
        }))
      }

      setCurrentVariations(variations)
      setSelectedVariation(null)
      
    } catch (error) {
      console.error('Generation failed:', error)
    } finally {
      setWorkflowState(prev => ({ ...prev, isGenerating: false, progress: 0 }))
    }
  }

  // Handle variation selection
  const handleVariationSelect = (variationId: string) => {
    setSelectedVariation(variationId)
    
    // Update design history
    const selectedVar = currentVariations.find(v => v.id === variationId)
    if (selectedVar) {
      setWorkflowState(prev => ({
        ...prev,
        designHistory: {
          ...prev.designHistory,
          iterations: [
            ...prev.designHistory.iterations,
            {
              id: `iteration-${Date.now()}`,
              concept: workflowState.selectedConcept || INITIAL_CONCEPTS[0],
              phase: workflowState.currentPhase,
              variations: currentVariations,
              selectedVariation: variationId,
              timestamp: new Date()
            }
          ]
        }
      }))
    }
  }

  // Proceed to next phase
  const proceedToNextPhase = () => {
    const nextPhaseIndex = currentPhaseIndex + 1
    if (nextPhaseIndex < phaseOrder.length) {
      const nextPhase = phaseOrder[nextPhaseIndex]
      setWorkflowState(prev => ({ ...prev, currentPhase: nextPhase }))
      generateVariations(nextPhase, workflowState.selectedConcept)
    }
  }

  // Start over
  const startOver = () => {
    setWorkflowState(prev => ({
      ...prev,
      currentPhase: 'concept',
      selectedConcept: undefined,
      designHistory: {
        ...prev.designHistory,
        iterations: []
      }
    }))
    generateVariations('concept')
  }

  // Initialize with concept generation
  useEffect(() => {
    generateVariations('concept')
  }, [])

  const getPhaseTitle = (phase: WorkflowPhase) => {
    const titles = {
      concept: 'Choose Your Design Concept',
      layout: 'Select Layout Style',
      typography: 'Pick Typography Treatment',
      colors: 'Choose Color & Accents',
      final: 'Final Production'
    }
    return titles[phase]
  }

  const getPhaseDescription = (phase: WorkflowPhase) => {
    const descriptions = {
      concept: 'Pick the design direction that best represents A Stronger Life',
      layout: 'Choose how elements are arranged on the card',
      typography: 'Select the font style and text treatment',
      colors: 'Decide where to place the emerald accent color',
      final: 'Generate your high-resolution production files'
    }
    return descriptions[phase]
  }

  return (
    <div className="min-h-screen bg-gradient-medical p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">
            <span className="text-gradient-emerald">Business Card Generator</span>
          </h1>
          <p className="text-muted-foreground text-lg">
            Iterative AI-powered design for A Stronger Life
          </p>
        </div>

        {/* Workflow Progress */}
        <WorkflowProgress 
          currentPhase={workflowState.currentPhase}
          completedPhases={workflowState.designHistory.iterations.map(i => i.phase)}
        />

        <Separator className="my-8" />

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Variations Section */}
          <div className="lg:col-span-2">
            <Card className="card-premium">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-primary" />
                  {getPhaseTitle(workflowState.currentPhase)}
                </CardTitle>
                <CardDescription>
                  {getPhaseDescription(workflowState.currentPhase)}
                </CardDescription>
              </CardHeader>
              <CardContent>
                {workflowState.isGenerating ? (
                  <div className="flex flex-col items-center justify-center py-12">
                    <Loader2 className="h-8 w-8 animate-spin text-primary mb-4" />
                    <p className="text-muted-foreground mb-4">
                      Generating {workflowState.currentPhase} variations...
                    </p>
                    <Progress value={workflowState.progress} className="w-64" />
                  </div>
                ) : (
                  <VariationSelector
                    variations={currentVariations}
                    selectedId={selectedVariation}
                    onSelect={handleVariationSelect}
                  />
                )}

                {/* Action Buttons */}
                {!workflowState.isGenerating && (
                  <div className="flex justify-between items-center mt-6 pt-6 border-t">
                    <Button 
                      variant="outline" 
                      onClick={startOver}
                      className="flex items-center gap-2"
                    >
                      <RotateCcw className="h-4 w-4" />
                      Start Over
                    </Button>

                    {selectedVariation && currentPhaseIndex < phaseOrder.length - 1 && (
                      <Button 
                        onClick={proceedToNextPhase}
                        className="flex items-center gap-2 bg-primary hover:bg-primary/90"
                      >
                        Continue to {phaseOrder[currentPhaseIndex + 1]}
                        <ArrowRight className="h-4 w-4" />
                      </Button>
                    )}

                    {workflowState.currentPhase === 'final' && (
                      <Button 
                        size="lg"
                        className="bg-primary hover:bg-primary/90"
                      >
                        Generate Production Files
                        <CheckCircle2 className="ml-2 h-4 w-4" />
                      </Button>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Current Selection */}
            {selectedVariation && (
              <Card className="card-premium">
                <CardHeader>
                  <CardTitle className="text-sm">Current Selection</CardTitle>
                </CardHeader>
                <CardContent>
                  <DesignPreview 
                    variation={currentVariations.find(v => v.id === selectedVariation)}
                  />
                </CardContent>
              </Card>
            )}

            {/* Design History */}
            {workflowState.designHistory.iterations.length > 0 && (
              <Card className="card-premium">
                <CardHeader>
                  <CardTitle className="text-sm">Design Journey</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {workflowState.designHistory.iterations.map((iteration, index) => (
                    <div key={iteration.id} className="flex items-center gap-2 text-sm">
                      <Badge variant="secondary" className="w-16">
                        {iteration.phase}
                      </Badge>
                      <span className="text-muted-foreground">
                        {iteration.selectedVariation && 
                          currentVariations.find(v => v.id === iteration.selectedVariation)?.label}
                      </span>
                    </div>
                  ))}
                </CardContent>
              </Card>
            )}

            {/* Cost Tracker */}
            <Card className="card-premium">
              <CardHeader>
                <CardTitle className="text-sm">Session Cost</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Iterations:</span>
                    <span>${(workflowState.designHistory.iterations.length * 0.005).toFixed(3)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Production:</span>
                    <span>$0.19</span>
                  </div>
                  <Separator />
                  <div className="flex justify-between font-medium">
                    <span>Total:</span>
                    <span>${(workflowState.designHistory.iterations.length * 0.005 + 0.19).toFixed(3)}</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}