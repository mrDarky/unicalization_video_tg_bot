# Enhanced Video Processing Modes - User Guide

This document describes the enhanced video processing capabilities of the Telegram bot.

## Overview

The bot now supports three powerful video processing modes with a **filters-first** workflow:

1. **Mode 1**: Process multiple videos with the same settings
2. **Mode 2**: Process two video groups with different settings and combine them
3. **Mode N**: Process 3-5 video groups with different settings and combine them

## Mode 1: Single Configuration, Multiple Videos

### Workflow
1. **Configure Modifications First**: Choose all the filters and modifications you want to apply
2. **Upload Multiple Videos**: Send one or more videos to the bot
3. **Process All**: All videos will be processed with the same settings

### Example Use Case
You have 5 videos and want to apply the same blur filter and speed change to all of them:
- Select modifications: Blur filter, Speed 1.5x
- Upload 5 videos
- Get back 5 processed videos, all with the same modifications

### Benefits
- Consistent processing across all videos
- Save time configuring the same settings multiple times
- Batch processing efficiency

## Mode 2: Two Video Groups with Combining

### Workflow
1. **Configure Group 1 Modifications**: Set up filters for the first group of videos
2. **Upload Group 1 Videos**: Send one or more videos for group 1
3. **Configure Group 2 Modifications**: Set up filters for the second group of videos  
4. **Upload Group 2 Videos**: Send one or more videos for group 2
5. **Select Combining Strategy**: Choose how to combine videos from both groups
6. **Select Layout**: Choose the merge layout (horizontal, vertical, sequential)

### Combining Strategies

#### First-with-First Pairing (1:1)
Pairs the first video from Group 1 with the first video from Group 2, second with second, etc.

**Example:**
- Group 1: [A, B, C]
- Group 2: [X, Y, Z]
- Result: [A+X, B+Y, C+Z] (3 videos)

#### All-with-All (Cartesian Product)
Every video from Group 1 is combined with every video from Group 2.

**Example:**
- Group 1: [A, B]
- Group 2: [X, Y, Z]
- Result: [A+X, A+Y, A+Z, B+X, B+Y, B+Z] (6 videos)

#### Sequential
All videos from Group 1 followed by all videos from Group 2 in one long video.

**Example:**
- Group 1: [A, B]
- Group 2: [X, Y]
- Result: [A→B→X→Y] (1 video)

### Layout Options
- **Horizontal**: Videos side-by-side
- **Vertical**: Videos stacked top-to-bottom
- **Sequential**: Videos played one after another

### Example Use Cases

**Product Comparison Videos:**
- Group 1: 3 videos of Product A (with brightness filter)
- Group 2: 3 videos of Product B (with contrast filter)
- Strategy: First-with-First
- Layout: Horizontal
- Result: 3 side-by-side comparison videos

**Marketing Content:**
- Group 1: 2 intro videos (with text overlay)
- Group 2: 5 product demo videos (with speed change)
- Strategy: All-with-All
- Layout: Sequential
- Result: 10 videos, each with an intro followed by a demo

## Mode N: Multiple Video Groups

### Workflow
1. **Select Number of Groups**: Choose 3, 4, or 5 groups
2. **For Each Group**:
   - Configure modifications
   - Upload one or more videos
3. **Select Combining Strategy**: Choose how to combine all groups
4. **Select Layout**: Choose the merge layout

### Combining Strategies

All strategies from Mode 2 apply, but now work with N groups:

#### First-with-First Pairing
Takes the first video from each group and combines them, then second from each group, etc.

**Example (3 groups):**
- Group 1: [A1, A2]
- Group 2: [B1, B2, B3]
- Group 3: [C1, C2]
- Result: [A1+B1+C1, A2+B2+C2] (2 videos)

#### All-with-All (Cartesian Product)
Every possible combination of videos from all groups.

**Example (3 groups):**
- Group 1: [A1, A2]
- Group 2: [B1, B2]
- Group 3: [C1]
- Result: [A1+B1+C1, A1+B2+C1, A2+B1+C1, A2+B2+C1] (4 videos)

**Note:** This can create many videos! With 2 videos in each of 3 groups, you get 2×2×2 = 8 videos.

#### Sequential
All videos from all groups played in order.

**Example:**
- Group 1: [A1, A2]
- Group 2: [B1]
- Group 3: [C1, C2, C3]
- Result: [A1→A2→B1→C1→C2→C3] (1 video)

### Example Use Cases

**Multi-Angle Product Review (3 groups):**
- Group 1: Front view videos (brightness +10%)
- Group 2: Side view videos (contrast +20%)
- Group 3: Top view videos (saturation +15%)
- Strategy: First-with-First
- Layout: Horizontal
- Result: Multi-angle synchronized views

**Tutorial Series (4 groups):**
- Group 1: Intro videos
- Group 2: Step 1 demonstrations
- Group 3: Step 2 demonstrations
- Group 4: Outro videos
- Strategy: Sequential
- Layout: Sequential
- Result: Complete tutorial videos

**A/B/C Testing Content (5 groups):**
- Group 1-5: Different versions of the same content with different filters
- Strategy: All videos from each group processed individually
- Result: Multiple variations for testing

## Available Modifications

All modes support the following modifications:

- **Speed Change**: 0.5x to 2.0x playback speed
- **Scale/Resize**: Custom dimensions (e.g., 1920x1080, 1280x720)
- **Filters**:
  - Hue adjustment
  - Brightness adjustment
  - Contrast adjustment
  - Saturation adjustment
  - Blur effect
  - Sharpen effect
  - Grayscale conversion
  - Sepia tone
  - Negative/Invert colors
  - Noise effect
- **Rotation**: 90°, 180°, 270°, or -90°
- **Text Overlay**: Add custom text to videos
- **Trim/Cut**: Cut video to specific length
- **Crop**: Crop video to specific dimensions

## Tips and Best Practices

1. **Start Small**: Test with 1-2 videos per group first before uploading many
2. **Watch File Sizes**: Larger videos take longer to process
3. **Cartesian Product Warning**: "All-with-All" strategy can create many videos quickly
4. **Consistent Formats**: Use videos with similar resolutions for best results when merging
5. **Preview First**: Process a single video to preview the effect before batch processing

## Limits

- Maximum video size: 100MB per video (configurable)
- Cartesian product: Limited to 100 combinations in Mode N to prevent overload
- Processing time: Depends on video size and number of modifications

## Troubleshooting

**Issue: Videos not merging properly**
- Solution: Ensure videos have similar resolutions or use scale modification first

**Issue: Processing takes too long**
- Solution: Reduce video size, use fewer modifications, or process fewer videos at once

**Issue: Not enough space for all combinations**
- Solution: Use First-with-First or Sequential strategy instead of All-with-All

## Command Reference

- `/start` - Start the bot and show main menu
- `🎬 Process 1 Video` - Enter Mode 1
- `🎥 Process 2 Videos` - Enter Mode 2
- `🎞️ Process N Videos` - Enter Mode N
- `/help` - Show help information

## Examples

### Example 1: Batch Filter Application
**Scenario**: Apply sepia filter to 10 vacation videos

1. Click "🎬 Process 1 Video"
2. Select "🎨 Apply Filter" → "📜 Sepia"
3. Click "✅ Done"
4. Upload all 10 videos
5. Click "✅ Done - Process Videos"
6. Receive 10 sepia-filtered videos

### Example 2: Before/After Comparison
**Scenario**: Create side-by-side comparison of original vs edited

1. Click "🎥 Process 2 Videos"
2. Configure Group 1: No modifications (original)
3. Upload original videos
4. Configure Group 2: Brightness +30%, Contrast +20%
5. Upload same videos again
6. Select "First-with-First" strategy
7. Select "Horizontal" layout
8. Receive comparison videos

### Example 3: Video Montage
**Scenario**: Create a montage from different scenes

1. Click "🎞️ Process N Videos"
2. Select "4️⃣ 4 Groups"
3. For each group, configure filters and upload scene videos
4. Select "Sequential" strategy
5. Select "Sequential" layout
6. Receive one complete montage video

---

**Need help?** Contact support or use the `/help` command in the bot.
