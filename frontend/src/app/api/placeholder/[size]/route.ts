import { NextRequest, NextResponse } from 'next/server'

export async function GET(
  request: NextRequest,
  { params }: { params: { size: string } }
) {
  const { searchParams } = new URL(request.url)
  const text = searchParams.get('text') || 'Business Card'
  const bg = searchParams.get('bg') || '1a1a1a'
  const color = searchParams.get('color') || '00c9a7'
  const [width, height] = params.size.split('x').map(Number)

  // Create SVG placeholder
  const svg = `
    <svg width="${width}" height="${height}" xmlns="http://www.w3.org/2000/svg">
      <rect width="100%" height="100%" fill="#${bg}"/>
      <rect x="10%" y="10%" width="80%" height="80%" rx="8" fill="none" stroke="#${color}" stroke-width="2" opacity="0.3"/>
      <circle cx="20%" cy="30%" r="4" fill="#${color}" opacity="0.6"/>
      <text x="50%" y="50%" font-family="Arial, sans-serif" font-size="14" fill="#${color}" text-anchor="middle" dominant-baseline="middle">
        ${text.replace(/\+/g, ' ')}
      </text>
      <text x="50%" y="70%" font-family="Arial, sans-serif" font-size="10" fill="#${color}" text-anchor="middle" opacity="0.7">
        A Stronger Life
      </text>
    </svg>
  `

  return new NextResponse(svg, {
    headers: {
      'Content-Type': 'image/svg+xml',
      'Cache-Control': 'public, max-age=86400', // Cache for 1 day
    },
  })
}