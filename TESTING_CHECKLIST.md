# Testing Checklist for Enhanced Video Processing Modes

Use this checklist to validate the new video processing features.

## Prerequisites

- [ ] Bot is running (`python bot_main.py`)
- [ ] Bot token is configured in `.env`
- [ ] FFmpeg is installed and accessible
- [ ] Temp directories exist and are writable
- [ ] At least 2-3 sample videos available for testing (small files recommended, e.g., <10MB each)

## Mode 1 Testing

### Basic Flow
- [ ] Start bot with `/start`
- [ ] Click "🎬 Process 1 Video"
- [ ] Verify: Bot shows modifications selection keyboard
- [ ] Select a modification (e.g., "⚡ Change Speed")
- [ ] Enter a valid value (e.g., "1.5")
- [ ] Verify: Bot confirms modification added
- [ ] Click "✅ Done"
- [ ] Verify: Bot prompts for video upload with "Done" button

### Single Video
- [ ] Upload 1 video
- [ ] Verify: Bot confirms video received
- [ ] Click "✅ Done - Process Videos"
- [ ] Verify: Bot processes and returns 1 modified video

### Multiple Videos
- [ ] Repeat Mode 1 flow
- [ ] Configure modifications
- [ ] Upload 3 videos
- [ ] Verify: Bot confirms each video (Video 1, Video 2, Video 3)
- [ ] Click "✅ Done - Process Videos"
- [ ] Verify: Bot returns 3 processed videos, all with the same modifications

### No Modifications
- [ ] Start Mode 1
- [ ] Click "✅ Done" without selecting modifications
- [ ] Upload video(s)
- [ ] Verify: Videos are processed (copied without modifications)

## Mode 2 Testing

### Basic Flow - First-with-First
- [ ] Click "🎥 Process 2 Videos"
- [ ] Verify: Bot shows modifications for Group 1
- [ ] Select modification for Group 1 (e.g., "🎨 Apply Filter" → "☀️ Brightness")
- [ ] Click "✅ Done"
- [ ] Upload 2 videos for Group 1
- [ ] Click "✅ Done"
- [ ] Verify: Bot prompts for Group 2 modifications
- [ ] Select modification for Group 2 (e.g., "🎨 Apply Filter" → "📜 Sepia")
- [ ] Click "✅ Done"
- [ ] Upload 2 videos for Group 2
- [ ] Click "✅ Done"
- [ ] Select "1️⃣ First with First (1:1 pairing)"
- [ ] Select layout (e.g., "➡️ Horizontal")
- [ ] Verify: Bot returns 2 merged videos (1:1 pairing)

### All-with-All Strategy
- [ ] Repeat Mode 2 flow
- [ ] Upload 2 videos for Group 1
- [ ] Upload 2 videos for Group 2
- [ ] Select "🔢 All with All (cartesian)"
- [ ] Select layout
- [ ] Verify: Bot returns 4 merged videos (2×2 combinations)

### Sequential Strategy
- [ ] Repeat Mode 2 flow
- [ ] Upload 2 videos for Group 1
- [ ] Upload 2 videos for Group 2
- [ ] Select "🔄 Sequential"
- [ ] Verify: Bot returns 1 long video with all 4 videos concatenated

### Different Layouts
- [ ] Test horizontal layout: Videos should be side-by-side
- [ ] Test vertical layout: Videos should be top-to-bottom
- [ ] Test sequential layout: Videos should play one after another

## Mode N Testing

### 3 Groups - First-with-First
- [ ] Click "🎞️ Process N Videos"
- [ ] Select "3️⃣ 3 Groups"
- [ ] Configure and upload videos for Group 1 (upload 2 videos)
- [ ] Configure and upload videos for Group 2 (upload 2 videos)
- [ ] Configure and upload videos for Group 3 (upload 2 videos)
- [ ] Select "1️⃣ First with First"
- [ ] Select layout
- [ ] Verify: Bot returns 2 combined videos (first from each group, second from each group)

### 4 Groups - Sequential
- [ ] Select "4️⃣ 4 Groups"
- [ ] Configure and upload videos for each group
- [ ] Select "🔄 Sequential"
- [ ] Verify: Bot returns 1 long video with all groups concatenated

### 5 Groups - All-with-All (Limited)
- [ ] Select "5️⃣ 5 Groups"
- [ ] Upload 1 video for each group (5 total)
- [ ] Select "🔢 All with All"
- [ ] Verify: Bot returns 1 combined video (1×1×1×1×1 = 1)
- [ ] Try with 2 videos per group
- [ ] Verify: Bot limits to 100 combinations or returns appropriate number

## Modification Types Testing

Test each modification type in Mode 1:

- [ ] **Speed**: Enter 0.5, 1.5, 2.0 - verify playback speed changes
- [ ] **Filter - Brightness**: Verify video brightness changes
- [ ] **Filter - Blur**: Verify video has blur effect
- [ ] **Filter - Sepia**: Verify sepia tone applied
- [ ] **Filter - Grayscale**: Verify black and white
- [ ] **Scale**: Enter "1280 720" - verify resolution change
- [ ] **Rotate**: Enter "90" - verify 90° rotation
- [ ] **Text**: Enter "Test Text" - verify text overlay appears

## Error Handling Testing

- [ ] Upload video > 100MB: Verify error message about file size
- [ ] Enter invalid speed (e.g., "5"): Verify error message
- [ ] Enter invalid scale (e.g., "abc"): Verify error message
- [ ] Enter invalid rotation (e.g., "45"): Verify error message
- [ ] Click "Done" without uploading videos: Verify error message
- [ ] Cancel operation: Verify bot returns to main menu

## Edge Cases

- [ ] Upload 1 video in Group 1, 5 videos in Group 2, strategy First-with-First: Only 1 pair should be created
- [ ] Upload 10 videos in Mode 1: All should process successfully
- [ ] Apply multiple modifications in sequence: All should apply correctly
- [ ] Use non-standard video formats: Verify FFmpeg handles them

## UI/UX Testing

- [ ] All buttons have clear labels
- [ ] Progress messages are displayed
- [ ] Error messages are helpful
- [ ] Success messages confirm actions
- [ ] Video counters are accurate (e.g., "Video 1 received", "Group 1 Video 2")
- [ ] Cancel button works at all stages

## Performance Testing

- [ ] Process 5 videos simultaneously in Mode 1: Monitor time and memory
- [ ] Create 20 combinations with All-with-All: Verify reasonable processing time
- [ ] Process large videos (50MB+): Verify no crashes

## Cleanup Testing

- [ ] After processing, check temp directory: Verify temporary files are cleaned up
- [ ] Check processed directory: Verify final videos are saved
- [ ] Verify database records are updated with correct status

## Integration Testing

- [ ] Multiple users using bot simultaneously: Verify no state conflicts
- [ ] Process videos while admin panel is open: Verify database updates
- [ ] Check user statistics after processing: Verify counts are accurate

## Documentation Verification

- [ ] ENHANCED_MODES_GUIDE.md examples match actual behavior
- [ ] WORKFLOWS_VISUAL.md diagrams match actual workflow
- [ ] README.md feature list is accurate

## Issues Found

Record any issues encountered:

1. Issue: _______________
   Steps to reproduce: _______________
   Expected: _______________
   Actual: _______________

2. Issue: _______________
   Steps to reproduce: _______________
   Expected: _______________
   Actual: _______________

## Sign-off

- [ ] All critical features tested and working
- [ ] All blocking issues resolved or documented
- [ ] Documentation is accurate
- [ ] Ready for user acceptance testing

Tested by: ________________
Date: ________________
Version: ________________

