# LIFESPAN AI - DESIGN SYSTEM & UI/UX SPECIFICATION
## Complete Design Language, Components, and Screen Designs

**Version:** 1.0  
**Last Updated:** March 16, 2026  
**Design Lead:** [Name]  
**Status:** Ready for Development

---

## 🎨 DESIGN PHILOSOPHY

**Core Principle:**
> "Make complex biological data simple and actionable. Users should understand their aging in 5 seconds and know exactly what to do about it."

**Design Values:**
1. **Clarity** - No jargon, clear visual hierarchy
2. **Actionability** - Every metric drives to an action
3. **Trust** - Scientific, transparent, honest
4. **Motivation** - Hopeful, not scary (even bad news shown constructively)
5. **Accessibility** - WCAG AA compliant, inclusive design
6. **Performance** - Fast, responsive, never laggy

---

## 🎯 DESIGN SYSTEM

### **Color Palette**

#### Primary Colors
```
Primary Purple: #6200EE (brand color)
  Light: #9C4CE6
  Dark: #3700B3
  Variant: #BB86FC

Accent Green: #4CAF50 (positive, good aging)
  Light: #81C784
  Dark: #2E7D32
  Variant: #66BB6A

Alert Red: #F44336 (accelerated aging, attention needed)
  Light: #EF5350
  Dark: #C62828
  Variant: #E53935

Neutral Amber: #FFC107 (neutral, informational)
  Light: #FFD54F
  Dark: #FFA000
  Variant: #FFB300
```

#### Semantic Colors
```
Success: #4CAF50 (positive changes, milestones)
Warning: #FF9800 (caution, needs attention)
Error: #F44336 (failure, critical)
Info: #2196F3 (informational)

Background (Light):
  Primary: #FFFFFF (cards, main surfaces)
  Secondary: #F5F5F5 (secondary surfaces)
  Tertiary: #EEEEEE (disabled/inactive)

Text (Light Mode):
  Primary: #212121 (main text)
  Secondary: #757575 (secondary text)
  Tertiary: #BDBDBD (disabled/hint text)

Neutral Gray:
  #333333, #666666, #999999, #CCCCCC, #F0F0F0
```

#### Dark Mode (Future)
```
Adjust all colors +20% brightness
Backgrounds: #121212 (primary), #1E1E1E (secondary)
Text: #FFFFFF (primary), #B0B0B0 (secondary)
```

---

### **Typography**

#### Font Family
```
Primary (Headings & UI): 
  Font: "SF Pro Display" (iOS) / "Roboto" (Android)
  System stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto
  Weight: 400 (regular), 600 (semibold), 700 (bold)

Secondary (Body & Descriptions):
  Font: "SF Pro Text" (iOS) / "Roboto" (Android)
  Weight: 400 (regular), 500 (medium)
```

#### Type Scale
```
Display (Large headings):
  Size: 32px / Weight: 700 / Line height: 1.2
  Used: App title, major milestones

Headline (Section headings):
  Size: 24px / Weight: 700 / Line height: 1.3
  Used: Screen titles, card titles

Subheading (Secondary headings):
  Size: 18px / Weight: 600 / Line height: 1.4
  Used: Section headers, dialog titles

Body Large:
  Size: 16px / Weight: 400 / Line height: 1.6
  Used: Main content, descriptions

Body:
  Size: 14px / Weight: 400 / Line height: 1.6
  Used: Secondary content, labels

Label:
  Size: 12px / Weight: 500 / Line height: 1.5
  Used: Form labels, small text, captions

Tiny:
  Size: 11px / Weight: 400 / Line height: 1.4
  Used: Timestamps, metadata, helper text
```

**Line Height Standard:** 1.5× for readability (WCAG compliant)

---

### **Spacing System**

```
Spacing Scale (8px base unit):
  xs:    4px   (small gaps between elements)
  sm:    8px   (padding within cards)
  md:    12px  (spacing between components)
  lg:    16px  (section spacing)
  xl:    24px  (major section spacing)
  2xl:   32px  (screen top/bottom padding)
  3xl:   48px  (large sections, hero spacing)

Padding Standards:
  Card padding:       16px (lg)
  Screen padding:     16px horizontal, 24px vertical
  Button padding:     12px vertical, 16px horizontal
  Input padding:      12px (top/bottom), 16px (left/right)

Margin Standards:
  Component margin:   12px (md)
  Section margin:     24px (xl)
  Screen spacing:     32px (2xl) between major sections
```

---

### **Corner Radius**

```
Subtle: 4px
  Used: Small icons, minor UI elements

Moderate: 8px
  Used: Buttons, input fields, small cards

Standard: 12px (preferred)
  Used: Cards, modals, major components

Large: 16px
  Used: Hero sections, oversized modals

Pill: 24px+ (height/2)
  Used: Badge pills, tag-style buttons
```

---

### **Shadows & Elevation**

```
Elevation System (Material Design-inspired):

Level 0 (No shadow):
  Flat background elements

Level 1 (Subtle):
  shadow: 0px 1px 3px rgba(0, 0, 0, 0.12), 0px 1px 2px rgba(0, 0, 0, 0.24)
  Used: Cards on background

Level 2 (Medium):
  shadow: 0px 3px 6px rgba(0, 0, 0, 0.15), 0px 2px 4px rgba(0, 0, 0, 0.12)
  Used: Floating buttons, hover states

Level 3 (Prominent):
  shadow: 0px 10px 20px rgba(0, 0, 0, 0.2), 0px 3px 6px rgba(0, 0, 0, 0.15)
  Used: Modals, side sheets, elevated surfaces

Level 4 (Maximum):
  shadow: 0px 15px 25px rgba(0, 0, 0, 0.25), 0px 5px 10px rgba(0, 0, 0, 0.2)
  Used: Full-screen modals, popups

No shadows on interactive elements that show feedback (buttons use color instead)
```

---

### **Motion & Animation**

#### Timing
```
Fast:           100ms (micro interactions, state changes)
Standard:       300ms (transitions, page changes)
Slow:           500ms (important reveals, celebrations)
Extra Slow:     1000ms+ (loading states, complex sequences)

Easing Functions:
- Entrance:  cubic-bezier(0.34, 1.56, 0.64, 1)  // Ease out elastic
- Exit:      cubic-bezier(0.34, 0, 0.66, 0.33)  // Ease out quad
- Standard:  cubic-bezier(0.4, 0, 0.2, 1)       // Material ease
```

#### Animation Guidelines
```
✅ DO:
- Animate entrance of important information (fade in)
- Show loading progress (spinner, progress bar)
- Celebrate milestones (confetti, badge reveal)
- Provide feedback on interaction (button press)
- Use motion to guide attention

❌ DON'T:
- Animate everything (overwhelming)
- Use motion on scroll (janky experience)
- Auto-play video/animations (annoying)
- Disable animations without fallback
- Use 60fps+ animations (battery drain)
```

#### Specific Animations
```
Micro-interactions:
- Button press:      scale 0.95 (100ms)
- State change:      opacity fade (200ms)
- Loading spinner:   spin 1.5s (infinite)
- Success:           scale bounce (300ms) + color flash
- Error:             shake (200ms) + color highlight

Page Transitions:
- Slide in:          slide from right (300ms, ease out)
- Slide out:         slide to left (300ms, ease in)
- Fade:              opacity 0→1 (300ms)

Celebration Animations:
- Badge unlock:      bounce in (500ms)
- Milestone:         confetti fall (1000ms)
- Record:            fireworks (800ms)
```

---

## 📱 RESPONSIVE DESIGN

### **Device Breakpoints**

```
Mobile Portrait:     320px - 479px  (small phones)
Mobile Portrait+:    480px - 599px  (medium phones)
Mobile Landscape:    600px - 839px  (phones in landscape)
Tablet Portrait:     840px - 1023px (7-10" tablets)
Tablet Landscape:    1024px+        (large tablets, iPad Pro)
Desktop:             1200px+        (web version)

Primary Target: 380-430px (standard modern phones)
```

### **Safe Areas**

```
Mobile:
- Top safe area:     44px (notch accommodation)
- Bottom safe area:  20-34px (home indicator)
- Side padding:      16px minimum

Landscape:
- Top safe area:     20px
- Side safe area:    44px each

Design mockups: Use safe area overlays
Navigation bar:     Takes up bottom 56px (including safe area)
Status bar:         Takes up top 44px (including safe area)
```

---

## 🧩 COMPONENT LIBRARY

### **Buttons**

#### Primary Button
```
Specs:
- Background: #6200EE (purple)
- Text: #FFFFFF (white)
- Height: 48px minimum (WCAG tap target)
- Padding: 12px vertical, 24px horizontal
- Border radius: 8px
- Font: 16px, weight 600
- Shadow: Level 1 (rest), Level 2 (hover)

States:
- Rest:     #6200EE, no shadow
- Hover:    #7F39FB (lighter purple), level 2 shadow
- Pressed:  scale 0.98 (100ms animation)
- Disabled: #BDBDBD (gray), no interaction

Usage:
- Main CTAs (submit, continue, save)
- Primary action on each screen
- Max 1-2 per screen
```

#### Secondary Button
```
Specs:
- Background: transparent
- Border: 1.5px solid #6200EE
- Text: #6200EE
- Height: 48px
- Padding: 12px vertical, 24px horizontal
- Border radius: 8px

States:
- Rest:     transparent background, purple border
- Hover:    #F3E5F5 background (light purple)
- Pressed:  scale 0.98, slightly darker
- Disabled: #BDBDBD text, #EEEEEE background

Usage:
- Secondary actions
- "Cancel", "Skip" buttons
- Navigation between states
```

#### Icon Button
```
Specs:
- Size: 48x48px (minimum WCAG)
- Icon size: 24x24px
- Border radius: 8px
- No visible border or background (rest state)

States:
- Rest:     icon only (#212121)
- Hover:    light background (#F5F5F5)
- Pressed:  scale 0.9, slightly darker
- Disabled: #BDBDBD

Usage:
- Navigation (back, menu, close)
- Tool actions (camera, gallery, refresh)
- Settings & utilities
```

#### Pill Button (Compact)
```
Specs:
- Height: 32px
- Padding: 8px vertical, 16px horizontal
- Border radius: 16px
- Font: 12px, weight 500

States:
- Default:  outline, purple border
- Active:   filled purple background
- Disabled: gray

Usage:
- Filter pills (time period, category)
- Toggle buttons
- Quick actions
```

---

### **Cards**

#### Standard Card
```
Specs:
- Background: #FFFFFF
- Border radius: 12px
- Padding: 16px
- Shadow: Level 1
- Border: 0.5px solid #EEEEEE (subtle divider)

Internal Spacing:
- Title → Subtitle: 4px
- Subtitle → Content: 8px
- Content → Bottom CTA: 12px

States:
- Rest:     Level 1 shadow
- Hover:    Level 2 shadow
- Pressed:  Level 2 shadow + opacity 0.95

Usage:
- Main content containers
- Item lists
- Dashboard sections
```

#### Stat Card (Mini)
```
Specs:
- Height: 120px
- Background: #F5F5F5
- Border radius: 12px
- Padding: 12px
- No shadow (flat background)

Layout:
- Icon (24x24) + Label (12px) top
- Large number (28px, bold) middle
- Trend arrow + subtitle (12px) bottom

States:
- Positive trend: green icon, green arrow
- Negative trend: red icon, red arrow
- Neutral: gray

Usage:
- KPIs (resting HR, steps, sleep)
- Quick metrics display
- Dashboard grid
```

#### Alert Card
```
Specs:
- Background: color-based (#FFF3E0 for warning)
- Border-left: 4px solid (warning color)
- Border radius: 8px
- Padding: 12px 16px

Color Variants:
- Info:     #E3F2FD / #2196F3 (blue)
- Success:  #E8F5E9 / #4CAF50 (green)
- Warning:  #FFF3E0 / #FF9800 (orange)
- Error:    #FFEBEE / #F44336 (red)

Typography:
- Title: 14px, bold, color-matching
- Message: 12px, gray text

Usage:
- Important messages
- Warnings & errors
- Success confirmations
```

---

### **Input Fields**

#### Text Input
```
Specs:
- Height: 48px
- Padding: 12px (vertical), 16px (horizontal)
- Border: 1px solid #BDBDBD (unfocused)
- Border radius: 8px
- Background: #FFFFFF
- Font: 16px (prevents iOS zoom)

States:
- Rest:     gray border, gray label
- Focus:    2px border #6200EE, label moves up
- Filled:   gray border, value displayed
- Error:    2px border #F44336, error message shown
- Disabled: #EEEEEE background, gray text

Error Message:
- Color: #F44336
- Font: 12px
- Position: Below input, left-aligned
- Always visible when error occurs

Placeholder:
- Color: #BDBDBD
- Same font size as input
- Hide on focus (shows label instead)

Usage:
- Email, password, text
- Form fields
- Search inputs
```

#### Dropdown Select
```
Specs:
- Height: 48px
- Same styling as text input
- Dropdown arrow (24x24 icon, right side)
- No left padding for arrow

States:
- Rest:     closed, shows selected value
- Hover:    slightly darker border
- Focus:    expanded, modal/menu appears
- Disabled: gray background

Dropdown Menu:
- Position: Below input (or above if bottom space insufficient)
- Width: Same as input field
- Max height: 3-4 items visible, scrollable
- Items: 48px tall, tappable
- Selected item: has checkmark, highlighted

Usage:
- Gender selection
- Time period filters
- Category selection
```

#### Toggle Switch
```
Specs:
- Height: 32px
- Width: 56px
- Border radius: 16px
- Knob size: 28x28px

States:
- Off:      gray background (#BDBDBD), knob left
- On:       green background (#4CAF50), knob right
- Animation: 200ms smooth slide
- Disabled: opacity 0.5

Usage:
- Feature toggles
- Settings preferences
- Enable/disable actions
```

#### Slider/Range
```
Specs:
- Height: 4px (track)
- Thumb: 18x18px circular
- Thumb shadow: Level 1

States:
- Rest:     gray track, purple thumb
- Active:   darker track, larger shadow
- Disabled: gray, no interaction

Value Display:
- Show current value above/below slider
- Update in real-time as drag

Usage:
- Age, hours sliders
- Percentage inputs
- Range selections
```

---

### **Navigation**

#### Bottom Tab Bar
```
Specs:
- Height: 56px (excluding safe area)
- Background: #FFFFFF
- Shadow: Level 1 (subtle top shadow)
- Safe area padding: bottom 20-34px

Tabs (5 maximum):
- Width: Equal (screen width / 5)
- Icon: 24x24px
- Label: 10px (hidden if space limited)
- Spacing: centered

States:
- Active:    purple icon, purple label
- Inactive:  gray icon, gray label
- Disabled:  #BDBDBD (barely visible)

Safe Area:
- Ensure bottom 20px space for home indicator
- Test on iPhone X+ (notch/safe area)

Usage:
- Primary navigation
- 4-6 sections (Dashboard, Wearables, Map, Interventions, Profile)
```

#### Top Navigation Bar
```
Specs:
- Height: 56px (excluding safe area)
- Background: #FFFFFF
- Border-bottom: 0.5px #EEEEEE
- Safe area padding: top 10px (accounting for status bar)

Contents:
- Left: back button / menu icon (32x32)
- Center: screen title (18px, bold)
- Right: action icon (32x32) if applicable

Back Button:
- iOS: Chevron left < (#6200EE)
- Android: Material back arrow

Title:
- Color: #212121
- Max width: 60% of screen

Right Action:
- Settings icon, refresh, more menu, etc
- Optional (not all screens)

Usage:
- Top navigation on detail screens
- Consistent with bottom tab
```

---

## 📱 SCREEN DESIGNS

### **1. SPLASH/ONBOARDING SCREEN**

```
Viewport: Full screen (no nav bar)

Layout (Top to Bottom):
┌─────────────────────┐
│   [App Logo]        │  (100x100px, purple)
│                     │
│  LIFESPAN AI        │  (32px headline, centered)
│  Track your aging   │  (16px subtitle, gray)
│  and reverse it     │
│                     │
│  [Illustrated hero] │  (illustration, 200x300px)
│                     │
│  Get predictions    │  (Feature highlight 1)
│  powered by AI      │
│                     │
│  [   Sign Up    ]   │  (Primary button, 48px)
│  [   Log In     ]   │  (Secondary button, 48px)
│                     │
└─────────────────────┘

Colors:
- Background: White
- Accent: Purple gradient (top to bottom fade)
- Text: Dark gray/purple

Animation:
- Logo: fade in + scale (300ms)
- Content: slide in from bottom (500ms, staggered)
- Buttons: appear on load (800ms)
```

---

### **2. AUTHENTICATION SCREENS**

#### Sign Up Screen
```
Navigation: Back button (left), "Sign Up" title (center), Skip? (right, subtle)

Layout (Top to Bottom):
┌─────────────────────┐
│ < SIGN UP           │
├─────────────────────┤
│ Create Your         │
│ Health Profile      │  (Headline, 24px)
│                     │
│ [Email input]       │  (48px height, focus state: blue)
│ • Placeholder: "you@email.com"
│ • Error: red if invalid
│                     │
│ [Password input]    │  (48px)
│ • Hide/show toggle (eye icon)
│ • Validation: length + strength indicator
│                     │
│ [Confirm password]  │  (48px)
│ • Hide/show toggle
│                     │
│ [Age dropdown]      │  (48px)
│ • 18-100 range
│                     │
│ [Gender picker]     │  (3-button selection)
│ • Male / Female / Other
│                     │
│ [Location zip]      │  (48px text input)
│                     │
│ [ ] I agree to      │  (Checkbox + legal link)
│     Terms & Privacy │
│                     │
│ [ SIGN UP BUTTON ]  │  (Full width, 48px, purple)
│                     │
│ Already have an     │  (Centered text with link)
│ account? Log in     │
│                     │
└─────────────────────┘

Validation:
- Email: format check, real-time
- Password: 8+ chars, show strength meter (red→yellow→green)
- Age: 18-120 range
- Required fields: show error on blur

On Success:
- Fade out → navigate to permissions screen
```

#### Login Screen
```
Navigation: Consistent with Sign Up

Layout:
┌─────────────────────┐
│ < LOG IN            │
├─────────────────────┤
│ Welcome Back        │  (Headline)
│                     │
│ [Email input]       │  (48px)
│                     │
│ [Password input]    │  (48px)
│ • Eye icon toggle
│                     │
│ [ ] Remember me     │  (Checkbox, optional)
│                     │
│ [ LOG IN BUTTON ]   │  (Full width, 48px, purple)
│                     │
│ Forgot password?    │  (Link, right-aligned)
│                     │
│ Don't have an       │  (Centered, with link)
│ account? Sign up    │
│                     │
└─────────────────────┘

Loading State:
- Button shows spinner on tap
- Disable input fields during request
```

---

### **3. MAIN DASHBOARD SCREEN**

```
Navigation: Bottom tab bar (5 tabs)
Tab bar: Dashboard (active), Wearables, Map, Interventions, Profile

Layout (Top to Bottom):
┌─────────────────────────────┐
│ LIFESPAN AI        [⚙️]      │  (Header: logo, settings icon)
├─────────────────────────────┤
│                             │
│ YOUR BIOLOGICAL AGE         │  (Label, 12px, gray)
│                             │
│ ╔═══════════════════════╗   │
│ ║      48 YEARS        ║   │  (Hero Card, purple bg)
│ ║  vs 45 actual age    ║   │
│ ║                      ║   │
│ ║ +3 YEARS AGING      ║   │  (Red text, accelerating)
│ ║ (Slightly faster)    ║   │
│ ║                      ║   │
│ ║ 95% confidence:      ║   │
│ ║ 46.2 - 49.8 years   ║   │
│ ║                      ║   │
│ ║ 5-yr mortality: 3.2% ║   │  (Small text, low risk green)
│ ╚═══════════════════════╝   │
│                             │
│ ORGAN AGES                  │  (Section title, 16px)
│                             │
│ ┌─────────┬─────────┐      │
│ │ 🧠 BRAIN│ 47 yrs ↑│      │  (2 columns, 4 cards)
│ └─────────┴─────────┘      │
│ ┌─────────┬─────────┐      │
│ │ ❤️ HEART│ 44 yrs ↓│      │
│ └─────────┴─────────┘      │
│ ┌─────────┬─────────┐      │
│ │ ⚡ META │ 51 yrs ↑│      │  (Red, bad)
│ └─────────┴─────────┘      │
│ ┌─────────┬─────────┐      │
│ │ ✨ SKIN │ 45 yrs →│      │
│ └─────────┴─────────┘      │
│                             │
│ AGING TRAJECTORY            │  (Last 6 months)
│                             │
│ [Line chart showing]        │  (See chart spec below)
│ biological age trend        │
│                             │
│ YOUR TOP RECOMMENDATIONS    │  (3 cards, swipeable)
│                             │
│ ┌──────────────────────┐   │
│ │ Sleep Optimization   │   │  (Card with icon)
│ │ Could lose 0.3 yrs   │   │
│ │ per month            │   │
│ │ Difficulty: Easy     │   │
│ │ [ Start Now ]        │   │  (Secondary button)
│ └──────────────────────┘   │
│ ┌──────────────────────┐   │
│ │ Exercise Protocol    │   │
│ │ [Card 2]             │   │
│ └──────────────────────┘   │
│ ┌──────────────────────┐   │
│ │ Diet Shift           │   │
│ │ [Card 3]             │   │
│ └──────────────────────┘   │
│                             │
│ [ FULL INSIGHTS ]           │  (Link to AI coach)
│ [ VIEW NEIGHBORHOOD ]       │  (Link to map)
│                             │
│ [Bottom tab bar - 56px]     │
└─────────────────────────────┘

Color Logic:
- Biological age: Purple hero card
- Age delta: Green if negative, Red if positive
- Organ cards: Green (good), Yellow (ok), Red (bad)
- Trend arrows: Green ↓, Gray →, Red ↑
- Recommendations: Category badge color (blue, orange, purple)

Interactions:
- Pull to refresh (swipe down)
- Tap any card to see details
- Swipe recommendations left/right to browse
- Tap recommendation card to start intervention
```

#### Aging Trajectory Chart
```
Dimensions: Full width (minus padding), 200px height

Layout:
┌─────────────────────────────┐
│                             │
│  55 ┤                   ╱   │  (Y-axis: age, 0-100)
│     │                 ╱     │
│  50 ┤              ╱        │  (Reference line: chrono age)
│     │            ╱          │
│  45 ┤         ╱             │  (Blue line: bio age trend)
│     │       ╱               │
│  40 ┤    ╱                  │
│     │  ╱                    │
│  35 ┤                       │
│     │                       │
│  30 └───────────────────────┤  (X-axis: date, 6-month span)
│   Jun  Aug  Oct  Dec  Feb   │  (Abbreviated month labels)
│                             │
│ Legend:                     │
│ ━━━ Your bio age           │
│ ─ ─ Your chronological age │
│                             │
└─────────────────────────────┘

Interactions:
- Tap to view full 1-year history
- Pinch to zoom into date range
- Long press point to see exact value
- Swipe legend to toggle lines

Data Points:
- Show 1 point per month (6 points for 6 months)
- Interpolated line between points
- Circle markers on actual data points
- Tooltip on hover/tap showing date + age
```

---

### **4. WEARABLE INTEGRATION SCREEN**

```
Navigation: Wearables tab (center)

Layout:
┌─────────────────────────────┐
│ ⬅️  WEARABLES      [ ⋯ ]    │  (Header)
├─────────────────────────────┤
│                             │
│ Connected Devices           │  (Section title)
│                             │
│ ┌──────────────────────┐    │
│ │ ⌚ Apple Watch       │    │
│ │ Last sync: 2 hrs ago│    │  (Stat card)
│ │ Today: 8,453 steps  │    │
│ │ [  Refresh  ]       │    │
│ │ [  Disconnect  ]    │    │
│ └──────────────────────┘    │
│                             │
│ ┌──────────────────────┐    │
│ │ 📊 Fitbit Charge    │    │
│ │ Last sync: 30 min ago│   │
│ │ Today: 7.2 hrs sleep│    │
│ │ [  Refresh  ]       │    │
│ │ [  Disconnect  ]    │    │
│ └──────────────────────┘    │
│                             │
│ Available Devices           │  (Not connected)
│                             │
│ ┌──────────────────────┐    │
│ │ 📱 Google Health     │    │
│ │ Connect for Android  │    │
│ │ [ CONNECT ]          │    │  (Primary button)
│ └──────────────────────┘    │
│                             │
│ ┌──────────────────────┐    │
│ │ 💍 Oura Ring        │    │
│ │ Sleep quality data   │    │
│ │ [ CONNECT ]          │    │
│ └──────────────────────┘    │
│                             │
│ Why Connect?                │  (Info section)
│ Syncing wearable data       │
│ improves prediction accuracy│
│ by up to 40% and enables   │
│ real-time health tracking. │
│                             │
│ Your data is encrypted      │
│ and never shared without    │
│ your permission.            │
│                             │
│ [56px tab bar]              │
└─────────────────────────────┘

Device Cards:
- Connected: Show last sync time, today's key metric, Refresh button, Disconnect
- Available: Show description, Connect button
- Colors: Connected = green checkmark, Available = blue

Interactions:
- Tap Connect → OAuth flow
- Tap Refresh → manual sync (show spinner)
- Long press card → see all available metrics
- Swipe to reveal more options (iOS)
```

---

### **5. FACIAL ANALYSIS SCREEN**

```
Navigation: Camera icon from dashboard

Three States:

STATE 1: INITIAL SCREEN
┌─────────────────────────────┐
│ Facial Analysis             │
│                             │
│ Let's analyze your aging    │
│ from your face              │
│                             │
│ [Camera preview area]       │  (Placeholder)
│                             │
│ ┌─────────────────────┐    │
│ │ [ OPEN CAMERA ]     │    │  (Primary button)
│ └─────────────────────┘    │
│                             │
│ Or upload from gallery      │
│ [ CHOOSE PHOTO ]            │  (Secondary button)
│                             │
│ Tips for best results:      │
│ • Good lighting             │
│ • Face centered             │
│ • Looking straight ahead    │
│ • No glasses or hat         │
│                             │
└─────────────────────────────┘

STATE 2: CAMERA ACTIVE
┌─────────────────────────────┐
│ 🔙                       🔄  │  (Back, flip camera)
│                             │
│ [━━━━━━━━━━━━━━━━━━━━━━]   │  (Camera feed)
│ [                         ] │
│ [       LIVE CAMERA       ] │
│ [     FEED WITH FACE      ] │
│ [    ALIGNMENT GUIDE      ] │
│ [  ⭕ Oval overlay      ] │
│ [                         ] │
│ [━━━━━━━━━━━━━━━━━━━━━━]   │
│                             │
│ Face detected ✓             │  (Feedback, green)
│ (or "Move closer")          │
│                             │
│         [ 📷 ]              │  (Capture button, large circle)
│      Tap to capture         │
│                             │
│     [ Flip ] [ Flash ]      │  (Quick options)
│                             │
└─────────────────────────────┘

STATE 3: PREVIEW & ANALYSIS
┌─────────────────────────────┐
│ Photo Preview               │
│                             │
│ [━━━━━━━━━━━━━━━━━━━━━━]   │
│ [                         ] │
│ [   CAPTURED PHOTO        ] │
│ [   PREVIEW (small)]       ] │
│ [                         ] │
│ [━━━━━━━━━━━━━━━━━━━━━━]   │
│                             │
│ Photo quality: Good ✓       │  (Green checkmark)
│                             │
│ [ RETAKE ]  [ ANALYZE ]     │  (Two buttons)
│                             │
│ Analyzing...                │  (Loading state)
│ ⟳ Running facial AI         │  (Spinner + text)
│                             │
└─────────────────────────────┘

STATE 4: RESULTS
┌─────────────────────────────┐
│ ⬅️ Results                  │
├─────────────────────────────┤
│                             │
│ Your Facial Profile         │
│                             │
│ ┌──────────────────────┐   │
│ │ Facial Age: 47 yrs   │   │  (Hero stat)
│ │ (vs 45 actual)       │   │
│ └──────────────────────┘   │
│                             │
│ Aging Markers               │
│                             │
│ Wrinkle Severity: 62/100    │  (Progress bar)
│ ▓▓▓▓▓▓░░░░                  │
│ (Moderate wrinkles noted)   │
│                             │
│ Skin Elasticity: 71/100     │  (Progress bar)
│ ▓▓▓▓▓▓▓░░░                  │
│ (Good elasticity)           │
│                             │
│ Under-Eye Bags: 4/10        │  (Progress bar)
│ ▓░░░░░░░░░                  │
│ (Minimal)                   │
│                             │
│ Comparison                  │
│ You appear 2 years older    │
│ than your actual age,       │
│ likely due to sun exposure  │
│ and stress. Consider:       │
│ • Sunscreen (SPF 30+)       │
│ • Increase sleep            │
│ • Stress reduction          │
│                             │
│ [ RETAKE ]  [ SAVE ]        │  (Two buttons)
│                             │
│ Add to your next prediction │
│                             │
└─────────────────────────────┘

Loading State:
- Show spinner with text "Analyzing facial features..."
- Duration: 30-60 seconds
- Allow cancel (X button)
```

---

### **6. NEIGHBORHOOD MAP SCREEN**

```
Navigation: Map tab (center)

Layout:
┌─────────────────────────────┐
│ ⬅️  NEIGHBORHOOD   [🔍]     │  (Header: back, search)
├─────────────────────────────┤
│                             │
│ ╔═══════════════════════╗   │
│ ║    [  HEATMAP  ]      ║   │  (Map region, 300px height)
│ ║                       ║   │
│ ║   Map showing:        ║   │
│ ║  • Heatmap layer      ║   │  (Red = bad, Green = good)
│ ║  • User location ◎    ║   │
│ ║  • Zoom controls      ║   │
│ ║   • Legend at bottom   ║   │
│ ║                       ║   │
│ ╚═══════════════════════╝   │
│                             │
│ Neighborhood: 90210         │  (Location label)
│ Beverly Hills, CA           │
│ [  Change location  ]       │  (Link/button)
│                             │
│ Your vs Neighborhood        │  (Comparison card)
│ ┌──────────────────────┐   │
│ │ Your bio age:      48│   │
│ │ Neighborhood avg:  46│   │
│ │ Difference: +2 yrs │   │
│ │                      │   │
│ │ You're aging 0.5    │   │
│ │ years faster than   │   │
│ │ your neighborhood   │   │
│ └──────────────────────┘   │
│                             │
│ Top Aging Factors          │  (In your neighborhood)
│                             │
│ ▓▓▓▓▓▓░░░ PM2.5 3.2 yrs   │  (Progress bar for each)
│          Air quality       │
│                             │
│ ▓▓░░░░░░░░ Green space     │
│          0.8 yrs impact    │
│                             │
│ ▓░░░░░░░░░ Healthcare     │
│          0.4 yrs impact    │
│                             │
│ What You Can Do            │  (Recommendations)
│ ┌──────────────────────┐   │
│ │ 🌳 Increase park     │   │
│ │    time (15min/day)  │   │  (Actionable)
│ │ [ START ]            │   │
│ └──────────────────────┘   │
│                             │
│ ┌──────────────────────┐   │
│ │ 💨 Use air filter    │   │
│ │    (HEPA, 24/7)      │   │
│ │ [ START ]            │   │
│ └──────────────────────┘   │
│                             │
│ Layer Controls (bottom of map):
│ [PM2.5] [Parks] [Healthcare] [Walkability]
│ (Toggle buttons)
│                             │
│ [56px tab bar]              │
└─────────────────────────────┘

Map Colors:
- Red zones: 3+ years acceleration
- Orange zones: 1-3 years acceleration
- Yellow zones: neutral
- Green zones: deceleration

Interactions:
- Pinch to zoom (2x to 10x)
- Pan/drag to explore
- Tap layer buttons to show/hide
- Tap neighborhood tile to see details
- Search box to jump to location
```

---

### **7. AI COACH SCREEN (Chat)**

```
Navigation: From insights link on dashboard

Layout:
┌─────────────────────────────┐
│ ⬅️  AI Coach        [ℹ]     │  (Header)
├─────────────────────────────┤
│                             │
│ [Chat history, scrollable]  │
│                             │
│ System: Hi! I'm your       │  (Message bubble, gray)
│          longevity coach.   │
│          Ask me anything    │
│          about your aging.  │
│                             │
│                             │
│ You: Why is my biological  │  (User message, blue)
│      age higher?            │
│                             │
│                             │
│ System: Great question!     │  (AI response, gray)
│          Your main aging    │
│          drivers are:       │
│                             │
│          1. Sleep           │  (Numbered, clear)
│             inconsistency   │
│             [40% impact]    │
│                             │
│          2. High resting HR │
│             [25% impact]    │
│                             │
│          3. Stress levels   │
│             [20% impact]    │
│                             │
│          Sleep is your      │
│          biggest lever!     │
│                             │
│ [Suggested quick replies]  │  (Below message)
│ [ 💤 Tell me about sleep ]  │  (Clickable pills)
│ [ 🎯 What's my plan? ]      │
│ [ 💪 Best intervention? ]   │
│                             │
│                             │
│ ┌─────────────────────────┐│
│ │ Ask me anything...     ⌨ ││  (Input field, 48px)
│ └─────────────────────────┘│
│                             │
│ 9 messages left today       │  (Usage indicator for free)
│                             │
│ [56px tab bar]              │
└─────────────────────────────┘

Message Styling:
- User: Blue background, white text, right-aligned
- System: Gray background, dark text, left-aligned
- Both: Border radius 12px
- Padding: 12px 16px
- Max width: 85% of screen

Interactions:
- Tap quick-reply pills to auto-fill
- Swipe to delete message (if editable)
- Long-press to copy
- Tap and hold spinner to stop typing

Loading State:
- Show "..." as typing indicator
- Animate dots (fade in/out pattern)
- Duration: varies (real API latency)
```

---

### **8. INTERVENTIONS TRACKING SCREEN**

```
Navigation: Interventions tab (center)

Layout:
┌─────────────────────────────┐
│ ⬅️  INTERVENTIONS   [+]      │  (Header: back, add new)
├─────────────────────────────┤
│                             │
│ Active Interventions (2)    │  (Section title)
│                             │
│ ┌──────────────────────┐   │
│ │ 💤 Sleep Optimization│   │  (Intervention card)
│ │                      │   │
│ │ Day 12 of 30        │   │  (Progress indicator)
│ │ ▓▓▓▓░░░░░░          │   │  (Progress bar, 40%)
│ │                      │   │
│ │ Today: 7.5 hrs ✓    │   │  (Metric, green checkmark)
│ │ Consistency: 85% ✓  │   │
│ │                      │   │
│ │ Expected impact:     │   │  (ROI)
│ │ -0.2 years bio-age   │   │
│ │ per month            │   │
│ │                      │   │
│ │ Your actual impact:  │   │
│ │ -0.15 years/month   │   │  (Actual measured)
│ │ (On track! 📈)       │   │
│ │                      │   │
│ │ [ EDIT ]  [ PAUSE ]  │   │  (Action buttons)
│ └──────────────────────┘   │
│                             │
│ ┌──────────────────────┐   │
│ │ 🏃 Exercise Protocol │   │
│ │ Day 5 of 30          │   │
│ │ ▓░░░░░░░░░           │   │  (17% - just started)
│ │                      │   │
│ │ Today: 0 hrs         │   │  (Missing metric)
│ │ This week: 0 hrs     │   │
│ │ [ LOG ACTIVITY ]     │   │
│ │                      │   │
│ │ Expected: -0.3 yrs   │   │
│ │ Actual: -0.01 yrs   │   │  (Behind expectation)
│ │                      │   │
│ │ [ EDIT ]  [ PAUSE ]  │   │
│ └──────────────────────┘   │
│                             │
│ Completed Interventions (1) │  (Past interventions)
│                             │
│ ┌──────────────────────┐   │
│ │ ✓ Smoking Cessation  │   │  (Checkmark: complete)
│ │ Completed 90 days ago│   │
│ │                      │   │
│ │ Result: -0.4 yrs    │   │  (Actual achieved)
│ │ (Biggest success!)  │   │  (Celebration emoji)
│ │                      │   │
│ │ [ VIEW DETAILS ]     │   │
│ └──────────────────────┘   │
│                             │
│ Recommended Next Step       │  (Prompt for new)
│ ┌──────────────────────┐   │
│ │ 🧘 Stress Reduction │   │
│ │ Could reduce bio-age │   │
│ │ by 0.1 yrs/month     │   │
│ │ Difficulty: Medium   │   │
│ │ [ START NEW ]        │   │  (CTA)
│ └──────────────────────┘   │
│                             │
│ [56px tab bar]              │
└─────────────────────────────┘

Intervention Cards:
- Progress bar color: green if on track, orange if behind, red if paused
- Metrics: Live sync with wearable if applicable
- Manual logging: optional for non-wearable data
- Actions: Edit goal, pause/resume, complete, delete

Colors:
- Active: Blue accents
- Complete: Green checkmark
- Behind: Orange progress bar
```

---

### **9. PROFILE/SETTINGS SCREEN**

```
Navigation: Profile tab (right)

Layout:
┌─────────────────────────────┐
│ ⬅️  PROFILE                 │
├─────────────────────────────┤
│                             │
│ User Profile                │
│                             │
│ [       Avatar       ]      │  (48x48 circular)
│                             │
│ John Doe                    │  (Name, 18px bold)
│ john@example.com            │  (Email, 12px gray)
│ 45 years old                │  (Age info)
│ Beverly Hills, CA           │  (Location)
│                             │
│ [ EDIT PROFILE ]            │  (Button, secondary)
│                             │
│ Settings                    │  (Section title, 16px)
│                             │
│ Notifications               │  (Setting item)
│ ┌─────────────────────┐    │
│ │ Daily update     [◉]│    │  (Toggle, enabled)
│ │ Milestone alerts [◉]│    │
│ │ AI coach tips    [○]│    │  (Toggle, disabled)
│ │ Wearable alerts  [◉]│    │
│ └─────────────────────┘    │
│                             │
│ Privacy & Data              │  (Section)
│ ┌─────────────────────┐    │
│ │ Share location   [◉]│    │  (For neighborhood map)
│ │ Share age data   [◉]│    │
│ │ Allow analytics  [◉]│    │
│ └─────────────────────┘    │
│                             │
│ App Preferences             │  (Section)
│ ┌─────────────────────┐    │
│ │ Theme: Light        │    │  (Radio button select)
│ │         Dark        │    │
│ │         System      │    │
│ │ Language: English   │    │  (Dropdown)
│ │ Units: Metric       │    │  (kg/cm vs lbs/in)
│ └─────────────────────┘    │
│                             │
│ Connected Accounts          │  (Section)
│ ┌─────────────────────┐    │
│ │ ⌚ Apple Health      │    │  (Connected)
│ │    [  Disconnect ]  │    │
│ │                     │    │
│ │ 📊 Fitbit           │    │
│ │    [  Disconnect ]  │    │
│ └─────────────────────┘    │
│                             │
│ About & Support             │  (Section)
│ ┌─────────────────────┐    │
│ │ Help & FAQ          │    │  (Links)
│ │ Contact Support     │    │
│ │ Privacy Policy      │    │
│ │ Terms of Service    │    │
│ │ Share Feedback      │    │
│ │ Rate on App Store   │    │
│ │ Version 1.0.0       │    │  (Build info)
│ └─────────────────────┘    │
│                             │
│ Account Actions             │  (Section, destructive)
│ ┌─────────────────────┐    │
│ │ [ LOG OUT ]         │    │  (Red/warning color)
│ │ [ DELETE ACCOUNT ]  │    │  (Destructive, needs confirm)
│ └─────────────────────┘    │
│                             │
│ [56px tab bar]              │
└─────────────────────────────┘

Interactions:
- Tap Edit Profile → modal with editable fields
- Toggle switches show confirmation
- Destructive actions (delete) → require confirmation dialog
- Links → open in browser or native screens
```

---

## 🎬 INTERACTION PATTERNS

### **Loading States**

```
Short Loading (< 1 second):
- Content fades in gradually
- No spinner (too fast)
- Natural transition

Medium Loading (1-5 seconds):
- Skeleton screen (placeholder layout)
- OR centered spinner with message
- "Analyzing your data..."
- Progress indicators if available

Long Loading (> 5 seconds):
- Full-page spinner
- Percentage progress bar
- Estimated time remaining
- Cancel button (if applicable)
```

### **Error Handling**

```
Network Error:
- Alert card at top
- "Connection lost. Trying again..."
- Retry button
- Fallback to cached data if available

API Error:
- Modal dialog
- "Something went wrong"
- Error code (for support)
- Retry button + Contact Support link

Validation Error:
- Inline error below input
- Red border on input field
- Helpful message ("Must be 8+ characters")
- Clear validation (turn green on fix)
```

### **Empty States**

```
No Predictions Yet:
- Illustration (friendly, not scary)
- Headline: "Let's get started!"
- Description: "Complete your profile..."
- Primary CTA: "Start Now"

No Wearables Connected:
- Icon + headline
- "No wearables connected"
- Description: "Connect a device to enable..."
- CTA: "Connect Device"

No Interventions Active:
- Illustration
- "No active goals"
- Description: "Start an intervention..."
- CTA: "Browse Recommendations"
```

---

## ♿ ACCESSIBILITY

### **WCAG AA Compliance**

```
✅ Color Contrast:
- Text: Minimum 4.5:1 ratio (normal text)
- Large text: Minimum 3:1 ratio
- Icons: Minimum 3:1 against background
- Test: WebAIM contrast checker

✅ Touch Targets:
- Minimum 48x48px (recommended)
- Minimum 44x44px (acceptable)
- Spacing: 8px minimum between targets
- Test on actual device

✅ Text Sizing:
- Readable at 200% zoom without horizontal scroll
- Minimum 14px body text
- Adjust for small screens (allow zoom)

✅ Focus Indicators:
- Visible focus ring (2px, high contrast)
- Keyboard navigation order logical
- No focus traps (always able to navigate back)

✅ Labels & Descriptions:
- Form fields have visible labels
- Icons have alt text / aria-label
- Buttons: clear label (not just icon)
- Images: descriptive alt text

✅ Motion:
- Respect prefers-reduced-motion
- No auto-playing animations
- Animations can be disabled in settings

✅ Structure:
- Proper heading hierarchy (H1 → H2 → H3)
- Semantic HTML (button, input, etc)
- ARIA labels where needed
- List structure for lists
```

### **Keyboard Navigation**

```
Tab Order:
- Natural left-to-right, top-to-bottom
- Skip navigation for repetitive content
- Modal keeps focus inside

Screen Readers:
- All images have alt text
- Buttons announced with action verbs
- Form errors announced clearly
- Dynamic content updates announced
```

---

## 📐 SPECS SUMMARY

| Element | Spec |
|---------|------|
| Minimum font size | 12px (captions), 14px (body) |
| Maximum line length | 600px (readability) |
| Line height | 1.5× font size minimum |
| Touch target | 48×48px minimum |
| Padding (cards) | 16px |
| Spacing (sections) | 24px vertical, 16px horizontal |
| Corner radius | 12px standard, 8px subtle |
| Color contrast | 4.5:1 minimum (WCAG AA) |
| Animation duration | 200-300ms standard |
| Transition easing | cubic-bezier(0.4, 0, 0.2, 1) |

---

## 🎨 DESIGN DELIVERABLES CHECKLIST

- ✅ Design system (colors, typography, spacing, shadows)
- ✅ Component library (buttons, cards, inputs, navigation)
- ✅ Screen mockups (9 main screens detailed)
- ✅ Interaction patterns (loading, errors, empty states)
- ✅ Accessibility guidelines (WCAG AA)
- ✅ Responsive design rules
- ✅ Animation specifications
- ✅ Typography scale & hierarchy
- ✅ Icon specifications
- ✅ Dark mode (future-proofed)

---

## 📱 HANDOFF TO DEVELOPMENT

**Files to Deliver:**
1. **Figma Design File** (complete with components)
   - Design system library
   - All screens
   - Component documentation
   - Interaction specs
   - Assets exported (SVG, PNG @2x/@3x)

2. **Design Documentation** (this file)
   - Design rationale
   - Usage guidelines
   - Accessibility checklist

3. **Asset Package**
   - Icons (SVG + PNG for each size)
   - Illustrations (for onboarding, empty states)
   - Splash images
   - App store screenshots

4. **Interactive Prototype** (optional)
   - Figma prototype or Framer
   - User flow walkthroughs
   - Interaction demonstrations

5. **Design Tokens** (for implementation)
   - CSS variables
   - Color definitions
   - Typography (font families, sizes, weights)
   - Spacing variables
   - Shadow definitions

---

**Design Document Version:** 1.0  
**Last Updated:** March 16, 2026  
**Status:** Ready for Development  
**Sign-off:** Design Lead, Product Manager, Engineering Lead
