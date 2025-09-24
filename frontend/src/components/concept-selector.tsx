"use client"

import React from 'react'
import { motion } from 'framer-motion'
import { BusinessCardConcept } from '@/types'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

interface ConceptSelectorProps {
  concepts: BusinessCardConcept[]
  selectedId?: string
  onSelect: (concept: BusinessCardConcept) => void
}

export function ConceptSelector({ concepts, selectedId, onSelect }: ConceptSelectorProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {concepts.map((concept, index) => (
        <motion.div
          key={concept.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
        >
          <Card
            className={`cursor-pointer transition-all hover:scale-105 ${
              selectedId === concept.id ? 'border-primary shadow-emerald' : 'hover:border-primary/50'
            }`}
            onClick={() => onSelect(concept)}
          >
            <CardHeader>
              <CardTitle className="text-lg">{concept.name}</CardTitle>
              <CardDescription>{concept.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="aspect-[16/10] bg-gradient-to-br from-muted/30 to-muted/60 rounded-lg flex items-center justify-center">
                <p className="text-xs text-muted-foreground">Preview</p>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      ))}
    </div>
  )
}