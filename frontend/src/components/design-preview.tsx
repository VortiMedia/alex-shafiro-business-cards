"use client"

import React from 'react'
import { motion } from 'framer-motion'
import { Badge } from '@/components/ui/badge'
import { DesignVariation } from '@/types'
import Image from 'next/image'

interface DesignPreviewProps {
  variation?: DesignVariation
}

export function DesignPreview({ variation }: DesignPreviewProps) {
  if (!variation) {
    return (
      <div className="flex items-center justify-center h-32 text-muted-foreground text-sm">
        No design selected
      </div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="space-y-3"
    >
      {/* Preview Image */}
      <div className="relative aspect-[16/10] bg-gradient-to-br from-muted/30 to-muted/60 rounded-lg overflow-hidden">
        {variation.imageUrl ? (
          <Image
            src={variation.imageUrl}
            alt={`Selected design ${variation.label}`}
            fill
            className="object-cover"
            sizes="300px"
          />
        ) : (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="w-12 h-8 bg-[#1A1A1A] rounded mx-auto mb-2 flex items-center justify-center">
                <div className="w-1.5 h-1.5 bg-[#00C9A7] rounded-full"></div>
              </div>
              <p className="text-xs text-muted-foreground">
                Card Preview
              </p>
            </div>
          </div>
        )}
        
        {/* Selection Badge Overlay */}
        <div className="absolute top-2 left-2">
          <Badge variant="default" className="bg-primary text-primary-foreground">
            {variation.label}
          </Badge>
        </div>
      </div>
      
      {/* Details */}
      <div className="space-y-2">
        <p className="text-sm font-medium">
          {variation.description}
        </p>
        <p className="text-xs text-muted-foreground">
          {variation.prompt}
        </p>
      </div>
    </motion.div>
  )
}