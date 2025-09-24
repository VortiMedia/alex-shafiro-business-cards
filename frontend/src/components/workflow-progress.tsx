"use client"

import React from 'react'
import { motion } from 'framer-motion'
import { CheckCircle2, Circle, ArrowRight } from 'lucide-react'
import { WorkflowPhase } from '@/types'

interface WorkflowProgressProps {
  currentPhase: WorkflowPhase
  completedPhases: WorkflowPhase[]
}

const PHASES: { phase: WorkflowPhase; label: string; description: string }[] = [
  { phase: 'concept', label: 'Concept', description: 'Choose design direction' },
  { phase: 'layout', label: 'Layout', description: 'Arrange elements' },
  { phase: 'typography', label: 'Typography', description: 'Select fonts' },
  { phase: 'colors', label: 'Colors', description: 'Choose accents' },
  { phase: 'final', label: 'Final', description: 'Production files' }
]

export function WorkflowProgress({ currentPhase, completedPhases }: WorkflowProgressProps) {
  const getCurrentPhaseIndex = () => PHASES.findIndex(p => p.phase === currentPhase)
  const isPhaseCompleted = (phase: WorkflowPhase) => completedPhases.includes(phase)
  const isCurrentPhase = (phase: WorkflowPhase) => phase === currentPhase

  return (
    <div className="max-w-4xl mx-auto">
      {/* Desktop Progress Bar */}
      <div className="hidden md:flex items-center justify-between">
        {PHASES.map((step, index) => (
          <React.Fragment key={step.phase}>
            {/* Step Circle */}
            <div className="flex flex-col items-center">
              <motion.div
                initial={{ scale: 0.8 }}
                animate={{ scale: 1 }}
                className={`relative flex items-center justify-center w-12 h-12 rounded-full border-2 transition-all duration-300 ${
                  isPhaseCompleted(step.phase)
                    ? 'bg-primary border-primary text-primary-foreground'
                    : isCurrentPhase(step.phase)
                    ? 'border-primary bg-primary/10 text-primary'
                    : 'border-muted-foreground/30 text-muted-foreground'
                }`}
              >
                {isPhaseCompleted(step.phase) ? (
                  <CheckCircle2 className="h-6 w-6" />
                ) : (
                  <span className="text-sm font-semibold">{index + 1}</span>
                )}
                
                {/* Active Phase Glow */}
                {isCurrentPhase(step.phase) && (
                  <motion.div
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="absolute inset-0 rounded-full border-2 border-primary/50"
                  />
                )}
              </motion.div>
              
              {/* Labels */}
              <div className="mt-3 text-center">
                <p className={`text-sm font-medium ${
                  isCurrentPhase(step.phase) ? 'text-primary' : 'text-foreground'
                }`}>
                  {step.label}
                </p>
                <p className="text-xs text-muted-foreground">
                  {step.description}
                </p>
              </div>
            </div>
            
            {/* Connection Line */}
            {index < PHASES.length - 1 && (
              <div className="flex-1 mx-4">
                <div className={`h-0.5 transition-colors duration-300 ${
                  getCurrentPhaseIndex() > index
                    ? 'bg-primary'
                    : 'bg-muted-foreground/20'
                }`} />
              </div>
            )}
          </React.Fragment>
        ))}
      </div>

      {/* Mobile Progress */}
      <div className="md:hidden space-y-4">
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <span>Step {getCurrentPhaseIndex() + 1} of {PHASES.length}</span>
          <div className="flex-1 bg-muted-foreground/20 h-1 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${((getCurrentPhaseIndex() + 1) / PHASES.length) * 100}%` }}
              transition={{ duration: 0.5 }}
              className="h-full bg-primary"
            />
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <div className={`flex items-center justify-center w-10 h-10 rounded-full border-2 ${
            'border-primary bg-primary/10 text-primary'
          }`}>
            <span className="text-sm font-semibold">{getCurrentPhaseIndex() + 1}</span>
          </div>
          <div>
            <p className="font-medium text-primary">
              {PHASES[getCurrentPhaseIndex()].label}
            </p>
            <p className="text-sm text-muted-foreground">
              {PHASES[getCurrentPhaseIndex()].description}
            </p>
          </div>
        </div>
        
        {/* Completed Steps */}
        {completedPhases.length > 0 && (
          <div className="text-xs text-muted-foreground">
            Completed: {completedPhases.map(phase => 
              PHASES.find(p => p.phase === phase)?.label
            ).join(', ')}
          </div>
        )}
      </div>
    </div>
  )
}