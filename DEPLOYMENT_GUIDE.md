# 🚀 Deployment Guide

## GitHub Pages Deployment

### Step 1: Push to GitHub

```bash
# If you haven't already, create a new repo on GitHub
# Then push your code:

git remote add origin https://github.com/yourusername/fuzzy-traffic-system.git
git branch -M main
git push -u origin main
```

### Step 2: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top right)
3. Click **Pages** (left sidebar)
4. Under "Build and deployment":
   - Source: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/ (root)**
5. Click **Save**

### Step 3: Update GitHub Actions Permissions (if needed)

1. Go to **Settings** → **Actions** → **General**
2. Under "Workflow permissions":
   - Select **Read and write permissions**
   - Check **Allow GitHub Actions to create and approve pull requests**
3. Click **Save**

### Step 4: Wait for Deployment

- GitHub Actions will automatically deploy your site
- Check the **Actions** tab to see deployment progress
- Usually takes 2-5 minutes
- Your site will be live at: `https://yourusername.github.io/fuzzy-traffic-system/`

### Step 5: Update README Links

Update the following in `README.md`:

```markdown
**[View Live Dashboard](https://yourusername.github.io/fuzzy-traffic-system/)**
```

And in `web/index.html`:

```html
<a href="https://github.com/yourusername/fuzzy-traffic-system" ...>
```

---

## Running Locally

### Generate Comparison Data

Before viewing the dashboard, generate comparison results:

```bash
poetry install
poetry shell
python src/main.py
```

This creates `web/data/comparison_results.json`.

### View Dashboard

**Option 1: Direct file**
```bash
open web/index.html
# or
firefox web/index.html
```

**Option 2: Local server**
```bash
cd web
python -m http.server 8000
# Open http://localhost:8000
```

---

## Verification Checklist

- [ ] All tests pass: `python test_system.py`
- [ ] Data generated: `python src/main.py`
- [ ] Web dashboard works locally
- [ ] Code pushed to GitHub
- [ ] GitHub Pages enabled
- [ ] Actions workflow succeeded
- [ ] Live site accessible
- [ ] Charts display correctly
- [ ] All links work

---

## Troubleshooting

### GitHub Actions Fails

**Error: Permission denied**
- Go to Settings → Actions → General
- Enable "Read and write permissions"

**Error: Deploy failed**
- Check Actions tab for error details
- Verify `/web` folder exists in main branch
- Ensure `deploy.yml` is in `.github/workflows/`

### Dashboard Shows Mock Data

This is normal if you haven't run the simulation yet.

**To show real data:**
```bash
python src/main.py
git add web/data/comparison_results.json
git commit -m "Add comparison results"
git push
```

### Charts Not Displaying

- Check browser console for errors
- Verify Chart.js CDN is loading
- Make sure JavaScript is enabled
- Try clearing browser cache

### 404 Page Not Found

- Verify GitHub Pages is enabled
- Check Settings → Pages shows green "Your site is published"
- Wait a few minutes after enabling
- Verify URL: `https://USERNAME.github.io/REPO-NAME/`

---

## Custom Domain (Optional)

To use a custom domain:

1. Add `CNAME` file to `/web` directory:
   ```
   yourdomain.com
   ```

2. Configure DNS:
   - Add CNAME record pointing to `yourusername.github.io`

3. Go to Settings → Pages
   - Enter custom domain
   - Check "Enforce HTTPS"

---

## Continuous Deployment

The project includes automatic deployment via GitHub Actions.

**Every time you push to `main`:**
1. GitHub Actions runs `.github/workflows/deploy.yml`
2. Builds the site from `/web` folder
3. Deploys to GitHub Pages
4. Site updates automatically (~2-5 min)

**To disable auto-deploy:**
- Delete `.github/workflows/deploy.yml`
- Or go to Actions → Disable workflow

---

## Production Checklist

Before sharing your site:

- [ ] Update all "yourusername" placeholders
- [ ] Add real comparison data
- [ ] Test all scenarios in dashboard
- [ ] Verify mobile responsiveness
- [ ] Check all external links
- [ ] Add Google Analytics (optional)
- [ ] Update project description
- [ ] Add screenshot to README

---

**Your site is now live! 🎉**

Share it: `https://yourusername.github.io/fuzzy-traffic-system/`
