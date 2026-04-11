# Sticky Navbar Template

## Overview
The navbar is already sticky across all pages. The CSS property `position: sticky; top: 0; z-index: 50;` is applied in `assets/css/styles.css` to the `.site-header` class.

## For All Future Pages

### Required Header HTML
Add this header code immediately after the opening `<body>` tag on ALL new pages:

```html
<header class="site-header" role="banner">
  <div class="container">
    <div class="branding">
      <a class="logo" href="index.html" aria-label="CUET Medical Center Home">CUET Medical Center</a>
    </div>
    <button id="menuToggle" class="menu-toggle" aria-label="Toggle navigation" aria-controls="topNav" aria-expanded="false">
      <span class="bar"></span>
      <span class="bar"></span>
      <span class="bar"></span>
    </button>
    <nav id="topNav" class="top-nav" aria-label="Primary">
      <a href="about.html" class="nav-link">About</a>
      <a href="doctors.html" class="nav-link">Doctors</a>
      <a href="pharmacy.html" class="nav-link">Pharmacy</a>
      <a href="emergency.html" class="nav-link">Emergency</a>
      <a href="contact.html" class="nav-link">Contact</a>
      <a href="login.html" class="btn btn-primary">Login</a>
    </nav>
  </div>
</header>
```

### Key Points
- **Placement**: Add the header immediately after `<body>` and before any main content
- **Sticky Behavior**: Enabled automatically via CSS - stays at top when scrolling
- **Mobile Responsive**: The menu toggle button (`#menuToggle`) handles mobile navigation
- **Link Paths**: For pages in subdirectories (like `student/`), adjust paths to parent:
  - From `student/` folder: Use `../index.html`, `../about.html`, etc.

### Path Adjustments by Location

**Pages in root folder:**
```html
<a href="index.html">...</a>
<a href="about.html">...</a>
```

**Pages in `student/` subfolder:**
```html
<a href="../index.html">...</a>
<a href="../about.html">...</a>
```

### Navbar Features
- **Sticky Position**: Remains visible at top while scrolling
- **Backdrop Blur**: Modern frosted glass effect
- **Z-Index**: Set to 50 to stay above other content
- **Responsive**: Menu toggle button for mobile devices
- **High Contrast**: Color scheme adapts to light/dark themes

### CSS Styling
The navbar styling is fully defined in `assets/css/styles.css`:
- `.site-header` - Main header styling with sticky positioning
- `.top-nav` - Navigation menu layout
- `.menu-toggle` - Mobile hamburger menu button
- `.logo` - Branding text with gradient effect
- `.nav-link` & `.btn-primary` - Navigation link styles

**No additional CSS needed** - the navbar receives all styling from the main stylesheet.

## Implementation Checklist for New Pages
- [ ] Add `<link rel="stylesheet" href="assets/css/styles.css">` in `<head>` (if using relative paths, adjust as needed)
- [ ] Add complete header code after `<body>` tag
- [ ] Verify navbar appears at top and stays visible when scrolling
- [ ] Test responsive menu toggle on mobile
- [ ] Verify links work correctly (especially path references)
- [ ] For pages in subfolders, use `../` paths for parent directory links

## Testing
1. Open page in browser
2. Scroll down - navbar should stay at top
3. On small screens, click hamburger menu to toggle navigation
4. Verify all links navigate correctly

## Updates Made
Updated all pages to include sticky navbar:
- ✅ All root-level public pages (index, about, doctors, pharmacy, services, etc.)
- ✅ Login page
- ✅ Doctor pages (doctor, medical-records, prescriptions, roster, profile)
- ✅ Admin page
- ✅ All student pages (student/, 11 pages total)
- ✅ Alerts, notices, and other utility pages

**Total Pages Updated: 26+**
