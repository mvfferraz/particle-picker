# Deploy Web Version to GitHub Pages

**Author:** Matheus Ferraz

## What is This?

This is a **pure HTML/JavaScript version** of the Particle Picker Dashboard that runs entirely in the browser. No server needed!

## Features

✅ **100% Client-Side** - All processing happens in your browser  
✅ **No File Upload to Server** - Your data stays on your computer  
✅ **Free Hosting** - GitHub Pages is completely free  
✅ **Fast** - No server round-trips  
✅ **Shareable** - Send the URL to anyone  

## Deployment Steps

### Step 1: Commit the Web Version

```bash
cd particle-picker-dashboard

# Add the docs folder
git add docs/

# Commit
git commit -m "Add web version for GitHub Pages"

# Push
git push origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub:
   ```
   https://github.com/SEU_USUARIO/particle-picker-dashboard
   ```

2. Click **"Settings"** (top menu)

3. Click **"Pages"** (left sidebar)

4. Under **"Source"**, select:
   - **Branch:** `main`
   - **Folder:** `/docs`

5. Click **"Save"**

6. Wait 1-2 minutes

7. Your site will be live at:
   ```
   https://SEU_USUARIO.github.io/particle-picker-dashboard/
   ```

### Step 3: Test It!

1. Open the URL in your browser

2. Drag and drop a `.star`, `.csv`, or `.box` file

3. See your data visualized instantly!

## How It Works

### File Processing

1. **User selects file** → File stays on their computer
2. **JavaScript reads file** → Using FileReader API (browser-native)
3. **Parser processes data** → Extracts particle coordinates
4. **Statistics calculated** → All in browser memory
5. **Charts generated** → Using Plotly.js

### Security & Privacy

- ✅ Files **never leave your computer**
- ✅ No server upload
- ✅ No tracking or analytics
- ✅ Works offline (after first load)

## File Size Limits

- **Maximum:** 50MB (browser memory limit)
- **Recommended:** < 10MB for best performance

For larger files, use the Python version:
```bash
make run-dashboard
```

## Supported Formats

### .star Files (RELION)
Parses `data_particles` section automatically

### .csv Files
Requires columns: `CoordinateX`, `CoordinateY`, `MicrographName` (or similar)

### .box Files (EMAN2)
Format: `X Y Width Height` (one particle per line)

## Customization

### Change Colors

Edit `docs/index.html`, line ~25-30:
```css
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
```

### Add Your Logo

Edit `docs/index.html`, line ~260:
```html
<h1>🔬 Your Lab Name</h1>
```

### Modify Statistics

Edit `docs/parser.js` to add custom calculations

## Troubleshooting

### Page Not Loading

1. Check GitHub Pages settings
2. Make sure `docs/index.html` exists
3. Wait 2-3 minutes after enabling Pages
4. Clear browser cache

### File Not Parsing

1. Check browser console (F12)
2. Verify file format matches examples
3. Try a smaller test file first

### Charts Not Showing

1. Check internet connection (Plotly loads from CDN)
2. Disable browser extensions
3. Try different browser

## Updates

To update the web version:

```bash
# Make changes to files in docs/
git add docs/
git commit -m "Update web version"
git push

# Wait 1-2 minutes, changes go live automatically
```

## Comparison: Web vs Python Version

| Feature | Web (GitHub Pages) | Python (Dash) |
|---------|-------------------|---------------|
| **Hosting** | Free (GitHub) | Free (Render) or Local |
| **Setup** | None | pip install |
| **File Size** | < 50MB | Unlimited |
| **Speed** | Very Fast | Fast |
| **Privacy** | 100% Private | Upload to server |
| **Offline** | Yes (after 1st load) | No |
| **Sharing** | Just send URL | Need server |

## When to Use Which Version

**Use Web Version When:**
- Files < 50MB
- Quick analysis needed
- Want to share with colleagues
- Don't want to install anything
- Need privacy (files stay local)

**Use Python Version When:**
- Large files (> 50MB)
- Need advanced features
- Want to customize extensively
- Batch processing multiple files
- Integration with other tools

## Example URLs

After deployment, share these URLs:

**Your Dashboard:**
```
https://matheusferraz.github.io/particle-picker-dashboard/
```

**Direct Link to Upload:**
```
https://matheusferraz.github.io/particle-picker-dashboard/#upload
```

## Browser Compatibility

✅ Chrome/Edge (recommended)  
✅ Firefox  
✅ Safari  
⚠️ IE11 (not supported)  

## Analytics (Optional)

To add Google Analytics:

1. Get tracking ID from analytics.google.com
2. Add to `docs/index.html` before `</head>`:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR_ID');
</script>
```

## Custom Domain (Optional)

To use your own domain (e.g., `particles.yourlab.com`):

1. Add `CNAME` file in `docs/`:
   ```
   particles.yourlab.com
   ```

2. Configure DNS at your domain provider:
   ```
   Type: CNAME
   Name: particles
   Value: SEU_USUARIO.github.io
   ```

3. Enable HTTPS in GitHub Pages settings

## Support

Questions? Issues?
- Open GitHub Issue
- Check browser console for errors
- Test with example files first

## License

Same as main project: MIT License

---

**Enjoy your free, fast, private particle analysis dashboard! 🚀**
