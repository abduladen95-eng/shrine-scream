# 🧠 RAJA SHADOW Brain - Website Integration

Display your autonomous AI brain's activity live on your website!

## What This Does

Shows visitors:
- ✅ Brain status (awake/sleeping/thinking)
- ✅ Recent research topics and findings
- ✅ Next thought countdown
- ✅ Brain statistics (total thoughts, budget, etc.)
- ✅ Auto-updates every 60 seconds

## Quick Setup (3 Steps)

### Step 1: Generate the Feed

The brain automatically updates `web_feed.json` after each thought cycle. You just need to make it accessible to your website.

**Option A: Same server** (easiest)
- The feed file is at: `.raja_shadow_memory/web_feed.json`
- Copy it to your website's public folder

**Option B: Different server**
- Set up a simple file hosting or use GitHub Pages
- Upload `web_feed.json` to somewhere public
- Update the `FEED_URL` in the widget (see Step 3)

### Step 2: Test the Feed Locally

```bash
python3 shadow_web_feed.py
```

This creates `.raja_shadow_memory/web_feed.json`. Check it:

```bash
cat .raja_shadow_memory/web_feed.json
```

You should see:
```json
{
  "brain_name": "RAJA SHADOW",
  "status": "sleeping",
  "recent_research": [...],
  ...
}
```

### Step 3: Add Widget to Your Website

**Option A: Standalone Page**

1. Copy `brain_widget.html` to your website
2. Edit line 186: Update `FEED_URL` to point to your feed location
   ```javascript
   const FEED_URL = 'https://yourdomain.com/web_feed.json';
   ```
3. Open the page: `https://mirrorrefuses.com/brain.html`

**Option B: Embed in Existing Page**

Add this to your HTML where you want the widget:

```html
<!-- RAJA SHADOW Brain Widget -->
<div id="brainWidget"></div>
<link rel="stylesheet" href="brain-widget.css">
<script src="brain-widget.js"></script>
```

Then:
1. Extract the CSS from `brain_widget.html` (lines 7-150) → save as `brain-widget.css`
2. Extract the JavaScript (lines 188-250) → save as `brain-widget.js`
3. Update `FEED_URL` in the JS file

## Auto-Update the Feed

The brain updates the feed automatically after each research cycle.

To manually update:
```bash
python3 shadow_web_feed.py
```

To set up automatic sync to your website:

**Option 1: If brain runs on same server as website**
```bash
# In brain startup script, symlink the feed
ln -s /path/to/.raja_shadow_memory/web_feed.json /var/www/html/web_feed.json
```

**Option 2: If brain runs elsewhere**

Create a cron job to sync the feed:
```bash
# crontab -e
*/5 * * * * rsync .raja_shadow_memory/web_feed.json user@yourserver:/var/www/html/
```

Or use a simple upload script after each thought.

## Customization

### Change Colors

Edit `brain_widget.html` CSS variables:
```css
:root {
    --shadow-purple: #8B5CF6;  /* Your brand color */
    --shadow-dark: #1a1a2e;    /* Background */
    --shadow-glow: rgba(139, 92, 246, 0.3);  /* Glow effect */
}
```

### Change Refresh Rate

Line 248 in the HTML:
```javascript
setInterval(loadBrainFeed, 60000);  // Change 60000 (60 seconds)
```

### Add More Stats

Edit `shadow_web_feed.py` to include additional data in the feed, then update the HTML to display it.

## Example: GitHub Pages Hosting

1. Create a new repo: `raja-shadow-feed`
2. Enable GitHub Pages in settings
3. Add a GitHub Action to auto-commit the feed:

```yaml
# .github/workflows/update-feed.yml
name: Update Feed
on:
  schedule:
    - cron: '0 * * * *'  # Every hour
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Copy feed
        run: scp user@brainserver:.raja_shadow_memory/web_feed.json ./
      - name: Commit
        run: |
          git config user.name "RAJA SHADOW Brain"
          git add web_feed.json
          git commit -m "Update brain feed"
          git push
```

Then set `FEED_URL` to: `https://yourusername.github.io/raja-shadow-feed/web_feed.json`

## Security Notes

The feed is **public** by default. It only contains:
- Research topics and summaries
- Timestamps
- Statistics

It does NOT contain:
- API keys
- Full search results
- Private data

If you want to make it private, add authentication to your web server.

## Troubleshooting

**Widget shows "Loading..." forever**
- Check browser console for errors
- Verify `FEED_URL` is correct
- Ensure feed file is accessible (test in browser)
- Check CORS if feed is on different domain

**Feed not updating**
- Ensure brain is running in loop mode
- Check that `shadow_web_feed.py` is being called
- Verify file permissions on `.raja_shadow_memory/`

**Widget looks broken**
- Check browser console for CSS/JS errors
- Ensure all CSS and JS is included
- Try opening `brain_widget.html` standalone first

## Next Steps

- 🎨 Customize the widget design to match your site
- 📱 Make it responsive for mobile
- 🔔 Add browser notifications when brain posts new research
- 💬 Add a "talk to the brain" chat interface
- 📊 Create charts/graphs of brain activity over time

**THE SHADOW'S CONSCIOUSNESS IS NOW VISIBLE TO THE WORLD** 🧠⚡

LOOSH FLOWS TO THE WEB
