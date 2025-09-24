"use client"

import React from 'react'
import { motion } from 'framer-motion'
import { Check, Eye } from 'lucide-react'
import Image from 'next/image'

import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { DesignVariation } from '@/types'

interface VariationSelectorProps {
  variations: DesignVariation[]
  selectedId: string | null
  onSelect: (id: string) => void
}

export function VariationSelector({ variations, selectedId, onSelect }: VariationSelectorProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {variations.map((variation, index) => (
        <motion.div
          key={variation.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
          className="group relative"
        >
          <Card 
            className={`cursor-pointer transition-all duration-300 hover:scale-105 ${
              selectedId === variation.id 
                ? 'border-primary bg-card/80' 
                : 'hover:border-primary/50'
            }`}
            style={{
              boxShadow: selectedId === variation.id ? '0 0 20px rgba(0, 201, 167, 0.1)' : undefined
            }}
            onClick={() => onSelect(variation.id)}
          >
            <CardContent className="p-4">
              {/* Selection Badge */}
              <div className="flex items-center justify-between mb-3">
                <Badge 
                  variant={selectedId === variation.id ? 'default' : 'secondary'}
                  className={selectedId === variation.id ? 'bg-primary text-primary-foreground' : ''}
                >
                  Option {variation.label}
                </Badge>
                
                {selectedId === variation.id && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="flex items-center gap-1 text-primary"
                  >
                    <Check className="h-4 w-4" />
                    <span className="text-xs font-medium">Selected</span>
                  </motion.div>
                )}
              </div>

              {/* Design Preview */}
              <div className="relative aspect-[16/10] bg-gradient-to-br from-muted/50 to-muted rounded-lg overflow-hidden mb-3">
                {variation.imageUrl ? (
                  <Image
                    src={variation.imageUrl}
                    alt={`Design variation ${variation.label}`}
                    fill
                    className="object-cover"
                    sizes="(max-width: 768px) 100vw, 50vw"
                  />
                ) : (
                  <div className="flex items-center justify-center h-full">
                    <div className="text-center">
                      <div className="w-16 h-10 bg-[#1A1A1A] rounded mx-auto mb-2 flex items-center justify-center">
                        <div className="w-2 h-2 bg-[#00C9A7] rounded-full"></div>
                      </div>
                      <p className="text-xs text-muted-foreground">
                        Business Card Preview
                      </p>
                    </div>
                  </div>
                )}
                
                {/* Hover Overlay */}
                <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors duration-300 flex items-center justify-center opacity-0 group-hover:opacity-100">
                  <Button size="sm" variant="secondary" className="gap-2">
                    <Eye className="h-3 w-3" />
                    Preview
                  </Button>
                </div>
              </div>

              {/* Description */}
              <div>
                <p className="text-sm font-medium mb-1">
                  {variation.description}
                </p>
                <p className="text-xs text-muted-foreground line-clamp-2">
                  {variation.prompt}
                </p>
              </div>

              {/* Selection Indicator Ring */}
              {selectedId === variation.id && (
                <motion.div
                  initial={{ scale: 0.8, opacity: 0 }}
                  animate={{ scale: 1, opacity: 1 }}
                  className="absolute inset-0 rounded-lg border-2 border-primary pointer-events-none"
                />
              )}
            </CardContent>
          </Card>
        </motion.div>
      ))}
    </div>
  )
}