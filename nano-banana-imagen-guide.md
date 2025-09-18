# 🟡 Nano Banana (Gemini 2.5 Flash Image) + 🖼️ Imagen — Ultimate Prompting & API Guide

A single, practical reference that merges **Google’s Imagen docs** with a distilled **Nano Banana (Gemini 2.5 Flash Image)** tutorial. Designed for builders who want **repeatable quality**—whether you’re calling the API or prompting via Google AI Studio.

---

## TL;DR — What You Can Do
- **Text → Image** with Nano Banana (Gemini 2.5 Flash Image) and **Imagen 4 / 3** models.
- **Edit images** via text (inpainting / semantic masking).
- **Compose multi-image scenes** (style transfer & composition).
- **Parameterize prompts** for reliable, on-brand outputs.
- **Dial in photorealism** with camera & lens vocabulary.
- **Place short text into images** (titles, posters, labels).

> All Imagen outputs include a **SynthID watermark**. Prompt length max (Imagen): **480 tokens**.

---

## Quick Start — Imagen API (Python)

```python
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

client = genai.Client()

response = client.models.generate_images(
    model="imagen-4.0-generate-001",
    prompt="Robot holding a red skateboard",
    config=types.GenerateImagesConfig(
        number_of_images=4,  # 1–4
    )
)

for generated_image in response.generated_images:
    generated_image.image.show()
```

**Key Config**
- `numberOfImages`: 1–4 (default: 4)
- `sampleImageSize`: `1K` or `2K` (*Ultra/Standard only*, default: `1K`)
- `aspectRatio`: `"1:1" | "3:4" | "4:3" | "9:16" | "16:9"` (default: `1:1`)
- `personGeneration`: `"dont_allow" | "allow_adult"(default) | "allow_all"`  
  > `allow_all` **not allowed** in EU/UK/CH/MENA

---

## Model Matrix

### Imagen 4
- **Models**: `imagen-4.0-generate-001`, `imagen-4.0-ultra-generate-001`, `imagen-4.0-fast-generate-001`
- **Input**: Text (≤ **480** tokens)
- **Output**: Images (**1–4**)
- **Updated**: **June 2025**

### Imagen 3
- **Model**: `imagen-3.0-generate-002`
- **Input**: Text
- **Output**: Images (up to **4**)
- **Updated**: **February 2025**

> You can also generate images using **Gemini’s built‑in multimodal** capabilities (Nano Banana / Gemini 2.5 Flash Image).

---

## Core Prompting Framework (Works for Nano Banana & Imagen)

**Always structure prompts as:**

**Subject** + **Context/Background** + **Style/Medium** + **Lighting/Mood** + **Framing/Lens** + **Quality Modifiers** + **Aspect Ratio**

**Example (general):**
```
A sketch of a modern apartment building (subject) surrounded by skyscrapers (context), isometric style (style), soft morning light (lighting), clean minimal lines, high-quality (quality), 4:3 aspect ratio (framing).
```

### Iterative Refinement (Essential)
Start broad → inspect → add details → repeat until it matches your vision.

**Example (evolving a scene):**
- `A park in the spring next to a lake`
- `... golden hour, the sun setting across the lake`
- `... golden hour, red wildflowers, shallow depth of field`

---

## Templates You’ll Actually Reuse

### 1) Photorealistic Portrait (Reliable)
```
Close-up portrait photo of a [subject; age/look/persona] on a [location], [lighting style: soft warm backlight + cool fill], [mood], 
shot on a [35mm/50mm] prime lens at [f/1.8–f/2.8], shallow depth of field, subtle skin texture, natural color grading, 
high dynamic range, professional photography, 4K, ultra detailed, [aspect ratio].
```

**Notes from field testing**
- Nano Banana may **not always respect aspect ratio**—include it, but validate output.
- Use **lens + aperture** to force bokeh & depth cues.

### 2) Cinematic Landscape
```
Wide shot of [landscape/region] during [golden hour/blue hour/foggy dawn], atmospheric haze, dramatic sky, 
shot on [24mm wide-angle] at [f/8], long exposure hints (smooth water/clouds), 
professional photography, HDR, highly detailed textures, [aspect ratio].
```

### 3) Product Photo (E‑commerce/Ads)
```
Studio-lit product photograph of a [material/color] [product], on [background surface/material], 
soft diffused key light with gentle rim light, sharp focus, high-resolution, minimal reflections, 
ultra realistic with crisp edges, commercial grade, [aspect ratio].
```

**Tip:** Mention **transmission/refraction** for glass/liquids: “light passes through the frosted blue glass casting a faint blue shadow.”

### 4) Illustration / Anime
```
[Subject/action] in [art style: Studio Ghibli / retro anime / watercolor / ink sketch], 
limited color palette ([colors]), soft cel shading, warm ambient lighting, 
clean line art, expressive character design, cinematic framing, [aspect ratio].
```

### 5) Text in Image (Poster/Label)
```
Poster design titled "[TITLE]" in bold [font vibe], subtitle "[TAGLINE]" below, 
clean layout with strong hierarchy, high contrast, legible at small sizes, 
limit text length to <= 25 characters, 1–3 distinct phrases max, [aspect ratio].
```

**Reality check:** Imagen’s text rendering is improving; **regenerate** if spacing/kerning is off.

### 6) Parameterized Logos (For Apps/Forms)
```
A {logo_style} logo for a {company_area} company on a solid color background. 
Include the text {company_name}. Minimal, scalable, crisp edges.
```

---

## Aspect Ratios (When They Matter)
- **1:1** (default) — social posts, avatars
- **4:3** — classic photography, editorial/layouts
- **3:4** — full-height portrait, ads
- **16:9** — landscape, web hero, YouTube thumbnails
- **9:16** — shorts/reels, tall architecture/objects

> If AR is ignored, **crop or regenerate**; add framing hints (“full body centered,” “tight headshot,” etc.).

---

## Photorealism Cheatsheet

| Use Case | Lens | Focal Length | Extras |
|---|---|---|---|
| **Portraits** | Prime/Zoom | 24–35mm | Film noir, duotone (two colors), depth of field |
| **Objects / Food / Plants** | **Macro** | 60–105mm | High detail, controlled lighting |
| **Sports / Wildlife** | Telephoto Zoom | 100–400mm | Fast shutter, motion tracking |
| **Astro / Landscapes** | Wide-angle | 10–24mm | Long exposure, smooth water/clouds |

**Quality Modifiers**  
- General: `high-quality`, `beautiful`, `stylized`  
- Photos: `4K`, `HDR`, `studio photo`  
- Art: `detailed`, `by a professional`

---

## Editing Images (Inpainting / Semantic Masking)

**One-shot edit (color/material change):**
```
Edit the uploaded photo. Change only the [object] to [new color/material]. 
Preserve lighting, reflections, and all other elements. Seamless inpainting.
```

**Multi-step edits (safer for complex changes):**
1. Change object A.  
2. Approve → Re-submit result as input.  
3. Change object B.  
4. Approve → Continue.

**Composition / Multi-image merge:**
```
Combine the outfit from Image A with the model in Image B. 
Output a realistic full-body shot, matching lighting and shadows to the background. 
Blend fabric physics, correct perspective and body pose.
```
> Results vary. If physics look “pasted,” re-run with **pose / fabric / shadow** hints.

---

## Six Best Practices (Distilled from Google’s Guide + Field Notes)

1) **Be hyper‑specific**  
Describe materials, edges, lighting direction, micro‑details (stitching, patina, grain).

2) **Provide context + intent**  
State the **use case** (logo for high‑end minimalist skincare brand) to guide taste.

3) **Refine conversationally**  
Iterate: base → recolor → relight → reframe → retouch. Don’t chase perfection in one shot.

4) **Break complex scenes into steps**  
Use “First…, then…, finally…” to control composition and hierarchy **in one prompt**; or multi‑prompt stages.

5) **Use semantic negatives**  
Prefer “empty, deserted street” over “no cars”. Describe absence positively.

6) **Speak photography**  
Use **lens/focal length/aperture/lighting** to enforce look and composition.

---

## Field-Tested Examples (Nano Banana)

**Portrait (street musician, 60s):**
```
Close-up portrait of a street musician in their 60s, warm artificial tunnel lighting mixed with cool fluorescent overhead light, 
35mm at f/2.2, shallow depth of field, honest wrinkles and skin texture, cinematic color grade, muted tones, professional photography, 4K.
```

**Cinematic Hiker (Scottish Highlands):**
```
Wide shot of a mountain hiker in rugged alpine terrain, Scottish Highlands at golden hour, 24mm wide angle at f/8, dramatic clouds, 
crisp ridgelines, subtle atmospheric haze, travel magazine photo, HDR, highly detailed textures.
```

**Studio Product (Skincare):**
```
Ultra-realistic studio-lit product photograph of a frosted blue glass skincare bottle on a white sandy textured background, 
soft key light with subtle rim light, light passes through glass casting a faint blue shadow, sharp focus, commercial grade, 4K.
```

**Anime Illustration (Ghibli vibe):**
```
A botanist examining a glowing mushroom in an enchanted forest, retro anime style, muted sage green palette, 
soft cel shading, warm ambient lighting, gentle bloom highlights, cinematic framing.
```

**Poster With Text:**
```
Poster design titled "Summerland" in bold geometric sans-serif; subtitle "Summer never felt so good" below. 
Strong visual hierarchy, clean composition, text <= 25 characters per line, legible at small sizes.
```

---

## Troubleshooting & Consistency

- **Aspect ratio ignored?** Add explicit framing (“full-height centered subject, head-to-toe in frame”), then crop if needed.
- **Faces/hands off?** Emphasize “portrait, natural skin, subtle pores, realistic hands,” regenerate 2–3x.
- **Style drift?** Lock with **style tags** or anchor with a **reference image** (Gemini multimodal).
- **Blurry product edges?** Specify “hard, crisp edges; sharp focus; controlled reflection.”
- **Text messy?** Keep it **short**; regenerate; try fewer phrases; guide font *vibe* not exact font.

---

## Handy Checklists

**Before Prompting**
- Subject, context, style picked?
- Lighting + lens chosen?
- Quality modifiers added?
- Aspect ratio decided?

**For Edits**
- Identify *only* what changes.
- Preserve everything else explicitly.
- Consider multi-step edits for complex changes.

**For Logos / Params**
- Use `{variables}` for style / sector / name.
- Enforce background rule (e.g., “solid color background”).

---

## Example: Prompt Bank (Copy/Paste)

**Moody City Night Car**
```
Cinematic three-quarter view of a black coupe on wet neon-lit city streets at night, reflective asphalt, 
cool cyan and magenta rim lighting, light rain particles, 50mm lens at f/2.0, shallow depth, filmic contrast, 16:9.
```

**Editorial Food**
```
Overhead photo of a handmade margherita pizza on a rustic wooden table, natural window light, soft shadows, 
crisp basil leaves, blistered crust detail, macro textures, professional food photography, 4:3.
```

**Architectural Sketch**
```
Isometric sketch of a modern apartment building surrounded by taller skyscrapers, fine technical linework, 
subtle hatching, grayscale with selective highlight accents, presentation-board ready, 3:4.
```

---

## Notes & Sources
- Techniques consolidated from Google’s **Imagen** documentation and a Nano Banana walkthrough.
- Imagen models embed **SynthID** watermarks.
- Prompt length (Imagen): **≤ 480 tokens**.

---

## Appendix — Frequently Used Phrases
- **Lighting**: softbox, rim light, backlight, volumetric light, golden hour, blue hour
- **Lenses**: 24mm wide-angle, 35mm/50mm prime, 85mm portrait, 100mm macro, 200mm telephoto
- **Qualities**: editorial, cinematic, commercial grade, ultra-detailed, HDR, 4K
- **Surfaces**: matte, glossy, brushed metal, frosted glass, patina, grain
- **Composition**: rule of thirds, centered, symmetrical, leading lines, shallow DOF
