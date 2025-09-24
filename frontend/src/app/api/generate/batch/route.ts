import { NextRequest, NextResponse } from 'next/server'

interface BatchGenerateRequest {
  phase: 'concept' | 'layout' | 'typography' | 'colors' | 'final'
  baseConcept?: string
  quality: 'draft' | 'review' | 'production'
  count?: number
}

export async function POST(request: NextRequest) {
  try {
    const body: BatchGenerateRequest = await request.json()
    const { phase, baseConcept, quality, count = 4 } = body

    // Validate request
    if (!phase) {
      return NextResponse.json(
        { error: 'Missing required field: phase' },
        { status: 400 }
      )
    }

    // Generate mock variations based on phase
    const variations = Array.from({ length: count }, (_, index) => {
      let label: string
      let description: string

      switch (phase) {
        case 'concept':
          const concepts = ['Clinical Precision', 'Athletic Edge', 'Luxury Wellness', 'Minimalist Pro']
          label = String.fromCharCode(65 + index) // A, B, C, D
          description = concepts[index] || `Concept ${index + 1}`
          break
        case 'layout':
          label = (index + 1).toString()
          description = [
            'Logo top-left, contact bottom-right',
            'Centered logo, contact info below',
            'Vertical layout, logo left side',
            'Horizontal split, balanced design'
          ][index] || `Layout ${index + 1}`
          break
        case 'typography':
          label = String.fromCharCode(97 + index) // a, b, c, d
          description = [
            'Bold sans-serif, high contrast',
            'Light weight, more spacing',
            'Mixed weights, visual hierarchy',
            'Condensed font, compact layout'
          ][index] || `Typography ${index + 1}`
          break
        case 'colors':
          label = ['i', 'ii', 'iii', 'iv'][index] || (index + 1).toString()
          description = [
            'Emerald accent on name only',
            'Emerald accent on company name',
            'Emerald glow background element',
            'Emerald border accent'
          ][index] || `Color ${index + 1}`
          break
        default:
          label = (index + 1).toString()
          description = `Final variation ${index + 1}`
      }

      return {
        id: `${phase}-${index + 1}`,
        label,
        description,
        imageUrl: `/api/placeholder/400/250?text=${encodeURIComponent(description)}&bg=1a1a1a&color=00c9a7`,
        prompt: `${phase} refinement: ${description}`,
        cost: quality === 'production' ? 0.19 : 0.005
      }
    })

    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 2000))

    const response = {
      success: true,
      jobId: `batch-${Date.now()}`,
      variations,
      totalCost: variations.reduce((sum, v) => sum + v.cost, 0),
      model: 'gemini',
      metadata: {
        phase,
        baseConcept,
        quality,
        count,
        timestamp: new Date().toISOString()
      }
    }

    return NextResponse.json(response)

  } catch (error) {
    console.error('Batch generation API error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}