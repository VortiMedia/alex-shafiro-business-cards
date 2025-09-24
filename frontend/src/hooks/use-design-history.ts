"use client"

import { useState, useCallback } from 'react'
import { DesignHistory, DesignIteration, WorkflowPhase, DesignVariation, BusinessCardConcept } from '@/types'

interface UseDesignHistoryReturn {
  history: DesignHistory
  addIteration: (iteration: Omit<DesignIteration, 'id' | 'timestamp'>) => void
  updateIteration: (iterationId: string, updates: Partial<DesignIteration>) => void
  getIterationByPhase: (phase: WorkflowPhase) => DesignIteration | undefined
  getSelectedVariationByPhase: (phase: WorkflowPhase) => DesignVariation | undefined
  exportHistory: () => string
  importHistory: (historyJson: string) => boolean
  clearHistory: () => void
  getCompletedPhases: () => WorkflowPhase[]
  getCurrentSelectionPath: () => string
}

const createInitialHistory = (): DesignHistory => ({
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
})

export function useDesignHistory(): UseDesignHistoryReturn {
  const [history, setHistory] = useState<DesignHistory>(createInitialHistory)

  const addIteration = useCallback((iteration: Omit<DesignIteration, 'id' | 'timestamp'>) => {
    const newIteration: DesignIteration = {
      ...iteration,
      id: `iteration-${Date.now()}`,
      timestamp: new Date()
    }

    setHistory(prev => ({
      ...prev,
      iterations: [...prev.iterations, newIteration]
    }))
  }, [])

  const updateIteration = useCallback((iterationId: string, updates: Partial<DesignIteration>) => {
    setHistory(prev => ({
      ...prev,
      iterations: prev.iterations.map(iteration =>
        iteration.id === iterationId
          ? { ...iteration, ...updates }
          : iteration
      )
    }))
  }, [])

  const getIterationByPhase = useCallback((phase: WorkflowPhase) => {
    return history.iterations.find(iteration => iteration.phase === phase)
  }, [history.iterations])

  const getSelectedVariationByPhase = useCallback((phase: WorkflowPhase) => {
    const iteration = getIterationByPhase(phase)
    if (!iteration || !iteration.selectedVariation) return undefined
    
    return iteration.variations.find(variation => variation.id === iteration.selectedVariation)
  }, [getIterationByPhase])

  const exportHistory = useCallback(() => {
    return JSON.stringify(history, null, 2)
  }, [history])

  const importHistory = useCallback((historyJson: string) => {
    try {
      const importedHistory = JSON.parse(historyJson) as DesignHistory
      
      // Validate the structure
      if (!importedHistory.sessionId || !importedHistory.iterations || !importedHistory.clientInfo) {
        return false
      }
      
      setHistory(importedHistory)
      return true
    } catch (error) {
      console.error('Failed to import history:', error)
      return false
    }
  }, [])

  const clearHistory = useCallback(() => {
    setHistory(createInitialHistory())
  }, [])

  const getCompletedPhases = useCallback(() => {
    return history.iterations
      .filter(iteration => iteration.selectedVariation)
      .map(iteration => iteration.phase)
  }, [history.iterations])

  const getCurrentSelectionPath = useCallback(() => {
    const selections = history.iterations
      .filter(iteration => iteration.selectedVariation)
      .map(iteration => {
        const selectedVar = iteration.variations.find(v => v.id === iteration.selectedVariation)
        return `${iteration.phase}:${selectedVar?.label || '?'}`
      })
    
    return selections.join(' → ')
  }, [history.iterations])

  return {
    history,
    addIteration,
    updateIteration,
    getIterationByPhase,
    getSelectedVariationByPhase,
    exportHistory,
    importHistory,
    clearHistory,
    getCompletedPhases,
    getCurrentSelectionPath
  }
}